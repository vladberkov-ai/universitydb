# ADR-OMX-002 — execution-context scoped Git blocker and prompt completion

Date: 2026-11-07. Owner: repo. Status: adopted for H-005 preparation only. No application architecture decision.

## Context / evidence
H-005 authorizes continuing the same workspace, refreshing only stale members of the original four-file allowlist, completing H-004 prompt coverage, and one local docs checkpoint if normal permissions allow. All 10 vault input hashes and 3 workspace baselines matched. All 21 files in the old H-004 manifest matched before edits. Current tool subprocesses see the workspace on ext4 rw but `.git` as empty tmpfs ro/mode 555. Ordinary `git init` returned exit 128, unable to copy its template description: Read-only file system. The explicit tool permission policy marks `.git` read-only and sandbox escalation unavailable.

The chat review reports a separate external UbuntuD view with no `.git` and an ext4 rw parent. These observations have different execution contexts and do not contradict each other. The tool view and mount namespace are directly observed; a sandbox/mount-view explanation is consistent with policy/evidence, but the external namespace and exact mapping were not independently accessed or proven here.

## Alternatives
1. Use normal Git and a supported specific permission escalation: desired path, but ordinary initialization failed and the active policy automatically rejects sandbox escalation; no supported prompt is available.
2. Change mounts/mode, use another git-dir/workspace, or call an external namespace/WSL process to evade restrictions: rejected as permission bypass or duplicate-repository risk.
3. Repeatedly ask for unsupported approval/reinstall OMX/clear session selectors: rejected; not supported, not a proven fix and risks unrelated state.
4. Complete independent safe preparation, preserve historical records, and return the localized blocker: selected per H-005.

## Decision / rationale
Keep the same workspace and solo lane. Archive the prior chat receipt and H-004 prompt receipt byte-for-byte before updating pointers. Refresh only requirements after verifying the existing destination hash; leave the three unchanged projections alone. Keep the original H-004 partial export and old validation intact; derive a new export through the actual H-004 final response, splitting logical stages at the actual H-005 user message in the **same** native session. Record H-005 separately with its current cutoff, without fabricating its future final reply.

Do not equate a doctor failure to total CLI unavailability: direct Codex/Node version and OMX export work. A minimal Node spawnSync probe reports both a successful child version/status 0 and an EPERM error; doctor treats error as failure before status. Hook smoke and session binding are **not certified healthy** by these narrower successes. The stored runtime PID is not visible in this tool PID namespace; current native session selectors equal the metadata native ID, but ownership/liveness across namespaces remains unproved. Do not clear selectors or recover locks.

## Consequences / verification / reopening
Saved files and message coverage can be verified now; Git root/branch/HEAD/checkpoint remain unavailable in this context. Future runtime-owned/stateful workflows need their own binding/hooks/spawn checks in an authorized context; successful documentation/export is not blanket approval. Workers/architecture/implementation/push are still prohibited. The future Git cadence remains proposed.

See [H-005 report](../reports/H-005-preparation-completion.md), [input evidence](../operations/H-005-input-verification.json), [environment evidence](../operations/H-005-environment-checks.json), [receipt](../operations/H-005-preparation-receipt.json) and [validation](../operations/H-005-preparation-validation.json). Minimal recovery condition: this same workspace must be supplied with normal authorized writable Git metadata in a supported execution context; then re-inspect and make the checked docs commit. No instruction to bypass the sandbox or create another copy is implied. Next action now is to return the report to chat, not start architecture.

## H-006-v4 context update (history above retained)
The same repository now has visible Git metadata, unborn main and no remotes. In the current sandbox, ordinary `git update-index --force-write-index --refresh` failed EROFS (128); the supported explicit permission request succeeded (0). This supersedes the historical claim that no escalation path is offered, not the old evidence itself. No mount/namespace/git-dir bypass, reinitialization, global configuration or remote change was used. Stage A checks the preparation allowlist and commits it; B is authorized documentary advisory planning only after verified A, with real planning/review agents, no execution handoff or product implementation. See [current preparation report](../reports/H-006-preparation-checkpoint.md).
