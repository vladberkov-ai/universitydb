# ADR-OMX-003 — Минимальный локальный стек

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
Нужны настоящий LangGraph, SQL, простой экран и полная трасса, срок ограничен. Продуктовых dependencies пока нет.

## Варианты
SQLite/direct LangGraph/OpenAI SDK/Streamlit/local JSONL; PostgreSQL+API/UI+LangSmith; CLI-only.

## Рекомендация
Первый вариант; кандидат Python3.13/LangGraph1.2.20/openai3.46.0/Streamlit1.67.0, compatibility ещё проверить. Luna baseline, snapshot Mini или Sol отдельные evaluation profiles.

## Обоснование
Минимум сервисов и явная диагностируемость. CLI не покрывает экран; серверный вариант viable, но избыточен сейчас.

## Последствия
Собственный trace contract, отсутствие HA/remote auth и stable model alias; key/access/budget неизвестны. Prices/pins из dated research, не guarantee.

## Проверка
Clean lock/install+security audit, реальный vertical slice S6, версии/usage/trace, full E2E. До live explicit budget; никаких calls в B.

## Пересмотр
Concurrent writers/remote users, measured low Luna quality, изменившиеся API/цены или restart requirement.

Связанные [архитектура](../plans/architecture-proposal.md), [контракты](../plans/contracts.md), [проверки](../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
