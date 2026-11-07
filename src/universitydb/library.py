"""Library adapter: open loans per reader, including zero; no grade scaling."""

import re
from pathlib import Path
from typing import Any, ClassVar

from universitydb.contracts import Failure, PlanProposal, ResultSpec, SQLProposal, Step, bindings
from universitydb.domain_support import (
    column,
    normalize_sql,
    readonly_catalog_connection,
    resolve_entities,
)

SPEC = ResultSpec.model_validate(
    {
        "metric_id": "l.open_count.v1",
        "shape": "aggregate",
        "group_keys": ["reader_id"],
        "columns": [column("reader_id"), column("name", "string"), column("open_count")],
        "components": {"sum": None, "denominator": None, "count": "open_count"},
        "unit": "count",
        "scale": 1,
    }
)


class Library:
    tables: ClassVar[dict[str, list[str]]] = {
        "Readers": ["reader_id", "name"],
        "Books": ["book_id", "title"],
        "Loans": ["loan_id", "reader_id", "book_id", "returned"],
    }
    functions: ClassVar[list[str]] = ["count"]
    registry: ClassVar[list[ResultSpec]] = [SPEC]

    def accept_spec(self, spec: ResultSpec) -> None:
        if spec != SPEC:
            raise Failure("RESULT_CONTRACT_INVALID", "Unregistered Library ResultSpec.")

    def descriptor(self) -> dict[str, Any]:
        return {
            "version": "I2-I3-1",
            "schema_id": "library-v1",
            "dialect": "sqlite",
            "tables": self.tables,
            "allowed_functions": self.functions,
            "registry": [SPEC.model_dump()],
            "policy": "Open means returned=0. Count each reader including zero. SQL template: "
            + self.query(SPEC, {})[0]
            + ". Optional reader_id bound WHERE r.reader_id=:reader_id before GROUP BY.",
        }

    def catalog(self, path: Path) -> dict[str, list[dict[str, Any]]]:
        with readonly_catalog_connection(path) as conn:
            rows = conn.execute(
                "SELECT reader_id,name FROM Readers ORDER BY reader_id LIMIT 1001"
            ).fetchall()
            if len(rows) > 1000:
                raise Failure(
                    "RESOURCE_LIMIT", "Catalog exceeds the supported 1000 entity schema limit."
                )
            return {"reader_id": [{"id": r[0], "label": r[1]} for r in rows]}

    def inspect_data(self, path: Path) -> None:
        with readonly_catalog_connection(path) as conn:
            for table, columns in self.tables.items():
                for col in columns:
                    expected = "text" if col in ("name", "title") else "integer"
                    if conn.execute(
                        f"SELECT 1 FROM {table} WHERE typeof({col}) != ? LIMIT 1", [expected]
                    ).fetchone():
                        raise Failure("DATA_INCONSISTENT", "Invalid Library column type.")
                    if (
                        expected == "text"
                        and conn.execute(
                            f"SELECT 1 FROM {table} WHERE length(trim({col}))=0 LIMIT 1"
                        ).fetchone()
                    ):
                        raise Failure("DATA_INCONSISTENT", "Empty Library label.")
                if conn.execute(
                    f"SELECT 1 FROM {table} GROUP BY {columns[0]} HAVING COUNT(*)>1 LIMIT 1"
                ).fetchone():
                    raise Failure("DATA_INCONSISTENT", "Duplicate Library identity.")
            if conn.execute("SELECT 1 FROM Loans WHERE returned NOT IN (0,1) LIMIT 1").fetchone():
                raise Failure("DATA_INCONSISTENT", "Invalid returned flag.")

    def resolve(
        self,
        question: str,
        catalog: dict[str, list[dict[str, Any]]] | None = None,
        choices: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        assigned_fields = set(re.findall(r"\b([A-Za-z_]\w*_id)\s*=", question))
        if assigned_fields - {"reader_id"}:
            raise Failure(
                "INVALID_INPUT", "Unsupported entity filter; no filter is silently ignored."
            )
        if re.search(
            r"\b(drop|delete|insert|update|attach|pragma|alter|create|grade|grades|student|students|course|courses|teacher|teachers|semester|mean|average)\b",
            question,
            re.IGNORECASE,
        ) or not re.search(r"\b(loans?|borrowed|unreturned)\b", question, re.IGNORECASE):
            raise Failure(
                "INVALID_INPUT", "Library supports read-only open-loan counts by reader only."
            )
        if not re.search(r"\b(open|unreturned)\b|not returned", question, re.IGNORECASE):
            raise Failure(
                "INVALID_INPUT",
                "Specify open/unreturned loans; other Library metrics are unsupported.",
            )
        if catalog:
            named = re.search(r"\b(?i:loans?)\s+(?:(?i:for)\s+)?([A-Z][\w-]*)", question)
            known = {str(entry["label"]).casefold() for entry in catalog.get("reader_id", [])}
            if named and named.group(1).casefold() not in known | {
                "per",
                "by",
                "for",
                "all",
                "reader",
                "readers",
                "reader_id",
                "count",
            }:
                raise Failure(
                    "INVALID_INPUT", "Unknown reader name; use a catalog name or reader_id."
                )
        return resolve_entities(question, catalog or {}, choices or {}, ("reader_id",))

    def clarification_options(
        self, field: str, catalog: dict[str, list[dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        if field != "reader_id":
            raise Failure("PLAN_INVALID", "Clarification field is not registered by this adapter.")
        return [{"value": entry["id"], "label": entry["label"]} for entry in catalog.get(field, [])]

    def validate_plan(self, plan: PlanProposal) -> None:
        if plan.needs_clarification or plan.clarification_field is not None:
            raise Failure("PLAN_INVALID", "Resolve catalog ambiguity before planning.")
        for step in plan.steps:
            self.accept_spec(step.result_spec)
            if step.result_refs:
                raise Failure("PLAN_INVALID", "Library open-count has no registered dependencies.")

    def query(
        self,
        spec: ResultSpec,
        scope: dict[str, Any],
        resolved_refs: dict[str, list[Any]] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        self.accept_spec(spec)
        if resolved_refs:
            raise Failure("DEPENDENCY_INVALID", "Library metric has no dependency parameters.")
        params = {k: v for k, v in scope.items() if k == "reader_id"}
        sql = "SELECT r.reader_id AS reader_id, r.name AS name, COUNT(l.loan_id) AS open_count FROM Readers r LEFT JOIN Loans l ON r.reader_id=l.reader_id AND l.returned=0"
        if params:
            sql += " WHERE r.reader_id=:reader_id"
        return sql + " GROUP BY r.reader_id,r.name ORDER BY r.reader_id", params

    def validate_sql(
        self,
        proposal: SQLProposal,
        scope: dict[str, Any],
        step: Step | None = None,
        resolved_refs: dict[str, list[Any]] | None = None,
    ) -> dict[str, Any]:
        spec = step.result_spec if step else SPEC
        self.accept_spec(spec)
        if (
            proposal.result_spec != spec
            or proposal.expected_columns != [c.name for c in spec.columns]
            or proposal.result_kind != "aggregate"
        ):
            raise Failure(
                "RESULT_CONTRACT_INVALID", "Library SQL metadata differs from accepted spec."
            )
        sql, params = self.query(spec, scope, resolved_refs)
        if bindings(proposal.parameters) != params:
            raise Failure("PROVIDER_INVALID_OUTPUT", "Library bindings differ from resolved scope.")
        if normalize_sql(proposal.sql, self.tables) != normalize_sql(sql, self.tables):
            raise Failure(
                "UNSAFE_SQL", "SQL differs from registered open-loan count including zero."
            )
        return params

    def adapt_result(
        self, rows: list[list[Any]], spec: ResultSpec, scope: dict[str, Any]
    ) -> dict[str, Any]:
        self.accept_spec(spec)
        ids = set()
        for row in rows:
            if (
                len(row) != 3
                or type(row[0]) is not int
                or type(row[1]) is not str
                or type(row[2]) is not int
            ):
                raise Failure(
                    "RESULT_CONTRACT_INVALID", "Library rows must match declared nonnull types."
                )
            if row[0] in ids or row[2] < 0 or not row[1].strip():
                raise Failure("DATA_INCONSISTENT", "Invalid Library count or duplicate reader.")
            ids.add(row[0])
        label = f"reader_id={scope['reader_id']}" if "reader_id" in scope else "reader_id=all"
        return {
            "answer": {
                "text": f"{label}: open loans {rows}.",
                "columns": [{"name": c.name, "type": c.type} for c in spec.columns],
                "rows": rows,
                "scope": label,
                "empty_reason": None if rows else "no_rows",
                "truncated": False,
            },
            "dependency_rows": rows,
        }
