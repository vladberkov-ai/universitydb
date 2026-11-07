<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 3

**OKAY. Workflow verdict: `approve`.**

**Blocking findings: 0. Обязательных исправлений нет.** Новых проблем, препятствующих принятию документального пакета B для обсуждения в чате, не обнаружено.

B2-R1 исправлен; прежние исправления B1/B2/B3/B4 сохранены. Пакет достаточно конкретен и внутренне согласован для последующего отдельного поручения реализации после принятия решений владельцем. Это **не разрешение реализации**, не подтверждение работоспособности приложения и не завершение lifecycle.

Далее `P/` означает `.omx/plans/H-006-B2/iteration-3/`.

## Проверенное основание

Полностью прочитаны:

- `P/plan-bundle.md`: **773 строки, 124495 bytes**, все **14 составляющих документов**, включая обе changes mappings;
- manifest и baseline receipt iteration 3;
- actual user task, grounded context, authoritative H-006-v5 пакет, текущие requirements/acceptance contract и принятый scope;
- применимые инструкции проекта, локальные ralplan/plan skills, свежий D2 report;
- полные Architect/Critic reviews iterations 1–2 и завершённый **Architect3 `approve`**;
- сохранённые researcher/dependency-expert final texts как **датированные reused research inputs 2026-11-07**, не новые исследования или reviewer verdicts.

Конкретного нового external-research gap не выявлено. Candidate pins не считаются установленными, совместно проверенными или прошедшими security audit.

### Свежие read-only проверки

| Проверка | Результат |
|---|---|
| Raw hashes и размеры manifest iteration 3 | **15/15 совпали** |
| Составляющие документы против соответствующих разделов bundle | **14/14 byte-equivalent** |
| Fenced JSON examples | **12/12 синтаксически разобраны** |
| Полный M1: топология и типы symbolic references | **pass**, без необходимости runtime values |
| Три Z-пары raw DBResult → Answer | **pass documentary consistency** |
| Текущие vault hashes против `inputs-observed.json.current_sha256` | **25/25 совпали** |
| Предыдущие iterations 1/2 против их manifests | **13/13 и 14/14 сохранены** |
| Матрица требований | **17 R + 8 U** |
| Исходные non-runtime файлы против B2 baseline | **95/95 неизменны** |
| Git index против baseline | **неизменен** |
| Git | canonical root, `main`, HEAD A сохранён; staging/remotes пусты |
| Дополнительные quality gates | CLI вернул `{"gates":[],"stage":"ralplan"}` |

Raw SHA-256 bundle до завершения review:

`e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`

Raw SHA-256 прочитанного Architect3 review:

`0914935a942be1c89c0c56d26f0be4371b795a674c590662ccd0939d3df4ce00`

HEAD:

`8931d832d49311ac0d63c3a7a359b4293058da89`

Manifest содержит raw hashes; штатный baseline — domain-separated lifecycle digest. Различие этих представлений не принимается за подмену.

Original PDF самостоятельно повторно не декодировал: использован явно атрибутированный `.omx/context/H-006-B2/pdf-read-receipt.json` лидера о четырёх страницах; текущий PDF hash сверён. Architect3 completion observation прочитан как evidence лидера, не выдан за самостоятельно выполненный host lifecycle audit.

Файлы, Git, state, IDs, tracker и Obsidian мною не изменялись. Детей не запускал.

## Summary

- **Clarity:** pass — роли компонентов, типы, фазы проверки, ошибки и границы выполнения определены.
- **Verifiability:** pass — независимые fixtures, exact expected, отрицательные mutations, pass/fail и будущие evidence paths конкретны.
- **Completeness:** pass — требуемые документы и все 25 R/U строк присутствуют; обнаруженные ранее blocking gaps устранены.
- **Big Picture:** pass — компактный локальный demonstrator соответствует принятому scope; proposed/accepted/actually-tested не смешаны.
- **Principle/Option Consistency:** pass — рекомендации согласованы с минимальностью, schema-agnostic boundary и разделением safety/semantics/evidence.
- **Alternatives Depth:** pass — локальный и серверный варианты рассмотрены честно; CLI не выдан за достаточный принятый экран.
- **Risk/Verification Rigor:** pass — границы retries/resources, недостаточность shape/read-only checks, live/injected distinction и public delivery раскрыты.
- **Deliberate Additions:** pass — три credible pre-mortem и расширенные unit/actual-DB/mocked-graph/live-NL/UI-E2E/trace/manual/public/defense проверки присутствуют.

## Проверка предыдущих замечаний

| Finding | Результат Critic3 и evidence |
|---|---|
| **B1: static DAG против runtime binding** | **Исправлено.** `P/contracts.md`, раздел «Двухфазный DAG…»: `validate_plan` принимает typed symbolic references предшественников; `bind_results` требует completed/domain-validated/nontruncated данные. Полный M1, cycle/missing-alias mutations и D1–D3 имеют точные фазы отказа и запрет downstream calls. `GraphState.results` хранит выбранные dependency rows, raw candidates остаются в trace. |
| **B2: metric/unit/grain/result boundary** | **Исправлено.** Конечный ResultSpec registry и DomainResultAdapter закрепляют integer components, unit/scale, group keys, exact ties и half-up2. Library count не проходит grade normalization. Wrong unit/denominator/grain имеют определённые ошибки. Evidence: `P/contracts.md`, ResultSpec/registry и JSON examples; `P/test-plan.md`, V1–V2. |
| **B2-R1: пустой scalar SUM** | **Исправлено полностью на уровне документов.** Нормативная формула — `COALESCE(SUM(grade_units),0)`, не row-level COALESCE. Z1/Z2/Z3 содержат полные typed raw messages и нормализованные Answer. DB-Z и UNIT-Z проверяют разные границы. Evidence: `P/contracts.md`, «B2-R1…»; `P/test-plan.md`, S10/N1–N3/V1 и заключительный раздел; `P/ADR-OMX-006-schema-boundary-tracing.md`. |
| **B3: live accuracy против injected failures** | **Исправлено.** EI1–EI3 явно injected, имеют provenance и 0 paid calls. Live denominator — 48 real-model conversations с continuation; N1–N4 проверяют no-data outcomes. Unexpected failures учитываются, не удаляются из denominator. Раскрытые prototypes не названы уже созданным sealed suite. Evidence: `P/test-plan.md`, live gate и «Две разные negative lanes»; ADR007. |
| **B4: принятый экран** | **Исправлено.** SQL/bindings, typed DB rows и полные same-run events/attempts доступны из экрана. UI1 различает success, pause/resume, repair и terminal error; opaque ID, исчезнувшие attempts и rows другого run — fail. Evidence: `P/architecture-proposal.md`, компоненты; `P/test-plan.md`, UI1; matrix R06/R17; implementation I1/I4. |
| **A1: provider bindings** | **Достаточно для documentary B.** Closed bounded array, discriminator/type checks, deterministic SQLite mapping, duplicate/placeholder checks описаны. Actual SDK smoke остаётся future. |
| **A2: resource boundaries** | **Достаточно с явным residual risk.** W1–W3 различают request/SQL/bindings/value boundaries и byte/token accounting. Watchdog не выдан за hard memory isolation; production gap сохранён. |

### B2-R1: независимая проверка согласованности

| Случай | Raw `[sum_units,graded_count,enrollment_count]` | Normalized Answer |
|---|---|---|
| Нет enrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
| Enrollment существует, grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
| Настоящая оценка 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

Во всех трёх raw examples sum/counts — non-null integers, scalar `row_count=1`. Число aggregate rows не подменяет количество исходных enrollments. Отсутствующие GROUP BY группы не обещаны автоматически. Nullable raw sum запрещён, а не молча исправляется formatter-ом.

Будущая **DB-Z** требует действительных SQLite components/types до adapter; **UNIT-Z** отдельно проверяет преобразование и отклонение `sum_units=null`. Это устраняет прежнюю возможность подтвердить formatter, не подтвердив raw query result.

Нового SQL probe не потребовалось. Эти проверки остаются **документальными**, DB-Z/UNIT-Z — **not-run**.

## Репрезентативные implementation walkthroughs

### 1. M1: зависимость, мутация и ties

Полный план принимается до SQL. F1 top adapter выбирает course2, runtime binding получает cohort `{1}`, final mean — `95.00`. F2 меняет top на course1, cohort — `{1,2,3}`, ответы — `{95.00,80.00,50.00}`. Tie fixture выбирает оба курса и union cohort, ответы — `{90.00,90.00,null}`.

Truncated/corrupted dependency останавливает следующий provider/SQL call. Core не подставляет все raw candidates вместо выбранных top IDs.

**Вывод:** исполнителю не требуется угадывать фазу разрешения references или семантику промежуточного результата.

### 2. Scalar mean: пустота, NULL и настоящий ноль

Приём ResultSpec, raw integer components и normal output теперь согласованы для всех трёх случаев. SQL отвечает за aggregate components, domain adapter — за точную нормализацию/rounding; модель не придумывает числа. Несоответствующий raw shape отвергается.

**Вывод:** прежний обязательный no-rows сценарий больше не требует нарушить контракт.

### 3. Library и экранный failure path

Library заменяет DB/descriptor/domain adapter, не core. Counts `1/1` и all-returned `0/0` не масштабируются как grades. Unchanged-core hash, actual DB, mocked graph, live NL и UI evidence остаются отдельными будущими проверками.

Injected refusal показывает отсутствие SQL/DB; injected repair показывает обе попытки и финальные typed results. Ни один такой результат не становится live accuracy evidence.

**Вывод:** portability и UI/error acceptance проверяемы без расширения B до реализации.

### Независимая арифметическая сверка

Целочисленный/рациональный пересчёт документальных fixtures подтвердил:

- S1–S6 sums в hundredths: `50000/35000/40000/25000/26000/16000`;
- соответствующие graded/enrollment counts и averages;
- M1/F1, M1/F2 и tie outcomes, перечисленные выше.

Это вычисление expected по документальным строкам, **не SQL/application/E2E test**.

## Полнота требований и границ

- **R01–R04:** ERD/имена/offerings/semesters/grades, четыре фильтра, JOIN duplication trap, unequal groups, retakes и содержательный M1 покрыты.
- **R05–R08:** Library unchanged-core transfer, полная trace chain, ambiguity/resume, controlled errors, actual-model NL и E2E разведены.
- **R09–R10:** обязанности DB/agent/prompts/tracing/UI и все пять production тем раскрыты без production-ready claim.
- **R11–R15:** schema/seed/code/tests/examples/public комплект, clean clone, remote SHA и anonymous access остаются будущими обязательствами; local B commit их не закрывает.
- **R16–R17:** самостоятельная owner rehearsal и простой экран предусмотрены, согласие агентов не заменяет защиту.
- **U01–U08:** actual/template/read-context и omissions различены; deadline hour открыт; native lifecycle проверяет лидер; ADR/history/ownership/A/B сохранены; исторический U07 не присвоен B; глубокое понимание ещё предстоит наблюдать.

Owner acceptance, credentials/budget, будущий compatibility smoke и public authority — gates соответствующих будущих действий, **не самостоятельные blockers documentary B**.

Отозванный `27/30` не восстановлен. Новый `48/48` явно proposed, имеет ограниченное small-suite назначение и не объявлен статистической гарантией.

## Alternatives, tradeoff и synthesis

**Сильнейшая альтернатива:** для маленького demonstrator свободный read-only SQL с независимым oracle и прозрачными traces проще; чрезмерный typed IR способен превратить задание в собственный compiler и задержать первый настоящий vertical slice.

**Реальное напряжение:** свободные result columns уменьшают адаптерный код, но вынуждают downstream угадывать units/grain/dependencies. Строгий ResultSpec снимает угадывание ценой registry и boundary tests.

**Синтез текущего пакета достаточен:** конечные shapes/domain adapters, двухфазные references и точная арифметика при сохранении настоящей SQL generation. Универсальный query compiler не вводится. Независимый semantic oracle остаётся необходимым: model/shape/read-only/trace completeness не доказывают правильность SQL.

## Advisory observations — не обязательные исправления

1. Сохранить конечный размер ResultSpec registry при реализации; новые метрики добавлять через domain adapter и tests, не University heuristics в core.
2. При упаковке не повышать уровень доказанности: candidate pins, walkthroughs, fixture arithmetic и review approval не превращать в executed compatibility/E2E/security evidence.
3. Сохранить I0→I1 и ранний настоящий vertical slice; не заменять его предварительным строительством универсальных абстракций.

## Stop condition

**Critic3 review завершён: `approve`, обязательных исправлений 0.**

Лидер далее проверяет реальное native completion этого агента, фиксирует результат configured gates и выполняет supported Advisory closeout. Пустой список дополнительных gates не заменяет reviews.

Terminal state, `active:false`, explicit отсутствие execution authorization/handoff, prompt coverage, public-safe packaging, link/privacy/diff checks и отдельный docs-коммит B **ещё должен подтвердить лидер**. Этот verdict не присваивает их результаты.

Application tests, actual SDK compatibility, live eval, UI execution, public delivery и owner rehearsal — **not-run**. Все новые архитектурные решения остаются **proposed до обсуждения в чате**.

<!-- END_CRITIC_REVIEW -->
