"""Synthetic monetary regression; never open the canonical authority."""

import hashlib
import json
from decimal import Decimal

import pytest

from universitydb.contracts import Failure
from universitydb.llm import Spending, load_h015, migrate_h015


def legacy(tmp_path):
    path = tmp_path / "spending.json"
    old = Spending(path, "gpt-6.1-sol", Decimal(10), Decimal("5.50"), Decimal(11), practical=True)
    held = old.reserve(12000, 32768)
    old.record_usage(held.attempt_id, 20, 10)
    return path, path.read_bytes()


def migrate(path, raw, backup):
    return migrate_h015(
        path,
        hashlib.sha256(raw).hexdigest(),
        backup,
        expected_calls=1,
        expected_effective_usd="0.426448",
    )


def test_migration_preserves_history_and_replay(tmp_path):
    path, raw = legacy(tmp_path)
    before = json.loads(raw)
    receipt = migrate(path, raw, tmp_path / "backup")
    assert (tmp_path / "backup").read_bytes() == raw
    assert (tmp_path / "backup").stat().st_mode & 0o777 == 0o600
    after = json.loads(path.read_bytes())
    assert after["attempts"] == before["attempts"]
    assert after["profile"] == before["profile"]
    assert after["effective_usd"] == before["effective_usd"]
    assert receipt["replayed"] is False
    current = path.read_bytes()
    assert migrate(path, raw, tmp_path / "backup")["replayed"] is True
    assert path.read_bytes() == current
    new = load_h015(path).reserve(12000, 32768)
    load_h015(path).record_usage(new.attempt_id, 10, 10)
    assert json.loads(path.read_bytes())["calls"] == 2
    with pytest.raises(Failure):
        Spending(
            path, "gpt-6.1-sol", Decimal(10), Decimal("5.50"), Decimal(11), practical=True
        ).reserve()


def test_stale_missing_and_corrupt_rejected(tmp_path):
    path, raw = legacy(tmp_path)
    with pytest.raises(Failure):
        migrate(path, raw + b" ", tmp_path / "backup")
    assert path.read_bytes() == raw
    path.write_text("{}")
    with pytest.raises(Failure):
        migrate(path, b"{}", tmp_path / "backup")
    path.unlink()
    with pytest.raises(Failure):
        migrate(path, raw, tmp_path / "backup")


def test_unsettled_hold_preserved_and_stopped(tmp_path):
    path, raw = legacy(tmp_path)
    record = json.loads(raw)
    record["attempts"][0].update(observed_usd=None, input_tokens=None, output_tokens=None)
    record.update(
        observed_usd="0",
        input_tokens=0,
        output_tokens=0,
        stop={"reason": "pending_usage", "attempt_id": record["attempts"][0]["id"]},
    )
    path.write_text(json.dumps(record))
    raw = path.read_bytes()
    migrate(path, raw, tmp_path / "backup")
    with pytest.raises(Failure):
        load_h015(path).reserve()


def test_drift_and_atomic_failure(tmp_path, monkeypatch):
    path, raw = legacy(tmp_path)
    from universitydb import llm

    def crash(*args):
        raise OSError("simulated replace crash")

    with monkeypatch.context() as m:
        m.setattr(llm.os, "replace", crash)
        with pytest.raises(Failure):
            migrate(path, raw, tmp_path / "backup")
    assert path.read_bytes() == raw
    migrate(path, raw, tmp_path / "backup")
    record = json.loads(path.read_bytes())
    record["authorizations"][0]["profile"]["input_rate"] = "1"
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path).reserve()


def test_shared_concurrent_reservation(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")

    def attempt(_):
        try:
            return load_h015(path).reserve().attempt_id
        except Failure:
            return None

    with ThreadPoolExecutor(max_workers=4) as pool:
        ids = list(pool.map(attempt, range(4)))
    assert sum(x is not None for x in ids) == 1
    assert len(load_h015(path).inspect()["uncertain_attempts"]) == 1


def test_campaign_limit_and_threshold(tmp_path):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    for _ in range(240):
        b = load_h015(path)
        call = b.reserve()
        b.record_usage(call.attempt_id, 0, 0)
    assert load_h015(path).inspect()["campaign_calls"] == 240
    before = path.read_bytes()
    with pytest.raises(Failure):
        load_h015(path).reserve()
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "failure", ["PROVIDER_REFUSAL", "PROVIDER_INVALID_OUTPUT", "PROVIDER_INCOMPLETE"]
)
@pytest.mark.parametrize("mode", ["known", "missing", "model", "tier"])
def test_h015_known_terminal_failure_can_continue(tmp_path, monkeypatch, failure, mode):
    from pathlib import Path
    from unittest.mock import patch

    from test_provider_worker import configure

    from universitydb.contracts import PlanProposal
    from universitydb.llm import OpenAIProvider

    configure(monkeypatch)
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    monkeypatch.setenv("UNIVERSITYDB_BUDGET_POLICY", "h015-practical-v1")
    monkeypatch.setenv("UNIVERSITYDB_CAP_USD", "120")
    monkeypatch.setenv("UNIVERSITYDB_INPUT_USD_PER_MILLION", "5.50")
    monkeypatch.setenv("UNIVERSITYDB_OUTPUT_USD_PER_MILLION", "11")
    monkeypatch.setattr("universitydb.llm.canonical_budget_path", lambda: path)
    response = {
        "error": failure,
        "message": "terminal",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "returned_model": "gpt-6.1-sol",
            "returned_service_tier": "default",
        },
        "raw_response": {"id": "response-original", "output": [{"content": [{"type": "refusal"}]}]},
    }

    if mode == "missing":
        del response["usage"]["input_tokens"]
    elif mode == "model":
        response["usage"]["returned_model"] = "other"
    elif mode == "tier":
        response["usage"]["returned_service_tier"] = "priority"

    class Worker:
        returncode = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def communicate(self, *args, **kwargs):
            return json.dumps(response), None

    evidence = tmp_path / "evidence"
    with (
        patch("universitydb.llm.subprocess.Popen", return_value=Worker()),
        pytest.raises(Failure) as caught,
    ):
        OpenAIProvider(Path("src/universitydb/prompts"), path, evidence_dir=evidence).call(
            "plan", {}, PlanProposal
        )
    assert caught.value.details["accounting_stop"] is (mode != "known")
    assert (load_h015(path).inspect()["stop"] is None) == (mode == "known")
    assert bool(load_h015(path).inspect()["uncertain_attempts"]) == (mode == "missing")
    files = list(evidence.glob("*.json"))
    assert len(files) == 2
    for file in files:
        assert "OPENAI_API_KEY" not in file.read_text()
        assert file.stat().st_mode & 0o777 == 0o600
        kind = "request" if file.name.endswith("request.json") else "response"
        assert (
            hashlib.sha256(file.read_bytes()).hexdigest()
            == caught.value.details[f"evidence_{kind}_sha256"]
        )
    if mode == "known":
        assert load_h015(path).reserve()
    else:
        with pytest.raises(Failure):
            load_h015(path).reserve()


@pytest.mark.parametrize(
    "field,value", [("input_rate", "NaN"), ("output_rate", "-1"), ("cap_usd", "121")]
)
def test_policy_rate_or_cap_drift_rejected(tmp_path, field, value):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    record = json.loads(path.read_bytes())
    record["authorizations"][1][field] = value
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path)


def test_reservation_envelope_no_lower_bound_bypass(tmp_path):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    before = path.read_bytes()
    with pytest.raises(Failure):
        load_h015(path).reserve(1, 1)
    assert before == path.read_bytes()


def _process_migrate(args):
    path, raw, backup = args
    return migrate(path, raw, backup)["replayed"]


def _process_reserve(path):
    try:
        return load_h015(path).reserve().attempt_id
    except Failure:
        return None


def test_two_process_migration_and_reservation(tmp_path):
    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor

    path, raw = legacy(tmp_path)
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(max_workers=2, mp_context=context) as pool:
        replay = list(pool.map(_process_migrate, [(path, raw, tmp_path / "backup")] * 2))
        assert sorted(replay) == [False, True]
        reservations = list(pool.map(_process_reserve, [path, path]))
    assert sum(v is not None for v in reservations) == 1
    assert load_h015(path).inspect()["calls"] == 2


def test_dispatch_equality_then_overflow(tmp_path):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    b = load_h015(path)
    # Synthetic test boundary only: live loader always restores fixed110 policy.
    b.threshold = Decimal("0.852896")
    call = b.reserve()
    b.record_usage(call.attempt_id, 0, 0)
    assert load_h015(path).snapshot()["effective_usd"] == "0.852896"
    before = path.read_bytes()
    with pytest.raises(Failure):
        b.reserve()
    assert path.read_bytes() == before


def test_historical_rate_segment_remains_distinct(tmp_path):
    path = tmp_path / "spending.json"
    old = Spending(path, "gpt-6.1-sol", Decimal(10), Decimal(1), Decimal(2), practical=True)
    call = old.reserve(1000, 2000)
    old.record_usage(call.attempt_id, 100, 200)
    raw = path.read_bytes()
    migrate_h015(
        path,
        hashlib.sha256(raw).hexdigest(),
        tmp_path / "backup",
        expected_calls=1,
        expected_effective_usd="0.005",
    )
    b = load_h015(path)
    call = b.reserve()
    b.record_usage(call.attempt_id, 100, 200)
    assert load_h015(path).snapshot()["observed_usd"] == "0.00325"
    record = json.loads(path.read_bytes())
    record["authorizations"][0]["profile"]["input_rate"] = "1.5"
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path)


@pytest.mark.parametrize("value", [2.0, True, "2"])
def test_policy_version_type_is_strict(tmp_path, value):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    record = json.loads(path.read_bytes())
    record["authorizations"][1]["version"] = value
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path)


def test_original_profile_type_drift_is_strict(tmp_path):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    record = json.loads(path.read_bytes())
    record["profile"]["version"] = True
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path)


def test_ledger_call_count_type_is_strict(tmp_path):
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    record = json.loads(path.read_bytes())
    record["calls"] = True
    path.write_text(json.dumps(record))
    with pytest.raises(Failure):
        load_h015(path)


def test_provider_rejects_noncanonical_h015_authority(tmp_path, monkeypatch):
    from pathlib import Path
    from unittest.mock import patch

    from test_provider_worker import configure

    from universitydb.contracts import PlanProposal
    from universitydb.llm import OpenAIProvider

    configure(monkeypatch)
    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    before = path.read_bytes()
    monkeypatch.setenv("UNIVERSITYDB_BUDGET_POLICY", "h015-practical-v1")
    monkeypatch.setattr("universitydb.llm.canonical_budget_path", lambda: tmp_path / "other.json")
    with patch("universitydb.llm.subprocess.Popen") as dispatch, pytest.raises(Failure):
        OpenAIProvider(Path("src/universitydb/prompts"), path).call("plan", {}, PlanProposal)
    dispatch.assert_not_called()
    assert path.read_bytes() == before
