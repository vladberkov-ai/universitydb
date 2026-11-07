# Post-closeout Advisory repair — 2026-11-07

The prior tracker repair worked in the real B2 run: seven real native children were tracked, iteration 3 received Architect/Critic approval, and the official closeout succeeded. The remaining defect was in `syncSkillStateFromTurn`: it inferred a new phase/active flag from late assistant prose even for an already closed Advisory.

The defect was reproduced in an isolated fixture on the previous runtime (`late notify reactivated closed advisory`). A tested guard now leaves Advisory lifecycle ownership with the canonical generation journal. A matching committed terminal journal is reconciled with the existing locked reconciliation mechanism. A second guard prevents notify from replaying an echoed Advisory invocation through the generic activation writer; direct native UserPromptSubmit owns activation. Generation mismatch, wrong state root and corrupt projection are not repaired from prose. Other skill behavior is unchanged.

Runtime `dist/scripts/notify-hook/auto-nudge.js`, the notify activation entry point and both corresponding shipped TS sources were patched, with original backups in `[PRIVATE_RUNTIME_BACKUP]`. Exact hashes/diff: `installed-manifest.json`, `compatibility.patch`. This remains a local patch to OMX 0.21.46, which may be overwritten by package updates.

## Validation

- Red regression on the previous installation reproduces reactivation after valid closeout.
- The repaired fixture passes the existing native lifecycle checks plus terminal persistence after review/execution/planning prose and through the full late notify CLI.
- 112 upstream notify/auto-nudge and Advisory tests passed; no skips or failures.
- Synthetic events, plan and reviewer artifacts were used only in isolated temporary directories. No new real agents or project reviews were run.

## Current UniversityDB state

Using the existing `reconcileRalplanAdvisory` function, the already-closed generation `ec3e1f0b-d751-4088-bfb2-ec386c08549c` was reconciled from its committed journal. The successful complete command was not repeated. No hand-written state, fabricated review or tracker mutation was used.

While the old CLI/background processes were still running, the live skill mirror continued to receive periodic active writes despite fixes on disk; their exact remaining writer/cache path was not conclusively traced. The idle old Codex was then exited normally through `/quit`, and its pointer was released. Reconciliation after shutdown restored terminal state; six one-second observations showed inactive state with unchanged modification time. `omx status` now reports skill-active inactive. This live observation is separate from the isolated regression proof; a future real running-session closeout after restart remains unmeasured.

Receipt: `reconciliation-result.json`: fence closed, journal approved/proven, session skill and mode inactive, execution handoff false. Original evidence bundle digest remains `57ddd777824da540443657e5f843e8fbd292ef1a528c7112080cd809e7ba5a90`.

All 168 baseline material files—including the final architecture and all reviews under `.omx/plans/H-006-B2/`—remain byte-identical; commit A and Git index are unchanged. Backups are outside the project. Runtime terminal mirrors were reconciled; these are deliberately separate from the material preservation claim.

## Continue

Start a fresh ordinary CLI session to load the patched code. Do not start a new Advisory, rerun planning/research/review, cancel the closed generation or repeat closeout. Resume only safe docs packaging, validation and the previously authorized B docs commit, while keeping architecture decisions proposed. Read this maintenance report and the existing B2 report as context; the old blocker is historical, but the prepared design is not yet packaged/committed.

No product code, application tests/evals, dependency installs, B commit or push were performed by this maintenance task.
