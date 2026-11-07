"""Isolated actual Streamlit/graph/SQLite; scripted proposals are NOT NL accuracy."""

import hashlib
import json
import shutil
from pathlib import Path

import pytest
from conftest import ROOT, outputs
from streamlit.testing.v1 import AppTest
from ui_fixtures import plan, proposal, step

from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library


@pytest.fixture
def isolated_app(tmp_path, monkeypatch):
    root = tmp_path / "app"
    shutil.copytree(ROOT / "resources", root / "resources")
    fixture = tmp_path / "injected.json"
    monkeypatch.setenv("UNIVERSITYDB_ROOT", str(root))
    monkeypatch.setenv("UNIVERSITYDB_TEST_MODE", "1")
    monkeypatch.setenv("UNIVERSITYDB_TEST_FIXTURE", str(fixture))
    monkeypatch.setenv("UNIVERSITYDB_LIVE_APPROVED", "no")
    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    before = {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (ROOT / "runtime").rglob("*")
        if p.is_file()
    }
    yield root, fixture
    after = {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (ROOT / "runtime").rglob("*")
        if p.is_file()
    }
    assert after == before, "AppTest must not touch the repository runtime/ledger"


def app_with(fixture: Path, values):
    fixture.write_text(json.dumps(values))
    app = AppTest.from_file(str(ROOT / "src/universitydb/ui.py"), default_timeout=30).run()
    assert not app.exception
    return app


def test_agent_retained_across_ui_rerun(isolated_app):
    _, fixture = isolated_app
    app = app_with(fixture, outputs())
    initial_agent = app.session_state["agent"]
    app.button[0].click().run()
    assert not app.exception and app.success and "80.00" in app.success[0].value
    run_id = app.session_state["result"]["run_id"]
    app.run()
    assert app.session_state["agent"] is initial_agent
    assert app.session_state["result"]["run_id"] == run_id
    assert initial_agent.provider.calls == 2
    assert any("same-run trace" in e.label for e in app.expander)


def test_dataset_switch_clears_answer_and_uses_separate_db(isolated_app):
    root, fixture = isolated_app
    lib = Library()
    app = app_with(
        fixture,
        {
            "university-v1": outputs(),
            "library-v1": [plan(step(LIBRARY_SPEC)), proposal(lib, LIBRARY_SPEC, {})],
        },
    )
    app.button[0].click().run()
    assert app.success and "80.00" in app.success[0].value
    university_agent = app.session_state["agent"]
    app.selectbox[0].select("Library").run()
    assert not app.exception and not app.success
    assert app.session_state["agent"] is not university_agent
    app.text_area[0].set_value("How many open loans does each reader have?")
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    answer = app.session_state["result"]["answer"]
    assert answer["rows"] == [[1, "Ada", 1], [2, "Bob", 1]]
    assert answer["columns"][-1]["name"] == "open_count"
    assert (root / "runtime/university-v1.db").exists()
    assert (root / "runtime/library-v1.db").exists()
    assert not (root / "runtime/spending.json").exists()


def test_injected_refusal_clears_old_success_and_shows_full_error_trace(isolated_app):
    _, fixture = isolated_app
    app = app_with(
        fixture,
        outputs()
        + [
            {"injected_error": {"code": "PROVIDER_REFUSAL", "message": "Offline injected refusal."}}
        ],
    )
    app.button[0].click().run()
    assert app.success
    app.button[0].click().run()
    assert not app.exception and not app.success
    assert "PROVIDER_REFUSAL" in app.error[0].value
    result = app.session_state["result"]
    assert result["execution_profile"] == "offline/injected"
    assert not any(e["kind"] == "db_result" for e in result["events"])
    assert result["events"][-1]["kind"] == "run_end"
    assert all(e["run_id"] == result["run_id"] for e in result["events"])


def test_real_checkpoint_pause_resume_retained_same_run_and_no_replayed_calls(isolated_app):
    from universitydb.domain import University, make_spec

    _, fixture = isolated_app
    spec = make_spec("grade_mean")
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, {"student_id": 1})])
    app.text_area[0].set_value("What is the average grade for Alex?")
    app.button[0].click().run()
    assert not app.exception and not app.success
    paused = app.session_state["result"]
    agent = app.session_state["agent"]
    assert paused["status"] == "clarification"
    assert [option["value"] for option in paused["clarification"]["options"]] == [1, 3]
    assert agent.provider.calls == 0
    assert not any(e["kind"] == "sql_attempt" for e in paused["events"])
    assert app.selectbox[1].options == ["Alex (ID: 1)", "Alex (ID: 3)"]
    app.button[1].click().run()
    assert not app.exception and app.success and "86.67" in app.success[0].value
    resumed = app.session_state["result"]
    assert resumed["run_id"] == paused["run_id"]
    assert any(e["kind"] == "resume" for e in resumed["events"])
    assert agent.provider.calls == 2
    app.run()
    assert app.session_state["agent"] is agent and agent.provider.calls == 2
    assert app.session_state["result"]["run_id"] == paused["run_id"]


def test_current_semester_choice_and_expired_resume_no_calls(isolated_app):
    from universitydb.domain import University, make_spec

    _, fixture = isolated_app
    spec = make_spec("grade_mean")
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, {"semester_id": "S1"})])
    app.text_area[0].set_value("What is the average grade in the current semester?")
    app.button[0].click().run()
    assert not app.exception and app.session_state["result"]["status"] == "clarification"
    agent = app.session_state["agent"]
    now = agent._now()
    agent._now = lambda: now + 901
    app.button[1].click().run()
    assert not app.exception and not app.success
    assert "RESUME_EXPIRED" in app.error[0].value
    assert agent.provider.calls == 0


def test_current_semester_selection_uses_actual_same_run(isolated_app):
    from universitydb.domain import University, make_spec

    _, fixture = isolated_app
    spec = make_spec("grade_mean")
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, {"semester_id": "S1"})])
    app.text_area[0].set_value("What is the average grade in the current semester?")
    app.button[0].click().run()
    run_id = app.session_state["result"]["run_id"]
    app.button[1].click().run()
    assert not app.exception and app.success and "87.50" in app.success[0].value
    assert app.session_state["result"]["run_id"] == run_id


def test_library_ambiguity_and_schema_switch_cannot_resume_foreign_run(isolated_app):
    import sqlite3

    _, fixture = isolated_app
    app = app_with(
        fixture,
        {
            "university-v1": outputs(),
            "library-v1": [
                plan(step(LIBRARY_SPEC)),
                proposal(Library(), LIBRARY_SPEC, {"reader_id": 2}),
            ],
        },
    )
    app.selectbox[0].select("Library").run()
    assert "Bea" not in app.text_area[0].value
    agent = app.session_state["agent"]
    with sqlite3.connect(agent.database) as connection:
        connection.execute("UPDATE Readers SET name='Ada' WHERE reader_id=2")
    app.text_area[0].set_value("How many open loans for Ada?")
    app.button[0].click().run()
    paused = app.session_state["result"]
    assert paused["status"] == "clarification" and agent.provider.calls == 0
    # Form values are delivered with its submit, not a forced pre-submit rerun.
    app.selectbox[1].select(1)
    app.button[1].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    assert app.session_state["result"]["answer"]["rows"] == [[2, "Ada", 1]]
    app.selectbox[0].select("University").run()
    assert not app.success
    other = app.session_state["agent"]
    rejected = other.resume(paused["clarification"], 2, request_id="foreign-ui-test")
    assert rejected["status"] == "error"
    assert rejected["error"]["code"] in ("RESUME_FORBIDDEN", "RESUME_EXPIRED")
    assert other.provider.calls == 0


def test_repair_attempts_visible_and_library_zero_not_grade_scaled(isolated_app):
    import sqlite3
    from copy import deepcopy

    root, fixture = isolated_app
    values = outputs()
    invalid = deepcopy(values[1])
    invalid["sql"] = invalid["sql"].replace("e.grade_units", "e.unknown_grade_units")
    app = app_with(
        fixture,
        {
            "university-v1": [values[0], invalid, values[1]],
            "library-v1": [plan(step(LIBRARY_SPEC)), proposal(Library(), LIBRARY_SPEC, {})],
        },
    )
    app.button[0].click().run()
    assert not app.exception and app.success and "80.00" in app.success[0].value
    events = app.session_state["result"]["events"]
    assert any(e["kind"] == "error" and e["payload"].get("repair") for e in events)
    assert app.session_state["agent"].provider.calls == 3
    assert any("unknown_grade_units" in e.value for e in app.json)
    assert any("unknown_grade_units" in e.value for e in app.code)
    app.selectbox[0].select("Library").run()
    with sqlite3.connect(root / "runtime/library-v1.db") as connection:
        connection.execute("UPDATE Loans SET returned=1")
        connection.execute("INSERT INTO Readers VALUES(3,'Cy')")
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    assert app.session_state["result"]["answer"]["rows"] == [
        [1, "Ada", 0],
        [2, "Bob", 0],
        [3, "Cy", 0],
    ]


def test_missing_database_safe_error_no_stale_answer(isolated_app):
    _, fixture = isolated_app
    app = app_with(fixture, outputs() + outputs())
    app.button[0].click().run()
    assert app.success
    app.session_state["agent"].database.unlink()
    app.button[0].click().run()
    assert not app.exception and not app.success
    assert "DB_UNAVAILABLE" in app.error[0].value


@pytest.mark.parametrize("fixture_name", ["F1", "F2"])
def test_m1_ui_all_actual_step_rows_bindings_and_final_means(isolated_app, fixture_name):
    import sqlite3

    from ui_fixtures import m1_outputs

    root, fixture = isolated_app
    oracle = json.loads((ROOT / "docs/operations/H-013/frozen-oracle.json").read_text())["m1"][
        fixture_name
    ]
    app = app_with(fixture, m1_outputs(oracle["top_course_ids"], oracle["cohort_student_ids"]))
    if fixture_name == "F2":
        with sqlite3.connect(root / "runtime/university-v1.db") as connection:
            connection.execute("INSERT INTO Enrollments VALUES(3,2,5000)")
    app.text_area[0].set_value(
        "For students of the course with the highest mean in S1, show their mean across all S1 courses."
    )
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    result = app.session_state["result"]
    assert [outcome["step_id"] for outcome in result["step_results"]] == ["top", "cohort", "means"]
    assert [row[0] for row in result["step_results"][0]["dependency_rows"]] == oracle[
        "top_course_ids"
    ]
    assert [row[0] for row in result["step_results"][1]["dependency_rows"]] == oracle[
        "cohort_student_ids"
    ]
    assert [row[1] for row in result["answer"]["rows"]] == [
        entry["mean"] for entry in oracle["final"]
    ]
    assert len([e for e in result["events"] if e["kind"] == "db_result"]) == 3
    assert any("course_ids_0" in block.value for block in app.code)
    assert any("student_ids_0" in block.value for block in app.code)
    assert any("dependency_rows" in block.value for block in app.json)
    assert result["events"][-1]["kind"] == "run_end"
    assert app.session_state["agent"].provider.calls == 4
