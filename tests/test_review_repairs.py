"""Independent-review regression locks: immutable replay, trace, SQLite identity/errors."""

import json
import sqlite3
from copy import deepcopy
from unittest.mock import patch

import pytest
from conftest import QUESTION, outputs

from universitydb import db
from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.domain import University
from universitydb.llm import ScriptedProvider


def agent_at(database, tmp_path, now=1000.0, proposals=None):
    provider = ScriptedProvider(outputs() if proposals is None else proposals)
    agent = Agent(University(), database, provider, tmp_path / "traces")
    clock = [now]
    agent._now = lambda: clock[0]
    return agent, provider, clock


def test_eight_unexpired_terminal_contexts_are_not_evicted(database, tmp_path):
    agent, provider, _ = agent_at(database, tmp_path, proposals=[])
    first = agent.run("", request_id="id-0")
    for i in range(1, 8):
        agent.run("", request_id=f"id-{i}")
    denied = agent.run("", request_id="ninth")
    assert denied["error"]["code"] == "RESOURCE_LIMIT"
    assert len(agent._runs) == 8
    assert agent.run("", request_id="id-0") == first
    assert provider.calls == 0


@pytest.mark.parametrize("offset", [899.999, 900.0, 900.001])
@pytest.mark.parametrize("paused", [False, True])
def test_exact_run_replay_ttl_and_owner_trace(database, tmp_path, offset, paused):
    agent, provider, clock = agent_at(database, tmp_path, proposals=[] if paused else outputs())
    question = "mean Alex" if paused else QUESTION
    first = agent.run(question, request_id="accepted")
    trace = tmp_path / "traces" / (first["run_id"] + ".jsonl")
    before = trace.read_bytes()
    clock[0] += offset
    result = agent.run(question, request_id="accepted")
    if offset < 900:
        assert result == first
        assert trace.read_bytes() == before
    else:
        assert result["error"]["code"] == "RESUME_EXPIRED"
        assert result["run_id"] == result["trace_id"] == first["run_id"]
        assert result["events"] and result["events"][-1]["kind"] == "run_end"
        assert result["events"] == [json.loads(line) for line in trace.read_text().splitlines()]
        if paused:
            assert trace.read_bytes() != before
            assert result["events"][-1]["request_id"] == "accepted"
        else:
            assert trace.read_bytes() == before  # A terminal success trace is immutable.
    assert provider.calls == (0 if paused else 2)


def test_32_immutable_identities_survive_expired_context_cleanup(database, tmp_path):
    agent, provider, clock = agent_at(database, tmp_path, proposals=[])
    first = agent.run("", request_id="id-0")
    for i in range(1, 32):
        if i % 8 == 0:
            clock[0] += 900
        agent.run("", request_id=f"id-{i}")
    identity = deepcopy(agent._requests["id-0"])
    clock[0] += 900
    expired = agent.run("", request_id="id-0")
    conflict = agent.run("different", request_id="id-0")
    denied = agent.run("", request_id="id-32")
    assert expired["error"]["code"] == "RESUME_EXPIRED"
    assert expired["run_id"] == first["run_id"] and expired["events"]
    assert conflict["error"]["code"] == "REPLAY_CONFLICT"
    assert denied["error"]["code"] == "RESOURCE_LIMIT"
    assert len(agent._requests) == 32 and agent._requests["id-0"] == identity
    assert not agent._runs and not agent._responses
    with pytest.raises(AttributeError):
        agent._requests["id-0"].expires_at = clock[0] + 900
    assert provider.calls == 0


def test_post_startup_sqlite_lock_is_not_repaired(database, tmp_path):
    agent, provider, _ = agent_at(database, tmp_path)
    connection = sqlite3.connect(database)
    original = agent._action

    def lock_after_validation(name, state):
        update = original(name, state)
        if name == "validate_sql":
            connection.execute("BEGIN EXCLUSIVE")
        return update

    try:
        with patch.object(agent, "_action", lock_after_validation):
            result = agent.run(QUESTION)
    finally:
        connection.rollback()
        connection.close()
    assert result["error"]["code"] == "DB_UNAVAILABLE", result
    assert provider.calls == 2
    assert not any(e["payload"].get("repair") for e in result["events"])
    assert result["answer"] is None


def test_wal_visible_mutation_leaves_main_hash_but_startup_rejects(database, tmp_path):
    connection = sqlite3.connect(database)
    try:
        assert connection.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
        connection.commit()
        before = db.file_hash(database)
        connection.execute(
            "UPDATE Enrollments SET grade_units=1000 WHERE student_id=1 AND offering_id=1"
        )
        connection.commit()
        assert db.file_hash(database) == before
        with sqlite3.connect(database) as observer:
            assert (
                observer.execute(
                    "SELECT grade_units FROM Enrollments WHERE student_id=1 AND offering_id=1"
                ).fetchone()[0]
                == 1000
            )
        agent, provider, _ = agent_at(database, tmp_path, proposals=[])
        result = agent.run(QUESTION)
        assert result["error"]["code"] == "DATA_INCONSISTENT", result
        assert provider.calls == 0
    finally:
        connection.close()


@pytest.mark.parametrize("offset", [899.999, 900.0, 900.001])
def test_resume_ttl_inclusive_and_exact_accepted_replay_expiry(database, tmp_path, offset):
    domain = University()
    from test_i2_core import scripted_step

    spec = domain.spec
    sql, params = domain.query(spec, {"student_id": 1})
    agent, provider, clock = agent_at(
        database, tmp_path, proposals=list(scripted_step(spec, sql, params))
    )
    first = agent.run("mean Alex", request_id="start")
    clock[0] += offset
    result = agent.resume(first["clarification"], 1, request_id="choice")
    if offset < 900:
        assert result["status"] == "ok" and provider.calls == 2
        assert agent.resume(first["clarification"], 1, request_id="choice") == result
        clock[0] = 1900.0
        expired = agent.resume(first["clarification"], 1, request_id="choice")
        assert expired["error"]["code"] == "RESUME_EXPIRED"
        assert expired["run_id"] == first["run_id"] and expired["events"] == result["events"]
    else:
        assert result["error"]["code"] == "RESUME_EXPIRED" and provider.calls == 0
        assert result["run_id"] == first["run_id"] and result["events"][-1]["kind"] == "run_end"


def test_start_replay_actual_binding_change_has_owner_trace(database, tmp_path):
    agent, provider, _ = agent_at(database, tmp_path, proposals=[])
    first = agent.run("mean Alex", request_id="start")
    with sqlite3.connect(database) as conn:
        conn.execute('UPDATE Students SET name="Changed" WHERE student_id=4')
    rejected = agent.run("mean Alex", request_id="start")
    assert rejected["error"]["code"] == "DATA_INCONSISTENT"
    assert rejected["run_id"] == first["run_id"]
    assert rejected["events"][-1]["kind"] == "run_end"
    assert rejected["events"][-1]["request_id"] == "start"
    assert provider.calls == 0


def test_wal_mode_change_rejected_before_resume_and_execute(database, tmp_path):
    from conftest import SCOPE, SQL

    agent, provider, _ = agent_at(database, tmp_path, proposals=[])
    first = agent.run("mean Alex", request_id="start")
    with sqlite3.connect(database) as conn:
        assert conn.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
    rejected = agent.resume(first["clarification"], 1, request_id="choice")
    assert rejected["error"]["code"] == "DATA_INCONSISTENT" and provider.calls == 0
    with pytest.raises(Failure) as error:
        db.execute(database, SQL, SCOPE, University.tables, University.functions)
    assert error.value.code == "DATA_INCONSISTENT"


@pytest.mark.parametrize(
    "sqlite_code,expected",
    [
        (sqlite3.SQLITE_BUSY, "DB_UNAVAILABLE"),
        (sqlite3.SQLITE_LOCKED, "DB_UNAVAILABLE"),
        (sqlite3.SQLITE_CANTOPEN, "DB_UNAVAILABLE"),
        (sqlite3.SQLITE_IOERR, "DB_UNAVAILABLE"),
        (sqlite3.SQLITE_CORRUPT, "DATA_INCONSISTENT"),
        (sqlite3.SQLITE_NOTADB, "DATA_INCONSISTENT"),
    ],
)
def test_worker_sqlite_error_taxonomy(sqlite_code, expected, database):
    from universitydb import db_worker

    error = sqlite3.OperationalError("injected SQLite error")
    error.sqlite_errorcode = sqlite_code
    with (
        patch("universitydb.db_worker.sqlite3.connect", side_effect=error),
        pytest.raises(Failure) as caught,
    ):
        db_worker.run({"path": str(database), "timeout": 2})
    assert caught.value.code == expected


@pytest.mark.parametrize("sql", ["SELECT (", "SELECT absent_column FROM Students"])
def test_only_syntax_or_unknown_column_remains_repairable(database, sql):
    with pytest.raises(Failure) as error:
        db.execute(database, sql, {}, University.tables, University.functions)
    assert error.value.code == "SQL_INVALID"


def test_m1_plan_checkpoint_resume_keeps_actual_dependencies_and_budgets(database, tmp_path):
    from test_i3_dependencies import QUESTION as M1_QUESTION
    from test_i3_dependencies import ActualReferenceProvider

    provider = ActualReferenceProvider()
    provider.plan.update(needs_clarification=True, clarification_field="semester_id")
    agent, _, _ = agent_at(database, tmp_path, proposals=[])
    agent.provider = provider
    first = agent.run(M1_QUESTION, request_id="m1-start")
    assert first["status"] == "clarification" and provider.calls == 1
    assert not any(e["kind"] == "sql_attempt" for e in first["events"])
    result = agent.resume(first["clarification"], "S1", request_id="m1-choice")
    assert result["status"] == "ok", result
    assert result["answer"]["rows"] == [[1, "95.00", 2, 2]]
    assert provider.calls == 4
    payloads = [entry["payload"] for entry in provider.history if entry["operation"] == "sql"]
    assert [payload["resolved_refs"] for payload in payloads] == [
        {},
        {"course_ids": [2]},
        {"student_ids": [1]},
    ]
    snapshot = agent.compiled.get_state({"configurable": {"thread_id": first["run_id"]}})
    assert snapshot.values["counters"]["llm_calls"] == 4
    assert snapshot.values["counters"]["sql_attempts"] == 3
    assert snapshot.values["counters"]["clarifications"] == 1
    assert agent.resume(first["clarification"], "S1", request_id="m1-choice") == result
    assert provider.calls == 4
    trace = tmp_path / "traces" / (result["run_id"] + ".jsonl")
    assert result["events"] == [json.loads(line) for line in trace.read_text().splitlines()]
    assert {e["request_id"] for e in result["events"]} == {"m1-start", "m1-choice"}
    (tmp_path / "m1-resume-proof.json").write_text(
        json.dumps(
            {
                "profile": "offline/injected; not real-model NL-to-SQL accuracy",
                "run_id": result["run_id"],
                "answer": result["answer"],
                "provider_history": provider.history,
                "sql_proposals": provider.proposals,
                "counters": snapshot.values["counters"],
                "step_results": result["step_results"],
                "trace_basename": trace.name,
                "trace_sha256": db.file_hash(trace),
            },
            indent=2,
        )
    )


def test_real_worker_busy_is_database_failure_not_repairable_sql(database):
    from conftest import SCOPE, SQL

    from universitydb import db_worker

    connection = sqlite3.connect(database)
    connection.execute("BEGIN EXCLUSIVE")
    try:
        with pytest.raises(Failure) as error:
            db_worker.run(
                {
                    "path": str(database),
                    "sql": SQL,
                    "parameters": SCOPE,
                    "tables": University.tables,
                    "functions": University.functions,
                    "timeout": 2,
                }
            )
        assert error.value.code == "DB_UNAVAILABLE"
    finally:
        connection.rollback()
        connection.close()


def test_full_registry_resume_fails_closed_before_dispatch(database, tmp_path):
    agent, provider, clock = agent_at(database, tmp_path, proposals=[])
    for i in range(31):
        if i and i % 8 == 0:
            clock[0] += 900
        agent.run("", request_id=f"used-{i}")
    paused = agent.run("mean Alex", request_id="last-identity")
    assert paused["status"] == "clarification"
    denied = agent.resume(paused["clarification"], 1, request_id="new-choice")
    assert denied["error"]["code"] == "RESOURCE_LIMIT"
    assert not any(e["kind"] == "run_end" for e in denied["events"])
    assert provider.calls == 0 and len(agent._requests) == 32
    assert agent.run("mean Alex", request_id="last-identity") == paused


def test_foreign_request_does_not_read_or_modify_owned_trace(database, tmp_path):
    agent, provider, _ = agent_at(database, tmp_path, proposals=[])
    paused = agent.run("mean Alex", request_id="start")
    trace = tmp_path / "traces" / (paused["run_id"] + ".jsonl")
    original = trace.read_bytes()
    run = agent.run("mean Alex", request_id="start", session_id="foreign")
    resume = agent.resume(paused["clarification"], 1, request_id="start", session_id="foreign")
    for result in (run, resume):
        assert result["error"]["code"] == "RESUME_FORBIDDEN"
        assert result["events"] == [] and result["run_id"] == ""
    assert trace.read_bytes() == original and provider.calls == 0
