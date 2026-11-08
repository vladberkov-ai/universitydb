# H-015 observer-v2 correction-preparation code review

## Scope and authority

Independent G005 **development/future-readiness** review only. Reviewed the complete
new `tools/eval/correct_mean_nullability_v2.py`,
`tests/test_h015_observer_v2.py`, correction design and development test receipt.
No actual campaign, oracle, original observation/score or monetary file was opened
or processed in this review turn. No product/frozen source, lifecycle, credentials,
ledger or Git operations were performed. Reviewer owns only this review artifact.
Actual-data application/reanalysis remains gated on the owner's clarification.

The original final-assessment HIGH remains open in
[final-code-review.md](final-code-review.md); reviewing preparation does not resolve
it, replace strict v1 score2/48, authorize actual reanalysis or accept product quality.

## Initial preparation review

Source SHA256:
`83df73f72cc49bb992d4d4eb462bd1cdf97ded32a599036d2b4a60e3abc9f636`.
Tests SHA256:
`317ed4bebb2075fa6b3c1c692eb87f62bbb2ae8405f4a6aafc9323b3790d5eca`.
These initial identities are retained if the author applies a formatting-only fix.

### Specification/security/correctness checks

- Stdlib-only postprocessor; no product/provider/oracle/scorer/frozen-observer
  import, duplication or monkeypatch. No question generation, paid retry, scoring,
  threshold adjustment or numeric recalculation is reachable from its CLI.
- Explicit scalar `u.grade_mean.v1` raw contract owns nullable derived-mean
  representation. Exact strict JSON spec comparison rejects bool/int coercion;
  grouped/other recognized metrics are not changed. Sample NULL presence is used
  only to verify the original v1 projection, never to decide corrected nullability.
- Copy-and-delta changes only applicable `/observed/types/<index>` decimal→decimal?.
  Rows, scalar values, NULL/reasons, choices, dependencies, outcomes and all six
  checks remain unchanged, including false checks and ordinary error records.
- A closed externally reviewed receipt binds v1 records and every consumed
  completed/state/exchanges/original-trace artifact. Unknown/unconsumed/missing/
  escaping paths and hash drift reject. Source identity assertions are provenance,
  not authentication of owner authority or reviewer independence; docs say so.
- Correction requires retained scalar contract, actual raw/adapted/answer event,
  state and projected-row agreement. Exclusive new output/manifest creation cannot
  overwrite originals, input records or receipt, and rejects campaign-contained
  output. Failures are explicit, not silent defaults or fallback scoring paths.
- Two-file crash atomicity is not claimed. A partial new pair is explicitly invalid
  evidence and must not be consumed; input preservation does not depend on success.

No functional/security blocker found in the bounded synthetic correction source.

### Initial diagnostic gap

**[LOW] Repository formatting gate fails on both new Python files.**
Files: `tools/eval/correct_mean_nullability_v2.py:79` and
`tests/test_h015_observer_v2.py:33` (representative first diagnostics).
Fresh `ruff format --check --no-cache` reports **2 files would be reformatted**.
The preparation receipt records lint/type/compile but does not establish the
repository's formatting gate. Fix only the two new files with the installed
formatter and refresh exact source/test/design receipt identities; do not edit v1.
Root informed before final preparation verdict. This is a concrete validation gap,
not a semantic regression or reason to broaden the correction.

### Reviewer-owned fresh evidence

- Ruff lint on both new files: **PASS**.
- Strict mypy with isolated `/tmp` cache on the correction source: **PASS1file**.
- Synthetic correction tests only: **33passed0.15s** (no actual-data application).
- Formatting: **FAIL** as preserved above; author follow-up pending.
- `git diff --check`: clean.

No full suite/DB tests were run by reviewer concurrently with root's full run.
Root owns separate full/static integration and architecture review. Preparation
approval is pending the formatting/identity follow-up only; actual application
and original valid-assessment closure remain separately gated.

## Corrected preparation follow-up — final future-fix-readiness verdict

The author formatted only the two new Python files, refreshed development receipt
identities, added explicit identity-only passthrough for registered Library
`l.open_count.v1` with a successful count/zero synthetic regression, and documented
mandatory paired-output acceptance. Original v1 source/records/score are not changed.
The initial LOW formatting finding is **resolved**, not waived; its history above
remains intact.

### Final reviewed identities

- Corrector: `8560fcb2c7458ab778dbac1d55530f8b634561727f74281b4809c53bf6389908`.
- Synthetic tests: `ac296b2ff5ea1815e9fc4a3aad9ea3af4c9ff050d7db914ee310aca21f71dbc0`.
- Design: `138d125907fd1212419facad2567f8d476144f8001ae067ad206542e40504f53`.
- Development receipt: `6ce527175a625d48a26272480e8330cc1bc10b2597ba238e2b87e49c799833a0`.

Reviewer independently rehashed all four identities and re-inspected the changes.
The Library path returns unchanged records, never interprets counts as grades.
Manual acceptance now explicitly requires separately authorized successful CLI
exit, strict complete closed manifest, all input/output/source/receipt/original
hashes, exact disclosed type-only full-record delta and independent review before
any downstream use. Partial files do not pass merely because the frozen scorer
would parse records. This is a documented manual gate, not claimed automated
activation enforcement or crash-atomic two-file publication.

### Fresh independent diagnostics — final preparation files

- Ruff `check --no-cache` on both files: **PASS**.
- Ruff `format --check --no-cache` on both files: **2 already formatted / PASS**.
- Strict mypy, isolated `/tmp` cache, corrector `--follow-imports=skip`: **PASS1file**.
- New synthetic tests only: **34passed0.17s**. No actual campaign/oracle/application
  or scoring execution was involved. Author separately reports72focused tests
  (38existing observer plus34new); root owns full-suite integration evidence.

The earlier root609-test full pass and two-file formatting failure are historical
validation, not claimed as a fresh final-source full run. No full suite/DB/browser
rerun was initiated by reviewer.

## Code Review Summary — preparation only

**Files Reviewed:**4 (new correction source/tests/design/development receipt).
**Total Issues:**0 unresolved;1initial LOW formatting issue resolved.

### By Severity — preparation scope

- CRITICAL:0
- HIGH:0
- MEDIUM:0
- LOW:0

### Recommendation

**APPROVE — future offline correction-preparation readiness only.**

Specification compliance, root-cause guard, security/input confinement, strict
contract projection, preservation and modified-file diagnostics are addressed.
This is a narrow explicit representation repair, not a fallback answer path or
relaxed grader. No numeric answer/check/outcome/denominator adjustment is introduced.

**The original actual-assessment HIGH/REQUEST CHANGES remains open.** No actual48
correction/reanalysis/scoring is authorized or performed by this approval; it must
wait for owner clarification and root's separately receipted acceptance gates.
No replacement score, quality pass, native completion, publication or owner
acceptance follows. Root owns separate architecture/gate synthesis and integration.

## Separate bounded report-honesty note

Root also invited final-document honesty review. Current report correctly preserves
original2/48 instrument output,38product failures, openHIGH, no corrected tally and
no native-completion/acceptance claim. One MEDIUM attribution overclaim was reported
to root: the paragraph saying both reviewers directly checked12nonmonetary targets
and688history files exceeds this lane's evidence. This lane directly checked427
collection/68freeze/monetary/1088annotation references, but attributed those larger
preservation scans to root receipts. Root should repair that attribution; this note
is separate from the four-file correction-preparation approval above.

## Narrow final documentation/receipt verification

The separate MEDIUM report-attribution concern is **resolved**. The current report's
live-cutoff paragraph now explicitly distinguishes this reviewer's direct427
collection/68freeze/monetary/1088annotation-reference checks from root's direct
12nonmonetary/688historical preservation scan. Root's
`postresults-preservation.json` attributes its own427/688/12/4v1-observation and
monetary verification correctly; this reviewer does not claim to have reproduced
that root scan in this narrow follow-up.

Read `postresults-verification.json`: root now records a fresh final-development
**610passed146.05s**, Ruff/format43/strict mypy14+1/compile/diff PASS. The earlier
609pass→two-file format failure remains separate history. These are attributed
fresh root results, not reviewer-launched tests or actual-data reanalysis.
Read-only HEAD is `f61c0128f3b1f229e4a78e0d3c8908d8b9c928d1`; reviewed correction
and test hashes remain exactly8560fcb2…/ac296b2f… above. No Git mutation was performed.

Report score/cost/state boundaries remain honest: qualified original2/48,38real
product failures, eight type-only false negatives, retainedUSD14.499232 and new
observedUSD0.2776070; no replacement score, actual correction, push, acceptance or
native COMPLETE/strict claim. Root receipt records actual nativeACTIVE,
G004review_blocked/G005in_progress: a supported blocked-checkpoint request was
rejected before process creation and not retried or bypassed. No successful
blocked transition is inferred. At this read cutoff the report still labels the
latest full run pending; root was informed to refresh that draft sentence to the
new610receipt while preserving old validation history. Writer owns those edits.

Future-preparation **APPROVE** is unchanged. Original actual-assessment
**HIGH/REQUEST CHANGES remains OPEN**, with actual reanalysis awaiting owner
clarification. This note adds no application/scoring/lifecycle authority and does
not modify or supersede the frozen final-assessment review.
