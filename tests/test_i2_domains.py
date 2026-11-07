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
    for question in ["Mean current semester", "How many?"]:
        with pytest.raises(Failure, match="Choose|Conflicting"):
            domain.resolve(question, catalog)
    for question in ["Mean student_id=99", "Mean student=Nobody"]:
        with pytest.raises(Failure) as caught:
            domain.resolve(question, catalog)
        assert caught.value.code == "INVALID_INPUT"
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


def graph_result(database, tmp_path, spec, scope, question=None):
    from universitydb.agent import Agent
    from universitydb.llm import ScriptedProvider

    p = proposal_for(University(), spec, scope)
    plan = {
        "version": "1",
        "steps": [step_for(spec).model_dump()],
        "needs_clarification": False,
        "clarification_field": None,
    }
    provider = ScriptedProvider([plan, p.model_dump()])
    question = question or "Mean all " + " ".join(f"{k}={v}" for k, v in scope.items())
    agent = Agent(University(), database, provider, tmp_path / "trace")
    result = agent.run(question)
    assert result["status"] == "ok", result.get("error")
    assert provider.calls == 2
    assert len(result["step_results"]) == 1
    assert [e for e in result["events"] if e["kind"] == "db_result"]
    return result


@pytest.mark.parametrize("case", ORACLE["scopes"], ids=lambda c: str(c["scope"]))
def test_compiled_graph_all_16_filter_scopes_means_counts(database, tmp_path, case):
    mean = graph_result(database, tmp_path, make_spec("grade_mean"), case["scope"])
    assert mean["answer"]["rows"] == [[case["mean"], *case["raw"][1:]]]
    counts = graph_result(
        database,
        tmp_path,
        make_spec("enrollment_counts"),
        case["scope"],
        "Count enrollments " + " ".join(f"{k}={v}" for k, v in case["scope"].items()),
    )
    assert counts["answer"]["rows"] == [[case["raw"][2], case["raw"][1], case["distinct_students"]]]


@pytest.mark.parametrize("key", GROUPS)
def test_compiled_graph_every_group_mutates_independently(database, tmp_path, key):
    spec = make_spec("grade_mean", key)
    expected = ORACLE["scopes"][0]["groups"][key]
    result = graph_result(database, tmp_path, spec, {})
    assert result["answer"]["rows"] == [[g["key"], g["mean"], *g["raw"][1:]] for g in expected]
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=1000 WHERE student_id=2 AND offering_id=1")
    expected = ORACLE["mutations"]["grade_2_1_to_1000"]["groups"][key]
    result = graph_result(database, tmp_path, spec, {})
    assert result["answer"]["rows"] == [[g["key"], g["mean"], *g["raw"][1:]] for g in expected]


@pytest.mark.parametrize(
    "scope,reason,rows",
    [
        ({"course_id": 2, "semester_id": "S2"}, "no_rows", [[None, 0, 0]]),
        ({"course_id": 3, "semester_id": "S1"}, "no_grades", [[None, 0, 1]]),
        ({"student_id": 1}, None, [["86.67", 3, 3]]),
        ({"student_id": 1, "course_id": 1}, None, [["80.00", 2, 2]]),
        ({"student_id": 1, "course_id": 1, "semester_id": "S2"}, None, [["70.00", 1, 1]]),
    ],
)
def test_compiled_graph_q2_q7_q8_mean_states(database, tmp_path, scope, reason, rows):
    result = graph_result(database, tmp_path, make_spec("grade_mean"), scope)
    assert result["answer"]["rows"] == rows
    assert result["answer"]["empty_reason"] == reason


def test_compiled_graph_q3_q6_q8_zero_q9_top_ties(database, tmp_path):
    scope = {"student_id": 1, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}
    assert graph_result(database, tmp_path, make_spec("grade_mean"), scope)["answer"]["rows"] == [
        ["90.00", 1, 1]
    ]
    listing = graph_result(
        database, tmp_path, make_spec("enrollment_rows"), {"course_id": 1, "semester_id": "S1"}
    )
    assert [(r[0], r[2], r[-1]) for r in listing["answer"]["rows"]] == [
        (1, 1, 9000),
        (2, 1, 6000),
        (3, 1, None),
        (2, 5, 10000),
    ]
    top = graph_result(
        database, tmp_path, make_spec("top_course", "course_id"), {"semester_id": "S1"}
    )
    assert [r[0] for r in top["answer"]["rows"]] == [2]
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=8000 WHERE student_id=2 AND offering_id=1")
        conn.execute("UPDATE Enrollments SET grade_units=9000 WHERE student_id=1 AND offering_id=2")
    top = graph_result(
        database, tmp_path, make_spec("top_course", "course_id"), {"semester_id": "S1"}
    )
    assert top["answer"]["rows"] == [[1, "90.00", 3, 4], [2, "90.00", 1, 1]]
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=0 WHERE student_id=1 AND offering_id=1")
    assert graph_result(database, tmp_path, make_spec("grade_mean"), scope)["answer"]["rows"] == [
        ["0.00", 1, 1]
    ]


@pytest.mark.parametrize(
    "question",
    [
        "Mean Bea student_id=1",
        "Mean student_id=1 student_id=2",
        "Mean Zed",
        "Mean for Zed",
        "Mean student=Zed",
        "Mean student named Zed",
        "Mean student_id=-1",
        "Mean student_id=nope",
        "Mean student_id=",
        "Mean reader_id=1",
        "Mean offering_id=1",
    ],
)
def test_conflicting_unknown_identity_terminal_no_provider_or_sql(database, tmp_path, question):
    from universitydb.agent import Agent
    from universitydb.llm import ScriptedProvider

    provider = ScriptedProvider([])
    result = Agent(University(), database, provider, tmp_path / "trace").run(question)
    assert result["status"] == "error"
    assert result["error"]["code"] == "INVALID_INPUT"
    assert result["clarification"] is None
    assert provider.calls == 0
    assert not [e for e in result["events"] if e["kind"] == "sql_attempt"]


def test_adapter_clarification_options_are_catalog_grounded(database):
    domain = University()
    catalog = domain.catalog(database)
    assert domain.clarification_options("student_id", catalog) == [
        {"value": 1, "label": "Alex"},
        {"value": 2, "label": "Bea"},
        {"value": 3, "label": "Alex"},
        {"value": 4, "label": "Dana"},
    ]
    assert [o["value"] for o in domain.clarification_options("count_object", catalog)] == [
        "enrollment_count",
        "graded_count",
        "distinct_student_count",
    ]
    with pytest.raises(Failure, match="not registered"):
        domain.clarification_options("untrusted", catalog)


@pytest.mark.parametrize("key", ["student_id", "course_id", "teacher_id", "semester_id"])
def test_compiled_graph_each_filter_discriminating_mutation(database, tmp_path, key):
    fixed = {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}
    scope = {key: fixed[key]}
    baseline = next(c for c in ORACLE["scopes"] if c["scope"] == scope)
    assert (
        graph_result(database, tmp_path, make_spec("grade_mean"), scope)["answer"]["rows"][0][0]
        == baseline["mean"]
    )
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=1000 WHERE student_id=2 AND offering_id=1")
    expected = ORACLE["mutations"]["grade_2_1_to_1000"]["filter_effects"][key]
    assert graph_result(database, tmp_path, make_spec("grade_mean"), scope)["answer"]["rows"] == [
        [expected["mean"], *expected["raw"][1:]]
    ]
    assert expected["raw"] != baseline["raw"]


@pytest.mark.parametrize(
    "question,scope,expected",
    [
        (
            "Mean Bea with Kim in DB S1",
            {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"},
            "80.00",
        ),
        ("Mean Alex student_id=1", {"student_id": 1}, "86.67"),
        ("Mean DB", {"course_id": 1}, "80.00"),
    ],
)
def test_compiled_graph_catalog_names_and_id_consistency(
    database, tmp_path, question, scope, expected
):
    assert (
        graph_result(database, tmp_path, make_spec("grade_mean"), scope, question)["answer"][
            "rows"
        ][0][0]
        == expected
    )


@pytest.mark.parametrize(
    "question,field,choice,scope,spec,expected",
    [
        ("Mean Alex", "student_id", 3, {"student_id": 3}, make_spec("grade_mean"), [[None, 0, 1]]),
        (
            "Mean current semester",
            "semester_id",
            "S1",
            {"semester_id": "S1"},
            make_spec("grade_mean"),
            [["87.50", 4, 6]],
        ),
        (
            "How many?",
            "count_object",
            "distinct_student_count",
            {"count_object": "distinct_student_count"},
            make_spec("enrollment_counts"),
            [[8, 6, 4]],
        ),
    ],
)
def test_real_checkpoint_catalog_and_count_choices(
    database, tmp_path, question, field, choice, scope, spec, expected
):
    from universitydb.agent import Agent
    from universitydb.llm import ScriptedProvider

    p = proposal_for(University(), spec, scope)
    plan = {
        "version": "1",
        "steps": [step_for(spec).model_dump()],
        "needs_clarification": False,
        "clarification_field": None,
    }
    provider = ScriptedProvider([plan, p.model_dump()])
    agent = Agent(University(), database, provider, tmp_path / "trace")
    paused = agent.run(question)
    assert paused["status"] == "clarification" and provider.calls == 0, paused
    assert paused["clarification"]["field"] == field
    result = agent.resume(paused["clarification"], choice, request_id="choice")
    assert result["status"] == "ok", result
    assert result["answer"]["rows"] == expected
    assert result["run_id"] == paused["run_id"] and provider.calls == 2


@pytest.mark.parametrize(
    "question",
    ["Open loan count", "Average books", "DROP TABLE Students", "nonsense", "Mean student Zed"],
)
def test_university_unsupported_or_natural_unknown_no_calls(database, tmp_path, question):
    from universitydb.agent import Agent
    from universitydb.llm import ScriptedProvider

    provider = ScriptedProvider([])
    result = Agent(University(), database, provider, tmp_path / "trace").run(question)
    assert result["status"] == "error"
    assert result["error"]["code"] == "INVALID_INPUT"
    assert provider.calls == 0
    assert not [e for e in result["events"] if e["kind"] == "sql_attempt"]


def test_compiled_s1_groups_and_rounded_equal_not_exact_top(database, tmp_path):
    expected = next(c for c in ORACLE["scopes"] if c["scope"] == {"semester_id": "S1"})["groups"][
        "course_id"
    ]
    result = graph_result(
        database, tmp_path, make_spec("grade_mean", "course_id"), {"semester_id": "S1"}
    )
    assert result["answer"]["rows"] == [[g["key"], g["mean"], *g["raw"][1:]] for g in expected]
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=8333 WHERE student_id=1 AND offering_id=2")
    result = graph_result(
        database, tmp_path, make_spec("top_course", "course_id"), {"semester_id": "S1"}
    )
    assert result["answer"]["rows"] == [[1, "83.33", 3, 4]]


def test_university_catalog_bound_and_owned_reads_missing_fail_closed(database, tmp_path):
    domain = University()
    with sqlite3.connect(database) as conn:
        conn.executemany(
            "INSERT INTO Students VALUES(?,?)", [(i, f"Name{i}") for i in range(5, 1005)]
        )
    with pytest.raises(Failure, match="1000 entity"):
        domain.catalog(database)
    for read in [domain.catalog, domain.inspect_data]:
        with pytest.raises(Failure) as caught:
            read(tmp_path / "missing.sqlite")
        assert caught.value.code == "DB_UNAVAILABLE"


def test_university_owned_reads_locked_classification(database):
    domain = University()
    with sqlite3.connect(database) as conn:
        conn.execute("BEGIN EXCLUSIVE")
        for read in [domain.catalog, domain.inspect_data]:
            with pytest.raises(Failure) as caught:
                read(database)
            assert caught.value.code == "DB_UNAVAILABLE"


def m1_family_plan():
    # Kept independent of the core lane's dynamic provider/test helper.
    steps = [
        step_for(make_spec("top_course", "course_id"), "best").model_dump(),
        step_for(make_spec("student_ids"), "people").model_dump(),
        step_for(make_spec("grade_mean", "student_id"), "averages").model_dump(),
    ]
    for step, upstream, column, bind_as in [
        (steps[1], "best", "course_id", "course_ids"),
        (steps[2], "people", "student_id", "student_ids"),
    ]:
        step["depends_on"] = [upstream]
        step["result_refs"] = [
            {"from_step": upstream, "column": column, "type": "integer", "bind_as": bind_as}
        ]
    return {
        "version": "1",
        "steps": steps,
        "needs_clarification": False,
        "clarification_field": None,
    }


def test_domain_registered_edges_and_independent_variants_not_narrowed():
    from universitydb.contracts import PlanProposal

    domain = University()
    raw = m1_family_plan()
    domain.validate_plan(PlanProposal.model_validate(raw))
    prefix = {**raw, "steps": raw["steps"][:2]}
    domain.validate_plan(PlanProposal.model_validate(prefix))
    for spec in domain.registry:
        single = {**raw, "steps": [step_for(spec).model_dump()]}
        domain.validate_plan(PlanProposal.model_validate(single))
    independent = {
        **raw,
        "steps": [
            step_for(make_spec("grade_mean"), "a").model_dump(),
            step_for(make_spec("enrollment_counts"), "b").model_dump(),
        ],
    }
    domain.validate_plan(PlanProposal.model_validate(independent))


@pytest.mark.parametrize(
    "mutation",
    [
        "source_metric",
        "source_grain",
        "column",
        "type",
        "bind_as",
        "missing_ref",
        "missing_dep",
        "extra_ref",
        "extra_dep",
        "consumer_metric",
        "consumer_grain",
        "forward",
    ],
)
def test_domain_wrong_or_incomplete_reference_family_fails_before_sql(database, tmp_path, mutation):
    from universitydb.agent import Agent
    from universitydb.llm import ScriptedProvider

    raw = m1_family_plan()
    if mutation == "source_metric":
        raw["steps"][0]["result_spec"] = make_spec("grade_mean", "course_id").model_dump()
    elif mutation == "source_grain":
        raw["steps"][0]["result_spec"] = make_spec("grade_mean", "teacher_id").model_dump()
    elif mutation in ("column", "type", "bind_as"):
        raw["steps"][1]["result_refs"][0][mutation] = {
            "column": "sum_units",
            "type": "string",
            "bind_as": "student_ids",
        }[mutation]
    elif mutation == "missing_ref":
        raw["steps"][1]["result_refs"] = []
    elif mutation == "missing_dep":
        raw["steps"][1]["depends_on"] = []
    elif mutation == "extra_ref":
        raw["steps"][1]["result_refs"].append(
            {**raw["steps"][1]["result_refs"][0], "bind_as": "extra"}
        )
    elif mutation == "extra_dep":
        raw["steps"][2]["depends_on"].append("best")
    elif mutation == "consumer_metric":
        raw["steps"][2]["result_spec"] = make_spec("enrollment_counts", "student_id").model_dump()
    elif mutation == "consumer_grain":
        raw["steps"][2]["result_spec"] = make_spec("grade_mean", "course_id").model_dump()
    else:
        raw["steps"][1]["result_refs"][0]["from_step"] = "averages"
        raw["steps"][1]["depends_on"] = ["averages"]
    provider = ScriptedProvider([raw])
    result = Agent(University(), database, provider, tmp_path / "trace").run(
        "For students of the top course in S1 show their means"
    )
    assert result["error"]["code"] == "PLAN_INVALID", result
    assert provider.calls == 1
    assert not [e for e in result["events"] if e["kind"] == "sql_attempt"]


@pytest.mark.parametrize("fixture", ["F1", "F2", "tie", "empty", "no_grades"])
def test_m1_registered_domain_queries_use_actual_upstream_oracle(database, fixture):
    expected = ORACLE["m1"][fixture]
    with sqlite3.connect(database) as conn:
        conn.execute("DELETE FROM Enrollments")
        conn.executemany("INSERT INTO Enrollments VALUES(?,?,?)", expected["enrollments"])
    scope = {"semester_id": "S1"}
    _, top = execute_spec(database, make_spec("top_course", "course_id"), scope)
    course_ids = [row[0] for row in top["dependency_rows"]]
    _, cohort = execute_spec(database, make_spec("student_ids"), scope, {"course_ids": course_ids})
    student_ids = [row[0] for row in cohort["dependency_rows"]]
    _, means = execute_spec(
        database, make_spec("grade_mean", "student_id"), scope, {"student_ids": student_ids}
    )
    assert course_ids == expected["top_course_ids"]
    assert student_ids == expected["cohort_student_ids"]
    assert means["answer"]["rows"] == [
        [g["key"], g["mean"], *g["raw"][1:]] for g in expected["final"]
    ]
    if not course_ids:
        sql, params = University().query(make_spec("student_ids"), scope, {"course_ids": []})
        assert "0 = 1" in sql and params == scope
