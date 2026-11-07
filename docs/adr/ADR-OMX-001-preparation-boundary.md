# ADR-OMX-001 — bounded solo preparation and Git blocker

Date: 2026-11-07. Owner: repo. Status: adopted for this preparation stage only.

## Historical H-004 context (tool sandbox observation)
H-004 v2 requires preparation, provenance and prompt accounting, but forbids architecture, implementation, workers and publication. All 25 listed input hashes matched. The preferred workspace exists in UbuntuD; the legacy candidate has instructions and private bootstrap materials, not a Git repository. Within H-004's tool sandbox, `.git` was an empty read-only tmpfs mount, so Git reported no repository. This was not a statement that the whole UbuntuD filesystem was read-only.

## Alternatives
1. Launch Team/autopilot or architecture planning: rejected; violates the stage boundary and adds no value to bounded documentation preparation.
2. Replace/unmount/chmod the protected `.git`, redirect Git metadata elsewhere, or initialize a second repository: rejected; violates sandbox or single-repository/location constraints.
3. Abandon all preparation because commit is blocked: rejected; H-004 explicitly permits independent safe progress when blocked.
4. Direct solo preparation using the installed OMX CLI, prepare independent public-safe documents in the selected workspace, and report the Git blocker: selected.

## Decision and rationale
Use the local `understand → execute → verify → report` lane, without workers, subagents or durable-goal workflows. Read and hash private inputs without modifying/exporting them wholesale. Export exactly four authorized chat projections with source/destination hashes and link/redaction accounting. Keep OMX working memory separate and link to stable repo-owned results. No dependencies or application artifacts are created.

Treat the selected workspace as the canonical **target**, not an initialized/proven Git repository. Normal Git operations must wait for a session with writable `.git` at this same location. Public preparation artifacts do not imply public availability or complete application requirements.

## Consequences
Files can be saved and verified now; initialization/staging/commit/branch/HEAD cannot be honestly reported as complete. History and runtime prompt coverage remain explicitly incomplete. No silent material migration, competing repo, remote or push is introduced. The next stage is not started.

## Verification and reconsideration
See the [preparation report](../reports/H-004-repository-preparation.md), [input checks](../operations/input-verification.json), [receipt](../operations/chat-export-receipt.json) and [validation](../operations/preparation-validation.json). Reconsider the Git blocker only after the normal execution environment supplies writable metadata; re-inspect candidates/status before mutation. This ADR chooses no SQL engine, graph contract, model, UI or application architecture.

## H-005 follow-up, 2026-11-07
The [H-004 receipt archive](../operations/history/H-004-chat-export-receipt.json) preserves the original export provenance. H-005 refreshed the requirements projection after all destination conflict checks passed; other three source/destination pairs were unchanged. H-004's old validation is intentionally historical, not current proof. Its final response is now available in the completed **logical-stage** message export; the same native session continued into H-005. No full-tool coverage is claimed.

H-005 again observes the read-only Git mount inside the tool sandbox while its parent workspace is ext4 rw; normal `git init` fails with EROFS. A separate chat-side UbuntuD observation reported no `.git`; that is not independently reproduced here. [ADR-OMX-002](ADR-OMX-002-execution-context-and-checkpoint.md) scopes the permission blocker and diagnostic limitations. The H-004 decision/history is retained; application architecture remains undecided.

## H-006-v4 context update (history above retained)
The same repository now has visible Git metadata, unborn main and no remotes. In the current sandbox, ordinary `git update-index --force-write-index --refresh` failed EROFS (128); the supported explicit permission request succeeded (0). This supersedes the historical claim that no escalation path is offered, not the old evidence itself. No mount/namespace/git-dir bypass, reinitialization, global configuration or remote change was used. Stage A checks the preparation allowlist and commits it; B is authorized documentary advisory planning only after verified A, with real planning/review agents, no execution handoff or product implementation. See [current preparation report](../reports/H-006-preparation-checkpoint.md).
