"""I1 evidence recorder: real graph/provider; no transport or answer substitution."""

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from universitydb.agent import Agent
from universitydb.config import PROFILE, logical_operation, payload_estimate, wire_payload
from universitydb.domain import University
from universitydb.llm import OpenAIProvider
from universitydb.ui import QUESTION

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


class RecordingProvider(OpenAIProvider):
    """Capture exact shared wire-builder result; delegate unchanged real dispatch."""

    def __init__(self, directory):
        super().__init__(ROOT / "src/universitydb/prompts", ROOT / "runtime/spending.json")
        self.directory = directory
        self.sequence = 0

    def call(self, operation, payload, output_type, *, timeout=PROFILE.run_seconds):
        self.sequence += 1
        prompt = (self.prompts / f"{operation}.txt").read_text()
        wire = wire_payload(
            operation,
            logical_operation(operation, payload),
            PROFILE.model,
            prompt,
            json.dumps(payload, ensure_ascii=False),
        )
        path = self.directory / f"request-{self.sequence:02d}.json"
        save(path, wire)
        result, usage = super().call(operation, payload, output_type, timeout=timeout)
        save(
            self.directory / f"response-{self.sequence:02d}.json",
            {"parsed_output": result.model_dump(), "usage": usage},
        )
        return result, usage


def main():
    mode = sys.argv[1:]
    if mode not in (["--live-s6"], ["--live-mutation"]):
        # Offline smoke: no construction of real provider, no ledger mutation/network.
        assert ROOT.joinpath("resources/seed.sql").exists()
        wire = wire_payload("plan", "plan", PROFILE.model, "test", "{}")
        assert payload_estimate(wire)[1] <= PROFILE.input_bytes
        print("offline harness validation passed; no network or ledger mutation")
        return
    mutation = mode == ["--live-mutation"]
    planned = (
        json.loads((EVIDENCE / "mutation-planned-oracle.json").read_text()) if mutation else None
    )
    question = planned["question"] if planned else QUESTION
    oracle = (
        planned["oracle"]
        if planned
        else {"sum_units": 16000, "graded_count": 2, "enrollment_count": 2, "answer": "80.00"}
    )
    directory = EVIDENCE / ("mutation" if mutation else "s6")
    directory.mkdir(parents=True, exist_ok=False)
    ledger = ROOT / "runtime/spending.json"
    database = ROOT / "runtime/university.db"
    before = hashlib.sha256(database.read_bytes()).hexdigest()
    save(
        directory / "baseline.json",
        {
            "started_at": datetime.now(UTC).isoformat(),
            "database_sha256_before": before,
            "spending_ledger_present": ledger.exists(),
            "spending_before": json.loads(ledger.read_text()) if ledger.exists() else None,
            "question": question,
            "independent_oracle": oracle,
            "capture_coverage": "Exact shared wire-builder payload before real provider call; typed outputs and safe usage after call. Not raw HTTP bytes/headers/credentials or hidden model reasoning.",
        },
    )
    result = Agent(
        University(), database, RecordingProvider(directory), ROOT / "runtime/traces"
    ).run(question)
    save(directory / "result.json", result)
    trace = ROOT / "runtime/traces" / f"{result['run_id']}.jsonl"
    (directory / "trace.jsonl").write_bytes(trace.read_bytes())
    save(
        directory / "receipt.json",
        {
            "finished_at": datetime.now(UTC).isoformat(),
            "status": result["status"],
            "error": result["error"],
            "answer": result["answer"],
            "run_id": result["run_id"],
            "database_sha256_after": hashlib.sha256(database.read_bytes()).hexdigest(),
            "database_unchanged": before == hashlib.sha256(database.read_bytes()).hexdigest(),
            "spending_after": json.loads(ledger.read_text()) if ledger.exists() else None,
        },
    )
    print(json.dumps(json.loads((directory / "receipt.json").read_text()), ensure_ascii=False))


if __name__ == "__main__":
    main()
