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

## H-013 current local implementation versus future production work

The sections above preserve their historical I1/proposal cutoffs. Current H-013
frozen candidate f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0 passed410offline tests
and static checks. [Exact-process M1/Library proof](../operations/H-013/m1-final/manifest.json)
now verifies dependent F1/F2/tie, checkpoint composition and same-core portability.
Final frozen-source browser passed all six classes (seven captures); independent code-reviewer APPROVE and architect CLEAR received; root native/strict closeout remain separately pending. This is **not
production readiness** or real-model NL→SQL accuracy. Current scoped decisions:
[ADR012](../adr/ADR-OMX-012-I2-I3-offline-contracts.md), [whole contract](I2-I3-offline-contract.md).

| Area | Implemented local boundary / evidence | Still future, not implied |
|---|---|---|
| Reliability | Closed per-step/public contracts, registered adapter semantics, bounded DAG and actual typed result binding; real in-memory LangGraph pause/resume with session/schema/data/policy/checkpoint binding, two pauses/900s, replay/conflict checks; common bounded repair/retry and terminal accounting stop. CP-C source/evidence and subsequent CP-D tests distinguish cutoffs. | Durable restart recovery/HA/migrations/SLO/failover, arbitrary request correctness, exactly-once external effects, hard process-memory isolation. Process restart expires continuation; framework snapshot/transient memory is not the131072-byte application result bundle. |
| Scalability | Read-only synthetic SQLite, one retained Agent per UI context with bounded run/request receipts, small static DAG and whole-run calls/time/token/result/retained/trace ceilings; separate Library adapter exercises common core. | Multi-user auth/tenant quotas, admission queues, benchmarked concurrency, distributed saver/trace stores, concurrent writers or another SQL dialect. Same-core portability is not universal SQL or an automatic production migration. |
| Observability | Same-run JSONL input/nodes/provider/SQL proposals/validation/execution/raw typed rows/adapted results/binds/resume/answer-or-error; English panels/downloads, primary error preservation, no success on trace failure. Actual offline browser examples are source-cutoff labeled. | Central protected searchable traces, retention/PII policy, alerts/on-call, audited long-term storage; no secret/raw private payload publication or claim that a trace grants data/publication permission. |
| Security/privacy | Explicit server-owned session continuation, client echo never authority; AST/table/function allowlists, typed bound values, read-only URI/authorizer/watchdog, catalog/integrity scans and unchanged DB hashes. Fixtures/injection require explicit test environment and never normal-profile fallback. Actual ledger/I1/locks preserved offline. | Public authentication/authorization/row-level isolation, OS memory sandbox, hardened network/secret manager/dependency threat model and real personal-data policy. Safe SELECT is not proof of intended semantics; independent oracle still catches wrong aggregation/JOIN. Never expose this unauthenticated synthetic UI as a public service. |
| Deployment/cost | Existing locked Python/SQLite/LangGraph/Streamlit stack; temporary isolated offline DB/runtime/UI tests and exact source/hash/local-checkpoint receipts. Offline tasks load no credentials and make0 paid/count calls; original monetary holds/cap/history remain unchanged. | I4 real-model accuracy protocol/authorization and clean release checks, I5 publication permission/fresh remote/anonymous access/defense, hardened container/CI/CD/TLS/rollbacks/backups and live cost governance. No new spending authority from offline completion. |

Bounds remain conservative application limits, not guarantees under arbitrary OS/filesystem
stalls; failed attempts remain evidence and do not authorize raised product ceilings.
The accepted Sol high/medium/medium profile, deterministic formatter and independent
oracle remain; future verbalization/judge assessment above stays an obligation to
compare, not permission to add live calls or new judges here. Final offline DoD,
source identity, invariant audit, independent review and remaining live/publication/
owner-defense obligations are reported separately. Absence of live/push authority
is not a blocker to this offline block, but does not close those later obligations.

Current supported DB identity is DELETE-journal only; WAL/non-DELETE is rejected at
startup and before execution/resume/replay, not converted or silently hashed as if
main-file SHA represented WAL-visible data. Concurrent writer/snapshot support is
future work. Server-session request registry keeps32 immutable IDs/tombstones and
8unexpired contexts; capacity/900s inclusive expiry fail closed, with explicit new
session recovery rather than automatic identity eviction. These are demo bounds, not
public authentication or durable cross-restart exactly-once guarantees.
