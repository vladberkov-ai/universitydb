"""Affected H016 natural text through real Streamlit, graph, temporary SQLite.

Fixed provider plan/SQL proposals are explicit offline UI fixtures, not accuracy
proof. The text_area is the only scope input; production resolver must agree with
proposal bindings or validation rejects them. Repository runtime is preserved by
the existing isolated_app fixture. No credentials/live provider are enabled.
"""

import json

import pytest
from test_i2_ui import app_with
from test_i2_ui import isolated_app as isolated_app  # noqa: PLC0414 -- fixture registration
from ui_fixtures import plan, proposal, step

from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library


def assert_visible_trace(app):
    result = app.session_state["result"]
    panel = next(item for item in app.expander if item.label == "Full same-run trace")
    assert json.loads(panel.json[0].value) == result["events"]
    assert result["events"][-1]["kind"] == "run_end"
    assert not app.exception


def test_combined_natural_id_filters_visible_answer_scope_and_trace(isolated_app):
    _, fixture = isolated_app
    spec = make_spec("grade_mean")
    scope = {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, scope)])
    question = "Mean for student ID 2, course ID 1, teacher ID 10, in semester S1."
    app.text_area[0].set_value(question)
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    assert "80.00" in app.success[0].value
    result = app.session_state["result"]
    assert result["answer"]["rows"] == [["80.00", 2, 2]]
    assert all(f"{key}={value}" in result["answer"]["scope"] for key, value in scope.items())
    assert app.text_area[0].value == question
    assert app.session_state["agent"].provider.calls == 2
    assert any(":teacher_id" in block.value for block in app.code)
    assert_visible_trace(app)


def test_natural_output_id_projection_reaches_real_listing(isolated_app):
    _, fixture = isolated_app
    spec = make_spec("enrollment_rows")
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, {"course_id": 1})])
    app.text_area[0].set_value("List student IDs, course ID and grades for course ID 1.")
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    result = app.session_state["result"]
    assert result["answer"]["rows"] == [
        [1, "Alex", 1, 1, "DB", 10, "Kim", "S1", 9000],
        [2, "Bea", 1, 1, "DB", 10, "Kim", "S1", 6000],
        [3, "Alex", 1, 1, "DB", 10, "Kim", "S1", None],
        [1, "Alex", 3, 1, "DB", 11, "Lee", "S2", 7000],
        [2, "Bea", 3, 1, "DB", 11, "Lee", "S2", 8000],
        [2, "Bea", 5, 1, "DB", 10, "Kim", "S1", 10000],
    ]
    assert "course_id=1" in result["answer"]["scope"]
    assert any("grade_units" in block.value for block in app.code)
    assert_visible_trace(app)


def test_output_id_projection_does_not_replace_same_run_ambiguity(isolated_app):
    _, fixture = isolated_app
    spec = make_spec("grade_mean")
    app = app_with(fixture, [plan(step(spec)), proposal(University(), spec, {"student_id": 3})])
    app.text_area[0].set_value("Show mean for Alex with student ID in output.")
    app.button[0].click().run()
    paused = app.session_state["result"]
    agent = app.session_state["agent"]
    assert paused["status"] == "clarification", paused
    assert agent.provider.calls == 0
    app.selectbox[1].select(1)
    app.button[1].click().run()
    result = app.session_state["result"]
    assert not app.exception and app.success, result.get("error")
    assert result["run_id"] == paused["run_id"]
    assert result["answer"]["rows"] == [[None, 0, 1]]
    assert result["answer"]["empty_reason"] == "no_grades"
    assert "student_id=3" in result["answer"]["scope"]
    assert agent.provider.calls == 2
    assert any(event["kind"] == "resume" for event in result["events"])
    assert_visible_trace(app)


def test_library_natural_filter_then_global_id_projection(isolated_app):
    _, fixture = isolated_app
    domain = Library()
    values = [
        plan(step(LIBRARY_SPEC)),
        proposal(domain, LIBRARY_SPEC, {"reader_id": 2}),
        plan(step(LIBRARY_SPEC)),
        proposal(domain, LIBRARY_SPEC, {}),
    ]
    app = app_with(fixture, {"university-v1": [], "library-v1": values})
    app.selectbox[0].select("Library").run()
    app.text_area[0].set_value("Count open loans for reader ID 2.")
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    assert app.session_state["result"]["answer"]["rows"] == [[2, "Bob", 1]]
    assert "reader_id=2" in app.session_state["result"]["answer"]["scope"]
    initial_id = app.session_state["result"]["run_id"]
    assert_visible_trace(app)
    app.text_area[0].set_value("For every reader show reader ID, name and open loan count.")
    app.button[0].click().run()
    result = app.session_state["result"]
    assert not app.exception and app.success, result.get("error")
    assert result["run_id"] != initial_id
    assert result["answer"]["rows"] == [[1, "Ada", 1], [2, "Bob", 1]]
    assert "reader_id=all" in result["answer"]["scope"]
    assert app.session_state["agent"].provider.calls == 4
    assert_visible_trace(app)


@pytest.mark.parametrize(
    "kind,negative",
    [
        ("university", "Mean for student ID 999."),
        ("university", "Mean for Bea, student ID 1."),
        ("library", "Count open loans for reader ID 999."),
        ("library", "Count open loans for Ada, reader ID 2."),
    ],
)
def test_unknown_and_conflicting_natural_ids_clear_previous_success(isolated_app, kind, negative):
    _, fixture = isolated_app
    if kind == "university":
        spec, domain, scope = make_spec("grade_mean"), University(), {"student_id": 2}
        question = "Mean for student ID 2."
    else:
        spec, domain, scope = LIBRARY_SPEC, Library(), {"reader_id": 2}
        question = "Count open loans for reader ID 2."
    values = [plan(step(spec)), proposal(domain, spec, scope)]
    app = app_with(
        fixture, values if kind == "university" else {"university-v1": [], "library-v1": values}
    )
    if kind == "library":
        app.selectbox[0].select("Library").run()
    app.text_area[0].set_value(question)
    app.button[0].click().run()
    assert not app.exception and app.success, app.session_state["result"].get("error")
    agent = app.session_state["agent"]
    assert agent.provider.calls == 2
    app.text_area[0].set_value(negative)
    app.button[0].click().run()
    result = app.session_state["result"]
    assert not app.exception and not app.success
    assert result["answer"] is None
    assert result["error"]["code"] == "INVALID_INPUT"
    assert "INVALID_INPUT" in app.error[0].value
    assert agent.provider.calls == 2
    assert not any(event["kind"] == "db_result" for event in result["events"])
    assert_visible_trace(app)
