"""Closed wire types for the single supported scalar aggregate slice."""

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
    steps: list[Step] = Field(min_length=1, max_length=1)
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
