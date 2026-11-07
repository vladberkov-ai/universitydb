import json
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pytest
from conftest import QUESTION, SCOPE, SQL, outputs
from langgraph.graph.state import CompiledStateGraph

from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.domain import University
from universitydb.llm import OpenAIProvider, ScriptedProvider, Spending
from universitydb.tracing import Trace


def run(database, tmp_path, proposals=None, question=QUESTION):
    provider = ScriptedProvider(proposals if proposals is not None else outputs())
    agent = Agent(University(), database, provider, tmp_path / "traces")
    assert isinstance(agent.compiled, CompiledStateGraph)
    return agent.run(question), provider


def test_real_graph_s6_and_complete_trace(database, tmp_path):
    result, provider = run(database, tmp_path)
    assert result["status"] == "ok", result
    assert provider.calls == 2
    assert result["answer"]["rows"] == [["80.00", 2, 2]]
    assert result["execution_profile"] == "offline/injected"
    events = result["events"]
    assert [e["seq"] for e in events] == list(range(1, len(events) + 1))
    assert {e["run_id"] for e in events} == {result["run_id"]}
    assert len({e["event_id"] for e in events}) == len(events)
    assert [e["kind"] for e in events].count("run_end") == 1
    assert [e["payload"]["rows"] for e in events if e["kind"] == "db_result"] == [[[16000, 2, 2]]]
    for node in (
        "validate_input",
        "load_schema",
        "resolve_scope",
        "plan",
        "validate_plan",
        "generate_sql",
        "validate_sql",
        "execute",
        "inspect_result",
        "answer",
    ):
        assert any(e["node"] == node and e["kind"] == "node_start" for e in events)
    persisted = [
        json.loads(line)
        for line in (tmp_path / "traces" / f"{result['run_id']}.jsonl").read_text().splitlines()
    ]
    assert persisted == events


def test_changed_data_graph_not_canned(database, tmp_path):
    import sqlite3

    with sqlite3.connect(database) as connection:
        connection.execute(
            "UPDATE Enrollments SET grade_units=2000 WHERE student_id=2 AND offering_id=5"
        )
    result, _ = run(database, tmp_path)
    assert result["answer"]["rows"] == [["40.00", 2, 2]]
    assert [e["payload"]["rows"] for e in result["events"] if e["kind"] == "db_result"] == [
        [[8000, 2, 2]]
    ]


def test_changed_explicit_input_graph(database, tmp_path):
    scope = {**SCOPE, "student_id": 1}
    result, _ = run(
        database,
        tmp_path,
        outputs(scope),
        QUESTION.replace("student_id=2", "student_id=1").replace("Bea", "Alex"),
    )
    assert result["answer"]["rows"] == [["90.00", 1, 1]]


@pytest.mark.parametrize(
    "bad",
    [{}, {"version": "1", "steps": [], "needs_clarification": False, "clarification_field": None}],
)
def test_typed_bad_provider_rejected(database, tmp_path, bad):
    result, provider = run(database, tmp_path, [bad])
    assert result["error"]["code"] == "PROVIDER_INVALID_OUTPUT"
    assert result["answer"] is None and provider.calls == 1
    assert not any(e["kind"] == "sql_attempt" for e in result["events"])


@pytest.mark.parametrize(
    "sql",
    ["DROP TABLE Students", SQL + "; SELECT 1", SQL.replace("o.course_id = :course_id", "1=1")],
)
def test_graph_unsafe_no_execution(database, tmp_path, sql):
    result, provider = run(database, tmp_path, outputs(sql=sql))
    assert result["error"]["code"] in {"UNSAFE_SQL", "PROVIDER_INVALID_OUTPUT"}
    assert provider.calls == 2 and result["answer"] is None
    assert not any(e["kind"] == "sql_attempt" for e in result["events"])


def test_missing_key_no_network(database, tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "budget.json")
    with patch(
        "universitydb.llm.subprocess.Popen", side_effect=AssertionError("network/client forbidden")
    ):
        result = Agent(University(), database, provider, tmp_path / "traces").run(QUESTION)
    assert result["error"]["code"] == "PROVIDER_UNAVAILABLE"
    assert result["answer"] is None


def test_trace_failure_no_success_or_db(database, tmp_path):
    provider = ScriptedProvider(outputs())
    with patch.object(
        Trace, "emit", side_effect=Failure("TRACE_UNAVAILABLE", "injected sink failure")
    ):
        result = Agent(University(), database, provider, tmp_path / "traces").run(QUESTION)
    assert result["error"]["code"] == "TRACE_UNAVAILABLE"
    assert provider.calls == 0 and result["answer"] is None


@pytest.mark.parametrize("kind", ["answer", "run_end"])
def test_late_trace_failure_never_publishes_success(database, tmp_path, kind):
    original = Trace.emit

    def failing(self, node, event_kind, payload, attempt=0):
        if event_kind == kind:
            raise Failure("TRACE_UNAVAILABLE", "injected late sink failure")
        return original(self, node, event_kind, payload, attempt)

    with patch.object(Trace, "emit", failing):
        result, _ = run(database, tmp_path)
    assert result["error"]["code"] == "TRACE_UNAVAILABLE"
    assert result["answer"] is None


def test_sql_timeout_graph(database, tmp_path):
    with patch(
        "universitydb.agent.db.execute",
        side_effect=Failure("SQL_TIMEOUT", "injected bound timeout"),
    ):
        result, _ = run(database, tmp_path)
    assert result["error"]["code"] == "SQL_TIMEOUT"
    assert result["answer"] is None


def test_persistent_spending_shared_across_instances_and_failures(tmp_path):
    ledger = tmp_path / "ledger.json"

    def budget():
        return Spending(ledger, "approved-test", Decimal(".028"), Decimal(1), Decimal(1))

    assert budget().reserve().amount == "0.014"
    assert budget().reserve().amount == "0.014"
    with pytest.raises(Failure) as error:
        budget().reserve()
    assert error.value.code == "BUDGET_EXCEEDED"
    assert json.loads(ledger.read_text())["calls"] == 2


def test_unsupported_inputs_no_provider(database, tmp_path):
    for question in ("DROP TABLE Students", "x" * 2001):
        result, provider = run(database, tmp_path, [], question)
        assert result["error"]["code"] == "INVALID_INPUT"
        assert provider.calls == 0


def test_one_recoverable_parse_repair(database, tmp_path):
    plan, bad = outputs(sql="SELECT (")
    result, provider = run(database, tmp_path, [plan, bad, outputs()[1]])
    assert result["status"] == "ok", result
    assert provider.calls == 3
    assert result["answer"]["rows"] == [["80.00", 2, 2]]
    assert any(e["payload"].get("repair") for e in result["events"])


def test_parse_repair_exhaustion(database, tmp_path):
    plan, bad = outputs(sql="SELECT (")
    result, provider = run(database, tmp_path, [plan, bad, bad])
    assert result["error"]["code"] == "SQL_INVALID"
    assert provider.calls == 3
    assert result["answer"] is None


def test_single_transient_retry(database, tmp_path, monkeypatch):
    monkeypatch.setattr("universitydb.agent.time.sleep", lambda _: None)
    plan, sql = outputs()
    result, provider = run(
        database, tmp_path, [Failure("PROVIDER_TRANSIENT", "test timeout"), plan, sql]
    )
    assert result["status"] == "ok"
    assert provider.calls == 3
    result, provider = run(database, tmp_path, [Failure("PROVIDER_TRANSIENT", "test timeout")] * 2)
    assert result["error"]["code"] == "PROVIDER_UNAVAILABLE"
    assert provider.calls == 2


def test_trace_limit_is_error(database, tmp_path):
    original = Trace.__init__

    def bounded(self, directory, run_id, **kwargs):
        original(self, directory, run_id, limit=5000)

    with patch.object(Trace, "__init__", bounded):
        result, _ = run(database, tmp_path)
    assert result["status"] == "error"
    assert result["answer"] is None
