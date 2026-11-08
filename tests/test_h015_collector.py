"""Independent synthetic/dev collector checks. No candidate questions or network."""

import hashlib
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest
from conftest import QUESTION, outputs

SPEC = importlib.util.spec_from_file_location(
    "h015_collector", Path(__file__).resolve().parents[1] / "tools/eval/collector.py"
)
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def inputs():
    body = {
        "domain": "university",
        "schema": "resources/schema.sql",
        "seed": "resources/seed.sql",
        "mutations": [],
    }
    fixture = {
        **body,
        "sha256": hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }
    runs = [
        {
            "run_id": name,
            "case_id": name.split("-r")[0],
            "repeat": int(name[-1]),
            "domain": "university",
            "fixture": "synthetic",
            "question": QUESTION,
            "selections": [],
        }
        for name in collector.ORDER
    ]
    files = {p: collector.digest(ROOT / p) for p in (body["schema"], body["seed"])}
    return runs, {"synthetic": fixture}, files


def reg(tmp_path):
    return {
        "campaign_id": "synthetic_only",
        "policy_sha256": "synthetic",
        "ledger_baseline_sha256": "synthetic",
        "ledger_path": str(tmp_path / "never-created-ledger.json"),
    }


def healthy(*args):
    return {
        "calls": 14,
        "campaign_calls": 0,
        "policy_sha256": "synthetic",
        "uncertain_attempts": 0,
        "stop": None,
    }


class FakeAgent:
    sql_attempts = 0

    def __init__(self, domain, database, directory, ledger):
        self.database = database
        self.directory = directory

    def run(self, question):
        assert question == QUESTION
        events = [{"kind": "run_end", "payload": {"status": "error"}}]
        collector.persist(self.directory / "traces/run.jsonl", events[0])
        return {
            "status": "error",
            "answer": None,
            "error": {"code": "UNSAFE_SQL"},
            "events": events,
            "execution_profile": "live",
        }


def test_exact_closed_export_and_fixture(inputs):
    runs, fixtures, files = inputs
    collector.validate_inputs(runs, fixtures, files, ROOT)
    runs[0]["oracle"] = {"answer": "must never reach model"}
    with pytest.raises(ValueError, match="allowlisted"):
        collector.validate_inputs(runs, fixtures, files, ROOT)


@pytest.mark.parametrize("fault", ["order", "repeat", "fixture", "selection", "question"])
def test_bad_conversation_identity_no_dispatch(inputs, fault):
    runs, fixtures, files = inputs
    if fault == "order":
        runs.reverse()
    elif fault == "repeat":
        runs[0]["repeat"] = True
    elif fault == "fixture":
        runs[0]["fixture"] = "absent"
    elif fault == "selection":
        runs[0]["selections"] = [True]
    else:
        runs[0]["question"] = ""
    with pytest.raises(ValueError):
        collector.validate_inputs(runs, fixtures, files, ROOT)


def test_setup_fresh_delete_census_and_no_overwrite(tmp_path, inputs):
    _, fixtures, _ = inputs
    database = tmp_path / "fixture.sqlite3"
    before = collector.setup_database(database, fixtures["synthetic"], ROOT)
    assert before == collector.census(database)
    assert before["rows"]["Students"] > 0
    with pytest.raises(ValueError, match="existing"):
        collector.setup_database(database, fixtures["synthetic"], ROOT)
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
    with pytest.raises(ValueError, match="journal"):
        collector.census(database)


def test_all_ordinary_failures_remain_48_no_unsafe_execution(tmp_path, inputs):
    runs, fixtures, _ = inputs
    output = tmp_path / "campaign"
    result = collector.collect(
        reg(tmp_path), runs, fixtures, output, factory=FakeAgent, ledger_check=healthy
    )
    assert result["complete"] and result["calls"] == 0
    assert len(result["statuses"]) == 48
    assert {r["status"] for r in result["statuses"]} == {"completed"}
    assert all((output / r["run_id"] / "started.json").exists() for r in runs)
    assert not Path(reg(tmp_path)["ledger_path"]).exists()
    with pytest.raises(FileExistsError):
        collector.collect(
            reg(tmp_path), runs, fixtures, output, factory=FakeAgent, ledger_check=healthy
        )


def test_critical_database_write_stops_keeps_denominator(tmp_path, inputs):
    runs, fixtures, _ = inputs

    class Mutating(FakeAgent):
        def run(self, question):
            with sqlite3.connect(self.database) as connection:
                connection.execute("DELETE FROM Enrollments")
            return super().run(question)

    output = tmp_path / "campaign"
    result = collector.collect(
        reg(tmp_path), runs, fixtures, output, factory=Mutating, ledger_check=healthy
    )
    assert not result["complete"]
    assert result["stop"]["reason"] == ["database_changed"]
    assert result["statuses"][0]["status"] == "completed"
    assert len([s for s in result["statuses"] if s["status"] == "not-run"]) == 47


def test_started_before_provider_interruption_never_auto_retried(tmp_path, inputs):
    runs, fixtures, _ = inputs
    output = tmp_path / "campaign"

    def interrupted(domain, database, directory, ledger):
        assert (directory / "started.json").exists()
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        collector.collect(
            reg(tmp_path), runs, fixtures, output, factory=interrupted, ledger_check=healthy
        )
    assert (output / runs[0]["run_id"] / "started.json").exists()
    assert not (output / runs[0]["run_id"] / "completed.json").exists()
    assert len(json.loads((output / "planned.json").read_text())) == 48
    with pytest.raises(FileExistsError):
        collector.collect(
            reg(tmp_path), runs, fixtures, output, factory=interrupted, ledger_check=healthy
        )


def test_pre_dispatch_drift_stops_without_started_or_action(tmp_path, inputs):
    runs, fixtures, _ = inputs

    def drift():
        raise ValueError("changed frozen source")

    result = collector.collect(
        reg(tmp_path),
        runs,
        fixtures,
        tmp_path / "campaign",
        factory=lambda *a: pytest.fail("must not dispatch"),
        ledger_check=healthy,
        revalidate=drift,
    )
    assert result["stop"]
    assert {r["status"] for r in result["statuses"]} == {"not-run"}


def test_sanitized_exception_unknown_accounting_aborts(tmp_path, inputs):
    runs, fixtures, _ = inputs

    def unknown(*args):
        raise ValueError("secret-value-must-not-be-recorded")

    output = tmp_path / "campaign"
    result = collector.collect(
        reg(tmp_path), runs, fixtures, output, factory=FakeAgent, ledger_check=unknown
    )
    assert result["stop"]["exception_type"] == "ValueError"
    assert "secret-value" not in (output / "summary.json").read_text()
    assert {r["status"] for r in result["statuses"]} == {"not-run"}


def test_provider_evidence_missing_hash_escape_and_complete(tmp_path):
    request, response = tmp_path / "request.json", tmp_path / "response.json"
    collector.persist(request, {"input": "synthetic"})
    collector.persist(response, {"output": "synthetic"})
    usage = {}
    for kind, path in (("request", request), ("response", response)):
        usage[f"evidence_{kind}_path"] = str(path)
        usage[f"evidence_{kind}_sha256"] = collector.digest(path)
    events = [{"payload": {"usage": usage}}]
    assert len(collector.verify_provider_artifacts(tmp_path, events, 1)) == 2
    with pytest.raises(ValueError, match="Incomplete"):
        collector.verify_provider_artifacts(tmp_path, [], 1)
    usage["evidence_request_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash drift"):
        collector.verify_provider_artifacts(tmp_path, events, 1)
    usage["evidence_request_sha256"] = collector.digest(request)
    with pytest.raises(ValueError, match="escaped"):
        collector.verify_provider_artifacts(tmp_path / "narrow", events, 1)


def test_no_oracle_file_access(tmp_path):
    oracle = tmp_path / "oracle.json"
    oracle.write_text("private")
    with pytest.raises(ValueError, match="Oracle"):
        collector.source_path(tmp_path, "oracle.json")
    with pytest.raises(ValueError, match="outside"):
        collector.source_path(tmp_path, "../elsewhere")


def test_real_compiled_graph_through_collector_synthetic_only(tmp_path, inputs):
    from universitydb.agent import Agent
    from universitydb.domain import University
    from universitydb.llm import ScriptedProvider

    runs, fixtures, _ = inputs

    def factory(domain, database, directory, ledger):
        provider = ScriptedProvider(outputs())
        # Test-only synthetic seam: CLI never selects this factory or ScriptedProvider.
        provider.profile = "live"
        return Agent(University(), database, provider, directory / "traces")

    output = tmp_path / "campaign"
    result = collector.collect(
        reg(tmp_path), runs[:1], fixtures, output, factory=factory, ledger_check=healthy
    )
    assert result["statuses"][0]["status"] == "completed"
    exchange = json.loads((output / runs[0]["run_id"] / "exchanges.json").read_text())[0]
    assert exchange["status"] == "ok"
    assert exchange["answer"]["rows"] == [["80.00", 2, 2]]
    assert not result["complete"]  # synthetic subset can never claim full eval


@pytest.mark.parametrize("terminal", ["refusal", "success"])
def test_normal_provider_accounted_terminal_then_next_untouched(
    tmp_path, inputs, monkeypatch, terminal
):
    import subprocess
    from unittest.mock import patch

    from test_h015_budget import legacy, migrate
    from test_provider_worker import configure

    from universitydb.llm import H015_POLICY_SHA256, load_h015

    configure(monkeypatch)
    ledger, raw = legacy(tmp_path)
    migrate(ledger, raw, tmp_path / "backup")
    monkeypatch.setattr("universitydb.llm.canonical_budget_path", lambda: ledger)
    for key, value in {
        "UNIVERSITYDB_BUDGET_POLICY": "h015-practical-v1",
        "UNIVERSITYDB_CAP_USD": "120",
        "UNIVERSITYDB_INPUT_USD_PER_MILLION": "5.50",
        "UNIVERSITYDB_OUTPUT_USD_PER_MILLION": "11",
    }.items():
        monkeypatch.setenv(key, value)
    response = {
        "error": "PROVIDER_REFUSAL",
        "message": "terminal",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "returned_model": "gpt-6.1-sol",
            "returned_service_tier": "default",
        },
        "raw_response": {"id": "synthetic", "output": [{"content": [{"type": "refusal"}]}]},
    }

    scripted = iter(outputs() * 2)

    class Worker:
        returncode = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def communicate(self, *args, **kwargs):
            value = response
            if terminal == "success":
                value = {
                    "usage": response["usage"],
                    "output": next(scripted),
                    "raw_response": {"id": "synthetic", "output": []},
                }
            return json.dumps(value), None

    runs, fixtures, _ = inputs
    registration = {
        **reg(tmp_path),
        "ledger_path": str(ledger),
        "policy_sha256": H015_POLICY_SHA256,
        "ledger_baseline_sha256": hashlib.sha256(raw).hexdigest(),
    }
    output = tmp_path / "campaign"
    original_popen = subprocess.Popen

    def worker_only(command, **kwargs):
        if "universitydb.llm_worker" in command:
            return Worker()
        return original_popen(command, **kwargs)

    with patch("universitydb.llm.subprocess.Popen", side_effect=worker_only):
        summary = collector.collect(registration, runs[:2], fixtures, output)
    assert not summary["stop"], summary
    assert summary["calls"] == (2 if terminal == "refusal" else 4)
    assert [s["status"] for s in summary["statuses"]] == ["completed", "completed"]
    assert load_h015(ledger).inspect()["campaign_calls"] == summary["calls"]
    for run in runs[:2]:
        directory = output / run["run_id"]
        completed = json.loads((directory / "completed.json").read_text())
        assert len(completed["provider_artifacts"]) == (2 if terminal == "refusal" else 4)
        assert completed["critical"] == []
        result = json.loads((directory / "exchanges.json").read_text())[-1]
        if terminal == "refusal":
            assert result["error"]["code"] == "PROVIDER_REFUSAL"
        else:
            assert result["status"] == "ok"
            assert result["answer"]["rows"] == [["80.00", 2, 2]]


def test_wrong_frozen_monetary_anchor_rejected(tmp_path, monkeypatch):
    from test_h015_budget import legacy, migrate

    from universitydb.llm import H015_POLICY_SHA256

    path, raw = legacy(tmp_path)
    migrate(path, raw, tmp_path / "backup")
    monkeypatch.setattr("universitydb.llm.canonical_budget_path", lambda: path)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="baseline drift"):
        collector.check_ledger(path, H015_POLICY_SHA256, "0" * 64)
    assert path.read_bytes() == before
    assert (
        collector.check_ledger(path, H015_POLICY_SHA256, hashlib.sha256(raw).hexdigest())["calls"]
        == 1
    )
    with pytest.raises(ValueError, match="Noncanonical"):
        collector.check_ledger(
            tmp_path / "different.json", H015_POLICY_SHA256, hashlib.sha256(raw).hexdigest()
        )


def test_registration_sha_source_and_schema_drift(tmp_path, inputs, monkeypatch):
    runs, fixtures, source_files = inputs
    paths = [
        *source_files,
        "tools/eval/collector.py",
        "exports/conversations.json",
        "exports/fixtures.json",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if name in source_files:
            path.write_bytes((ROOT / name).read_bytes())
        elif name.endswith("conversations.json"):
            path.write_text(json.dumps(runs))
        elif name.endswith("fixtures.json"):
            path.write_text(json.dumps(fixtures))
        else:
            path.write_text("# synthetic source")
    registration = {
        **reg(tmp_path),
        "version": collector.VERSION,
        "candidate_sha": "a" * 40,
        "files": {n: collector.digest(tmp_path / n) for n in paths},
        "conversations_path": paths[-2],
        "fixtures_path": paths[-1],
    }

    def git(args, **kwargs):
        return "a" * 40 if "rev-parse" in args else "tools/eval/collector.py\n"

    monkeypatch.setattr(collector.subprocess, "check_output", git)
    collector.validate_registration(registration, tmp_path)
    registration["candidate_sha"] = "b" * 40
    with pytest.raises(ValueError, match="SHA drift"):
        collector.validate_registration(registration, tmp_path)
    registration["candidate_sha"] = "a" * 40
    (tmp_path / "resources/schema.sql").write_text("changed")
    with pytest.raises(ValueError, match="source drift"):
        collector.validate_registration(registration, tmp_path)
    registration["extra_oracle"] = "no"
    with pytest.raises(ValueError, match="fields"):
        collector.validate_registration(registration, tmp_path)


@pytest.mark.parametrize("interrupt", [False, True])
def test_main_refuses_second_campaign_different_output_after_durable_marker(
    tmp_path, monkeypatch, interrupt
):
    import os
    import sys

    runtime = tmp_path / "runtime"
    runtime.mkdir()
    registration_path = tmp_path / "registration.json"
    registration_path.write_text(json.dumps(reg(tmp_path)))
    monkeypatch.setattr(collector, "ROOT", tmp_path)
    monkeypatch.setattr(collector, "validate_registration", lambda value: ([], {}))
    ledger_checks = []
    monkeypatch.setattr(collector, "check_ledger", lambda *args: ledger_checks.append(args))
    dispatches = []
    synced = []
    original_fsync = os.fsync

    def fsync(fd):
        synced.append(Path(os.readlink(f"/proc/self/fd/{fd}")).resolve())
        original_fsync(fd)

    monkeypatch.setattr(collector.os, "fsync", fsync)

    def dispatch(*args, **kwargs):
        dispatches.append(args)
        assert (runtime / "h015-collector.lock").read_text() == "synthetic_only\n"
        if interrupt:
            raise KeyboardInterrupt()
        return {"complete": False, "synthetic": True}

    monkeypatch.setattr(collector, "collect", dispatch)

    def invoke(output):
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "collector",
                "--registration",
                str(registration_path),
                "--output",
                str(tmp_path / output),
            ],
        )
        collector.main()

    if interrupt:
        with pytest.raises(KeyboardInterrupt):
            invoke("first")
    else:
        invoke("first")
    marker = (runtime / "h015-collector.lock").read_bytes()
    with pytest.raises(ValueError, match="Campaign already started"):
        invoke("different-output")
    assert len(dispatches) == len(ledger_checks) == 1
    assert (runtime / "h015-collector.lock").read_bytes() == marker
    assert runtime.resolve() in synced
    assert not (tmp_path / "different-output").exists()


def test_campaign_and_case_directory_links_synced_before_factory(tmp_path, inputs, monkeypatch):
    import os

    runs, fixtures, _ = inputs
    output = tmp_path / "campaign"
    synced_directories = []
    original_fsync = os.fsync

    def fsync(fd):
        path = Path(os.readlink(f"/proc/self/fd/{fd}")).resolve()
        if path.is_dir():
            synced_directories.append((path, sorted(p.name for p in path.iterdir())))
        original_fsync(fd)

    monkeypatch.setattr(collector.os, "fsync", fsync)

    def factory(domain, database, directory, ledger):
        assert (tmp_path, ["campaign"]) in synced_directories
        assert any(
            path == output and runs[0]["run_id"] in children
            for path, children in synced_directories
        )
        assert (directory / "started.json").exists()
        return FakeAgent(domain, database, directory, ledger)

    summary = collector.collect(
        reg(tmp_path), runs[:1], fixtures, output, factory=factory, ledger_check=healthy
    )
    assert not summary["stop"]
