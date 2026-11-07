"""SQLite provisioning and a read-only subprocess execution boundary."""

import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

from universitydb.contracts import Failure, ResultSpec, validate_result


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initialize(path: Path, resources: Path) -> None:
    if path.exists():
        raise Failure("DB_UNAVAILABLE", "Refusing to overwrite an existing database.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.executescript((resources / "schema.sql").read_text())
        connection.executescript((resources / "seed.sql").read_text())
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise Failure("DATA_INCONSISTENT", "Foreign key integrity failed.")


def inspect(path: Path, tables: dict[str, list[str]]) -> dict[str, Any]:
    """Trusted startup scan, separate from generated SQL request attempts."""
    try:
        with sqlite3.connect(
            path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.5
        ) as connection:
            if connection.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                raise Failure("DATA_INCONSISTENT", "Database integrity failed.")
            if connection.execute("PRAGMA foreign_key_check").fetchall():
                raise Failure("DATA_INCONSISTENT", "Database foreign keys failed.")
            found = {
                r[0]
                for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            if found != set(tables):
                raise Failure("DATA_INCONSISTENT", "Database table set does not match descriptor.")
            for name, columns in tables.items():
                if not name.isidentifier():
                    raise Failure("DATA_INCONSISTENT", "Invalid descriptor identifier.")
                actual = [r[1] for r in connection.execute(f'PRAGMA table_info("{name}")')]
                if actual != columns:
                    raise Failure("DATA_INCONSISTENT", "Database columns do not match descriptor.")
    except sqlite3.Error as exc:
        raise Failure("DB_UNAVAILABLE", "Database cannot be opened or inspected.") from exc
    return {"db_sha256": file_hash(path), "sqlite_version": sqlite3.sqlite_version}


def execute(
    path: Path,
    sql: str,
    parameters: dict[str, Any],
    tables: dict[str, list[str]],
    functions: list[str],
    *,
    timeout: float = 2.0,
    watchdog: float = 3.0,
    expected_hash: str | None = None,
    result_spec: ResultSpec | None = None,
    step_id: str = "query",
) -> dict[str, Any]:
    if not path.is_file():
        raise Failure("DB_UNAVAILABLE", "Database is missing.")
    if expected_hash is not None and file_hash(path) != expected_hash:
        raise Failure("DATA_INCONSISTENT", "Database changed after startup.")
    payload = {
        "path": str(path.resolve()),
        "sql": sql,
        "parameters": parameters,
        "tables": tables,
        "functions": functions,
        "timeout": timeout,
        "result_spec": result_spec.model_dump() if result_spec is not None else None,
        "step_id": step_id,
    }
    try:
        with subprocess.Popen(
            [sys.executable, "-m", "universitydb.db_worker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        ) as worker:
            try:
                output, _ = worker.communicate(json.dumps(payload), timeout=watchdog)
            except subprocess.TimeoutExpired as exc:
                worker.kill()
                worker.communicate()
                raise Failure(
                    "SQL_TIMEOUT", "Database worker exceeded watchdog and was terminated."
                ) from exc
            if worker.returncode != 0:
                raise Failure("DB_UNAVAILABLE", "Database worker failed.")
    except OSError as exc:
        raise Failure("DB_UNAVAILABLE", "Database worker could not start.") from exc
    try:
        result: dict[str, Any] = json.loads(output)
    except (ValueError, TypeError) as exc:
        raise Failure("DB_UNAVAILABLE", "Invalid database worker response.") from exc
    if "error" in result:
        raise Failure(result["error"], result["message"])
    if result_spec is not None:
        validate_result(result, result_spec)
    return result
