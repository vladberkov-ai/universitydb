# H016 evidence/document checkpoint packaging plan

Status: plan only; no staging/commit from this document. Root owns lifecycle and
will request the bounded performer checkpoint after actual final evidence/reviews.

## Explicit scope and immutable exclusions

- Current English reader docs: AGENTS.md, README.md, docs/assignment-status.md,
  docs/manual-e2e.md, docs/adr/README.md and docs/ai/README.md.
- Existing RU/EN prompt bundles plus only new H016 actual-task/translation files;
  provenance receipts, selected exact delegated task projections/results and
  input hash census. No wholesale session/private/vault export.
- New H016 report and stable docs/operations/H-016 evidence: regression logs/proofs/
  traces, independent reviews, all failed browser attempts plus successful final
  browser screenshots/traces/receipts, final verification/clean-run receipts and
  runner-source projection, preservation and invariant audit.
- Stage a generated **explicit file list**, review every path and freeze its hash
  before committing; do not use blanket add or include still-running output.
- Exclude docs/operations/H-016/workflow runtime artifacts, every .omx session/
  goal/state/lock, original untracked locks, __pycache__, temporary DB/runtime/
  ledgers, venv/cache, credentials and all historical H015/frozen evidence.
- Source/harness/test candidates are already separately committed. This packaging
  commit must not imply a new executable/full-test SHA; report it docs-only.

## Raw evidence and diff/privacy checks

Preserve retained raw logs and their pinned hashes exactly. Do not silently trim,
rewrite or normalize them to satisfy whitespace checks. The earlier CP1 two text
projections' disclosed normalization remains a historical exception, not authority
to modify pinned later evidence. For a staged diff whitespace warning, retain the
check output, identify the exact evidence path/line and distinguish harmless
terminal whitespace from a prose/source defect. Fix new authored prose only;
report any accepted raw-output whitespace explicitly rather than claiming an
unqualified clean check. No NUL/overlap log becomes final passing evidence.

Check all staged text for secret values/credential assignments, private vault or
credential paths, headers/env dumps and unintended private transcript material.
Inspect all retained screenshots as evidence/privacy allows; machine scans alone
are not universal privacy certification. Assert staged paths stay inside the
explicit delegated allowlist. Verify local links and prompt/source hashes and
compare immutable historical files/sets against baseline. Keep saved, committed,
pushed and public distinct; push is not authorized or run.

## Final identity and lifecycle handoff

Record exact candidate58f2fe9b955eb25cb5a0ee2a9e1d967a60cdcc32 and independently
validated source/test/resource/tool identity to3bc. Record final archive test and
browser results only from their actual receipts. Keep rejectedf925full and failed
browser1/2 separate. A later root native/strict receipt belongs to a separate
bounded docs-only checkpoint; writer must never manufacture completion from
local state. Final native COMPLETE/strict PASS remain root postconditions.
