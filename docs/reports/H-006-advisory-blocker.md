# H-006-v4 — A committed; B blocked before advisory activation

Date: 2026-11-07, Asia/Jerusalem. Owner: repo. Status: **blocker**, not architecture approval.

## A — verified checkpoint
Commit `8931d832d49311ac0d63c3a7a359b4293058da89` on main. Exactly 42 explicit preparation files; all manifest blob hashes match, post-commit tree clean; remotes absent. [Post-commit receipt](../operations/H-006-A-postcommit-receipt.json) includes the complete staged-patch digest/review. Input hashes 19/19, prior manifest 34/34 and four source/destination pairs passed; 84 Markdown + 5 Wiki links, scoped privacy and whitespace checks passed. No previous H-006 package used. Original PDF read on all four pages; nothing installed.

## B — exact prerequisite failure
After A, read local Ralplan/Plan instructions, ran `omx status` and `omx quality-gates list --stage ralplan --json`: no active Ralplan; configured gates `[]`. Native `agent_type` routing and installed role files are present, so adapted-authority preflight is not applicable and was not run.

Ordinary `omx doctor` failed writing its temporary smoke directory (EROFS). Supported explicit permission request reran it successfully as a process, but results are **19 pass / 0 warning / 1 fail**, not healthy: `State root/session binding`, `bad_selectors=CODEX_SESSION_ID`, pointer usable. Current native export selector differs from the native ID in the runtime pointer. These are diagnostic values, not root/turn authority. Minimal hook smoke passes; it does not prove activation of this actual request.

No canonical advisory activation/root/turn binding or pending generation exists on the available workflow surface. `omx ralplan status --json` returns **No Ralplan state found**. Installed CLI source confirms that shell `run --task` alone, without an existing advisory/start profile, starts Standard mode; putting advisory text in the task would not activate the requested Advisory. It was therefore not used as a substitute. No internal activation functions, fabricated hook payloads, manual state writes, selector changes, recovery, or prompt-label consensus were used. Lock inspection reports `safeToRecover=false`.

Per H-006-v4, missing canonical identity stops this workflow. Planner, Architect, Critic, researcher and gates **not-run**; no review verdict or architectural decision exists. Advisory completion **not-run** because there is no active generation/review evidence; no terminal `active:false` is fabricated. No execution authorization/handoff. No architecture B commit: its lifecycle prerequisite was not met. This blocker report and supporting post-A evidence are saved separately, **not committed as a completed B**.

## Evidence, coverage, boundaries
- [Runtime commands, exits and diagnostics](../operations/H-006-B-runtime-blocker.json).
- [Actual prompt / current cutoff coverage](../ai/omx/H-006-prompt-coverage-blocker.json); [prompt index](../ai/README.md). Real H-005 final included in its separate completed-stage export. Current H-006 cutoff ends at blocker progress, not the future final reply. No children were launched; no child prompts falsely listed. Application runtime prompts not-created.
- Architecture/contracts/ERD/test fixtures/implementation plan/new architectural ADRs: **not-created**, not reviewed. Accepted requirements and chat decisions unchanged; product R statuses stay open.
- Application tests/build/live or paid eval, product dependency installation, remote/push/public verification: **not-run**. Obsidian unchanged.

## Required continuation boundary
Continuation needs a supported OMX context that supplies a consistent canonical session/root/turn activation for this request. A usable pointer must not be reassigned or recovered from diagnostic IDs alone. Preserve A and existing runtime state; resume only at B readiness with the real native roles, not a solo substitute. No architecture preference or user acceptance is inferred. The result returns to chat with this blocker; implementation remains forbidden.
