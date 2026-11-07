from decimal import Decimal
from unittest.mock import patch

import pytest
from conftest import QUESTION, SCOPE, outputs
from pydantic import ValidationError

from universitydb.agent import Agent
from universitydb.contracts import Binding, Failure, PlanProposal, SQLProposal, bindings
from universitydb.domain import University
from universitydb.llm import ScriptedProvider, Spending
from universitydb.tracing import Trace


def test_binding_closed_and_byte_bounds():
    with pytest.raises(ValidationError):
        Binding(name="x", type="integer", integer_value=True, text_value=None)
    with pytest.raises(Failure):
        bindings([Binding(name="x", type="text", integer_value=None, text_value="é" * 1001)])
    one = Binding(name="x", type="integer", integer_value=1, text_value=None)
    with pytest.raises(Failure):
        bindings([one, one])
    with pytest.raises(Failure):
        bindings([Binding(name="x", type="integer", integer_value=None, text_value=None)])


def test_sql_size_and_closed_proposal():
    value = outputs()[1]
    value["sql"] = "x" * 8001
    with pytest.raises(ValidationError):
        SQLProposal.model_validate(value)
    value = outputs()[1]
    value["sql"] = "é" * 4001
    with pytest.raises(Failure) as error:
        University().validate_sql(SQLProposal.model_validate(value), SCOPE)
    assert error.value.code == "RESOURCE_LIMIT"
    value = outputs()[1]
    value["extra"] = True
    with pytest.raises(ValidationError):
        SQLProposal.model_validate(value)


def test_provider_call_limit_and_deadline(database, tmp_path):
    agent = Agent(University(), database, ScriptedProvider(outputs()), tmp_path / "traces")
    agent.trace = Trace(tmp_path / "traces", "limit")
    agent.deadline = float("inf")
    agent.calls = 5
    with pytest.raises(Failure) as error:
        agent._call("plan", {}, PlanProposal)
    assert error.value.code == "BUDGET_EXCEEDED"
    agent.deadline = 0
    with pytest.raises(Failure):
        agent._check_deadline()


def test_trace_budget_persists_terminal_error(database, tmp_path):
    original = Trace.__init__

    def limited(self, directory, run_id, **kwargs):
        original(self, directory, run_id, limit=5000)

    with patch.object(Trace, "__init__", limited):
        result = Agent(
            University(), database, ScriptedProvider(outputs()), tmp_path / "traces"
        ).run(QUESTION)
    assert result["status"] == "error" and result["answer"] is None
    assert result["events"][-1]["kind"] == "run_end"


def test_budget_actual_usage_reconciled_without_releasing_hold(tmp_path):
    import json

    ledger = tmp_path / "spend.json"
    budget = Spending(ledger, "test", Decimal(".1"), Decimal(1), Decimal(2))
    budget.reserve()
    budget.record_usage(100, 50)
    record = json.loads(ledger.read_text())
    assert record["reserved_usd"] == ".016" or Decimal(record["reserved_usd"]) == Decimal(".016")
    assert Decimal(record["observed_usd"]) == Decimal(".0002")
    assert record["input_tokens"] == 100 and record["output_tokens"] == 50
