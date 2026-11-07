# Production considerations — current I1 and future work

## Implemented I1 baseline (2026-11-07)

The application now exists. The proposal below is retained as design history, not an implementation checklist already completed. Current reliability includes typed contracts, bounded attempts and subprocess watchdogs; current storage is read-only SQLite during generated queries. JSONL traces and UI inspection work. Security is limited to synthetic loopback use, SQL allowlists/authorizer and local credentials. Dependency versions are locked and reviewer run instructions are in the root README. Conversational checkpoint/resume, multi-user scaling, auth, hard memory isolation and production deployment are not implemented.

Before production: test failure/recovery and durable state; benchmark concurrency and quotas; centralize protected tracing/alerts; add authentication/authorization/resource isolation; define hardened deployment/rollback and backups. The five-topic proposal below expands these tasks. The implemented provider/DB process kill does not guarantee wall-clock limits under arbitrary parent filesystem stalls.

## Historical proposed design

Proposed 2026-11-07; The application has not yet been created, **not production-ready**. "On task" below means a planned, uncompleted property.

| Topic | Plan for a compact task | Before production additionally |
|---|---|---|
| Reliability | typed contracts, bounded retries/timeouts, no unsafe fallback, independent oracle, InMemorySaver with explicit expiry after restart | durable checkpoints with secure serialization, migrations/backups/restore drills, failure recovery, HA/SLO/error budgets, provider outage strategy |
| Scalability | local read-only SQLite, one active request/UI session, small result/token caps | workload benchmark, queue/admission control, tenant quotas, connection pools; for concurrent writers, consider PostgreSQL and the new dialect adapter/test suite; do not migrate SQLite security policy blindly |
| Monitoring/tracing | local complete versioned JSONL Andscreen expanders SQL/bindings/typed results/full trace, attempts/usage/cost/latency/error codes, synthetic public exports | searchable centralized storage, retention/access policy, dashboards/alerts p95 latency/errors/token spend, trace sampling doesn't loseaudit/security events, on-call ownership |
| Security/privacy | loopback only, synthetic data, no keys in logs/repo, mode=ro+authorizer/allowlists+limits, process SQL watchdog, ingress/output checks | authentication/authorization/row-level access, tenant isolation, secret manager/rotation, dependency supply-chain audit, privacy/legal review, encrypted data/checkpoints, sandbox resource isolation, threat model/pentest |
| Deployment | reproducible Python+dependency lock/version receipt, clean clone instructions, local config presence checks | container/hardened runtime, CI/CD signed artifacts, rollout/rollback/migration gates, TLS/network policies, infra access controls, production cost governance |

Read-only ≠ semantic correctness; JSON schema ≠ correct SQL; trace completeness ≠ permission/publication; store=False ≠ zero retention. Progress handler cooperative, hard worker kill/memory enforcement must be separately implemented/measured. Lack of authentication is acceptable only loopback synthetic demo; do not publish the UI as a service available to everyone. LangSmith optional future alternative after retention/billing/privacy review, optional dependency.

Future check: owner explains each tradeoff and shows planned vs actual evidence; failed production feature is not masked in assignment readiness. Revision triggers: real personal data, remote multi-user access, DB entry, concurrent workloads, durable resume/recovery or new provider/SQL dialect. Then we need a new ADR/threat model, not a mechanical increase in limits. See [architecture](architecture-proposal.md), [tests](test-plan.md).

Iteration2 clarification: bounded SQL/bindings/input byte gates and oversized-value tests W1–W3 do not prove hard memory isolation. SQLite can allocate memory before the fetch/progress handler; in the local synthetic demo this is clearly a residual risk. Before remote/untrusted production, OS worker memory/resource policy and real adversarial verification are required; the new dependency/parser/tokenizer in B is not selected.

## H-008 required future assessment (accepted CHAT-029; not implemented)
Before production, explicitly assess LLM verbalization, additional semantic SQL review and a qualitative evaluation judge against the current deterministic baseline. This is an obligation to evaluate, not a decision to add any LLM now. Compare baseline-versus-LLM variants on independent numeric/row correctness, groundedness (no invented numbers), semantic scope fidelity, diagnostic usefulness, explainability and diagnostic regressions using representative positive/adversarial cases and versioned traces. Record latency/cost/privacy tradeoffs, failure cases and a justified adopt/reject decision in a new ADR. A judge's favorable text cannot override the independent oracle or SQL/DB safety boundary. No extra LLM calls/dependencies/evals are authorized in current I1. [ADR009](../adr/ADR-OMX-009-Sol-operation-profile.md) records the accepted profile and still-open live gates; old proposed production text remains historical.
