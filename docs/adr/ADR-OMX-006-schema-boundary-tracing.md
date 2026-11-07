# ADR-OMX-006 — Schema boundary и собственные traces

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
R05/R06 требуют адаптируемость и полную Input→Nodes→SQL→Results→Answer цепь; не требуют определённой платформы.

## Варианты
Domain names embedded in core; descriptor+domain adapter; generic arbitrary-dialect abstraction. JSONL или LangSmith.

## Рекомендация
Минимальный ResultSpec+domain result adapter: metric/group keys/typed aliases/unit/scale/components, точные sum_units+graded_count для averages/ties; nonnull integer sum_units через aggregate-level COALESCE(SUM(grade_units),0), различение пустоты/NULL-only/настоящего0 по denominator/enrollment_count; core не угадывает University по именам. SQLite-specific DB adapter, schema-agnostic core и University/Library descriptors; local versioned JSONL по contracts с full synthetic rows, redaction/public export отдельные.

## Обоснование
Вторая схема — реальный ограниченный transfer test; не заявлять поддержку всех dialects. Локальные traces не требуют account/network service.

## Последствия
Своя completeness проверка/retention, library scope только тот же dialect. Полные реальные PII не допустимы в demo. LangSmith требует отдельного billing/retention решения.

## Проверка
L1 same core hash+DB+live+E2E; V1–V2 units/grain/denominator failures; DB-Z actual raw components и отдельно UNIT-Z нормализация трёх zero cases; T1/T2+UI1 chain/completeness/screen access/secret exclusion; trace failure не success.

## Пересмотр
Новый dialect, real personal data, remote centralized tracing/retention/SLO requirement.

Связанные [архитектура](../plans/architecture-proposal.md), [контракты](../plans/contracts.md), [проверки](../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
