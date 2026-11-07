"""Actual Streamlit magic must not render UI method return values as content."""

import json

from conftest import outputs
from test_i2_ui import app_with
from test_i2_ui import isolated_app as isolated_app  # noqa: PLC0414 -- pytest fixture registration


def assert_no_magic_returns(app):
    assert not app.exception
    assert not app.get("help_info"), "Bare UI return value rendered API help"
    assert all(block.value.strip().strip("`") != "None" for block in app.markdown)


def test_actual_magic_success_then_refusal_has_rows_trace_without_help(isolated_app):
    _, fixture = isolated_app
    app = app_with(
        fixture,
        outputs()
        + [{"injected_error": {"code": "PROVIDER_REFUSAL", "message": "Offline refusal."}}],
    )
    app.button[0].click().run()
    assert app.success and "80.00" in app.success[0].value
    result = app.session_state["result"]
    db_panel = next(e for e in app.expander if e.label == "DB typed rows")
    expected = [e["payload"] for e in result["events"] if e["kind"] == "db_result"]
    assert [json.loads(block.value) for block in db_panel.json] == [expected]
    adapted = next(e for e in app.expander if e.label.startswith("Adapted step"))
    assert "dependency_rows" in adapted.json[0].value
    trace = next(e for e in app.expander if e.label == "Full same-run trace")
    assert json.loads(trace.json[0].value) == result["events"]
    assert result["events"][-1]["kind"] == "run_end"
    assert_no_magic_returns(app)
    app.button[0].click().run()
    assert not app.success and "PROVIDER_REFUSAL" in app.error[0].value
    db_panel = next(e for e in app.expander if e.label == "DB typed rows")
    assert not db_panel.json
    assert [block.value for block in db_panel.markdown] == ["DB query was not executed."]
    adapted = next(e for e in app.expander if e.label.startswith("Adapted step"))
    assert not adapted.json
    assert [block.value for block in adapted.markdown] == ["No adapted step results yet."]
    result = app.session_state["result"]
    assert not any(e["kind"] == "db_result" for e in result["events"])
    assert result["events"][-1]["kind"] == "run_end"
    assert_no_magic_returns(app)


def test_actual_magic_clarification_empty_panels_without_none(isolated_app):
    _, fixture = isolated_app
    app = app_with(fixture, outputs())
    app.text_area[0].set_value("What is the average grade for Alex?")
    app.button[0].click().run()
    assert app.session_state["result"]["status"] == "clarification"
    assert not app.success
    assert app.session_state["agent"].provider.calls == 0
    assert_no_magic_returns(app)


def test_actual_magic_refusal_empty_panels_without_none(isolated_app):
    _, fixture = isolated_app
    app = app_with(
        fixture,
        [{"injected_error": {"code": "PROVIDER_REFUSAL", "message": "Offline refusal."}}],
    )
    app.button[0].click().run()
    assert not app.success and "PROVIDER_REFUSAL" in app.error[0].value
    assert_no_magic_returns(app)
