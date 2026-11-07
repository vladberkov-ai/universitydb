"""Closed wire types for the bounded domain adapters and typed dependent steps."""

import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Failure(Exception):
    def __init__(self, code: str, message: str, *, details: dict[str, Any] | None = None) -> None:
        self.details = details or {}
        self.code = code
        self.message = message
        super().__init__(message)


class Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ResultColumn(Closed):
    name: str
    type: Literal["integer", "string", "boolean"]
    nullable: bool


class Components(Closed):
    sum: str | None
    denominator: str | None
    count: str | None


class ResultSpec(Closed):
    metric_id: str
    shape: Literal["aggregate", "rows", "top"]
    group_keys: list[str]
    columns: list[ResultColumn]
    components: Components
    unit: str
    scale: int


class Reference(Closed):
    from_step: str
    column: str
    type: Literal["integer", "string", "boolean"]
    bind_as: str


class Step(Closed):
    step_id: str = Field(min_length=1, max_length=128)
    depends_on: list[str]
    purpose: str = Field(max_length=2000)
    result_refs: list[Reference]
    result_spec: ResultSpec


class PlanProposal(Closed):
    version: Literal["1"]
    steps: list[Step] = Field(min_length=1, max_length=3)
    needs_clarification: bool
    clarification_field: str | None


class Binding(Closed):
    name: str = Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
    type: Literal["integer", "text", "null"]
    integer_value: int | None
    text_value: str | None


class SQLProposal(Closed):
    version: Literal["1"]
    step_id: str = Field(min_length=1, max_length=128)
    result_spec: ResultSpec
    sql: str = Field(min_length=1, max_length=8000)
    parameters: list[Binding] = Field(max_length=100)
    expected_columns: list[str]
    result_kind: Literal["rows", "aggregate"]
    explanation: str = Field(max_length=1000)


def bindings(values: list[Binding]) -> dict[str, int | str | None]:
    if len(str([b.model_dump() for b in values]).encode()) > 8192:
        raise Failure("RESOURCE_LIMIT", "Bindings exceed byte limit.")
    result: dict[str, int | str | None] = {}
    for value in values:
        if value.name in result:
            raise Failure("PROVIDER_INVALID_OUTPUT", "Duplicate binding.")
        if value.type == "integer" and value.integer_value is not None and value.text_value is None:
            result[value.name] = value.integer_value
        elif value.type == "text" and value.text_value is not None and value.integer_value is None:
            if len(value.text_value.encode()) > 2000:
                raise Failure("RESOURCE_LIMIT", "Binding text exceeds byte limit.")
            result[value.name] = value.text_value
        elif value.type == "null" and value.integer_value is None and value.text_value is None:
            result[value.name] = None
        else:
            raise Failure("PROVIDER_INVALID_OUTPUT", "Binding type/value mismatch.")
    return result


def validate_dag(plan: PlanProposal) -> None:
    """Validate static references without requiring future execution results."""
    known: dict[str, Step] = {}
    for step in plan.steps:
        if step.step_id in known:
            raise Failure("PLAN_INVALID", "Duplicate step identity.")
        if len(set(step.depends_on)) != len(step.depends_on):
            raise Failure("PLAN_INVALID", "Duplicate dependency.")
        if any(dependency not in known for dependency in step.depends_on):
            raise Failure("PLAN_INVALID", "Missing or forward dependency.")
        if set(step.depends_on) != {ref.from_step for ref in step.result_refs}:
            raise Failure("PLAN_INVALID", "Dependencies must exactly match result references.")
        names: set[str] = set()
        for ref in step.result_refs:
            if not ref.bind_as.isidentifier() or ref.bind_as in names:
                raise Failure("PLAN_INVALID", "Invalid or duplicate reference binding.")
            names.add(ref.bind_as)
            source = known[ref.from_step]
            columns = {column.name: column for column in source.result_spec.columns}
            column = columns.get(ref.column)
            if column is None or column.type != ref.type or column.nullable:
                raise Failure("PLAN_INVALID", "Reference column/type is not approved.")
        known[step.step_id] = step


def _typed(value: Any, kind: str) -> bool:
    return type(value) is {"integer": int, "string": str, "boolean": bool}[kind]


def validate_result(result: dict[str, Any], spec: ResultSpec) -> None:
    """Use accepted metadata, never first-row inference, for NULL/empty typing."""
    if result.get("truncated") is not False:
        raise Failure("RESULT_TOO_LARGE", "Truncated result is not usable.")
    if result.get("result_spec") != spec.model_dump():
        raise Failure("RESULT_CONTRACT_INVALID", "Copied result spec differs from accepted spec.")
    step_id = result.get("step_id")
    if not isinstance(step_id, str) or not 1 <= len(step_id) <= 128:
        raise Failure("RESULT_CONTRACT_INVALID", "Invalid result step identity.")
    if type(result.get("elapsed_ms")) is not int or result["elapsed_ms"] < 0:
        raise Failure("RESULT_CONTRACT_INVALID", "Invalid result elapsed time.")
    expected = [{"name": column.name, "type": column.type} for column in spec.columns]
    if result.get("columns") != expected:
        raise Failure("RESULT_CONTRACT_INVALID", "Result columns differ from accepted spec.")
    rows = result.get("rows")
    if not isinstance(rows, list) or len(rows) > 100:
        raise Failure("RESULT_TOO_LARGE", "Invalid or oversized result rows.")
    if len(json.dumps(rows).encode()) > 65536:
        raise Failure("RESULT_TOO_LARGE", "Result exceeds byte limit.")
    if type(result.get("row_count")) is not int or result["row_count"] != len(rows):
        raise Failure("RESULT_CONTRACT_INVALID", "Result count differs from rows.")
    for row in rows:
        if not isinstance(row, list) or len(row) != len(spec.columns):
            raise Failure("RESULT_CONTRACT_INVALID", "Result row width differs from accepted spec.")
        for value, column in zip(row, spec.columns, strict=True):
            if value is None and column.nullable:
                continue
            if not _typed(value, column.type):
                raise Failure(
                    "RESULT_CONTRACT_INVALID", "Result value has incorrect declared type."
                )


def materialize_refs(
    step: Step,
    completed: dict[str, dict[str, Any]],
    trusted_specs: dict[str, ResultSpec] | None = None,
) -> dict[str, list[Any]]:
    """Materialize typed values from actual completed results, not SQL fragments."""
    resolved: dict[str, list[Any]] = {}
    for ref in step.result_refs:
        result = completed.get(ref.from_step)
        if result is None:
            raise Failure("DEPENDENCY_INVALID", "Missing completed dependency result.")
        try:
            spec = ResultSpec.model_validate(result["result_spec"])
            index = [column.name for column in spec.columns].index(ref.column)
        except (ValueError, KeyError) as exc:
            raise Failure("DEPENDENCY_INVALID", "Dependency schema is invalid.") from exc
        column = spec.columns[index]
        if result.get("truncated") is not False:
            raise Failure("RESULT_TOO_LARGE", "Dependency is truncated.")
        if column.type != ref.type or column.nullable:
            raise Failure("DEPENDENCY_INVALID", "Dependency type is invalid.")
        if trusted_specs is not None:
            accepted = trusted_specs.get(ref.from_step)
            if accepted is None or accepted != spec or result.get("step_id") != ref.from_step:
                raise Failure(
                    "DEPENDENCY_INVALID", "Dependency spec/identity differs from accepted step."
                )
            try:
                validate_result(result, accepted)
            except Failure as exc:
                if exc.code == "RESULT_TOO_LARGE":
                    raise
                raise Failure(
                    "DEPENDENCY_INVALID", "Dependency metadata or values invalid."
                ) from exc
        rows = result.get("rows")
        if not isinstance(rows, list) or len(rows) > 100:
            raise Failure("RESULT_TOO_LARGE", "Dependency exceeds value limit.")
        if any(not isinstance(row, list) or len(row) != len(spec.columns) for row in rows):
            raise Failure("DEPENDENCY_INVALID", "Dependency row width is invalid.")
        for row in rows:
            for value, declared in zip(row, spec.columns, strict=True):
                if value is None and declared.nullable:
                    continue
                if not _typed(value, declared.type):
                    raise Failure("DEPENDENCY_INVALID", "Dependency result type is invalid.")
        values: list[Any] = []
        for row in rows:
            if not isinstance(row, list) or len(row) != len(spec.columns):
                raise Failure("DEPENDENCY_INVALID", "Dependency row width is invalid.")
            value = row[index]
            if not _typed(value, ref.type):
                raise Failure("DEPENDENCY_INVALID", "Dependency value has incorrect type.")
            if value not in values:
                values.append(value)
        if len(json.dumps(values).encode()) > 8192:
            raise Failure("RESULT_TOO_LARGE", "Dependency values exceed byte limit.")
        resolved[ref.bind_as] = sorted(values)
    return resolved
