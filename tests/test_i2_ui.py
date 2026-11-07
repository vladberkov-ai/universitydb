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
    app = AppTest.from_file(str(ROOT / "src/universitydb/ui.py")).run()
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
    assert not app.exception and app.success
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
