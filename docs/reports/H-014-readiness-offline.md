# H-014 v2 — offline readiness report

**WIP checkpoint — final clean-run, browser, independent reviews and native closeout pending.**
This is the bounded I4 + verification-I5 **offline** readiness task, not full live
acceptance, publication or owner defense. No live generation/access/count calls,
credential loading, monetary ledger/cap/hold changes, push or vault writes are
permitted. Accepted ADR-CHAT-006 semantics and Sol high/medium/medium are unchanged.

## Identity and checkpoints

- Published starting main/origin/main: `6cc7ad3af426d0da6818281b035c5e683806f357`.
- Historical H-013 product tested SHA: `f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0`,
  410 offline tests / 157 oracle, COMPLETE / strict PASS13/13. The publication
  checkpoint's 59 targeted E2E checks were not another full product run.
- CP-R1 audit/baseline: `8a9cd5d` (initial REQUEST CHANGES, not final approval).
- Scoped repair: `dc715201c32585b4845456cf7f6a115cd04ac278`.
- CP-R2 frozen tracked-only candidate: **`331eb5a61648bccb7fa66eecb58d9cc284eda2a0`**.
  The first final clean attempt passed457tests/static92.09s but readiness E2E
  found a new regression: `Show mean grade grouped by course across all enrollments`
  returned INVALID_INPUT before provider dispatch. Candidate **not accepted**;
  preserved failed attempt and new scoped repair/re-freeze/full rerun are required.
- Later evidence/documentation commits are not newly full-tested product identities.

## Independent audit and repair

[Initial independent audit](../operations/H-014/reviews/cp-r1-code-audit.md) found
unknown named targets disappearing into global/all scope in both domains. The
[pre-fix regressions](../operations/H-014/scope-fix/pre-fix-pytest.txt) failed twice
with two known controls passing. The scoped adapter-owned guard repair and 14
regressions reject unknown supported targets before provider dispatch, with terminal
trace and no fabricated success. [ADR013](../adr/ADR-OMX-013-readiness-scope-boundary.md)
records alternatives and the bounded language limitation; no universal NL claim.

## Clean-run and evidence cutoff

**New blocking evidence:** first corrected-candidate331eb5a clean run passed
457tests/static92.09s, then fresh readiness E2E rejected
`Show mean grade grouped by course across all enrollments` with INVALID_INPUT and
zero provider calls. The baseline6cc runner had passed this case. Candidate is **not
accepted**, not waived by457tests; preserve the failed attempt, add a failing
regression, minimally repair/re-freeze and rerun full clean gates. Root/repair lane
own this continuation; final reviews/native completion remain pending.


[Verifier scope](../operations/H-014/clean-run-scope.md),
[environment](../operations/H-014/clean-run-environment.json) and
[browser toolchain](../operations/H-014/clean-run-browser-toolchain.json) describe
a tracked-only disposable local clone, frozen `uv.lock`, new venv and isolated
DB/runtime/cache, never a second canonical repository. Initial sandbox registry DNS
failed; supported escalated retry succeeded. Partial retry caches/provisioned browser
binaries are disclosed, not represented as all-fresh download proof.
Initial clean baseline at6cc7ad3 separately passed410tests/static/157oracle and both
DB init/safe repeat refusal: [receipt](../operations/H-014/clean-run-initial/receipt.json).
That is a real fresh baseline run, not final corrected candidate acceptance.
Final candidate regression/static/oracle/repeat-init/compiled-graph/browser receipts,
screenshots, same-run trace and owned process cleanup are **pending**.
CP-R2 candidate checks passed: Ruff format/check for five scripts/tests, 33 synthetic
eval harness tests, cached diff check. Those 33 tests are not live model accuracy.

## Proposed live decision package — no execution

[Protocol](../plans/H-014-live-eval-protocol.md),
[budget](../plans/H-014-live-eval-budget.md),
[manifest](../operations/H-014/eval/package-manifest.json) and
[planned runs](../operations/H-014/eval/planned-runs-v1.json) define 24 held-out
candidate cases, six categories × four cases × two repeats = 48 conversations;
maximum 240 generation calls, separate optional six-conversation smoke maximum30.
No evaluator-level reruns/best-of: existing one shared transient provider retry
and bounded SQL repair are internal attempts charged within the same run ceiling.
All48 are **not-run**. Scorer validation uses synthetic/dev fixtures only. Held-out
exposure is disclosed in protocol; do not claim an unseen sealed dataset. Questions
are separated from oracle answers, failures stay in denominator, no best-of/retry
selection. Proposed44/48 overall and≥7/8/category plus zero unsafe/privacy/fabricated
success and100%mandatory behaviors are **not accepted**. Fresh exact-model Standard official research independently establishes conditional
5.50/11short-envelope R=USD0.426448; full240reserveUSD102.347520 plus retained
H5.970272. Proposed aggregate choices: smoke C22/D20/contingency2; full C120/D110/10
(recommended full evidence); separate smoke+full C140/D125/15. These are not authority
or invoice guarantees; scenarios and tier/tax/account uncertainty are explicit. Future
history-preserving approval/migration is required; no cap migration is applied.

## Requirement and invariant audit

| Requirement | Current evidence / remaining gate |
|---|---|
| R01/R02/R11 | University+Library schema/seed and typed data/integrity; final clean init/repeat-init/hash receipts pending |
| R03 | Real compiled LangGraph→SQLite→formatter; offline injected provider only, broad real NL quality not-run |
| R04 | All16filter scopes, five group grains, three count objects, NULL≠zero, exact ties, all-semester equal enrollment weights; M1 actual typed result bindings; clean regression/trace pending |
| R05 | Library unit1/zero/schema isolation on same core; clean/browser proof pending |
| R06 | Ordered same-run nodes/SQL/bindings/raw/adapted rows/answer-or-error trace; fresh browser proof pending |
| R07 | Grounded ambiguity, session-bound expiry/conflict/replay, bounded repair, corruption/safety/provider/accounting failures; named-target regression repaired |
| R08 | Full offline/static/oracle/AppTest/browser gates pending; eval harness33PASS does not replace live48 |
| R09 | Existing adapter/core separation; independent final review pending |
| R10 | [Production boundaries](../plans/production-considerations.md), not production-ready |
| R12/R13/R14 | Tracked code/tests/ADR/prompts/examples and exact candidate receipts, final links/evidence audit pending |
| R15 | Previously published baseline remains; new publication awaiting separate authority, push not-run |
| R16/R17 | Offline working/debuggable evidence under verification; owner explanation/defense deferred |
| U01 | Actual root task and bounded child projections; RU original / EN reader translation, no full hidden transcript claim |
| U02 | Exact deadline/timezone remains unknown, not invented |
| U03 | Root-owned supported current-native-owner binding and separate H014 workflow; completed I1/H013 not resumed |
| U04 | ADR013 scoped repair rationale, existing accepted semantics unchanged; eval thresholds/budget proposed |
| U05 | Vault read-only; original results/ledger/locks preserved, final hash comparison pending |
| U06 | Explicit-path local CP commits; no amend/reset/blanket staging/push; fresh remote check pending |

Preserve DAG≤3,≤5generation calls/run,≤4SQL attempts,180s active,60/45s calls,
32768output; checkpoint≤2pauses/900s,in-process only; read-only validated SQL and
DELETE-only DB mode. Typed dependency values never become SQL fragments. Runtime
prompt hashes and locked dependencies remain unchanged. Final independent invariant
proof is pending, not inferred from count of tests or historical H013 verdicts.

## Provenance, preservation and privacy

[Actual received task](../ai/omx/H-014-actual-prompt.txt) and
[prompt receipt](../operations/H-014/prompt-receipt.json) preserve the received root
wording with private vault-prefix redaction only; the H014v2 handoff/listed inputs are
read context, not substituted prompts. [Baseline](../operations/H-014/baseline.json)
records source and preservation hashes, including monetary ledger
`2753fe2fdf1dc366ffecdb5a86dcd9cf184d83707a00da0de62a8a4e4963f125`.
Original H013 results/failed attempts, completed I1/H013 workflows and untracked locks
are not rewritten. Final fresh preservation/remote receipt is pending.

Privacy caveat: the initial local CP-R1 commit preserved a nonsecret private
vault-prefix in a delegated-task projection before root redaction arrived. The next
repair commit corrects current public text to `<PRIVATE_VAULT>`; no history rewrite
or history-wide private-path-absence claim. Future publication needs its own review.
Credentials were not loaded; no secrets belong in public evidence.

## Final gates / not-run

Final independent code-reviewer and architect verdicts: **pending**, not reused from
H013. Cleaner/diff/link/public-doc audit and final native COMPLETE/strict: pending,
root-owned. Live/API/count/access/credential loading/monetary mutation/push and owner
defense: **not-run**. Missing live/push authority does not block this bounded offline
DoD, but this WIP cutoff has not yet achieved that DoD.
