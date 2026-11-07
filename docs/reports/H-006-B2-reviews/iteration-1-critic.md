<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 1

**REJECT текущую редакцию; workflow verdict: `iterate`.**

Пакет содержателен, но пока не позволяет реализовать обязательные сценарии без догадок. Независимо подтверждены три blocking findings Architect; ещё один пробел касается уже принятого состава демонстрационного экрана. Требуется документальная Planner revision и новый полный Architect → Critic цикл. Этот review не разрешает реализацию, публикацию, paid calls или execution handoff.

## Проверенное основание

Полностью прочитаны actual task, grounded context, authoritative H-006-v5 пакет, актуальные требования и acceptance contract, все 12 constituent documents в bundle, завершённый Architect review, сохранённые researcher/dependency-expert final texts. Исследования использованы как **исторические входы от 2026-11-07**, не новые исследования или approvals.

Read-only проверки:

- Все **13/13** raw hashes и размеры из `iteration-1/manifest.json` совпали.
- Все **12/12** constituent documents byte-equivalent соответствующим разделам bundle.
- Raw SHA-256 bundle до завершения review:
  `b83dadcc0ea53f63afea1e2bfe7da3b562dba5313cc06cbe8b6c114961755fc6`.
- Raw SHA-256 прочитанного Architect review:
  `2b6aec6d1b8b68926e53c5ba42d08e7a3df81e03825ec4a5fed35bfba73b9e3e`.
- **25/25** текущих vault hashes совпали с `inputs-observed.json.current_sha256`. Пять отличий от исторического manifest уже объяснены D2; это не новые изменения требований.
- HEAD остаётся `8931d832d49311ac0d63c3a7a359b4293058da89`.
- В matrix присутствуют **17 R + 8 U** строк.
- `omx quality-gates list --stage ralplan --json` вернул `gates:[]`. Это не заменяет обязательные reviews.
- Прочитана реализация установленного `digestAdvisoryArtifacts`: штатные artifact/manifest digests используют domain-separated `hashParts`, поэтому не обязаны равняться raw `sha256sum`. Различие baseline digest и raw hash **не является найденной подменой**.

Независимо пересчитаны documentary fixtures целочисленной/рациональной арифметикой:

- S1–S6: суммы в физических hundredths `50000/35000/40000/25000/26000/16000`; counts и averages соответствуют таблице.
- M1/F1: top C2, cohort `{1}`, результат `95.00`.
- M1/F2: top C1, cohort `{1,2,3}`, результаты `{95.00,80.00,50.00}`.
- Tie mutation: top `{C1,C2}`, результаты `{90.00,90.00,null}`.

Это **не выполнение SQL, приложения или продуктовых тестов**. Original PDF повторно самостоятельно не декодировал: использован явно предоставленный leader receipt чтения четырёх страниц, сверенный по hash PDF. Файлы, Git, tracker, state и Obsidian мною не изменялись; субагенты не запускались.

Далее `P/` означает `.omx/plans/H-006-B2/iteration-1/`.

## Summary

- **Clarity:** основные решения конкретны; фазы dependency validation и семантика передаваемого результата неоднозначны.
- **Verifiability:** независимые fixtures и sensitivity сильные; live fault cases пока не воспроизводимы.
- **Completeness:** документы и все R/U строки присутствуют; четыре указанных стыка ещё не закрыты.
- **Big Picture:** компактный локальный demonstrator соответствует принятому направлению; proposed/accepted/actually-tested разделены правильно.
- **Principle/Option Consistency:** **fail локально** — unit/grain boundary не обеспечивает заявленную независимость core; смешение live generation и injected faults ослабляет принцип разделения доказательств.
- **Alternatives Depth:** **pass** — минимальный локальный и серверный варианты рассмотрены содержательно; CLI справедливо исключён как единственный интерфейс.
- **Risk/Verification Rigor:** **fail до B1–B4**; ограничения безопасности, semantic correctness и public delivery в остальном описаны честно.
- **Deliberate Additions:** три credible pre-mortem и расширенный unit/DB/mock/live/E2E/observability/manual/public/defense план **присутствуют**. Их наличие не устраняет противоречия конкретных сценариев.

## Blocking findings

### B1 — Полный зависимый план противоречит правилу «references только к завершённым steps»

**Evidence:** `P/contracts.md:27,45–46`; `P/architecture-proposal.md`, раздел «Граф и содержательный dependent path».

`PlanProposal` создаётся до выполнения SQL и содержит весь DAG. Однако references разрешены только к завершённым steps и существующим typed columns; `Step` даже не объявляет выходную схему.

**Симуляция:** при приёме M1 корректная ссылка второго шага на первый ещё не может указывать на завершённый результат. Буквальная реализация отвергнет M1; другая реализация отложит проверку по собственному усмотрению.

**Минимальное исправление Planner:**

1. Разделить static plan validation и runtime result binding.
2. В static фазе разрешить unresolved symbolic references к предшественникам DAG, проверяя IDs, ацикличность, направление и объявленные output columns/types.
3. Перед dependent SQL требовать завершённый нетранкированный результат и материализовать typed values.
4. Назначить точные failure codes и фазу отказа для missing column/type mismatch/truncated dependency.
5. Добавить конкретный валидный M1 plan и отрицательные cycle/missing-column/runtime-overflow examples.

**Pass:** M1 план принимается до SQL; его ссылки связываются только после соответствующих результатов; каждый отрицательный пример останавливается на указанной фазе без downstream call.

С Architect B1 **согласен по собственному чтению**.

### B2 — Metric/grain/unit не связаны с результатом, хотя formatter обязан их проверять

**Evidence:** `P/contracts.md:28–30,42,45,47–48`; `P/architecture-proposal.md`, разделы предметной арифметики и schema-agnostic boundary.

`Metric` имеет описание/unit/grain, но ни Step, ни SQLProposal, ни DBResult нормативно не связывают конкретный результат с этой метрикой. `expected_columns` задаёт только имена. Formatter при этом должен проверять grain, units, counts и выполнять нормализацию.

**Симуляция S6:** DBResult с колонкой `average` и decimal-строкой не сообщает, означают ли числа physical hundredths или внешние оценки. Из уже округлённого среднего нельзя восстановить точное сравнение ties. Library count требует другого правила, но место его реализации не определено.

**Минимальное исправление Planner:**

- Добавить небольшой result specification либо явный domain-result-adapter contract: metric/result-shape ID, group keys, typed aliases, unit/scale, необходимые aggregate components.
- Для average/top закрепить integer `sum_units` и `graded_count`, владельца exact comparisons и финального rounding, zero-denominator/NULL поведение.
- Не переносить University-specific проверки в core через распознавание имён колонок.
- Показать concrete messages и expected для S6, M1/ties, Library count и ошибок wrong unit/missing denominator/wrong grain.

**Pass:** сообщения однозначно преобразуются в `80.00`, корректный набор ties и Library counts без эвристик по имени `average`. Неверные формы дают указанную ошибку, не plausible answer.

С Architect B2 **согласен**. Полный typed SQL compiler не требуется.

### B3 — Live generation suite требует ошибок, которые нельзя воспроизводимо получить от модели

**Evidence:** `P/test-plan.md:64–72,82–92`; связанные `P/requirements-test-matrix.md` R-07/R-08, `P/ADR-OMX-007-verification-delivery.md`.

E3 deterministic refusal/incomplete/malformed responses включены затем в full E2E с actual model. Категория `failure/refusal/invalid SQL` также входит в обязательные 24 held-out cases ×2, но механизм воздействия не определён.

**Контрпример:** настоящая модель генерирует корректный SQL вместо ошибочного. Обработка SQL-ошибки не была проверена, но это не дефект NL→SQL. Подменить ответ transport fixture и засчитать его как live generation — обратная методологическая ошибка.

**Минимальное исправление Planner:**

1. Все provider/SQL failure branches оставить обязательными controlled injected tests.
2. Отдельно определить UI/E2E fault-injection lane с provenance воздействия; не включать его в live generation score.
3. Live negative cases задавать пользовательскими запросами с конкретными допустимыми outcomes, не требованием намеренно получить ошибочную генерацию.
4. Явно обозначить unexpected provider failures как неудачные live attempts.
5. Согласовать категории, denominator, repetitions, budget и ADR/matrix после разделения.

**Pass:** для каждого negative case ясно, какой компонент реальный, что именно инъецировано и какое свойство доказывает результат. Mocks/injections не считаются NL→SQL accuracy.

С Architect B3 **согласен**. Сам предложенный strict small-suite threshold не отвергаю: он честно proposed и не назван статистической гарантией.

### B4 — Экран с одним trace ID не покрывает уже принятые SQL/данные/полную трассу

**Evidence:** accepted `docs/chat/decisions/ADR-CHAT-002-result-scope.md`, раздел «Решение»; `P/test-plan.md:84,102`; `P/requirements-test-matrix.md` R-06/R-17.

Принятый scope включает экран с ответом, SQL, данными и полной трассой. Конкретный screen acceptance перечисляет question/answer/clarification/error/**trace ID**, но не просмотр SQL, typed DB rows и всей цепи событий.

**Контрпример:** экран показывает правильный ответ и непрозрачный ID; JSONL существует на диске, но демонстратор не даёт открыть его из согласованного интерфейса. Текущий screen checklist допускает такой результат.

Это Architect A3, которое я **поднимаю до blocking** из-за прямого accepted scope, а не нового предпочтения UI.

**Минимальное исправление Planner:**

- Нормативно указать простой локальный expander/view либо доступную ссылку, открывающую SQL с безопасными bindings, DB columns/rows и полный trace того же run.
- Добавить manual/E2E pass-fail для success, clarification/resume и error с несколькими attempts.
- Согласовать R-06/R-17, implementation I1/I4 и scope walkthrough.

**Pass:** наблюдатель из экрана может проследить конкретный вопрос до SQL, фактических строк и ответа/ошибки; совпадают run/trace IDs; trace ID без доступного содержимого — fail. Отдельная tracing platform и UI implementation в B не нужны.

## Advisory, не самостоятельные blockers

1. **Strict provider wire representation.** `P/contracts.md:3,27,48`: closed objects и динамический parameter map требуют явного wire/domain mapping до compatibility smoke. Полезен небольшой пример bounded list bindings с deterministic conversion; конкретное представление выбирает Planner. По архивному research нельзя заявлять, что candidate stack уже установлен или заведомо несовместим.

2. **Resource boundary coverage.** `P/contracts.md:33–34`; `P/production-considerations.md`: добавить отдельные будущие boundary tests для input-token limit, SQL/parameter size и большого одиночного DB value. Timeout/result caps не выдавать за hard memory isolation; текущий residual risk обозначен честно.

Новые внешние research calls для B1–B4 не требуются. Если revision выбирает новый parser, tokenizer или provider-fault mechanism, фактуру по нему следует отдельно проверить, а не добавлять из памяти.

## Проверка покрытия пакета

| Область | Оценка |
|---|---|
| R-01/02: ERD, имена, offerings, semesters, grades | Достаточный предложенный дизайн и конкретные fixtures; domain правила не выданы за PDF |
| R-03/04: LangGraph, JOIN/filters, dependent reasoning | Oracle/sensitivity сильные; B1/B2 блокируют однозначный контракт выполнения |
| R-05: переносимость | Конкретная Library schema и unchanged-core проверка есть; result boundary требует B2 |
| R-06: полные traces | Содержание/attempts/errors/redaction предусмотрены; экранная демонстрация требует B4 |
| R-07/08: ошибки, SQL/NL/E2E | Уровни в основном разделены правильно; B3 нарушает воспроизводимость live отрицательных сценариев |
| R-09/10: модули и production | Ответственности и пять production тем раскрыты; production-ready не заявляется |
| R-11..15: комплект и public delivery | Будущие evidence/clean clone/SHA/anonymous access предусмотрены; local commit не подменяет public proof |
| R-16/17: объяснимый demonstrator/защита | Наблюдаемая owner rehearsal предусмотрена; B4 нужен для полного демонстрационного scope |
| U-01 | Actual/template/read-context и omissions различены; приложенная received-task projection не означает full native transcript coverage |
| U-02 | Даты сохранены; точный час честно open |
| U-03 | Реальный lifecycle должен подтвердить лидер; reviews не заменены prompt labels |
| U-04 | ADR003–007 содержат варианты/обоснование/последствия/проверку/пересмотр |
| U-05/06 | Ownership, сохранение A/истории, отдельный B commit и запрет remote/push отражены |
| U-07 | Исторический verified переход не выдан за новый результат B |
| U-08 | Будущий глубокий разбор/самостоятельное объяснение предусмотрены, но ещё не выполнены |

Отсутствие credentials, owner acceptance и public authority **не блокирует documentary B**; оно блокирует соответствующие будущие live/public действия. Proposed domain decisions сами по себе не недостаток: рекомендации и альтернативы представлены.

## Сильнейшая альтернатива и синтез

Steelman против усиления контрактов: маленькому учебному SQL agent могут быть достаточны read-only SQL, независимые oracle и прозрачные traces; слишком богатый IR превратит демонстратор в собственный query compiler и нарушит минимальность.

Реальное напряжение: свободный SQL даёт простоту и выразительность, но свободные units/grain/references вынуждают downstream угадывать. Полный compiler чрезмерен.

**Синтез:** сохранить предложенный стек и свободную SQL generation, добавить только двухфазные references и небольшой result contract для поддерживаемых shapes. Независимый oracle остаётся обязательным; runtime validation не объявляется доказательством произвольной NL semantics.

## Stop condition и handoff

Передать **полный этот review и завершённый Architect review Planner**. Исправить B1–B4 в новой immutable iteration, согласовав contracts/examples/test-plan/matrix/ADR/implementation, затем выполнить новый отдельный Architect → отдельный Critic цикл и актуальные configured gates. Не patch-ить reviewed baseline.

**Approval текущей iteration отсутствует.** До passing reviews не считать B согласованным и не закрывать его как approved/proven архитектуру. Поддерживаемый closeout, native completion/provenance, prompt packaging и commit проверяет лидер. Никакой execution authorization не создано.

<!-- END_CRITIC_REVIEW -->
