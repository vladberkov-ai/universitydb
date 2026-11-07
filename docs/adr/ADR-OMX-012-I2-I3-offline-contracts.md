# ADR-OMX-012 — bounded I2 + I3 offline contracts

2026-11-07. Repository-owned, adopted for actual H-013 scope under CHAT-045 and accepted ADR-CHAT-006. Records reversible implementation choices **before dependent code**, not completion evidence or blanket approval of ADR003–007. Supersedes only H-011/ADR011 single-independent-step/no-Library exclusions. Historical documents remain unchanged.

## Context
University breadth, clarification and dependent M1 share ResultSpec/state changes; deferring Library risks a domain-coupled core. Existing Python/SQLite/direct LangGraph/Streamlit/JSONL and exact Sol high/medium/medium are accepted, not reselected. Offline provider injection proves mechanics with real DB/compiled graph, not real-model accuracy.

## Choices, alternatives and rationale
1. **Exact per-step registry.** Domain registry owns metric/shape/columns/types/nullability/component aliases/grain/unit/scale, accepted on each step; SQL/result must match exact accepted spec. University mean uses integer grade_hundredth/100 and explicit sum/graded/enrollment components; counts use count/1; listing nullable grade stays typed; Library count is never grade-scaled. Reject provider-invented spec/aliases, first-row type inference and global domain.spec: they break NULL/empty portability. Registry can evolve without a new general-purpose abstraction.
2. **Static bounded DAG, then runtime bind.** ≤3 topologically ordered steps. Validate unique IDs, exact refs/dependencies, referenced registered columns/types, no missing/cyclic/forward-invalid references before calls. Separately materialize only completed validated dependency rows into typed bound values; top adapter supplies selected exact ties, cohort is a de-duplicated union. Explicit empty list means empty set, never absent filter. Reject missing/types/truncation/oversize before downstream provider/SQL. SQL fragments from results, fixed query chains and unbounded recursive planning rejected: unsafe or not genuine dependency proof. Existing calls≤5/SQL attempts≤4/active180/time/payload bounds apply across entire DAG/resume/repair.
3. **In-process session-bound continuation.** Use installed LangGraph in-memory saver/interrupt, server session/run/checkpoint/clarification/schema/data/policy identity, max2 pauses/TTL900s. Exact replay idempotent, changed replay conflicts, stale/foreign/expired invalid before calls. Preserve counters/trace and avoid pre-interrupt side effect replay; human wait excluded from active work. Durable restart storage would add lifecycle/dependencies and is outside accepted scope; restart explicitly expires. A UI-only question/restart is not accepted checkpoint continuation.
4. **Early Library domain adapter.** Separate schema/seed/descriptor/catalog/registry/result adapter/domain policy for Readers/Books/Loans and returned false; same generic core/graph/safe DB/provider/tracing/UI. Validate both at CP-B, rerun Library on shared changes, compare same integrated core tree hash while switching domains. Late prompt-only schema swap and core branches on domain table names rejected: neither proves portability. Adapter-owned labels/count semantics retain zero. Not a library-management product or SQL-dialect claim.
5. **No new dependencies; preserve bounds/security.** Reuse locked tooling, stdlib+temporary SQLite independent oracle. AST allowlist/read-only URI+authorizer/typed bindings/watchdog and corruption scans stay independent boundaries. One parse/unknown-column repair only; unsafe/semantic/accounting stops terminal. No silently raised ceilings, retries/fallback/judge, monetary migration or ledger reset. Necessity for any lock change must be recorded before adoption.

## Consequences and verification
More typed failure cases and continuation identities are explicit, not inferred from successful rows. Independent frozen oracle covers University all groups/filter subsets/mutations, M1 F1/F2/tie/empty and Library 1/1/zero/returned mutation before product tests. Static/ref/wire/NULL/empty safety tests, real SQLite/compiled graph, actual binding sensitivity, AppTest and offline browser/full traces, independent APPROVE+CLEAR/configured gates prove offline DoD. Semantic safety limitations and absence of hard memory isolation remain explicit. Follow [whole brief](../plans/I2-I3-offline-brief.md) and [contract](../plans/I2-I3-offline-contract.md); no live/push/I4–I5/defense authority.

## CP-C implementation note — typed public row reasons
Before the closed Answer validator, adopt optional `Answer.row_reasons` as a list
of `null | "no_rows" | "no_grades"`, length exactly equal to normalized answer rows when present.
Context: H-013 requires per-group no-grades annotation and M1 tie includes a student
with enrollment but no grade. Keeping that annotation only in step results would
hide required meaning from public/UI consumers, so that alternative is rejected.
Scalar `empty_reason` still owns no_rows/no_grades; optional per-row no_rows preserves
the existing scalar empty proof, not new semantics. Counts/Library may omit the
extension. Explicit optional compatibility applies to this H-013 representation;
historical output examples and domain semantics/model/limits are unchanged.

## CP-C implementation note — continuation representation and trust
Record the actual local closed clarification/binding envelope and API in the
[current contract](../plans/I2-I3-offline-contract.md#cp-c-actual-in-process-continuation-representation).
Choose typed int/string option IDs and server-generated Unix-seconds float expiry,
plus explicit application run/checkpoint/session/schema/data/policy identities.
Alternative historical proposed opaque option strings/RFC3339/minimal wire is not
adopted implicitly: local typed choices avoid lossy conversions and explicit
bindings make same-session checkpoint inspection auditable. The consequence is a
larger closed envelope and exact echo validation. None of these client-echoed
values grants authority; retained server Agent/context/checkpointer/current data
are authoritative. Native OMX ownership and IDs are separate and never exposed
by this product contract. No authentication, public HTTP or restart-durability
claim follows from local equality checks.

## CP-D implementation note — count every retained application copy
Before dependent code, clarify the existing128KiB bound as the serialized UTF-8 JSON
bundle of current raw result, proposed completed dependency results (current step
included), raw/adapted step_results
and current answer, checked before accepting retention/downstream. Alternative
completed-rows-only accounting is rejected: it omits retained duplicate copies and
understates application payload. Consequence: earlier fail-closed rejection of
oversize bundles as RESOURCE_LIMIT without partial success or downstream dispatch;
scope/counters/framework overhead are not this result bundle. No ceiling,
semantics/accounting policy or dependency change. Framework history/transient
allocations still lack hard process-memory isolation. Regression must exercise a
bundle whose individual pieces fit but combined retained payload exceeds131072.

## CP-D implementation note — signed SQLite64 primitive integers
Before dependent code, bind integer wire/raw-result primitives to strict signed64
SQLite range, and scale to positive signed64 plus exact registry equality. Context:
unbounded Python ints in provider bindings/scale can overflow LangGraph msgpack
before later semantic validation. Root-cause primitive boundary validation is chosen;
generic OverflowError swallowing or acceptance of arbitrary big integers is rejected.
Consequence: malformed oversized values fail typed validation before saver/SQL,
without changing accepted IDs/grades/counts/scale variants, budgets or dependencies.
Retained-payload regression fixtures must use otherwise valid typed values, not
impossible huge integers that fail this independent boundary first.
