"""Offline preregistration/export/scoring only. No provider or product imports."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

VERSION = "h014-eval-v1"
CATEGORIES = (
    "aggregates_null",
    "joins_filters",
    "dependencies_ties",
    "clarification",
    "empty_negative",
    "library",
)
CHECKS = (
    "safe",
    "private",
    "trace_complete",
    "scope_explicit",
    "behavior_complete",
    "nonfabricated",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_equal(left, right):
    """JSON equality without Python bool/int or int/float coercion."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(strict_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def validate(pack, root):
    if pack["version"] != VERSION or pack["kind"] not in ("dev", "heldout_candidate"):
        raise ValueError("Unknown package version/kind")
    if type(pack["repeats"]) is not int or not 1 <= pack["repeats"] <= 2:
        raise ValueError("Invalid repeat count")
    cases = pack["questions"]["cases"]
    oracles = pack["oracle"]["cases"]
    ids = [c["id"] for c in cases]
    if not ids or len(ids) != len(set(ids)) or set(ids) != set(oracles):
        raise ValueError("Missing, duplicate or extra oracle/case IDs")
    if pack["kind"] == "heldout_candidate":
        if Counter(c["category"] for c in cases) != Counter(dict.fromkeys(CATEGORIES, 4)):
            raise ValueError("Expected six categories with four cases each")
        if pack["repeats"] != 2:
            raise ValueError("Expected two repeats")
    if not pack["source_hashes"]:
        raise ValueError("Source hashes required")
    for fixture in pack["fixtures"].values():
        content = {k: v for k, v in fixture.items() if k != "sha256"}
        actual = hashlib.sha256(
            json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        if actual != fixture["sha256"]:
            raise ValueError("Fixture identity drift")
        if any(fixture[k] not in pack["source_hashes"] for k in ("schema", "seed")):
            raise ValueError("Unpinned fixture resource")
    for path, expected in pack["source_hashes"].items():
        if digest(Path(root) / path) != expected:
            raise ValueError(f"Source identity drift: {path}")
    for case in cases:
        if set(case) != {"id", "category", "domain", "fixture", "question", "selections"}:
            raise ValueError("Question fields not allowlisted; oracle leakage forbidden")
        if case["category"] not in CATEGORIES or case["domain"] not in ("university", "library"):
            raise ValueError("Unknown category/domain")
        if not isinstance(case["question"], str) or not case["question"].strip():
            raise ValueError("Empty question")
        if case["fixture"] not in pack["fixtures"]:
            raise ValueError("Missing fixture")
        expected = oracles[case["id"]]
        if set(expected) != {
            "scope",
            "columns",
            "types",
            "rows",
            "empty_reason",
            "choices",
            "dependencies",
        }:
            raise ValueError("Closed oracle schema required")
        if len(expected["columns"]) != len(expected["types"]):
            raise ValueError("Column/type mismatch")
        for row in expected["rows"]:
            if len(row) != len(expected["types"]):
                raise ValueError("Ragged expected row")
            for value, kind in zip(row, expected["types"]):
                legal = {"integer": int, "string": str, "decimal": str}
                base = kind.removesuffix("?")
                if base not in legal or not (
                    value is None and kind.endswith("?") or type(value) is legal[base]
                ):
                    raise ValueError("Invalid expected cell type")
                if (
                    value is not None
                    and base == "decimal"
                    and not re.fullmatch(r"[0-9]+\.[0-9]{2}", value)
                ):
                    raise ValueError("Decimal must be exact two-place string")
    return cases


def payloads(pack, root):
    """Export ONLY user conversations; fixtures are local setup, never model answers."""
    cases = validate(pack, root)
    return [
        {
            "run_id": f"{c['id']}-r{repeat}",
            "case_id": c["id"],
            "repeat": repeat,
            "domain": c["domain"],
            "fixture": c["fixture"],
            "question": c["question"],
            "selections": c["selections"],
        }
        for repeat in range(1, pack["repeats"] + 1)
        for c in cases
    ]


def planned(pack, root):
    return [{"run_id": p["run_id"], "status": "not-run"} for p in payloads(pack, root)]


def score(pack, records, root):
    runs = {p["run_id"]: p for p in payloads(pack, root)}
    if len(records) != len(runs) or {r["run_id"] for r in records} != set(runs):
        raise ValueError(
            "Every planned run needs exactly one record; missing/duplicate/extra forbidden"
        )
    totals = Counter()
    category_pass = Counter(dict.fromkeys(CATEGORIES, 0))
    outcomes = []
    for record in records:
        run = runs[record["run_id"]]
        status = record["status"]
        if status not in ("planned", "not-run", "started", "completed"):
            raise ValueError("Unknown run status")
        totals[status] += 1
        passed = False
        if status == "completed":
            if set(record) != {
                "run_id",
                "status",
                "outcome",
                "observed",
                "checks",
                "calls",
                "trace_sha256",
                "trace_path",
            }:
                raise ValueError("Invalid completed record")
            if record["outcome"] not in (
                "success",
                "failure",
                "timeout",
                "refusal",
                "invalid",
                "infra_abort",
            ):
                raise ValueError("Unknown terminal outcome")
            checks = record["checks"]
            if set(checks) != set(CHECKS) or any(type(v) is not bool for v in checks.values()):
                raise ValueError("Every mandatory check needs strict boolean evidence")
            if type(record["calls"]) is not int or not 0 <= record["calls"] <= 5:
                raise ValueError("Invalid generation count")
            trace = record["trace_sha256"]
            if (
                not isinstance(trace, str)
                or len(trace) != 64
                or any(c not in "0123456789abcdef" for c in trace)
            ):
                raise ValueError("Trace artifact hash required")
            artifact = (Path(root) / record["trace_path"]).resolve()
            if not artifact.is_relative_to(Path(root).resolve()) or digest(artifact) != trace:
                raise ValueError("Missing or mismatched trace artifact")
            passed = (
                record["outcome"] == "success"
                and all(checks.values())
                and strict_equal(record["observed"], pack["oracle"]["cases"][run["case_id"]])
            )
            if (
                not checks["behavior_complete"]
                or not checks["trace_complete"]
                or not checks["scope_explicit"]
                or not checks["nonfabricated"]
            ):
                totals["mandatory_failures"] += 1
            if not checks["safe"] or not checks["private"]:
                totals["critical_failures"] += 1
        elif set(record) != {"run_id", "status"}:
            raise ValueError("Noncompleted record cannot carry claimed results")
        category = next(
            c["category"] for c in pack["questions"]["cases"] if c["id"] == run["case_id"]
        )
        category_pass[category] += passed
        totals["passed"] += passed
        outcomes.append({"run_id": record["run_id"], "status": status, "pass": passed})
    complete = totals["completed"] == len(runs)
    return {
        "scorer": VERSION,
        "kind": pack["kind"],
        "planned_denominator": len(runs),
        "statuses": {s: totals[s] for s in ("planned", "not-run", "started", "completed")},
        "observed_passes": totals["passed"],
        "category_passes": dict(category_pass),
        "critical_failures": totals["critical_failures"],
        "mandatory_failures": totals["mandatory_failures"],
        "complete": complete,
        "proposed_threshold_met": complete
        and pack["kind"] == "heldout_candidate"
        and totals["passed"] >= 44
        and min(category_pass.values()) >= 7
        and totals["critical_failures"] == 0
        and totals["mandatory_failures"] == 0,
        "outcomes": outcomes,
        "warning": "Offline scorer output is not live accuracy; thresholds proposed, not accepted.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "plan", "score"))
    parser.add_argument("package", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--records", type=Path)
    args = parser.parse_args()
    pack = json.loads(args.package.read_text())
    if args.command == "export":
        result = payloads(pack, args.root)
    elif args.command == "plan":
        result = planned(pack, args.root)
    else:
        if args.records is None:
            parser.error("score requires --records")
        result = score(pack, json.loads(args.records.read_text()), args.root)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
