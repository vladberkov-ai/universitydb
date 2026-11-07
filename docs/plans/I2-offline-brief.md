# H-011 v2 — I2-offline bounded execution brief

Authority: actual received H-011 task, CHAT-043 accepting ADR-CHAT-006 and entire I2-offline scope/DoD. Sources read-only and hashes recorded in docs/operations/H-011/baseline.json. I1 complete; no resume/replacement of I1. Source package is read context, not actual prompt. Public docs/UI English; actual prompt originals and RU/EN reader bundles separately attributed.

## Goals
1. CP1 contracts and decisions: current AGENTS, ADR index, plan, all R01–17/U01–08 matrix/assignment audit, accepted scoped ADR011, independent frozen seed oracle Q1–Q12, privacy/link/hash checks and local docs commit before dependent code.
2. CP2 query breadth: single-step mean/count/list/group/top, all optional four-filter combinations, validated identities, per-step typed ResultSpec/nullable/empty results, AST allowlist/read-only SQLite/authorizer, domain integrity scan and independent actual-DB oracle/mutations; tests/runtime prompts and verified local commit.
3. CP3 clarification failures and UI: real session-bound in-memory graph interrupt/checkpoint/resume, two pauses/15min TTL, rejection/replay/conflict/identity/counter/active-work proof, one recoverable repair and all failure lanes, complete same-run JSONL/UI across reruns, offline AppTest/browser evidence and verified local commit.
4. CP4 offline completion: cleaner, repeated full offline tests/Ruff/format/mypy/compile/diff/privacy/links/hash checks, every accepted invariant audited, independent code-reviewer APPROVE plus architect CLEAR and configured blocking gates, actual prompts/source identity/traces/screenshots/report and local commit. Then actual native completion, fresh snapshot, supported strict checkpoint and separate postcommit/goal receipt commit (never self-referential/amend).

## Architecture and domain invariants
- Keep Python3.12/locked dependencies, direct compiled LangGraph, SQLite, Streamlit, JSONL and isolated domain adapter; no schema-specific identifiers in core. One independent SQL step, not I3 multi-step/Library.
- Equal weights for graded enrollments/all offerings; NULL is not zero. All-semesters default explicit; three count objects distinct. All exact rational top ties before HALF_UP display. Known catalog IDs/names only; ambiguity/conflict/current semester/vague count handled explicitly.
- Registered exact per-step ResultSpec carries metric/grain/unit/scale/types/nullability; NULL/empty values never infer types from first row. Full real SQLite oracle independent of production formatter; plausible wrong safe SQL must fail semantic tests.
- Clarification server-session/run/checkpoint/clarification/schema/data/policy bound, max2 pauses, TTL15min; true interrupt/checkpoint. Accepted replay idempotent, changed payload conflict, stale/foreign/invalid/expired reject before dispatch. Waiting excluded from active work, counters persist; no paid replay or restart durability claim.
- Keep plan high/SQL and repair medium on exact gpt-6.1-sol without fallback; output32768, timeouts60/45, active180, calls5. One parse/unknown-column repair; unsafe/semantic mismatch not repair. Preserve unknown-usage accounting stop.
- All attempts, SQL/bindings, typed rows, answer/error link one full trace; no success on trace failure, no silent result truncation, no stale UI answer. Synthetic loopback data only.

## Verification and stop conditions
Frozen independent seed components Q1–Q12 and every filter/group mutation, negative contracts/corruption/security/checkpoint/provider/DB/result/trace/payload bounds, real SQLite and compiled graph scripted tests, installed SDK strict schema/full wire sizing. Full offline pytest, Ruff check/format, mypy, compileall, diff check; temporary DB/ledger and isolated UI runtime only. Offline browser success/clarification/repair/error with screenshots and JSONL required, not real-model accuracy.

No live/API generation, count endpoint, credential loading, cap/monetary ledger/hold changes, push/remote changes, vault writes, I3–I5 or defense. Preserve A/B/I1 artifacts and initial untracked locks. No new dependencies unless necessary with rationale. Explicit own-path staging, verified CP1–CP4 and receipt commits, no blanket add/reset/amend. Saved/local committed/push not-run separately reported.

Select distinct nested-cwd artifacts at docs/operations/H-011/workflow: installed source/tests support artifact isolation from root I1. Artifact support alone is not lifecycle authority; actual creation failed before mutation, and no current-native writable binding is certified. Do not use --force, manual IDs/state or second leader. If supported activation cannot be established, preserve exact failure and test one new discriminating hypothesis, then report blocker rather than fabricate workflow/roles.

Final report: docs/reports/H-011-I2-offline.md with actual local and fresh remote SHA (or explicit retrieval gap), receipts/check commands/expected-vs-actual/trace/review/prompt coverage/locks+ledger hashes/gaps. Offline DoD excludes live and push; neither absence blocks completion. Stop after report and terminate owned offline server.
