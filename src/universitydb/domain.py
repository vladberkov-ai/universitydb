"""University registry, catalog resolution, SQL semantics and exact result adaptation.

The core knows neither relation names nor grade units. Registered relational templates
are also the closed domain SQL subset; provider SQL is checked, never substituted.
"""

import re
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, ClassVar

from universitydb.contracts import Failure, PlanProposal, ResultSpec, SQLProposal, Step, bindings
from universitydb.domain_support import (
    clarify,
    column,
    normalize_sql,
    readonly_catalog_connection,
    resolve_entities,
)

TABLES = {
    "Students": ["student_id", "name"],
    "Teachers": ["teacher_id", "name"],
    "Courses": ["course_id", "code", "title"],
    "Semesters": ["semester_id", "starts_on", "ends_on"],
    "Offerings": ["offering_id", "course_id", "teacher_id", "semester_id", "section"],
    "Enrollments": ["student_id", "offering_id", "grade_units"],
}
GROUPS = ("course_id", "student_id", "teacher_id", "offering_id", "semester_id")
FILTERS = ("student_id", "course_id", "teacher_id", "semester_id")
KEY_SQL = {k: ("e." if k == "student_id" else "o.") + k for k in GROUPS}
MEAN_NAMES = ("sum_units", "graded_count", "enrollment_count")
COUNT_EXPRESSIONS = {
    "enrollment_count": "COUNT(*)",
    "graded_count": "COUNT(e.grade_units)",
    "distinct_student_count": "COUNT(DISTINCT e.student_id)",
}
RELATION = " FROM Enrollments e JOIN Offerings o ON e.offering_id = o.offering_id"


def make_spec(metric: str, group: str | None = None) -> ResultSpec:
    """Construct only registered variants; accept_spec is the authority boundary."""
    keys = [group] if group else []
    cols = [column(group, "string" if group == "semester_id" else "integer")] if group else []
    mean = metric in ("grade_mean", "top_course")
    if mean:
        cols += [column(n) for n in MEAN_NAMES]
    elif metric == "enrollment_counts":
        cols += [column(n) for n in COUNT_EXPRESSIONS]
    elif metric == "student_ids":
        keys, cols = ["student_id"], [column("student_id")]
    elif metric == "enrollment_rows":
        keys = ["student_id", "offering_id"]
        cols = [
            column("student_id"),
            column("student_name", "string"),
            column("offering_id"),
            column("course_id"),
            column("course_title", "string"),
            column("teacher_id"),
            column("teacher_name", "string"),
            column("semester_id", "string"),
            column("grade_units", nullable=True),
        ]
    else:
        raise ValueError("Unknown registry family")
    return ResultSpec.model_validate(
        {
            "metric_id": f"u.{metric}.v1",
            "shape": "top"
            if metric == "top_course"
            else "rows"
            if metric in ("student_ids", "enrollment_rows")
            else "aggregate",
            "group_keys": keys,
            "columns": cols,
            "components": {
                "sum": "sum_units" if mean else None,
                "denominator": "graded_count" if mean else None,
                "count": "enrollment_count" if mean or metric == "enrollment_counts" else None,
            },
            "unit": "grade_hundredth"
            if mean or metric == "enrollment_rows"
            else "identifier"
            if metric == "student_ids"
            else "count",
            "scale": 100 if mean or metric == "enrollment_rows" else 1,
        }
    )


SPEC = make_spec("grade_mean")
REGISTRY = [
    make_spec(metric, group)
    for metric in ("grade_mean", "enrollment_counts")
    for group in (None, *GROUPS)
] + [
    make_spec("top_course", "course_id"),
    make_spec("enrollment_rows"),
    make_spec("student_ids"),
]


class University:
    spec = SPEC  # Direct I1 formatter callers only; core uses each accepted Step.
    registry = REGISTRY
    tables = TABLES
    functions: ClassVar[list[str]] = ["sum", "count", "coalesce"]

    def accept_spec(self, spec: ResultSpec) -> None:
        if spec not in self.registry:
            raise Failure(
                "RESULT_CONTRACT_INVALID", "ResultSpec is not an exact registered variant."
            )

    def descriptor(self) -> dict[str, Any]:
        return {
            "version": "I2-I3-1",
            "schema_id": "university-v1",
            "dialect": "sqlite",
            "tables": self.tables,
            "allowed_functions": self.functions,
            "registry": {
                "mean_template": SPEC.model_dump(),
                "groups": list(GROUPS),
                "count_template": make_spec("enrollment_counts").model_dump(),
                "other": [s.model_dump() for s in self.registry[-3:]],
            },
            "policy": "Equal graded enrollments, NULL excluded, all offerings/retakes. Absent filters mean all including semesters. "
            "Mean projections COALESCE(SUM(e.grade_units),0) AS sum_units, COUNT(e.grade_units) AS graded_count, COUNT(*) AS enrollment_count. "
            "Base Enrollments e JOIN Offerings o ON e.offering_id=o.offering_id. Optional equality predicates named student_id/course_id/teacher_id/semester_id; "
            "group keys e.student_id or o.course_id/teacher_id/offering_id/semester_id. For rows GROUP BY key ORDER BY key. "
            "Top returns ALL course components, adapter selects exact maximum ties. student_ids uses SELECT DISTINCT e.student_id ORDER BY e.student_id. "
            "Dependency course_ids/student_ids bind named <ref>_0,<ref>_1 etc in IN clause. Empty ref WHERE 0=1. "
            "Listing adds Students s,Courses c,Teachers t joins on IDs and ordered declared projections; ORDER BY e.offering_id,e.student_id.",
        }

    def catalog(self, path: Path) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {}
        with readonly_catalog_connection(path) as conn:
            for key, table, label in (
                ("student_id", "Students", "name"),
                ("teacher_id", "Teachers", "name"),
                ("course_id", "Courses", "title"),
                ("semester_id", "Semesters", "semester_id"),
            ):
                extra = ",code" if table == "Courses" else ""
                rows = conn.execute(
                    f"SELECT {key},{label}{extra} FROM {table} ORDER BY {key} LIMIT 1001"
                ).fetchall()
                if len(rows) + sum(len(entries) for entries in result.values()) > 1000:
                    raise Failure(
                        "RESOURCE_LIMIT", "Catalog exceeds the supported 1000 entity schema limit."
                    )
                result[key] = [
                    {"id": r[0], "label": r[1], "aliases": list(dict.fromkeys(r[1:]))} for r in rows
                ]
        return result

    def inspect_data(self, path: Path) -> None:
        with readonly_catalog_connection(path) as conn:
            for table, cols in self.tables.items():
                for col in cols:
                    expected = (
                        "text"
                        if col
                        in (
                            "name",
                            "code",
                            "title",
                            "semester_id",
                            "starts_on",
                            "ends_on",
                            "section",
                        )
                        else "integer"
                    )
                    null = " AND " + col + " IS NOT NULL" if col == "grade_units" else ""
                    if conn.execute(
                        f"SELECT 1 FROM {table} WHERE typeof({col}) != ?{null} LIMIT 1", [expected]
                    ).fetchone():
                        raise Failure("DATA_INCONSISTENT", "Invalid domain column type.")
                    if (
                        expected == "text"
                        and conn.execute(
                            f"SELECT 1 FROM {table} WHERE length(trim({col}))=0 LIMIT 1"
                        ).fetchone()
                    ):
                        raise Failure("DATA_INCONSISTENT", "Empty catalog label.")
            if conn.execute(
                "SELECT 1 FROM Enrollments WHERE grade_units NOT BETWEEN 0 AND 10000 LIMIT 1"
            ).fetchone():
                raise Failure("DATA_INCONSISTENT", "Grade outside accepted range.")
            checks = [
                ("Enrollments", "student_id,offering_id"),
                ("Offerings", "offering_id"),
                ("Offerings", "course_id,semester_id,section"),
                ("Courses", "code"),
            ]
            checks += [
                (table, cols[0]) for table, cols in self.tables.items() if table != "Enrollments"
            ]
            for table, key in checks:
                if conn.execute(
                    f"SELECT 1 FROM {table} GROUP BY {key} HAVING COUNT(*)>1 LIMIT 1"
                ).fetchone():
                    raise Failure("DATA_INCONSISTENT", "Duplicate domain identity.")
            if conn.execute("SELECT 1 FROM Semesters WHERE starts_on>ends_on LIMIT 1").fetchone():
                raise Failure("DATA_INCONSISTENT", "Invalid semester interval.")

    def resolve(
        self,
        question: str,
        catalog: dict[str, list[dict[str, Any]]] | None = None,
        choices: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        assigned_fields = {
            key.casefold()
            for key in re.findall(r"\b([A-Za-z_]\w*_id)\s*=", question, re.IGNORECASE)
        }
        if assigned_fields - set(FILTERS):
            raise Failure(
                "INVALID_INPUT", "Unsupported entity filter; no filter is silently ignored."
            )
        choices = choices or {}
        if re.search(
            r"\b(drop|delete|insert|update|attach|pragma|alter|create)\b", question, re.IGNORECASE
        ):
            raise Failure("INVALID_INPUT", "Only read-only University questions are supported.")
        if re.search(
            r"\b(loans?|readers?|books?|borrowed|unreturned)\b", question, re.IGNORECASE
        ) or not re.search(
            r"mean|average|средн|count|how many|сколько|list|show|top|highest|best|покаж|спис|наиб",
            question,
            re.IGNORECASE,
        ):
            raise Failure(
                "INVALID_INPUT",
                "Unsupported University query intent; ask for means, enrollment counts/listing or top courses.",
            )
        scope = resolve_entities(
            question, catalog or {}, choices, FILTERS, {"semester_id": r"\bS\d+\b"}
        )
        if catalog:
            # Recognize a bounded name-bearing shorthand instead of silently turning
            # an unknown requested person into an unfiltered global aggregate.
            group_nouns = "|".join(key.removesuffix("_id") for key in GROUPS)
            named_targets = re.finditer(
                r"\b(?:mean|average)(?:\s+grades?)?\s+(?:for|of)\s+([A-Za-z][\w-]*)"
                r"|\b(?:mean|average)\s+(grades?)\s+(?:grouped\s+by\s+"
                rf"(?:{group_nouns})(?:s|_id)?"
                r"|excluding\s+ungraded\s+enrollments?)\b"
                r"|\b(?:mean|average)\s+grades?\s+([A-Za-z][\w-]*)"
                r"|\b(?:mean|average)\s+([A-Za-z][\w-]*)"
                r"|\b([A-Za-z][\w-]*)['’]s\s+(?:mean|average|grades?)\b",
                question,
                re.IGNORECASE,
            )
            for named in named_targets:
                token = next(group for group in named.groups() if group).casefold()
                semantic = {
                    "all",
                    "across",
                    "over",
                    "grade",
                    "grades",
                    "enrollments",
                    "enrollment",
                    "student",
                    "students",
                    "course",
                    "courses",
                    "teacher",
                    "teachers",
                    "offering",
                    "offerings",
                    "semester",
                    "semesters",
                    "current",
                    "per",
                    "by",
                    "in",
                    "on",
                    "with",
                    "each",
                    "globally",
                    "overall",
                }
                known = {
                    str(label).casefold()
                    for entries in catalog.values()
                    for entry in entries
                    for label in entry.get("aliases", [entry["label"]])
                }
                if token not in semantic and token not in known and not token.endswith("_id"):
                    raise Failure(
                        "INVALID_INPUT",
                        "Unknown name in mean request; use a known catalog name or explicit ID.",
                    )
        if (
            re.search(r"current semester|текущ\w* семестр", question, re.IGNORECASE)
            and "semester_id" not in scope
        ):
            clarify(
                "semester_id",
                [
                    {"value": e["id"], "label": e["label"]}
                    for e in (catalog or {}).get("semester_id", [])
                ],
                "Choose an explicit semester.",
            )
        if re.search(r"how many|\bcount\b|сколько", question, re.IGNORECASE) and not re.search(
            r"enroll|graded|distinct|unique|student|оцен|студент|запис", question, re.IGNORECASE
        ):
            if choices.get("count_object") not in COUNT_EXPRESSIONS:
                clarify(
                    "count_object",
                    [{"value": k, "label": k.replace("_", " ")} for k in COUNT_EXPRESSIONS],
                    "Choose the count object.",
                )
            scope["count_object"] = choices["count_object"]
        return scope

    def clarification_options(
        self, field: str, catalog: dict[str, list[dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        if field == "count_object":
            return [{"value": key, "label": key.replace("_", " ")} for key in COUNT_EXPRESSIONS]
        if field in FILTERS:
            return [
                {"value": entry["id"], "label": entry["label"]} for entry in catalog.get(field, [])
            ]
        raise Failure("PLAN_INVALID", "Clarification field is not registered by this adapter.")

    def validate_plan(self, plan: PlanProposal) -> None:
        if plan.needs_clarification or plan.clarification_field is not None:
            raise Failure("PLAN_INVALID", "Catalog clarification must precede planning.")
        known: dict[str, Step] = {}
        for step in plan.steps:
            self.accept_spec(step.result_spec)
            if step.depends_on or step.result_refs:
                if len(step.result_refs) != 1 or step.depends_on != [step.result_refs[0].from_step]:
                    raise Failure(
                        "PLAN_INVALID",
                        "Dependent University steps require exactly one registered reference edge.",
                    )
                ref = step.result_refs[0]
                upstream = known.get(ref.from_step)
                if upstream is None:
                    raise Failure(
                        "PLAN_INVALID", "A registered dependency must precede its consumer."
                    )
                if step.result_spec == make_spec("student_ids"):
                    source, name, bind_as = (
                        make_spec("top_course", "course_id"),
                        "course_id",
                        "course_ids",
                    )
                elif step.result_spec == make_spec("grade_mean", "student_id"):
                    source, name, bind_as = make_spec("student_ids"), "student_id", "student_ids"
                else:
                    raise Failure(
                        "PLAN_INVALID", "This registered result family has no dependent variant."
                    )
                if (
                    upstream.result_spec != source
                    or ref.column != name
                    or ref.type != "integer"
                    or ref.bind_as != bind_as
                ):
                    raise Failure(
                        "PLAN_INVALID",
                        "Reference does not match an allowed metric/grain/column/type/binding family.",
                    )
            known[step.step_id] = step

    def query(
        self,
        spec: ResultSpec,
        scope: dict[str, Any],
        resolved_refs: dict[str, list[Any]] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Registered SQL template for transparent examples and independent execution tests."""
        self.accept_spec(spec)
        metric = spec.metric_id.split(".")[1]
        group = spec.group_keys[0] if spec.group_keys else None
        prefix = (
            [f"{KEY_SQL[group]} AS {group}"]
            if group and metric not in ("student_ids", "enrollment_rows")
            else []
        )
        relation = RELATION
        if metric in ("grade_mean", "top_course"):
            expressions = prefix + [
                "COALESCE(SUM(e.grade_units),0) AS sum_units",
                "COUNT(e.grade_units) AS graded_count",
                "COUNT(*) AS enrollment_count",
            ]
        elif metric == "enrollment_counts":
            expressions = prefix + [
                f"{expression} AS {name}" for name, expression in COUNT_EXPRESSIONS.items()
            ]
        elif metric == "student_ids":
            expressions = ["DISTINCT e.student_id AS student_id"]
        else:
            expressions = [
                "e.student_id AS student_id",
                "s.name AS student_name",
                "o.offering_id AS offering_id",
                "o.course_id AS course_id",
                "c.title AS course_title",
                "o.teacher_id AS teacher_id",
                "t.name AS teacher_name",
                "o.semester_id AS semester_id",
                "e.grade_units AS grade_units",
            ]
            relation += " JOIN Students s ON e.student_id=s.student_id JOIN Courses c ON o.course_id=c.course_id JOIN Teachers t ON o.teacher_id=t.teacher_id"
        params = {k: v for k, v in scope.items() if k in FILTERS}
        predicates = [f"{KEY_SQL[k]} = :{k}" for k in FILTERS if k in params]
        for name, values in (resolved_refs or {}).items():
            key = {"course_ids": "course_id", "student_ids": "student_id"}.get(name)
            if key is None or any(type(v) is not int for v in values) or len(values) > 100:
                raise Failure("DEPENDENCY_INVALID", "Unsupported domain dependency binding.")
            if values:
                names = [f"{name}_{i}" for i in range(len(values))]
                params.update(zip(names, values, strict=True))
                predicates.append(f"{KEY_SQL[key]} IN ({','.join(':' + n for n in names)})")
            else:
                predicates.append("0 = 1")
        sql = "SELECT " + ", ".join(expressions) + relation
        if predicates:
            sql += " WHERE " + " AND ".join(predicates)
        if group and metric not in ("student_ids", "enrollment_rows"):
            sql += f" GROUP BY {KEY_SQL[group]} ORDER BY {KEY_SQL[group]}"
        elif metric == "student_ids":
            sql += " ORDER BY e.student_id"
        elif metric == "enrollment_rows":
            sql += " ORDER BY e.offering_id, e.student_id"
        return sql, params

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
            or proposal.result_kind != ("aggregate" if spec.shape == "aggregate" else "rows")
        ):
            raise Failure(
                "RESULT_CONTRACT_INVALID", "SQL proposal does not match accepted ResultSpec."
            )
        expected, params = self.query(spec, scope, resolved_refs)
        if bindings(proposal.parameters) != params:
            raise Failure(
                "PROVIDER_INVALID_OUTPUT",
                "Bindings must equal resolved scope and dependency values.",
            )
        actual_tree = normalize_sql(proposal.sql, self.tables)
        expected_tree = normalize_sql(expected, self.tables)
        if actual_tree != expected_tree:
            raise Failure(
                "UNSAFE_SQL",
                "SQL does not match registered projections/joins/grouping and four exact optional bound filters.",
            )
        return params

    def adapt_result(
        self, rows: list[list[Any]], spec: ResultSpec, scope: dict[str, Any]
    ) -> dict[str, Any]:
        self.accept_spec(spec)
        for row in rows:
            if len(row) != len(spec.columns):
                raise Failure(
                    "RESULT_CONTRACT_INVALID", "Result width differs from registered schema."
                )
            for value, col in zip(row, spec.columns, strict=True):
                expected = {"integer": int, "string": str, "boolean": bool}[col.type]
                if not (value is None and col.nullable) and type(value) is not expected:
                    raise Failure(
                        "RESULT_CONTRACT_INVALID", "Result value differs from declared type."
                    )
        if spec.shape == "aggregate" and not spec.group_keys and len(rows) != 1:
            raise Failure("RESULT_CONTRACT_INVALID", "Expected exactly one aggregate row.")
        metric = spec.metric_id.split(".")[1]
        mean = metric in ("grade_mean", "top_course")
        if spec.group_keys:
            positions = [[c.name for c in spec.columns].index(k) for k in spec.group_keys]
            keys = [tuple(row[i] for i in positions) for row in rows]
            if len(set(keys)) != len(keys):
                raise Failure("DATA_INCONSISTENT", "Duplicate result grouping identities.")
        selected = [list(r) for r in rows]
        if mean:
            for row in rows:
                total, graded, count = row[-3:]
                if not (0 <= graded <= count and 0 <= total <= 10000 * graded):
                    raise Failure("DATA_INCONSISTENT", "Grade/count components are inconsistent.")
            if metric == "top_course":
                graded_rows = [r for r in selected if r[-2]]
                maximum = max((Fraction(r[-3], r[-2]) for r in graded_rows), default=None)
                selected = sorted(
                    [r for r in graded_rows if Fraction(r[-3], r[-2]) == maximum],
                    key=lambda r: r[0],
                )
            adapted = [
                r[:-3]
                + [
                    str(
                        (Decimal(r[-3]) / (100 * r[-2])).quantize(
                            Decimal("0.01"), rounding=ROUND_HALF_UP
                        )
                    )
                    if r[-2]
                    else None,
                    r[-2],
                    r[-1],
                ]
                for r in selected
            ]
            cols = [{"name": c.name, "type": c.type} for c in spec.columns[:-3]] + [
                {"name": "average", "type": "decimal"},
                {"name": "graded_count", "type": "integer"},
                {"name": "enrollment_count", "type": "integer"},
            ]
        else:
            if metric == "enrollment_counts" and any(
                not (0 <= r[-2] <= r[-3] and 0 <= r[-1] <= r[-3]) for r in rows
            ):
                raise Failure(
                    "DATA_INCONSISTENT", "Counts must be nonnegative and bounded by enrollments."
                )
            if metric == "enrollment_rows" and any(
                r[-1] is not None and not 0 <= r[-1] <= 10000 for r in rows
            ):
                raise Failure("DATA_INCONSISTENT", "Listing grade out of range.")
            adapted, cols = selected, [{"name": c.name, "type": c.type} for c in spec.columns]
        label = "; ".join(
            f"{key}={scope[key]}" if key in scope else f"{key}=all" for key in FILTERS
        )
        reason = "no_rows" if not selected else None
        row_reasons = (
            [None if r[-2] else "no_rows" if r[-1] == 0 else "no_grades" for r in selected]
            if mean
            else [None] * len(selected)
        )
        if mean and not spec.group_keys:
            reason = row_reasons[0]
        text = f"{label}: " + (
            f"mean {adapted[0][-3] if adapted[0][-3] is not None else 'undefined'} ({selected[0][-2]} grades; {selected[0][-1]} enrollments)."
            if mean and not spec.group_keys
            else f"{metric}: {len(selected)} rows."
        )
        return {
            "answer": {
                "text": text,
                "columns": cols,
                "rows": adapted,
                "scope": label,
                "empty_reason": reason,
                "row_reasons": row_reasons,
                "truncated": False,
            },
            "dependency_rows": selected,
        }

    def answer(self, rows: list[list[Any]], scope: dict[str, Any]) -> dict[str, Any]:
        return self.adapt_result(rows, SPEC, scope)["answer"]  # type: ignore[no-any-return]
