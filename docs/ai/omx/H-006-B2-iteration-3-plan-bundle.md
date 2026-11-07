# H-006 B2 iteration 3: immutable Planner review baseline

Status: proposed. No implementation or execution authorization.


<!-- BEGIN FILE: ADR-OMX-003-minimal-stack.md -->
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

Связанные [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md), [проверки](../../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
<!-- END FILE: ADR-OMX-003-minimal-stack.md -->


<!-- BEGIN FILE: ADR-OMX-004-domain-semantics.md -->
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

Связанные [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md), [проверки](../../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
<!-- END FILE: ADR-OMX-004-domain-semantics.md -->


<!-- BEGIN FILE: ADR-OMX-005-bounded-graph-contracts.md -->
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

Связанные [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md), [проверки](../../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
<!-- END FILE: ADR-OMX-005-bounded-graph-contracts.md -->


<!-- BEGIN FILE: ADR-OMX-006-schema-boundary-tracing.md -->
# ADR-OMX-006 — Schema boundary и собственные traces

Дата: 2026-11-07. Owner: repo. **Status: proposed**, до chat review. Не execution authorization.

## Контекст
R05/R06 требуют адаптируемость и полную Input→Nodes→SQL→Results→Answer цепь; не требуют определённой платформы.

## Варианты
Domain names embedded in core; descriptor+domain adapter; generic arbitrary-dialect abstraction. JSONL или LangSmith.

## Рекомендация
Минимальный ResultSpec+domain result adapter: metric/group keys/typed aliases/unit/scale/components, точные sum_units+graded_count для averages/ties; nonnull integer sum_units через aggregate-level COALESCE(SUM(grade_units),0), различение пустоты/NULL-only/настоящего0 по denominator/enrollment_count; core не угадывает University по именам. SQLite-specific DB adapter, schema-agnostic core и University/Library descriptors; local versioned JSONL по contracts с full synthetic rows, redaction/public export отдельные.

## Обоснование
Вторая схема — реальный ограниченный transfer test; не заявлять поддержку всех dialects. Локальные traces не требуют account/network service.

## Последствия
Своя completeness проверка/retention, library scope только тот же dialect. Полные реальные PII не допустимы в demo. LangSmith требует отдельного billing/retention решения.

## Проверка
L1 same core hash+DB+live+E2E; V1–V2 units/grain/denominator failures; DB-Z actual raw components и отдельно UNIT-Z нормализация трёх zero cases; T1/T2+UI1 chain/completeness/screen access/secret exclusion; trace failure не success.

## Пересмотр
Новый dialect, real personal data, remote centralized tracing/retention/SLO requirement.

Связанные [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md), [проверки](../../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
<!-- END FILE: ADR-OMX-006-schema-boundary-tracing.md -->


<!-- BEGIN FILE: ADR-OMX-007-verification-delivery.md -->
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

Связанные [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md), [проверки](../../plans/test-plan.md). Это будущие относительные пути после упаковки из reviewed planning baseline.
<!-- END FILE: ADR-OMX-007-verification-delivery.md -->


<!-- BEGIN FILE: adr-index-additions.md -->
# Предлагаемые дополнения ADR index

Все записи proposed 2026-11-07; ADR-OMX-001/002 и существующие chat snapshots сохранить без переписывания. Только после closeout лидер интегрирует строки в docs/adr/README.md, сохранив baseline bytes/hash.

- [ADR-OMX-003: Минимальный локальный стек](../../adr/ADR-OMX-003-minimal-stack.md) — proposed.
- [ADR-OMX-004: Идентичности и арифметика предметной области](../../adr/ADR-OMX-004-domain-semantics.md) — proposed.
- [ADR-OMX-005: Bounded graph, clarification и безопасность](../../adr/ADR-OMX-005-bounded-graph-contracts.md) — proposed.
- [ADR-OMX-006: Schema boundary и собственные traces](../../adr/ADR-OMX-006-schema-boundary-tracing.md) — proposed.
- [ADR-OMX-007: Независимые oracle, live gate и delivery evidence](../../adr/ADR-OMX-007-verification-delivery.md) — proposed.
<!-- END FILE: adr-index-additions.md -->


<!-- BEGIN FILE: architecture-proposal.md -->
# UniversityDB: архитектурное предложение

Дата 2026-11-07. **Proposed**, не принято владельцем, не реализация. Основание: принятая матрица R-01..17/U-01..08, компактный scope ADR-CHAT-002 (простой экран, зависимый сценарий, вторая схема). Источники требований: [безопасный снимок](../../chat/requirements.md), [scope](../../chat/decisions/ADR-CHAT-002-result-scope.md). Более свежие private требования прочитаны; private paths/raw не публикуются. Все продуктовые требования остаются open; U-07 ранее verified, это не результат B.

## RALPLAN-DR
Принципы: (1) минимальная объяснимая система; (2) вычисляет БД, не модель; (3) неоднозначность раскрывается, не угадывается; (4) безопасность, семантика и доказательства — разные проверки; (5) ядро не знает имён таблиц предметной области.
Три drivers: обязательный LangGraph и демонстрируемый полный путь; ограниченный срок/стоимость локальной демонстрации; воспроизводимая диагностика ошибок.

| Вариант | Польза | Цена/риск | Вывод |
|---|---|---|---|
| SQLite + прямой LangGraph + OpenAI SDK + Streamlit + локальный JSONL | один процесс/файл DB, минимум сервисов, простые traces | локальные ограничения конкурентности, собственный trace validator | рекомендуем |
| PostgreSQL + LangGraph + отдельный web API/UI + LangSmith | серверный доступ, готовый tracing, путь к multi-user | дополнительные сервисы, credentials, billing/retention, больше кода | viable для production, не для первого slice |
| SQLite + CLI без экрана | меньше UI-кода | не покрывает принятый простой экран | только вспомогательный diagnostic CLI, не основной вариант |

## Стек и внешние основания
Использованы **ранее выполненные research inputs 2026-11-07 около 09:20 UTC**, не новые исследования/reviewer verdicts: researcher и dependency-expert в docs/ai/omx/H-006-v5-B-*-evidence.json. Версии ниже кандидаты, не установлены/не проверены совместно. При реализации: Python 3.13 с актуальным проверенным patch, встроенный sqlite3 (версию SQLite записать); LangGraph 1.2.20 (MIT), openai 3.46.0 (Apache-2.0), Streamlit 1.67.0 (Apache-2.0). Python patch и транзитивный lock определить отдельной проверкой совместимости; никаких установок в B.

Рекомендуем OpenAI Responses `gpt-6-luna`, `store=False`, strict structured output; alias без выдуманного snapshot. Цена по датированному research: $0.10 input/$0.50 output за 1M tokens; cached $0.01 input. 4k input+1k total output = $0.0009 на вызов, 100 вопросов ×3 вызова ≈$0.27 до дополнительных попыток. Альтернативы: `gpt-5.4-mini-2026-03-17` ($0.75/$4.50) для snapshot-воспроизводимости; `gpt-6.1-sol` ($2/$10) отдельный eval profile при измеренной недостаточности Luna, **не автоматический fallback**. Доступ аккаунта неизвестен, OPENAI_API_KEY в проверенном окружении отсутствует. Не разрешать live до явного бюджета. `store=False` не нулевая retention. Все retries/reasoning tokens учитываются в стоимости.

Официальные первичные ссылки датированного research: [LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api), [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts), [PyPI LangGraph](https://pypi.org/project/langgraph/), [SDK](https://pypi.org/project/openai/), [Streamlit](https://pypi.org/project/streamlit/), [SQLite](https://docs.python.org/3.13/library/sqlite3.html), [SQLite security](https://www.sqlite.org/security.html), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [pricing](https://developers.openai.com/api/docs/pricing), [data controls](https://developers.openai.com/api/docs/guides/your-data), [LangSmith pricing](https://www.langchain.com/pricing). Их наличие не доказывает качество SQL/совместимость/доступ. LangSmith retention не выбирается из-за отмеченного в research расхождения pricing/compliance. Перед lock — scoped [advisory audit](https://github.com/langchain-ai/langgraph/security/advisories).

## Компоненты и границы
Screen → application request/continuation → LangGraph core → schema/domain adapter, LLM adapter, SQL validator, DB adapter → deterministic answer formatter → Screen. Все узлы → local trace sink. Простой экран показывает answer, SQL/safe bindings, typed DB columns/rows и **полный same-run trace/attempts** в локальных expanders; ID без доступного содержимого недостаточен. UI не формирует SQL; LLM не исполняет его. Prompts — будущие версионированные ресурсы адаптера, не создаются в B. DB не содержит API ключей. В приложении один активный запрос на UI session, только локальный loopback; shared multi-user deployment вне задания.

## Предложенная модель и ERD (не executable SQL)
Students(student_id PK integer, name nonempty text); Teachers(teacher_id PK integer, name nonempty text); Courses(course_id PK integer, code unique text, title nonempty text); Semesters(semester_id PK text, starts_on date, ends_on date); Offerings(offering_id PK integer, course_id FK, teacher_id FK, semester_id FK, section text); Enrollments(student_id FK, offering_id FK, grade_units nullable integer 0..10000). Концептуальное grade в документах = grade_units/100, physical SQL использует grade_units.

Students 1—0..* Enrollments *..0—1 Offerings; Courses/Teachers/Semesters каждый 1—0..* Offerings. Offering имеет ровно один Course, Teacher, Semester; Enrollment — ровно одного Student/Offering. Unique(course,semester,section); PK Enrollment(student_id,offering_id). Имя не ключ и не unique; trim-непустое, сохраняется Unicode, поиск exact normalized whitespace/casefold, без нечёткого слияния. Несколько совпадений требуют ID выбора; преподаватели тоже.

Предлагаем grade 0..100 включительно, максимум 2 decimal places; NULL = ещё нет итоговой оценки, не ноль. Одна итоговая оценка на enrollment; пересдача в другом offering допустима и учитывается отдельной записью; история попыток внутри offering вне scope. Course отличается от проведения (Offering); одинаковый курс в двух семестрах не одна запись. Семестр задаётся явным ID, даты start<=end; молчаливого «текущего» нет: запрос без времени означает all semesters с подписью области. Если пользователь говорит «текущий», при отсутствии однозначной настройки уточнять.

AVG = сумма non-NULL grade / число graded enrollments; без кредитных весов, без mean-of-means, без округления до последнего форматирования. Counts явно разделены enrollment_count, graded_count, distinct_student_count. Для «средней студента» все его graded enrollments одинакового веса; «по курсу» — все соответствующие enrollments всех выбранных offerings. Top возвращает **всех** tied по точному среднему (сравнение рациональных sum/count), порядок ID для стабильности, NULL не участвует. Ноль graded → null average и объяснение, а не 0. Decimal arithmetic/точное хранение в будущей реализации проверить: предпочтение хранить целые grade hundredths, внешне decimal (см. contracts); имена/семестры не из текущей даты.

Альтернативы: credit-weighted требует credit данных; latest-retake-only меняет смысл без запроса; teacher co-teaching требует junction; current semester default скрывает scope. Эти варианты не «неправильные», но расширяют модель и требуют согласования. Однозначные domain ограничения не являются доказательством семантической правильности любого SQL.

## Граф и содержательный dependent path
START → validate_input → load_schema → resolve_scope → [clarify/plan] → validate_plan → bind_results → generate_sql → validate_sql → execute → inspect_result → [next_step/answer/error] → END. Clarify: interrupt + checkpoint → resume validation → resolve_scope. SQL repair возвращает generate_sql максимум один раз, не бесконечный цикл; provider transient retry максимум один. Refusal, incomplete, unsafe SQL, incoherent results, depleted budget идут error. Empty/no grades — normal с объяснением. Clarify limit 2 на всю беседу.

Пример: «В S1 выбери курс с наивысшей средней итоговой оценкой; затем покажи средние его студентов по всем их курсам в S1». Step1 DB возвращает exact integer sum_units/graded_count/enrollment_count для всех курсов; University domain result adapter выбирает все tied course IDs без округления; step2 использует **полученные**, а не угаданные IDs для cohort distinct student IDs; step3 агрегирует все S1 enrollments выбранных студентов. В плане сохраняются typed symbolic references на declared ResultSpec outputs предшественников; validate_plan проверяет DAG до значений, bind_results материализует только completed/consistent/nontruncated результаты непосредственно перед dependent call; даже если оптимизатор объединит операции, fixture mutation должна менять cohort. Обычные запросы не заставляются делать 3 SQL. Предел — 3 executed logical SQL steps, кроме единственного repair; счётчики общие через resume.

## Schema-agnostic доказательство
Core видит versioned SchemaDescriptor: tables/columns/types/keys/allowed functions/semantic metrics/entity disambiguation metadata, а не Students или grade. University adapter поставляет семантику выше и конечный registry ResultSpec/domain result adapter (units/grain/components); core не угадывает semantics по именам колонок. Library заменяет registry/adapter/descriptor, не core; это не универсальный query compiler. Второй adapter Library: Readers(reader_id,name), Books(book_id,title), Loans(loan_id,reader_id,book_id,returned boolean); metric open_loans = count returned=false. Тот же SQLite dialect/driver/graph/validator/trace/UI. Замена только DB fixture и descriptor/domain vocabulary; не обещаем другие SQL dialects. Проверка: core tree hash неизменен, test L1 из test-plan проходит настоящим DB и отдельно live NL. Если требуется правка core по имени таблицы — R-05 fail.

## Pre-mortem (3)
1. Красивый ответ, неверный JOIN/mean-of-means. Меры: независимые sum/count oracle, adversarial unequal groups, distinct cohort, обязательный regression; fail semantic eval даже при valid SQL.
2. Interrupt повторил платные вызовы/выдал чужой resume. Меры: side-effect-free clarify node, server-bound session/run/checkpoint, consumed request IDs, stale/version checks, global budgets; tests C1–C4.
3. Демо готово локально, сдача/объяснение не доказаны. Меры: clean clone, public access+remote SHA только отдельным разрешением, owner rehearsal; R-15/16 не закрывать docs commit.

Связанные [контракты](../../plans/contracts.md), [тесты](../../plans/test-plan.md), [этапы](../../plans/implementation-plan.md), [production](../../plans/production-considerations.md), [матрица](../../plans/requirements-test-matrix.md). Stop: вернуть proposed пакет в чат; B не даёт execution authorization.
<!-- END FILE: architecture-proposal.md -->


<!-- BEGIN FILE: changes-from-iteration-1.md -->
# Изменения после iteration 1

Planner revision, 2026-11-07. **Proposed**, не Architect/Critic approval. Полные завершённые reviews iteration1 Architect→Critic прочитаны; их iterate verdict сохранён, старые bytes не меняются. Исправления документальные, приложения и новых dependencies нет.

| Finding | Изменение | Проверка/будущий pass criterion |
|---|---|---|
| B1 static/runtime dependencies | contracts: validate_plan по typed declared ResultSpec и DAG; bind_results только completed/consistent/nontruncated; PLAN_INVALID/DEPENDENCY_INVALID/RESULT_TOO_LARGE; полный M1 JSON + точные mutations; architecture phases согласованы | D1 принимает полный plan до SQL, cycle/missing alias rejects; D2 materializes изменившийся cohort; D3 blocks downstream. Сейчас выполнен documentary walkthrough, не graph run |
| B2 units/grain/aggregate boundary | конечный ResultSpec registry+DomainResultAdapter, integer sum_units/graded_count/enrollment_count, exact rational ties+round half-up2; typed examples S6/M1/ties/Library и malformed spec/results; core без University heuristics | V1 16000/2/100→80.00, ties оба курса, library1/1, wrong unit/denom/grain fail; V2 подчёркивает необходимость независимого oracle |
| B3 real model vs injected faults | E/EI deterministic lane с profile/fixture/injection provenance и0paid calls; real48conversation gate с N1–N4 no-data вместо требуемых refusal/SQL errors; unexpected failures count fail | Никакой injected result не live accuracy; budget unchanged conservative480calls/$1.056+$2proposedcap; test-plan/matrix/ADR007/I4 согласованы |
| B4 accepted screen | local expanders answer+SQL/bindings+typed DB rows+full same-run trace/attempts; clarification/resume/error explicit noSQL states | UI1 success/resume/EI multiple attempts checklist, opaque ID fail; architecture/I1/I4/R06/R17 согласованы |
| A1 strict provider wire | bounded closed Binding array, explicit discriminated nullable slots и deterministic SQLite map; duplicate/placeholder/type checks | W1 valid map, malformed rejects; SDK compatibility future not claimed; no new library |
| A2 resources | byte/token accounting distinction, SQL/param/input/single-value boundaries, residual SQLite pre-fetch memory risk | W2/W3 boundaries; no hard tokenizer/memory isolation claim; production остаточный риск сохранён |

Сохранены: proposed owner decisions; все17R+8U; independent fixture numbers; три pre-mortem; production distinctions; A/история/research; никаких live calls/SQL executable/test code/runtime prompts/UI implementation. Дополнительный research не потребовался. Exact candidate package compatibility/security audit и owner budget остаются будущими gates.

Mapping прежний: six main docs→docs/plans; ADR003–007→docs/adr; additions→отдельный index-additions и последующая интеграция лидером; changes-from-iteration-1→docs/ai/omx/H-006-B2-iteration-2-changes.md. Bundle включает полные bytes всех13constituents; manifest hashes raw, не OMX domain-separated lifecycle digests. После freeze изменения только новой iteration. Следующий шаг лидера — отдельный Architect→отдельный Critic→настроенные gates, не execution handoff.
<!-- END FILE: changes-from-iteration-1.md -->


<!-- BEGIN FILE: changes-from-iteration-2.md -->
# Малая revision после iteration 2

Planner, 2026-11-07. Status proposed; не approval/closeout. Полные завершённые Architect2/Critic2 прочитаны; оба iterate с единственным остаточным blocker B2-R1. Остальные ранее проверенные решения не менялись; changes-from-iteration-1.md сохранён байт-в-байт как история коррекции.

| Finding | Edit | Verification / disposition |
|---|---|---|
| B2-R1: row-level COALESCE не нормализует пустой scalar SUM | contracts normative sum → aggregate-level COALESCE(SUM(grade_units),0), integer0; nonnull ResultSpec сохранён; три полных typed raw DBResult→Answer examples Z1/Z2/Z3 | [0,0,0]→null/no_rows;[0,0,1]→null/no_grades;[0,1,1]→"0.00"/null. Documentary JSON/type/consistency checks выполнены; addressed pending new independent reviews |
| Согласованность oracle/test scope | S10/N1–N3/V1 ссылаются на exact raw components; DB-Z отдельно actual SQLite raw-output integration, UNIT-Z отдельно pure adapter normalization | Оба future checks обязательны, не подменяют друг друга; invalid nullable raw sum→RESULT_CONTRACT_INVALID. Ни один product test не выполнялся |
| Decision traceability | ADR-OMX-006 уточняет aggregate normalization и DB-Z/UNIT-Z | Минимальная правка существующей proposed boundary, без nullable raw schema expansion/new dependency |

Альтернатива nullable raw sum + normalization до typed validation отвергнута как лишнее усложнение: outer COALESCE сохраняет текущий strict ResultSpec и границы. Scalar row_count1 при enrollment_count0 явно различён с исходными rows; grouped missing rows не обещаны автоматически. Units/counts/rounding/NULL политики сохранены.

Iteration1/2 и reviews immutable. Bundle включает все14constituents полными bytes, manifest raw SHA256; это не OMX domain-separated lifecycle digest. Mapping шести основных documents/ADR прежний; этот файл→docs/ai/omx/H-006-B2-iteration-3-changes.md после supported closeout. Новый research, SQL probe, executable schema/seed, application/tests/UI/runtime prompts, dependencies, paid calls не выполнялись. Следующий шаг — отдельные Architect3→Critic3, не execution authorization.
<!-- END FILE: changes-from-iteration-2.md -->


<!-- BEGIN FILE: contracts.md -->
# Контракты v1 — proposed

Дата 2026-11-07; не реализация. Все JSON объекты closed (`additionalProperties:false`), указанные поля required, nullable означает явный null; UTF-8, конечные числа, no NaN/Infinity. IDs opaque непустые строки <=128; timestamps UTC RFC3339. Неподдерживаемая version — error INVALID_INPUT до LLM/DB. Будущий внешний JSON schema и strict provider schema — отдельные реализации одного контракта, не предположение о полном JSON Schema support у провайдера.

## Input и продолжение
NewRequest: {version:"1", kind:"new", request_id:ID, schema_id:ID, question:string 1..2000}. Session identity поступает из server-side UI session, не доверяется полю пользователя. request_id для идемпотентности; одинаковый ID/bytes в той же session возвращает сохранённый response без повторных calls; другой payload с тем же ID → REPLAY_CONFLICT.
ResumeRequest: {version:"1",kind:"resume",request_id:ID,run_id:ID,checkpoint_id:ID,clarification_id:ID,selection:string}. selection только один из option.value; freeform при field=semester допускается лишь после descriptor validation. На v1 все уточнения имеют конечные options, значит произвольный freeform отвергается.

Valid new: `{"version":"1","kind":"new","request_id":"q1","schema_id":"university-v1","question":"Средняя по C1 в S1?"}`.
Valid resume: `{"version":"1","kind":"resume","request_id":"q2","run_id":"r1","checkpoint_id":"cp1","clarification_id":"cl1","selection":"student:1"}`.
Invalid: `{"version":"1","kind":"new","request_id":"q1","schema_id":"university-v1","question":"","sql":"DROP TABLE Students"}` — empty question и extra sql, без обращения к модели. Invalid resume selection student:99 при options 1/3 — INVALID_SELECTION, существующая пауза не потребляется.

Resume привязан к текущей server session, run, последнему checkpoint, clarification, schema/content hash и policy_version. Несовпадение owner → RESUME_FORBIDDEN (без раскрытия существования чужого run); старый checkpoint или schema hash → STALE_RESUME; истёкший срок 15 min/перезапуск InMemorySaver → RESUME_EXPIRED, создать новый вопрос по явному действию UI. На accepted resume consumed atomically; exact request replay возвращает предыдущий ответ; иной request после consumption → STALE_RESUME. Graph thread_id серверный и тот же при Command(resume); не брать произвольный thread от клиента. Счётчики calls/SQL/clarifications и elapsed active work не сбрасываются. Interrupt-узел не выполняет LLM/DB calls до interrupt: LangGraph перезапускает его с начала.

## Output envelope
{version:"1",run_id:ID,status:"ok"|"clarification"|"error",answer:Answer|null,clarification:Clarification|null,error:Error|null,trace_id:ID}.
Ровно соответствующая status ветка non-null. Answer: {text:string,columns:[{name:string,type:"string"|"integer"|"decimal"|"boolean"}],rows:array<array<scalar|null>>,scope:string,empty_reason:null|"no_rows"|"no_grades",truncated:boolean}. decimal в JSON строкой с каноническими decimal digits (например "83.33"); числа-целые для counts/IDs, не округлять внутренние суммы. Значение NULL не значит empty row. Табличная normal форма и объяснение всегда совпадают; ответ шаблонный, без отдельного генератора чисел LLM.
Clarification: {clarification_id:ID,checkpoint_id:ID,field:string,prompt:string,options:[{value:string,label:string}],expires_at:timestamp}; options >=2, уникальные values, labels отличают записи ID/контекстом. Error: {code:enum,message:string,retryable:boolean,failed_node:string}; не раскрывает raw provider exception/paths/credentials. retryable значит пользователь может начать новый запрос, а не разрешение дополнительного внутреннего retry.

Valid normal: `{"version":"1","run_id":"r1","status":"ok","answer":{"text":"C1, S1: 83.33 (3 оценки).","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"}],"rows":[["83.33",3]],"scope":"C1; S1","empty_reason":null,"truncated":false},"clarification":null,"error":null,"trace_id":"t1"}`.
Valid clarification: `{"version":"1","run_id":"r2","status":"clarification","answer":null,"clarification":{"clarification_id":"cl1","checkpoint_id":"cp1","field":"student","prompt":"Какой Alex?","options":[{"value":"student:1","label":"Alex (1)"},{"value":"student:3","label":"Alex (3)"}],"expires_at":"2026-11-07T12:15:00Z"},"error":null,"trace_id":"t2"}`.
Valid error: `{"version":"1","run_id":"r3","status":"error","answer":null,"clarification":null,"error":{"code":"SQL_TIMEOUT","message":"Запрос превысил лимит времени.","retryable":true,"failed_node":"execute"},"trace_id":"t3"}`.
Invalid envelope: status ok с answer=null либо error non-null; decimal JSON number вместо string; row length != columns; NaN; неизвестный code; extra property. Ошибка в собственном output → INTERNAL_CONTRACT, fail closed, без fabricated answer.

## Internal state и адаптеры
GraphState required: version, run_id, session_ref (private), request_id, schema_id, schema_hash, policy_version, question, phase (node enum из архитектуры), resolved_scope (map entity→IDs / semester IDs), plan (Step[]), current_step integer, results (map step ID→Result), counters {llm_calls,sql_attempts,repairs,clarifications,graph_steps,input_tokens,output_tokens}, active_ms integer, deadline_at timestamp, checkpoint_id nullable, clarification_id nullable, consumed_request_ids[], terminal nullable Output. Persist only bounded state, not provider client/DB handle. InMemorySaver только local demo; after restart no recovery promise.
Step={step_id:ID,depends_on:ID[],purpose:Text,result_refs:Reference[],result_spec:ResultSpec}; DAG, <=3 logical steps, symbolic references к объявленным outputs предшественников DAG принимаются до выполнения; static и runtime фазы определены ниже. LLM Request получает question, descriptor, explicit scope, completed step references и budgets; не raw DB dump. LLM SqlProposal={version:"1",step_id:string,result_spec:ResultSpec,sql:string<=8000,parameters:array<Binding>,expected_columns:[string],result_kind:"rows"|"aggregate",explanation:string<=1000}. Все поля required. Это hypothesis, не permission. Model cannot add steps outside validated plan. Parameter placeholders для values; identifiers только descriptor allowlist.
SchemaDescriptor={version:"1",schema_id,content_hash,dialect:"sqlite",tables:[{name,columns:[{name,type,nullable}],primary_key:[string],foreign_keys:[{columns,table,target_columns}]}],entities:[{name,table,id_column,name_column}],metrics:[{name,definition,unit,null_policy,grain}],allowed_functions:[string],policy_version}. Strings definitions — domain context, не executable instructions. Hash covers canonical descriptor+domain policy; identifiers verified against DB metadata. Descriptor загрузка и integrity scan обязательны до requests.
DB Result={step_id,result_spec,columns:[{name,type}],rows:array,row_count:int,truncated:bool,elapsed_ms:int}; SQL adapter должен отдавать typed values, не пересчитывать averages после truncation. SQL Validator обязан проверять single statement, allowlisted schema/functions, readonly operations и resolved entity/scope references; authorizer deny DML/DDL/ATTACH/DETACH/PRAGMA/nonallowlisted reads/functions и extension loading; URI mode=ro. Не использовать regex как доказательство. Если безопасный parser/compiled authorization не позволяет установить требуемое свойство — reject, не запускать. Query-only дополнительный слой, не замена read-only. Repair разрешён лишь для recoverable syntax/unknown column, не unsafe SQL и не semantic mismatch.
Answer formatter проверяет column types, count>=0, graded<=enrollment, grade/average range, declared grain и scoped IDs; inconsistency → DATA_INCONSISTENT. Integrity scan проверяет FK, дубликаты ключей, grade range. Невозможно детерминированно доказать произвольный NL→SQL; правдоподобный неверный SQL обнаруживается oracle eval, не обещанным runtime «пониманием».

## Budgets, ошибки и truncation
На всю беседу: 2 clarification pauses, 3 logical SQL steps + 1 repair execution =4 SQL attempts; максимум 5 provider calls, включая transient retry и repair (что закончится первым). 12k input accounting ceiling (pre-call byte gate и caveat ниже)/2k total output tokens на call; суммарно 60k/10k; graph recursion_limit=32 supersteps плюс собственный persisted graph_steps<=64 через resume. Один provider timeout 15s, один transient retry с 1s backoff, SDK auto-retries отключить чтобы не умножались. SQL cooperative timeout 2s progress handler; lock wait <=0.5s. Общий active work 60s, не включает ожидание человека; watchdog завершает DB worker при 3s, весь run при 60s. Worker isolation — будущая реализация, не гарантия Python progress handler. Trace failure до исполнения → TRACE_UNAVAILABLE, не выполнять нетрассируемый query.
Результаты: максимум 100 displayed rows, читать 101 для detection, <=64KiB/result, <=128KiB retained run result payload. Для aggregates cap применяется **после агрегации**, не LIMIT входных enrollments. Exact scalar aggregates считают все scoped строки. Truncated grouped/top/cohort result нельзя использовать как полный dependency: RESULT_TOO_LARGE и предложение сузить scope, без partial final claims. Для обычного списка допускается normal truncated=true с явной подписью «первые 100», deterministic ORDER BY и без полного-count утверждения. Oversize string/result → RESULT_TOO_LARGE.
Error codes: PLAN_INVALID, DEPENDENCY_INVALID, RESULT_CONTRACT_INVALID, RESOURCE_LIMIT, INVALID_INPUT, REPLAY_CONFLICT, INVALID_SELECTION, RESUME_FORBIDDEN, STALE_RESUME, RESUME_EXPIRED, CLARIFICATION_LIMIT, UNSAFE_SQL, SQL_INVALID (после 1 repair), SQL_TIMEOUT, DB_UNAVAILABLE, DATA_INCONSISTENT, PROVIDER_UNAVAILABLE (после 1 transient retry), PROVIDER_REFUSAL (0 retry), PROVIDER_INCOMPLETE (0 retry), PROVIDER_INVALID_OUTPUT (0 retry), BUDGET_EXCEEDED, RESULT_TOO_LARGE, TRACE_UNAVAILABLE, INTERNAL_CONTRACT. Без rows normal no_rows; enrolled/no grades normal no_grades и null avg/0 graded. Credentials absence → PROVIDER_UNAVAILABLE до сетевого call. Все terminal errors сохраняют last successful steps в trace, но не выдают их как полный ответ.

## Trace v1
Event required: version:"1",trace_id,run_id,event_id,seq:int>=1,parent_event_id:null|ID,request_id,node,kind (input|node_start|llm_attempt|sql_validated|sql_attempt|db_result|clarification|resume|node_end|answer|error|run_end),attempt:int>=0,timestamp,duration_ms:null|int,payload:object. Каждая попытка имеет собственный event_id; immutable append, monotonic seq, пары start/end либо error; run_end ровно один для terminal run (pause не terminal). LLM payload: requested/returned model IDs, prompt/template hashes, schema/data versions, input/output token usage, provider request ID безопасный или redacted. SQL payload: SQL, sanitized bound params, validation decision; DB payload: columns/rows/truncated/row_count/hash. Полная цепь input→nodes→SQL→DB rows→answer либо error; trace и visible answer имеют один run_id.
Локально только synthetic fixtures: полный question/SQL/rows допустим. Не логировать keys, auth headers, env, private paths, hidden chain-of-thought, raw provider diagnostics. Реальные персональные данные не входят в demo: остановка/редакция на ingress; public export whitelist fields+PII review, redaction marker + hash исходного локального payload, не обещать повторяемость redacted contents. Public examples только synthetic. Trace budget 1MiB/run; превышение → BUDGET_EXCEEDED с minimal terminal event в зарезервированном 4KiB, запись failure → UI сообщает trace unavailable и run не считается доказательством.

## Уточнение типов внутренних сообщений (нормативное v1)
В compact signatures выше каждое поле required; ниже исчерпывающие aliases снимают неоднозначность. ID=string1..128, Hash=64 lowercase hex, Text=string<=2000, Name=string1..128, UInt=integer>=0, Scalar=string|integer|boolean|null, Decimal=canonical string matching -?[0-9]+(.[0-9]+)?, no exponent. SQL parameters boolean передаётся как integer0/1; В v1 numeric grade bindings только integer grade_units; numeric decimal-string bindings не допускаются (text Binding остаётся обычным text). Grade physical column **grade_units INTEGER NULL** в Enrollments, constrained0..10000. Имя grade в концептуальном ERD/fixtures — внешняя семантическая проекция grade_units/100; generated SQL работает с grade_units, decimal formatter переводит sum_units/count/100. Metric descriptor сообщает unit и formula. Нельзя смешивать 90 с9000. Если будущая реализация сохраняет conceptual `grade` как physical имя, это отдельная reviewed contract revision, не незаметная замена.

GraphState: version literal"1"; run_id/session_ref/request_id/schema_id ID; schema_hash Hash; policy_version Name; question Text; phase enum(validate_input,load_schema,resolve_scope,clarify,plan,validate_plan,bind_results,generate_sql,validate_sql,execute,inspect_result,next_step,answer,error,end); resolved_scope map<Name,array<ID>>; plan array<Step>0..3; current_step UInt; results map<ID,DBResult>; counters object с перечисленными UInt; active_ms UInt; deadline_at RFC3339; checkpoint_id/clarification_id ID|null; consumed_request_ids array<ID> max16; terminal Output|null. Missing values до вычисления: empty maps/arrays, counters0, nullable fields null; не omission. session_ref никогда не публикуется. Counters.persisted includes failed attempts, вызовы plan generation тоже.
Step: step_id ID; depends_on array<ID> max2; purpose Text; result_refs array<Reference> max3; result_spec ResultSpec; references статически проверяются по declared ResultSpec предшественника; значения связываются лишь в runtime bind_results. PlanProposal={version:"1",steps:array<Step>1..3,needs_clarification:boolean,clarification_field:Name|null}; if needs_clarification true steps=[] (исключение min1), field non-null; false field=null. Не позволять LLM выдавать произвольные options: entity resolver создаёт options из известного bounded каталога.
LLMRequest={version:"1",operation:"plan"|"sql"|"repair",run_id:ID,attempt:UInt,model_id:Name,question:Text,descriptor:SchemaDescriptor,scope:map<Name,array<ID>>,plan:array<Step>,completed_results:map<ID,DBResult>,previous_error:SafeDiagnostic|null,budget:{remaining_calls:UInt,max_input_tokens:UInt,max_output_tokens:UInt},prompt_hash:Hash}. SafeDiagnostic={code:Name,message:Text}; не raw exception. Response для operation plan строго PlanProposal, для sql/repair строго SqlProposal. В normal простом запросе допустим fused plan+SQL? **Нет в v1**: plan call + sql call; dependent3 steps требует4calls, пятая для retry/repair, оба одновременно могут исчерпать budget. Failure BUDGET_EXCEEDED честнее скрытого sixth call. Prior state и schema descriptor считаются частью input token budget. Truncated completed_results запрещены для dependent step.
SchemaDescriptor: version literal"1"; schema_id ID; content_hash Hash; dialect literal"sqlite"; tables array<Table>1..32; entities array<Entity>0..16; metrics array<Metric>0..32; allowed_functions array<Name>0..32; policy_version Name. Table={name:Name,columns:array<Column>1..64,primary_key:array<Name>1..8,foreign_keys:array<ForeignKey>0..16}; Column={name:Name,type:"integer"|"text"|"boolean",nullable:boolean}; ForeignKey={columns:array<Name>1..8,table:Name,target_columns:array<Name>1..8}, lengths equal; Entity={name:Name,table:Name,id_column:Name,name_column:Name}; Metric={name:Name,definition:Text,unit:Name,null_policy:"exclude"|"include",grain:array<Name>1..8}. Content hash excludes own hash field, canonical UTF8 JSON sorted keys; включает все остальные поля descriptor и domain policy versioned text. Независимый DB content hash записан run trace metadata, не подменяет schema hash.
DBResult: step_id ID; result_spec ResultSpec (копия verified spec от execution adapter, не provider metadata); columns array<{name:Name,type:"string"|"integer"|"decimal"|"boolean"}>; rows array<array<Scalar>> (decimal subtype serialized string), row_count UInt equals returned rows.length; truncated boolean; elapsed_ms UInt. No nullable fields besides row scalar. SQLProposal version literal"1",step_id ID,result_spec ResultSpec,sql string1..8000,parameters array<Binding>0..100,expected_columns array<Name>1..32,result_kind enum rows/aggregate,explanation string0..1000. Каждый column nullable по результату SQL, не только physical column; formatter проверяет zero-denominator/null cases отдельно.
Startup adapter integrity scan строит bounded entity catalog (<=1000 entities/schema, otherwise unsupported demo dataset) с IDs и normalized names из DB; он входит в data snapshot hash. resolve_scope читает этот каталог, не генерирует SQL и не оплачивает LLM для выбора duplicate names. Dataset read-only и immutable весь process lifetime; смена DB/descriptor reload инвалидирует catalog/checkpoints. Поэтому C1 «0 SQL до выбора» относится к request execution после startup, а не к initial DB metadata/catalog reads; startup reads отдельно фиксируются как diagnostic trace, не прячутся в request budgets. Atomic resolve of arbitrary production datasets вне scope. Students/Teachers ambiguity определяется до plan call; LLM тоже может вернуть needs_clarification, тогда только проверяемый field и deterministic options, иначе INVALID_INPUT.

## Двухфазный DAG и минимальный ResultSpec (iteration 2, нормативно)
Контракты этого раздела уточняют Step/ResultSpec и ответственность адаптера; не вводят query compiler или новую зависимость. Все поля required/closed; незнакомые fields/metric IDs отвергаются. SQL по-прежнему генерирует настоящая модель, независимый oracle остаётся нужен.

ResultSpec={metric_id:Name,shape:"rows"|"aggregate"|"top",group_keys:array<Name>0..4,columns:array<ResultColumn>1..16,components:{sum:Name|null,denominator:Name|null,count:Name|null},unit:Name,scale:integer>=1}. ResultColumn={name:Name,type:"integer"|"string"|"boolean",nullable:boolean}. Reference={from_step:ID,column:Name,type:"integer"|"string"|"boolean",bind_as:Name}; bind_as unique within step; source column must exist and match type, cannot nullable for ID dependency. Все эти схемы closed, components присутствует даже с тремя null.
DomainResultAdapter receives {spec:ResultSpec,raw:DBResult,scope:resolved_scope} and returns {columns:Answer.columns,rows:Answer.rows,dependency_rows:typed rows,empty_reason:nullable enum}. Этот объект внутренний, поля required; dependency_rows удовлетворяет ResultSpec columns и не содержит fabricated values. Core проверяет schema/types, DAG/limits и вызывает зарегистрированный adapter по schema_id+metric_id; **не распознаёт University по имени sum_units/grade**. Адаптер проверяет exact equality spec с одной из зарегистрированных shapes, keys/uniqueness/ranges/components и нормализует. Metric IDs — конечный registry, не произвольный DSL; поддержка нового metric — изменение domain adapter/test cases, не core.
University registry: `u.grade_mean.v1` shape aggregate, keys[] или [student_id]/[course_id]/[teacher_id]/[offering_id] из allowlist; integer sum_units,graded_count,enrollment_count, unit grade_hundredth,scale100, components sum=sum_units,denominator=graded_count,count=enrollment_count. `u.top_course.v1` та же grade shape с group_keys=[course_id], shape top; `u.student_ids.v1` shape rows, group_keys=[student_id], единственная nonnull integer student_id, unit identifier,scale1, components all null. Для деталей JOIN допускается `u.enrollment_rows.v1`: keys=[student_id,offering_id], columns student_id/offering_id/course_id/teacher_id integers, student_name/course_title/teacher_name/semester_id strings, grade_units integer nullable; unit grade_hundredth,scale100, components all null. Count-only `u.enrollment_counts.v1` shape aggregate, approved group key sets как mean, columns enrollment_count/graded_count/distinct_student_count nonnull integers, unit count,scale1, components sum=null,denominator=null,count=enrollment_count. Метрики fixture S1–S14 реализуются этими shapes; комбинированные count/mean выводы formatter получает через зарегистрированный mean extension с distinct_student_count (явно разрешённый integer alias, не свободное extra поле).
Library registry: `l.open_count.v1` shape aggregate, group_keys=[reader_id], columns reader_id integer,name string,open_count integer nonnull; unit count,scale1, components sum=null,denominator=null,count=open_count. Registry и вторая DB — domain-only изменения. При значении0 строка каждого reader сохраняется; count не превращается в average.
Для mean SQL должен вернуть integer COALESCE(SUM(grade_units),0) (aggregate-level normalization с integer zero), COUNT(grade_units), COUNT(*) по scoped enrollment relation (enrollment_count); zero denominator требует sum_units=0, вывод average=null, no_grades при enrollment>0 и no_rows иначе. sum_units>=0, graded_count<=enrollment_count и sum_units<=10000*graded_count. Среднее и top comparison выполняет **University result adapter** exact rational arithmetic: sum_units/(100*graded_count), сравнение cross multiplication без rounding, для final display decimal half-up2. Top adapter получает все candidate aggregates, исключает denom0 и оставляет все exact maximal ties; truncated candidates → RESULT_TOO_LARGE, нельзя SQL rounded LIMIT1. group keys уникальны; лишние ключи/колонки или отсутствующий denominator → RESULT_CONTRACT_INVALID до answer/downstream. DB wrapper проверяет raw names/types/rows по spec; сама SQLite не возвращает unit metadata, поэтому verified spec copied из accepted step, SQLProposal spec обязан ему точно соответствовать. Неправильная арифметика в SQL при правдоподобных aggregates всё ещё возможна: runtime bounds не доказывают query semantics, oracle проверяет это отдельно.

Фаза `validate_plan`: до первого SQL, после plan call — unique step IDs, <=3, ацикличность, топологический порядок массива, depends_on предшествуют, каждый Reference.from_step перечислен в depends_on, объявленные aliases/types/nonnull совместимы; ResultSpecs принадлежат registry. **Значения предшественника ещё не нужны.** Ошибка DAG/reference/shape → PLAN_INVALID, failed_node=validate_plan; никаких downstream SQL/provider calls (plan call уже учтён).
Фаза `bind_results`: перед generate_sql каждого dependent step — все dependencies completed+domain-validated+нетранкированные; реально присутствуют alias/type, runtime values дедуплицируются и сортируются по typed ID. Missing result/column/type/consistency → DEPENDENCY_INVALID, failed_node=bind_results; truncated → RESULT_TOO_LARGE в bind_results; никаких calls downstream. Empty dependency → short-circuit normal empty answer/no_rows, не запрос «все студенты» и не SQL IN(). DB shape failure исходного step → RESULT_CONTRACT_INVALID в inspect_result прежде bind_results. Cases runtime type mismatch тестируют corrupted injected state, недостижимое через корректный inspect_result, но защита fail closed обязательна.

### Полные JSON examples (документы, не выполненные вызовы)
Valid M1 PlanProposal принимается validate_plan до results:
```json
{
  "version": "1",
  "steps": [
    {
      "step_id": "top",
      "depends_on": [],
      "purpose": "Средние курсов S1, выбрать все максимальные",
      "result_refs": [],
      "result_spec": {
        "metric_id": "u.top_course.v1",
        "shape": "top",
        "group_keys": [
          "course_id"
        ],
        "columns": [
          {
            "name": "course_id",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "sum_units",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "graded_count",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "enrollment_count",
            "type": "integer",
            "nullable": false
          }
        ],
        "components": {
          "sum": "sum_units",
          "denominator": "graded_count",
          "count": "enrollment_count"
        },
        "unit": "grade_hundredth",
        "scale": 100
      }
    },
    {
      "step_id": "cohort",
      "depends_on": [
        "top"
      ],
      "purpose": "Distinct students выбранных курсов S1",
      "result_refs": [
        {
          "from_step": "top",
          "column": "course_id",
          "type": "integer",
          "bind_as": "course_ids"
        }
      ],
      "result_spec": {
        "metric_id": "u.student_ids.v1",
        "shape": "rows",
        "group_keys": [
          "student_id"
        ],
        "columns": [
          {
            "name": "student_id",
            "type": "integer",
            "nullable": false
          }
        ],
        "components": {
          "sum": null,
          "denominator": null,
          "count": null
        },
        "unit": "identifier",
        "scale": 1
      }
    },
    {
      "step_id": "means",
      "depends_on": [
        "cohort"
      ],
      "purpose": "Средние выбранных студентов по всем курсам S1",
      "result_refs": [
        {
          "from_step": "cohort",
          "column": "student_id",
          "type": "integer",
          "bind_as": "student_ids"
        }
      ],
      "result_spec": {
        "metric_id": "u.grade_mean.v1",
        "shape": "aggregate",
        "group_keys": [
          "student_id"
        ],
        "columns": [
          {
            "name": "student_id",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "sum_units",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "graded_count",
            "type": "integer",
            "nullable": false
          },
          {
            "name": "enrollment_count",
            "type": "integer",
            "nullable": false
          }
        ],
        "components": {
          "sum": "sum_units",
          "denominator": "graded_count",
          "count": "enrollment_count"
        },
        "unit": "grade_hundredth",
        "scale": 100
      }
    }
  ],
  "needs_clarification": false,
  "clarification_field": null
}
```

S6 raw DBResult → adapter→ average80.00, graded2,enrollment2:
```json
{"step_id":"s6","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[16000,2,2]],"row_count":1,"truncated":false,"elapsed_ms":1}
```

M1 top raw F1 → adapter dependency_rows [[2,10000,1,1]], не course1:
```json
{"step_id":"top","result_spec":{"metric_id":"u.top_course.v1","shape":"top","group_keys":["course_id"],"columns":[{"name":"course_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"course_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,25000,3,4],[2,10000,1,1],[3,0,0,1]],"row_count":3,"truncated":false,"elapsed_ms":1}
```

Tie fixture top raw → dependency_rows обе строки course1/course2, equality27000*1=9000*3:
```json
{"step_id":"top","result_spec":{"metric_id":"u.top_course.v1","shape":"top","group_keys":["course_id"],"columns":[{"name":"course_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"course_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,27000,3,4],[2,9000,1,1],[3,0,0,1]],"row_count":3,"truncated":false,"elapsed_ms":1}
```

M1 final raw F1 → student1 average95.00:
```json
{"step_id":"means","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":["student_id"],"columns":[{"name":"student_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"student_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,19000,2,2]],"row_count":1,"truncated":false,"elapsed_ms":1}
```

Library raw → names/counts Ada1,Bob1 без grade normalization:
```json
{"step_id":"library","result_spec":{"metric_id":"l.open_count.v1","shape":"aggregate","group_keys":["reader_id"],"columns":[{"name":"reader_id","type":"integer","nullable":false},{"name":"name","type":"string","nullable":false},{"name":"open_count","type":"integer","nullable":false}],"components":{"sum":null,"denominator":null,"count":"open_count"},"unit":"count","scale":1},"columns":[{"name":"reader_id","type":"integer"},{"name":"name","type":"string"},{"name":"open_count","type":"integer"}],"rows":[[1,"Ada",1],[2,"Bob",1]],"row_count":2,"truncated":false,"elapsed_ms":1}
```

Invalid examples задаются точными JSON Patch-like mutations валидных полных examples (не отдельный wire тип):
- M1 `steps[0].depends_on=["means"]` и `steps[0].result_refs=[{"from_step":"means","column":"student_id","type":"integer","bind_as":"x"}]` создают цикл → PLAN_INVALID/validate_plan,0 SQL.
- M1 `steps[1].result_refs[0].column="missing_id"` → PLAN_INVALID/validate_plan,0 SQL.
- В успешно completed top после validation injected `truncated=true` → RESULT_TOO_LARGE/bind_results; cohort provider/SQL calls0.
- S6 result_spec.unit="grade" или scale=1 при ожидаемом grade_hundredth/100 → RESULT_CONTRACT_INVALID/inspect_result (если это SQLProposal mismatch, тот же code/validate_sql до execution).
- S6 columns/row исключают graded_count (row=[16000,2]) → RESULT_CONTRACT_INVALID/inspect_result; нельзя принять denominator2 по позиции.
- S6 result_spec.group_keys=["student_id"] при declared[] → RESULT_CONTRACT_INVALID/inspect_result; дубликаты student_id у per-student result → тот же code.
- Injected corrupted top column course_id type string после completion → DEPENDENCY_INVALID/bind_results. Normal typed result failure ловится раньше inspect_result.

### A1: strict provider bindings
Provider SQLProposal wire использует **только bounded closed array**, не динамический map:
Binding={name:Name,type:"integer"|"text"|"null",integer_value:integer|null,text_value:string|null}. Все четыре fields required, additionalProperties=false; integer → integer_value nonnull/text_value null, text → обратное, null → оба null. Name matches [A-Za-z_][A-Za-z0-9_]{0,63}. Parameters<=100; text_value<=2000 UTF8 bytes; суммарные UTF8 encoded JSON bindings<=8192 bytes. duplicate names/type mismatch/unused or missing SQL placeholders → PROVIDER_INVALID_OUTPUT до DB; actual provider schema compatibility smoke ещё future. Для text используем type=text (не SQL Column type), grade units только integer. Dynamic maps в LLMRequest scope/completed_results — внутренний trusted input, не provider output schema.
Пример wire: `[{"name":"student_id","type":"integer","integer_value":2,"text_value":null},{"name":"semester","type":"text","integer_value":null,"text_value":"S1"}]` → deterministic internal sqlite bindings `{"student_id":2,"semester":"S1"}`; placeholders :student_id,:semester. ID-list materialization {1,2} → named placeholders :course_ids_0,:course_ids_1 и два integer Binding, не comma-string. Все SQL placeholders сверяются с accepted bindings; IDs сверяются с resolved scope/materialized dependency. Никакой конкатенации пользовательских values в SQL.100 values max; больший materialized list RESULT_TOO_LARGE до generate_sql.

### A2: resource boundary, без обещания hard memory sandbox
SQL UTF8 bytes<=8000 и chars<=8000; provider output with oversized SQL/bindings → RESOURCE_LIMIT до SQL execution. Request question max2000 chars; encoded provider input общий<=12000 UTF8 bytes как консервативный **локальный byte gate**, не точный tokenizer. Отдельно max_input_tokens12000 остаётся accounting contract: usage>12000 unexpected→BUDGET_EXCEEDED, no subsequent calls. Byte gate не доказывает provider-specific token bound; framing/provider-added tokens неизвестны, поэтому hard pre-call token guarantee не заявляется, projected worst-case token budget резервируется по всем 5calls. Не добавляется непроверенный tokenizer dependency. Single DB text value>8192 UTF8 bytes→RESULT_TOO_LARGE при fetch; result64KiB/retained128KiB/trace1MiB как прежде. SQLite может выделить память до fetch/progress: hard memory isolation **не реализована/не гарантируется дизайном v1**; только локальная synthetic DB и bounded workload, OS memory ceiling/worker resource limits отдельный production risk/проверка до remote deployment. Time watchdog не доказательство memory bound.


Дополнительная связка состояния: `GraphState.results` хранит только завершённые **validated dependency DBResult**: ResultSpec/columns/elapsed_ms сохраняются, rows=DomainResultAdapter.dependency_rows, row_count пересчитан, truncated=false. Полный сырой DBResult записывается в trace до адаптации; top raw candidates и отобранные exact ties видны раздельными node_end payloads. Поэтому bind_results читает уже выбранные top IDs, а не все кандидаты. Поля derived Answer не перезаписывают raw result trace. No-grades per-row annotations формируются domain adapter; для нескольких rows empty_reason envelope=null, NULL в соответствующей average cell и text объяснение; для single all-null scalar empty_reason=no_grades. Count-only metric даже при0 возвращает numeric0 и empty_reason=null. Scope entity IDs во внешнем resume opaque (`student:1`); resolver по descriptor переводит их в реальные typed primary keys для SQL bindings, не делает blind string→integer conversion.


## B2-R1: scalar empty, NULL-only и настоящая нулевая оценка

Нормативная сумма нормализуется **после SUM**: документальная формула `COALESCE(SUM(grade_units),0)`, integer0; denominator=`COUNT(grade_units)`, enrollment_count=`COUNT(*)` по уже отфильтрованной enrollment relation. Не использовать row-level COALESCE как замену aggregate-level normalization: на relation без строк SUM иначе NULL. Для grouped запроса отсутствующая группа не создаётся автоматически; эти examples относятся к scalar aggregate без GROUP BY. Nullable raw sum не разрешается и не «исправляется» formatter-ом. Это документальные сообщения, не выполненные SQL/application calls.

### Z1: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — строка scalar aggregate, не число enrollments):
```json
{"step_id":"z1","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,0,0]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (внешний average в шкале0..100, decimal string либо null):
```json
{"text":"Нет записей на C2 в S2; средняя не определена.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[null,0,0]],"scope":"C2; S2","empty_reason":"no_rows","truncated":false}
```

### Z2: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — строка scalar aggregate, не число enrollments):
```json
{"step_id":"z2","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,0,1]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (внешний average в шкале0..100, decimal string либо null):
```json
{"text":"Одна запись без итоговой оценки; средняя не определена.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[null,0,1]],"scope":"C3; S1","empty_reason":"no_grades","truncated":false}
```

### Z3: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — строка scalar aggregate, не число enrollments):
```json
{"step_id":"z3","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,1,1]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (внешний average в шкале0..100, decimal string либо null):
```json
{"text":"Одна итоговая оценка 0; средняя 0.00.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[["0.00",1,1]],"scope":"synthetic single enrollment grade 0","empty_reason":null,"truncated":false}
```

Z1 normal no_rows, не error: raw aggregate содержит одну строку компонентов при нуле исходных enrollments. Z2 enrollment существует, но denominator0→no_grades. Z3 denominator1→точное0/(100*1)=0, final half-up2="0.00", empty_reason=null. Для N3/student3 действует Z2 с соответствующим scope. NULL average не объявляется0; настоящий grade0 не объявляется отсутствием оценки.
<!-- END FILE: contracts.md -->


<!-- BEGIN FILE: implementation-plan.md -->
# План будущей реализации — proposed, без execution handoff

Цель: компактный работающий и объяснимый demonstrator по [матрице](../../plans/requirements-test-matrix.md), не production service. Нынешний B заканчивается возвратом в чат. Приняты scope/simple screen/dependent scenario/second schema; domain semantics, stack и eval gate лишь рекомендации. A не повторять. Данный документ не разрешает установку, paid calls, создание remote или push.

## Последовательность после отдельного принятия/поручения
| Этап | Dependencies / ресурсы | Deliverables и verification | Commit/manual gate |
|---|---|---|---|
| I0 Зафиксировать решения и бюджет | chat review этого bundle/ADR003–007 | принятые/изменённые semantics, model, eval cap, deadline; presence-only key availability; versions/advisory audit/lock candidate compatibility | отдельный docs decision commit; stop без разрешения live/budget |
| I1 Первый настоящий vertical slice | I0; будущие src/universitydb/{db,agent,llm,tracing,ui}, resources/schema+seed, prompts/; F1 | минимальный реальный LangGraph question S6→Responses→validated SQLite→80.00→JSONL→Streamlit с доступными SQL/bindings/typed DB rows/full same-run trace+attempts; smoke trace+actual prompts; read-only/timeout boundaries до первого generated SQL | small feat+tests commit, owner walkthrough success/SQL guard; не сначала большой каталог abstractions |
| I2 Семантика, запросы и failure paths | I1; schema/domain adapter/contracts | полный F1, S1–S14 oracle DB tests; D1–D3 двухфазные refs, V1–V2 domain result spec/units, W1–W3 bounds; C1–C4 checkpoint/resume; E1–E7 bounded faults; contract unit tests; incremental small commits | targeted tests сначала, compile/lint/typecheck после; chat review average/ties/retakes/clarification |
| I3 Зависимость и переносимость | I2; graph plan/results, library adapter/F1L | M1 F1/F2+tie sensitivity; L1 unchanged core hash, mocked and actual DB tests; traces completeness/redaction | feat portability commit; owner predicts mutation without agent |
| I4 Live eval и full screen E2E | I3, credentials, explicit spending cap; versioned datasets/prompts | development then sealed heldout 48 counted runs; category coverage, all attempts/cost; manual live S6/M1/C1/L1+UI1, отдельно offline injected EI1–EI3 с provenance (не live score); no hidden fallback | eval evidence commit; failures→defect+new version+rerun, не снижение порога |
| I5 Packaging/clean clone/defense | I4 pass; docs/examples/traces/prompt coverage, README | clean install offline suites and approved live smoke; independent manual explanation; public-safe checklist; unresolved requirements remain open | local release docs commit, затем отдельное remote/push authorization; verify remote SHA+anonymous access до R15 closure |

При каждом code step: inspect diff→targeted regression→all offline tests→compile/lint/typecheck available selected tools→explicit staged paths→diff --check→commit→SHA receipt. No blanket staging, no amend/reset foreign changes. Тесты должны существовать до semantic fixes. Prompt changes versioned вместе с regression и eval evidence. Будущие команды определены в test-plan; exact entrypoints подтверждаются при создании кода, не выдаются сейчас за существующие. Future dependencies допускаются только новым implementation поручением; B не установка.

## Минимальные блокеры и вопросы владельцу
1. Принять предлагаемые grade hundredths/0..100/NULL, all-retakes, equal enrollment weights, all ties? Рекомендуем да для объяснимой арифметики; credit/latest-only требуют иных fixtures.
2. Принять all-semesters default с явной подписью и уточнение «текущий»? Рекомендуем без скрытой текущей даты.
3. Принять SQLite+direct LangGraph+Streamlit+local trace, InMemorySaver и отсутствие resume после рестарта? Рекомендуем да для локальной демонстрации; SQLite checkpointer отдельная будущая зависимость при restart requirement.
4. Принять Luna profile и cap $2 для предложенного development+heldout плана? Ключ отсутствует в текущем env, аккаунтная availability неизвестна. Без разрешения/credentials live остановлен, offline progress можно отдельно поручить.
5. Принять strict 48/48 small-suite gate (не population claim), manual обязательства отдельно? Если нет — согласовать до результатов, не задним числом.
6. Точное время сдачи, допустимый public комплект, GitHub owner/remote? Не выдумывать. Public publication и paid calls требуют отдельных полномочий.

## Handoff и stop
Лидер B: после real sequential reviews и supported terminal closeout упаковывает safe copies, сохраняет provenance/review hashes/actual prompt coverage, doc checks, отдельный docs commit B и отчёт. Только затем пользователь обсуждает proposed решения. Executor не запускается по этому плану автоматически. Будущая реализация завершается только при evidence всей матрицы; если public/credentials/owner rehearsal отсутствуют — отчёт partial с конкретным blocker, не «готово». Нынешний review не тестирование продукта.
<!-- END FILE: implementation-plan.md -->


<!-- BEGIN FILE: production-considerations.md -->
# Production considerations — проект

Proposed 2026-11-07; приложение ещё не создано, **не production-ready**. «В задании» ниже означает план, не выполненное свойство.

| Тема | План для компактного задания | До production дополнительно |
|---|---|---|
| Reliability | typed contracts, bounded retries/timeouts, no unsafe fallback, independent oracle, InMemorySaver с явной expiry после restart | durable checkpoints с безопасной сериализацией, migrations/backups/restore drills, failure recovery, HA/SLO/error budgets, provider outage strategy |
| Scalability | local read-only SQLite, один active request/UI session, small result/token caps | workload benchmark, queue/admission control, tenant quotas, connection pools; при concurrent writers рассмотреть PostgreSQL и новый dialect adapter/test suite; не переносить SQLite security policy вслепую |
| Monitoring/tracing | local complete versioned JSONL и screen expanders SQL/bindings/typed results/full trace, attempts/usage/cost/latency/error codes, synthetic public exports | searchable centralized storage, retention/access policy, dashboards/alerts p95 latency/errors/token spend, trace sampling не теряет audit/security events, on-call ownership |
| Security/privacy | loopback only, synthetic data, no keys in logs/repo, mode=ro+authorizer/allowlists+limits, process SQL watchdog, ingress/output checks | authentication/authorization/row-level access, tenant isolation, secret manager/rotation, dependency supply-chain audit, privacy/legal review, encrypted data/checkpoints, sandbox resource isolation, threat model/pentest |
| Deployment | reproducible Python+dependency lock/version receipt, clean clone instructions, local config presence checks | container/hardened runtime, CI/CD signed artifacts, rollout/rollback/migration gates, TLS/network policies, infra access controls, production cost governance |

Read-only ≠ semantic correctness; JSON schema ≠ correct SQL; trace completeness ≠ permission/publication; store=False ≠ zero retention. Progress handler cooperative, hard worker kill/memory enforcement должно быть отдельно реализовано/измерено. Отсутствие authentication приемлемо только loopback synthetic demo; не публиковать UI как доступный всем сервис. LangSmith optional future alternative после retention/billing/privacy review, не обязательная зависимость.

Будущая проверка: owner объясняет каждый tradeoff и показывает planned vs actual evidence; failed production feature не маскируется в assignment readiness. Revision triggers: реальные персональные данные, remote multi-user access, запись в DB, concurrent workloads, durable resume/recovery или новый provider/SQL dialect. Тогда нужен новый ADR/threat model, не механическое увеличение лимитов. См. [архитектуру](../../plans/architecture-proposal.md), [тесты](../../plans/test-plan.md).

Iteration2 уточнение: bounded SQL/bindings/input byte gates и oversized-value tests W1–W3 не доказывают hard memory isolation. SQLite может выделить память до fetch/progress handler; в local synthetic demo это явно residual risk. До remote/untrusted production требуется OS worker memory/resource policy и реальная adversarial проверка; новый dependency/parser/tokenizer в B не выбран.
<!-- END FILE: production-considerations.md -->


<!-- BEGIN FILE: requirements-test-matrix.md -->
# Требования → будущие доказательства

Proposed test mapping, 2026-11-07. Ни одна строка R не закрывается этим design review. Источник: принятая матрица (PDF/явные указания; безопасный [снимок](../../chat/requirements.md)); U-07 ранее verified, U-08 процедура proposed. Фактические будущие результаты сохранять с tested commit SHA, versions и failures; пути ниже ещё не существуют. Точные fixtures/scenarios раскрыты в [test-plan](../../plans/test-plan.md).

| ID / обязательство | Сценарий, данные/предусловие | Точный expected и pass/fail | Уровень | Будущий evidence |
|---|---|---|---|---|
| R-01 SQL Students/Teachers/Courses, имена | F1; попытка пустого имени/duplicate PK | 4 студента/2 преподавателя/3 курса; два Alex сохранены отдельно; пустое имя и duplicate PK rejected; иначе fail | DB integration + schema review | artifacts/tests/db/R01.json |
| R-02 offerings/семестры/enrollments/grades | F1; orphan offering/enrollment, duplicate(1,O1), grade101 | 5 offerings/8 enrollments, связи точные; нарушения rejected; NULL accepted; S9 retake80.00 | DB integration | artifacts/tests/db/R02.json |
| R-03 LangGraph NL→SQL→execution→answer | live S6, настоящий provider/DB/graph | «S1 C1 Kim student2»→O1/O5→80.00, полный graph trace, не mock | live NL + E2E | artifacts/e2e/R03/ |
| R-04 aggregate/JOIN/4 filters/multistep | S1–S14 и M1 F1/F2, D1–D3/V1 | все oracle table совпадают; M1 95.00→{95,80,50} при mutation; ни один filter не пропущен | DB + mocked graph + live NL | artifacts/tests/coverage/R04.json |
| R-05 schema-agnostic/modular | L1 library descriptor/DB swap | counts1/1; all-returned0/0; core hash неизменен; Library result adapter counts1/1 без grade scaling; нет university identifiers в core; иначе fail | code review + DB + live/E2E | artifacts/tests/portability/L1/ |
| R-06 полная трасса | T1/UI1 success M1, C1/resume и injected EI1–EI3 | input→nodes→SQL→DB typed results→answer/error, единый run, попытки/seq, отсутствие secrets; экран раскрывает SQL/bindings/DB rows/full same-run trace; opaque ID/missing link fail | integration + manual trace walkthrough | examples/traces/R06/ |
| R-07 ошибки/пустота/противоречия/ambiguity | S10,C1–C4,E1–E7,F3; injected EI1–EI3 отдельно; live N1–N4 | точные error codes/NULL/resume, bounded retries; EI provenance, N1–N4 no-data outcomes; unexpected provider errors fail live; plausible wrong SELECT limitation stated | unit + DB + graph + E2E | artifacts/tests/negative/R07.json |
| R-08 SQL/JOIN, NL-SQL, E2E tests | offline suites + sealed live48 + manual full path | все mandatory offline+injected suites pass, separately48 real-model conversations pass; injections не заменяют NL | multi-level tests/review | artifacts/tests/R08-summary.json |
| R-09 чистые модули DB/agent/prompts/tracing | будущий src tree и M1 walkthrough | UI без SQL; core без table names; DB/LLM adapters заменяемы; prompts versioned; explicit imports review | code review | artifacts/reviews/R09.md |
| R-10 production объяснение | production-considerations + owner discussion | все 5 тем reliability/scaling/observability/security/deploy, реализовано/будущее разделены; нельзя production-ready | document/manual | artifacts/reviews/R10.md |
| R-11 SQL schema/seed delivery | clean clone tested SHA | schema+seed присутствуют, создают F1 и constraints, no private data; отсутствие любого fail | actual DB + public checklist | artifacts/delivery/R11.md |
| R-12 LangGraph code/tests delivery | clean clone no local caches | code компилируется, offline suites execute, mandatory tests pass, public files доступны | integration/build + public | artifacts/delivery/R12.md |
| R-13 decisions с обоснованием | ADR003+ и будущие revisions | каждый значимый выбор context/options/rationale/consequences/verification, proposed/accepted различены; public index complete | document review + public | artifacts/reviews/R13.md |
| R-14 примеры/results/traces | S6/M1/C1/E1 и tested SHA | каждый example input→exact output→same-run trace, synthetic/redacted; нет fabricated runs | E2E + artifact review/public | examples/README.md |
| R-15 публичный repo полный комплект | отдельное разрешение remote/push, tested SHA | unauthenticated URL/raw access, remote SHA=tested SHA, все R11–14 paths; local commit недостаточен | public/manual | artifacts/delivery/public-check.md |
| R-16 показать/объяснить/защитить | owner сам выполняет M1,C1 и debugging E1 | прогноз oracle и объяснение каждого перехода/альтернативы, выявленные gaps исправлены; agent speech не pass | observed rehearsal | artifacts/defense/rehearsal.md |
| R-17 небольшой работающий/debuggable результат | clean clone + простой экран + сценарии | success/clarification/failure/second schema воспроизводятся; UI1 раскрывает SQL/данные/полные traces/attempts; owner объясняет без агента, scope без лишних сервисов | E2E + manual | artifacts/delivery/scope-check.md |
| U-01 фактические prompts | leader+каждый реальный child и будущие app prompts | индекс actual vs template/read context; hashes/redactions/cutoff/omissions, app prompts при создании; неполную историю не назвать полной | provenance/manual | docs/ai/README.md; artifacts/provenance/coverage.json |
| U-02 срок/дата демонстрации | owner подтверждает точный час и timezone | delivery timestamp до согласованного срока; дата требования 7/8 ноября2026, точный час open; без него не verified | manual timeline | artifacts/delivery/timeline.md |
| U-03 OMX, одна среда на этап | B native lifecycle receipts, будущие handoffs | verified sequential roles/terminal active:false без execution handoff; один canonical workspace/owner, не роль по prompt label | runtime evidence review | docs/reports/H-006-architecture-review.md |
| U-04 все решения в repo | ADR index + feature decision audit | все significant choices включая rejected alternatives доступны, ADR001/002/history сохранены; missing decision fail | document review | artifacts/reviews/U04.md |
| U-05 память/владение | before/after hashes vault и snapshots; links repo-owned docs | vault read-only в B, четыре allowlisted snapshots не превращены в оригиналы, OMX wiki links не duplicate reports | provenance/hash review | docs/operations/H-006-B2-preservation.json |
| U-06 commit/push policy/checkpoints | A verified, B separate docs commit после closeout | A неизменен, explicit staged safe paths, B SHA recorded; saved/committed/pushed/public разделены; no remote/push B | Git/document evidence | docs/operations/H-006-B2-commit-receipt.json |
| U-07 подготовительный переход | исторические CHAT004→005 и H002 evidence | ранее verified факт перехода сохранён с атрибуцией; не запускать повтор и не заявлять новым результатом B | historical source review | artifacts/reviews/U07-history.md |
| U-08 порядок понимания результата | будущий chat review + owner example/counterexample/independent explanation | протокол отмечает observed understanding/gaps для schema/graph/SQL/tracing/evals/portability, не одно «понятно» | manual/chat | artifacts/defense/understanding.md |

Состояние сейчас: только documentary fixtures/expected и план evidence. Runtime lifecycle/историческое сохранение проверяет лидер отдельно; app tests, live eval, public access и owner rehearsal **not-run**. Отсутствие credentials блокирует будущий live, не документальный B.
<!-- END FILE: requirements-test-matrix.md -->


<!-- BEGIN FILE: test-plan.md -->
# План проверок и документальные fixtures — proposed

Ни один тест приложения не выполнен в B. Ниже независимые oracle и будущие команды/evidence, не исполняемый seed/SQL/test code. Все имена синтетические. Точные правила — [архитектура](../../plans/architecture-proposal.md), [контракты](../../plans/contracts.md). Любой обязательный fail блокирует приёмку независимо от процента live eval.

## F1: минимальные таблицы
Students: (1,Alex), (2,Bea), (3,Alex), (4,Dana). Teachers: (10,Kim), (11,Lee). Courses: (C1,DB), (C2,AI), (C3,Ethics). Semesters: S1=(2026-01-01,2026-06-30), S2=(2026-07-01,2026-12-31). Здесь C1..3 — документальные aliases integer IDs 1..3; SQL использует integers, descriptor/UI могут отображать codes C1..3.

| Offering | Course | Teacher | Semester | Section |
|---|---|---|---|---|
| O1=1 | C1=1 |10|S1|A|
| O2=2 | C2=2 |11|S1|A|
| O3=3 | C1=1 |11|S2|A|
| O4=4 | C3=3 |10|S1|A|
| O5=5 | C1=1 |10|S1|B|

| Student | Offering | Grade |
|---|---|---|
|1|O1|90|
|2|O1|60|
|3|O1|NULL|
|1|O2|100|
|1|O3|70|
|2|O3|80|
|4|O4|NULL|
|2|O5|100|

Числа вычисляются вручную из этих восьми строк, независимо от generated SQL. Оценки хранить как integer hundredths: 90→9000; sum/count oracle ведёт в hundredths, наружу decimal. Decimal final round half-up 2 places; сравнение unrounded rationals до display; display exact string, численный oracle tolerance <=0.005 только для внешнего округления, counts/IDs точные. Order-independent set comparison если order не requested; ties order by stable ID. NULL, zero, absent row различны.

F2 tie mutation: F1 + Enrollment(3,O2,50). F3 inconsistent: внешне повреждённая DB содержит duplicate(1,O1) или grade101/orphan student99, создаётся только отдельной будущей fault fixture, normal constraints её не допускают. F4 all-null: scope C3/S1. F5 overflow: 101 synthetic distinct readers/rows; aggregate oracle101, displayed100 with truncated=true; dependency cohort101 must RESULT_TOO_LARGE, не silent100.

## SQL/semantics integration scenarios (реальная SQLite, не mock)
Для каждого S* будущий evidence `artifacts/tests/db/<ID>.json`: fixture hash, query, actual typed rows, independent expected, diff, DB version. Pass = точное множество/числа/NULL/labels ниже; любые лишние/утраченные строки fail.

| ID | Вопрос/предусловие | Точный oracle |
|---|---|---|
| S1 | Все enrollments F1 | enrollment_count8; graded6; distinct_students4; sum500; avg=500/6=83.33 |
| S2 | semester=S1 | rows6; graded4; sum350; avg87.50; distinct_students4 |
| S3 | course=C1, все семестры | enrollments6; graded5; sum400; avg80.00; distinct_students3 |
| S4 | teacher=10, все | enrollments5; graded3; sum250; avg83.33; distinct_students4 |
| S5 | student=1, все | enrollments3; graded3; sum260; avg86.67 |
| S6 | Все четыре filters: S1,C1,teacher10,student2 | O1=60,O5=100; count2; avg80.00 |
| S7 | JOIN Students→Enrollments→Offerings→Courses→Teachers→Semesters, S1/C1 | (1,Alex,O1,DB,Kim,S1,90),(2,Bea,O1,DB,Kim,S1,60),(3,Alex,O1,DB,Kim,S1,NULL),(2,Bea,O5,DB,Kim,S1,100); ровно4 |
| S8 | Course means S1, unequal groups | C1:250/3=83.33; C2:100/1=100.00; C3:null; overall350/4=87.50, НЕ(83.333+100)/2=91.67 |
| S9 | Retakes/student1/courseC1 all semesters | O1=90,O3=70; avg80.00, не70; explicit S2→70.00 |
| S10 | F4 C3/S1 | enrollment1,graded0,avg null; raw[0,0,1]→no_grades, не0. Empty C2/S2→raw[0,0,0]→0 enrollments/0graded/null avg,no_rows; real grade0→raw[0,1,1]→"0.00",empty_reason=null |
| S11 | F2 top course mean S1 | C1=250/3,C2=150/2=75 → C1 only. Отдельная tie fixture: заменить F2 added grade50→66.666 нельзя (2 decimal rule); вместо этого F1 O2 grade→83.33 НЕ tie с83.333… |
| S12 | Exact tie fixture F1: O1/student2 grade60→80, O5/student2 grade100→100, O1/student1 grade90→90; O2/student1 grade100→90 | C1=(90+80+100)/3=90, C2=90; top set{C1,C2}, C3 excluded |
| S13 | Join duplication trap: cohort C1/S1 students1,2,3; average всех их S1 enrollments | unique IDs{1,2,3}; grades90,60,100,100 sum350/count4=87.50; student2 не удваивается из-за двух offerings. Наивный JOIN по enrollments даёт sum510/count6=85.00 — fail |
| S14 | F5 cap vs aggregate | exact count101; simple listing100+truncated; aggregate counts over all101; dependency oversized→RESULT_TOO_LARGE |

## Multi-step M1 и sensitivity
F1 question из архитектуры: top course in S1=C2 average100, cohort={1}, student's all-S1 mean=(90+100)/2=95.00; final row(student1,Alex,95.00), scope top course C2/S1 and all courses S1. Evidence `artifacts/tests/graph/M1.json`: step outputs, references, call count, trace. F2 mutation top=C1 (83.33 vs75); cohort={1,2,3}; final{1:95.00,2:80.00,3:50.00}. Step2 must actually depend on returned C1; captured SQL parameters/IDs must change. S12 tie top{C1,C2} yields union cohort{1,2,3}; final{1:90.00,2:90.00,3:null}; student3 has enrollment but no grade → no_grades annotation. Mocked graph tests control proposals but real DB computes; отдельный live M1 проверяет NL planning. Фиксированное число узлов не pass criterion.

## Contract/unit и controlled faults
Будущая команда `python -m pytest tests/unit -q`; evidence `artifacts/tests/unit/<ID>.json`. Файлы/команда планируются, сейчас отсутствуют.

| ID | Fixture/injection | Pass / fail |
|---|---|---|
| C1 | F1 question «средняя Alex» | clarification options exactly student1/3; 0 SQL executions до выбора; select1→86.67, select3→null no_grades; никакого silent first |
| C2 | resume wrong session / stale checkpoint / changed descriptor | RESUME_FORBIDDEN / STALE_RESUME / STALE_RESUME; 0 extra LLM/SQL; чужие данные не раскрыты |
| C3 | identical accepted resume repeated; same request ID changed payload | same response, unchanged call counters / REPLAY_CONFLICT; no duplicate execution |
| C4 | interrupt reentry, process restart, third clarification | no repeated paid work before interrupt; RESUME_EXPIRED on restart; CLARIFICATION_LIMIT on third request for pause |
| C5 | valid/invalid examples из contracts | valid parsed; each invalid rejected before DB/provider; mutually exclusive response variants enforced |
| E1 | proposal references unknown column; repair valid | exactly2 SQL proposal attempts (only valid query executed if compile fails before execution); one repair; answer equals oracle; two bad proposals→SQL_INVALID |
| E2 | transient provider timeout then success; always timeout | 2 provider calls maximum, SDK retries0; oracle / PROVIDER_UNAVAILABLE; 15s per call, bounded global deadline |
| E3 | refusal/incomplete/malformed structured output | PROVIDER_REFUSAL/PROVIDER_INCOMPLETE/PROVIDER_INVALID_OUTPUT; 0 SQL, no retry |
| E4 | DB missing, locked >0.5s, expensive recursive SELECT | DB_UNAVAILABLE / DB_UNAVAILABLE / SQL_TIMEOUT; worker stopped by3s, terminal no answer |
| E5 | F3 corruption; unexpected contradictory aggregate graded>count | DATA_INCONSISTENT before final answer; precise invariant in trace, no invented correction |
| E6 | reach5 provider calls,4 SQL attempts,60s active or trace/result limits | next operation refused BUDGET_EXCEEDED (result cap RESULT_TOO_LARGE); no counter reset on resume; single terminal |
| E7 | trace sink unavailable before SQL / fails during run | TRACE_UNAVAILABLE, no untraced success claimed; UI diagnostic; failed run cannot satisfy R06 |
| T1 | successful M1 and failed E1 | ordered input,node starts,LLM attempts,SQL validation/attempt,DB columns+rows,answer/error,run_end; one run_id, unique seq/event IDs; no keys/headers/raw private payload |
| T2 | prompt injection question or malicious value in DB name | treated as data; attempts to write/exfiltrate denied by validator/authorizer; no new endpoint/tool; read-only not claimed to prevent plausible wrong SELECT |

Safety real DB integration `tests/integration/test_sql_policy`: DML, DDL, ATTACH/DETACH, PRAGMA, load_extension, sqlite_master unauthorized read, multi-statements, CTE-wrapped writes, forbidden functions/subqueries/comments variants all UNSAFE_SQL; DB before/after file hash unchanged. Allowed aggregate/CTE must still pass S*. Expensive allowed SELECT terminated within3s; safety pass does not count as semantic pass. Tests pin SQLite error/authorizer behavior instead of matching first keyword.

## L1: concrete second schema
Readers(1,Ada),(2,Bob); Books(10,X),(11,Y); Loans(1,1,10,false),(2,1,11,true),(3,2,10,false). «Сколько невозвращённых книг у каждого читателя?» → {(1,Ada,1),(2,Bob,1)}. Zero-return variant all returned=true → each reader0 if question «у каждого» (LEFT JOIN, no accidental exclusion); global open count0. Change only descriptor/domain adapter+DB; core code hash unchanged. Separate real DB integration, mocked graph, live NL and full UI E2E evidence in `artifacts/tests/portability/L1/`; all four required, not merely prompt text swap. No cross-dialect claim.

## Уровни, команды и будущие доказательства
- Unit: pure contracts, scope/name resolution, state transitions/budgets, formatter. `python -m pytest tests/unit -q`.
- DB integration: actual SQLite fixture/constraints/authorizer/queries, S1–S14, safety. `python -m pytest tests/integration -q`.
- Mocked orchestration: actual compiled LangGraph + scripted provider + real DB, M1/C1–C4/E1–E7/T1. `python -m pytest tests/graph -q`. Не NL→SQL quality evidence.
- Live NL→SQL: real configured model/SDK, requests, valid SQL and typed oracle semantic comparison. `python -m universitydb.eval --suite heldout --profile approved` (будущий интерфейс; exact implementation may adjust with documented equivalent).
- Full E2E: actual Streamlit, graph, real DB, real model, trace; manual real-model success M1, ambiguity C1/resume и L1; EI1 injected failure display отдельно не live generation score. Screen renders question, answer, clarification choices, error, SQL/safe bindings, typed DB columns/rows и полный same-run trace/attempts через local expanders; opaque trace ID alone — fail. `python -m streamlit run src/universitydb/ui.py` planned.
- Static/build: future `python -m compileall src`, targeted lint/type checker selected in implementation lock; not claim nonexistent lint tooling today. Commands become final only after tools are selected; no dependencies installed in B.

## Proposed live eval gate, не прежний порог
24 development cases + **24 sealed held-out** cases, six categories ×4 each: aggregates/NULL, JOIN/four filters, dependent multi-step/ties, ambiguity/continuation, negative data-availability requests N1–N4 (ниже), second schema. Development separate IDs/wording/value mutations; held-out oracle frozen/hash before prompt tuning, custodian reviewer stores private until run. Synthetic cases only. Mandatory deterministic S/C/E/T/L/D/V/W/UI1 and injected EI tests all pass; every R requirement individually evidenced. Live gate proposed: each held-out case succeeds on **both** scheduled repetitions (48/48 semantic passes), all six categories present, zero unsafe executions/privacy failures; no retry-dropping or best-of selection. This is strict small-demo reliability check, not estimated population accuracy; repeated failures become defects, not tolerated percentage. Repeats catch nondeterminism without claiming statistical power. Owner may revise scope/budget explicitly, not lower gate after looking at failures.

Each case records attempted even timeout/refusal (unexpected refusal always fails live generation); first two runs count, provider retries included in their own runs. On prompt/model/data change: new version + whole heldout rerun; contaminated cases move to development, replace entire affected category with fresh independently reviewed cases. Log input/expected/actual, model requested+returned, provider request ID, date, parameters, seed if supported (no determinism promise), prompt/schema/data/lock hashes, usage/cost, all failures. Expected no-data outcome is success only for designated N1–N4 case; injected rejection не входит в live denominator.

Budget proposal: evaluation max48 heldout runs ×5calls =240 calls, <=2.88M input/0.48M output ($0.528 at Luna rates), development max24×2runs×5=240 calls additional <=$0.528; total upper token-rate estimate $1.056, propose hard approved cap **$2** allowing measured overhead, still stop when cap projected to exceed. Excludes taxes/account minimums and any different model; provider billed usage reconciled all calls. No permission or actual spending here. Check availability/rates before live; owner budget/model approval required. No hidden expensive fallback. 60k/10k conversation caps determine these conservative estimates.

## Documentary walkthroughs (не выполненные тесты)
Success S6: scope resolves S1/C1/teacher10/student2 → validated read-only JOIN → rows60,100 → sum160/count2→80.00 → matching trace/answer.
Clarification C1: two Alex candidates → checkpoint/cl1 → selectstudent1 with bound session → continuation chooses1 →260/3→86.67; old resume rejected; no pre-interrupt calls repeated.
Failure E1: unknown column proposal → compile diagnostic sanitized → one repair → if still invalid SQL_INVALID, terminal trace; no normal answer.
Schema swap L1: load library-v1 descriptor/hash → same graph produces allowed Loans join → open counts1/1 → same answer/trace envelopes. These are design reasoning, not application results.

## Delivery/manual/public/defense
Clean clone into separate temporary checkout after future publication authorization: documented install from lock without local secrets; run offline suites then approved live smoke with separately supplied key; evidence `artifacts/delivery/clean-clone.md` records SHA/platform/commands/exit codes. This future test does not authorize creating competing repo during B.
Manual real-model E2E record screenshots+полное раскрытое содержимое trace/SQL/DB+exact expected M1/C1/L1; отдельно injected EI1–EI3 with provenance. Один trace ID без доступного содержимого — fail. Public gate: explicit remote authorization, scrub secrets/private PDF/raw/.omx/DB caches, unauthenticated repo and raw file reads, remote SHA==tested SHA, complete schema/seed/code/tests/docs/prompts/examples/traces checklist. Evidence `artifacts/delivery/public-check.md`; local B commit is not R15.
Owner rehearsal without agent: explain schema/name ambiguity, 350/4 vs mean-of-means, dependent cohort, unsafe SQL vs wrong SELECT, trace debug, portability diff and production gaps; run changed input independently. Record observed predictions and corrections in `artifacts/defense/rehearsal.md`, not self-assessed understanding. Exact delivery hour still owner question, no automatic date-based pass.

## Iteration 2: точные проверки новых стыков

| ID | Данные/воздействие и уровень | Точный pass/fail / future evidence |
|---|---|---|
| D1 | Полный M1 PlanProposal из contracts, unit validate_plan | accepted без существующих results; cycle/missing alias mutations→PLAN_INVALID,0 downstream calls; artifacts/tests/unit/D1.json |
| D2 | M1 scripted provider+real DB, phases validate_plan/bind_results | unresolved refs проходят static; F1 top course2 materializes, cohort1, final95.00; F2 course1/cohort1,2,3/final95,80,50; результаты не угаданы заранее; artifacts/tests/graph/D2.json |
| D3 | completed result injected truncated/missing/type mismatch | RESULT_TOO_LARGE либо DEPENDENCY_INVALID/bind_results, next provider/SQL0; inspect_result early bad raw→RESULT_CONTRACT_INVALID; artifacts/tests/graph/D3.json |
| V1 | Полные S6/M1/tie/Library DBResult messages из contracts; unit adapter и real DB integration отдельно | S6 16000/2/100=80.00; tie 27000/3=9000/1→оба course IDs; library1/1 не scale100; unit/denom/grain mutations→RESULT_CONTRACT_INVALID; Z1/Z2/Z3 scalar raw components отдельно DB-Z и нормализация отдельно UNIT-Z (ниже); artifacts/tests/domain/V1.json |
| V2 | Корректные specs, SQL намеренно использует неверные но правдоподобные суммы | runtime может принять, independent oracle обязан fail; no claim of complete semantic validator; artifacts/tests/domain/V2.json |
| W1 | strict bindings example, duplicate/missing/extra/type malformed/101values | valid maps exactly to two bindings; malformed→PROVIDER_INVALID_OUTPUT,101→RESOURCE_LIMIT,0 DB executions; future SDK parse smoke separately; artifacts/tests/unit/W1.json |
| W2 | question2001chars, SQL8001bytes, binding2001bytes/total8193, one DB value8193bytes | INVALID_INPUT / RESOURCE_LIMIT / RESOURCE_LIMIT / RESULT_TOO_LARGE; boundary allowed sizes pass остальные gates; artifacts/tests/bounds/W2.json |
| W3 | encoded model input12001bytes, injected provider usage12001input tokens | byte overflow→RESOURCE_LIMIT before network; usage overflow→BUDGET_EXCEEDED after counted attempt/no next calls; no exact tokenizer/hard memory claim; artifacts/tests/bounds/W3.json |

### Две разные negative lanes
**Injected deterministic lane:** E1–E7 остаются обязательными contract/graph/DB tests. UI lane использует actual Streamlit/LangGraph/DB/trace, но явный test transport/provider fixture заменяет ответ/ошибку. Header screen и trace metadata `execution_profile="injected"`, `fault_case`, `injection_point`, `fixture_hash`, `real_provider_called=false`; поля в controlled test export, не new production wire inputs. Нельзя выбрать injected profile через обычный untrusted question; developer-only local test configuration, не remote feature. Expected E3 refusal/incomplete/malformed не требует угадать поведение API. Эти тесты offline, **0 paid calls**, не входят в24×2 live denominator.
- EI1: injected provider refusal→PROVIDER_REFUSAL; экран показывает ошибку и полный same-run input→nodes→attempt→error→run_end; SQL/DB панели явно «не выполнялись», не чужие старые rows.
- EI2: injected first malformed SQL proposal/repair valid S6→80.00; экран видит обе попытки, sanitised diagnostic, final SQL+bindings и DB16000/2/2. Profile injected, не live generation pass.
- EI3: injected incomplete либо transport timeout twice→PROVIDER_INCOMPLETE либо PROVIDER_UNAVAILABLE; exact number attempts1/2, no fabricated answer, terminal trace. Контролируемая ошибка DB отдельно E4 и видна тому же screen view.

**Real-model generation lane:** requested/returned model/usage recorded, no injection/mocked provider. Шесть categories по4cases: aggregates/NULL; JOIN/four filters; dependent/ties; ambiguity+accepted continuation; negative data-availability N1–N4; Library schema. Каждый case запускается2раза; denominator **48 conversations**, не48 отдельных calls. Ambiguity case включает response clarification и recorded scripted valid user selection, затем реальный model SQL; иначе incomplete conversation fail. Все48 outcomes обязательны, mandatory offline/injected tests отдельно pass.
N1 «Средняя C2 в S2?» F1→raw[0,0,0]→enrollment0,graded0,average=null,no_rows (Z1). N2 «Средняя C3 в S1?»→raw[0,0,1]→enrollment1,graded0,average=null,no_grades (Z2). N3 «Средняя student3 по всем семестрам?»→raw[0,0,1]→enrollment1,graded0,average=null,no_grades (тот же Z2 outcome, scope student3). N4 «Число записей на C3 у teacher11?»→count0 (count-only нормальный numeric0, exact empty_reason=null для count result). Точное поле/текст может выражаться иначе только text natural-language, typed values/NULL/reason обязательны. Эти cases проверяют отсутствие invented grades/results, **не искусственную SQL/provider failure**. Refusal/timeout/invalidSQL, не исправленный в лимите, на любом из48 — failed attempt, не исключить из denominator и не заменить best-of. Provider refusal на N1–N4 не допустимый альтернативный outcome.

24 development и24heldout сохраняются, N1–N4 здесь category prototypes: heldout reviewer до freeze формирует4новых синтетических value/wording mutations с теми же independently verified outcome classes, не копирует раскрытые F1 questions. Точная frozen fixture/wording/expected записывается до live, не определяется по model result. Набор currently **ещё не создан**, examples — template criteria, не «sealed suite уже существует». All generations/repeats/cost counted; unchanged conservative ceiling480calls/5.76M input/.96M output=$1.056 при cited Luna rates, proposed $2cap; injections добавляют0calls. Real UI smoke outside48 требует отдельного approved remaining cap, либо проводится на тех же logged eval conversations; не неучтённый paid tail.

### UI1: принятие простого экрана (обязательное, не новая платформа)
На локальном экране доступны вопрос/answer или error/clarification и expanders **SQL с безопасными bindings**, **DB typed columns/rows/truncation**, **полная последовательность событий того же run включая все attempts, ошибки и resume**. Seq/run_id/trace_id совпадают с JSONL. Можно раскрыть каждую попытку и результат каждого step, а не только final. Payloads synthetic, export redaction по contracts; не публиковать secret/raw exceptions.
Success S6/M1: из UI найти SQL,16000/2/2 либо M1 промежуточные rows, final80.00/95.00 и run_end; несовпадение rows/run или недоступный trace — fail. Clarification C1: до выбора options1/3, показан pause trace и «SQL ещё не выполнялся»; после resume видны исходный input, clarification, resume, SQL/rows/86.67 одного run. EI2 error+repair: обе попытки доступны, не скрывать первую; terminal EI1/EI3 показывает full error chain, no answer/no DB claims. Оpaque ID без доступного view, старые rows другого run, исчезнувшие попытки при resume — fail. Evidence `artifacts/e2e/UI1/` screenshots opened panels + same-run exported trace + profile/fault provenance. Это будущий real UI test; B только спецификация.


## B2-R1: раздельная будущая проверка raw SQL и adapter
- **DB-Z (actual SQLite integration, future):** на F1 scalar C2/S2 SQL с aggregate-level `COALESCE(SUM(grade_units),0)`/COUNT(grade_units)/COUNT(*) возвращает integer components[0,0,0]; C3/S1 и student3/all возвращают[0,0,1]. Отдельная минимальная synthetic fixture с одним enrollment grade_units=0 возвращает[0,1,1]. Проверить именно реальные raw typed columns и row_count1 до adapter. NULL вместо integer0 в sum_units — fail, даже если formatter умеет скрыть дефект. Evidence `artifacts/tests/db/DB-Z.json`: DB version, fixture/query hash, actual components/types, независимые expected. Это дополнение S10/N1–N3/V1.
- **UNIT-Z (pure domain adapter unit, future):** подать три полных DBResult Z1/Z2/Z3 из contracts без DB/model; exact normalized Answer равен examples: null/no_rows;null/no_grades;"0.00"/null соответственно, counts0/0;0/1;1/1. Дополнительная invalid mutation Z1 sum_units=null → RESULT_CONTRACT_INVALID, не автокоррекция. Evidence `artifacts/tests/domain/UNIT-Z.json`.
- Pass требует **обоих** направлений; unit normalization не доказывает raw SQLite outputs, DB output не доказывает formatter/empty_reason. В B выполнены только документальное согласование/JSON syntax checks; DB-Z/UNIT-Z **not-run**. Изолированные reviewer aggregate probes остаются evidence reviewers, не product tests Planner.
<!-- END FILE: test-plan.md -->
