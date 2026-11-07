# ADR-OMX-007 — Независимые oracle, live gate и delivery evidence

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
Mocked graph не измеряет NL-SQL. Ранее предложенный27/30 снят; процент не заменяет обязательные R/U. Saved/committed/public различны.

## Варианты
Единый success percentage; только unit mocks; layered checks+independent fixtures+small strict live suite/manual/public gates.

## Рекомендация
S/C/E/T/L+D/V/W/UI1 mandatory tests; EI1–EI3 deterministic injected UI lane с provenance и0 paid calls отдельно, 24dev+24heldout×2 counted runs; proposed48/48 **real-model conversations** semantic passes, включая4negative-data cases×2, без injected faults в denominator без unsafe/privacy failures; <=$2 approved cap; ручная защита и public SHA отдельно.

## Обоснование
Малый демонстратор должен воспроизводить каждый обещанный сценарий; strict повторение обнаруживает нестабильность, но не статистическая гарантия на произвольные вопросы.

## Последствия
Gate может потребовать prompt/model refinement и свежих heldout; нельзя best-of/relabel failures. Budget/key/public authority ещё отсутствуют; B только docs.

## Проверка
test-plan oracle/manual раскрытый SQL/DB/full trace path, N1–N4 real-model no-data outcomes vs injected E1–E7/EI1–EI3; unexpected provider failures count failed live attempts, all attempts+hashes/usage, clean clone, remote SHA anonymous access, observed owner explanation; current application checks not-run.

## Пересмотр
Owner-approved revised scope до eval, token-rate changes, dataset contamination, новый model/prompt/schema или наблюдаемый failure pattern.

Связанные [архитектура](../plans/architecture-proposal.md), [контракты](../plans/contracts.md), [проверки](../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
