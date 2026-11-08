## Current H-015 scoped decision — 2026-11-08

[ADR-OMX-014](ADR-OMX-014-H015-full-live-eval.md) records prospective collector and
atomic history-preserving shared budget-policy migration choices under actual
H015/CHAT053/054/ADR-CHAT007. Full48/max240,aggregate120/dispatch110/reserve10 include
historic5.970272/14entries; no smoke or new push authority. Implementation/measurement
proof is pending in the [H015 report](../reports/H-015-full-live-eval.md). Accepted
ADR006/Sol unchanged; ADR003–007 remain proposed. Earlier current-stage headers
below are preserved historical cutoffs, not new H015 restrictions.

## Current H-011 scope
I1 is complete (native completion and strict checkpoint recorded in H009 postcheckpoint receipt). ADR-CHAT-006 is accepted for I2-offline by CHAT-043; [ADR011](ADR-OMX-011-I2-offline-semantics.md) adopts only that scope. ADR003–007 remain proposed, not blanket approvals. No live or push authority.

# Decision index

Owner: repo. Updated: 2026-11-07. Application architecture: **not yet approved**.

| Decision | Owner/status | Location |
|---|---|---|
| ADR-CHAT-001: memory ownership | chat / accepted; safe derivative | [Snapshot](../chat/decisions/ADR-CHAT-001-memory-ownership.md) |
| ADR-CHAT-002: compact demonstration scope | chat / accepted; safe derivative | [Snapshot](../chat/decisions/ADR-CHAT-002-result-scope.md) |
| ADR-CHAT-003: repository location and OMX method | chat / accepted per verified private input; deliberately not exported (outside four-file allowlist) | Preparation-only consequences recorded in [ADR-OMX-001](ADR-OMX-001-preparation-boundary.md); source ID is attribution, not a missing public link |
| ADR-OMX-001: bounded preparation / blocked Git | repo / adopted for this stage | [ADR](ADR-OMX-001-preparation-boundary.md) |
| ADR-OMX-002: execution-context scope, checkpoint blocker and prompt completion | repo / adopted for H-005 preparation only | [ADR](ADR-OMX-002-execution-context-and-checkpoint.md) |

The authoritative chat originals remain in the private source store. Projections are immutable derivatives, not new originals. No application architecture, domain semantics, technology, numeric eval threshold or future Git policy has been accepted by this index. Future significant decisions need context, alternatives (including rejected ones), reasons, consequences and verification; architecture is returned to chat before implementation.

## H-006 B — proposed, awaiting owner chat review

Architecture recommendations passed separate Architect/Critic reviews, not owner acceptance. No implementation authorization.

- [ADR-OMX-003-minimal-stack](ADR-OMX-003-minimal-stack.md) — **proposed**.
- [ADR-OMX-004-domain-semantics](ADR-OMX-004-domain-semantics.md) — **proposed**.
- [ADR-OMX-005-bounded-graph-contracts](ADR-OMX-005-bounded-graph-contracts.md) — **proposed**.
- [ADR-OMX-006-schema-boundary-tracing](ADR-OMX-006-schema-boundary-tracing.md) — **proposed**.
- [ADR-OMX-007-verification-delivery](ADR-OMX-007-verification-delivery.md) — **proposed**.

[Architecture review / closeout / limitations](../reports/H-006-architecture-review.md). Historical accepted scope and preparation ADR001/002 are unchanged.

## H-007 limited implementation authority
[ADR-OMX-008 — scoped I1 choices](ADR-OMX-008-I1-scoped-implementation.md) is adopted provisionally for S6 by the new user task only. It does not promote ADR003–007 or accept the full project design. Model/access/spending and real live/UI acceptance remain independent gates.

## H-008 accepted model configuration
[ADR-OMX-009 — Sol operation profile](ADR-OMX-009-Sol-operation-profile.md) implements accepted ADR-CHAT-004 / CHAT-029 for this limited I1. Model/effort accepted; bounded limits provisional and live adequacy unproven. Supersedes only ADR008's prior unknown-model/old-limit clauses, preserving history and unrelated proposals.

## H-009 practical I1 spending policy
[ADR-OMX-010](ADR-OMX-010-I1-practical-budget-policy.md) adopts accepted ADR-CHAT-005 / CHAT-034 for I1 only: total10, new-dispatch threshold8, contingency2, explicit estimate-based residual uncertainty. Supersedes the old strict input/count-fee proof, not a claim it was achieved; live/final gates and unrelated ADR proposals remain unchanged.

## H-013 — current combined offline scope
[ADR-OMX-012](ADR-OMX-012-I2-I3-offline-contracts.md) records adopted scoped implementation choices before dependent code: per-step registry, static bounded DAG then typed actual-result binding, in-memory session-bound continuation, early Library adapter and unchanged dependencies/bounds. Actual H-013 / CHAT-045 expands accepted ADR006/ADR011 only beyond single-step/no-Library; ADR003–007 remain proposed. Full I2+I3 offline proof is pending, not conferred by this decision. [Whole brief](../plans/I2-I3-offline-brief.md), [acceptance contract](../plans/I2-I3-offline-contract.md).

## H-014 scoped repair
[ADR-OMX-013](ADR-OMX-013-readiness-scope-boundary.md) records the independently found named-target scope-loss defect,
failing regressions and existing adapter-owned fail-closed guard repair. This is
not reacceptance of proposed ADR003–007 or a new architecture/domain decision.
Final readiness proof is tracked in the [H014 report](../reports/H-014-readiness-offline.md).
