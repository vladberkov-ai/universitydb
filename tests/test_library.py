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
