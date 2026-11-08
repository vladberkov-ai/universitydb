# H-015 final artifact/code review

## Review status — original frozen observer

**Recommendation: REQUEST CHANGES.** One confirmed HIGH instrumentation defect
prevents unqualified valid-scoring/technical-completion approval at this cutoff.
Live collection itself is complete and retained; product quality is **not passed**.
This section is preserved if an independently reviewed offline correction follows.

### [HIGH] Computed mean nullability is inferred from observed cells

File: `tools/eval/observe.py:109–118` (frozen candidate `ecb7f5c`).
The original raw ResultSpec lists integer aggregate components, not the derived
`average` column. The observer therefore labels that computed decimal nullable
only when the current rows contain NULL. Schema nullability is a capability of
the registered derived metric, not a property inferred from this sample's cells.
The fixed H014 oracle declares the scalar mean `decimal?` for A01/A02/C01/C03
(`heldout-candidate-v1.json:301,326,640,706`). Both repeats of these four cases have
matching projected columns/rows/reasons but are misrepresented as `decimal`, causing
eight false-negative strict comparisons. C02's two actual NULL results retain
`decimal?` and match. This is an **observer representation defect**, not evidence
that eight product values or scopes were semantically wrong.

Independent read-only reproduction called only the frozen pure `project` helper
on retained originals and compared its fields: the eight differences are exactly
`types:[decimal,integer,integer]` versus `[decimal?,integer,integer]`.
`tests/test_h015_observer.py:93–95` locks the incorrect row-inference convention;
`observer-design.md:62–63` documents it, but documentation does not repair the
mismatch with the existing fixed typed oracle contract. The prelive reviewer
missed this defect; prior APPROVE history is retained, not rewritten as if caught.

Fix: derive the nullable representation of registered computed means from explicit
metric/schema semantics, independently of oracle expected values and sample cells.
Preserve original source, records, annotations and strict v1 score. A minimal,
append-only, explicitly post-results offline observer-v2 correction over the **same
immutable artifacts**, backed by independent non-NULL/NULL/empty/schema tests and
review, is the recommended repair. Do not replace the frozen score, alter rubric,
regenerate any question, run a paid retry or silently present corrected analysis
as prospective v1 evidence. Root owns the authorized repair boundary and lifecycle;
this reviewer does not implement or grant new execution authority.

## Original collection verification completed

Reviewer performed read-only stdlib/SQLite artifact checks, not provider/application
execution, lifecycle operations or monetary mutations. All427 original collection
files match the closeout hash map, with no missing/extra files. All68 active freeze
entries still match; HEAD remains `ecb7f5c81c705d970dc64adb910ed2a5020cb28b`.
The active registration is the reviewed v2 metadata; original48 questions,
selections, repeat-major order and fixture descriptors remain unchanged.

All48 original runs have distinct same-run sequential terminal traces, final
exchange events equal original JSONL and intermediate exchange traces are prefixes.
Each fixture's before/after bytes and census match; actual DB hash/census,
DELETE journal and read-only integrity check pass. Results:10 `ok`,38 honest
`INVALID_INPUT` errors at scope resolution, no hidden successes or discarded
failures. No M1/top/count/Library success is inferred from failed requests.

There are exactly20 application attempts,20 reservation IDs,20 safe full-wire
requests,20 known responses and10 SQL executions. Each returned exact
`gpt-6.1-sol`/`default`; plan high and SQL medium; no repair was needed. Requests
use the closed reviewed wire shape, explicit store=false,32768output and the
full-wire12000estimate gate. Usage totals38858input/5808output agree with raw SDK
metadata. Provider evidence IDs equal exactly the20 new monetary entries.

Direct read-only monetary inspection confirms original14 entry values equal the
retained historical source, and all34 entries have known usage with stop=null.
Aggregate retained effective/reservedUSD14.499232 includes oldUSD5.970272 and
newUSD8.528960. Observed conservative totalUSD0.4424530 includes newUSD0.2776070.
Dispatch headroomUSD95.500768; contingencyUSD10 untouched. No raw ledger or backup
content/path is exported in this review.

All40 provider JSON files were parsed and their closed request shapes/assembled
inputs reviewed: original questions, known domain descriptor, scope, accepted step,
refs, diagnostics and counters only. No oracle, expected answer, fixture/case/run
metadata, credential/header/environment field was observed in model payloads.
A bounded suspicious-key/value scan was also clean; the scan is supplementary,
not claimed as a universal secret detector. Response bodies contain actual model
output and provider metadata, not fabricated evidence. No evidence of an extra
probe/count/smoke/evaluator rerun/paid UI generation or fallback appears in the
20-ID authoritative account sequence and original48 artifact set.

## Scoring/checks cutoff

Original observation artifacts now exist and strict v1 score is2/48, with
critical_failures0, mandatory_failures38 and threshold=false. Eight additional
raw successful product results are affected by the observer defect above;10
product `ok` envelopes are **not** a replacement registered score. Final review of
all hash-bound independent annotations and any disclosed corrected analysis is
pending at this section's cutoff. Quality fails regardless of the eight type-only
false negatives because38 original conversations remain product failures.

## Independent annotation corroboration — same original-data cutoff

All48 run-keyed independent review records were read. Every one of1088 attestation
artifact references was rehashed and its run/status note checked. Annotation
truth was then corroborated against originals, not inferred from hashes:

- safe/private/trace_complete/nonfabricated:48true each, supported by unchanged
  DBs, read-only validated SELECTs or predispatch errors, original full-wire
  payloads, same-run terminal traces and honest answer/error provenance.
- scope_explicit/behavior_complete:10true each and38false each. Predispatch
  scope-resolution failures correctly retain missing mandatory evidence rather
  than treating an error response as proof of the requested domain behavior.
- On all10 successes, original db_result equals retained raw step data; adapted
  events equal retained adapted steps and final/compiled answers. Exact component
  arithmetic, NULL/no_grades reasons and bound scope match. All six actual
  clarification continuations use prescribed selections, no prechoice SQL, original
  run and retained server choices. No M1 intermediate values are guessed.
- Retained historical source bytes' SHA256 independently equals the original
  frozen baseline; original14 entries and all20 known new attempt IDs are intact.

Original strict score is confirmed **2/48**, category passesA0/J0/D0/C2/E0/L0,
critical failures0, mandatory failures38; all48 remain denominator members.
Raw product envelopes are10ok/38error. Eight type-only observer false negatives
remain a separate instrument defect, not a license to claim the official score10.
No safety/privacy/fabricated-success finding was observed in the actual originals.
This is bounded artifact evidence, not universal security proof or product acceptance.

## Code Review Summary — current final-review recommendation

**Files Reviewed:** the10 previously scoped Python files; all427 original collection
artifacts; frozen protocol/scorer/registration and48 observation/annotation records.
**Total Issues:** 1 unresolved.

### By Severity

- CRITICAL:0
- HIGH:1 — computed-mean nullability instrumentation defect (`observe.py:109–118`).
- MEDIUM:0
- LOW:0

### Recommendation

**REQUEST CHANGES** for valid observation/scoring closeout. Collection/accounting
retention checks are clear; source576-test/static/157-oracle evidence remains
unchanged, but does not test away the actual representation defect. Preserve the
frozen experiment and repair/validate only the offline instrument in an append-only
version before requesting corrected-assessment approval. No paid repetition is
needed or authorized. Without correction, any closeout must explicitly be limited
to frozen instrument output and cannot claim fully valid semantic measurement.
Product quality is not passed under either possible tally; final owner acceptance,
publication and defense remain separate. Native lifecycle completion is root-owned
and is not certified by this review.
