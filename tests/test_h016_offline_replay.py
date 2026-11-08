"""Development-known H015 questions, OFFLINE regression only; never a live rescore.

Historical registration is read-only. No collector, observer, scorer, or corrector
is imported. Fixture resources/mutations rebuild private temporary SQLite files.
Scripted plans are an explicit test boundary; SQL uses actual production scope and
actual validated upstream references. No expected scope enters Agent.run.
"""

import hashlib
import json
import os
import socket
import sqlite3
from copy import deepcopy
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
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

ROOT = Path(__file__).resolve().parents[1]
REGISTRATION = ROOT / "docs/operations/H-015/registration"
CONVERSATIONS = json.loads((REGISTRATION / "conversations.json").read_text())
CASES = [case for case in CONVERSATIONS if case["repeat"] == 1]
FIXTURES = json.loads((REGISTRATION / "fixtures.json").read_text())


@pytest.fixture(autouse=True)
def deny_network(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("H016 offline replay forbids network access")

    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)


def make_plan(specs):
    steps = []
    for index, spec in enumerate(specs):
        step = scripted_step(spec, "", {}, f"s{index}")[0]["steps"][0]
        if index:
            column, binding = (
                ("course_id", "course_ids") if index == 1 else ("student_id", "student_ids")
            )
            step["depends_on"] = [f"s{index - 1}"]
            step["result_refs"] = [
                {
                    "from_step": f"s{index - 1}",
                    "column": column,
                    "type": "integer",
                    "bind_as": binding,
                }
            ]
        steps.append(step)
    return {
        "version": "1",
        "steps": steps,
        "needs_clarification": False,
        "clarification_field": None,
    }


class ReplayTransport(ScriptedProvider):
    def __init__(self, domain, specs):
        super().__init__([])
        self.domain = domain
        self.specs = specs
        self.plan = make_plan(specs)
        self.history = []

    def call(self, operation, payload, output_type, *, timeout=180):
        self.calls += 1
        self.history.append({"operation": operation, "payload": deepcopy(payload)})
        if operation == "plan":
            value = self.plan
        else:
            index = int(payload["step"]["step_id"][1:])
            spec = self.specs[index]
            sql, params = self.domain.query(spec, payload["scope"], payload["resolved_refs"])
            value = scripted_step(spec, sql, params, f"s{index}")[1]
        return output_type.model_validate(value), {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "real_provider_called": False,
            "injection_point": "h016_offline_replay_actual_scope_and_refs",
        }


def family(case_id):
    if case_id in {"D03", "D04", "X-M1", "X-M1-TIE"}:
        return [
            make_spec("top_course", "course_id"),
            make_spec("student_ids"),
            make_spec("grade_mean", "student_id"),
        ]
    if case_id in {"D01", "D02", "X-TOP"}:
        return [make_spec("top_course", "course_id")]
    if case_id in {"J03", "C04", "E04", "X-COUNT"}:
        return [make_spec("enrollment_counts")]
    if case_id in {"J04", "E03", "X-LIST"}:
        return [make_spec("enrollment_rows")]
    if case_id.startswith("L") or case_id == "X-LIBRARY":
        return [LIBRARY_SPEC]
    return [make_spec("grade_mean")]


def expected_scope(case_id):
    return {
        "A01": {},
        "A02": {"semester_id": "S1"},
        "A03": {"course_id": 3, "semester_id": "S1"},
        "A04": {"course_id": 3, "semester_id": "S1"},
        "J01": {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
        "J02": {"student_id": 1, "course_id": 1},
        "J03": {"course_id": 1, "semester_id": "S1"},
        "J04": {"course_id": 1, "semester_id": "S1"},
        "C01": {"student_id": 1},
        "C02": {"student_id": 3},
        "C03": {"semester_id": "S1"},
        "C04": {"course_id": 1, "semester_id": "S1", "count_object": "enrollment_count"},
        "E01": {"course_id": 2, "semester_id": "S2"},
        "E02": {"teacher_id": 10, "semester_id": "S2"},
        "E03": {"course_id": 2, "semester_id": "S2"},
        "E04": {"course_id": 2, "semester_id": "S2"},
        "X-COMBINED": {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
        "X-COUNT": {"course_id": 1, "semester_id": "S1"},
        "X-LIST": {"course_id": 2, "semester_id": "S2"},
        "X-LIBRARY": {"reader_id": 2},
    }.get(case_id, {} if case_id.startswith("L") else {"semester_id": "S1"})


def oracle_rows(connection, spec, scope, refs):
    """Independent SQLite relational projections; no domain SQL/formatter calls."""
    metric = spec.metric_id.split(".")[1]
    if metric == "open_count":
        sql = (
            "SELECT r.reader_id,r.name,COUNT(l.loan_id) FROM Readers r LEFT JOIN Loans l "
            "ON r.reader_id=l.reader_id AND l.returned=0 "
        )
        if "reader_id" in scope:
            sql += "WHERE r.reader_id=:reader_id "
        sql += "GROUP BY r.reader_id,r.name ORDER BY r.reader_id"
        return [list(row) for row in connection.execute(sql, scope)]
    group = (
        spec.group_keys[0]
        if spec.group_keys and metric in {"grade_mean", "top_course", "enrollment_counts"}
        else None
    )
    group_sql = ("e." if group == "student_id" else "o.") + group if group else None
    if metric in {"grade_mean", "top_course"}:
        projection = (group_sql + "," if group else "") + (
            "COALESCE(SUM(e.grade_units),0),COUNT(e.grade_units),COUNT(*)"
        )
    elif metric == "enrollment_counts":
        projection = "COUNT(*),COUNT(e.grade_units),COUNT(DISTINCT e.student_id)"
    elif metric == "student_ids":
        projection = "DISTINCT e.student_id"
    else:
        projection = (
            "e.student_id,s.name,e.offering_id,o.course_id,c.title,o.teacher_id,"
            "t.name,o.semester_id,e.grade_units"
        )
    sql = f"SELECT {projection} FROM Enrollments e JOIN Offerings o USING(offering_id) "
    if metric == "enrollment_rows":
        sql += (
            "JOIN Students s USING(student_id) JOIN Courses c USING(course_id) "
            "JOIN Teachers t USING(teacher_id) "
        )
    params = {key: value for key, value in scope.items() if key != "count_object"}
    where = [("e." if key == "student_id" else "o.") + key + "=:" + key for key in params]
    for binding, values in refs.items():
        field = "o.course_id" if binding == "course_ids" else "e.student_id"
        names = []
        for index, value in enumerate(values):
            key = f"ref_{binding}_{index}"
            params[key] = value
            names.append(":" + key)
        where.append(field + " IN (" + ",".join(names) + ")" if names else "0=1")
    if where:
        sql += "WHERE " + " AND ".join(where)
    if group:
        sql += " GROUP BY " + group_sql
    order = (
        "e.offering_id,e.student_id"
        if metric == "enrollment_rows"
        else ("e.student_id" if metric == "student_ids" else group_sql)
    )
    if order:
        sql += " ORDER BY " + order
    return [list(row) for row in connection.execute(sql, params)]


def selected_rows(raw, spec):
    if spec.metric_id == "u.top_course.v1":
        eligible = [row for row in raw if row[-2]]
        maximum = max((Fraction(row[-3], row[-2]) for row in eligible), default=None)
        return [row for row in eligible if Fraction(row[-3], row[-2]) == maximum]
    return raw


def answer_rows(raw, spec):
    selected = selected_rows(raw, spec)
    if spec.metric_id in {"u.grade_mean.v1", "u.top_course.v1"}:
        return [
            row[:-3]
            + [
                str(
                    (Decimal(row[-3]) / (100 * row[-2])).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                )
                if row[-2]
                else None,
                row[-2],
                row[-1],
            ]
            for row in selected
        ]
    return selected


EXTRA = [
    {
        "case_id": "X-M1",
        "domain": "university",
        "fixture": "f2",
        "question": "Show student IDs and their mean in S1 for students of the highest-mean course in S1, keeping all tied courses.",
        "selections": [],
    },
    {
        "case_id": "X-M1-TIE",
        "domain": "university",
        "fixture": "tie",
        "question": "For students in all courses tied for top mean in S1, list student ID with mean over every S1 enrollment.",
        "selections": [],
    },
    {
        "case_id": "X-TOP",
        "domain": "university",
        "fixture": "tie",
        "question": "Show course ID and top mean for S1; preserve exact ties.",
        "selections": [],
    },
    {
        "case_id": "X-COMBINED",
        "domain": "university",
        "fixture": "u",
        "question": "Average grades for Bea, course ID 1, teacher ID 10, semester S1.",
        "selections": [],
    },
    {
        "case_id": "X-COUNT",
        "domain": "university",
        "fixture": "u",
        "question": "Show enrollment count, graded count and distinct student count for course ID 1 in S1.",
        "selections": [],
    },
    {
        "case_id": "X-LIST",
        "domain": "university",
        "fixture": "u",
        "question": "Show student IDs, course IDs and enrollment grades in course ID 2, S2.",
        "selections": [],
    },
    {
        "case_id": "X-LIBRARY",
        "domain": "library",
        "fixture": "all_returned",
        "question": "Show reader ID and open-loan count for reader ID 2.",
        "selections": [],
    },
]


@pytest.mark.parametrize("case", CASES + EXTRA, ids=lambda case: case["case_id"])
def test_development_known_offline_replay(tmp_path, case):
    descriptor = FIXTURES[case["fixture"]]
    path = tmp_path / "private-fixture.sqlite"
    with sqlite3.connect(path) as connection:
        for key in ("schema", "seed"):
            connection.executescript((ROOT / descriptor[key]).read_text())
        for statement in descriptor["mutations"]:
            connection.executescript(statement)
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    domain = University() if case["domain"] == "university" else Library()
    specs = family(case["case_id"])
    provider = ReplayTransport(domain, specs)
    agent = Agent(domain, path, provider, tmp_path / "traces")
    assert isinstance(agent.compiled, CompiledStateGraph)
    before = db.file_hash(path)
    result = agent.run(case["question"])
    pauses = []
    for index, selection in enumerate(case["selections"]):
        assert result["status"] == "clarification", result
        assert provider.calls == 0
        pauses.append(deepcopy(result["clarification"]))
        result = agent.resume(result["clarification"], selection, request_id=f"selection-{index}")
    assert result["status"] == "ok", result
    scope = expected_scope(case["case_id"])
    assert all(call["payload"]["scope"] == scope for call in provider.history)
    refs = {}
    with sqlite3.connect(path) as connection:
        for index, spec in enumerate(specs):
            raw = oracle_rows(connection, spec, scope, refs)
            step = result["step_results"][index]
            assert step["raw"]["rows"] == raw
            assert step["raw"]["columns"] == [
                {"name": column.name, "type": column.type} for column in spec.columns
            ]
            assert step["dependency_rows"] == selected_rows(raw, spec)
            assert step["answer"]["rows"] == answer_rows(raw, spec)
            sql_call = [entry for entry in provider.history if entry["operation"] == "sql"][index]
            assert sql_call["payload"]["resolved_refs"] == refs
            if index == 0 and len(specs) > 1:
                refs = {"course_ids": [row[0] for row in selected_rows(raw, spec)]}
            elif index == 1:
                refs = {"student_ids": [row[0] for row in raw]}
    assert result["answer"]["rows"] == result["step_results"][-1]["answer"]["rows"]
    if case["case_id"] in {"A03", "C02"}:
        assert result["answer"]["empty_reason"] == "no_grades"
    if case["case_id"] in {"E01", "E02", "E03"}:
        assert result["answer"]["empty_reason"] == "no_rows"
    if case["case_id"] == "A04":
        assert result["answer"]["rows"] == [["0.00", 1, 1]]
    if case["case_id"] in {"D02", "X-TOP", "X-M1-TIE"}:
        assert [row[0] for row in result["step_results"][0]["dependency_rows"]] == [1, 2]
    assert provider.calls == 1 + len(specs)
    assert db.file_hash(path) == before
    trace_path = tmp_path / "traces" / (result["run_id"] + ".jsonl")
    persisted = [json.loads(line) for line in trace_path.read_text().splitlines()]
    assert persisted == result["events"]
    assert persisted[-1]["kind"] == "run_end"
    assert len([event for event in persisted if event["kind"] == "db_result"]) == len(specs)
    output = os.environ.get("H016_REPLAY_EVIDENCE")
    if output:
        directory = Path(output)
        directory.mkdir(parents=True, exist_ok=True)
        # Retain exact terminal trace bytes for audit after temporary-fixture cleanup.
        (directory / (case["case_id"] + ".jsonl")).write_bytes(trace_path.read_bytes())
        proof = {
            "profile": "development-known OFFLINE regression; NOT live score",
            "case": case,
            "expected_scope": scope,
            "pauses": pauses,
            "answer": result["answer"],
            "steps": result["step_results"],
            "provider_calls": provider.calls,
            "actual_provider_scopes": [entry["payload"]["scope"] for entry in provider.history],
            "actual_sql_refs": [
                entry["payload"]["resolved_refs"]
                for entry in provider.history
                if entry["operation"] == "sql"
            ],
            "fixture_before_sha256": before,
            "fixture_after_sha256": db.file_hash(path),
            "trace_sha256": hashlib.sha256(trace_path.read_bytes()).hexdigest(),
        }
        (directory / (case["case_id"] + ".json")).write_text(json.dumps(proof, indent=2) + "\n")


@pytest.mark.parametrize("mask", range(16), ids=lambda mask: f"filter-subset-{mask:04b}")
def test_independent_natural_all_filter_subsets(tmp_path, mask):
    """Every accepted optional filter combination starts as ordinary user text."""
    fields = [
        ("student_id", 2, "student ID 2"),
        ("course_id", 1, "course ID 1"),
        ("teacher_id", 10, "teacher ID 10"),
        ("semester_id", "S1", "semester S1"),
    ]
    included = [entry for index, entry in enumerate(fields) if mask & (1 << index)]
    scope = {field: value for field, value, _ in included}
    question = (
        "Show mean grade for " + ", ".join(phrase for _, _, phrase in included) + "."
        if included
        else "Show mean grade across all enrollments and semesters."
    )
    run_independent_question(tmp_path, question, make_spec("grade_mean"), scope)


@pytest.mark.parametrize(
    "group", ["student_id", "course_id", "teacher_id", "offering_id", "semester_id"]
)
def test_independent_natural_grouping_with_id_projections(tmp_path, group):
    noun = group.removesuffix("_id")
    question = f"Show mean grade grouped by {noun}, with {noun} IDs in output."
    run_independent_question(tmp_path, question, make_spec("grade_mean", group), {})


@pytest.mark.parametrize(
    "phrase", ["Count enrollments", "Count graded enrollments", "Count distinct students"]
)
def test_independent_natural_count_objects_and_combined_filter(tmp_path, phrase):
    question = phrase + " for course ID 1 and teacher ID 10 in S1."
    run_independent_question(
        tmp_path,
        question,
        make_spec("enrollment_counts"),
        {"course_id": 1, "teacher_id": 10, "semester_id": "S1"},
    )


def run_independent_question(tmp_path, question, spec, expected):
    """Expected scope is oracle/assertion only, never Agent or transport input."""
    path = tmp_path / "independent.sqlite"
    db.initialize(path, ROOT / "resources")
    provider = ReplayTransport(University(), [spec])
    agent = Agent(University(), path, provider, tmp_path / "traces")
    before = db.file_hash(path)
    result = agent.run(question)
    assert result["status"] == "ok", result
    assert [entry["payload"]["scope"] for entry in provider.history] == [expected, expected]
    with sqlite3.connect(path) as connection:
        raw = oracle_rows(connection, spec, expected, {})
    assert result["step_results"][0]["raw"]["rows"] == raw
    assert result["step_results"][0]["raw"]["columns"] == [
        {"name": column.name, "type": column.type} for column in spec.columns
    ]
    assert result["answer"]["rows"] == answer_rows(raw, spec)
    assert provider.calls == 2
    assert db.file_hash(path) == before
    persisted = [
        json.loads(line)
        for line in (tmp_path / "traces" / (result["run_id"] + ".jsonl")).read_text().splitlines()
    ]
    assert persisted == result["events"]
    assert persisted[-1]["kind"] == "run_end"


@pytest.mark.parametrize(
    "question",
    [
        "Show mean for course ID",
        "Mean for course ID and teacher ID 10.",
        "Mean for course ID for teacher ID 10.",
        "Mean for course ID with teacher ID 10.",
        "Mean for semester ID nonsense in S1.",
        "Mean for semester ID S999 in S1.",
        "Mean for semester ID -1 in S1.",
        "Mean for semester ID = in S1.",
    ],
)
def test_malformed_identity_not_hidden_by_other_valid_scope(tmp_path, question):
    path = tmp_path / "private.sqlite"
    db.initialize(path, ROOT / "resources")
    provider = ReplayTransport(University(), [make_spec("grade_mean")])
    result = Agent(University(), path, provider, tmp_path / "traces").run(question)
    assert result["status"] == "error", result
    assert result["error"]["code"] == "INVALID_INPUT"
    assert result["answer"] is None
    assert provider.calls == 0
    assert not any(event["kind"] == "sql_attempt" for event in result["events"])


def test_compact_identity_must_not_silently_unfilter(tmp_path):
    path = tmp_path / "private.sqlite"
    db.initialize(path, ROOT / "resources")
    provider = ReplayTransport(University(), [make_spec("grade_mean")])
    result = Agent(University(), path, provider, tmp_path / "traces").run("Show mean for course2.")
    if result["status"] == "ok":
        assert [entry["payload"]["scope"] for entry in provider.history] == [
            {"course_id": 2},
            {"course_id": 2},
        ]
        with sqlite3.connect(path) as connection:
            assert result["step_results"][0]["raw"]["rows"] == oracle_rows(
                connection, make_spec("grade_mean"), {"course_id": 2}, {}
            )
    else:
        assert result["error"]["code"] == "INVALID_INPUT"
        assert provider.calls == 0
