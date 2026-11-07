"""Run CP-R2/R3 offline verification from a tracked-only disposable checkout.

Requires an already-created fresh environment via uv sync --locked. This script
never installs packages, fetches Git, loads credentials or alters real ledgers.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import sqlite3
import subprocess
import tempfile
from pathlib import Path

from universitydb.contracts import Failure
from universitydb.db import initialize

ROOT = Path(__file__).resolve().parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    os.chdir(ROOT)
    env = os.environ.copy()
    for name in (
        "OPENAI_API_KEY",
        "UNIVERSITYDB_ROOT",
        "UNIVERSITYDB_TEST_MODE",
        "UNIVERSITYDB_TEST_FIXTURE",
    ):
        env.pop(name, None)
    env.update(
        UNIVERSITYDB_LIVE_APPROVED="no", LANGSMITH_TRACING="false", LANGCHAIN_TRACING_V2="false"
    )
    receipt = {
        "tested_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "profile": "offline/injected; NOT real-model NL-to-SQL accuracy",
        "commands": [],
        "databases": {},
        "status": "running",
    }
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    with tempfile.TemporaryDirectory(prefix="h014-init-") as folder:
        for kind, resources in (
            ("university", ROOT / "resources"),
            ("library", ROOT / "resources/library"),
        ):
            database = Path(folder) / (kind + ".db")
            initialize(database, resources)
            before = digest(database)
            with sqlite3.connect(database) as connection:
                tables = [
                    r[0]
                    for r in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                    )
                ]
                counts = {
                    t: connection.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
                    for t in tables
                }
                assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
                assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
            try:
                initialize(database, resources)
            except Failure as failure:
                assert failure.code == "DB_UNAVAILABLE"
            else:
                raise AssertionError("Repeated initialization unexpectedly overwrote the database")
            assert digest(database) == before
            receipt["databases"][kind] = {
                "db_sha256": before,
                "row_counts": counts,
                "repeat_init": "refused DB_UNAVAILABLE; original DB hash unchanged",
                "resources_sha256": {
                    name: digest(resources / name) for name in ("schema.sql", "seed.sql")
                },
            }
    commands = [
        ["uv", "run", "--locked", "pytest", "-q", "--basetemp=" + str(out / "pytest-temp")],
        ["uv", "run", "--locked", "ruff", "check", "src", "tests"],
        ["uv", "run", "--locked", "ruff", "format", "--check", "src", "tests"],
        ["uv", "run", "--locked", "mypy", "src/universitydb", "--ignore-missing-imports"],
        ["uv", "run", "--locked", "python", "-m", "compileall", "-q", "src", "tests"],
        [
            "uv",
            "run",
            "--locked",
            "python",
            "docs/operations/H-014/readiness_e2e.py",
            str(out / "graph-e2e"),
        ],
        [
            "uv",
            "run",
            "--locked",
            "python",
            "docs/operations/H-013/m1/capture.py",
            str(out / "pytest-temp"),
            "--verification",
            "Fresh full pytest command in clean-run command-1.txt passed",
            "--output-dir",
            str(out / "m1"),
        ],
    ]
    for index, command in enumerate(commands, 1):
        with (out / f"command-{index}.txt").open("w") as stream:
            result = subprocess.run(
                command, check=False, env=env, stdout=stream, stderr=subprocess.STDOUT
            )
        receipt["commands"].append(
            {"argv": command, "exit_code": result.returncode, "log": f"command-{index}.txt"}
        )
        receipt["status"] = "failed" if result.returncode else "running"
        (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        if result.returncode:
            raise SystemExit(result.returncode)
    spec = importlib.util.spec_from_file_location(
        "h013_oracle", ROOT / "docs/operations/H-013/independent_oracle.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    frozen = ROOT / "docs/operations/H-013/frozen-oracle.json"
    checks = module.check(json.loads(frozen.read_text()))
    receipt["oracle"] = {
        "checks": len(checks),
        "check_names": checks,
        "frozen_sha256": digest(frozen),
        "product_imports": False,
    }
    receipt["runtime_ledger_absent"] = not (ROOT / "runtime/spending.json").exists()
    assert receipt["runtime_ledger_absent"]
    receipt["status"] = "passed"
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "passed",
                "tested_sha": receipt["tested_sha"],
                "commands": len(commands),
                "oracle_checks": len(checks),
            }
        )
    )


if __name__ == "__main__":
    main()
