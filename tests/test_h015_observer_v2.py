"""Synthetic-only post-results instrument repair; never reads actual collection/oracle."""

import copy
import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
V2 = runpy.run_path(str(ROOT / "tools/eval/correct_mean_nullability_v2.py"))


def fixture(value="37.25", reason=None):
    spec = copy.deepcopy(V2["SCALAR_MEAN_SPEC"])
    answer = {
        "columns": [
            {"name": n, "type": t}
            for n, t in [
                ("average", "decimal"),
                ("graded_count", "integer"),
                ("enrollment_count", "integer"),
            ]
        ],
        "rows": [[value, 0 if value is None else 1, 2]],
        "empty_reason": reason,
    }
    step = {
        "step_id": "synthetic-step",
        "answer": answer,
        "raw": {"step_id": "synthetic-step", "result_spec": spec, "rows": [[3725, 1, 2]]},
    }
    events = [
        {"kind": "db_result", "payload": step["raw"]},
        {"kind": "adapted_result", "payload": {k: v for k, v in step.items() if k != "raw"}},
        {"kind": "answer", "payload": answer},
    ]
    final = {
        "status": "ok",
        "run_id": "inner",
        "answer": answer,
        "step_results": [step],
        "events": events,
        "error": None,
    }
    state = {
        "answer": answer,
        "step_results": [step],
        "scope": {},
        "completed": {"synthetic-step": step["raw"]},
    }
    record = {
        "run_id": "synthetic-run",
        "status": "completed",
        "outcome": "success",
        "observed": {
            "scope": {},
            "columns": ["mean", "graded_count", "enrollment_count"],
            "types": ["decimal?" if value is None else "decimal", "integer", "integer"],
            "rows": copy.deepcopy(answer["rows"]),
            "empty_reason": reason,
            "choices": [],
            "dependencies": {},
        },
        "checks": dict.fromkeys(V2["CHECKS"], True),
        "calls": 2,
        "trace_sha256": "a" * 64,
        "trace_path": "/synthetic/traces/one.jsonl",
    }
    return record, state, [final]


@pytest.mark.parametrize(
    "value,reason", [("37.25", None), ("0.00", None), (None, "no_grades"), (None, "no_rows")]
)
def test_contract_nullable_independent_of_cell_and_preserves_everything(value, reason):
    inputs = fixture(value, reason)
    original = copy.deepcopy(inputs)
    result, changes = V2["correct_record"](*inputs)
    expected = copy.deepcopy(original[0])
    expected["observed"]["types"][0] = "decimal?"
    assert result == expected
    assert inputs == original
    assert len(changes) == (0 if value is None else 1)
    if changes:
        assert changes == [{"field": "/observed/types/0", "old": "decimal", "new": "decimal?"}]


@pytest.mark.parametrize(
    "fault",
    [
        "bool",
        "empty",
        "spec",
        "state",
        "rows",
        "type",
        "status",
        "outcome",
        "columns",
        "scope",
        "raw",
        "metric",
    ],
)
def test_fail_closed(fault):
    record, state, exchanges = fixture()
    if fault == "bool":
        record["observed"]["rows"][0][1] = True
    elif fault == "empty":
        record["observed"]["rows"] = []
    elif fault == "spec":
        exchanges[-1]["step_results"][-1]["raw"]["result_spec"]["scale"] = True
    elif fault == "state":
        state["answer"] = None
    elif fault == "rows":
        record["observed"]["rows"][0][0] = "99.99"
    elif fault == "type":
        record["observed"]["types"][0] = "integer"
    elif fault == "status":
        exchanges[-1]["status"] = "unknown"
    elif fault == "outcome":
        record["outcome"] = "failure"
    elif fault == "columns":
        record["observed"]["columns"] = ["mean", "mean", "enrollment_count"]
    elif fault == "scope":
        record["observed"]["scope"] = {"invented": 1}
    elif fault == "raw":
        state["completed"] = {}
    else:
        exchanges[-1]["step_results"][-1]["raw"]["result_spec"]["metric_id"] = "unknown"
    with pytest.raises(ValueError):
        V2["correct_record"](record, state, exchanges)


def test_grouped_and_other_registered_metrics_untouched():
    for metric, groups in [
        ("u.grade_mean.v1", ["student_id"]),
        ("u.top_course.v1", []),
        ("u.enrollment_counts.v1", []),
        ("u.student_ids.v1", []),
        ("u.enrollment_rows.v1", []),
    ]:
        record, state, exchanges = fixture()
        exchanges[-1]["step_results"][-1]["raw"]["result_spec"].update(
            metric_id=metric, group_keys=groups
        )
        result, changes = V2["correct_record"](record, state, exchanges)
        assert result == record and changes == []


def test_strict_json_duplicate_nonfinite_and_boolean_types(tmp_path):
    path = tmp_path / "input.json"
    for content in ['{"x":1,"x":2}', "[NaN]"]:
        path.write_text(content)
        with pytest.raises(ValueError):
            V2["read"](path)
    record, state, exchanges = fixture()
    record["calls"] = True
    with pytest.raises(ValueError):
        V2["correct_record"](record, state, exchanges)


def synthetic_campaign(tmp_path):
    campaign = tmp_path / "campaign"
    campaign.mkdir()
    record, state, exchanges = fixture()
    trace = campaign / "synthetic-run/traces/one.jsonl"
    trace.parent.mkdir(parents=True)
    trace.write_text("\n".join(json.dumps(e) for e in exchanges[-1]["events"]) + "\n")
    record.update(trace_path=str(trace), trace_sha256=V2["digest"](trace))
    artifacts = {
        "synthetic-run/graph-state.json": state,
        "synthetic-run/exchanges.json": exchanges,
        "synthetic-run/completed.json": {
            "run_id": "synthetic-run",
            "status": "completed",
            "calls": 2,
            "trace_hashes": {"synthetic-run/traces/one.jsonl": V2["digest"](trace)},
        },
    }
    for name, value in artifacts.items():
        (campaign / name).write_text(json.dumps(value))
    records = tmp_path / "records.json"
    records.write_text(json.dumps([record]))
    hashes = {name: V2["digest"](campaign / name) for name in artifacts}
    hashes["synthetic-run/traces/one.jsonl"] = V2["digest"](trace)
    receipt = tmp_path / "source-receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "source_version": "h015-observer-v1",
                "observer_sha256": V2["FROZEN_OBSERVER_SHA256"],
                "records_sha256": V2["digest"](records),
                "artifacts": hashes,
            }
        )
    )
    return campaign, records, receipt


def test_new_output_manifest_exclusive_and_no_oracle_access(tmp_path):
    campaign, records, receipt = synthetic_campaign(tmp_path)
    originals = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    output, manifest = tmp_path / "v2.json", tmp_path / "manifest.json"
    V2["run"](campaign, records, receipt, output, manifest)
    assert json.loads(output.read_text())[0]["observed"]["types"][0] == "decimal?"
    audit = json.loads(manifest.read_text())
    assert audit["output_sha256"] == V2["digest"](output)
    assert len(audit["changes"]) == 1
    assert all(p.read_bytes() == data for p, data in originals.items())
    with pytest.raises(FileExistsError):
        V2["run"](campaign, records, receipt, output, manifest)
    assert all(p.read_bytes() == data for p, data in originals.items())


@pytest.mark.parametrize("fault", ["duplicate", "drift", "escaping", "missing", "receipt", "alias"])
def test_campaign_rejects_bad_receipt_references_and_duplicate_runs(tmp_path, fault):
    campaign, records, receipt = synthetic_campaign(tmp_path)
    data = json.loads(receipt.read_text())
    if fault == "duplicate":
        value = json.loads(records.read_text())
        records.write_text(json.dumps(value * 2))
        data["records_sha256"] = V2["digest"](records)
    elif fault == "drift":
        (campaign / "synthetic-run/graph-state.json").write_text("{}")
    elif fault == "escaping":
        data["artifacts"]["../records.json"] = data["records_sha256"]
    elif fault == "missing":
        del data["artifacts"]["synthetic-run/exchanges.json"]
    elif fault == "receipt":
        data["source_version"] = "unknown"
    receipt.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        V2["run"](
            campaign,
            records,
            receipt,
            records if fault == "alias" else tmp_path / "v2.json",
            tmp_path / "manifest.json",
        )
    assert not (tmp_path / "manifest.json").exists()


@pytest.mark.parametrize(
    "outcome,code",
    [("failure", "INVALID_INPUT"), ("timeout", "SQL_TIMEOUT"), ("refusal", "PROVIDER_REFUSAL")],
)
def test_failure_records_and_checks_unchanged(outcome, code):
    record, state, exchanges = fixture()
    record["outcome"] = outcome
    record["checks"] = dict.fromkeys(V2["CHECKS"], False)
    exchanges[-1].update(status="error", answer=None, error={"code": code})
    updated, changes = V2["correct_record"](record, state, exchanges)
    assert updated == record and not changes


def test_existing_manifest_is_not_overwritten_or_orphan_output_left(tmp_path):
    campaign, records, receipt = synthetic_campaign(tmp_path)
    output, manifest = tmp_path / "new.json", tmp_path / "exists.json"
    manifest.write_text("original")
    with pytest.raises(FileExistsError):
        V2["run"](campaign, records, receipt, output, manifest)
    assert manifest.read_text() == "original" and not output.exists()


def test_untouched_minimal_statuses_and_duplicate_json(tmp_path):
    campaign, records, receipt = synthetic_campaign(tmp_path)
    values = [
        {"run_id": "untouched", "status": "not-run"},
        {"run_id": "unknown-charge", "status": "started"},
    ]
    records.write_text(json.dumps(values))
    source = json.loads(receipt.read_text())
    source.update(records_sha256=V2["digest"](records), artifacts={})
    receipt.write_text(json.dumps(source))
    output, manifest = tmp_path / "v2.json", tmp_path / "manifest.json"
    V2["run"](campaign, records, receipt, output, manifest)
    assert json.loads(output.read_text()) == values
    assert json.loads(manifest.read_text())["changes"] == []


def test_postprocessor_has_no_oracle_product_observer_or_network_import():
    import ast

    tree = ast.parse((ROOT / "tools/eval/correct_mean_nullability_v2.py").read_text())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module)
    assert imported == {"argparse", "copy", "hashlib", "json", "re", "pathlib", "typing"}


def test_projected_mean_only_preserves_false_checks_and_does_not_promote():
    record, state, exchanges = fixture("0.00")
    record["observed"].update(columns=["mean"], types=["decimal"], rows=[["0.00"]])
    record["checks"] = dict.fromkeys(V2["CHECKS"], False)
    updated, changes = V2["correct_record"](record, state, exchanges)
    assert updated["observed"]["rows"] == [["0.00"]]
    assert updated["checks"] == record["checks"]
    assert updated["observed"]["types"] == ["decimal?"]
    assert len(changes) == 1
    with pytest.raises(ValueError):
        V2["correct_record"](updated, state, exchanges)


def test_synthetic_cli(tmp_path):
    import subprocess
    import sys

    campaign, records, receipt = synthetic_campaign(tmp_path)
    output, manifest = tmp_path / "v2.json", tmp_path / "manifest.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/eval/correct_mean_nullability_v2.py"),
            "--campaign",
            str(campaign),
            "--records",
            str(records),
            "--source-receipt",
            str(receipt),
            "--output",
            str(output),
            "--manifest",
            str(manifest),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(manifest.read_text())["version"] == V2["VERSION"]


def test_registered_library_success_stays_count_only_and_unchanged():
    record, state, exchanges = fixture()
    spec = {
        "metric_id": "l.open_count.v1",
        "shape": "aggregate",
        "group_keys": ["reader_id"],
        "columns": [
            {"name": name, "type": kind, "nullable": False}
            for name, kind in [
                ("reader_id", "integer"),
                ("name", "string"),
                ("open_count", "integer"),
            ]
        ],
        "components": {"sum": None, "denominator": None, "count": "open_count"},
        "unit": "count",
        "scale": 1,
    }
    answer = {
        "columns": [{"name": col["name"], "type": col["type"]} for col in spec["columns"]],
        "rows": [[17, "Synthetic reader", 0], [23, "Other reader", 4]],
        "empty_reason": None,
    }
    step = {
        "step_id": "synthetic-library",
        "answer": answer,
        "dependency_rows": copy.deepcopy(answer["rows"]),
        "raw": {
            "step_id": "synthetic-library",
            "result_spec": spec,
            "rows": copy.deepcopy(answer["rows"]),
        },
    }
    events = [
        {"kind": "db_result", "payload": step["raw"]},
        {"kind": "adapted_result", "payload": {k: v for k, v in step.items() if k != "raw"}},
        {"kind": "answer", "payload": answer},
    ]
    final = exchanges[-1]
    final.update(answer=answer, step_results=[step], events=events)
    state.update(
        answer=answer,
        step_results=[step],
        completed={"synthetic-library": step["raw"]},
        scope={},
    )
    record["observed"].update(
        scope={},
        columns=["reader_id", "name", "open_count"],
        types=["integer", "string", "integer"],
        rows=copy.deepcopy(answer["rows"]),
    )
    original = copy.deepcopy((record, state, exchanges))
    updated, changes = V2["correct_record"](record, state, exchanges)
    assert updated == record and changes == []
    assert (record, state, exchanges) == original
    assert "decimal?" not in updated["observed"]["types"]
    assert updated["observed"]["rows"][0][-1] == 0
