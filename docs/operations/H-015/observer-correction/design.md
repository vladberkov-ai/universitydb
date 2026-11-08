# Post-results mean-nullability correction v2 — development only

## Boundary and plan (written before implementation)

Prepare an append-only artifact postprocessor and independent synthetic regression
suite. Do not execute on the original campaign, rerun the observer/scorer, change
numeric answers/checks, or claim a corrected score. Owner clarification and separate
independent code/architecture review remain prerequisites to actual use. Original
v1 output remains original instrument output; product quality remains failed.

1. Lock synthetic non-NULL, NULL, zero, empty, strict-type, malformed/provenance,
   duplicate and immutability boundaries before implementation.
2. Add a stdlib-only postprocessor; no product/provider/oracle/scorer imports.
   Derive applicability from retained final raw ResultSpec, not case identifiers,
   oracle types or observed NULL presence. Correct only scalar `u.grade_mean.v1`
   projected `mean` from `decimal` to `decimal?`.
3. Require a reviewer-prepared source receipt binding original records and every
   consumed campaign artifact by SHA256, with frozen observer version/source hash.
   Check final answer/raw/state/trace provenance. Reject unknown shapes/statuses,
   missing hashes, cross-run references, bool-as-int and drift. Other metrics and
   grouped means remain unchanged, never generalized by this repair.
4. Exclusive-create a new output and change manifest; record old/new hashes, exact
   field changes and source identities. Inputs and original scores remain untouched.
5. Run synthetic regressions, existing observer regressions and focused static
   checks. Perform a bounded no-op cleanup review (no masking fallback, duplicate
   observer, monkeypatch, speculative compatibility or dependency addition).

## Contract basis and exposure

Read context: private `handoffs/H-015-full-live-eval.md`, H015 brief, H014 protocol,
observer design and final code-review finding; no actual campaign artifacts or
oracle are read in development. The original observer source stays immutable.
`src/universitydb/domain.py` make_spec and adaptation (especially lines 507–526)
define scalar mean as a derived decimal string or NULL; raw columns contain sum,
graded count and enrollment count, not `average`. `contracts.py` Answer accepts
NULL independently of the current cell. The nullable representation is therefore
contract-owned, not inferred from sample presence. Zero is a decimal value, not
NULL. Empty input's scalar result is NULL with `no_rows`, not an empty row array.
An empty projected row array is rejected because scalar aggregate cardinality is
exactly one. No numerical recomputation is part of this correction.

Writer owns implementation only; root owns separate reviewers and any later
execution authorization. No Git, lifecycle, ledger, product or frozen-file edits.

## Future CLI and source receipt (NOT executed on original campaign)

```sh
.venv/bin/python tools/eval/correct_mean_nullability_v2.py \
  --campaign <immutable-original-campaign> \
  --records <reviewed-original-v1-records.json> \
  --source-receipt <independently-reviewed-source-receipt.json> \
  --output <new-v2-records.json> --manifest <new-correction-manifest.json>
```

The receipt is closed JSON with `source_version: h015-observer-v1`,
`observer_sha256` equal to frozen
`a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14`,
`records_sha256`, and `artifacts` (campaign-relative path → SHA256). Each completed
run consumes exactly its `completed.json`, `graph-state.json`, `exchanges.json`
and the single original trace named by the terminal receipt. Unknown/unconsumed
paths fail: the receipt is not permission to open arbitrary files. No oracle or
package argument exists. A reviewer must establish that the supplied records and
hashes are the actual reviewed v1 originals; self-consistent hashes do not prove
independence, truth, or owner execution authorization.

The tool checks terminal identity/calls/trace path/hash, retained events, public
answer/state/steps, and scalar mean's raw/adapted/answer event provenance. Existing
v1 checks are preserved even when false; it does not redo safety or semantic
assessment. Raw scalar ResultSpec must equal the registered domain contract using
strict JSON types. Other registered metrics and grouped means return unchanged;
Library row/count metrics therefore cannot acquire a mean correction. Unfinished
records remain minimal and unchanged. Unknown status, metric, projection or schema
fails rather than guessing. Reapplying to already corrected non-NULL records fails
because they are no longer original v1 projection. Partial projected scalar columns
remain permitted; omitting `mean` produces no delta.

Output and manifest paths must be distinct and outside the original campaign,
neither may alias records/receipt, and exclusive creation prevents overwrites.
If the manifest already exists the new empty output reservation is removed. Other
I/O failures can leave an incomplete new pair; such a pair is not approved evidence
and must not be consumed. There is no crash-atomic two-file publication claim.
Original input files are never rewritten. The manifest records source version,
frozen observer SHA, correction source SHA, source-receipt SHA, all consumed artifact
hashes, original/new records SHA, and every exact run/JSON-pointer old→new type delta.
There are no numerical corrections, new scores, thresholds or result tallies.

## Development verification and bounded cleanup

Synthetic-only tests cover non-NULL/NULL/zero/no-rows/no-grades, empty scalar row
rejection, strict bool/integer boundaries, duplicate keys/runs, malformed schema,
unknown metric/status, changed scope/rows/types/spec/state, missing/escaping/drifting
references, preserved unrelated metrics/grouping/failures/checks, immutability,
exclusive outputs, refusal to double-correct, and the CLI on fabricated artifacts.
AST import allowlist and source inspection confirm stdlib-only operation, with
no product/observer/scorer/provider/oracle import. This is not a general security
proof or actual collection validation. See `test-receipt.json` for exact hashes.

Bounded ai-slop-cleaner helper: behavior-lock tests precede implementation; no
masking fallback or compatibility branch added, no duplicate observer and no
monkeypatch. The only cleanup was removing an unnecessary map/lambda. Dead-code,
duplication and error-boundary passes required no broader edits; regression
reinforcement covers exclusive output and unchanged false checks. No UI concerns
apply. Initial lint/type diagnostics were corrected and fresh final checks pass.
Independent reviewer/architect approval and any actual-data execution remain root
owned and pending; this writer does not self-approve.

## Independent-review follow-up plan (before edits)

Root's full offline run passed 609 tests; its separate formatting check failed on
these two new files only. Correct those files with Ruff format, then explicitly
check both lint and format (lint success is not formatting proof). Add only the
registered Library `l.open_count.v1` unchanged metric path and an independent
successful count-only Library fixture, because the original whitelist omitted it.
Do not broaden grade semantics or add compatibility fallback. Strengthen the future
manual two-file acceptance gate below; do not apply correction to original data.
Rerun focused tests, lint, format, strict source mypy and compile checks; refresh
only this development receipt and source hashes. Root owns independent re-review.

## Mandatory future paired-output acceptance gate (manual, root owned)

The frozen harness does **not** validate the correction manifest. No automatic
activation helper exists in this scoped repair. The root must not supply new
records to any downstream scorer unless separately authorized and all of these
manual gates have passed and been receipted:

1. Retain the corrector's exact command and **successful exit status 0**. Merely
   finding output files does not prove successful or complete publication.
2. Both new files must exist and parse completely as strict JSON (reject duplicate
   keys and nonfinite values). The manifest must be a closed object with exactly
   `version`, `source_version`, `frozen_observer_sha256`,
   `correction_source_sha256`, `source_receipt_sha256`, `input_sha256`,
   `output_sha256`, `artifacts`, `changes`, `scope`; compare exact version/source
   identities to the independently reviewed correction and frozen v1.
3. Rehash the complete new output, original v1 input, reviewed correction source,
   reviewed source receipt, frozen observer and **every** referenced original
   campaign artifact. Each SHA256 must agree with the approved receipt/manifest;
   compare the receipt's closed artifact map to the manifest's full map. Missing,
   unknown, escaping, drifting or incomplete references block acceptance.
4. Independently verify the full-record delta is exactly the disclosed manifest
   changes: scalar contract-owned mean type only, never values, scope, choices,
   dependencies, checks, identity, status, denominator or original evidence. Record
   independent review approval. No emitted manifest authenticates its own inputs.

A missing, truncated, malformed, partial or unverified manifest blocks this gate
**even if** the new record JSON parses or the frozen harness would accept it.
An interrupted/failed CLI likewise blocks the gate even if both files exist.
This is a required manual protocol, not a claim of automated activation enforcement
or tested crash-atomic publication. There is no downstream scoring in development.

Independent-review correction: `src/universitydb/library.py` explicitly registers
`l.open_count.v1`; it is now an allowlisted unchanged path, backed by a synthetic
successful Library count/zero regression. No Library grade interpretation or
nullable mean label is introduced. Original source hashes and prior failed style
checks remain historical evidence, not silently described as passing.
