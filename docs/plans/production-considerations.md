# Production considerations — проект

Proposed 2026-11-07; приложение ещё не создано, **не production-ready**. «В задании» ниже означает план, не выполненное свойство.

| Тема | План для компактного задания | До production дополнительно |
|---|---|---|
| Reliability | typed contracts, bounded retries/timeouts, no unsafe fallback, independent oracle, InMemorySaver с явной expiry после restart | durable checkpoints с безопасной сериализацией, migrations/backups/restore drills, failure recovery, HA/SLO/error budgets, provider outage strategy |
| Scalability | local read-only SQLite, один active request/UI session, small result/token caps | workload benchmark, queue/admission control, tenant quotas, connection pools; при concurrent writers рассмотреть PostgreSQL и новый dialect adapter/test suite; не переносить SQLite security policy вслепую |
| Monitoring/tracing | local complete versioned JSONL и screen expanders SQL/bindings/typed results/full trace, attempts/usage/cost/latency/error codes, synthetic public exports | searchable centralized storage, retention/access policy, dashboards/alerts p95 latency/errors/token spend, trace sampling не теряет audit/security events, on-call ownership |
| Security/privacy | loopback only, synthetic data, no keys in logs/repo, mode=ro+authorizer/allowlists+limits, process SQL watchdog, ingress/output checks | authentication/authorization/row-level access, tenant isolation, secret manager/rotation, dependency supply-chain audit, privacy/legal review, encrypted data/checkpoints, sandbox resource isolation, threat model/pentest |
| Deployment | reproducible Python+dependency lock/version receipt, clean clone instructions, local config presence checks | container/hardened runtime, CI/CD signed artifacts, rollout/rollback/migration gates, TLS/network policies, infra access controls, production cost governance |

Read-only ≠ semantic correctness; JSON schema ≠ correct SQL; trace completeness ≠ permission/publication; store=False ≠ zero retention. Progress handler cooperative, hard worker kill/memory enforcement должно быть отдельно реализовано/измерено. Отсутствие authentication приемлемо только loopback synthetic demo; не публиковать UI как доступный всем сервис. LangSmith optional future alternative после retention/billing/privacy review, не обязательная зависимость.

Будущая проверка: owner объясняет каждый tradeoff и показывает planned vs actual evidence; failed production feature не маскируется в assignment readiness. Revision triggers: реальные персональные данные, remote multi-user access, запись в DB, concurrent workloads, durable resume/recovery или новый provider/SQL dialect. Тогда нужен новый ADR/threat model, не механическое увеличение лимитов. См. [архитектуру](architecture-proposal.md), [тесты](test-plan.md).

Iteration2 уточнение: bounded SQL/bindings/input byte gates и oversized-value tests W1–W3 не доказывают hard memory isolation. SQLite может выделить память до fetch/progress handler; в local synthetic demo это явно residual risk. До remote/untrusted production требуется OS worker memory/resource policy и реальная adversarial проверка; новый dependency/parser/tokenizer в B не выбран.
