# H-014 v2 — offline readiness report

**WIP — c631 mechanical checks PASS, but independent visual review BLOCK; candidate not accepted.**
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
- CP-R2 rejected tracked-only candidate: `331eb5a61648bccb7fa66eecb58d9cc284eda2a0`.
  The first final clean attempt passed457tests/static92.09s but readiness E2E
  found a new regression: `Show mean grade grouped by course across all enrollments`
  returned INVALID_INPUT before provider dispatch. Candidate **not accepted**;
  failed attempt preserved; subsequent c631repair is frozen, full rerun pending.
- Current frozen product/harness candidate: **`c631c0c62bebd7c291429e26783dbfc442bde3af`**.
  Repair preserves registered group/exclusion/all-five-axis/count prose and Library
  each/every forms while keeping bare unknown names fail-closed. Final focused39
  passed6.94s; independent code-reviewer focused39passed76.72s and scoped static
  checks passed. These are not the final full regression or a final verdict.
  Serialized fresh full clean/browser verification now PASSED:482tests92.83s,
  all seven pipeline commands exit0,157oracle, six browser classes/seven captures.
  Independent architect visual review subsequently BLOCKED c631: Streamlit
  DeltaGenerator help dump/noise in success DB panel and None in error panel.
  Minimal UI repair/regression/new freeze/full clean/browser rerun required.
- WIP docs checkpoints: `cd5a9493c81715bc9e59186ffb23279c683a1ff6`,
  `6c50a4fac369c2958046512d3de2ba840e95d9b5`,
  `91277b9cf0c9fee8419b29212f5040084e67f915`.
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
accepted**, not waived by457tests. Failing regressions and the subsequent c631c0c
repair now address that regression; corrected-candidate c631clean/browser proof has now passed; final reviews and
native completion remain pending.
[Rejected clean attempt](../operations/H-014/clean-run-final-attempt1/receipt.json)
and [failure summary](../operations/H-014/clean-run-final-attempt1/attempt-status.json)
retain actual command exits, init hashes and failure trace. Independent
[interim architect BLOCK](../operations/H-014/reviews/interim-architect.json) also
identified the Library each/every regression; this is not a final verdict.

Historical331browser attempt1 failed socket permission:
[command](../operations/H-014/browser/candidate331-attempt1-command.txt).
Supported retry attempt2 passed seven captures across six classes:
[receipt](../operations/H-014/browser/candidate331-attempt2/browser-receipt.json),
[same-run M1 trace](../operations/H-014/browser/candidate331-attempt2/m1.jsonl).
Those screenshots/traces remain **rejected331candidate evidence**, not final c631
browser proof; a browser pass did not waive the separate E2E blocker.


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
Final c631mechanical checks passed, but visual readiness is **BLOCKED**:
[clean receipt](../operations/H-014/clean-run-final-attempt2/receipt.json),
[browser receipt](../operations/H-014/browser/final-c631-attempt1/browser-receipt.json),
[preservation/remote](../operations/H-014/final-preservation-remote.json).
The serialized pipeline passed482tests92.83s, Ruff check/format, strict mypy,
compileall, readiness E2E and157 independent oracle checks; all seven command exits0.
Both DBs initialized with recorded seed/resource/row hashes; repeat init refused
without mutation. Fresh compiled graph proved group/top, M1 F1/F2/tie actual refs,
same-run clarification/resume/replay and Library same-core portability. Actual
browser passed six classes/seven captures with SQL/bindings/raw/adapted rows/full
same-run JSONL: success, clarification pause/resume, M1, Library, repair, terminal
error/no stale answer. Root inspected M1 adapted95.00, Ada1/Bob1 and error no SQL.
The28clean-manifest and53browser-manifest hashes were verified; owned server/browser
stopped, temporary runtime ledger absent, disposable tracked checkout clean.
These are fresh **c631** artifacts, not relabeled331 or H013 captures.

Independent architect visual inspection found `success-db.png` dominated by
Streamlit DeltaGenerator API help and `error-db.png` showing None. Root confirmed
bare ternary expressions around `st.json`/`st.write` in `ui.py` trigger Streamlit
magic return-value rendering. Captures/automated checks did not prove a clean UI:
**c631 is not accepted**. Preserve original screenshots; minimally repair explicit
if/else rendering, lock behavior with AppTest/browser regression, freeze a new
candidate and rerun full clean/browser gates. No global magic-disable or screenshot
masking; no source edit in this documentation lane. Final CLEAR/APPROVE/native
completion are not claimed.
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
| R01/R02/R11 | University+Library schema/seed and typed data/integrity; clean init/repeat-init/hash receipts PASS |
| R03 | Real compiled LangGraph→SQLite→formatter; offline injected provider only, broad real NL quality not-run |
| R04 | All16filter scopes, five group grains, three count objects, NULL≠zero, exact ties, all-semester equal enrollment weights; M1 actual typed result bindings; clean regression/trace PASS |
| R05 | Library unit1/zero/schema isolation on same core; clean/browser mechanical PASS; visual UI BLOCK |
| R06 | Ordered same-run nodes/SQL/bindings/raw/adapted rows/answer-or-error trace; mechanical browser checks PASS, visual architect BLOCK |
| R07 | Grounded ambiguity, session-bound expiry/conflict/replay, bounded repair, corruption/safety/provider/accounting failures; named-target regression repaired |
| R08 | 482offline/static/157oracle/AppTest/mechanical browser PASS; visual UI BLOCK; eval harness33PASS does not replace live48 |
| R09 | Existing adapter/core separation; independent final review pending |
| R10 | [Production boundaries](../plans/production-considerations.md), not production-ready |
| R12/R13/R14 | Tracked code/tests/ADR/prompts/examples and exact candidate receipts, final links/evidence audit pending |
| R15 | Previously published baseline remains; new publication awaiting separate authority, push not-run |
| R16/R17 | Offline working/debuggable evidence under verification; owner explanation/defense deferred |
| U01 | Actual root task and bounded child projections; RU original / EN reader translation, no full hidden transcript claim |
| U02 | Exact deadline/timezone remains unknown, not invented |
| U03 | Root-owned supported current-native-owner binding and separate H014 workflow; completed I1/H013 not resumed |
| U04 | ADR013 scoped repair rationale, existing accepted semantics unchanged; eval thresholds/budget proposed |
| U05 | Vault read-only; original results/ledger/locks preservation hashes verified |
| U06 | Explicit-path local CP commits; no amend/reset/blanket staging/push; fresh remote6cc7ad3 verified, push not-run |

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
Original H013 results/failed attempts and untracked locks are retained. [Final fresh preservation/remote receipt](../operations/H-014/final-preservation-remote.json)
verifies44source paths against c631Git blobs,263H013historical files,22vault inputs
and10preservation targets unchanged/restored. Fresh read-only ls-remote exit0 observes
origin/main6cc7ad3af426d0da6818281b035c5e683806f357; local work is not published. Root disclosed a transient orchestration
incident rather than asserting zero historical workflow writes:
[recovery receipt](../operations/H-014/orchestration-recovery.json),
[redacted rejected-event projection](../operations/H-014/rejected-wrong-cwd-steering-event.json).
One supported annotate_ledger command ran from the wrong canonical cwd: it rejected
completed I1 steering but appended one steering_rejected audit event. Under specific
supported permission, root verified the original31-record prefix and archived only
its own new rejected record, then removed only that append to restore original
ledger SHA256`980675a8f5b3a288809d7c98c3fb539ba1d51e43a6beb64dfb30d85c09d1e380`.
No original record, goal/brief/ID/pointer/lock or native goal state changed; monetary
ledger never changed. This is disclosed recovery, not a completed-I1 resume or
silent history rewrite. The correct annotation subsequently succeeded only inside
the new H014 workflow, reasserting the same seven invariant lines because the
original generic heading was not recognized by strict extraction; original brief
remains unchanged.

Privacy caveat: the initial local CP-R1 commit preserved a nonsecret private
vault-prefix in a delegated-task projection before root redaction arrived. The next
repair commit corrects current public text to `<PRIVATE_VAULT>`; no history rewrite
or history-wide private-path-absence claim. Future publication needs its own review.
Credentials were not loaded; no secrets belong in public evidence.

## Final gates / not-run

Final independent code-reviewer and architect verdicts: **pending**, not reused from
H013. Cleaner/final invariant/doc synthesis and final native COMPLETE/strict: pending,
root-owned. Live/API/count/access/credential loading/monetary mutation/push and owner
defense: **not-run**. Missing live/push authority does not block this bounded offline
DoD, but final independent approvals/native postconditions are still pending at this cutoff.
