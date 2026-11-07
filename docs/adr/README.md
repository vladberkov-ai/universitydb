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
