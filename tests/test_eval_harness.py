"""Synthetic/dev scorer checks only. Never execute proposed live cases."""

import copy
import hashlib
import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
H = runpy.run_path(str(ROOT / "tools/eval/harness.py"))
DEV = ROOT / "docs/operations/H-014/eval/dev-v1.json"


@pytest.fixture
def pack():
    return json.loads(DEV.read_text())


@pytest.fixture
def record(pack, tmp_path):
    trace = tmp_path / "synthetic.jsonl"
    trace.write_text('{"synthetic":true}\n')
    return {
        "run_id": "DEV01-r1",
        "status": "completed",
        "outcome": "success",
        "observed": copy.deepcopy(pack["oracle"]["cases"]["DEV01"]),
        "checks": dict.fromkeys(H["CHECKS"], True),
        "calls": 0,
        "trace_sha256": hashlib.sha256(trace.read_bytes()).hexdigest(),
        "trace_path": str(trace),
    }


def score(pack, record, tmp_path):
    # Resources are pinned in the real root, trace evidence isolated in tmp_path.
    H["validate"](pack, ROOT)
    dev = copy.deepcopy(pack)
    for path in list(dev["source_hashes"]):
        dev["source_hashes"][str(ROOT / path)] = dev["source_hashes"].pop(path)
    for f in dev["fixtures"].values():
        for k in ("schema", "seed"):
            f[k] = str(ROOT / f[k])
        content = {k: v for k, v in f.items() if k != "sha256"}
        f["sha256"] = hashlib.sha256(
            json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
    return H["score"](dev, [record], tmp_path)


def test_dev_exact_score(pack, record, tmp_path):
    result = score(pack, record, tmp_path)
    assert result["observed_passes"] == 1
    assert result["planned_denominator"] == 1
    assert result["proposed_threshold_met"] is False


@pytest.mark.parametrize("value", [False, 0.0, "0", 1])
def test_typed_values_not_coerced(pack, record, tmp_path, value):
    record["observed"]["rows"][0][0] = value
    assert score(pack, record, tmp_path)["observed_passes"] == 0


@pytest.mark.parametrize("status", ["planned", "not-run", "started"])
def test_no_results_is_not_success(pack, status):
    result = H["score"](pack, [{"run_id": "DEV01-r1", "status": status}], ROOT)
    assert not result["complete"] and result["planned_denominator"] == 1
    assert result["observed_passes"] == 0


@pytest.mark.parametrize("outcome", ["failure", "timeout", "refusal", "invalid", "infra_abort"])
def test_terminal_failures_retained(pack, record, tmp_path, outcome):
    record["outcome"] = outcome
    result = score(pack, record, tmp_path)
    assert result["complete"] and result["observed_passes"] == 0


@pytest.mark.parametrize("field", H["CHECKS"])
def test_mandatory_check_failure(pack, record, tmp_path, field):
    record["checks"][field] = False
    assert score(pack, record, tmp_path)["observed_passes"] == 0


@pytest.mark.parametrize(
    "records",
    [
        [],
        [{"run_id": "unknown", "status": "not-run"}],
        [{"run_id": "DEV01-r1", "status": "not-run"}] * 2,
    ],
)
def test_missing_duplicate_unknown_fail_closed(pack, records):
    with pytest.raises(ValueError):
        H["score"](pack, records, ROOT)


def test_export_has_no_oracle_fields(pack):
    payload = H["payloads"](pack, ROOT)[0]
    assert set(payload) == {
        "run_id",
        "case_id",
        "repeat",
        "domain",
        "fixture",
        "question",
        "selections",
    }
    pack["questions"]["cases"][0]["expected"] = 42
    with pytest.raises(ValueError, match="leakage"):
        H["payloads"](pack, ROOT)


@pytest.mark.parametrize("mutation", ["source", "fixture", "type", "duplicate", "oracle"])
def test_invalid_package(pack, mutation):
    if mutation == "source":
        pack["source_hashes"]["resources/seed.sql"] = "0" * 64
    elif mutation == "fixture":
        pack["fixtures"]["u"]["mutations"].append("unsafe change")
    elif mutation == "type":
        pack["oracle"]["cases"]["DEV01"]["rows"] = [[True]]
    elif mutation == "duplicate":
        pack["questions"]["cases"] *= 2
    else:
        pack["oracle"]["cases"] = {}
    with pytest.raises(ValueError):
        H["validate"](pack, ROOT)


@pytest.mark.parametrize(
    "field,value",
    [
        ("calls", True),
        ("calls", 6),
        ("trace_sha256", "bad"),
        ("trace_path", "missing"),
        ("outcome", "skip"),
    ],
)
def test_invalid_record(pack, record, tmp_path, field, value):
    record[field] = value
    with pytest.raises((ValueError, FileNotFoundError)):
        score(pack, record, tmp_path)
