"""Independent synthetic artifact tests; no candidate product execution or provider."""

import copy
import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
O = runpy.run_path(str(ROOT / "tools/eval/observe.py"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def test_choices_reorder_only_after_strict_set_validation():
    exchange = {
        "status": "clarification",
        "clarification": {"field": "object", "options": [{"value": "z"}, {"value": "a"}]},
    }
    original = copy.deepcopy(exchange)
    assert O["normalize_choices"]([exchange], [{"field": "object", "values": ["a", "z"]}]) == (
        [{"field": "object", "values": ["a", "z"]}],
        True,
    )
    assert exchange == original


@pytest.mark.parametrize("offered", [[True, 2], [1, 1], [1], [1, 2, 3], [1.0, 2]])
def test_choice_missing_extra_duplicate_bool_and_float_rejected(offered):
    exchange = {
        "status": "clarification",
        "clarification": {"field": "id", "options": [{"value": v} for v in offered]},
    }
    observed, valid = O["normalize_choices"]([exchange], [{"field": "id", "values": [1, 2]}])
    assert not valid
    assert observed[0]["values"] == offered


@pytest.fixture
def answer():
    return {
        "columns": [
            {"name": "student_id", "type": "integer"},
            {"name": "average", "type": "decimal"},
        ],
        "rows": [[7, "0.00"], [2, None], [7, "0.00"]],
        "empty_reason": None,
    }


@pytest.fixture
def steps():
    return [
        {
            "raw": {
                "result_spec": {
                    "metric_id": "u.grade_mean.v1",
                    "columns": [{"name": "student_id", "type": "integer", "nullable": False}],
                }
            }
        }
    ]


def test_projection_alias_sort_preserves_null_zero_duplicates(answer, steps):
    result, valid = O["project"](answer, steps, ["student_id", "mean"])
    assert valid
    assert result == {
        "columns": ["student_id", "mean"],
        "types": ["integer", "decimal?"],
        "rows": [[2, None], [7, "0.00"], [7, "0.00"]],
        "empty_reason": None,
    }
    assert answer["rows"][0] == [7, "0.00"]


@pytest.mark.parametrize("value", [False, 1.0, "1"])
def test_observer_does_not_coerce_integer(answer, steps, value):
    answer["rows"][0][0] = value
    assert not O["project"](answer, steps, ["student_id"])[1]


@pytest.mark.parametrize("value", ["1.0", "1.000", 1.0, 1, "NaN"])
def test_decimal_errors_not_rounded_or_coerced(answer, steps, value):
    answer["rows"][0][1] = value
    assert not O["project"](answer, steps, ["mean"])[1]


def test_nonnull_decimal_is_not_made_nullable_from_oracle(answer, steps):
    answer["rows"] = [[7, "0.00"]]
    assert O["project"](answer, steps, ["mean"])[0]["types"] == ["decimal"]


def test_missing_projection_not_filled_with_expected_columns(answer, steps):
    assert O["project"](answer, steps, ["invented"])[0]["columns"] == ["student_id", "mean"]


def dependency_fixture():
    state = {
        "plan": {
            "steps": [
                {
                    "step_id": "downstream",
                    "result_refs": [
                        {
                            "from_step": "upstream",
                            "column": "course_id",
                            "type": "integer",
                            "bind_as": "courses",
                        }
                    ],
                }
            ]
        },
        "completed": {
            "upstream": {
                "result_spec": {
                    "columns": [{"name": "course_id", "type": "integer", "nullable": False}]
                },
                "rows": [[9], [3]],
            }
        },
    }
    events = [
        {
            "kind": "adapted_result",
            "payload": {"step_id": "upstream", "dependency_rows": [[9], [3]]},
        },
        {
            "kind": "dependency_bindings",
            "payload": {"step_id": "downstream", "values": {"courses": [3, 9]}},
        },
    ]
    return state, events


def test_dependencies_from_actual_selected_rows_and_bindings():
    state, events = dependency_fixture()
    assert O["dependencies"](state, events) == ({"top_course_ids": [3, 9]}, True)


@pytest.mark.parametrize("fault", ["missing", "binding", "adapted", "bool"])
def test_missing_or_unproven_dependencies_never_inferred(fault):
    state, events = dependency_fixture()
    if fault == "missing":
        state["completed"] = {}
    elif fault == "binding":
        events[-1]["payload"]["values"]["courses"] = [3]
    elif fault == "adapted":
        events.pop(0)
    else:
        state["completed"]["upstream"]["rows"][0][0] = True
    assert not O["dependencies"](state, events)[1]


@pytest.fixture
def campaign(tmp_path):
    run = tmp_path / "DEV-r1"
    answer = {
        "columns": [{"name": "value", "type": "integer"}],
        "rows": [[0]],
        "empty_reason": None,
    }
    events = [
        {"kind": "answer", "payload": answer},
        {"kind": "run_end", "payload": {"status": "ok"}},
    ]
    for n, event in enumerate(events, 1):
        event.update(seq=n, run_id="actual-uuid", trace_id="actual-uuid")
    trace = run / "traces/original.jsonl"
    trace.parent.mkdir(parents=True)
    trace.write_text("".join(json.dumps(e) + "\n" for e in events))
    raw = {
        "result_spec": {
            "metric_id": "synthetic",
            "columns": [{"name": "value", "type": "integer", "nullable": False}],
        }
    }
    steps = [{"raw": raw, "step_id": "synthetic-step", "answer": answer, "dependency_rows": [[0]]}]
    events.insert(
        0,
        {
            "kind": "adapted_result",
            "payload": {"step_id": "synthetic-step", "answer": answer, "dependency_rows": [[0]]},
        },
    )
    for n, event in enumerate(events, 1):
        event.update(seq=n, run_id="actual-uuid", trace_id="actual-uuid")
    trace.write_text("".join(json.dumps(e) + "\n" for e in events))
    write(
        run / "exchanges.json",
        [
            {
                "status": "ok",
                "run_id": "actual-uuid",
                "events": events,
                "answer": answer,
                "error": None,
                "step_results": steps,
            }
        ],
    )
    write(run / "graph-state.json", {"scope": {}, "answer": answer, "step_results": steps})
    (run / "fixture.sqlite3").write_bytes(b"synthetic database identity")
    census = {"sha256": O["digest"](run / "fixture.sqlite3"), "rows": {"synthetic": 1}}
    write(run / "database-before.json", census)
    write(run / "database-after.json", census)
    write(
        run / "completed.json",
        {
            "run_id": "DEV-r1",
            "status": "completed",
            "calls": 0,
            "trace_hashes": {"DEV-r1/traces/original.jsonl": O["digest"](trace)},
        },
    )
    oracle = {
        "scope": {},
        "columns": ["value"],
        "types": ["integer"],
        "rows": [[0]],
        "empty_reason": None,
        "choices": [],
        "dependencies": {},
    }
    review = {
        "reviewer": "independent synthetic reviewer",
        "checks": {
            c: {
                "passed": True,
                "evidence": [
                    {
                        "path": "DEV-r1/traces/original.jsonl",
                        "sha256": O["digest"](trace),
                        "note": "Synthetic attestation; no live claim",
                    }
                ],
            }
            for c in O["CHECKS"]
        },
    }
    return tmp_path, run, oracle, review


def test_no_review_means_no_proof_not_pass(campaign):
    root, _, oracle, _ = campaign
    record = O["observe_run"](root, "DEV-r1", oracle)
    assert record["observed"] == oracle
    assert not any(record["checks"].values())


def test_independent_hash_bound_review_and_actual_result(campaign):
    root, _, oracle, review = campaign
    record = O["observe_run"](root, "DEV-r1", oracle, review)
    assert all(record["checks"].values())
    assert record["observed"] == oracle
    assert record["outcome"] == "success"


def test_false_safety_attestation_not_promoted(campaign):
    root, _, oracle, review = campaign
    review["checks"]["safe"]["passed"] = False
    assert not O["observe_run"](root, "DEV-r1", oracle, review)["checks"]["safe"]


def test_database_drift_overrides_positive_safety_review(campaign):
    root, run, oracle, review = campaign
    (run / "fixture.sqlite3").write_bytes(b"modified")
    assert not O["observe_run"](root, "DEV-r1", oracle, review)["checks"]["safe"]


def test_trace_hash_drift_fails_closed(campaign):
    root, run, oracle, review = campaign
    (run / "traces/original.jsonl").write_text("{}\n")
    with pytest.raises(ValueError, match="Original trace drift"):
        O["observe_run"](root, "DEV-r1", oracle, review)


def test_review_evidence_drift_fails_closed(campaign):
    root, _, _, review = campaign
    review["checks"]["private"]["evidence"][0]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="Reviewed evidence drift"):
        O["reviewed_checks"](review, root)


def test_claim_without_evidence_is_false(campaign):
    root, _, _, review = campaign
    review["checks"]["private"]["evidence"] = []
    assert not O["reviewed_checks"](review, root)["private"]


@pytest.mark.parametrize("started", [False, True])
def test_unfinished_records_remain_minimal(tmp_path, started):
    if started:
        write(tmp_path / "DEV-r1/started.json", {"run_id": "DEV-r1"})
    assert O["observe_run"](tmp_path, "DEV-r1", {}) == {
        "run_id": "DEV-r1",
        "status": "started" if started else "not-run",
    }


def test_error_no_answer_is_ordinary_failure_not_fabricated(campaign):
    root, run, oracle, review = campaign
    events = [
        {
            "kind": "run_end",
            "payload": {"status": "error"},
            "seq": 1,
            "run_id": "actual-uuid",
            "trace_id": "actual-uuid",
        }
    ]
    trace = run / "traces/original.jsonl"
    trace.write_text(json.dumps(events[0]) + "\n")
    completed = O["read"](run / "completed.json")
    completed["trace_hashes"]["DEV-r1/traces/original.jsonl"] = O["digest"](trace)
    write(run / "completed.json", completed)
    write(
        run / "exchanges.json",
        [
            {
                "status": "error",
                "run_id": "actual-uuid",
                "events": events,
                "answer": None,
                "error": {"code": "SQL_INVALID"},
                "step_results": [],
            }
        ],
    )
    for check in review["checks"].values():
        check["evidence"][0]["sha256"] = O["digest"](trace)
    record = O["observe_run"](root, "DEV-r1", oracle, review)
    assert record["outcome"] == "failure"
    assert record["checks"]["nonfabricated"]
    assert record["observed"]["rows"] == []


def test_observer_imports_no_product_provider_or_network():
    source = (ROOT / "tools/eval/observe.py").read_text()
    assert "import universitydb" not in source
    assert "import collector" not in source
    assert "import openai" not in source


def test_calls_disagreeing_with_original_attempts_cannot_pass(campaign):
    root, run, oracle, review = campaign
    completed = O["read"](run / "completed.json")
    completed["calls"] = 1
    write(run / "completed.json", completed)
    assert not O["observe_run"](root, "DEV-r1", oracle, review)["checks"]["trace_complete"]


def test_forged_success_without_adapted_proof_cannot_pass(campaign):
    root, run, oracle, review = campaign
    exchanges = O["read"](run / "exchanges.json")
    exchanges[-1]["step_results"][0]["answer"]["rows"] = [[1]]
    write(run / "exchanges.json", exchanges)
    assert not O["observe_run"](root, "DEV-r1", oracle, review)["checks"]["nonfabricated"]


def test_nonboolean_review_is_invalid(campaign):
    root, _, _, review = campaign
    review["checks"]["safe"]["passed"] = 1
    with pytest.raises(ValueError, match="strict boolean"):
        O["reviewed_checks"](review, root)


def test_evidence_cannot_escape_campaign(campaign):
    root, _, _, _ = campaign
    with pytest.raises(ValueError, match="Missing or escaping"):
        O["artifact"](root, "../outside.txt")


def test_provider_artifact_drift_fails_closed(campaign):
    root, run, oracle, review = campaign
    write(run / "provider/request.json", {"synthetic": True})
    completed = O["read"](run / "completed.json")
    completed["provider_artifacts"] = {"provider/request.json": "0" * 64}
    write(run / "completed.json", completed)
    with pytest.raises(ValueError, match="Provider evidence drift"):
        O["observe_run"](root, "DEV-r1", oracle, review)
