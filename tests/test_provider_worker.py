import json
import os
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from conftest import QUESTION, outputs

from universitydb.agent import Agent
from universitydb.contracts import Failure, PlanProposal
from universitydb.domain import University
from universitydb.llm import OpenAIProvider


def configure(monkeypatch):
    for key, value in {
        "OPENAI_API_KEY": "offline-test-not-a-real-key",
        "UNIVERSITYDB_MODEL": "gpt-6.1-sol",
        "UNIVERSITYDB_LIVE_APPROVED": "yes",
        "UNIVERSITYDB_BUDGET_POLICY": "practical-v1",
        "UNIVERSITYDB_RATES_CONFIRMED": "yes",
        "UNIVERSITYDB_CAP_USD": "10",
        "UNIVERSITYDB_INPUT_USD_PER_MILLION": "1",
        "UNIVERSITYDB_OUTPUT_USD_PER_MILLION": "1",
    }.items():
        monkeypatch.setenv(key, value)


def test_stalled_sdk_process_killed_reaped_cost_retained(tmp_path, monkeypatch):
    configure(monkeypatch)
    original = subprocess.Popen
    children = []

    def stalled(command, **kwargs):
        child = original([sys.executable, "-c", "import time;time.sleep(30)"], **kwargs)
        children.append(child.pid)
        return child

    provider = OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "spending.json")
    started = time.monotonic()
    with patch("universitydb.llm.subprocess.Popen", stalled), pytest.raises(Failure) as error:
        provider.call("plan", {}, PlanProposal, timeout=0.15)
    assert error.value.code == "PROVIDER_TRANSIENT"
    assert error.value.details["usage_status"] == "unknown"
    assert error.value.details["real_provider_called"] is None
    assert time.monotonic() - started < 1
    with pytest.raises(ProcessLookupError):
        os.kill(children[0], 0)
    ledger = json.loads((tmp_path / "spending.json").read_text())
    assert ledger["calls"] == 1 and ledger["reserved_usd"] == "0.044768"


def test_whole_graph_deadline_bounds_stalled_provider(database, tmp_path, monkeypatch):
    configure(monkeypatch)
    original = subprocess.Popen
    children = []

    def stalled_sdk(command, **kwargs):
        # SQL worker unchanged; only the SDK process stalls. No network is performed.
        assert command[-1] == "universitydb.llm_worker"
        child = original([sys.executable, "-c", "import time;time.sleep(30)"], **kwargs)
        children.append(child.pid)
        return child

    provider = OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "spend.json")
    agent = Agent(University(), database, provider, tmp_path / "traces")
    original_check = agent._check_deadline

    def shortened_deadline():
        agent.deadline = min(agent.deadline, start + 0.2)
        original_check()

    monkeypatch.setattr(agent, "_check_deadline", shortened_deadline)
    start = time.monotonic()
    with patch("universitydb.llm.subprocess.Popen", stalled_sdk):
        result = agent.run(QUESTION)
    assert time.monotonic() - start < 1.5
    assert result["answer"] is None and result["status"] == "error"
    assert result["error"]["code"] == "BUDGET_EXCEEDED"
    for pid in children:
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)


def test_offline_sdk_worker_response_parse_and_usage(tmp_path, monkeypatch):
    configure(monkeypatch)
    original = subprocess.Popen
    response = {
        "output": outputs()[0],
        "usage": {
            "returned_model": "gpt-6.1-sol",
            "returned_service_tier": "default",
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "provider_request_id": "offline-id",
        },
    }

    def scripted(command, **kwargs):
        return original(
            [
                sys.executable,
                "-c",
                f"import sys;sys.stdin.read();print({json.dumps(json.dumps(response))})",
            ],
            **kwargs,
        )

    provider = OpenAIProvider(Path("src/universitydb/prompts"), tmp_path / "spend.json")
    with patch("universitydb.llm.subprocess.Popen", scripted):
        parsed, usage = provider.call("plan", {}, PlanProposal)
    assert parsed == PlanProposal.model_validate(outputs()[0])
    assert usage["input_tokens"] == 100
    ledger = json.loads((tmp_path / "spend.json").read_text())
    assert ledger["observed_usd"] == "0.00015"
