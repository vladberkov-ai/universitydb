# ADR-OMX-004 — Идентичности и арифметика предметной области

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
PDF требует имена, курсы/семестры/учителей/enrollments/оценки, но не задаёт scale/retakes/weights/ties.

## Варианты
Нормализованные Offering/Enrollment; одна Course запись на каждое проведение; co-teaching junction; credit weights/latest-retake-only.

## Рекомендация
Students/Teachers имена nonunique, стабильные ID; Course→Offering с одним teacher/semester; grade nullable integer hundredths от0до10000; external decimal0..100; равные веса graded enrollments, all-retakes, все exact ties, all-semesters default.

## Обоснование
Разделяет курс и проведение, предотвращает silent identity merge, арифметика объяснима по малым fixtures без скрытых weights/current date.

## Последствия
Пересдачи внутри offering/co-teaching не моделируются; среднее курса не среднее средних. NULL не0. Любое изменение правил меняет oracle.

## Проверка
S1–S14 real DB constraints/aggregates, C1 duplicate-name clarification, точные рациональные tie comparisons, documented fixtures.

## Пересмотр
Владелец выбирает credit-weighted/latest-only/co-teaching/history или иной default semester.

Связанные [архитектура](../plans/architecture-proposal.md), [контракты](../plans/contracts.md), [проверки](../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
