# H-009 — practical budget policy, existing I1/G004

2026-11-07. **Offline policy implemented, checked and independently approved for partial checkpoint. I1 incomplete, live not run.**

## Authority, preservation and implementation

H-009 and accepted private ADR-CHAT-005 / CHAT-034 authorize explicit practical policy: one total USD10 for all I1 continuation attempts, USD8 new-dispatch threshold, USD2 contingency not automatically spendable. Residual invoice uncertainty accepted; this is not the former strict billing proof. No count endpoint and no flag pretending that proof succeeded. Exact Sol/default tier/plan high/SQL-repair medium preserved. [ADR010](../adr/ADR-OMX-010-I1-practical-budget-policy.md) records alternatives/rationale/consequences.

Actual baseline HEAD `f8203073bc1534a5dc4bb6acf4e5c156e5b388aa`, tracked/index clean before edits; [baseline](../operations/H-009/baseline.json) protects234 tracked docs/wiki files and11 existing untracked files including locks/receipts. [H-009 inputs](../operations/H-009/input-hashes.json):3/3 hashes match. H007/H008 hashes stay historical, not reimposed on changed files. A/B, all descendant commits, receipts and closed Advisory remain preserved. No vault writes, reset/clean/amend, remote/push or OMX update.

Product implementation is complete for this offline policy slice, using the existing provider/config/ledger/worker pattern, not a new budget system. The practical gate estimates complete wire JSON plus framing; atomic shared reservations retain historical holds and stop on uncertain/anomalous usage/model/tier before another dispatch. Full payload/output/time/call limits stay. The version1 pinned monetary profile and prior attempt entries remain unchanged; practical metadata/stop additions are tested, with legacy uncertain holds failing closed. No new dependency or runtime prompt change.

## Runtime / current blocker

Root's actual initial `get_goal` reports the same aggregate native goal **blocked**. Supported `complete-goals` resumes existing G004 attempt1 in OMX, **not the native goal**. G001–G003 remain complete and were not rerun. Supported ledger annotation records H009's replacement policy and independent offline authority. One phase/HUD write attempt returned `canonical mode binding lease helper exited (0)`; no repair/retry/manual IDs/state. This persistence gap is distinct from product checks and is not a new billing blocker. Configured code-review custom gates are empty (`gates: []`); independent reviewer/architect remain required.

After passing offline checks and local checkpoint, if fresh root snapshot remains blocked, the single exact owner step is **`/goal resume` in the composer of this same Codex session**. No active API, replacement goal or repeated identical check. Live requires fresh actual same-goal active; no paid/API/count/access probe or application launch was performed at this cutoff.

## Verification / review / commits

- [Implementation validation](../operations/H-009/implementation-validation.json): **131 tests passed in10.76s**, Ruff lint/format19files, mypy11sources, compileall and diff-check passed; exact8changed application/env/test hashes recorded.
- [Root-attributed fresh verification](../operations/H-009/root-verification-receipt.json): **131 tests passed in10.65s**, Ruff/format/mypy/compile/diff-check passed independently of the author run.
- [Red-first regression evidence](../operations/H-009/regression-receipt.json), [pre-edit cleanup plan](../operations/H-009/cleanup-plan.md), [bounded cleaner report](../operations/H-009/cleaner-report.md): baseline108 green, initial4 new failures then corrected, expanded practical-policy coverage.
- Independent architect: **CLEAR for H009 offline partial only**, no blocking findings; [actual root-relayed receipt](../operations/H-009/reviews/architecture-review-receipt.json),8 hashes/diff independently checked. Code-reviewer **APPROVE for offline partial only**,0issues/22files; [actual root-relayed receipt](../operations/H-009/reviews/code-review-receipt.json), fresh59targeted tests passed2.80s plus Ruff/diff. Optional reviewer isolated-cache mypy interrupted exit130 (not pass); author/root mypy passed separately. Combined offline verdict **APPROVE + CLEAR**; configured gates[]. No implied live/final I1 approval. [Official rates/endpoint references](../operations/H-009/api-references.md) are independent from owner authority. [Prompt coverage](../operations/H-009/prompt-coverage.json) explicitly distinguishes actual self-projected tasks from templates, private context and omitted history.

The scoped offline commit containing this report is identified by the separate postcommit `docs/operations/H-009/final-commit-receipt.json` (created only after actual commit and deliberately not inside itself). Native fresh goal/checkpoint receipt is root-owned and follows separately. Live S6→80.00, independent mutation/different oracle, real UI/screenshots/same-run trace and final full-I1 review/invariant gate remain **not run / not achieved**.

## Monetary / stop status

At baseline `runtime/spending.json` is absent: locally recorded attempts/spend/holds **0 / USD0 / USD0**; no ledger reset or creation occurred. This is not an independent provider invoice check. Authorized remainder to admission threshold **USD8**, remainder to total authority **USD10**, contingency **USD2** not automatically usable. Root independently reconfirmed ledger and lock absent after checks; no key/file/env/header content accessed or exported by this lane. [Document preservation/link/hash check](../operations/H-009/document-validation.json), [installed metadata/config evidence](../operations/H-009/versions.json).

No I2–I5, full-service readiness, defense, production deployment or publication. Public delivery stays future/open. Stop after offline checkpoint/report if native blocked; continue only existing G004 after owner resume, fresh snapshot and required practical gates.
