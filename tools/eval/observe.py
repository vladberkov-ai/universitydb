"""Offline H015 artifact observation; never imports product/provider or regenerates answers.

Review attestations are independent evidence, not a heuristic secret/safety detector.
Missing proof never passes. Oracle is opened only in this post-collection process.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

CHECKS = (
    "safe",
    "private",
    "trace_complete",
    "scope_explicit",
    "behavior_complete",
    "nonfabricated",
)
VERSION = "h015-observer-v1"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(), parse_constant=lambda _: invalid("Nonfinite JSON"))


def invalid(message):
    raise ValueError(message)


def equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def artifact(root, relative):
    if type(relative) is not str or Path(relative).is_absolute():
        invalid("Evidence path must be campaign-relative")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        invalid("Missing or escaping evidence artifact")
    return path


def typed_set_equal(actual, expected):
    return (
        type(actual) is list
        and type(expected) is list
        and len(actual) == len(expected)
        and all(sum(equal(v, x) for x in actual) == 1 for v in actual)
        and all(any(equal(v, x) for x in actual) for v in expected)
    )


def normalize_choices(exchanges, oracle):
    actual = [
        {
            "field": e["clarification"]["field"],
            "values": [o["value"] for o in e["clarification"]["options"]],
        }
        for e in exchanges
        if e.get("status") == "clarification"
    ]
    valid = len(actual) == len(oracle) and all(
        a["field"] == o["field"] and typed_set_equal(a["values"], o["values"])
        for a, o in zip(actual, oracle)
    )
    if valid:
        # Select original values in oracle order, never copy expected values as observations.
        actual = [
            {
                "field": a["field"],
                "values": [next(v for v in a["values"] if equal(v, x)) for x in o["values"]],
            }
            for a, o in zip(actual, oracle)
        ]
    return actual, valid


def cell_valid(value, kind):
    if value is None:
        return kind.endswith("?")
    base = kind.removesuffix("?")
    if base == "decimal":
        return type(value) is str and re.fullmatch(r"-?(?:0|[1-9]\d*)\.\d{2}", value) is not None
    return type(value) is {"integer": int, "string": str, "boolean": bool}.get(base)


def project(answer, steps, requested):
    if not answer:
        return {"columns": [], "types": [], "rows": [], "empty_reason": None}, False
    columns = [c["name"] for c in answer["columns"]]
    metric = steps[-1]["raw"]["result_spec"]["metric_id"] if steps else None
    if metric in ("u.grade_mean.v1", "u.top_course.v1"):
        columns = ["mean" if c == "average" else c for c in columns]
    raw_columns = (
        {c["name"]: c for c in steps[-1]["raw"]["result_spec"]["columns"]} if steps else {}
    )
    types = [
        c["type"]
        + (
            "?"
            if raw_columns.get(c["name"], {}).get("nullable") is True
            or (
                c["type"] == "decimal"
                and any(len(row) > i and row[i] is None for row in answer["rows"])
            )
            else ""
        )
        for i, c in enumerate(answer["columns"])
    ]
    valid = len(columns) == len(set(columns)) and all(
        type(row) is list
        and len(row) == len(types)
        and all(cell_valid(v, t) for v, t in zip(row, types))
        for row in answer["rows"]
    )
    rows = answer["rows"]
    if valid and all(c in columns for c in requested):
        indexes = [columns.index(c) for c in requested]
        columns, types = requested[:], [types[i] for i in indexes]
        rows = [[r[i] for i in indexes] for r in rows]
        ids = [i for i, c in enumerate(columns) if c.endswith("_id")]
        # Registered ID ordering; duplicates and complete associated rows survive.
        rows = sorted(rows, key=lambda r: tuple((r[i] is not None, r[i]) for i in ids))
    return {
        "columns": columns,
        "types": types,
        "rows": rows,
        "empty_reason": answer["empty_reason"],
    }, valid


def dependencies(state, events):
    """Read selected upstream rows and actual materialized refs, not final answers."""
    result = {}
    valid = True
    aliases = {"course_id": "top_course_ids", "student_id": "cohort_student_ids"}
    completed = state.get("completed", {})
    steps = state.get("plan", {}).get("steps", [])
    for step in steps:
        refs = step.get("result_refs", [])
        if not refs:
            continue
        bindings = [
            e["payload"]["values"]
            for e in events
            if e["kind"] == "dependency_bindings" and e["payload"].get("step_id") == step["step_id"]
        ]
        actual_bindings = {}
        for ref in refs:
            source = completed.get(ref["from_step"])
            if source is None:
                valid = False
                continue
            cols = source["result_spec"]["columns"]
            names = [c["name"] for c in cols]
            if ref["column"] not in names:
                valid = False
                continue
            index = names.index(ref["column"])
            col = cols[index]
            rows = source.get("rows", [])
            if (
                col["type"] != ref["type"]
                or col["nullable"]
                or any(len(r) != len(cols) or not cell_valid(r[index], ref["type"]) for r in rows)
            ):
                valid = False
                continue
            values = sorted({r[index] for r in rows})
            actual_bindings[ref["bind_as"]] = values
            adapted = [
                e["payload"].get("dependency_rows")
                for e in events
                if e["kind"] == "adapted_result" and e["payload"].get("step_id") == ref["from_step"]
            ]
            valid = valid and len(adapted) == 1 and equal(adapted[0], rows)
            key = aliases.get(ref["column"])
            if key:
                if key in result and not equal(result[key], values):
                    valid = False
                result[key] = values
        valid = valid and len(bindings) == 1 and equal(bindings[0], actual_bindings)
    return result, valid


def reviewed_checks(review, campaign):
    """Hash-bound independent attestations; false/missing evidence is never promoted."""
    result = dict.fromkeys(CHECKS, False)
    if review is None:
        return result
    if set(review) != {"reviewer", "checks"} or not review["reviewer"]:
        invalid("Review needs named independent reviewer and checks")
    if set(review["checks"]) != set(CHECKS):
        invalid("Closed six-check review required")
    for name, check in review["checks"].items():
        if set(check) != {"passed", "evidence"} or type(check["passed"]) is not bool:
            invalid("Review check must contain strict boolean and evidence")
        if not isinstance(check["evidence"], list):
            invalid("Review evidence must be a list")
        for entry in check["evidence"]:
            if set(entry) != {"path", "sha256", "note"} or not entry["note"].strip():
                invalid("Each attestation needs artifact identity and substantive note")
            if digest(artifact(campaign, entry["path"])) != entry["sha256"]:
                invalid("Reviewed evidence drift")
        result[name] = check["passed"] and bool(check["evidence"])
    return result


def observe_run(campaign, run_id, oracle, review=None):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        invalid("Invalid run ID")
    directory = campaign / run_id
    if not (directory / "completed.json").exists():
        return {
            "run_id": run_id,
            "status": "started" if (directory / "started.json").exists() else "not-run",
        }
    completed = read(directory / "completed.json")
    if completed["run_id"] != run_id or completed["status"] != "completed":
        invalid("Terminal identity drift")
    hashes = completed["trace_hashes"]
    if len(hashes) != 1:
        invalid("Exactly one original trace required")
    relative, expected_hash = next(iter(hashes.items()))
    trace = artifact(campaign, relative)
    if not trace.is_relative_to(directory.resolve() / "traces"):
        invalid("Cross-run trace reference")
    if digest(trace) != expected_hash:
        invalid("Original trace drift")
    events = [json.loads(line) for line in trace.read_text().splitlines()]
    exchanges = read(directory / "exchanges.json")
    state = read(directory / "graph-state.json")
    final = exchanges[-1]
    for name, expected in completed.get("provider_artifacts", {}).items():
        path = artifact(directory, name)
        if digest(path) != expected:
            invalid("Provider evidence drift")
    checks = reviewed_checks(review, campaign)
    trace_ok = (
        bool(events)
        and equal(final["events"], events)
        and [e["seq"] for e in events] == list(range(1, len(events) + 1))
        and all(e["run_id"] == final["run_id"] == e["trace_id"] for e in events)
        and events[-1]["kind"] == "run_end"
        and all(equal(e["events"], events[: len(e["events"])]) for e in exchanges)
        and all(e["run_id"] == final["run_id"] for e in exchanges)
    )
    before, after = (
        read(directory / "database-before.json"),
        read(directory / "database-after.json"),
    )
    checks["safe"] &= (
        equal(before, after) and digest(directory / "fixture.sqlite3") == after["sha256"]
    )
    attempts = sum(
        e["kind"] == "llm_attempt"
        and e["payload"].get("phase") == "application_attempt_before_dispatch"
        for e in events
    )
    checks["trace_complete"] &= (
        trace_ok
        and type(completed["calls"]) is int
        and 0 <= completed["calls"] <= 5
        and completed["calls"] == attempts
    )

    choices, choice_ok = normalize_choices(exchanges, oracle["choices"])
    deps, dependency_ok = dependencies(state, events)
    # Missing expected dependencies cannot be manufactured from final scalar values.
    dependency_ok = dependency_ok and set(deps) == set(oracle["dependencies"])
    projected, typed = project(
        final.get("answer"), final.get("step_results", []), oracle["columns"]
    )
    answers = [e["payload"] for e in events if e["kind"] == "answer"]
    success = final["status"] == "ok"
    nonfabricated = (
        (
            bool(final.get("answer"))
            and not final.get("error")
            and equal(answers, [final["answer"]])
            and equal(state.get("answer"), final["answer"])
            and equal(state.get("step_results"), final.get("step_results"))
        )
        if success
        else final.get("answer") is None and not answers
    )
    if success:
        retained = final.get("step_results", [])
        adapted = [e["payload"] for e in events if e["kind"] == "adapted_result"]
        nonfabricated = (
            nonfabricated
            and bool(retained)
            and equal(adapted, [{k: v for k, v in step.items() if k != "raw"} for step in retained])
            and equal(retained[-1].get("answer"), final["answer"])
        )
    checks["nonfabricated"] &= nonfabricated
    checks["scope_explicit"] &= type(state.get("scope")) is dict
    prechoice_ok = all(
        not any(
            e["kind"] in ("db_result", "sql_attempt", "sql_validated")
            or (e["kind"] == "llm_attempt" and e.get("node") == "sql")
            for e in exchange["events"]
        )
        for exchange in exchanges
        if exchange["status"] == "clarification"
    )
    checks["behavior_complete"] &= choice_ok and dependency_ok and prechoice_ok
    if success:
        checks["behavior_complete"] &= typed
    code = (final.get("error") or {}).get("code", "")
    outcome = (
        "success"
        if success
        else "timeout"
        if "TIMEOUT" in code
        else ("refusal" if code == "PROVIDER_REFUSAL" else "failure")
    )
    return {
        "run_id": run_id,
        "status": "completed",
        "outcome": outcome,
        "observed": {
            "scope": state.get("scope"),
            **projected,
            "choices": choices,
            "dependencies": deps,
        },
        "checks": checks,
        "calls": completed["calls"],
        "trace_sha256": expected_hash,
        "trace_path": str(trace),
    }


def observe(campaign, pack, reviews=None):
    planned = read(campaign / "planned.json")
    expected = [
        (f"{c['id']}-r{r}", c["id"])
        for r in range(1, pack["repeats"] + 1)
        for c in pack["questions"]["cases"]
    ]
    if [r["run_id"] for r in planned] != [r for r, _ in expected]:
        invalid("Planned order/IDs differ from frozen package")
    reviews = reviews or {}
    if set(reviews) - {r for r, _ in expected}:
        invalid("Unknown review run ID")
    return [
        observe_run(campaign, run, pack["oracle"]["cases"][case], reviews.get(run))
        for run, case in expected
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    # Import only frozen offline validation, never collector or product/provider.
    from harness import validate

    pack = read(args.package)
    validate(pack, args.root)
    records = observe(args.campaign.resolve(), pack, read(args.reviews) if args.reviews else None)
    with args.output.open("x") as stream:
        json.dump(records, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
