"""Library exercises the same real DB and compiled core as University."""

import json
import sqlite3
from pathlib import Path

import pytest
from test_i2_domains import proposal_for, step_for

from universitydb import db
from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.library import SPEC, Library
from universitydb.llm import ScriptedProvider

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((ROOT / "docs/operations/H-013/frozen-oracle.json").read_text())["library"]


@pytest.fixture
def library_db(tmp_path):
    path = tmp_path / "library.db"
    db.initialize(path, ROOT / "resources/library")
    return path


def actual(path):
    domain = Library()
    db.inspect(path, domain.tables)
    domain.inspect_data(path)
    p = proposal_for(domain, SPEC, {})
    params = domain.validate_sql(p, {}, step=step_for(SPEC))
    raw = db.execute(path, p.sql, params, domain.tables, domain.functions, result_spec=SPEC)
    return domain.adapt_result(raw["rows"], SPEC, {})


def test_library_baseline_zero_returned_mutations_and_scale(library_db):
    assert actual(library_db)["answer"]["rows"] == EXPECTED["expected"]
    assert SPEC.unit == "count" and SPEC.scale == 1
    assert actual(library_db)["answer"]["columns"] == [
        {"name": c.name, "type": c.type} for c in SPEC.columns
    ]
    with sqlite3.connect(library_db) as conn:
        conn.execute("INSERT INTO Readers VALUES(3,'Cy')")
    assert actual(library_db)["answer"]["rows"] == EXPECTED["reader_without_loans"]
    with sqlite3.connect(library_db) as conn:
        conn.execute("DELETE FROM Readers WHERE reader_id=3")
        conn.execute("UPDATE Loans SET returned=1 WHERE loan_id=1")
    assert actual(library_db)["answer"]["rows"] == EXPECTED["returned_mutation"]
    with sqlite3.connect(library_db) as conn:
        conn.execute("UPDATE Loans SET returned=1")
    assert actual(library_db)["answer"]["rows"] == EXPECTED["all_returned"]


def test_library_compiled_core_smoke(library_db, tmp_path):
    p = proposal_for(Library(), SPEC, {})
    plan = {
        "version": "1",
        "steps": [step_for(SPEC).model_dump()],
        "needs_clarification": False,
        "clarification_field": None,
    }
    provider = ScriptedProvider([plan, p.model_dump()])
    result = Agent(Library(), library_db, provider, tmp_path / "traces").run(
        "Count open loans per reader"
    )
    assert result["status"] == "ok", result.get("error")
    assert result["answer"]["rows"] == EXPECTED["expected"]
    assert [e for e in result["events"] if e["kind"] == "db_result"]


def test_library_name_ambiguity(library_db):
    with sqlite3.connect(library_db) as conn:
        conn.execute("INSERT INTO Readers VALUES(3,'Ada')")
    domain = Library()
    with pytest.raises(Failure) as caught:
        domain.resolve("Open loans Ada", domain.catalog(library_db))
    assert caught.value.code == "CLARIFICATION_REQUIRED"
    assert [o["value"] for o in caught.value.details["options"]] == [1, 3]
    assert domain.resolve("Open loans Ada", domain.catalog(library_db), {"reader_id": 3}) == {
        "reader_id": 3
    }


def test_library_fk_corruption_and_cross_schema(library_db, database):
    with sqlite3.connect(library_db) as conn:
        conn.execute("UPDATE Loans SET reader_id=999 WHERE loan_id=1")
    with pytest.raises(Failure, match="foreign keys"):
        db.inspect(library_db, Library.tables)
    with pytest.raises(Failure, match="table set"):
        db.inspect(database, Library.tables)


def test_library_returned_range_corruption(library_db):
    with sqlite3.connect(library_db) as conn:
        conn.execute("PRAGMA ignore_check_constraints=ON")
        conn.execute("UPDATE Loans SET returned=2 WHERE loan_id=1")
    with pytest.raises(Failure, match="returned"):
        Library().inspect_data(library_db)


def test_library_null_and_boolean_results_rejected():
    for rows in [
        [[1, "Ada", None]],
        [[1, "Ada", True]],
        [[1, "Ada", -1]],
        [[1, "Ada", 1], [1, "Ada", 2]],
    ]:
        with pytest.raises(Failure):
            Library().adapt_result(rows, SPEC, {})


def test_library_wrong_returned_storage_type_detected(library_db):
    with sqlite3.connect(library_db) as conn:
        conn.executescript(
            "ALTER TABLE Loans RENAME TO OldLoans; CREATE TABLE Loans(loan_id INTEGER, reader_id INTEGER, book_id INTEGER, returned); INSERT INTO Loans SELECT loan_id,reader_id,book_id,returned FROM OldLoans; DROP TABLE OldLoans;"
        )
        conn.execute("UPDATE Loans SET returned='false' WHERE loan_id=1")
    with pytest.raises(Failure, match="column type"):
        Library().inspect_data(library_db)


def test_library_real_checkpoint_ambiguity_and_selected_zero(library_db, tmp_path):
    with sqlite3.connect(library_db) as conn:
        conn.execute("INSERT INTO Readers VALUES(3,'Ada')")
    domain = Library()
    p = proposal_for(domain, SPEC, {"reader_id": 3})
    plan = {
        "version": "1",
        "steps": [step_for(SPEC).model_dump()],
        "needs_clarification": False,
        "clarification_field": None,
    }
    provider = ScriptedProvider([plan, p.model_dump()])
    agent = Agent(domain, library_db, provider, tmp_path / "traces")
    paused = agent.run("Open loans Ada")
    assert paused["status"] == "clarification" and provider.calls == 0
    assert [o["value"] for o in paused["clarification"]["options"]] == [1, 3]
    result = agent.resume(paused["clarification"], 3, request_id="selected-reader")
    assert result["status"] == "ok", result
    assert result["answer"]["rows"] == [[3, "Ada", 0]]
    assert provider.calls == 2 and result["run_id"] == paused["run_id"]
    assert agent.resume(paused["clarification"], 3, request_id="selected-reader") == result
    assert provider.calls == 2


def test_library_provider_clarification_options_grounded(library_db):
    domain = Library()
    assert domain.clarification_options("reader_id", domain.catalog(library_db)) == [
        {"value": 1, "label": "Ada"},
        {"value": 2, "label": "Bob"},
    ]
    with pytest.raises(Failure, match="not registered"):
        domain.clarification_options("student_id", domain.catalog(library_db))


@pytest.mark.parametrize(
    "question",
    [
        "DROP TABLE Readers",
        "average grade all",
        "Mean all students",
        "List books",
        "How many readers?",
        "Count all loans",
        "Count returned loans",
        "Open loans student_id=1",
        "nonsense",
    ],
)
def test_library_unsupported_or_write_intent_no_calls(library_db, tmp_path, question):
    provider = ScriptedProvider([])
    result = Agent(Library(), library_db, provider, tmp_path / "traces").run(question)
    assert result["status"] == "error"
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
    assert not [e for e in result["events"] if e["kind"] == "sql_attempt"]


@pytest.mark.parametrize(
    "question", ["Open loans Zed", "Open loans reader named Zed", "Open loans reader_id=-1"]
)
def test_library_unknown_name_never_unfilters(library_db, tmp_path, question):
    provider = ScriptedProvider([])
    result = Agent(Library(), library_db, provider, tmp_path / "traces").run(question)
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0


def test_library_catalog_bound_and_owned_reads_missing_fail_closed(library_db, tmp_path):
    domain = Library()
    with sqlite3.connect(library_db) as conn:
        conn.executemany(
            "INSERT INTO Readers VALUES(?,?)", [(i, f"Reader{i}") for i in range(3, 1003)]
        )
    with pytest.raises(Failure, match="1000 entity"):
        domain.catalog(library_db)
    for read in [domain.catalog, domain.inspect_data]:
        with pytest.raises(Failure) as caught:
            read(tmp_path / "missing.sqlite")
        assert caught.value.code == "DB_UNAVAILABLE"


def test_library_natural_all_reader_count_does_not_invent_identity(library_db, tmp_path):
    question = "How many open loans does each reader have?"
    domain = Library()
    assert domain.resolve(question, domain.catalog(library_db)) == {}
    p = proposal_for(domain, SPEC, {})
    plan = {
        "version": "1",
        "steps": [step_for(SPEC).model_dump()],
        "needs_clarification": False,
        "clarification_field": None,
    }
    provider = ScriptedProvider([plan, p.model_dump()])
    result = Agent(domain, library_db, provider, tmp_path / "traces").run(question)
    assert result["status"] == "ok", result
    assert result["answer"]["rows"] == EXPECTED["expected"]


def test_library_owned_reads_locked_classification(library_db):
    domain = Library()
    with sqlite3.connect(library_db) as conn:
        conn.execute("BEGIN EXCLUSIVE")
        for read in [domain.catalog, domain.inspect_data]:
            with pytest.raises(Failure) as caught:
                read(library_db)
            assert caught.value.code == "DB_UNAVAILABLE"
