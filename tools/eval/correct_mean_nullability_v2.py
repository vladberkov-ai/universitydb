"""Post-results artifact-only scalar mean type correction, not an evaluator or score.

Development tool: actual campaign use requires separate owner clarification/review.
No product, frozen observer, oracle, provider or scorer imports; no network activity.
"""

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

VERSION = "h015-mean-nullability-correction-v2"
FROZEN_OBSERVER_SHA256 = "a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14"
CHECKS = {
    "safe",
    "private",
    "trace_complete",
    "scope_explicit",
    "behavior_complete",
    "nonfabricated",
}
METRICS = {
    f"u.{name}.v1"
    for name in ("grade_mean", "top_course", "enrollment_counts", "student_ids", "enrollment_rows")
}
METRICS.add("l.open_count.v1")  # Library.SPEC: count-only; never a grade mean.

# Registered raw scalar mean contract: domain.make_spec, not oracle expected types/values.
SCALAR_MEAN_SPEC = {
    "metric_id": "u.grade_mean.v1",
    "shape": "aggregate",
    "group_keys": [],
    "columns": [
        {"name": name, "type": "integer", "nullable": False}
        for name in ("sum_units", "graded_count", "enrollment_count")
    ],
    "components": {"sum": "sum_units", "denominator": "graded_count", "count": "enrollment_count"},
    "unit": "grade_hundredth",
    "scale": 100,
}


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def equal(left: Any, right: Any) -> bool:
    return type(left) is type(right) and (
        left.keys() == right.keys() and all(equal(left[k], right[k]) for k in left)
        if type(left) is dict
        else len(left) == len(right) and all(equal(a, b) for a, b in zip(left, right))
        if type(left) is list
        else bool(left == right)
    )


def digest(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def read(path: str | Path) -> Any:
    return json.loads(
        Path(path).read_text(),
        object_pairs_hook=unique_object,
        parse_constant=lambda _: require(False, "Nonfinite JSON"),
    )


def correct_record(
    record: dict[str, Any], state: dict[str, Any], exchanges: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Return a copy plus exact field deltas; never infer nullability from values."""
    try:
        return _correct_record(record, state, exchanges)
    except (KeyError, TypeError, IndexError, AttributeError) as exc:
        raise ValueError("Malformed retained observation/artifact schema") from exc


def _correct_record(
    record: dict[str, Any], state: dict[str, Any], exchanges: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    require(
        set(record)
        == {
            "run_id",
            "status",
            "outcome",
            "observed",
            "checks",
            "calls",
            "trace_sha256",
            "trace_path",
        },
        "Closed completed record required",
    )
    require(record["status"] == "completed", "Unknown record status")
    require(type(record["calls"]) is int and 0 <= record["calls"] <= 5, "Invalid calls")
    require(
        set(record["checks"]) == CHECKS and all(type(v) is bool for v in record["checks"].values()),
        "Invalid checks",
    )
    observed = record["observed"]
    require(
        set(observed)
        == {"scope", "columns", "types", "rows", "empty_reason", "choices", "dependencies"},
        "Closed observed schema required",
    )
    require(type(exchanges) is list and bool(exchanges), "Missing exchanges")
    final = exchanges[-1]
    require(final["status"] in {"ok", "error", "clarification"}, "Unknown final status")
    if final["status"] != "ok":
        code = (final.get("error") or {}).get("code", "")
        outcome = (
            "timeout"
            if "TIMEOUT" in code
            else ("refusal" if code == "PROVIDER_REFUSAL" else "failure")
        )
        require(
            record["outcome"] == outcome and final.get("answer") is None,
            "Failure status/answer mismatch",
        )
        return copy.deepcopy(record), []
    require(record["outcome"] == "success" and not final.get("error"), "Success mismatch")
    answer, steps = final["answer"], final["step_results"]
    require(
        bool(steps)
        and equal(answer, state["answer"])
        and equal(steps, state["step_results"])
        and equal(answer, steps[-1]["answer"]),
        "Answer/state provenance mismatch",
    )
    require(equal(observed["scope"], state["scope"]), "Scope provenance mismatch")
    step = steps[-1]
    spec = step["raw"]["result_spec"]
    require(spec["metric_id"] in METRICS, "Unknown metric")
    require(type(spec["group_keys"]) is list, "Invalid grouping")
    if spec["metric_id"] != "u.grade_mean.v1" or spec["group_keys"]:
        return copy.deepcopy(record), []
    require(equal(spec, SCALAR_MEAN_SPEC), "Scalar mean contract drift")
    require(equal(state["completed"][step["step_id"]], step["raw"]), "Raw provenance mismatch")
    events = final["events"]
    require(
        equal([e["payload"] for e in events if e["kind"] == "answer"], [answer])
        and equal(
            [
                e["payload"]
                for e in events
                if e["kind"] == "db_result" and e["payload"].get("step_id") == step["step_id"]
            ],
            [step["raw"]],
        )
        and equal(
            [
                e["payload"]
                for e in events
                if e["kind"] == "adapted_result" and e["payload"].get("step_id") == step["step_id"]
            ],
            [{k: v for k, v in step.items() if k != "raw"}],
        ),
        "Original raw/adapted/answer event provenance mismatch",
    )

    require(
        answer["columns"]
        == [
            {"name": n, "type": t}
            for n, t in [
                ("average", "decimal"),
                ("graded_count", "integer"),
                ("enrollment_count", "integer"),
            ]
        ],
        "Derived answer schema mismatch",
    )
    rows = answer["rows"]
    require(
        type(rows) is list and len(rows) == 1 and type(rows[0]) is list and len(rows[0]) == 3,
        "Scalar mean must have one full row",
    )
    value, graded, count = rows[0]
    require(
        value is None or (type(value) is str and re.fullmatch(r"-?(?:0|[1-9]\d*)\.\d{2}", value)),
        "Invalid derived decimal",
    )
    require(
        type(graded) is int and type(count) is int and 0 <= graded <= count,
        "Invalid strict integer counts",
    )
    require(answer["empty_reason"] in (None, "no_rows", "no_grades"), "Invalid reason")
    names = ["mean", "graded_count", "enrollment_count"]
    columns = observed["columns"]
    require(
        type(columns) is list
        and bool(columns)
        and len(set(columns)) == len(columns)
        and all(c in names for c in columns),
        "Invalid projected columns",
    )
    indexes = [names.index(c) for c in columns]
    require(
        equal(observed["rows"], [[rows[0][i] for i in indexes]])
        and equal(observed["empty_reason"], answer["empty_reason"]),
        "Observed rows/reason differ from original answer",
    )
    kinds = ["decimal?" if value is None else "decimal", "integer", "integer"]
    require(
        equal(observed["types"], [kinds[i] for i in indexes]),
        "Observation is not the frozen v1 projection",
    )
    result = copy.deepcopy(record)
    changes = []
    if "mean" in columns:
        index = columns.index("mean")
        if result["observed"]["types"][index] == "decimal":
            result["observed"]["types"][index] = "decimal?"
            changes.append(
                {"field": f"/observed/types/{index}", "old": "decimal", "new": "decimal?"}
            )
    return result, changes


def run(
    campaign: Path, records_path: Path, receipt_path: Path, output: Path, manifest: Path
) -> dict[str, Any]:
    """Hash-bound local artifacts only. Caller supplies reviewed provenance receipt."""
    campaign = Path(campaign).resolve()
    records_path, receipt_path, output, manifest = (
        Path(p).resolve() for p in (records_path, receipt_path, output, manifest)
    )
    require(
        output != manifest
        and all(
            p not in {records_path, receipt_path} and not p.is_relative_to(campaign)
            for p in (output, manifest)
        ),
        "Outputs must be distinct, new, and outside original campaign",
    )
    receipt = read(receipt_path)
    require(
        type(receipt) is dict
        and set(receipt) == {"source_version", "observer_sha256", "records_sha256", "artifacts"},
        "Invalid source receipt",
    )
    require(
        receipt["source_version"] == "h015-observer-v1"
        and receipt["observer_sha256"] == FROZEN_OBSERVER_SHA256,
        "Unknown original instrument identity",
    )
    require(digest(records_path) == receipt["records_sha256"], "Original records drift")
    hashes = receipt["artifacts"]
    require(type(hashes) is dict, "Artifact hash map required")
    for relative, sha in hashes.items():
        require(
            type(relative) is str
            and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts
            and (campaign / relative).resolve().is_relative_to(campaign),
            "Escaping reference",
        )
        require(type(sha) is str and re.fullmatch(r"[0-9a-f]{64}", sha), "Invalid artifact hash")
    consumed = set()

    def original(relative: str) -> Path:
        require(relative in hashes, "Missing reviewed artifact reference")
        path = (campaign / relative).resolve()
        require(path.is_file() and digest(path) == hashes[relative], "Original artifact drift")
        consumed.add(relative)
        return path

    records = read(records_path)
    require(type(records) is list and bool(records), "Records must be a nonempty list")
    seen: set[str] = set()
    corrected: list[dict[str, Any]] = []
    changes: list[dict[str, str]] = []
    for record in records:
        require(
            type(record) is dict
            and type(record.get("run_id")) is str
            and re.fullmatch(r"[A-Za-z0-9_-]+", record["run_id"]),
            "Invalid run identity",
        )
        run_id = record["run_id"]
        require(run_id not in seen, "Duplicate run identity")
        seen.add(run_id)
        if record.get("status") in ("not-run", "started"):
            require(set(record) == {"run_id", "status"}, "Invalid unfinished record")
            corrected.append(copy.deepcopy(record))
            continue
        require(record.get("status") == "completed", "Unknown record status")
        terminal = read(original(f"{run_id}/completed.json"))
        require(
            terminal["run_id"] == run_id
            and terminal["status"] == "completed"
            and equal(terminal["calls"], record["calls"]),
            "Terminal identity/calls mismatch",
        )
        trace_hashes = terminal["trace_hashes"]
        require(type(trace_hashes) is dict and len(trace_hashes) == 1, "One trace required")
        relative, sha = next(iter(trace_hashes.items()))
        require(Path(relative).parent == Path(run_id) / "traces", "Cross-run trace reference")
        trace = original(relative)
        require(
            sha == record["trace_sha256"] == digest(trace)
            and Path(record["trace_path"]).resolve() == trace,
            "Trace identity mismatch",
        )
        state = read(original(f"{run_id}/graph-state.json"))
        exchanges = read(original(f"{run_id}/exchanges.json"))
        events = [
            json.loads(
                line,
                object_pairs_hook=unique_object,
                parse_constant=lambda _: require(False, "Nonfinite JSON"),
            )
            for line in trace.read_text().splitlines()
        ]
        require(bool(exchanges) and equal(events, exchanges[-1]["events"]), "Trace/event mismatch")
        updated, delta = correct_record(record, state, exchanges)
        corrected.append(updated)
        changes.extend({"run_id": run_id, **item} for item in delta)
    require(consumed == set(hashes), "Unconsumed/unknown artifact references")
    encoded = (json.dumps(corrected, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    audit = {
        "version": VERSION,
        "source_version": receipt["source_version"],
        "frozen_observer_sha256": FROZEN_OBSERVER_SHA256,
        "correction_source_sha256": digest(__file__),
        "source_receipt_sha256": digest(receipt_path),
        "input_sha256": receipt["records_sha256"],
        "output_sha256": hashlib.sha256(encoded).hexdigest(),
        "artifacts": hashes,
        "changes": changes,
        "scope": "post-results type-only correction; not a score or prospective evidence",
    }
    # Reserve both paths before writing; never truncate or replace an existing artifact.
    with output.open("xb") as out:
        try:
            with manifest.open("x") as proof:
                out.write(encoded)
                json.dump(audit, proof, indent=2, allow_nan=False)
                proof.write("\n")
        except FileExistsError:
            output.unlink()  # Only our just-created empty reservation; original manifest untouched.
            raise
    return audit


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("campaign", "records", "source-receipt", "output", "manifest"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    run(args.campaign, args.records, args.source_receipt, args.output, args.manifest)


if __name__ == "__main__":
    main()
