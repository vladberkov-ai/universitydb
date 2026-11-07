# UniversityDB — repository instructions

## Current boundary: H-006-v4 preparation checkpoint, then advisory design only
- Stage A is solo preparation and a verified local docs checkpoint on main. Stage B starts only after A is committed and verified.
- B uses standalone `$ralplan --advisory --deliberate`: real sequential Planner, Architect, Critic and configured quality gates; planning/research/reviewer subagents are permitted. No execution workers or application implementation.
- No application, executable SQL schema/seed, product tests, application runtime prompts, UI implementation, product dependencies or paid/live LLM calls. Documentary ERD/contracts/fixtures/test plans are allowed in B.
- Close advisory through its supported lifecycle, without execution authorization/handoff; only afterwards package safe stable docs and make separate docs commit B. All new architecture decisions stay proposed pending chat review. Stop after report.
- Git metadata is visible at this same workspace; A was committed on main as `8931d832d49311ac0d63c3a7a359b4293058da89`, with no remotes. Initial main was unborn. Current sandbox mount is ext4 read-only: ordinary force-write-index failed EROFS; the supported explicit permission request succeeded. Subsequent writes require their own supported permissions. Do not bypass restrictions or infer blanket write authority.
- Historical H-004/H-005 observations and restrictions remain scoped to those stages in their reports/ADRs; H-006-v4 supersedes their no-architecture/no-children boundary only for this documentary design stage.
- Git metadata, future code/dependencies/venv/tests and omx_wiki belong in this repository; dependencies and venv are not tracked.

## Current B blocker
- B stopped before advisory activation: runtime binding check fails `bad_selectors=CODEX_SESSION_ID`; no canonical advisory generation/root/turn binding is supplied. Roles were not launched and no architecture was produced. See `docs/reports/H-006-advisory-blocker.md`. Do not fabricate IDs, rewrite the usable runtime pointer, or substitute Standard/solo consensus.

## Ownership and evidence
- Obsidian is the authoritative chat/source store; read-only in this stage. Do not change its Wiki, manifest, `.obsidian`, or raw inputs.
- `docs/chat/` contains only the four H-004-v2-authorized, redacted, one-way snapshots; H-005 permits refreshing stale members of the same set. Never manually evolve them as a second original. Check destination hashes against the previous receipt before a refresh, then compare current source hashes; stop on conflicting local changes. Preserve previous receipts as provenance history. Do not apply H-004's historical input hashes to later agreed chat changes.
- `docs/` owns stable OMX reports, decisions and prompt records. `omx_wiki/` is OMX's own working memory and links to these documents; it does not replace/copy Obsidian.
- Preserve actual prompts separately from templates, read context and runtime prompts. Record session IDs, coverage, omissions and redactions. Do not publish private transcripts or secrets.
- Keep accepted scope distinct from proposals and implementation evidence. Do not revive the withdrawn 27/30 threshold or accept previously proposed domain rules implicitly.
- All significant decisions require context, alternatives, rationale, consequences and verification. Application architecture is still open.

## Git and validation
- Preserve existing instructions/materials and unrelated changes. Never move legacy materials silently or use blanket staging.
- H-006-v4 permits separate verified local docs commits A and B, after composition, hashes, links, privacy and diff checks. Use normal tool permissions and supported explicit escalation only when offered; the current interface supports specific requests. If Git is blocked, report not-committed without claiming success. Do not suggest permission bypasses.
- Do not change global Git configuration, create/change remotes, publish or push in this stage.
- Saved, committed, pushed and public are separate statuses. R-15 stays open until separately proven.
- Future checkpoint policy is proposed: see `docs/operations/git-checkpoints.md`.
- Report real checks, failures and not-run checks. Start with targeted documentation validation; application tests are not-run because this stage creates no application.

Start from `docs/reports/H-005-preparation-completion.md`, `docs/ai/README.md`, `docs/adr/README.md` and `omx_wiki/index.md`. The H-004 report/validation/partial export remain historical snapshots; use H-005 evidence for the updated files. Runtime ownership, automatic hooks and process spawning are not certified by successful session export or team doctor alone.

## H-006 B documentary-delivery update — 2026-11-07
The earlier “Current B blocker” section is historical, superseded only by the verified B2 closeout and subsequent repair evidence. Generation `ec3e1f0b-d751-4088-bfb2-ec386c08549c` is closed approved+proven; terminal mirrors inactive, no execution handoff. See `docs/reports/H-006-architecture-review.md`. Do not restart/review/research/complete/cancel that generation or manually change IDs/tracker. Current task only packages existing safe proposed documents and the separate local docs commit B, then stops for chat/orchestrator review. All architecture ADR003–007 remain proposed. Application implementation, product dependencies/tests/evals, runtime prompts, remote/push and Obsidian writes remain outside this authorization. Old blocker/research evidence stays unchanged.
