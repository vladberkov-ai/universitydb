"""Single-use SQLite worker. Parent enforces independent hard wall-clock termination."""

import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

from universitydb.contracts import Failure


def run(payload: dict[str, Any]) -> dict[str, Any]:
    started = time.monotonic()
    deadline = started + payload["timeout"]
    denied = False

    def authorize(
        action: int, arg1: str | None, arg2: str | None, database: str | None, trigger: str | None
    ) -> int:
        nonlocal denied
        allowed = action == sqlite3.SQLITE_SELECT
        if action == sqlite3.SQLITE_READ:
            allowed = (
                database in ("main", None)
                and arg1 in payload["tables"]
                and (arg2 in payload["tables"][arg1] or arg2 == "")
            )
        elif action == sqlite3.SQLITE_FUNCTION:
            allowed = bool(arg2 and arg2.lower() in payload["functions"])
        if not allowed:
            denied = True
        return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY

    try:
        with sqlite3.connect(
            Path(payload["path"]).as_uri() + "?mode=ro", uri=True, timeout=0.5
        ) as connection:
            connection.enable_load_extension(False)
            connection.execute("PRAGMA query_only=ON")
            connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 8000)
            connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 65536)
            connection.set_authorizer(authorize)
            connection.set_progress_handler(lambda: int(time.monotonic() >= deadline), 1000)
            cursor = connection.execute(payload["sql"], payload["parameters"])
            rows = [list(row) for row in cursor.fetchmany(101)]
            if len(rows) > 100 or len(json.dumps(rows).encode()) > 65536:
                raise Failure("RESULT_TOO_LARGE", "Database result exceeds limit.")
            if any(isinstance(v, str) and len(v.encode()) > 8192 for row in rows for v in row):
                raise Failure("RESULT_TOO_LARGE", "Database value exceeds limit.")
            columns = [
                {
                    "name": d[0],
                    "type": "integer"
                    if rows and all(type(r[i]) is int for r in rows)
                    else "string",
                }
                for i, d in enumerate(cursor.description or [])
            ]
            if payload.get("result_spec") is not None:
                declared = payload["result_spec"]["columns"]
                if [column["name"] for column in columns] != [c["name"] for c in declared]:
                    raise Failure("RESULT_CONTRACT_INVALID", "Unexpected result column names.")
                columns = [{"name": c["name"], "type": c["type"]} for c in declared]
            return {
                **(
                    {"result_spec": payload["result_spec"], "step_id": payload["step_id"]}
                    if payload.get("result_spec") is not None
                    else {}
                ),
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "truncated": False,
                "elapsed_ms": int((time.monotonic() - started) * 1000),
            }
    except sqlite3.Error as exc:
        if denied:
            raise Failure("UNSAFE_SQL", "SQLite authorization denied this statement.") from exc
        code = getattr(exc, "sqlite_errorcode", 0) & 255
        message = str(exc).lower()
        if code in {
            sqlite3.SQLITE_BUSY,
            sqlite3.SQLITE_LOCKED,
            sqlite3.SQLITE_CANTOPEN,
            sqlite3.SQLITE_IOERR,
        }:
            raise Failure("DB_UNAVAILABLE", "SQLite is unavailable or locked.") from exc
        if code in {
            sqlite3.SQLITE_CORRUPT,
            sqlite3.SQLITE_NOTADB,
            sqlite3.SQLITE_SCHEMA,
            sqlite3.SQLITE_CONSTRAINT,
        }:
            raise Failure("DATA_INCONSISTENT", "SQLite data or schema integrity failed.") from exc
        if code == sqlite3.SQLITE_TOOBIG:
            raise Failure("RESULT_TOO_LARGE", "SQLite result exceeds resource limit.") from exc
        if code == sqlite3.SQLITE_INTERRUPT or time.monotonic() >= deadline:
            raise Failure("SQL_TIMEOUT", "Database cooperative timeout exceeded.") from exc
        if code == sqlite3.SQLITE_ERROR and any(
            detail in message for detail in ("syntax error", "incomplete input", "no such column")
        ):
            raise Failure(
                "SQL_INVALID", "SQLite rejected query syntax or an unknown column."
            ) from exc
        raise Failure(
            "DB_UNAVAILABLE", "SQLite query failed outside the repairable subset."
        ) from exc


def main() -> None:
    try:
        result = run(json.load(sys.stdin))
    except Failure as exc:
        result = {"error": exc.code, "message": exc.message}
    except (OSError, ValueError, KeyError, TypeError):
        result = {"error": "DB_UNAVAILABLE", "message": "Database worker failed safely."}
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
