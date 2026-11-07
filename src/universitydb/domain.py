"""University-specific S6 vocabulary, SQL subset, and exact grade arithmetic."""

import re
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, ClassVar

import sqlglot
from sqlglot import exp

from universitydb.contracts import Failure, PlanProposal, ResultSpec, SQLProposal, bindings

SPEC = ResultSpec.model_validate(
    {
        "metric_id": "u.grade_mean.v1",
        "shape": "aggregate",
        "group_keys": [],
        "columns": [
            {"name": n, "type": "integer", "nullable": False}
            for n in ("sum_units", "graded_count", "enrollment_count")
        ],
        "components": {
            "sum": "sum_units",
            "denominator": "graded_count",
            "count": "enrollment_count",
        },
        "unit": "grade_hundredth",
        "scale": 100,
    }
)
TABLES = {
    "Students": ["student_id", "name"],
    "Teachers": ["teacher_id", "name"],
    "Courses": ["course_id", "code", "title"],
    "Semesters": ["semester_id", "starts_on", "ends_on"],
    "Offerings": ["offering_id", "course_id", "teacher_id", "semester_id", "section"],
    "Enrollments": ["student_id", "offering_id", "grade_units"],
}


class University:
    spec = SPEC
    tables = TABLES
    functions: ClassVar[list[str]] = ["sum", "count", "coalesce"]

    def resolve(self, question: str) -> dict[str, int | str]:
        if not re.search(r"средн|average|mean", question, re.IGNORECASE):
            raise Failure("INVALID_INPUT", "I1 supports only an explicit four-filter grade mean.")
        scope: dict[str, int | str] = {}
        for name in ("student_id", "course_id", "teacher_id"):
            hits = re.findall(rf"\b{name}\s*=\s*(\d+)\b", question, re.IGNORECASE)
            if len(hits) != 1:
                raise Failure(
                    "INVALID_INPUT", "Provide each of student_id, course_id, teacher_id once."
                )
            scope[name] = int(hits[0])
        semesters = re.findall(r"\bS\d+\b", question, re.IGNORECASE)
        if len(semesters) != 1:
            raise Failure(
                "INVALID_INPUT", "Provide exactly one explicit semester ID (for example S1)."
            )
        scope["semester_id"] = semesters[0].upper()
        return scope

    def descriptor(self) -> dict[str, Any]:
        return {
            "version": "I1-1",
            "schema_id": "university-v1",
            "dialect": "sqlite",
            "tables": self.tables,
            "allowed_functions": self.functions,
            "result_spec": self.spec.model_dump(),
            "policy": "Explicit four-filter scalar enrollment mean; NULL excluded, units/100. "
            "Join Enrollments e to Offerings o on offering_id only; no other tables.",
        }

    def validate_plan(self, plan: PlanProposal) -> None:
        step = plan.steps[0]
        if (
            plan.needs_clarification
            or plan.clarification_field is not None
            or step.depends_on
            or step.result_refs
            or step.result_spec != self.spec
        ):
            raise Failure(
                "PLAN_INVALID", "Only one independent scalar grade-mean step is supported."
            )

    def validate_sql(self, proposal: SQLProposal, scope: dict[str, int | str]) -> dict[str, Any]:
        if (
            proposal.result_spec != self.spec
            or proposal.result_kind != "aggregate"
            or proposal.expected_columns != [c.name for c in self.spec.columns]
        ):
            raise Failure(
                "RESULT_CONTRACT_INVALID", "SQL proposal does not match accepted ResultSpec."
            )
        if len(proposal.sql.encode()) > 8000:
            raise Failure("RESOURCE_LIMIT", "SQL exceeds byte limit.")
        params = bindings(proposal.parameters)
        if params != scope:
            raise Failure(
                "PROVIDER_INVALID_OUTPUT", "Bindings must equal the explicit resolved scope."
            )
        try:
            statements = sqlglot.parse(proposal.sql, read="sqlite")
        except sqlglot.errors.ParseError as exc:
            raise Failure("SQL_INVALID", "SQL could not be parsed.") from exc
        if len(statements) != 1 or not isinstance(statements[0], exp.Select):
            raise Failure("UNSAFE_SQL", "Exactly one supported SELECT is required.")
        tree = statements[0]
        if any(node.comments for node in tree.walk()):
            raise Failure("UNSAFE_SQL", "SQL comments are outside the supported subset.")
        allowed_args = {"expressions", "from_", "joins", "where"}
        if any(value for key, value in tree.args.items() if key not in allowed_args):
            raise Failure("UNSAFE_SQL", "Unsupported SELECT clause.")
        tables = list(tree.find_all(exp.Table))
        if len(tables) != 2 or {t.name for t in tables} != {"Enrollments", "Offerings"}:
            raise Failure(
                "UNSAFE_SQL", "Only the scoped enrollment/offering relation is supported."
            )
        if any(
            t.db or t.catalog or any(v for k, v in t.args.items() if k not in {"this", "alias"})
            for t in tables
        ):
            raise Failure("UNSAFE_SQL", "Qualified database/catalog names are unsupported.")
        aliases = {t.alias_or_name: "e" if t.name == "Enrollments" else "o" for t in tables}
        if len(aliases) != 2:
            raise Failure("UNSAFE_SQL", "Distinct relation aliases required.")
        for column in tree.find_all(exp.Column):
            if column.db or column.catalog or column.table not in aliases:
                raise Failure("UNSAFE_SQL", "All columns must use explicit relation aliases.")
            column.set("table", exp.to_identifier(aliases[column.table]))
        source = tree.args.get("from_")
        joins = tree.args.get("joins", [])
        if not source or source.this.name != "Enrollments" or len(joins) != 1:
            raise Failure("UNSAFE_SQL", "Unsupported relation or join count.")
        join = joins[0]
        if (
            join.side
            or join.kind not in ("", "INNER")
            or join.this.name != "Offerings"
            or any(v for k, v in join.args.items() if k not in {"this", "on", "kind"})
        ):
            raise Failure("UNSAFE_SQL", "Only an inner enrollment/offering join is supported.")

        def canon(node: Any) -> str:
            return str(node.sql(dialect="sqlite")).lower()

        if canon(join.args.get("on", exp.Null())) not in (
            "e.offering_id = o.offering_id",
            "o.offering_id = e.offering_id",
        ):
            raise Failure("UNSAFE_SQL", "Join must match offering primary/foreign key.")
        projections = [canon(p) for p in tree.expressions]
        if projections != [
            "coalesce(sum(e.grade_units), 0) as sum_units",
            "count(e.grade_units) as graded_count",
            "count(*) as enrollment_count",
        ]:
            raise Failure("UNSAFE_SQL", "Unsupported aggregate expressions.")
        where = tree.args.get("where")
        predicates = (
            list(where.this.flatten())
            if where and isinstance(where.this, exp.And)
            else ([where.this] if where else [])
        )
        expected = {
            "e.student_id = :student_id",
            "o.course_id = :course_id",
            "o.teacher_id = :teacher_id",
            "o.semester_id = :semester_id",
        }
        if len(predicates) != 4 or {canon(p) for p in predicates} != expected:
            raise Failure("UNSAFE_SQL", "All four exact bound equality filters are required.")
        return params

    def answer(self, rows: list[list[Any]], scope: dict[str, int | str]) -> dict[str, Any]:
        if len(rows) != 1 or len(rows[0]) != 3 or any(type(v) is not int for v in rows[0]):
            raise Failure(
                "RESULT_CONTRACT_INVALID", "Expected one row of three integer components."
            )
        total, graded, count = rows[0]
        if not (0 <= graded <= count and 0 <= total <= 10000 * graded):
            raise Failure("DATA_INCONSISTENT", "Grade/count components are inconsistent.")
        average = (
            str((Decimal(total) / (100 * graded)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            if graded
            else None
        )
        label = "; ".join(f"{key}={value}" for key, value in scope.items())
        return {
            "text": f"{label}: средняя {average if graded else 'не определена'} "
            f"({graded} оценок; {count} записей).",
            "columns": [
                {"name": "average", "type": "decimal"},
                {"name": "graded_count", "type": "integer"},
                {"name": "enrollment_count", "type": "integer"},
            ],
            "rows": [[average, graded, count]],
            "scope": label,
            "empty_reason": None if graded else ("no_rows" if count == 0 else "no_grades"),
            "truncated": False,
        }
