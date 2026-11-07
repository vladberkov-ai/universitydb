"""Strict shared step/result boundaries, independent of either domain."""

from copy import deepcopy

import pytest
from conftest import outputs

from universitydb.contracts import (
    Failure,
    PlanProposal,
    ResultSpec,
    materialize_refs,
    validate_dag,
    validate_result,
)


def plan_pair():
    value = outputs()[0]
    first = value["steps"][0]
    second = deepcopy(first)
    second.update(
        step_id="next",
        depends_on=["s6"],
        result_refs=[
            {"from_step": "s6", "column": "sum_units", "type": "integer", "bind_as": "ids"}
        ],
    )
    value["steps"].append(second)
    return PlanProposal.model_validate(value)


def test_static_dag_is_separate_from_completed_results():
    plan = plan_pair()
    validate_dag(plan)
    with pytest.raises(Failure, match="Missing"):
        materialize_refs(plan.steps[1], {})


@pytest.mark.parametrize(
    "mutation", ["forward", "missing", "duplicate", "column", "type", "undeclared"]
)
def test_bad_static_refs(mutation):
    value = plan_pair().model_dump()
    step = value["steps"][1]
    if mutation == "forward":
        value["steps"].reverse()
    elif mutation == "missing":
        step["depends_on"] = ["absent"]
    elif mutation == "duplicate":
        step["step_id"] = "s6"
    elif mutation == "column":
        step["result_refs"][0]["column"] = "unknown"
    elif mutation == "type":
        step["result_refs"][0]["type"] = "string"
    else:
        step["depends_on"] = []
    with pytest.raises(Failure):
        validate_dag(PlanProposal.model_validate(value))


def test_materialized_refs_check_types_dedupe_and_keep_empty():
    plan = plan_pair()
    spec = plan.steps[0].result_spec
    raw = {"result_spec": spec.model_dump(), "rows": [[2, 1, 1], [2, 1, 1]], "truncated": False}
    assert materialize_refs(plan.steps[1], {"s6": raw}) == {"ids": [2]}
    raw["rows"] = []
    assert materialize_refs(plan.steps[1], {"s6": raw}) == {"ids": []}
    for rows in ([[True, 1, 1]], [[None, 1, 1]], [[1, 1, 1]] * 101):
        raw["rows"] = rows
        with pytest.raises(Failure):
            materialize_refs(plan.steps[1], {"s6": raw})
    raw.update(rows=[], truncated=True)
    with pytest.raises(Failure):
        materialize_refs(plan.steps[1], {"s6": raw})


def test_declared_schema_preserves_nullable_and_empty():
    spec = ResultSpec.model_validate(
        {
            "metric_id": "fixture",
            "shape": "rows",
            "group_keys": [],
            "columns": [{"name": "value", "type": "integer", "nullable": True}],
            "components": {"sum": None, "denominator": None, "count": None},
            "unit": "identifier",
            "scale": 1,
        }
    )
    for rows in ([], [[None]], [[0]]):
        result = {
            "columns": [{"name": "value", "type": "integer"}],
            "rows": rows,
            "truncated": False,
            "row_count": len(rows),
            "step_id": "one",
            "result_spec": spec.model_dump(),
            "elapsed_ms": 0,
        }
        validate_result(result, spec)
    with pytest.raises(Failure):
        validate_result(
            {
                "columns": [{"name": "value", "type": "integer"}],
                "rows": [[True]],
                "truncated": False,
                "row_count": 1,
                "step_id": "one",
                "result_spec": spec.model_dump(),
                "elapsed_ms": 0,
            },
            spec,
        )


def complete_raw(spec, rows):
    return {
        "step_id": "s6",
        "result_spec": spec.model_dump(),
        "columns": [{"name": c.name, "type": c.type} for c in spec.columns],
        "rows": rows,
        "row_count": len(rows),
        "elapsed_ms": 0,
        "truncated": False,
    }


@pytest.mark.parametrize("mutation", ["spec", "row_count", "elapsed", "step_id", "columns"])
def test_strict_db_metadata(mutation):
    spec = plan_pair().steps[0].result_spec
    raw = complete_raw(spec, [[2, 1, 1]])
    if mutation == "spec":
        raw["result_spec"]["unit"] = "invented"
    elif mutation == "row_count":
        raw["row_count"] = True
    elif mutation == "elapsed":
        raw["elapsed_ms"] = -1
    elif mutation == "step_id":
        raw["step_id"] = ""
    else:
        raw["columns"] = []
    with pytest.raises(Failure, match="."):
        validate_result(raw, spec)


def test_dependency_uses_trusted_spec_sorted_and_full_metadata():
    plan = plan_pair()
    spec = plan.steps[0].result_spec
    raw = complete_raw(spec, [[3, 1, 1], [1, 1, 1], [3, 1, 1]])
    assert materialize_refs(plan.steps[1], {"s6": raw}, {"s6": spec}) == {"ids": [1, 3]}
    for mutation in ("spec", "count", "truncated", "oversized"):
        bad = deepcopy(raw)
        if mutation == "spec":
            bad["result_spec"]["scale"] = 1
        elif mutation == "count":
            bad["row_count"] = 0
        elif mutation == "truncated":
            bad["truncated"] = True
        else:
            bad["rows"] *= 34
            bad["row_count"] = len(bad["rows"])
        with pytest.raises(Failure) as error:
            materialize_refs(plan.steps[1], {"s6": bad}, {"s6": spec})
        assert error.value.code == (
            "RESULT_TOO_LARGE" if mutation in ("truncated", "oversized") else "DEPENDENCY_INVALID"
        )


def test_public_answer_reasons_are_closed_and_row_aligned():
    from pydantic import ValidationError

    from universitydb.contracts import Answer, RunError

    base = {
        "text": "undefined",
        "columns": [{"name": "average", "type": "decimal"}],
        "rows": [[None]],
        "scope": "all",
        "empty_reason": "no_rows",
        "truncated": False,
        "row_reasons": ["no_rows"],
    }
    Answer.model_validate(base)
    for change in (
        {"row_reasons": []},
        {"row_reasons": ["invented"]},
        {"rows": [[83.33]]},
        {"columns": [{"name": "average", "type": "decimal", "nullable": True}]},
    ):
        with pytest.raises(ValidationError):
            Answer.model_validate({**base, **change})
    for code in ("FOREIGN_SESSION", "CLARIFICATION_EXPIRED", "REQUEST_CONFLICT", "UNKNOWN_ENTITY"):
        with pytest.raises(ValidationError):
            RunError(code=code, message="bad alias", failed_node="resume", retryable=False)


def test_public_envelope_requires_one_exact_status_branch():
    from pydantic import ValidationError

    from universitydb.contracts import RunEnvelope

    value = {
        "version": "1",
        "run_id": "app-run",
        "trace_id": "app-run",
        "status": "error",
        "answer": None,
        "clarification": None,
        "error": {
            "code": "RESUME_EXPIRED",
            "message": "expired",
            "failed_node": "resume",
            "retryable": False,
        },
    }
    RunEnvelope.model_validate(value)
    with pytest.raises(ValidationError):
        RunEnvelope.model_validate({**value, "status": "ok"})
    with pytest.raises(ValidationError):
        RunEnvelope.model_validate({**value, "events": []})


def test_known_accounting_stop_transient_keeps_primary_error_code():
    from universitydb.contracts import RunError

    error = RunError(
        code="PROVIDER_TRANSIENT",
        message="Unknown usage; dispatch stopped.",
        failed_node="plan",
        retryable=False,
    )
    assert error.code == "PROVIDER_TRANSIENT"


def test_sqlite_integer_primitives_reject_extreme_values_before_checkpoint():
    from pydantic import ValidationError

    from universitydb.contracts import Binding

    for value in (-9223372036854775809, 9223372036854775808, 10**100, True):
        with pytest.raises(ValidationError):
            Binding(name="x", type="integer", integer_value=value, text_value=None)
    for value in (-9223372036854775808, 9223372036854775807):
        Binding(name="x", type="integer", integer_value=value, text_value=None)
    spec = plan_pair().steps[0].result_spec
    for scale in (0, -1, 10**100):
        with pytest.raises(ValidationError):
            ResultSpec.model_validate({**spec.model_dump(), "scale": scale})
    for value in (-9223372036854775809, 9223372036854775808):
        raw = complete_raw(spec, [[value, 1, 1]])
        with pytest.raises(Failure) as error:
            validate_result(raw, spec)
        assert error.value.code == "RESULT_CONTRACT_INVALID"


@pytest.mark.parametrize("question", [10**100, [10**100], {"question": 10**100}, 1.5, None, True])
def test_public_nonstr_question_rejected_before_fingerprint_saver_or_db(tmp_path, question):
    from unittest.mock import patch

    from universitydb.agent import Agent
    from universitydb.contracts import AgentOutput
    from universitydb.domain import University
    from universitydb.llm import ScriptedProvider

    provider = ScriptedProvider([])
    agent = Agent(University(), tmp_path / "not-opened.sqlite", provider, tmp_path / "trace")
    with patch(
        "universitydb.agent.db.inspect", side_effect=AssertionError("No DB startup allowed")
    ):
        result = agent.run(question)
    AgentOutput.model_validate(result)
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0 and not agent._runs and not agent._requests
