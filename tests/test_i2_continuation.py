"""Real checkpoint continuation; offline scripted transport, not model accuracy."""

from copy import deepcopy

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from test_i2_core import scripted_step

from universitydb.agent import Agent
from universitydb.domain import University, make_spec
from universitydb.llm import ScriptedProvider


def make_agent(database, tmp_path, outputs=None):
    domain = University()
    spec = make_spec("grade_mean")
    sql, params = domain.query(spec, {"student_id": 1})
    provider = ScriptedProvider(
        list(scripted_step(spec, sql, params)) if outputs is None else outputs
    )
    return Agent(
        domain, database, provider, tmp_path / "trace", session_id="server-session"
    ), provider


def test_real_pause_resume_and_replay(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex", request_id="start")
    assert first["status"] == "clarification"
    assert first["error"] is None and first["answer"] is None and provider.calls == 0
    assert isinstance(agent.saver, InMemorySaver)
    continuation = first["clarification"]
    snapshot = agent.compiled.get_state({"configurable": {"thread_id": first["run_id"]}})
    assert snapshot.interrupts
    assert snapshot.config["configurable"]["checkpoint_id"] == continuation["checkpoint_id"]
    assert snapshot.values["counters"]["llm_calls"] == 0
    result = agent.resume(continuation, 1, request_id="choice")
    assert result["status"] == "ok", result
    assert result["answer"]["rows"][0][0] == "86.67"
    assert result["run_id"] == first["run_id"] and provider.calls == 2
    assert agent.resume(continuation, 1, request_id="choice") == result
    assert provider.calls == 2
    assert agent.resume(continuation, 3, request_id="choice")["error"]["code"] == "REPLAY_CONFLICT"
    assert agent.resume(continuation, 1, request_id="different")["error"]["code"] == "STALE_RESUME"
    assert len([e for e in result["events"] if e["kind"] == "run_end"]) == 1
    final = agent.compiled.get_state({"configurable": {"thread_id": first["run_id"]}})
    assert final.values["counters"]["llm_calls"] == 2
    assert final.values["counters"]["sql_attempts"] == 1
    assert final.values["active_ms"] >= 0


@pytest.mark.parametrize(
    "kind", ["foreign", "checkpoint", "selection", "expired", "data", "policy"]
)
def test_resume_rejections_before_provider(database, tmp_path, kind):
    import sqlite3

    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex")
    continuation = deepcopy(first["clarification"])
    kwargs = {}
    selection = 1
    expected = {
        "foreign": "RESUME_FORBIDDEN",
        "checkpoint": "STALE_RESUME",
        "selection": "INVALID_SELECTION",
        "expired": "RESUME_EXPIRED",
        "data": "DATA_INCONSISTENT",
        "policy": "STALE_RESUME",
    }[kind]
    if kind == "foreign":
        kwargs["session_id"] = "another-session"
    elif kind == "checkpoint":
        continuation["checkpoint_id"] = "stale"
    elif kind == "selection":
        selection = True
    elif kind == "expired":
        agent._now = lambda: continuation["expires_at"] + 1
    elif kind == "data":
        with sqlite3.connect(database) as conn:
            conn.execute('UPDATE Students SET name="Changed" WHERE student_id=4')
    else:
        old = agent.domain.descriptor
        agent.domain.descriptor = lambda: {**old(), "policy": "changed"}
    result = agent.resume(continuation, selection, request_id="resume", **kwargs)
    assert result["error"]["code"] == expected, result
    assert provider.calls == 0


def test_request_replay_and_paused_run_survives_new_run(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex", request_id="a")
    assert agent.run("mean Alex", request_id="a") == first
    assert agent.run("different", request_id="a")["error"]["code"] == "REPLAY_CONFLICT"
    bad = agent.run("x" * 2001, request_id="b")
    assert bad["status"] == "error"
    result = agent.resume(first["clarification"], 1, request_id="resume")
    assert result["status"] == "ok" and provider.calls == 2


def test_model_requested_pause_preserves_completed_plan_call(database, tmp_path):
    domain = University()
    sql, params = domain.query(make_spec("grade_mean"), {"student_id": 1})
    plan, proposal = scripted_step(make_spec("grade_mean"), sql, params)
    plan.update(needs_clarification=True, clarification_field="student_id")
    agent, provider = make_agent(database, tmp_path, [plan, proposal])
    first = agent.run("mean all")
    assert first["status"] == "clarification" and provider.calls == 1
    result = agent.resume(first["clarification"], 1, request_id="resume")
    assert result["status"] == "ok", result
    assert provider.calls == 2


def test_two_pauses_wait_excluded_and_third_pause_terminal(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex current semester count")
    assert first["status"] == "clarification"
    start = agent._now()
    agent._now = lambda: start + 800  # Human wait is below TTL, above active-work budget.
    second = agent.resume(first["clarification"], 1, request_id="one")
    assert second["status"] == "clarification" and provider.calls == 0
    assert second["clarification"]["field"] == "semester_id"
    result = agent.resume(second["clarification"], "S1", request_id="two")
    assert result["error"]["code"] == "CLARIFICATION_LIMIT"
    snapshot = agent.compiled.get_state({"configurable": {"thread_id": first["run_id"]}})
    assert snapshot.values["counters"]["clarifications"] == 2
    assert snapshot.values["counters"]["llm_calls"] == 0
    assert snapshot.values["active_ms"] < 180000
    assert provider.calls == 0


def test_empty_model_plan_clarification_replans_once(database, tmp_path):
    domain = University()
    sql, params = domain.query(make_spec("grade_mean"), {"student_id": 1})
    plan, proposal = scripted_step(make_spec("grade_mean"), sql, params)
    pause = {
        "version": "1",
        "steps": [],
        "needs_clarification": True,
        "clarification_field": "student_id",
    }
    agent, provider = make_agent(database, tmp_path, [pause, plan, proposal])
    first = agent.run("mean all")
    assert first["status"] == "clarification" and provider.calls == 1
    result = agent.resume(first["clarification"], 1, request_id="resume")
    assert result["status"] == "ok" and provider.calls == 3
    assert len([e for e in result["events"] if e["kind"] == "sql_attempt"]) == 1


def test_unknown_usage_and_accounting_stop_never_retry(database, tmp_path):
    class UnknownUsage(ScriptedProvider):
        def call(self, *args, **kwargs):
            result, _ = super().call(*args, **kwargs)
            return result, {"input_tokens": 1, "output_tokens": 0}

    domain = University()
    spec = make_spec("grade_mean")
    sql, params = domain.query(spec, {})
    provider = UnknownUsage(list(scripted_step(spec, sql, params)))
    result = Agent(domain, database, provider, tmp_path / "unknown").run("mean all")
    assert result["error"]["code"] == "PROVIDER_INVALID_OUTPUT"
    assert result["answer"] is None and provider.calls == 1


def test_schema_and_actual_foreign_agent_isolation(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex")
    foreign, other = make_agent(database, tmp_path / "foreign")
    result = foreign.resume(first["clarification"], 1, request_id="foreign")
    assert result["error"]["code"] == "RESUME_EXPIRED"
    changed = deepcopy(first["clarification"])
    changed["schema_sha256"] = "different-schema"
    assert agent.resume(changed, 1, request_id="changed")["error"]["code"] == "STALE_RESUME"
    assert provider.calls == other.calls == 0


def test_counter_corruption_fails_before_any_dispatch(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex")
    config = {"configurable": {"thread_id": first["run_id"]}}
    snapshot = agent.compiled.get_state(config)
    counters = {**snapshot.values["counters"], "llm_calls": -1}
    agent.compiled.update_state(config, {"counters": counters})
    changed = deepcopy(first["clarification"])
    # An attacker cannot submit a fresh checkpoint envelope: server retains its exact envelope.
    changed["checkpoint_id"] = agent.compiled.get_state(config).config["configurable"][
        "checkpoint_id"
    ]
    assert agent.resume(changed, 1, request_id="bad")["error"]["code"] == "STALE_RESUME"
    # Direct corrupt checkpoint restoration must also fail closed at the core boundary.
    result = agent._execute_graph(agent._runs[first["run_id"]], {"question": "mean all"})
    assert result["error"]["code"] == "BUDGET_EXCEEDED"
    assert provider.calls == 0


def test_replay_revalidates_data_before_cached_result(database, tmp_path):
    import sqlite3

    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex", request_id="start")
    result = agent.resume(first["clarification"], 1, request_id="resume")
    assert result["status"] == "ok"
    with sqlite3.connect(database) as conn:
        conn.execute('UPDATE Students SET name="Different" WHERE student_id=4')
    assert (
        agent.resume(first["clarification"], 1, request_id="resume")["error"]["code"]
        == "DATA_INCONSISTENT"
    )
    assert agent.run("mean Alex", request_id="start")["error"]["code"] == "DATA_INCONSISTENT"
    assert provider.calls == 2


def test_graph_recursion_bound_is_terminal_traced_budget_failure(database, tmp_path):
    from unittest.mock import patch

    from langgraph.errors import GraphRecursionError

    agent, provider = make_agent(database, tmp_path)
    with patch.object(agent.compiled, "invoke", side_effect=GraphRecursionError("bounded")):
        result = agent.run("mean all")
    assert result["error"]["code"] == "BUDGET_EXCEEDED"
    assert result["answer"] is None and provider.calls == 0
    assert result["events"][-1]["kind"] == "run_end"


def test_actual_policy_change_ends_pending_run_but_client_stale_does_not(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex")
    stale = deepcopy(first["clarification"])
    stale["policy_sha256"] = "invented"
    rejected = agent.resume(stale, 1, request_id="bad")
    assert rejected["error"]["code"] == "STALE_RESUME"
    assert not any(e["kind"] == "run_end" for e in rejected["events"])
    old = agent.domain.descriptor
    agent.domain.descriptor = lambda: {**old(), "policy": "changed"}
    terminal = agent.resume(first["clarification"], 1, request_id="changed")
    assert terminal["error"]["code"] == "STALE_RESUME"
    assert terminal["events"][-1]["kind"] == "run_end"
    assert provider.calls == 0


def test_trace_preserves_actual_request_ids_across_resume(database, tmp_path):
    agent, provider = make_agent(database, tmp_path)
    first = agent.run("mean Alex", request_id="new-app-request")
    assert {e["request_id"] for e in first["events"]} == {"new-app-request"}
    result = agent.resume(first["clarification"], 1, request_id="resume-app-request")
    assert result["status"] == "ok" and provider.calls == 2
    assert {e["request_id"] for e in result["events"]} == {"new-app-request", "resume-app-request"}
    assert {e["run_id"] for e in result["events"]} == {first["run_id"]}
