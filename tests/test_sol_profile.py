"""Offline payload/accounting evidence, never real-provider accuracy."""

import json
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from conftest import QUESTION, outputs

from universitydb.agent import Agent
from universitydb.config import PROFILE, Profile
from universitydb.contracts import Failure, PlanProposal, SQLProposal
from universitydb.domain import University
from universitydb.llm import OpenAIProvider, ScriptedProvider, Spending
from universitydb.llm_worker import request


@pytest.mark.parametrize(
    "logical,effort,index", [("plan", "high", 0), ("sql", "medium", 1), ("repair", "medium", 1)]
)
def test_exact_sdk_payload(logical, effort, index):
    schema = (PlanProposal, SQLProposal)[index]
    client = MagicMock()
    client.responses.create.return_value = SimpleNamespace(
        status="completed",
        output=[],
        output_text=json.dumps(outputs()[index]),
        usage=SimpleNamespace(input_tokens=100, output_tokens=50, total_tokens=150),
        model=PROFILE.model,
        service_tier="default",
        id="offline",
    )
    policy = PROFILE.operation(logical)
    with patch("universitydb.llm_worker.OpenAI") as sdk:
        sdk.return_value.__enter__.return_value = client
        request(
            {
                "operation": "plan" if index == 0 else "sql",
                "logical_operation": logical,
                "model": PROFILE.model,
                "timeout": policy.timeout,
                "prompt": "test",
                "input": "{}",
            }
        )
    sdk.assert_called_once_with(max_retries=0, timeout=policy.timeout)
    client.responses.create.assert_called_once_with(
        model=PROFILE.model,
        store=False,
        max_output_tokens=32768,
        reasoning={"effort": effort},
        service_tier="default",
        instructions="test",
        input="{}",
        text={
            "format": {
                "type": "json_schema",
                "name": schema.__name__,
                "strict": True,
                "schema": schema.model_json_schema(),
            }
        },
    )


@pytest.mark.parametrize(
    "change", [{"model": "other"}, {"service_tier": "auto"}, {"calls": 0}, {"run_seconds": 0}]
)
def test_invalid_config_rejected(change):
    with pytest.raises(Failure):
        Profile(**change).validate()


@pytest.mark.parametrize("operation,model", [("unknown", PROFILE.model), ("plan", "other")])
def test_worker_invalid_before_client(operation, model):
    with patch("universitydb.llm_worker.OpenAI") as sdk, pytest.raises(Failure):
        request(
            {"operation": operation, "logical_operation": operation, "model": model, "timeout": 1}
        )
    sdk.assert_not_called()


@pytest.mark.parametrize(
    "missing",
    [
        "OPENAI_API_KEY",
        "UNIVERSITYDB_CAP_USD",
        "UNIVERSITYDB_LIVE_APPROVED",
        "UNIVERSITYDB_BILLING_VERIFIED",
    ],
)
def test_live_gate_zero_dispatch(tmp_path, monkeypatch, missing):
    from test_provider_worker import configure

    configure(monkeypatch)
    monkeypatch.delenv(missing)
    with patch("universitydb.llm.subprocess.Popen") as process, pytest.raises(Failure):
        OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "spend.json").call(
            "plan", {}, PlanProposal
        )
    process.assert_not_called()
    assert not (tmp_path / "spend.json").exists()


def test_policy_continuation_keeps_old_uncertain_hold_and_total_cap(tmp_path):
    path = tmp_path / "spend.json"

    def budget():
        return Spending(path, PROFILE.model, Decimal(".07"), Decimal(1), Decimal(1))

    old = budget().reserve()  # Exact old12000/2000 representation; no migration/reset.
    new = budget().reserve(PROFILE.input_tokens, PROFILE.operation("plan").output_tokens)
    assert old.amount == "0.014" and new.amount == "0.044768"
    record = json.loads(path.read_text())
    assert record["calls"] == 2 and len(record["attempts"]) == 2
    before = path.read_bytes()
    with pytest.raises(Failure):
        budget().reserve(PROFILE.input_tokens, PROFILE.operation("sql").output_tokens)
    assert path.read_bytes() == before
    for cap, rate in [(".08", "1"), (".07", "2")]:
        with pytest.raises(Failure):
            Spending(path, PROFILE.model, Decimal(cap), Decimal(rate), Decimal(1)).reserve()
    assert path.read_bytes() == before


def test_trace_retry_and_logical_repair_profile(database, tmp_path, monkeypatch):
    monkeypatch.setattr("universitydb.agent.time.sleep", lambda _: None)
    plan, bad = outputs(sql="SELECT (")
    provider = ScriptedProvider(
        [Failure("PROVIDER_TRANSIENT", "injected"), plan, bad, outputs()[1]]
    )
    result = Agent(University(), database, provider, tmp_path / "trace").run(QUESTION)
    assert result["status"] == "ok"
    attempts = [
        e["payload"]
        for e in result["events"]
        if e["kind"] == "llm_attempt"
        and e["payload"].get("phase") == "application_attempt_before_dispatch"
    ]
    assert [a["logical_operation"] for a in attempts] == ["plan", "plan", "sql", "repair"]
    assert [a["reasoning_effort"] for a in attempts] == ["high", "high", "medium", "medium"]
    assert attempts[-1]["reserved_run_tokens"] == 4 * (12000 + 32768)


def test_run_token_limit_prevents_dispatch(database, tmp_path):
    agent = Agent(University(), database, ScriptedProvider([]), tmp_path / "trace")
    agent.deadline = float("inf")
    agent.calls = 0
    agent.reserved_tokens = PROFILE.run_tokens
    with pytest.raises(Failure):
        agent._call("plan", {"question": QUESTION, "scope": {}, "descriptor": {}}, PlanProposal)
    assert agent.provider.calls == 0


@pytest.mark.parametrize("schema", [PlanProposal, SQLProposal])
def test_installed_sdk_strict_schema_serialization(schema):
    # Installed SDK conversion, not a network/client call or dependency update.
    from openai.lib._parsing._responses import type_to_text_format_param

    wire = type_to_text_format_param(schema)
    assert wire["type"] == "json_schema" and wire["strict"] is True

    def closed(node):
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert node["additionalProperties"] is False
                assert set(node["required"]) == set(node["properties"])
            for value in node.values():
                closed(value)
        elif isinstance(node, list):
            for value in node:
                closed(value)

    closed(wire["schema"])


def test_unknown_operation_and_wrong_schema_zero_dispatch(tmp_path, monkeypatch):
    from test_provider_worker import configure

    configure(monkeypatch)
    provider = OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "spend.json")
    with patch("universitydb.llm.subprocess.Popen") as process:
        for operation, schema in [
            ("repair", SQLProposal),
            ("oops", PlanProposal),
            ("plan", SQLProposal),
        ]:
            with pytest.raises(Failure):
                provider.call(operation, {}, schema)
    process.assert_not_called()
    assert not (tmp_path / "spend.json").exists()


@pytest.mark.parametrize("bad", ["model", "tier", "usage", "incomplete"])
def test_bad_worker_response_retains_reservation(tmp_path, monkeypatch, bad):
    import subprocess
    import sys

    from test_provider_worker import configure

    configure(monkeypatch)
    usage = {
        "returned_model": PROFILE.model,
        "returned_service_tier": "default",
        "input_tokens": 100,
        "output_tokens": 50,
        "total_tokens": 150,
    }
    if bad == "model":
        usage["returned_model"] = "other"
    elif bad == "tier":
        usage["returned_service_tier"] = "priority"
    elif bad == "usage":
        del usage["input_tokens"]
    data = {"output": outputs()[0], "usage": usage}
    if bad == "incomplete":
        data = {"error": "PROVIDER_INCOMPLETE", "message": "Incomplete test", "usage": usage}
    response = json.dumps(data)
    original = subprocess.Popen

    def scripted(command, **kwargs):
        return original(
            [sys.executable, "-c", f"import sys;sys.stdin.read();print({response!r})"], **kwargs
        )

    path = tmp_path / "spend.json"
    with patch("universitydb.llm.subprocess.Popen", scripted), pytest.raises(Failure) as failure:
        OpenAIProvider(Path("src/universitydb/prompts"), path).call("plan", {}, PlanProposal)
    assert failure.value.details["usage_status"] == ("unknown" if bad == "usage" else "known")
    assert failure.value.details["real_provider_called"] is True
    assert "returned_model" in failure.value.details["usage"]
    record = json.loads(path.read_text())
    assert record["calls"] == 1 and record["effective_usd"] == "0.044768"
    assert (record["attempts"][0]["observed_usd"] is None) == (bad == "usage")


@pytest.mark.parametrize("kind", ["incomplete", "refusal", "missing_parsed"])
def test_worker_failed_response_preserves_known_usage(kind):
    response = SimpleNamespace(
        status="incomplete" if kind == "incomplete" else "completed",
        output=[SimpleNamespace(content=[SimpleNamespace(type="refusal")])]
        if kind == "refusal"
        else [],
        output_text="",
        model=PROFILE.model,
        service_tier="default",
        id="offline-failure",
        usage=SimpleNamespace(input_tokens=100, output_tokens=32768, total_tokens=32868),
    )
    with patch("universitydb.llm_worker.OpenAI") as sdk:
        sdk.return_value.__enter__.return_value.responses.create.return_value = response
        result = request(
            {
                "operation": "plan",
                "logical_operation": "plan",
                "model": PROFILE.model,
                "timeout": 10,
                "prompt": "test",
                "input": "{}",
            }
        )
    assert "error" in result and result["usage"]["output_tokens"] == 32768
    assert result["usage"]["returned_model"] == PROFILE.model
    assert result["usage"]["returned_service_tier"] == "default"


def test_actual_db_watchdog_kills_and_reaps(database):
    import os
    import subprocess

    from universitydb import db

    original = subprocess.Popen
    children = []

    def observed(*args, **kwargs):
        child = original(*args, **kwargs)
        children.append(child.pid)
        return child

    sql = "SELECT count(*) FROM " + ",".join(f"Enrollments e{i}" for i in range(12))
    with patch("universitydb.db.subprocess.Popen", observed), pytest.raises(Failure):
        db.execute(
            database, sql, {}, University.tables, University.functions, timeout=20, watchdog=0.2
        )
    assert len(children) == 1
    with pytest.raises(ProcessLookupError):
        os.kill(children[0], 0)


@pytest.mark.parametrize(
    "status,text,code,has_usage",
    [
        ("incomplete", '{"version":', "PROVIDER_INCOMPLETE", True),
        ("completed", "{}", "PROVIDER_INVALID_OUTPUT", True),
        ("failed", json.dumps(outputs()[0]), "PROVIDER_INVALID_OUTPUT", True),
        ("cancelled", json.dumps(outputs()[0]), "PROVIDER_INVALID_OUTPUT", True),
        ("in_progress", json.dumps(outputs()[0]), "PROVIDER_INVALID_OUTPUT", True),
        ("completed", json.dumps(outputs()[0]), "BUDGET_EXCEEDED", False),
    ],
)
def test_real_sdk_failure_metadata_reconciled_before_parsing(
    database, tmp_path, monkeypatch, status, text, code, has_usage
):
    import httpx2
    from openai import OpenAI
    from test_provider_worker import configure

    configure(monkeypatch)
    wire = []

    def handler(req):
        wire.append(json.loads(req.content))
        return httpx2.Response(
            200,
            json={
                "id": "offline-known-usage",
                "object": "response",
                "created_at": 1,
                "status": status,
                "model": PROFILE.model,
                "service_tier": "default",
                "output": [
                    {
                        "id": "offline-msg",
                        "type": "message",
                        "role": "assistant",
                        "status": "incomplete" if status == "incomplete" else "completed",
                        "content": [{"type": "output_text", "text": text, "annotations": []}],
                    }
                ],
                "usage": {"input_tokens": 100, "output_tokens": 32768, "total_tokens": 32868}
                if has_usage
                else None,
            },
        )

    def sdk(**kwargs):
        return OpenAI(
            api_key="offline-not-real",
            http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
            **kwargs,
        )

    process = MagicMock()
    process.__enter__.return_value = process
    process.returncode = 0
    process.communicate.side_effect = lambda encoded, **_: (
        json.dumps(request(json.loads(encoded))),
        None,
    )
    path = tmp_path / "spend.json"
    with (
        patch("universitydb.llm_worker.OpenAI", sdk),
        patch("universitydb.llm.subprocess.Popen", return_value=process),
    ):
        result = Agent(
            University(),
            database,
            OpenAIProvider(Path("src/universitydb/prompts"), path),
            tmp_path / "trace",
        ).run(QUESTION)
    assert result["error"]["code"] == code
    ledger = json.loads(path.read_text())
    assert ledger["calls"] == 1 and ledger["output_tokens"] == (32768 if has_usage else 0)
    assert (ledger["attempts"][0]["observed_usd"] is not None) == has_usage
    error = next(
        e["payload"] for e in result["events"] if e["kind"] == "error" and "usage" in e["payload"]
    )
    assert error["usage_status"] == ("known" if has_usage else "unknown")
    assert error["real_provider_called"] is True
    assert error["usage"]["returned_model"] == PROFILE.model
    assert error["usage"]["returned_service_tier"] == "default"
    assert wire[0]["reasoning"] == {"effort": "high"}
    assert wire[0]["service_tier"] == "default" and wire[0]["store"] is False
    assert wire[0]["text"]["format"]["strict"] is True
