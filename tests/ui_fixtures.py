"""Explicit offline UI proposals, never normal provider fallback or result oracle."""

from typing import Any

from universitydb.contracts import ResultSpec


def step(
    spec: ResultSpec, step_id: str = "query", refs: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    refs = refs or []
    return {
        "step_id": step_id,
        "depends_on": sorted({r["from_step"] for r in refs}),
        "purpose": "Offline injected UI scenario",
        "result_refs": refs,
        "result_spec": spec.model_dump(),
    }


def plan(*steps: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "1",
        "steps": list(steps),
        "needs_clarification": False,
        "clarification_field": None,
    }


def proposal(
    domain: Any,
    spec: ResultSpec,
    scope: dict[str, Any],
    step_id: str = "query",
    refs: dict[str, list[Any]] | None = None,
) -> dict[str, Any]:
    # This supplies SQL proposals ONLY. The actual read-only SQLite computes rows;
    # test expected values are independently frozen before this helper existed.
    sql, parameters = domain.query(spec, scope, refs)
    return {
        "version": "1",
        "step_id": step_id,
        "result_spec": spec.model_dump(),
        "sql": sql,
        "parameters": [
            {
                "name": name,
                "type": "text" if isinstance(value, str) else "integer",
                "integer_value": None if isinstance(value, str) else value,
                "text_value": value if isinstance(value, str) else None,
            }
            for name, value in parameters.items()
        ],
        "expected_columns": [column.name for column in spec.columns],
        "result_kind": "rows" if spec.shape in ("rows", "top") else "aggregate",
        "explanation": "Offline injected proposal; database result is not supplied",
    }
