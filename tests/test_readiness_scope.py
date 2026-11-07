"""H-014 scope-loss regressions: injected transport is not model accuracy."""

import json
from pathlib import Path

import pytest
from test_i2_core import scripted_step

from universitydb import db
from universitydb.agent import Agent
from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library
from universitydb.llm import ScriptedProvider


@pytest.mark.parametrize(
    "kind,question,known_id",
    [
        ("university", "What is the average grade for Zoe?", None),
        ("library", "How many open loans does Zoe have?", None),
        ("university", "What is the mean of Zoe?", None),
        ("university", "Mean grade Zoe", None),
        ("university", "Average grades Zoe", None),
        ("university", "Mean grade grouped Zoe", None),
        ("university", "Mean grade excluding Zoe", None),
        ("university", "Mean grade Bea", 2),
        ("university", "Average grades Bea", 2),
        ("university", "What is Zoe's average grade?", None),
        ("library", "Count open loans of Zoe", None),
        ("library", "Count open loans for each Zoe", None),
        ("library", "Count open loans for every Zoe", None),
        ("library", "Count Zoe's open loans", None),
        ("university", "What is Bea's average grade?", 2),
        ("library", "Count Ada's open loans", 1),
        ("university", "What is the average grade for Bea?", 2),
        ("library", "How many open loans does Ada have?", 1),
    ],
)
def test_named_scope_compiled_graph(tmp_path, kind, question, known_id):
    domain = University() if kind == "university" else Library()
    spec = make_spec("grade_mean") if kind == "university" else LIBRARY_SPEC
    field = "student_id" if kind == "university" else "reader_id"
    resources = Path(__file__).resolve().parents[1] / "resources"
    database = tmp_path / "data.db"
    db.initialize(database, resources if kind == "university" else resources / "library")
    # A valid unfiltered proposal would previously produce misleading global success.
    scope = {} if known_id is None else {field: known_id}
    sql, params = domain.query(spec, scope)
    provider = ScriptedProvider(list(scripted_step(spec, sql, params)))
    agent = Agent(domain, database, provider, tmp_path / "trace")
    result = agent.run(question)
    if known_id is None:
        assert result["status"] == "error", result
        assert result["error"]["code"] == "INVALID_INPUT"
        assert result["answer"] is None
        assert provider.calls == 0
        assert not any(e["kind"] in ("sql_attempt", "db_result") for e in result["events"])
    else:
        assert result["status"] == "ok", result
        assert f"{field}={known_id}" in result["answer"]["scope"]
        assert provider.calls == 2
    assert result["events"][-1]["kind"] == "run_end"
    traces = list((tmp_path / "trace").glob("*.jsonl"))
    assert len(traces) == 1
    persisted = [json.loads(line) for line in traces[0].read_text().splitlines()]
    assert persisted[-1]["kind"] == "run_end"


@pytest.mark.parametrize(
    "question",
    [
        "Count open loans per reader",
        "Count open loans for each reader",
        "Count open loans for every reader",
        "Count open loans including readers with zero loans",
        "Count open loans that are not returned",
        "Count open loans by reader_id=1",
    ],
)
def test_library_non_target_prose_preserved(tmp_path, question):
    database = tmp_path / "library.db"
    db.initialize(database, Path(__file__).resolve().parents[1] / "resources/library")
    scope = Library().resolve(question, Library().catalog(database))
    assert scope == ({"reader_id": 1} if "reader_id=1" in question else {})


@pytest.mark.parametrize(
    "question,metric,group",
    [
        ("Show mean grade grouped by course across all enrollments", "grade_mean", "course_id"),
        ("Show mean grades grouped by student across all enrollments", "grade_mean", "student_id"),
        (
            "Show average grade grouped by teacher across all enrollments",
            "grade_mean",
            "teacher_id",
        ),
        (
            "Show average grades grouped by offering across all enrollments",
            "grade_mean",
            "offering_id",
        ),
        ("Show mean grade grouped by semester across all enrollments", "grade_mean", "semester_id"),
        ("Count enrollments grouped by course", "enrollment_counts", "course_id"),
        ("Count graded enrollments grouped by student", "enrollment_counts", "student_id"),
        ("Count distinct students grouped by teacher", "enrollment_counts", "teacher_id"),
        ("Count enrollments grouped by offering", "enrollment_counts", "offering_id"),
        ("Count enrollments grouped by semester", "enrollment_counts", "semester_id"),
        ("Mean grade excluding ungraded enrollments", "grade_mean", None),
        ("Show mean grade across all enrollments", "grade_mean", None),
        ("Show average grades overall", "grade_mean", None),
        ("What is the mean grade?", "grade_mean", None),
        ("What is the average grade in all semesters?", "grade_mean", None),
    ],
)
def test_university_supported_grade_group_prose(database, tmp_path, question, metric, group):
    domain = University()
    spec = make_spec(metric, group)
    sql, params = domain.query(spec, {})
    provider = ScriptedProvider(list(scripted_step(spec, sql, params)))
    result = Agent(domain, database, provider, tmp_path / "trace").run(question)
    assert result["status"] == "ok", result
    assert provider.calls == 2
    assert result["answer"]["rows"]
    for field in ("student_id", "course_id", "teacher_id", "semester_id"):
        assert f"{field}=all" in result["answer"]["scope"]
    assert any(event["kind"] == "db_result" for event in result["events"])
    assert result["events"][-1]["kind"] == "run_end"
