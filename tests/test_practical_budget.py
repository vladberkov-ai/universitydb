import json
from decimal import Decimal

import pytest

from universitydb.contracts import Failure
from universitydb.llm import Spending


def budget(path):
    return Spending(path, "gpt-6.1-sol", Decimal(10), Decimal(1), Decimal(1), practical=True)


def test_threshold_and_restart_pending_hold(tmp_path):
    path = tmp_path / "spending.json"
    b = budget(path)
    first = b.reserve(1_000_000, 7_000_000)
    with pytest.raises(Failure):
        budget(path).reserve(1, 1)
    b.record_usage(first.attempt_id, 1, 1)
    assert json.loads(path.read_text())["effective_usd"] == "8"
    with pytest.raises(Failure):
        budget(path).reserve(1, 1)


def test_history_preserved_and_policy_cannot_be_downgraded(tmp_path):
    path = tmp_path / "spending.json"
    old = Spending(path, "gpt-6.1-sol", Decimal(10), Decimal(1), Decimal(1))
    old_call = old.reserve(100, 100)
    old.record_usage(old_call.attempt_id, 1, 1)
    history = json.loads(path.read_text())["attempts"]
    current = budget(path).reserve(100, 100)
    record = json.loads(path.read_text())
    assert record["attempts"][:-1] == history
    with pytest.raises(Failure):
        old.reserve(100, 100)
    budget(path).record_usage(current.attempt_id, 1, 1)


def test_excess_or_uncertainty_durable_stop(tmp_path):
    path = tmp_path / "spending.json"
    b = budget(path)
    reservation = b.reserve(1, 1)
    b.record_usage(reservation.attempt_id, 100, 100)
    with pytest.raises(Failure):
        budget(path).reserve(1, 1)
    record = json.loads(path.read_text())
    assert record["stop"]["reason"] == "usage_exceeds_reservation"
    assert record["observed_usd"] == "0.0002"


def test_practical_cap_fixed(tmp_path):
    with pytest.raises(Failure):
        Spending(tmp_path / "s", "gpt-6.1-sol", Decimal(11), Decimal(1), Decimal(1), practical=True)


def test_unknown_legacy_hold_cannot_be_dispatched_around(tmp_path):
    path = tmp_path / "s"
    old = Spending(path, "gpt-6.1-sol", Decimal(10), Decimal(1), Decimal(1))
    old.reserve(100, 100)
    before = path.read_bytes()
    with pytest.raises(Failure):
        budget(path).reserve(100, 100)
    assert path.read_bytes() == before


def test_practical_reservation_atomic_between_callers(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = tmp_path / "s"

    def attempt(_):
        try:
            return budget(path).reserve(1, 1).attempt_id
        except Failure:
            return None

    with ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(attempt, range(4)))
    assert sum(v is not None for v in result) == 1
    assert json.loads(path.read_text())["calls"] == 1


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-1", "0"])
def test_practical_invalid_rates(tmp_path, value):
    with pytest.raises(Failure):
        Spending(
            tmp_path / "s", "gpt-6.1-sol", Decimal(10), Decimal(value), Decimal(1), practical=True
        )


@pytest.mark.parametrize(
    "fault", ["missing", "negative", "bool", "total", "excess", "model", "tier", "transport"]
)
def test_bad_response_persists_stop_across_provider_restart(tmp_path, monkeypatch, fault):
    from pathlib import Path
    from unittest.mock import patch

    from conftest import outputs
    from test_provider_worker import configure

    from universitydb.contracts import PlanProposal
    from universitydb.llm import OpenAIProvider

    configure(monkeypatch)
    usage = {
        "input_tokens": 100,
        "output_tokens": 50,
        "total_tokens": 150,
        "returned_model": "gpt-6.1-sol",
        "returned_service_tier": "default",
    }
    response = {"output": outputs()[0], "usage": usage}
    if fault == "missing":
        del usage["input_tokens"]
    elif fault == "negative":
        usage["input_tokens"] = -1
    elif fault == "bool":
        usage["input_tokens"] = True
    elif fault == "total":
        usage["total_tokens"] = 151
    elif fault == "excess":
        usage.update(input_tokens=12001, total_tokens=12051)
    elif fault == "model":
        usage["returned_model"] = "other"
    elif fault == "tier":
        usage["returned_service_tier"] = "priority"
    elif fault == "transport":
        response = {"error": "PROVIDER_TRANSIENT", "message": "safe transport error"}

    class Worker:
        returncode = 0

        def __enter__(self):
            return self

        def __exit__(self, *_):
            pass

        def communicate(self, *_args, **_kwargs):
            return json.dumps(response), None

    path = tmp_path / "s"
    with patch("universitydb.llm.subprocess.Popen", return_value=Worker()) as dispatch:
        for _ in range(2):
            provider = OpenAIProvider(Path("src/universitydb/prompts"), path)
            with pytest.raises(Failure):
                provider.call("plan", {}, PlanProposal)
        assert dispatch.call_count == 1
    record = json.loads(path.read_text())
    assert record["stop"] is not None
    assert record["calls"] == 1
    assert Decimal(record["reserved_usd"]) > 0
    if fault in ("excess", "model", "tier"):
        assert record["input_tokens"] == usage["input_tokens"]


def test_full_payload_estimate_includes_schema_and_metadata():
    from universitydb.config import payload_estimate, wire_payload

    wire = wire_payload("plan", "plan", "gpt-6.1-sol", "instructions", '{"history":[],"tools":[]}')
    size, estimate = payload_estimate(wire)
    assert size == len(json.dumps(wire, ensure_ascii=False).encode())
    assert estimate == size + 1024
    assert wire["text"]["format"]["strict"] is True
    assert wire["reasoning"] == {"effort": "high"}
    assert wire["service_tier"] == "default"


def test_old_billing_flag_never_authorizes_new_policy(tmp_path, monkeypatch):
    from pathlib import Path
    from unittest.mock import patch

    from test_provider_worker import configure

    from universitydb.contracts import PlanProposal
    from universitydb.llm import OpenAIProvider

    configure(monkeypatch)
    monkeypatch.delenv("UNIVERSITYDB_BUDGET_POLICY")
    monkeypatch.setenv("UNIVERSITYDB_BILLING_VERIFIED", "yes")
    with patch("universitydb.llm.subprocess.Popen") as dispatch, pytest.raises(Failure):
        OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "s").call(
            "plan", {}, PlanProposal
        )
    dispatch.assert_not_called()
    assert not (tmp_path / "s").exists()


def test_existing_holds_plus_next_reservation_exact_boundary(tmp_path):
    path = tmp_path / "s"
    b = budget(path)
    old = b.reserve(3_000_000, 3_000_000)
    b.record_usage(old.attempt_id, 1, 1)
    next_call = b.reserve(1_000_000, 1_000_000)
    b.record_usage(next_call.attempt_id, 1, 1)
    assert json.loads(path.read_text())["effective_usd"] == "8"
    with pytest.raises(Failure):
        budget(path).reserve(1, 1)


def test_uncertain_live_failure_never_application_retried(database, tmp_path):
    from conftest import QUESTION

    from universitydb.agent import Agent
    from universitydb.domain import University
    from universitydb.llm import ScriptedProvider

    provider = ScriptedProvider(
        [Failure("PROVIDER_TRANSIENT", "unknown usage", details={"accounting_stop": True})]
    )
    result = Agent(University(), database, provider, tmp_path / "traces").run(QUESTION)
    assert provider.calls == 1
    assert result["error"]["code"] == "PROVIDER_TRANSIENT"
