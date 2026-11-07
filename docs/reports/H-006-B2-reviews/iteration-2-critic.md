<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 2

**REJECT текущую редакцию; workflow verdict: `iterate`.**

Iteration 2 исправляет прежние B1/B3/B4 и основную часть B2. Независимо подтверждён остаточный **B2-R1**: нормативное выражение суммы несовместимо с non-null integer ResultSpec для пустого scalar aggregate. Требуется небольшая документальная revision, затем новый последовательный Architect → Critic цикл. Других blocking gaps при полном чтении текущего пакета не найдено.

Все архитектурные решения остаются **proposed**. Review не разрешает реализацию, paid calls, публикацию или execution handoff.

Далее `P/` означает `.omx/plans/H-006-B2/iteration-2/`.

## Проверенное основание

Прочитаны actual task и grounded context, полный authoritative H-006-v5 handoff, текущие requirements и acceptance contract, scope/ownership ADR, локальные ralplan/plan instructions, свежий D2 report, все 13 constituent documents текущего bundle, manifest и changes mapping. Прочитаны полные завершённые Architect1/Critic1 и **Architect2** reviews, baseline и Architect2 completion observation.

Сохранённые researcher/dependency-expert final texts прочитаны как **датированные reused inputs от 2026-11-07**, не новые исследования или approvals. Candidate pins не считаются установленными или проверенными совместно. Конкретного нового external-research gap не выявлено.

Read-only проверки:

- **14/14** manifest entries совпадают по raw SHA-256 и размеру.
- **13/13** constituent documents byte-equivalent соответствующим разделам bundle.
- Все **6** JSON-блоков bundle синтаксически разобраны.
- **25/25** текущих vault hashes совпадают с `inputs-observed.json.current_sha256`.
- Матрица содержит **17 R + 8 U**.
- `omx quality-gates list --stage ralplan --json` вернул `gates:[]`; это не заменяет обязательные reviews.
- HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, branch `main`.
- Bundle raw SHA-256 до и после review:

  `fe92a07802c9ba497948b0f22f9f4fdb2031ed83273062ae76765d6d99974e86`

- Прочитанный Architect2 review raw SHA-256:

  `445bcc65db20c1a1d5ec983cbc6aa41509dcdb394c1510f9b1dbecf2992a4fd8`

Штатный baseline использует domain-separated lifecycle digest, а manifest — raw hashes. Различие этих digest **не является признаком подмены**.

Original PDF самостоятельно повторно не декодировал: использован явно атрибутированный leader receipt чтения четырёх страниц; текущий PDF hash проверен среди 25 inputs. Completion observation Architect2 прочитан как evidence лидера, не выдан за независимо проведённый мною host lifecycle audit.

Независимая целочисленная/рациональная проверка документальных fixtures подтвердила:

- S1–S6: суммы hundredths `50000/35000/40000/25000/26000/16000` и соответствующие counts.
- M1/F1: top `{2}`, cohort `{1}`, итог `95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, итоги `{95.00,80.00,50.00}`.
- Tie mutation: top `{1,2}`, cohort `{1,2,3}`, итоги `{90.00,90.00,null}`.

Это арифметическая проверка документов, **не тест приложения**. Файлы, Git, state, IDs, tracker и Obsidian мною не изменялись; дети не запускались.

## Summary

- **Clarity:** высокий уровень конкретности; остаётся одно противоречие empty-aggregate representation.
- **Verifiability:** независимые fixtures, exact expectations, sensitivity и future evidence конкретны.
- **Completeness:** требуемые документы и все R/U присутствуют; B2-R1 блокирует согласованность обязательного no-rows сценария.
- **Big Picture:** компактный локальный demonstrator соответствует принятому scope; proposed/accepted/tested разделены.
- **Principle/Option Consistency:** **fail локально до B2-R1** — DB result должен удовлетворять объявленному typed normal path. Прочие прежние нарушения исправлены.
- **Alternatives Depth:** **pass** — локальный/серверный стек и упрощённый CLI рассмотрены честно; CLI не выдаётся за достаточный принятый экран.
- **Risk/Verification Rigor:** **pass кроме конкретного B2-R1**; safety, semantic correctness, live quality и public delivery не смешаны.
- **Deliberate Additions:** **pass** — три credible pre-mortem и расширенные unit/DB/mock/live/E2E/trace/manual/public/defense проверки присутствуют.

## Проверка исправлений iteration 1

| Finding | Результат Critic2 |
|---|---|
| **B1 — static/runtime dependencies** | **Исправлено документально.** Полный M1 допускает symbolic references до результатов; `validate_plan` проверяет объявленные outputs/DAG, `bind_results` — completed/consistent/nontruncated значения. Corrupted runtime state имеет отдельные negative cases. `GraphState.results` хранит уже отобранные dependency rows, raw candidates остаются в trace. Evidence: `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **B2 — metric/grain/unit boundary** | **Основная граница исправлена.** Конечный ResultSpec registry, domain adapter, integer components, exact ties, half-up2 и Library count normalization конкретны. Один остаточный blocking defect приведён ниже. Evidence: `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **B3 — live vs injected faults** | **Исправлено.** EI tests имеют injection provenance и 0 paid calls; live denominator — 48 real-model conversations, включая continuation. N1–N4 проверяют no-data outcomes, а не намеренную ошибку модели; unexpected failures не исключаются. Набор честно ещё не создан и не назван уже sealed. Evidence: `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **B4 — принятый экран** | **Исправлено.** SQL/bindings, typed DB rows и full same-run trace/attempts доступны из экрана; success/resume/error проверяются отдельно. Opaque ID и чужие старые rows — fail. Evidence: `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`; `P/implementation-plan.md:9–12`. |
| **A1 — strict provider bindings** | **Достаточно для documentary B.** Closed bounded array, discriminator validation и deterministic SQLite mapping описаны; actual SDK smoke остаётся future. Evidence: `P/contracts.md:238–241`; `P/test-plan.md:114–115`. |
| **A2 — resource boundaries** | **Достаточно с явным residual risk.** Есть byte/input/SQL/bindings/single-value boundaries; byte gate не выдан за exact tokenizer, watchdog — за memory isolation. Evidence: `P/contracts.md:243–244`; `P/test-plan.md:115–116`; `P/production-considerations.md:13–17`. |

## Единственный blocking finding

### B2-R1 — Внутренний COALESCE не нормализует пустой scalar SUM

**Приоритет:** P2. **Уверенность:** высокая. **Маршрут исправления:** Planner; малая документальная revision.

**Evidence:**

- `P/contracts.md:58` предписывает integer `SUM(COALESCE(grade_units,0))`, одновременно требует `sum_units=0` при нулевом denominator.
- `P/contracts.md:204–207` показывает `sum_units` как non-null integer в scalar mean ResultSpec.
- `P/test-plan.md:45,125` требует для C2/S2 normal `average=null`, `no_rows`, enrollment/graded count 0.
- `P/contracts.md:29,58,61` требует отклонять нарушенный result contract, а не угадывать исправление.

**Конкретная симуляция N1:**

1. Принят scalar `u.grade_mean.v1` для C2/S2.
2. Scoped relation пуста.
3. Внутренний `COALESCE` не обрабатывает ни одной строки; scalar `SUM` возвращает NULL.
4. Raw components становятся `[null,0,0]`.
5. Non-null integer ResultSpec отвергает результат вместо обязательного normal `no_rows`.

Таким образом буквальное выполнение нормативного правила не может пройти предусмотренный normal path. Это **дефект согласованности спецификации**, не обнаруженный баг приложения: приложения ещё нет.

### Независимая локальная проверка

Выполнен только schema-free SELECT в SQLite `:memory:`, без таблиц, schema/seed, файлов или приложения. Локальная SQLite **3.45.1**, не заявленная target version.

Для выражений

`SUM(COALESCE(grade_units,0)), COALESCE(SUM(grade_units),0), COUNT(grade_units), COUNT(*)`

получено:

| Входная relation | Результат |
|---|---|
| Пустая | `(NULL,0,0,0)` |
| Одна строка с NULL | `(0,0,0,1)` |
| Одна строка с настоящим 0 | `(0,0,1,1)` |

Это **изолированная диагностика aggregate semantics**, не product/DB integration test. Finding Architect2 подтверждён независимо.

### Минимальные исправления

1. **Согласовать нормативную формулу с ResultSpec.** Предпочтительно сохранить non-null integer components и использовать aggregate-level normalization, например документальное `COALESCE(SUM(grade_units),0)`. Не требуется менять стек или строить SQL compiler.
2. **Добавить три concrete raw → normalized examples:**

   | Случай | `[sum_units,graded_count,enrollment_count]` | Expected |
   |---|---|---|
   | Нет enrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
   | Enrollment есть, grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
   | Настоящая оценка 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

3. **Уточнить V1/S10/N1–N3 verification:** будущая real-DB проверка получает действительные raw SQL components, а отдельный adapter unit test преобразует их в normal answer. Не заменять первое вторым и не требовать продуктового запуска в B.

Допустимая альтернатива — nullable raw sum с явно указанной фазой нормализации — сложнее и для выбранного небольшого контракта не нужна.

**Pass следующей редакции:** no-row mean получает допустимые integer components и normal `no_rows`; NULL-only и real-zero различаются; нет необходимости нарушить ResultSpec, выдать error вместо normal outcome или молча угадать правило.

## Репрезентативные implementation walkthroughs

### 1. M1 dependency и mutation

Полный план принимается до SQL. F1 top adapter оставляет course2, runtime binding получает cohort student1, final mean равна95.00. F2 меняет top на course1 и cohort на1/2/3. `GraphState.results` не подставляет все raw candidate IDs вместо выбранных top IDs. Truncated или corrupted result останавливает downstream до provider/SQL.

**Итог:** прежний B1 больше не требует догадки исполнителя.

### 2. Scalar empty / NULL / zero

Для N1 ResultSpec требует integer sum, но предписанный SQL возвращает NULL. N2/N3 с существующей NULL-grade строкой и настоящий grade0 дают различные counts и должны оставаться различными normal outcomes.

**Итог:** B2-R1 — реальный локальный blocker; три случая должны быть согласованы вместе.

### 3. Перенос на Library и экранный failure path

Library меняет descriptor/domain adapter/fixture, не core; count1/1 и all-returned0/0 не масштабируются как grades. EI refusal/repair имеет injected provenance, не попадает в real-model score; экран показывает отсутствие SQL либо все реальные same-run attempts и typed results. Обязательные DB/live/E2E/core-hash доказательства остаются future.

**Итог:** переносимость, UI evidence и оценочная методика теперь достаточно конкретны для планирования.

## Покрытие и отсутствие дополнительных blockers

- **R-01/02:** предложены ERD, identities, names, cardinalities, semester/retake/NULL semantics и независимые fixtures; они не приписаны PDF.
- **R-03/04:** реальный LangGraph/provider/DB vertical slice, четыре фильтра, JOIN traps, unequal groups и M1 sensitivity предусмотрены.
- **R-05:** Library и unchanged-core boundary проверяемы; arbitrary SQL dialect support не обещан.
- **R-06/07/08:** traces/attempts/errors, controlled failures, actual-model generation и UI coverage разделены; empty mean требует B2-R1.
- **R-09/10:** обязанности модулей и пять production тем раскрыты; memory/authentication/retention limitations сохранены.
- **R-11..15:** actual schema/seed/code/tests/examples/public access/SHA — будущие обязательства; local B commit их не закрывает.
- **R-16/17:** manual walkthrough и самостоятельная owner defense предусмотрены отдельно от agent review.
- **U-01:** actual prompts/read context/templates/coverage omissions различены; текущий review не сертифицирует полную native transcript coverage.
- **U-02:** точный час остаётся открытым.
- **U-03:** native provenance, terminal lifecycle и отсутствие handoff проверяет лидер.
- **U-04..06:** proposed ADR003–007, ownership, сохранение A/истории и отдельный B docs commit отражены.
- **U-07:** historical verified переход не объявляется новым результатом B.
- **U-08:** обсуждение и наблюдаемое понимание ещё предстоят.

Неизвестные credentials/budget, owner acceptance и public authority **не самостоятельные blockers documentary B**. Они блокируют соответствующие будущие действия. Withdrawn27/30 не восстановлен; новый48/48 gate явно proposed.

## Alternatives и synthesis

**Strongest steelman:** свободный read-only SQL с независимым oracle и прозрачными traces проще для малого учебного проекта; чрезмерный typed IR может превратить demonstrator в собственный compiler.

**Реальное напряжение:** свободные result columns упрощают generation, но заставляют formatter угадывать units/grain/NULL. Небольшой ResultSpec устраняет угадывание, однако обязан соответствовать действительным aggregate edge cases.

**Синтез:** сохранить нынешний конечный registry/domain adapter и свободную SQL generation; исправить ровно empty-sum normalization и три boundary examples. Независимый oracle остаётся необходимым: typed shape не доказывает SQL semantics.

## Stop condition

Передать этот review и завершённый Architect2 review Planner. Создать **новую immutable iteration**, не менять reviewed bytes; после малой поправки выполнить новый отдельный Architect → отдельный Critic цикл и настроенные gates в пределах max5.

Текущая iteration **не approved**. Поддерживаемый closeout, native completion/provenance, `active:false`, prompt packaging и commit остаются обязанностью лидера после passing reviews. Этот review их не присваивает.

Application tests, actual SDK compatibility, live eval, UI execution, public delivery и owner rehearsal — **not-run**. Execution authorization/handoff отсутствует.
<!-- END_CRITIC_REVIEW -->
