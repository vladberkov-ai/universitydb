# Git checkpoints

Owner: repo. Date: 2026-11-07. Sources: private chat-owned Git protocol, H-004 v2 and current H-005 (read in full).

## Authorized for this stage
H-004 v2 and continuation H-005 authorize local preparation files, initialization at the same selected location after duplicate checks, and **one local preparation docs commit**, conditional on verification and writable Git metadata. They do not authorize remote creation/change or push. The `.git` read-only mount is an observation **inside the tool sandbox**, not of all UbuntuD; the parent is ext4 rw. Normal H-005 `git init` failed (exit 128 / Read-only file system). Sandbox escalation is disabled by the active permission policy, so no approved escalation path can be requested here. Do not work around it with a second Git directory/repository or an external process/alternate namespace.

When Git becomes available in this same workspace under normal tool permissions (supported specific escalation only when policy allows), inspect root, status, branch, worktrees, remotes and identity again; preserve any history/foreign changes that appeared. Review only the explicit public-safe file list in the [current report](../reports/H-005-preparation-completion.md) and [H-005 validation manifest](H-005-preparation-validation.json). The [H-004 validation](preparation-validation.json) is an immutable historical snapshot, not a current staging list. Run current link/hash/privacy checks and `git diff --check`; stage only explicit validated paths. Inspect `git diff --cached --stat`, `git diff --cached --name-status`, `git diff --cached --check` and the full staged patch; then make one docs commit. Capture HEAD and final status **after** commit, outside that commit. Do not include unrelated changes or raw runtime artifacts. Current staging and commit remain blocked, not complete.

## Proposed future policy, not blanket acceptance
- One finished unit of change plus its checks → commit before starting the next dependent unit.
- Architectural ADRs with alternatives/rationale precede dependent code.
- Checkpoint before a stage transition or pause; 30–60 minutes is a guideline during long work, not background automation or permission to stage unfinished runtime files.
- Honest WIP, if needed, identifies failing/not-run checks and is not a deliverable declaration.
- Stable plans, prompts, ADRs, results and reports live in versioned `docs/`, not only runtime `.omx/`.
- Each stage-boundary report states real SHA, tests, coverage, limitations and publication status. OMX persistence/reviewer agreement is not a commit or execution evidence.

## Publication — separate future authorization
Next publication step: establish GitHub owner/name, target branch and explicit publishing authority in a separate handoff; verify the complete safe deliverables before creating/configuring any remote or pushing. Afterwards verify the remote branch SHA and anonymous public access separately. This stage does none of that. R-15 remains open; no remote URL/SHA is invented.

Saved ≠ committed ≠ pushed ≠ public. Do not force-push, rewrite published history, initialize the vault, or infer authority from another session.

## H-006-v4 context update (history above retained)
The same repository now has visible Git metadata, unborn main and no remotes. In the current sandbox, ordinary `git update-index --force-write-index --refresh` failed EROFS (128); the supported explicit permission request succeeded (0). This supersedes the historical claim that no escalation path is offered, not the old evidence itself. No mount/namespace/git-dir bypass, reinitialization, global configuration or remote change was used. Stage A checks the preparation allowlist and commits it; B is authorized documentary advisory planning only after verified A, with real planning/review agents, no execution handoff or product implementation. See [current preparation report](../reports/H-006-preparation-checkpoint.md).
