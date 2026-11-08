"""H015 sequential evidence collector. Oracle/scoring is a separate process.

The CLI has no injected provider, test mode, resume, retry, or package-file input.
"""

import argparse
import fcntl
import hashlib
import json
import os
import sqlite3
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "h015-collector-v1"
ORDER = [
    f"{letter}{number:02}-r{repeat}"
    for repeat in (1, 2)
    for letter in "AJDCEL"
    for number in range(1, 5)
]
RUN_FIELDS = {"run_id", "case_id", "repeat", "domain", "fixture", "question", "selections"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()


def persist(path, value):
    """Create immutable evidence; never replace an earlier observation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def source_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("Source path outside repository or absent")
    # Collector must never open the oracle/package, even as a hash check.
    if path.suffix != ".sql" and ("oracle" in relative or "heldout" in relative):
        raise ValueError("Oracle access is forbidden in collector")
    return path


def validate_registration(reg, root=ROOT):
    fields = {
        "version",
        "campaign_id",
        "candidate_sha",
        "files",
        "conversations_path",
        "fixtures_path",
        "ledger_path",
        "policy_sha256",
        "ledger_baseline_sha256",
    }
    if set(reg) != fields or reg["version"] != VERSION:
        raise ValueError("Invalid registration fields/version")
    if not isinstance(reg["campaign_id"], str) or not reg["campaign_id"].isidentifier():
        raise ValueError("Invalid campaign identity")
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if sha != reg["candidate_sha"]:
        raise ValueError("Frozen candidate SHA drift")
    files = reg["files"]
    required = {reg["conversations_path"], reg["fixtures_path"], "tools/eval/collector.py"}
    # All executable product/collector/prompt/resources must be pinned, not just exports.
    tracked = subprocess.check_output(
        ["git", "ls-files", "src", "resources", "tools/eval"], cwd=root, text=True
    ).splitlines()
    required.update(p for p in tracked if not p.endswith(".pyc"))
    if not isinstance(files, dict) or not required <= files.keys():
        raise ValueError("Incomplete source freeze")
    for name, expected in files.items():
        if digest(source_path(root, name)) != expected:
            raise ValueError(f"Frozen source drift: {name}")
    runs = json.loads(source_path(root, reg["conversations_path"]).read_text())
    fixtures = json.loads(source_path(root, reg["fixtures_path"]).read_text())
    validate_inputs(runs, fixtures, files, root)
    return runs, fixtures


def validate_inputs(runs, fixtures, files, root):
    if not isinstance(runs, list) or [r.get("run_id") for r in runs] != ORDER:
        raise ValueError("Exactly frozen repeat-major 48 runs required")
    if not isinstance(fixtures, dict) or not fixtures:
        raise ValueError("Missing trusted setup")
    for name, fixture in fixtures.items():
        if set(fixture) != {"domain", "schema", "seed", "mutations", "sha256"}:
            raise ValueError("Invalid fixture fields")
        body = {k: v for k, v in fixture.items() if k != "sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(canonical).hexdigest() != fixture["sha256"]:
            raise ValueError("Fixture descriptor drift")
        if fixture["domain"] not in ("university", "library") or not isinstance(name, str):
            raise ValueError("Invalid fixture domain")
        if not isinstance(fixture["mutations"], list) or any(
            not isinstance(s, str) for s in fixture["mutations"]
        ):
            raise ValueError("Invalid trusted setup SQL")
        for key in ("schema", "seed"):
            path = source_path(root, fixture[key])
            if fixture[key] not in files or digest(path) != files[fixture[key]]:
                raise ValueError("Unpinned fixture source")
    for run in runs:
        if set(run) != RUN_FIELDS:
            raise ValueError("Conversation export is not allowlisted")
        case, repeat = run["run_id"].split("-r")
        if run["case_id"] != case or type(run["repeat"]) is not int or run["repeat"] != int(repeat):
            raise ValueError("Case identity mismatch")
        if run["fixture"] not in fixtures or fixtures[run["fixture"]]["domain"] != run["domain"]:
            raise ValueError("Wrong fixture/domain")
        if not isinstance(run["question"], str) or not run["question"].strip():
            raise ValueError("Empty question")
        if (
            not isinstance(run["selections"], list)
            or len(run["selections"]) > 2
            or any(type(v) not in (str, int) for v in run["selections"])
        ):
            raise ValueError("Invalid protocol selections")


def setup_database(path, fixture, root):
    if path.exists():
        raise ValueError("Refusing existing fixture database")
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA journal_mode=DELETE")
        for key in ("schema", "seed"):
            connection.executescript(source_path(root, fixture[key]).read_text())
        for statement in fixture["mutations"]:
            connection.executescript(statement)
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Fixture foreign key failure")
    return census(path)


def census(path):
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as connection:
        if connection.execute("PRAGMA journal_mode").fetchone() != ("delete",):
            raise ValueError("Unsupported database journal")
        if connection.execute("PRAGMA integrity_check").fetchone() != ("ok",):
            raise ValueError("Database integrity failure")
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        counts = {}
        for (name,) in tables:
            escaped = name.replace('"', '""')
            counts[name] = connection.execute(f'SELECT count(*) FROM "{escaped}"').fetchone()[0]
    return {"sha256": digest(path), "rows": counts}


def live_factory(domain, database, directory, ledger):
    from universitydb.agent import Agent
    from universitydb.domain import University
    from universitydb.library import Library
    from universitydb.llm import OpenAIProvider

    provider = OpenAIProvider(
        ROOT / "src/universitydb/prompts", ledger, evidence_dir=directory / "provider"
    )
    if type(provider) is not OpenAIProvider or provider.profile != "live":
        raise ValueError("Injected/test provider forbidden")
    return Agent(
        University() if domain == "university" else Library(),
        database,
        provider,
        directory / "traces",
    )


def verify_provider_artifacts(directory, events, monetary_delta):
    """Each dispatched reservation needs full request/response evidence."""
    artifacts = {}
    requests = set()
    responses = set()
    for event in events:
        usage = {**event["payload"], **event["payload"].get("usage", {})}
        for kind, seen in (("request", requests), ("response", responses)):
            name = usage.get(f"evidence_{kind}_path")
            expected = usage.get(f"evidence_{kind}_sha256")
            if name is None:
                continue
            path = Path(name).resolve()
            if not path.is_relative_to(directory.resolve()) or digest(path) != expected:
                raise ValueError("Provider evidence absent, escaped run, or hash drift")
            json.loads(path.read_text())
            seen.add(str(path))
            artifacts[str(path.relative_to(directory.resolve()))] = expected
    if len(requests) != monetary_delta or len(responses) != monetary_delta:
        raise ValueError("Incomplete full provider wire evidence")
    return artifacts


def check_ledger(ledger, policy_hash, baseline_hash):
    from universitydb.llm import canonical_budget_path, load_h015

    if ledger.resolve() != canonical_budget_path().resolve():
        raise ValueError("Noncanonical monetary authority")
    spending = load_h015(ledger)
    if spending.snapshot()["authorizations"][0]["source_sha256"] != baseline_hash:
        raise ValueError("Frozen historical monetary baseline drift")
    receipt = spending.inspect()
    if receipt["policy_sha256"] != policy_hash:
        raise ValueError("Frozen monetary policy drift")
    if receipt.get("stop") or receipt.get("uncertain_attempts"):
        raise ValueError("Stopped or unknown spending")
    return receipt


def collect(
    reg,
    runs,
    fixtures,
    output,
    *,
    root=ROOT,
    factory=live_factory,
    ledger_check=check_ledger,
    revalidate=None,
):
    """Private test seams; CLI never accepts factory/ledger injection."""
    output.mkdir(parents=True, exist_ok=False)
    parent = os.open(output.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)
    ledger = Path(reg["ledger_path"])
    persist(output / "registration.json", reg)
    persist(output / "planned.json", [{"run_id": r["run_id"], "status": "not-run"} for r in runs])
    calls = 0
    records = []
    stop = None
    for run in runs:
        directory = output / run["run_id"]
        directory.mkdir()
        parent = os.open(output, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(parent)
        finally:
            os.close(parent)
        try:
            if revalidate:
                revalidate()
            before_ledger = ledger_check(
                ledger, reg["policy_sha256"], reg["ledger_baseline_sha256"]
            )
            if calls + 5 > 240:
                raise ValueError("Campaign call ceiling")
            persist(
                directory / "started.json",
                {"run_id": run["run_id"], "status": "started", "ledger": before_ledger},
            )
            database = directory / "fixture.sqlite3"
            before = setup_database(database, fixtures[run["fixture"]], root)
            persist(directory / "database-before.json", before)
            agent = factory(run["domain"], database, directory, ledger)
            exchanges = [agent.run(run["question"])]
            for choice in run["selections"]:
                result = exchanges[-1]
                if result["status"] != "clarification":
                    break
                exchanges.append(
                    agent.resume(result["clarification"], choice, request_id=str(uuid.uuid4()))
                )
            result = exchanges[-1]
            persist(directory / "exchanges.json", exchanges)
            if hasattr(agent, "compiled"):
                context = agent._runs.get(result["run_id"])
                if context is None:
                    raise ValueError("Original graph context missing")
                snapshot = agent.compiled.get_state(context["config"])
                persist(directory / "graph-state.json", snapshot.values)
            after = census(database)
            persist(directory / "database-after.json", after)
            events = result["events"]
            generated = sum(
                e["kind"] == "llm_attempt"
                and e["payload"].get("phase") == "application_attempt_before_dispatch"
                for e in events
            )
            sql = agent.sql_attempts
            calls += generated
            trace_files = sorted((directory / "traces").glob("*.jsonl"))
            trace_hashes = {str(p.relative_to(output)): digest(p) for p in trace_files}
            after_ledger = ledger_check(ledger, reg["policy_sha256"], reg["ledger_baseline_sha256"])
            if len(trace_files) == 1:
                original = [json.loads(line) for line in trace_files[0].read_text().splitlines()]
                if original != events:
                    raise ValueError("Original trace/result mismatch")
            monetary_delta = after_ledger["calls"] - before_ledger["calls"]
            if not 0 <= monetary_delta <= generated:
                raise ValueError("Concurrent or inconsistent monetary attempts")
            if after_ledger["campaign_calls"] > 240:
                raise ValueError("Canonical campaign call ceiling")
            provider_artifacts = verify_provider_artifacts(directory, events, monetary_delta)
            critical = []
            if before != after:
                critical.append("database_changed")
            if generated > 5 or sql > 4 or calls > 240:
                critical.append("generation_or_sql_limit")
            if (
                len(trace_files) != 1
                or not events
                or (events[-1]["kind"] != "run_end" and result["status"] != "clarification")
            ):
                critical.append("incomplete_terminal_trace")
            if result.get("execution_profile") != "live":
                critical.append("nonlive_profile")
            if any(e["payload"].get("accounting_stop") for e in events):
                critical.append("accounting_stop")
            answers = [e["payload"] for e in events if e["kind"] == "answer"]
            if result["status"] == "ok" and (
                not result.get("answer") or result.get("error") or answers != [result["answer"]]
            ):
                critical.append("fabricated_success_envelope")
            record = {
                "run_id": run["run_id"],
                "status": "completed",
                "calls": generated,
                "sql_attempts": sql,
                "product_status": result["status"],
                "trace_hashes": trace_hashes,
                "ledger_after": after_ledger,
                "critical": critical,
                "provider_artifacts": provider_artifacts,
            }
            persist(directory / "completed.json", record)
            records.append(record)
            if critical:
                stop = {"run_id": run["run_id"], "reason": critical}
                break
        except Exception as exc:  # noqa: BLE001 — fail closed, never export exception text
            # Do not persist exception messages: third-party exceptions can contain secrets.
            stop = {
                "run_id": run["run_id"],
                "reason": "critical_or_accounting_integrity_stop",
                "exception_type": type(exc).__name__,
            }
            persist(directory / "abort.json", stop)
            break
    completed = {r["run_id"] for r in records}
    statuses = [
        {
            "run_id": r["run_id"],
            "status": "completed"
            if r["run_id"] in completed
            else "started"
            if (output / r["run_id"] / "started.json").exists()
            else "not-run",
        }
        for r in runs
    ]
    summary = {
        "version": VERSION,
        "campaign_id": reg["campaign_id"],
        "calls": calls,
        "statuses": statuses,
        "stop": stop,
        "complete": len(records) == 48 and not stop,
    }
    persist(output / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registration", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Campaign output already exists; no resume/retry")
    reg = json.loads(args.registration.read_text())
    runs, fixtures = validate_registration(reg)
    # One stable global campaign lock prevents parallel collectors from independent outputs.
    lock_path = ROOT / "runtime/h015-collector.lock"
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock.seek(0)
        if lock.read():
            raise ValueError("Campaign already started; no evaluator rerun")
        check_ledger(Path(reg["ledger_path"]), reg["policy_sha256"], reg["ledger_baseline_sha256"])
        lock.write(reg["campaign_id"] + "\n")
        lock.flush()
        os.fsync(lock.fileno())
        directory = os.open(lock_path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        result = collect(
            reg, runs, fixtures, args.output, revalidate=lambda: validate_registration(reg)
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
