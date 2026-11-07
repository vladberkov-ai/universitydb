<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 2

**Verdict: `iterate`.**
**Роль:** отдельный Architect, не Critic.
**Статус:** documentary advisory; решения остаются proposed. Реализация и execution handoff не разрешены.

## Summary

Iteration 2 содержательно исправляет B1, B3, B4 и большую часть B2. Однако в нормативном контракте среднего остаётся конкретное противоречие для **пустого набора**: предписанный `SUM(COALESCE(grade_units,0))` возвращает NULL, тогда как ResultSpec требует integer `sum_units=0`. Это ломает предусмотренный normal outcome S10/N1 при буквальной реализации контракта.

Нужна небольшая документальная поправка и три точных zero-case examples, **не смена архитектуры, не SQL compiler и не реализация приложения**.

Далее `P/` означает `.omx/plans/H-006-B2/iteration-2/`.

## Проверенное основание

Полностью прочитан `P/plan-bundle.md`: **713 строк, 114166 bytes**, все 13 constituent documents, включая changes mapping. Прочитаны actual task/context, authoritative H-006-v5 handoff, актуальные requirements/acceptance contract, принятый screen scope, завершённые Architect1/Critic1 reviews, Planner2 completion receipt, baseline receipt, свежий D2 report и оба сохранённых research-final.

Read-only проверки:

- **14/14** manifest entries совпали по raw SHA-256 и размеру.
- **13/13** constituent files byte-equivalent соответствующим разделам bundle.
- **13/13** файлов iteration 1 сохранены по её manifest.
- **25/25** текущих vault hashes совпали с `inputs-observed.json.current_sha256`.
- Все **6** JSON-блоков bundle синтаксически разобраны.
- Matrix содержит **17 R + 8 U**.
- `omx quality-gates list --stage ralplan --json` вернул `gates:[]`; это не заменяет reviews.
- HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, branch `main`.

Raw SHA-256 bundle до и после review:

`fe92a07802c9ba497948b0f22f9f4fdb2031ed83273062ae76765d6d99974e86`

Штатный baseline receipt использует другой, domain-separated digest; он не подменяется raw SHA-256.

Независимый пересчёт documentary fixtures подтвердил:

- S1–S6: sums в hundredths `50000/35000/40000/25000/26000/16000`, согласованные counts/averages.
- M1/F1: top `{2}`, cohort `{1}`, answer `95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, answers `{95.00,80.00,50.00}`.
- M1/ties: top `{1,2}`, cohort `{1,2,3}`, answers `{90.00,90.00,null}`.
- Расчёт предложенного token-rate estimate: `$1.056`.

Это арифметическая проверка документов, **не выполнение приложения или SQL integration tests**. Original PDF самостоятельно повторно не декодировал: использован явно атрибутированный leader receipt чтения четырёх страниц; текущий hash PDF проверен среди inputs.

Researcher/dependency-expert материалы использованы как **исторические inputs от 2026-11-07**, не новые исследования и не reviewer approvals. Candidate pins не означают installation/compatibility/security proof. Новых внешних исследований не проводил.

Файлы, Git, state, IDs, tracker и Obsidian не изменял; детей не запускал.

## Проверка замечаний предыдущего цикла

| Finding | Независимый результат |
|---|---|
| **B1 — static DAG / runtime binding** | **Исправлено на уровне проекта.** `validate_plan` допускает symbolic refs по объявленным outputs; `bind_results` требует completed/domain-validated/nontruncated данные. Полный M1 DAG, cycle/missing-column/runtime corruption mutations и запрет downstream calls конкретны. Последняя связка состояния сохраняет уже отобранные top dependencies, отдельно от raw candidate trace. Evidence: `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **B2 — metric/grain/unit/result boundary** | **Основная граница исправлена, остаток ниже blocking.** Есть конечный registry, ResultSpec, domain result adapter, exact integer components, rational ties, half-up2, Library count без grade scaling и отрицательные unit/denominator/grain examples. Core не обязан угадывать предметную семантику по именам колонок. Evidence: `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **B3 — injected faults / real-model score** | **Исправлено.** EI1–EI3 имеют injected provenance и 0 paid calls; actual-model suite отдельно считает 48 conversations, включая continuation. Unexpected failures не удаляются из denominator, N1–N4 требуют no-data outcomes, а не искусственной ошибки генерации. Раскрытые examples честно не названы sealed suite. Evidence: `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **B4 — полный экран** | **Исправлено.** SQL/bindings, typed DB rows и все same-run events/attempts доступны через expanders; предусмотрены success, clarification/resume, repair и terminal error, исключены чужие старые rows. Opaque ID явно fail. Evidence: `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`; `P/implementation-plan.md:9–12`. |
| **A1 — closed wire bindings** | **Достаточно для documentary stage.** Bounded closed array, nullable slots, discriminator validation, exact placeholder/name checks и deterministic conversion заданы. Будущий SDK compatibility smoke остаётся честно future, не blocker B сам по себе. Evidence: `P/contracts.md:238–241`; `P/test-plan.md:114–115`. |
| **A2 — resource boundaries** | **Достаточно с явно сохранённым residual risk.** Есть SQL/input/bindings/single-value boundary tests; byte accounting не выдан за exact tokenizer, watchdog — за memory isolation. Evidence: `P/contracts.md:243–244`; `P/test-plan.md:115–116`; `P/production-considerations.md:13–17`. |

## Единственный blocking finding

### B2-R1 — Внутренний COALESCE не нормализует SUM пустого набора

**Приоритет:** P2; обязательная малая документальная поправка.
**Уверенность:** высокая, подтверждено изолированной локальной диагностикой.

**Evidence:**

- `P/contracts.md:54–58`: mean registry требует integer components, а нормативное правило предписывает `SUM(COALESCE(grade_units,0))` и одновременно требует `sum_units=0` при нулевом denominator.
- `P/contracts.md:204–207`: concrete S6 ResultSpec объявляет `sum_units` non-nullable.
- `P/test-plan.md:45,125`: empty C2/S2 должен вернуть normal `average=null`, `no_rows`, enrollment/graded count 0.
- `P/contracts.md:29,58`: повреждённый result shape отклоняется; semantic mismatch не является разрешённым SQL repair.

**Контрпример буквальной реализации:**

1. Для N1 выбирается scalar `u.grade_mean.v1`.
2. Scoped relation C2/S2 не содержит строк.
3. Предписанный `SUM(COALESCE(grade_units,0))` возвращает NULL: ни одной строки, к которой применился бы внутренний COALESCE, нет.
4. Raw tuple получается `[null,0,0]`, не `[0,0,0]`.
5. ResultSpec validation отклоняет его, хотя обязательный expected — normal `no_rows`.

Это не доказанный дефект приложения: приложения нет. Это **противоречие нормативной спецификации конкретному обязательному сценарию**.

### Изолированная проверка aggregate semantics

Выполнены только schema-free SELECT на временном SQLite `:memory:`; без таблиц, schema/seed, файлов и приложения. Локальная SQLite: **3.45.1**, не объявляется будущей target version.

Для выражений:

`SUM(COALESCE(x,0)), COALESCE(SUM(x),0), COUNT(x), COUNT(*)`

получены:

| Вход | Результат |
|---|---|
| Ноль строк | `(NULL, 0, 0, 0)` |
| Одна строка с `x=NULL` | `(0, 0, 0, 1)` |

Это **изолированная диагностика поведения агрегата, не product/DB integration test**.

### Минимальное исправление

Предпочтительно сохранить нынешний non-null integer ResultSpec и заменить нормативное правило суммы на **aggregate-level normalization**, например документальное `COALESCE(SUM(grade_units),0)` с integer zero.

Добавить concrete raw-result → normalized-answer examples:

| Случай | `[sum_units,graded_count,enrollment_count]` | Expected |
|---|---|---|
| Нет enrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
| Есть enrollment, grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
| Есть настоящая оценка 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

Согласовать S10/N1–N3 и V1 с этими сообщениями. Future DB integration должен проверить **реальные SQL outputs**, а unit adapter tests — отдельно их преобразование.

Альтернатива — разрешить nullable raw sum и нормализовать в adapter до проверки другой формы — возможна, но расширяет контракт без необходимости. Для выбранной маленькой системы outer COALESCE проще.

**Pass для следующей редакции:** no-row path не требует нарушить nullable contract или поменять normal outcome на error; все три случая различены документально, дальнейшие продуктовые проверки остаются future.

## Архитектурная оценка остального пакета

- **ERD/семантика согласованы:** Course/Offering, nonunique names, FK/cardinalities, integer grade units, NULL, retakes, all-semesters scope и exact ties объяснены как proposed. Не приписаны PDF. Evidence: `P/architecture-proposal.md:25–34`; `P/ADR-OMX-004-domain-semantics.md:5–24`.
- **Bounded orchestration конкретна:** глобальные бюджеты сохраняются через resume; учитываются plan calls, provider retry и repair; interrupt-node не повторяет платную работу перед паузой. Evidence: `P/contracts.md:5–13,32–35,44–49`.
- **Portability ограничена разумно:** Library меняет domain adapter/descriptor/DB, не core; обещание не распространяется на произвольные SQL dialects. Unchanged-core проверка требует actual DB/live/E2E evidence. Evidence: `P/architecture-proposal.md:41–42`; `P/test-plan.md:76–84`.
- **Обязательства не закрыты бумажным review:** matrix различает SQL/app/live/public/manual/defense/provenance; local commit не заменяет R-15. Evidence: `P/requirements-test-matrix.md:3–33`; `P/implementation-plan.md:3–26`.
- **Deliberate additions присутствуют:** пять principles, три drivers, содержательные alternatives, три pre-mortem и расширенный unit/DB/graph/live/E2E/observability/manual/public план. Evidence: `P/architecture-proposal.md:5–14,44–49`; `P/test-plan.md:54–103`.
- **Production границы честные:** пять требуемых тем, planned против actual, отсутствие production-ready/security/memory гарантий. Evidence: `P/production-considerations.md:3–17`.

### Принципы

B1/B3/B4 больше не создают обнаруженных ранее нарушений границ и evidence. Остаточный B2-R1 нарушает согласованность принципа **«вычисляет БД, не модель»** с обещанным typed normal outcome: нижний слой должен выдавать представление, которое верхний слой вправе принять.

Это локальный дефект контракта, не основание отвергать выбранный стек или требовать универсальный semantic validator.

## Consensus addendum

**Antithesis — strongest steelman:** для компактного учебного решения свободный read-only SQL, независимые oracle и прозрачные traces могли бы быть достаточны. Дополнительные typed shapes рискуют разрастись в собственный query compiler и отодвинуть настоящий vertical slice.

**Tradeoff tension:** свободные результаты проще генерировать, но заставляют formatter угадывать units/grain/NULL; строгий ResultSpec устраняет угадывание, однако требует аккуратно согласовать реальные SQL edge cases с wire contract.

**Synthesis:** сохранить принятый iteration-2 компромисс — небольшой конечный ResultSpec registry и domain adapter, не полный compiler. Исправить ровно агрегатную нормализацию пустоты и добавить три точных examples. Независимый semantic oracle остаётся обязательным; runtime shape checks не доказывают правильность произвольного SQL.

Proposed owner decisions, неизвестные credentials/budget и будущий SDK smoke **не являются самостоятельными blockers documentary B**. Новых внешних research calls для указанной поправки не требуется.

## Рекомендации и stop condition

1. Передать этот завершённый review **отдельному Critic iteration 2**, не пропуская текущую последовательность.
2. При подтверждении B2-R1 выполнить малую Planner revision в **новой immutable iteration**, затем снова отдельные Architect → Critic и настроенные gates. Не исправлять уже reviewed bytes.
3. Не требовать реализации приложения или live calls ради принятия документальной поправки.
4. Lifecycle/native completion/closeout, prompt packaging и commit остаются ответственностью лидера; мой review их не удостоверяет.

**Review завершён: `iterate`, один blocking finding B2-R1.**
Application tests, live eval, actual provider compatibility, UI execution, public delivery и owner rehearsal — **not-run**. Execution authorization/handoff отсутствует.

<!-- END_ARCHITECT_REVIEW -->
