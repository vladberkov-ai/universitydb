"""Registered University behavior; expected values frozen before implementation."""

import json
import sqlite3
from pathlib import Path

import pytest

from universitydb import db
from universitydb.contracts import Failure, SQLProposal, Step
from universitydb.domain import FILTERS, GROUPS, University, make_spec

ORACLE = json.loads(
    (Path(__file__).resolve().parents[1] / "docs/operations/H-013/frozen-oracle.json").read_text()
)


def proposal_for(domain, spec, scope, refs=None, step_id="query"):
    sql, params = domain.query(spec, scope, refs)
    return SQLProposal.model_validate(
        {
            "version": "1",
            "step_id": step_id,
            "result_spec": spec.model_dump(),
            "sql": sql,
            "parameters": [
                {
                    "name": k,
                    "type": "text" if type(v) is str else "integer",
                    "integer_value": v if type(v) is int else None,
                    "text_value": v if type(v) is str else None,
                }
                for k, v in params.items()
            ],
            "expected_columns": [c.name for c in spec.columns],
            "result_kind": "aggregate" if spec.shape == "aggregate" else "rows",
            "explanation": "Offline registered query fixture",
        }
    )


def step_for(spec, step_id="query"):
    return Step.model_validate(
        {
            "step_id": step_id,
            "depends_on": [],
            "purpose": "Offline fixture",
            "result_refs": [],
            "result_spec": spec.model_dump(),
        }
    )


def execute_spec(database, spec, scope, refs=None):
    domain = University()
    proposal = proposal_for(domain, spec, scope, refs)
    params = domain.validate_sql(proposal, scope, step=step_for(spec), resolved_refs=refs)
    result = db.execute(
        database, proposal.sql, params, domain.tables, domain.functions, result_spec=spec
    )
    return result["rows"], domain.adapt_result(result["rows"], spec, scope)


@pytest.mark.parametrize("case", ORACLE["scopes"], ids=lambda c: str(c["scope"]))
def test_all_16_filter_subsets_all_five_groups_and_counts(database, case):
    raw, result = execute_spec(database, make_spec("grade_mean"), case["scope"])
    assert raw == [case["raw"]]
    assert result["answer"]["rows"] == [[case["mean"], *case["raw"][1:]]]
    for key in FILTERS:
        assert f"{key}=" in result["answer"]["scope"]
    for group in GROUPS:
        expected = case["groups"][group]
        raw, result = execute_spec(database, make_spec("grade_mean", group), case["scope"])
        assert raw == [[g["key"], *g["raw"]] for g in expected]
        assert result["answer"]["rows"] == [[g["key"], g["mean"], *g["raw"][1:]] for g in expected]
        assert result["answer"]["row_reasons"] == [g["reason"] for g in expected]
        raw, _ = execute_spec(database, make_spec("enrollment_counts", group), case["scope"])
        assert raw == [
            [g["key"], g["raw"][2], g["raw"][1], g["distinct_students"]] for g in expected
        ]
    raw, _ = execute_spec(database, make_spec("enrollment_counts"), case["scope"])
    assert raw == [[case["raw"][2], case["raw"][1], case["distinct_students"]]]


def test_q2_q3_q7_q8_explicit_oracles(database):
    cases = [
        ({}, "83.33"),
        ({"semester_id": "S1"}, "87.50"),
        ({"course_id": 1}, "80.00"),
        ({"teacher_id": 10}, "83.33"),
        ({"student_id": 1}, "86.67"),
        ({"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}, "80.00"),
        ({"student_id": 1, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}, "90.00"),
        ({"student_id": 1, "course_id": 1}, "80.00"),
        ({"student_id": 1, "course_id": 1, "semester_id": "S2"}, "70.00"),
        ({"course_id": 2, "semester_id": "S2"}, None),
        ({"course_id": 3, "semester_id": "S1"}, None),
    ]
    for scope, expected in cases:
        _, result = execute_spec(database, make_spec("grade_mean"), scope)
        assert result["answer"]["rows"][0][0] == expected


def test_q6_join_listing_labels_and_nullable_grade(database):
    rows, adapted = execute_spec(
        database, make_spec("enrollment_rows"), {"course_id": 1, "semester_id": "S1"}
    )
    assert rows == [
        [1, "Alex", 1, 1, "DB", 10, "Kim", "S1", 9000],
        [2, "Bea", 1, 1, "DB", 10, "Kim", "S1", 6000],
        [3, "Alex", 1, 1, "DB", 10, "Kim", "S1", None],
        [2, "Bea", 5, 1, "DB", 10, "Kim", "S1", 10000],
    ]
    assert adapted["answer"]["columns"][-1] == {
        "name": "grade_units",
        "type": "integer",
    }


@pytest.mark.parametrize("fixture", ["F1", "F2", "tie", "empty", "no_grades"])
def test_exact_top_ties_raw_candidates_and_selected_dependencies(database, fixture):
    expected = ORACLE["m1"][fixture]
    with sqlite3.connect(database) as conn:
        conn.execute("DELETE FROM Enrollments")
        conn.executemany("INSERT INTO Enrollments VALUES(?,?,?)", expected["enrollments"])
    _, result = execute_spec(database, make_spec("top_course", "course_id"), {"semester_id": "S1"})
    assert [r[0] for r in result["dependency_rows"]] == expected["top_course_ids"]


def test_exact_rational_not_rounded_top_and_half_up():
    domain = University()
    adapted = domain.adapt_result(
        [[1, 25000, 3, 3], [2, 8333, 1, 1]], make_spec("top_course", "course_id"), {}
    )
    assert [r[0] for r in adapted["dependency_rows"]] == [1]
    assert domain.answer([[1, 8, 8]], {})["rows"][0][0] == "0.00"
    assert domain.answer([[1, 2, 2]], {})["rows"][0][0] == "0.01"


def test_resolve_catalog_ambiguous_current_conflict_unknown(database):
    domain = University()
    catalog = domain.catalog(database)
    with pytest.raises(Failure) as caught:
        domain.resolve("Average Alex", catalog)
    assert caught.value.code == "CLARIFICATION_REQUIRED"
    assert [o["value"] for o in caught.value.details["options"]] == [1, 3]
    assert domain.resolve("Average Alex", catalog, {"student_id": 1}) == {"student_id": 1}
    assert domain.resolve("Mean Bea in DB with Kim S1", catalog) == {
        "student_id": 2,
        "course_id": 1,
        "teacher_id": 10,
        "semester_id": "S1",
    }
    for question in ["Mean current semester", "Mean Bea student_id=1", "How many?"]:
        with pytest.raises(Failure, match="Choose|Conflicting"):
            domain.resolve(question, catalog)
    for question in ["Mean student_id=99", "Mean student=Nobody"]:
        with pytest.raises(Failure) as caught:
            domain.resolve(question, catalog)
        assert caught.value.code == "UNKNOWN_ENTITY"
    assert domain.resolve("Mean current semester", catalog, {"semester_id": "S2"}) == {
        "semester_id": "S2"
    }


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s.replace("e.offering_id = o.offering_id", "e.student_id = o.offering_id"),
        lambda s: s.replace("SUM(e.grade_units)", "SUM(e.grade_units) / 2"),
        lambda s: s + " LIMIT 1",
        lambda s: s.replace(":course_id", "1"),
    ],
)
def test_plausible_safe_semantic_mutants_are_not_accepted(database, mutation):
    domain = University()
    spec = make_spec("grade_mean")
    p = proposal_for(domain, spec, {"course_id": 1})
    p.sql = mutation(p.sql)
    with pytest.raises(Failure):
        domain.validate_sql(p, {"course_id": 1}, step=step_for(spec))


@pytest.mark.parametrize(
    "rows,spec",
    [
        ([[True, 1, 1]], make_spec("grade_mean")),
        ([[0, 2, 1]], make_spec("grade_mean")),
        ([[0, 0, -1]], make_spec("grade_mean")),
        ([[1, 0, 0, 1], [1, 0, 0, 1]], make_spec("grade_mean", "course_id")),
        ([[None, 0, 0]], make_spec("enrollment_counts")),
        ([[-1, 0, 0]], make_spec("enrollment_counts")),
    ],
)
def test_invalid_result_types_components_duplicate_group(rows, spec):
    with pytest.raises(Failure):
        University().adapt_result(rows, spec, {})


def test_domain_integrity_and_mutated_grade(database):
    domain = University()
    domain.inspect_data(database)
    with sqlite3.connect(database) as conn:
        conn.execute("PRAGMA ignore_check_constraints=ON")
        conn.execute(
            "UPDATE Enrollments SET grade_units=10001 WHERE student_id=1 AND offering_id=1"
        )
    with pytest.raises(Failure, match="Grade"):
        domain.inspect_data(database)


def test_zero_empty_and_null_are_distinct_on_real_database(database):
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=0 WHERE student_id=1 AND offering_id=1")
    _, zero = execute_spec(
        database,
        make_spec("grade_mean"),
        {"student_id": 1, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
    )
    assert zero["answer"]["rows"] == [["0.00", 1, 1]]
    assert zero["answer"]["empty_reason"] is None
    _, empty = execute_spec(
        database, make_spec("grade_mean"), {"course_id": 2, "semester_id": "S2"}
    )
    _, null = execute_spec(database, make_spec("grade_mean"), {"course_id": 3, "semester_id": "S1"})
    assert empty["answer"]["empty_reason"] == "no_rows"
    assert null["answer"]["empty_reason"] == "no_grades"
    assert execute_spec(
        database, make_spec("enrollment_counts"), {"course_id": 2, "semester_id": "S2"}
    )[1]["answer"]["rows"] == [[0, 0, 0]]


@pytest.mark.parametrize(
    "patch",
    [
        {"unit": "grade"},
        {"scale": 1},
        {"group_keys": ["invented"]},
        {"metric_id": "u.unregistered.v1"},
    ],
)
def test_spec_registry_closed(patch):
    spec = make_spec("grade_mean").model_copy(update=patch)
    with pytest.raises(Failure) as caught:
        University().accept_spec(spec)
    assert caught.value.code == "RESULT_CONTRACT_INVALID"
