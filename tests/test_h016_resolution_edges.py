"""Independent boundary variants: production parsing is never replaced by test scope."""

import sqlite3

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
        ("university", "Mean for semester ID s1.", {"semester_id": "S1"}),
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
        ("university", "Show mean for course ID UNKNOWN_ID=3."),
        ("library", "Count open loans BOOK_ID=2."),
        ("university", "Mean for course ID 1 and 2."),
        ("university", "Mean for course IDs 1,2."),
        ("university", "Mean for course 1 or 2."),
        ("library", "Count open loans for reader ID 1 and 2."),
        ("library", "Count open loans for reader IDs 1,2."),
        ("university", "Show mean for course ID."),
        ("university", "Mean for course ID and teacher ID 10."),
        ("university", "Mean for course ID in S1."),
        ("university", "Mean for course 2.5."),
        ("university", "Mean for course 2abc."),
        ("university", "Mean for semester ID nope in S1."),
        ("university", "Mean for semester_id=S1 and semester_id=."),
        ("university", "Mean for semester ID S9 in S1."),
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


@pytest.mark.parametrize("kind", ["university", "library"])
def test_present_empty_catalog_rejects_unknown_explicit_id(tmp_path, kind):
    path, provider, _ = setup_run(tmp_path, kind)
    from universitydb.agent import Agent
    from universitydb.domain import University
    from universitydb.library import Library

    with sqlite3.connect(path) as connection:
        if kind == "library":
            connection.execute("DELETE FROM Loans")
            connection.execute("DELETE FROM Readers")
        else:
            connection.execute("DELETE FROM Enrollments")
            connection.execute("DELETE FROM Students")
    domain = University() if kind == "university" else Library()
    question = (
        "Mean for student ID 1" if kind == "university" else "Count open loans for reader ID 1"
    )
    agent = Agent(domain, path, provider, tmp_path / "empty-traces")
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
    assert (
        domain.resolve(
            "Show mean" if kind == "university" else "Count open loans", domain.catalog(path)
        )
        == {}
    )


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Show mean for course -1."),
        ("university", "Show mean for course #abc."),
        ("library", "Count open loans for reader -1."),
        ("library", "Count open loans for reader #abc."),
        ("university", "Show mean for offering ID 1."),
        ("library", "Count open loans for book ID 1."),
        ("university", "Show mean for teacher Lee and teacher Kim, teacher ID 11."),
        ("university", 'Show mean for student named "Bea Nobody".'),
        ("library", 'Count open loans for reader named "Ada Nobody".'),
    ],
)
def test_architect_boundary_findings_fail_closed(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
    assert result["answer"] is None


@pytest.mark.parametrize("kind", ["university", "library"])
@pytest.mark.parametrize("named", [False, True])
def test_whole_quoted_multiword_catalog_labels(tmp_path, kind, named):
    from universitydb.agent import Agent
    from universitydb.domain import University
    from universitydb.library import Library

    path, provider, _ = setup_run(tmp_path, kind)
    with sqlite3.connect(path) as connection:
        if kind == "university":
            connection.execute("UPDATE Students SET name='Bea Rivera' WHERE student_id=2")
        else:
            connection.execute("UPDATE Readers SET name='Ada Lovelace' WHERE reader_id=1")
    domain = University() if kind == "university" else Library()
    question = (
        'Show mean for student named "Bea Rivera".'
        if kind == "university"
        else 'Count open loans for reader named "Ada Lovelace".'
    )
    if not named:
        question = question.replace(" named", "")
    agent = Agent(domain, path, provider, tmp_path / "quoted-traces")
    result = agent.run(question)
    assert result["status"] == "ok", result
    expected = {"student_id": 2} if kind == "university" else {"reader_id": 1}
    assert provider.scopes == [expected, expected]


def test_ambiguous_label_and_explicit_id_intersect_not_conflict(tmp_path):
    _, provider, agent = setup_run(tmp_path, "university")
    result = agent.run("Show mean for Alex, student ID 3.")
    assert result["status"] == "ok", result
    assert provider.scopes == [{"student_id": 3}, {"student_id": 3}]
    assert result["answer"]["empty_reason"] == "no_grades"


@pytest.mark.parametrize(
    "kind,question",
    [
        ("library", 'Count open loans for "Zephyr".'),
        ("university", "Show mean in course ID with teacher ID 10."),
        ("university", "Show mean for course ID 1 excluding student ID 2."),
        ("university", "Show mean for all students except student ID 2."),
        ("library", "Count open loans excluding reader ID 1."),
    ],
)
def test_code_review_additional_fail_closed_findings(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0


@pytest.mark.parametrize("noun", [False, True])
def test_library_quoted_target_known_and_ambiguous_resume(tmp_path, noun):
    from universitydb.agent import Agent
    from universitydb.library import Library

    path, provider, agent = setup_run(tmp_path, "library")
    question = 'Count open loans for reader "Ada".' if noun else 'Count open loans for "Ada".'
    known = agent.run(question)
    assert known["status"] == "ok", known
    assert provider.scopes == [{"reader_id": 1}, {"reader_id": 1}]
    with sqlite3.connect(path) as connection:
        connection.execute("INSERT INTO Readers VALUES(3,'Ada')")
    agent = Agent(Library(), path, provider, tmp_path / "quoted-ambiguous-traces")
    paused = agent.run(question)
    assert paused["status"] == "clarification", paused
    assert provider.calls == 2
    assert {option["value"] for option in paused["clarification"]["options"]} == {1, 3}
    resumed = agent.resume(paused["clarification"], 3, request_id="quoted-choice")
    assert resumed["status"] == "ok", resumed
    assert resumed["answer"]["rows"] == [[3, "Ada", 0]]
    assert provider.scopes[-2:] == [{"reader_id": 3}, {"reader_id": 3}]


@pytest.mark.parametrize("mode", ["collision", "overlap", "both"])
def test_explicit_role_owns_catalog_name_span(tmp_path, mode):
    from universitydb.agent import Agent
    from universitydb.domain import University

    path, provider, _ = setup_run(tmp_path, "university")
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE Teachers SET name='Bea' WHERE teacher_id=11")
        if mode == "overlap":
            connection.execute("UPDATE Students SET name='Bea Rivera' WHERE student_id=2")
    question = (
        "Show mean for student Bea Rivera in semester S1."
        if mode == "overlap"
        else "Show mean for student Bea and teacher Bea in semester S1."
        if mode == "both"
        else "Show mean for student Bea in semester S1."
    )
    agent = Agent(University(), path, provider, tmp_path / "owned-traces")
    result = agent.run(question)
    expected = {"student_id": 2, "semester_id": "S1"}
    if mode == "both":
        expected["teacher_id"] = 11
    assert result["status"] == "ok", result
    assert provider.scopes == [expected, expected]
    if mode != "both":
        assert result["answer"]["rows"] == [["80.00", 2, 2]]


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", 'Show mean for student "Bea Nobody".'),
        ("library", 'Count open loans for reader "Ada Nobody".'),
    ],
)
def test_every_explicit_quoted_name_validates_whole_value(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0


@pytest.mark.parametrize("separate_semester", [False, True])
def test_owned_quoted_text_id_name_is_not_a_semester_filter(tmp_path, separate_semester):
    from universitydb.agent import Agent
    from universitydb.domain import University

    path, provider, _ = setup_run(tmp_path, "university")
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE Teachers SET name='S1' WHERE teacher_id=11")
    question = 'Show mean for teacher named "S1".'
    if separate_semester:
        question += " In semester S1."
    agent = Agent(University(), path, provider, tmp_path / "text-id-traces")
    result = agent.run(question)
    expected = {"teacher_id": 11}
    if separate_semester:
        expected["semester_id"] = "S1"
    assert result["status"] == "ok", result
    assert provider.scopes == [expected, expected]


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Show mean for student_id!=2."),
        ("university", "Show mean for course_id<>1."),
        ("university", "Show mean for teacher_id<=10."),
        ("library", "Count open loans for reader_id>1."),
    ],
)
def test_explicit_identity_non_equality_operators_reject(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0


@pytest.mark.parametrize(
    "question,selected",
    [
        ("Show mean for teacher ID 11.", 11),
        ("Show mean for teacher_id=11.", 11),
        ("Show mean for teacher 11.", 11),
        ('Show mean for teacher named "11".', 10),
    ],
)
def test_typed_id_span_is_not_numeric_catalog_name(tmp_path, question, selected):
    from universitydb.agent import Agent
    from universitydb.domain import University

    path, provider, _ = setup_run(tmp_path, "university")
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE Teachers SET name='11' WHERE teacher_id=10")
    agent = Agent(University(), path, provider, tmp_path / "typed-spans")
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert provider.scopes == [{"teacher_id": selected}, {"teacher_id": selected}]


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Show each student ID and course ID for enrollment rows in S1."),
        ("university", "List every teacher ID and course ID for enrollment rows in S1."),
        ("university", "Display all student IDs and course IDs for enrollment rows in S1."),
        ("university", "Return all student IDs and course IDs for enrollment rows in S1."),
        ("university", "Include every student ID and course ID for enrollment rows in S1."),
        ("library", "Show each reader ID and open loan count."),
        ("library", "List every reader ID and open loan count."),
        ("library", "Display all reader IDs and open loan counts."),
    ],
)
def test_quantified_identifier_projection_uses_output_grammar(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind, "enrollment_rows")
    result = agent.run(question)
    assert result["status"] == "ok", result
    expected = {"semester_id": "S1"} if kind == "university" else {}
    assert provider.scopes == [expected, expected]
    assert_trace(tmp_path, result)


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Show mean for each student ID."),
        ("university", "Show mean in every course ID."),
        ("library", "Show open loans for each reader ID."),
        ("library", "Show open loans for every reader ID with reader ID 1."),
    ],
)
def test_quantifier_does_not_turn_missing_target_into_projection(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Display open loans for reader ID 1."),
        ("university", "Return enrollment rows; DELETE all students."),
        ("library", "Include student ID 2 and open loan counts."),
    ],
)
def test_listing_verbs_preserve_write_and_cross_domain_guards(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
