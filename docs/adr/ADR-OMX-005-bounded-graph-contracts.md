# ADR-OMX-005 — Bounded graph, clarification и безопасность

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
Нужны meaningful multistep, ошибки и продолжение; LLM proposals недоверенные, interrupt перезапускает node.

## Варианты
Свободный agent loop; фиксированная цепочка без уточнений; bounded graph с typed state и checkpoint.

## Рекомендация
Bounded LangGraph по contracts v1: static validate_plan принимает typed symbolic refs по declared ResultSpec; runtime bind_results требует completed/consistent/nontruncated dependencies, error→no downstream. InMemorySaver для local demo, session-bound idempotent resume, 3 steps+1 repair,5calls,2clarifications; DB readonly/authorizer/limits/watchdog, deterministic formatter.

## Обоснование
Ограниченные ошибки/стоимость, объяснимые dependencies; free loop труднее отладить, chain без clarification нарушает scope.

## Последствия
После restart resume expired; safety не доказывает semantic correctness; limiter/policy тоже требуют actual DB testing; не обещаем arbitrary SQL correctness.

## Проверка
D1–D3,V1,W1–W3,C1–C5,E1–E7,SQL-policy integration,M1 sensitivity; no pre-interrupt side effects; pause budgets preserved.

## Пересмотр
Durable restart/multi-user requirement, новые operations/dialect, сложные >3step legitimate cases.

Связанные [архитектура](../plans/architecture-proposal.md), [контракты](../plans/contracts.md), [проверки](../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
