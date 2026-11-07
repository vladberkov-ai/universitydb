"""Readiness runner: real graph/SQLite, injected proposals; never NL accuracy.

Run from a tracked checkout root using its locked environment. Preserves full
actual JSONL and existing dynamic M1 proof outputs, without touching real runtime.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from test_i2_core import scripted_step

from universitydb import db
from universitydb.agent import Agent
from universitydb.domain import University, make_spec
from universitydb.llm import ScriptedProvider


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    receipt = {
        "tested_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "profile": "offline/injected; NOT real-model NL-to-SQL accuracy",
        "real_provider_called": False,
        "cases": {},
    }
    with tempfile.TemporaryDirectory(prefix="h014-readiness-") as folder:
        temp = Path(folder)
        path = temp / "university.db"
        db.initialize(path, ROOT / "resources")
        # Independently fixed values, not calculated by the production formatter.
        expected = {
            "group": [[1, "80.00", 5, 6], [2, "100.00", 1, 1], [3, None, 0, 1]],
            "top": [[2, "100.00", 1, 1]],
        }
        for name, metric in (("group", "grade_mean"), ("top", "top_course")):
            domain = University()
            spec = make_spec(metric, "course_id")
            sql, params = domain.query(spec, {})
            provider = ScriptedProvider(list(scripted_step(spec, sql, params)))
            result = Agent(domain, path, provider, temp / "traces").run(
                "Show mean grade grouped by course across all enrollments"
                if name == "group"
                else "Show the course with the highest mean grade"
            )
            (output / (name + "-result.json")).write_text(json.dumps(result, indent=2) + "\n")
            assert result["status"] == "ok", result
            assert result["answer"]["rows"] == expected[name], result["answer"]
            trace = temp / "traces" / (result["run_id"] + ".jsonl")
            shutil.copyfile(trace, output / (name + ".jsonl"))
            receipt["cases"][name] = {
                "expected_rows": expected[name],
                "actual_rows": result["answer"]["rows"],
                "trace_sha256": digest(trace),
                "provider_calls": provider.calls,
            }
        assert not (temp / "runtime/spending.json").exists()
        receipt["temporary_ledger_absent"] = True
    receipt["status"] = "passed"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
