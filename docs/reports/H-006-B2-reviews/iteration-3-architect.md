<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 3

**Verdict: `approve`.**
**Scope:** документальное архитектурное предложение; отдельный Architect, не Critic.
**Blocking findings:** отсутствуют. Обязательных исправлений до следующего review не требуется. Все архитектурные решения остаются **proposed**.

Далее `P/` означает `.omx/plans/H-006-B2/iteration-3/`.

## Summary

B2-R1 исправлен: нормативная aggregate-level нормализация соответствует non-null integer ResultSpec, а отсутствие записей, отсутствие оценок и настоящая нулевая оценка имеют различные, согласованные normal outcomes. Полное повторное чтение пакета не выявило новых блокирующих противоречий; прежние исправления dependency binding, domain boundary, live/injected evidence и экранного scope сохранены.

Approval относится только к архитектурной согласованности документов. Он не означает принятия решений владельцем, выполнения продуктовых проверок или разрешения реализации.

## Проверенное основание

Полностью прочитан `P/plan-bundle.md`: **773 строки, 124495 bytes**, все **14 constituent documents**, включая обе changes mappings. Прочитаны actual task/context, полный H-006-v5 handoff, актуальные requirements/acceptance contract, принятый scope, локальные planning instructions, D2 report, manifest, baseline receipt, Planner3 completion observation и полные Architect/Critic reviews iterations 1–2.

Сохранённые researcher/dependency-expert final texts прочитаны как **датированные reused inputs от 2026-11-07**, не новые исследования или reviewer approvals. Их применимость к неизменившемуся предложенному стеку сохраняется; нового конкретного research gap не обнаружено. Candidate pins не считаются установленными, совместно проверенными или прошедшими security audit.

### Свежие read-only проверки

- **15/15** manifest entries iteration 3 совпали по размеру и raw SHA-256.
- **14/14** constituent documents byte-equivalent соответствующим разделам bundle.
- Manifest entries iterations 1 и 2 сохранены: **13/13** и **14/14**.
- Все **12 fenced JSON blocks** синтаксически разобраны.
- Полный M1 проверен статически: топологические зависимости и типы references допустимы без runtime values.
- Три Z-пары проверены на integer/non-null raw components, counts, normalized rows и empty reasons.
- Матрица содержит **17 R + 8 U**.
- **25/25** текущих vault hashes совпали с `inputs-observed.json.current_sha256`.
- `omx quality-gates list --stage ralplan --json` вернул `gates:[]`; это не заменяет reviewers.
- Git root — текущий UniversityDB, branch `main`, HEAD **`8931d832d49311ac0d63c3a7a359b4293058da89`**; staging и список remotes пусты.

Raw SHA-256 bundle до и после проверки:

`e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`

Штатный baseline receipt использует domain-separated lifecycle digest; raw hash manifest не подменяет этот digest. Native lifecycle observation Planner прочитан как evidence лидера, не как независимо выполненный мною host audit.

Original PDF самостоятельно повторно не декодировал: использован атрибутированный leader receipt четырёх страниц; текущий PDF hash сверён среди 25 inputs.

## B2-R1: исправление подтверждено

### Root cause и устранение

Прежняя проблема находилась на границе SQL aggregate → typed result: row-level COALESCE не обеспечивал non-null sum для relation без строк.

Теперь `P/contracts.md:58,250–284` задаёт:

- `COALESCE(SUM(grade_units),0)` с integer zero;
- `COUNT(grade_units)` для denominator;
- `COUNT(*)` по scoped enrollment relation для enrollment count;
- запрет исправлять nullable raw sum молча в formatter;
- различение scalar aggregate row count и числа исходных enrollments;
- отсутствие обещания автоматически создавать отсутствующие GROUP BY группы.

Concrete examples согласованы:

| Случай | Raw components | Normalized outcome |
|---|---|---|
| Нет enrollments | `[0,0,0]` | `average=null`, `no_rows` |
| Enrollment есть, grade NULL | `[0,0,1]` | `average=null`, `no_grades` |
| Настоящий grade 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

Typed DBResult и Answer представлены полностью, без расширения nullable-контракта или эвристического восстановления потерянных данных.

**Verification boundary исправлена также:** `P/test-plan.md:45,112,125,134–137` согласует S10/N1–N3/V1 и отдельно требует:

- **DB-Z:** действительные raw SQLite outputs/types до adapter;
- **UNIT-Z:** чистое преобразование трёх typed messages и отклонение `sum_units=null`.

Одна проверка явно не заменяет другую. ADR006 закрепляет ту же границу: `P/ADR-OMX-006-schema-boundary-tracing.md:11–21`.

Новый SQL probe не потребовался. Здесь выполнена документальная проверка; DB-Z/UNIT-Z остаются **not-run**.

## Полный архитектурный cross-check

| Область | Вывод и evidence |
|---|---|
| **ERD и предметные правила** | Course/Offering, обязательные связи, nonunique имена со стабильными IDs, integer hundredths, NULL, all-retakes, равные веса, exact ties и all-semesters scope согласованы с fixtures. Правила явно proposed, не приписаны PDF. `P/architecture-proposal.md:25–34`; `P/ADR-OMX-004-domain-semantics.md:5–24`. |
| **Static DAG → runtime binding** | `validate_plan` принимает typed symbolic references по declared outputs; `bind_results` требует completed/domain-validated/nontruncated данные. `GraphState.results` содержит выбранные dependency rows, а raw candidates сохраняются отдельно в trace. Cycle/missing alias/type/truncation имеют конкретные stops до downstream calls. `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **Metric/unit/grain boundary** | Конечный ResultSpec registry и DomainResultAdapter исключают необходимость распознавать University semantics в core по именам колонок. Integer components сохраняют точное сравнение ties; Library count не масштабируется как grade. Shape validation не выдаётся за доказательство SQL semantics. `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **Clarification/resume и бюджеты** | Session-bound resume, replay/conflict/stale/expiry branches, side-effect-free interrupt и общие counters через resume согласованы. Plan calls, transient retry и repair входят в лимит; sixth call не скрывается. `P/contracts.md:5–13,32–35,44–49`; `P/test-plan.md:59–70`. |
| **Safety/resources** | Read-only/authorizer/allowlists отделены от semantic oracle. Closed Binding array и placeholder checks конкретны. Byte gate не объявлен exact tokenizer; watchdog не объявлен memory isolation. Residual memory risk явно сохранён. `P/contracts.md:29–39,238–244`; `P/test-plan.md:74,114–116`; `P/production-considerations.md:13–17`. |
| **Portability** | Library имеет конкретные данные, expected counts и zero-return variant; требуется unchanged-core evidence плюс DB/mock/live/UI проверки. Arbitrary-dialect portability не обещана. `P/architecture-proposal.md:41–42`; `P/test-plan.md:76–84`. |
| **Live versus injected evidence** | EI1–EI3 явно injected, с provenance и нулём paid calls; real-model denominator — 48 conversations, включая continuation. N1–N4 требуют no-data outcomes, а не намеренной ошибки модели. Unexpected failures учитываются; disclosed examples не названы готовым sealed suite. `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **Экран и полная трасса** | SQL/bindings, typed DB rows и все same-run events/attempts доступны из экрана. Success, clarification/resume, repair и terminal error имеют pass/fail; opaque ID и старые rows другого run — fail. `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`. |
| **Delivery и требования** | Все R/U привязаны к соответствующим будущим DB/app/live/manual/public/defense/provenance доказательствам. Local commit не закрывает R-15; исторический U-07 не присвоен B. `P/requirements-test-matrix.md:3–33`. |
| **Реализация и production** | Первый реальный vertical slice предшествует дальнейшему расширению. Owner decisions, budget, compatibility и public authority вынесены в будущие gates. Пять production тем раскрыты без заявления production-ready. `P/implementation-plan.md:5–26`; `P/production-considerations.md:3–17`. |

### Независимая арифметическая сверка fixtures

Целочисленный/рациональный пересчёт документальных строк подтвердил:

- S1–S6: суммы hundredths `50000/35000/40000/25000/26000/16000` и соответствующие counts/averages.
- M1/F1: top `{2}`, cohort `{1}`, answer `95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, answers `{95.00,80.00,50.00}`.
- M1/tie fixture: top `{1,2}`, cohort `{1,2,3}`, answers `{90.00,90.00,null}`.
- Предложенная token-rate арифметика — `$1.056`; это не измерение стоимости и не spending permission.

Это **проверка документов, не SQL/application/E2E tests**.

## Deliberate principles и риски

Пять principles, три drivers, содержательные альтернативы и три pre-mortem присутствуют: `P/architecture-proposal.md:5–14,44–49`. Расширенный test plan охватывает unit, actual DB, mocked graph, live NL, UI E2E, observability, manual/public/defense проверки.

**Новых нарушений principles не обнаружено.** Прежнее противоречие B2-R1 устранено без разрастания архитектуры. Принцип «вычисляет БД, не модель» сохраняется: SQL возвращает проверяемые компоненты, domain adapter выполняет точную нормализацию/сравнение, а не придумывает числа.

## Advisory observations — не обязательные исправления

1. **Сохранить конечный размер registry при реализации.** ResultSpec решает конкретные units/grain/dependency задачи; превращение его в универсальный SQL compiler нарушило бы минимальность. Новые метрики должны иметь собственные domain tests, а не эвристики в core.
2. **Не повысить уровень доказанности при упаковке.** Candidate pins, документальные walkthroughs, fixture arithmetic и этот approval нельзя переименовать в compatibility, executed E2E или production evidence.
3. **Сохранить предложенный порядок I0→I1.** Credentials, бюджет, owner acceptance, SDK smoke и public authority остаются будущими gates, но не являются самостоятельными blockers документального B.

Withdrawn `27/30` не восстановлен. Новый `48/48` остаётся явно **proposed**, не статистической гарантией и не заменой обязательных требований.

## Trade-offs и consensus addendum

**Antithesis — strongest steelman:** маленькому учебному demonstrator могли бы быть достаточны свободный read-only SQL, независимый oracle и прозрачная трасса. Избыточный typed IR увеличивает реализацию и может отложить первый настоящий сквозной запуск.

**Tradeoff tension:** свободные result columns проще генерировать, но они заставляют downstream угадывать units/grain/NULL/dependencies. Строгий контракт устраняет угадывание, однако требует аккуратного согласования SQL edge cases.

| Вариант | Плюс | Цена |
|---|---|---|
| Свободный SQL/result shape | Меньше адаптерного кода | Неоднозначная downstream семантика |
| Полный typed query compiler | Более сильная структурная проверка | Избыточный scope и ограничение выразимости |
| **Конечный ResultSpec + domain adapter** | Явные границы при сохранении настоящей SQL generation | Небольшой registry и обязательные boundary tests |

**Synthesis:** текущий пакет реализует достаточный компромисс: конечные shapes, двухфазные references, точная арифметика и теперь корректная empty-sum normalization. Независимый semantic oracle остаётся необходимым; runtime shape и readonly checks не доказывают правильность произвольного SQL.

## Stop condition

**Architect review завершён: `approve`, blocking findings 0.**

Следующий шаг лидера — проверить native completion этого агента, затем передать immutable iteration 3 и этот полный review **отдельному Critic3**, после него — configured gates. Мой verdict не заменяет Critic, lifecycle closeout или owner acceptance.

Native provenance/completion, supported terminal closeout, `active:false`, отсутствие execution handoff, prompt packaging и commit B остаются обязанностью лидера. Я их не присваиваю.

Файлы, Git, state, IDs, tracker и Obsidian не изменял; детей не запускал. Application tests, SDK compatibility, live eval, UI execution, public delivery и owner rehearsal — **not-run**. Execution authorization отсутствует.
<!-- END_ARCHITECT_REVIEW -->
