"""Real SQLite + compiled graph portability, not real-model NL-to-SQL accuracy."""

from pathlib import Path

import pytest
from langgraph.graph.state import CompiledStateGraph

from universitydb import db
from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library
from universitydb.llm import ScriptedProvider
from universitydb.sql_policy import validate_sql


def scripted_step(spec, sql, params, step_id="one"):
    step = {
        "step_id": step_id,
        "purpose": "Offline fixture",
        "depends_on": [],
        "result_refs": [],
        "result_spec": spec.model_dump(),
    }
    plan = {
        "version": "1",
        "steps": [step],
        "needs_clarification": False,
        "clarification_field": None,
    }
    proposal = {
        "version": "1",
        "step_id": step_id,
        "result_spec": spec.model_dump(),
        "sql": sql,
        "parameters": [
            {
                "name": k,
                "type": "text" if type(v) is str else "integer",
                "integer_value": v if type(v) is int else None,
                "text_value": v if type(v) is str else None,
            }
            for k, v in params.items()
        ],
        "expected_columns": [c.name for c in spec.columns],
        "result_kind": "aggregate" if spec.shape == "aggregate" else "rows",
        "explanation": "Offline scripted SQL",
    }
    return plan, proposal


@pytest.mark.parametrize("kind", ["university", "library"])
def test_both_adapters_real_db_compiled_graph(tmp_path, kind):
    domain = University() if kind == "university" else Library()
    spec = make_spec("grade_mean") if kind == "university" else LIBRARY_SPEC
    resources = Path("resources") if kind == "university" else Path("resources/library")
    path = tmp_path / "database.sqlite"
    db.initialize(path, resources)
    sql, parameters = domain.query(spec, {})
    provider = ScriptedProvider(list(scripted_step(spec, sql, parameters)))
    agent = Agent(domain, path, provider, tmp_path / "trace")
    assert isinstance(agent.compiled, CompiledStateGraph)
    result = agent.run("mean across all enrollments" if kind == "university" else "open loan count")
    assert result["status"] == "ok", result
    assert provider.calls == 2
    assert len(result["step_results"]) == 1
    if kind == "university":
        assert result["answer"]["rows"][0][0] == "83.33"
    else:
        assert result["answer"]["rows"] == [[1, "Ada", 1], [2, "Bob", 1]]
    assert [e for e in result["events"] if e["kind"] == "db_result"]


def test_full_wire_gate_applies_to_scripted_provider(database, tmp_path):
    domain = University()
    original = domain.descriptor
    domain.descriptor = lambda: {**original(), "oversized": "x" * 12000}
    provider = ScriptedProvider([])
    result = Agent(domain, database, provider, tmp_path / "trace").run("mean all")
    assert result["error"]["code"] == "RESOURCE_LIMIT"
    assert provider.calls == 0


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE X",
        "SELECT 1; SELECT 2",
        "SELECT * FROM (SELECT * FROM X)",
        "SELECT load_extension(:x) FROM X",
    ],
)
def test_shared_ast_boundary(sql):
    with pytest.raises(Failure):
        validate_sql(sql, {}, {"X": ["id"]}, ["count"])


def test_db_declared_null_and_empty_columns(database):
    spec = make_spec("grade_mean", "course_id")
    domain = University()
    sql, params = domain.query(spec, {"semester_id": "S99"})
    raw = db.execute(database, sql, params, domain.tables, domain.functions, result_spec=spec)
    assert raw["rows"] == []
    assert raw["columns"] == [{"name": c.name, "type": c.type} for c in spec.columns]


def test_adapter_schema_instances_reject_foreign_plan(database, tmp_path):
    """A provider's foreign registered spec never crosses the chosen DB adapter."""
    path = tmp_path / "library.sqlite"
    db.initialize(path, Path("resources/library"))
    university = University()
    library = Library()
    for domain, database_path, foreign, spec in (
        (university, database, library, LIBRARY_SPEC),
        (library, path, university, make_spec("grade_mean")),
    ):
        sql, params = foreign.query(spec, {})
        provider = ScriptedProvider(list(scripted_step(spec, sql, params)))
        agent = Agent(domain, database_path, provider, tmp_path / domain.descriptor()["schema_id"])
        result = agent.run("mean all" if domain is university else "open loan count")
        assert result["status"] == "error"
        assert result["error"]["code"] == "RESULT_CONTRACT_INVALID"
        assert provider.calls == 1
        assert not any(e["kind"] == "sql_attempt" for e in result["events"])


def test_ambiguous_name_is_clarification_not_unsupported(database, tmp_path):
    """Accepted I2 semantic change from I1's blanket rejection of 'mean Alex'."""
    provider = ScriptedProvider([])
    result = Agent(University(), database, provider, tmp_path / "trace").run("mean Alex")
    assert result["status"] == "clarification"
    assert result["error"] is None
    assert {option["value"] for option in result["clarification"]["options"]} == {1, 3}
    assert provider.calls == 0
    assert not any(e["kind"] == "sql_attempt" for e in result["events"])


def test_locked_database_startup_fails_without_provider(database, tmp_path):
    import sqlite3

    connection = sqlite3.connect(database)
    connection.execute("BEGIN EXCLUSIVE")
    try:
        provider = ScriptedProvider([])
        result = Agent(University(), database, provider, tmp_path / "locked").run("mean all")
        assert result["error"]["code"] == "DB_UNAVAILABLE"
        assert provider.calls == 0 and result["answer"] is None
    finally:
        connection.rollback()
        connection.close()


@pytest.mark.parametrize("location", ["plan_scale", "sql_binding"])
def test_provider_extreme_integer_rejected_before_saver_or_sql(database, tmp_path, location):
    from conftest import QUESTION, outputs

    proposals = outputs()
    if location == "plan_scale":
        proposals[0]["steps"][0]["result_spec"]["scale"] = 10**100
    else:
        proposals[1]["parameters"][0]["integer_value"] = 10**100
    provider = ScriptedProvider(proposals)
    result = Agent(University(), database, provider, tmp_path / "extreme").run(QUESTION)
    assert result["error"]["code"] == "PROVIDER_INVALID_OUTPUT", result
    assert result["answer"] is None
    assert provider.calls == (1 if location == "plan_scale" else 2)
    assert not any(e["kind"] == "sql_attempt" for e in result["events"])
    assert result["events"][-1]["kind"] == "run_end"
