"""Independent boundary variants: production parsing is never replaced by test scope."""

import pytest
from test_h016_natural_scope import assert_trace, setup_run


@pytest.mark.parametrize(
    "kind,question,scope",
    [
        ("university", "Show mean for course ID: 2.", {"course_id": 2}),
        ("university", "Show mean for student ID=2!", {"student_id": 2}),
        ("university", "Show mean for teacher ID #11?", {"teacher_id": 11}),
        ("university", "Show mean for STUDENT_ID=2.", {"student_id": 2}),
        ("university", "Mean for course #2.", {"course_id": 2}),
        ("university", "Mean for course 2, COURSE id 2.", {"course_id": 2}),
        ("university", "Mean for Bea, student ID 2.", {"student_id": 2}),
        ("library", "Count open loans for reader ID: 2.", {"reader_id": 2}),
        ("library", "Count open loans for READER_ID=1!", {"reader_id": 1}),
        ("library", "Count open loans for reader #1, reader ID 1.", {"reader_id": 1}),
    ],
)
def test_identity_syntax_variants_use_actual_scope(tmp_path, kind, question, scope):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert provider.scopes == [scope, scope]
    assert_trace(tmp_path, result)


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Mean for course ID 2abc."),
        ("university", "Mean for course ID 2.5."),
        ("university", "Mean for course ID +2."),
        ("university", "Mean for course ID: nope."),
        ("university", "Mean for course ID."),
        ("university", "Mean for course_id=1 and course_id=."),
        ("university", "Mean for student named Zephyr and Bea."),
        ("university", "Mean for student named Zephyr, student ID 2."),
        ("university", "Mean for Bea, student ID 2 and student ID nope."),
        ("library", "Count open loans for reader ID 1abc."),
        ("library", "Count open loans for reader ID 1.5."),
        ("library", "Count open loans for reader ID +1."),
        ("library", "Count open loans for reader ID: nope."),
        ("library", "Count open loans for reader ID."),
        ("library", "Count open loans for reader_id=1 and reader_id=."),
        ("library", "Count open loans for Ada, reader named Zephyr."),
        ("library", "Count open loans for reader named Zephyr, reader ID 1."),
        ("library", "Count open loans for Ada, reader ID 1 and reader ID nope."),
    ],
)
def test_every_explicit_identity_is_validated_before_provider(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
    assert result["answer"] is None
    assert not any(event["kind"] == "sql_attempt" for event in result["events"])
    assert_trace(tmp_path, result)
