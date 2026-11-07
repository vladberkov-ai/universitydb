# План проверок и документальные fixtures — proposed

Ни один тест приложения не выполнен в B. Ниже независимые oracle и будущие команды/evidence, не исполняемый seed/SQL/test code. Все имена синтетические. Точные правила — [архитектура](architecture-proposal.md), [контракты](contracts.md). Любой обязательный fail блокирует приёмку независимо от процента live eval.

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
