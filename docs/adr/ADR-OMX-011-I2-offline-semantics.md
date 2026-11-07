# ADR-OMX-011 — accepted I2-offline semantics and continuation

2026-11-07. Owner: repository. Status: adopted for I2-offline by actual H-011 task and accepted ADR-CHAT-006 / CHAT-043. This is a reviewed-safe technical synthesis, not a private transcript export. ADR003–007 remain proposed; I1 and its completed workflow are unchanged.

## Context and decision
Extend the existing Python3.12/SQLite/LangGraph/Streamlit architecture, not replace it. Each question has one independent SQL step. Mean, three explicit count objects, enrollment JOIN listing, mean/count grouping by course/student/teacher/offering/semester and top course use registered per-step ResultSpec. All combinations of optional student/course/teacher/semester filters are supported; absent filters explicitly mean all, including all semesters. Runtime plan and SQL remain provider proposals, not canned answers; scripted transport is tests only.

Grades remain integer hundredths 0..10000 or NULL. Each graded enrollment has equal weight, including retakes across offerings; NULL excluded, zero included. No history within an offering, credit weighting or latest-only rule. Counts distinguish enrollments, graded enrollments and distinct students. Top selects all exact rational maxima before HALF_UP two-place display, ordered by ID; no-grades candidates excluded. Every result has explicit grain, unit, nullability and exact component aliases. No row-first inference for NULL/empty results.

Names resolve against a validated bounded server catalog; duplicates require a choice, ID/name conflicts and unknown entities never silently select. “Current semester” requires a known semester choice; vague count requires an object. Clarification uses actual LangGraph interrupt/checkpoint with in-process memory. Server session/run/checkpoint/clarification/schema/data/policy identities bind resume. Two pauses, 15-minute TTL; human waiting excluded from active work. Exact accepted replay is idempotent, changed same-ID payload conflicts; invalid/foreign/stale/expired resumes fail before calls. No pre-interrupt paid side effects replay, counters persist. Restart loses continuation explicitly; durable restart recovery not promised.

## Alternatives and rationale
- Latest-only/credit weights need other data and change accepted arithmetic; rejected for this stage.
- Silent current semester/first Alex loses explicit scope and identity; rejected.
- Durable persistence adds lifecycle/migrations and is not accepted scope; InMemorySaver meets the local session demonstration with honest expiry.
- Regex-only SQL security rejected: retain AST allowlist, validated bound values, read-only SQLite authorizer and worker watchdog. Safe SQL still is not proof of semantic correctness: independent oracle must detect plausible wrong JOIN/aggregate.
- Unrestricted SQL compiler or new libraries rejected: extend existing adapter/registry/patterns only. Core contains no University table/grade identifiers. Multi-step and Library deferred to I3.

## Consequences and verification
Keep output32768, plan60/SQL-repair45s, active180s, five provider attempts; no silent limit increase. One parse/unknown-column repair, no unsafe/semantic repair. Provider unknown-usage accounting_stop is terminal without retry; old monetary ledger, cap and holds unchanged. Fail closed on corruption, oversized results and trace failure, never truncate aggregate/top. UI English, same-run trace survives reruns; no stale answer.

Verify frozen independent oracle Q1–Q12, all 16 filter subsets and discriminating mutations, every grouping key, exact ties/NULL/empty, corrupted DBs, strict schemas/bindings/units/grain, real SQLite/compiled graph, checkpoint rejection/replay/limits, provider/DB/trace failures, full-payload size and installed strict wire compatibility, AppTest and offline browser success/clarification/repair/error. Cleaner then full regression/static checks, independent code-reviewer APPROVE and architect CLEAR plus configured blocking gates are required. [Contract](../plans/I2-offline-contract.md), [brief](../plans/I2-offline-brief.md).

No live/API/count call, credentials, monetary change, push, I3–I5 or defense. Offline completion is independent of future live authorization. Changes to accepted semantics/limits require a separate scoped decision, not test weakening.
