<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 1

**Verdict: `iterate`**
**Роль:** отдельный Architect; не Critic.
**Статус решений:** proposed; этот review не разрешает реализацию или закрытие Advisory.

## Summary

Рекомендованный минимальный стек, предметная модель и большая часть независимых эталонов архитектурно обоснованы. Однако три стыка требуют документального исправления: валидация зависимого плана, передача семантики агрегатов между адаптерами и воспроизводимость отрицательных live/E2E-проверок. Поэтому **APPROVE сейчас не даю**.

## Проверенный baseline и границы evidence

Полностью прочитан `.omx/plans/H-006-B2/iteration-1/plan-bundle.md`: 465 строк, все 12 составляющих документов.

**Raw SHA-256:**
`b83dadcc0ea53f63afea1e2bfe7da3b562dba5313cc06cbe8b6c114961755fc6`

Проверены:

- `.omx/plans/H-006-B2/iteration-1/manifest.json`: все **13/13** файлов совпадают по размеру и SHA-256; включает bundle.
- Все **12/12** constituent documents совпадают с соответствующими разделами bundle.
- Повторный raw hash bundle перед завершением review совпал.
- **25/25** текущих vault inputs совпадают с `current_sha256` в `.omx/context/H-006-B2/inputs-observed.json`.
- Текущий HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`.
- Прочитаны полный authoritative H-006-v5 handoff, actual task, context/activation/Planner completion/baseline receipts, свежая D2, принятая актуальная R/U matrix, acceptance contract, scope/ownership ADR и оба сохранённых research-final.
- Original PDF независимо повторно не декодировал: использован предоставленный лидером `.omx/context/H-006-B2/pdf-read-receipt.json`, фиксирующий чтение четырёх страниц. Это **не собственная повторная PDF-проверка Architect**.
- Researcher/dependency-expert материалы от 2026-11-07 использованы как **ранее выполненное исследование**, не новые исследования или reviewer approvals.

Выполнен независимый пересчёт документальных fixtures посредством целочисленной/рациональной арифметики — **не SQL, не продуктовый тест**. Подтверждены S1–S6, M1/F1 `95.00`, M1/F2 `{95.00,80.00,50.00}` и tie mutation `{90.00,90.00,null}`.

Файлы, Git, runtime state, tracker и Obsidian мною не изменялись. Review передаётся лидеру текстом для сохранения отдельного immutable artifact.

## Положительные архитектурные выводы

1. **Предметная модель согласована с большинством эталонов.** Course отделён от Offering; имена не являются ключами; NULL, пересдачи между offerings, равные веса, all-semesters default и exact ties явно proposed. Fixtures различают среднее по строкам и среднее средних, а M1 проверяется изменением данных, меняющим промежуточный cohort.
   Evidence: `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:25–39`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:27–52`.

2. **Оркестрация действительно bounded на уровне проекта.** Есть общие call/SQL/repair/clarification budgets, отключение SDK retries, отдельные provider branches, session-bound resume, replay protection, restart expiry и запрет побочных эффектов перед interrupt. Известная особенность повторного запуска interrupt-node учтена.
   Evidence: `.omx/plans/H-006-B2/iteration-1/contracts.md:5–13,32–35,44–49`.

3. **Безопасность не выдана за семантическую правильность.** Read-only, authorizer, allowlists и watchdog отделены от oracle-based проверки правильности ответа; plausible wrong SELECT честно остаётся ограничением. Trace failure не превращается в success.
   Evidence: `.omx/plans/H-006-B2/iteration-1/contracts.md:29–39`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:64–74`.

4. **Переносимость имеет проверяемый ограниченный scope.** Library — конкретная вторая схема, с expected и zero-return variant; предусмотрены неизменность core hash, реальные DB/live/E2E проверки. Не заявляется поддержка произвольных SQL dialects.
   Evidence: `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:41–42`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:76–84`.

5. **Документальный lifecycle не смешан с продуктовой готовностью.** Все 17 R и 8 U имеют строки будущих доказательств; public access, owner defense, реальные prompts и Git отдельно от приложения. ADR003–007 содержат варианты, причины, последствия, проверки и условия пересмотра. Три pre-mortem и расширенные уровни проверок присутствуют.
   Evidence: `.omx/plans/H-006-B2/iteration-1/requirements-test-matrix.md:3–33`; `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:44–49`; `.omx/plans/H-006-B2/iteration-1/plan-bundle.md:6–165`.

## Blocking findings

### B1 — Не разделены статическая проверка DAG и runtime binding результатов

**Приоритет:** P1. **Исправление:** небольшое/среднее, документальное.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/contracts.md:27,45–46`
`.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:37–39`

Контракт требует, чтобы references указывали только на уже завершённые steps, запрещает future references и требует существующие typed columns. Одновременно единственный начальный `PlanProposal` должен содержать весь план до SQL-выполнения, а `Step` не объявляет схему своего результата.

**Контрпример:** обязательный M1 должен заранее содержать зависимость step2 от `step1.course_id`, а step3 — от `step2.student_id`. В момент принятия `PlanProposal` ни один результат ещё не существует. Буквальная проверка контракта отклонит корректный M1; другая реализация молча отложит проверку, хотя нормативный момент её выполнения не определён.

Это не требование заранее знать будущие **значения**. Требуется различить плановую ссылку и разрешённую для выполнения привязку.

**Минимальная поправка:**

- При приёме плана проверять уникальные IDs, DAG, топологическое направление и объявленные выходные имена/типы предыдущих steps.
- Будущие результаты предыдущих по DAG steps разрешать как **unresolved symbolic references**.
- Непосредственно перед генерацией/исполнением зависимого SQL требовать завершённый, непротиворечивый, нетранкированный результат и материализовать reference в типизированные значения.
- Определить failure code для отсутствующей/неверно типизированной колонки и запрет downstream calls при ошибке.
- Добавить валидный полный M1 PlanProposal, invalid cycle, missing column и runtime truncated-reference examples с expected.

**Проверка исправления:** документальный M1 проходит обе фазы, но cycle, отсутствующая колонка и oversized cohort останавливаются на явно указанной фазе без следующего SQL.

### B2 — Formatter/validator обещают семантические проверки, но результат не связан с metric/grain/unit

**Приоритет:** P1. **Исправление:** среднее, без смены стека.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/contracts.md:27–30,42,45–48`
`.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:32,42`

Formatter должен проверять grain, scoped IDs, `graded<=enrollment`, диапазоны и переводить `sum_units/count/100`. Но нормативные `SQLProposal`/`DBResult` несут свободные имена колонок и scalar types, не обязательную связь с метрикой, единицей, агрегатными компонентами или grain. `Metric` содержит описание, но результат не указывает, к какой записи Metric он относится.

**Контрпример:** `expected_columns=["average"]` и decimal result допустимы по контракту. Из них нельзя определить, содержит колонка среднее в физических hundredths, уже нормализованную оценку или другую decimal-метрику. Нельзя восстановить точные `sum/count` для tie comparison, если вернулся только округлённый average. Аналогично не определено, какой adapter обязан реализовать University-specific проверки, чтобы core не начал распознавать названия `grade`/`graded_count`.

Это **не** требование доказать произвольную NL→SQL семантику. Речь о заявленных детерминированных правилах единиц, результата и domain boundaries.

**Минимальная поправка — один из двух вариантов:**

1. Небольшой `ResultSpec` у шага: metric/result-shape identifier, group keys, typed aliases, unit/scale и требуемые aggregate components; либо
2. Явный контракт domain result adapter, который получает проверенную спецификацию и DBResult, выполняет domain validation/normalization и возвращает унифицированный Answer.

Для average/top определить обязательные integer `sum_units` и `graded_count`, владельца точного сравнения/финального округления, правила нулевого знаменателя. Core не должен реализовывать University-specific семантику по названиям колонок.

**Проверка исправления:** показать concrete messages для S6, M1/ties и Library count, включая неверную единицу/недостающий denominator/неожиданный grain. Они должны иметь однозначные результаты без эвристик по свободному имени колонки.

**Принципы:** сейчас не завершено обеспечение принципов 2 и 5 — «вычисляет БД, не модель» и schema-agnostic core. Это проектный пробел границы, не доказанный дефект существующего кода.

### B3 — Отрицательные live/E2E cases не имеют воспроизводимого механизма воздействия

**Приоритет:** P1. **Исправление:** небольшое/среднее, test-plan.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/test-plan.md:64–72,82–92`

E3 требует refusal/incomplete/malformed output. Эти случаи корректно предусмотрены для scripted-provider graph tests. Однако затем E3 включён в **full E2E с actual model**, а category `failure/refusal/invalid SQL` включена в обязательные 24 held-out real-model cases с двумя успешными повторениями.

Не указано, какие faults вызываются настоящим provider, какие вводятся тестовым transport/adapter и какие являются обычными отрицательными пользовательскими вопросами. Намеренно получить invalid SQL или refusal от настоящей модели — не воспроизводимый fault-injection контракт.

**Контрпример:** настоящий provider отвечает корректным structured proposal вместо ожидаемой искусственной SQL-ошибки. Проверка обработки ошибок формально не состоялась, но это не свидетельствует о плохом NL→SQL. Обратная ошибка — подменить response и затем засчитать результат как live generation evidence.

**Минимальная поправка:**

- Оставить все E3 branches в обязательных deterministic injected tests.
- Для UI/E2E явно маркировать injected provider/transport faults и сохранять источник воздействия; не включать их в real-model generation score.
- В live suite определить конкретные negative-user-request classes и допустимые наблюдаемые outcomes; не требовать от модели сгенерировать ошибочный SQL ради прохождения теста.
- Если нужен отдельный live provider-failure experiment, описать механизм, expected и стоимость; не обещать неподтверждённое поведение API.
- Уточнить denominator/category mapping и бюджет после разделения. Сам proposed строгий порог не отвергается.

**Проверка исправления:** для каждого отрицательного case понятно, что реально вызывается, что подменяется и какое именно свойство доказывается.

**Принцип:** текущее смешение рискует нарушить принцип 4 — разделение безопасности, семантики и доказательств.

## Advisory findings

### A1 — Strict provider schema mapping следует определить явно

`contracts.md:3` объявляет закрытые JSON objects, а `contracts.md:48` использует динамический `parameters` map. Уже прочитанное research предупреждает о подмножестве JSON Schema и закрытых объектах.

Разделение external/provider schema признано, но преобразование ещё не описано. Рекомендуется explicit wire representation — например, ограниченный массив `{name,value}` с проверкой уникальности — и deterministic conversion в DB bindings. Нужен пример strict SQLProposal schema/normalization и будущий compatibility smoke. Это **не утверждение**, что выбранные candidate packages уже несовместимы.

### A2 — Ресурсные пределы требуют отдельных будущих boundary tests

`contracts.md:33–34` хорошо ограничивает calls, время и возвращаемые bytes, но эти caps сами по себе не ограничивают память SQLite до выдачи первой строки. `production-considerations.md:13` честно оставляет hard memory enforcement отдельной работой.

До I1 следует выбрать scoped SQLite limits/worker resource policy либо явно сохранить остаточный риск. Добавить тесты input-token overflow, SQL/parameter size и очень крупного одиночного значения. Не считать прохождение обычного timeout теста доказательством memory isolation.

### A3 — Уточнить видимость SQL/данных/trace на демонстрационном экране

`test-plan.md:84` перечисляет trace ID, но принятый scope включает показ ответа, SQL, данных и полной трассы (`docs/chat/decisions/ADR-CHAT-002-result-scope.md`, раздел «Решение»). Простого ID недостаточно для практического walkthrough без определённого способа открыть соответствующие события. Достаточен локальный expander/просмотр или явная доступная ссылка; отдельная tracing platform не нужна.

## Root cause

Документы хорошо описывают компоненты по отдельности, но местами заменяют **контракт передачи между компонентами** обещанием поведения: «проверить typed reference», «проверить grain», «показать real-provider failure». Нужна не новая архитектура, а несколько нормативных связок с конкретными сообщениями и фазами проверки.

## Trade-offs и consensus addendum

### Antithesis — strongest steelman

Для небольшого учебного демонстратора свободный read-only SQL agent, независимые fixtures и прозрачная трасса могут быть достаточны. Добавление богатого typed query/result IR рискует превратить короткий проект в собственный SQL compiler и ухудшить принцип минимальности. Нельзя требовать универсального доказательства NL-семантики, которое сам план справедливо не обещает.

### Реальное tradeoff tension

| Вариант | Польза | Цена |
|---|---|---|
| Свободный SQL и свободные result columns | Минимум адаптерного кода, широкий NL scope | Неоднозначные units/grain/dependencies; formatter вынужден угадывать |
| Полный typed query IR с генерацией SQL | Сильная структурная проверяемость | Существенный объём, ограничение выразимости, риск scope creep |
| **Минимальный ResultSpec + двухфазные references** | Ясные units/aggregate outputs и зависимые переходы; сохраняет настоящий NL→SQL | Небольшой дополнительный контракт и domain adapter tests |

### Synthesis

Сохранить предложенный минимальный стек и свободную генерацию SQL внутри проверяемого безопасного subset. Добавить только небольшой result contract для поддерживаемых метрик и разделить symbolic plan references от runtime bindings. Semantic oracle остаётся независимым от модели; никакой контракт не объявляется доказательством произвольной правильности SQL.

Proposed owner decisions — scale, retakes, default semester, model, budget, strict small-suite gate — **сами по себе не blockers**: рекомендации, альтернативы и условия пересмотра представлены.

## Рекомендации и stop condition

1. Исправить B1/B2 в контрактах и согласовать M1/S6/Library examples; не создавать приложение или executable schema.
2. Исправить B3 в test-plan и соответствующих matrix/ADR references.
3. Передать этот review отдельному Critic текущего цикла; мой verdict не заменяет его проверку. Последующую revision проводить через предусмотренный полный цикл.
4. Дополнительное research для указанных документальных исправлений не требуется. Выбор конкретного parser/tokenizer или нового provider-failure механизма потребует отдельного scoped verification, если Planner решит его добавить.

**Review завершён; verdict `iterate`.** Продуктовые tests/live/API compatibility/security execution — **not-run**. Terminal lifecycle, native completion и closeout проверяет лидер после фактического завершения этого агента. Execution authorization отсутствует.

<!-- END_ARCHITECT_REVIEW -->
