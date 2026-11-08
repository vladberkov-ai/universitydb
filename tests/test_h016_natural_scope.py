"""Independent natural-input regressions; scripted transport is NOT model accuracy.

No H015 questions/oracles/artifacts are imported. Only Agent.run receives the
question: the transport consumes production-resolved scope, never test scope.
Expected scopes are assertions and independent SQLite oracle inputs only.
"""

import json
import sqlite3
from copy import deepcopy
from pathlib import Path

import pytest
from langgraph.graph.state import CompiledStateGraph
from test_i2_core import scripted_step

from universitydb import db
from universitydb.agent import Agent
from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library
from universitydb.llm import ScriptedProvider


class ResolvedScopeTransport(ScriptedProvider):
    """Offline plan/SQL fixture boundary, using actual production payload scope."""

    def __init__(self, domain, spec):
        super().__init__([])
        self.domain = domain
        self.spec = spec
        self.scopes = []

    def call(self, operation, payload, output_type, *, timeout=180):
        self.calls += 1
        scope = deepcopy(payload["scope"])
        self.scopes.append(scope)
        sql, params = self.domain.query(self.spec, scope)
        plan, proposal = scripted_step(self.spec, sql, params)
        value = plan if operation == "plan" else proposal
        return output_type.model_validate(value), {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "real_provider_called": False,
            "injection_point": "h016_actual_resolved_scope_transport",
        }


def setup_run(tmp_path, kind, metric="grade_mean"):
    domain = University() if kind == "university" else Library()
    spec = make_spec(metric) if kind == "university" else LIBRARY_SPEC
    path = tmp_path / "fixture.sqlite"
    resources = Path(__file__).resolve().parents[1] / "resources"
    db.initialize(path, resources if kind == "university" else resources / "library")
    provider = ResolvedScopeTransport(domain, spec)
    agent = Agent(domain, path, provider, tmp_path / "traces")
    assert isinstance(agent.compiled, CompiledStateGraph)
    return path, provider, agent


def assert_trace(tmp_path, result):
    persisted = [
        json.loads(line)
        for line in (tmp_path / "traces" / (result["run_id"] + ".jsonl")).read_text().splitlines()
    ]
    assert persisted == result["events"]
    assert persisted[-1]["kind"] == "run_end"
    assert [event["seq"] for event in persisted] == list(range(1, len(persisted) + 1))


def university_oracle(path, scope, metric):
    """Independent SQL, not domain.query/adapt_result or frozen campaign oracle."""
    predicates = []
    for field in scope:
        alias = "e" if field == "student_id" else "o"
        predicates.append(f"{alias}.{field} = :{field}")
    projection = (
        "e.student_id,s.name,e.offering_id,o.course_id,c.title,o.teacher_id,t.name,"
        "o.semester_id,e.grade_units"
        if metric == "enrollment_rows"
        else "COALESCE(SUM(e.grade_units),0),COUNT(e.grade_units),COUNT(*)"
    )
    sql = f"SELECT {projection} FROM Enrollments e JOIN Offerings o USING(offering_id) "
    if metric == "enrollment_rows":
        sql += (
            "JOIN Students s USING(student_id) JOIN Courses c USING(course_id) "
            "JOIN Teachers t USING(teacher_id) "
        )
    if predicates:
        sql += " WHERE " + " AND ".join(predicates)
    if metric == "enrollment_rows":
        sql += " ORDER BY e.offering_id,e.student_id"
    with sqlite3.connect(path) as connection:
        return [list(row) for row in connection.execute(sql, scope)]


@pytest.mark.parametrize(
    "question,scope",
    [
        ("Show the mean grade for course ID 2.", {"course_id": 2}),
        ("Average grade: student ID 2!", {"student_id": 2}),
        ("What is the mean for teacher ID 11?", {"teacher_id": 11}),
        ("Show mean for COURSE id 1.", {"course_id": 1}),
        ("Show mean for student Id 4.", {"student_id": 4}),
        ("Mean for course ID 3 in semester S1.", {"course_id": 3, "semester_id": "S1"}),
        ("Mean for student ID 1 and teacher ID 11.", {"student_id": 1, "teacher_id": 11}),
        (
            "Mean for student ID 2, course ID 1, teacher ID 10 in S1.",
            {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
        ),
        (
            "Mean for Bea in course ID 1 with teacher Kim, S1.",
            {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
        ),
        ("Mean for course ID 2 and teacher ID 10.", {"course_id": 2, "teacher_id": 10}),
    ],
)
def test_natural_numeric_ids_reach_real_sql(tmp_path, question, scope):
    path, provider, agent = setup_run(tmp_path, "university")
    before = db.file_hash(path)
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert provider.scopes == [scope, scope]
    assert result["step_results"][0]["raw"]["rows"] == university_oracle(path, scope, "grade_mean")
    assert provider.calls == 2
    assert db.file_hash(path) == before
    assert_trace(tmp_path, result)


@pytest.mark.parametrize(
    "question",
    [
        "Show enrollment rows with student IDs and course IDs.",
        "List enrollments with course ID, teacher ID, and student ID.",
        "Show student ID and course ID for enrollments in S1.",
        "List enrollment rows showing teacher IDs for course ID 1.",
    ],
)
def test_projection_ids_are_not_unknown_names(tmp_path, question):
    path, provider, agent = setup_run(tmp_path, "university", "enrollment_rows")
    scope = (
        {"semester_id": "S1"}
        if "S1" in question
        else {"course_id": 1}
        if "ID 1" in question
        else {}
    )
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert provider.scopes == [scope, scope]
    assert result["step_results"][0]["raw"]["rows"] == university_oracle(
        path, scope, "enrollment_rows"
    )
    assert_trace(tmp_path, result)


@pytest.mark.parametrize(
    "question,scope",
    [
        ("Count open loans for reader ID 1.", {"reader_id": 1}),
        ("Show unreturned loans for READER id 2!", {"reader_id": 2}),
        ("Count open loans for Ada, reader ID 1.", {"reader_id": 1}),
        ("Count open loans by reader IDs.", {}),
        ("Show reader ID and open loan count per reader.", {}),
        ("Count open loans for reader Id 2?", {"reader_id": 2}),
    ],
)
def test_library_natural_ids_and_projection_reach_same_core(tmp_path, question, scope):
    path, provider, agent = setup_run(tmp_path, "library")
    before = db.file_hash(path)
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert provider.scopes == [scope, scope]
    sql = (
        "SELECT r.reader_id,r.name,COUNT(l.loan_id) FROM Readers r "
        "LEFT JOIN Loans l ON l.reader_id=r.reader_id AND l.returned=0 "
    )
    if scope:
        sql += "WHERE r.reader_id=:reader_id "
    sql += "GROUP BY r.reader_id,r.name ORDER BY r.reader_id"
    with sqlite3.connect(path) as connection:
        expected = [list(row) for row in connection.execute(sql, scope)]
    assert result["answer"]["rows"] == expected
    assert db.file_hash(path) == before
    assert_trace(tmp_path, result)


@pytest.mark.parametrize(
    "kind,question",
    [
        ("university", "Mean for student ID 999."),
        ("university", "Mean for course ID -1."),
        ("university", "Mean for teacher ID nonsense."),
        ("university", "Mean for course ID =."),
        ("university", "Mean for student ID 1 and student ID 2."),
        ("university", "Mean for Bea, student ID 1."),
        ("university", "Mean for student named Zephyr."),
        ("library", "Count open loans for reader ID 999."),
        ("library", "Count open loans for reader ID -2."),
        ("library", "Count open loans for reader ID nope."),
        ("library", "Count open loans for reader ID =."),
        ("library", "Count open loans for reader ID 1 and reader ID 2."),
        ("library", "Count open loans for Ada, reader ID 2."),
        ("library", "Count open loans for reader named Zephyr."),
    ],
)
def test_unknown_malformed_conflicting_identity_never_unfilters(tmp_path, kind, question):
    _, provider, agent = setup_run(tmp_path, kind)
    result = agent.run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert result["answer"] is None
    assert provider.calls == 0
    assert not any(event["kind"] in {"sql_attempt", "db_result"} for event in result["events"])
    assert_trace(tmp_path, result)


@pytest.mark.parametrize("kind", ["university", "library"])
def test_id_projection_preserves_catalog_ambiguity_and_resume(tmp_path, kind):
    path, provider, agent = setup_run(tmp_path, kind)
    if kind == "university":
        question = "Show mean grade for Alex with student ID in output."
        field, selected = "student_id", 3
    else:
        # Recreate Agent after fixture mutation, so identity/hash binds actual data.
        with sqlite3.connect(path) as connection:
            connection.execute("INSERT INTO Readers VALUES(3,'Ada')")
        agent = Agent(Library(), path, provider, tmp_path / "traces")
        question = "Count open loans for Ada with reader ID in output."
        field, selected = "reader_id", 3
    paused = agent.run(question)
    assert paused["status"] == "clarification", paused
    assert provider.calls == 0
    assert {item["value"] for item in paused["clarification"]["options"]} == {1, 3}
    result = agent.resume(paused["clarification"], selected, request_id="choose-identity")
    assert result["status"] == "ok", result
    assert provider.scopes == [{field: selected}, {field: selected}]
    if kind == "library":
        assert result["answer"]["rows"] == [[3, "Ada", 0]]
    else:
        assert result["answer"]["empty_reason"] == "no_grades"
    assert result["run_id"] == paused["run_id"]
    assert_trace(tmp_path, result)
