# H-011 preparation-only cleaner

Scope: changed current-boundary documentation, new brief/ADR/contract/readiness/report/provenance. Not a final I2 product cleaner or completion gate.

Behavior lock: all product/schema/seed/test/dependency/old-evidence hashes unchanged; 129 baseline tests passed with unsafe repo-runtime AppTest excluded; 37 independent temporary-SQLite fixture checks. No application refactor.

Bounded cleanup plan: keep historical evidence and decisions immutable; distinguish current accepted scope from proposals; remove only the two documented duplicate final paragraphs in README/manual E2E; avoid new abstractions/dependencies. Literal equality initially missed trailing LF differences; a bounded whitespace-normalized comparison removed only the known duplicate paragraphs. Reviewers caught that initial mismatch before checkpoint.

Fallback classification: candidate OMX_ROOT routing was diagnostic only, not used as an ownership bypass; no masking fallback added. Root I1 --force/reset/replacement rejected. Missing current-native lifecycle authority remains visible. No SQL/runtime/provider fallback code changed.

Passes: duplicate removal completed; no dead application code/naming/abstraction passes applicable because source unchanged. Editorial/current-scope changes only. No UI/style changes. Source static verification/Ruff/format/mypy/compile/diff passed; independent reviewers separately review documents, not author self-approval. Full product/security/graph/UI cleaner gates deferred until actual I2 implementation is authorized on a proven supported lifecycle binding.
