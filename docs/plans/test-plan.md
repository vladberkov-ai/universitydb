# Inspection plan and documentary fixtures - proposed

No application test is executed in B. Below are independent oracle and future commands/evidence, non-executable seed/SQL/test code. All names are synthetic. The exact rules are [architecture](architecture-proposal.md), [contracts](contracts.md). Any mandatory fail blocks acceptance regardless of the live eval percentage.

## F1: minimal tables
Students: (1,Alex), (2,Bea), (3,Alex), (4,Dana). Teachers: (10,Kim), (11,Lee). Courses: (C1,DB), (C2,AI), (C3,Ethics). Semesters: S1=(2026-01-01,2026-06-30), S2=(2026-07-01,2026-12-31). Here C1..3 are documentary aliases integer IDs 1..3; SQL uses integers, descriptor/UI can display codes C1..3.

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

The numbers are calculated manually from these eight lines, regardless of the generated SQL. Store estimates as integer hundredths: 90→9000; sum/count oracle leads to hundredths, out to decimal. Decimal final round half-up 2 places; comparison of unrounded rationals to display; display exact string, numeric oracle tolerance <=0.005 for outer rounding only, counts/IDs exact. Order-independent set comparison if order is not requested; ties order by stable ID. NULL, zero, absent row are different.

F2 tie mutation: F1 + Enrollment(3,O2,50). F3 inconsistent: externally damaged DB contains duplicate(1,O1) or grade101/orphan student99, only a separate future fault fixture is created, normal constraints do not allow it. F4 all-null: scope C3/S1. F5 overflow: 101 synthetic distinct readers/rows; aggregate oracle101, displayed100 with truncated=true; dependency cohort101 must RESULT_TOO_LARGE, not silent100.

## SQL/semantics integration scenarios (real SQLite, not mock)
For each S* future evidence `artifacts/tests/db/<ID>.json`: fixture hash, query, actual typed rows, independent expected, diff, DB version. Pass = exact set/numbers/NULL/labels below; any extra/lost lines fail.

| ID | Question/precondition | Accurate oracle |
|---|---|---|
| S1 | Allenrollments F1 | enrollment_count8; graded6; distinct_students4; sum500; avg=500/6=83.33 |
| S2 | semester=S1 | rows6; graded4; sum350; avg87.50; distinct_students4 |
| S3 | course=C1, all semesters | enrollments6; graded5; sum400; avg80.00; distinct_students3 |
| S4 | teacher=10, All| enrollments5; graded3; sum250; avg83.33; distinct_students4 |
| S5 | student=1, All| enrollments3; graded3; sum260; avg86.67 |
| S6 | All four filters: S1,C1,teacher10,student2 | O1=60,O5=100; count2; avg80.00 |
| S7 | JOIN Students→Enrollments→Offerings→Courses→Teachers→Semesters, S1/C1 | (1,Alex,O1,DB,Kim,S1,90),(2,Bea,O1,DB,Kim,S1,60),(3,Alex,O1,DB,Kim,S1,NULL),(2,Bea,O5,DB,Kim,S1,100); smooth4 |
| S8 | Course means S1, unequal groups | C1:250/3=83.33; C2:100/1=100.00; C3:null; overall350/4=87.50, NOT(83.333+100)/2=91.67 |
| S9 | Retakes/student1/courseC1 all semesters | O1=90,O3=70; avg80.00, Not70; explicit S2→70.00 |
| S10 | F4 C3/S1 | enrollment1,graded0,avg null; raw[0,0,1]→no_grades, Not0. Empty C2/S2→raw[0,0,0]→0 enrollments/0graded/null avg,no_rows; real grade0→raw[0,1,1]→"0.00",empty_reason=null |
| S11 | F2 top course mean S1 | C1=250/3,C2=150/2=75 → C1 only. Separate tie fixture: you cannot replace F2 added grade50→66.666 (2 decimal rule); instead F1 O2 grade→83.33 NOT tie with83.333… |
| S12 | Exact tie fixture F1: O1/student2 grade60→80, O5/student2 grade100→100, O1/student1 grade90→90; O2/student1 grade100→90 | C1=(90+80+100)/3=90, C2=90; top set{C1,C2}, C3 excluded |
| S13 | Join duplication trap: cohort C1/S1 students1,2,3; average of all their S1 enrollments | unique IDs{1,2,3}; grades90,60,100,100 sum350/count4=87.50; student2 does not double due to two offerings. A naive JOIN on enrollments gives sum510/count6=85.00 - fail |
| S14 | F5 cap vs aggregate | exact count101; simple listing100+truncated; aggregate counts over all101; dependency oversized→RESULT_TOO_LARGE |

## Multi-step M1 Andsensitivity
F1 question from architecture:top course in S1=C2 average100, cohort={1}, student's all-S1 mean=(90+100)/2=95.00; final row(student1,Alex,95.00), scope top course C2/S1 and all courses S1. Evidence `artifacts/tests/graph/M1.json`: step outputs, references, call count, trace. F2 mutation top=C1 (83.33 vs75); cohort={1,2,3}; final{1:95.00,2:80.00,3:50.00}. Step2 must actually depend on returned C1; captured SQL parameters/IDs must change. S12 tie top{C1,C2} yields union cohort{1,2,3}; final{1:90.00,2:90.00,3:null}; student3 has enrollment but no grade → no_grades annotation. Mocked graph tests control proposals but real DB computes; separatelive M1 checksNL planning. No fixed number of nodespass criterion.

## Contract/unit Andcontrolled faults
Future team `python -m pytest tests/unit -q`; evidence `artifacts/tests/unit/<ID>.json`. Files/command planned, currently missing.

| ID | Fixture/injection | Pass / fail |
|---|---|---|
| C1 | F1 question "average Alex" | clarification options exactly student1/3; 0 SQL executions before selection; select1→86.67, select3→null no_grades; no silent first |
| C2 | resume wrong session / stale checkpoint / changed descriptor | RESUME_FORBIDDEN / STALE_RESUME / STALE_RESUME; 0 extra LLM/SQL; other people's data is not disclosed |
| C3 | identical accepted resume repeated; same request ID changed payload | same response, unchanged call counters / REPLAY_CONFLICT; no duplicate execution |
| C4 | interrupt reentry, process restart, third clarification | no repeated paid work before interrupt; RESUME_EXPIRED on restart; CLARIFICATION_LIMIT on third request for pause |
| C5 | valid/invalid examples fromcontracts | valid parsed; each invalid rejected before DB/provider; mutually exclusive response variants enforced |
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
Readers(1,Ada),(2,Bob); Books(10,X),(11,Y); Loans(1,1,10,false),(2,1,11,true),(3,2,10,false). «How many unreturned books does each reader have?→ {(1,Ada,1),(2,Bob,1)}. Zero-return variant all returned=true → each reader0 if question «everyone"(LEFT JOIN, no accidental exclusion); global open count0. Change only descriptor/domain adapter+DB; core code hash unchanged. Separate real DB integration, mocked graph, live NL and full UI E2E evidence in `artifacts/tests/portability/L1/`; all four required, not merely prompt text swap. No cross-dialect claim.

## Levels, commands and future proofs
- Unit: pure contracts, scope/name resolution, state transitions/budgets, formatter. `python -m pytest tests/unit -q`.
- DB integration: actual SQLite fixture/constraints/authorizer/queries, S1–S14, safety. `python -m pytest tests/integration -q`.
- Mocked orchestration: actual compiled LangGraph + scripted provider + real DB, M1/C1–C4/E1–E7/T1. `python -m pytest tests/graph -q`. NotNL→SQL quality evidence.
- Live NL→SQL: real configured model/SDK, requests, valid SQL and typed oracle semantic comparison. `python -m universitydb.eval --suite heldout --profile approved` (future interface;exact implementation may adjust with documented equivalent).
- Full E2E: actual Streamlit, graph, real DB, real model, trace; manual real-model success M1, ambiguity C1/resume AndL1; EI1 injected failure display not separatelylive generation score. Screen renders question, answer, clarification choices, error, SQL/safe bindings, typed DB columns/rows and fullsame-run trace/attempts throughlocal expanders; opaque trace ID alone — fail. `python -m streamlit run src/universitydb/ui.py` planned.
- Static/build: future `python -m compileall src`, targeted lint/type checker selected in implementation lock; not claim nonexistent lint tooling today. Commands become final only after tools are selected; no dependencies installed in B.

## Proposed live eval gate, not the same threshold
24 development cases + **24 sealed held-out** cases, six categories ×4 each: aggregates/NULL, JOIN/four filters, dependent multi-step/ties, ambiguity/continuation, negative data-availability requests N1–N4 (below), second schema. Development separate IDs/wording/value mutations; held-out oracle frozen/hash before prompt tuning, custodian reviewer stores private until run. Synthetic cases only. Mandatory deterministic S/C/E/T/L/D/V/W/UI1 and injected EI tests all pass; every R requirement individually evidenced. Live gate proposed: each held-out case succeeds on **both** scheduled repetitions (48/48 semantic passes), all six categories present, zero unsafe executions/privacy failures; no retry-dropping or best-of selection. This is strict small-demo reliability check, not estimated population accuracy; repeated failures become defects, not tolerated percentage. Repeats catch nondeterminism without claiming statistical power. Owner may revise scope/budget explicitly, not lower gate after looking at failures.

Each case records attempted even timeout/refusal (unexpected refusal always fails live generation); first two runs count, provider retries included in their own runs. On prompt/model/data change: new version + whole heldout rerun; contaminated cases move to development, replace entire affected category with fresh independently reviewed cases. Log input/expected/actual, model requested+returned, provider request ID, date, parameters, seed if supported (no determinism promise), prompt/schema/data/lock hashes, usage/cost, all failures. Expected no-data outcome is success only for designated N1–N4 case; injected rejection not included inlive denominator.

Budget proposal: evaluation max48 heldout runs ×5calls =240 calls, <=2.88M input/0.48M output ($0.528 at Luna rates), development max24×2runs×5=240 calls additional <=$0.528; total upper token-rate estimate $1.056, propose hard approved cap **$2** allowing measured overhead, still stop when cap projected to exceed. Excludes taxes/account minimums and any different model; provider billed usage reconciled all calls. No permission or actual spending here. Check availability/rates before live; owner budget/model approval required. No hidden expensive fallback. 60k/10k conversation caps determine these conservative estimates.

## Documentary walkthroughs (not completed tests)
Success S6: scope resolves S1/C1/teacher10/student2 → validated read-only JOIN → rows60,100 → sum160/count2→80.00 → matching trace/answer.
Clarification C1: two Alex candidates → checkpoint/cl1 → selectstudent1 with bound session → continuation chooses1 →260/3→86.67; old resume rejected; no pre-interrupt calls repeated.
Failure E1: unknown column proposal → compile diagnostic sanitized → one repair → if still invalid SQL_INVALID, terminal trace; no normal answer.
Schema swap L1: load library-v1 descriptor/hash → same graph produces allowed Loans join → open counts1/1 → same answer/trace envelopes. These are design reasoning, not application results.

## Delivery/manual/public/defense
Clean clone into separate temporary checkout after future publication authorization: documented install from lock without local secrets; run offline suites then approved live smoke with separately supplied key; evidence `artifacts/delivery/clean-clone.md` records SHA/platform/commands/exit codes. This future test does not authorize creating competing repo during B.
Manual real-model E2E record screenshots+full disclosed content trace/SQL/DB+exact expected M1/C1/L1; Separately injected EI1–EI3 with provenance. Odin trace ID without available content — fail. Public gate: explicit remote authorization, scrub secrets/private PDF/raw/.omx/DB caches, unauthenticated repo and raw file reads, remote SHA==tested SHA, complete schema/seed/code/tests/docs/prompts/examples/traces checklist. Records `artifacts/delivery/public-check.md`; local B commit is not R15.
Owner rehearsal without agent: explain schema/name ambiguity, 350/4 vs mean-of-means, dependent cohort, unsafe SQL vs wrong SELECT, trace debug, portability diff and production gaps; run changed input independently. Record observed predictions and corrections in `artifacts/defense/rehearsal.md`, not self-assessed understanding. Exact delivery hour still owner question, no automatic date-based pass.

## Iteration 2: precise checks of new joints

| ID | Data/Impact and Level | Exact pass/fail/future evidence |
|---|---|---|
| D1 | Full M1 PlanProposal from contracts, unit validate_plan | accepted without existing results; cycle/missing alias mutations→PLAN_INVALID,0 downstream calls; artifacts/tests/unit/D1.json |
| D2 | M1 scripted provider+real DB, phases validate_plan/bind_results | unresolved refs pass static; F1 top course2 materializes, cohort1, final95.00; F2 course1/cohort1,2,3/final95,80,50; the results are not predicted in advance; artifacts/tests/graph/D2.json |
| D3 | completed result injected truncated/missing/type mismatch | RESULT_TOO_LARGE orDEPENDENCY_INVALID/bind_results, next provider/SQL0; inspect_result early bad raw→RESULT_CONTRACT_INVALID; artifacts/tests/graph/D3.json |
| V1 | Full S6/M1/tie/Library DBResult messages from contracts; unit adapter and real DB integration separately | S6 16000/2/100=80.00; tie 27000/3=9000/1→both course IDs; library1/1 not scale100; unit/denom/grain mutations→RESULT_CONTRACT_INVALID; Z1/Z2/Z3 scalar raw components separately DB-Z and normalization separately UNIT-Z (below); artifacts/tests/domain/V1.json |
| V2 | Correct specs, SQL intentionally uses incorrect but plausible amounts | runtime can accept, independent oracle must fail; no claim of complete semantic validator; artifacts/tests/domain/V2.json |
| W1 | strict bindings example, duplicate/missing/extra/type malformed/101values | valid maps exactly to two bindings; malformed→PROVIDER_INVALID_OUTPUT,101→RESOURCE_LIMIT,0 DB executions; future SDK parse smoke separately; artifacts/tests/unit/W1.json |
| W2 | question2001chars, SQL8001bytes, binding2001bytes/total8193, one DB value8193bytes | INVALID_INPUT / RESOURCE_LIMIT / RESOURCE_LIMIT / RESULT_TOO_LARGE; boundary allowed sizes pass restgates; artifacts/tests/bounds/W2.json |
| W3 | encoded model input12001bytes, injected provider usage12001input tokens | byte overflow→RESOURCE_LIMIT before network; usage overflow→BUDGET_EXCEEDED after counted attempt/no next calls; no exact tokenizer/hard memory claim; artifacts/tests/bounds/W3.json |

### Two different negative lanes
**Injected deterministic lane:** E1–E7 remain mandatory contract/graph/DB tests. UI lane uses actual Streamlit/LangGraph/DB/trace, but explicit test transport/provider fixture replaces response/error. Header screen and trace metadata `execution_profile="injected"`, `fault_case`, `injection_point`, `fixture_hash`, `real_provider_called=false`; fields in controlled test export, not new production wire inputs. You cannot select an injected profile through a regular untrusted question; developer-only local test configuration, not remote feature. Expected E3 refusal/incomplete/malformed does not require guessing the behavior of the API. These tests are offline, **0 paid calls**, not included in 24×2 live denominator.
- EI1: injected provider refusal→PROVIDER_REFUSAL; screen shows error and full same-run input→nodes→attempt→error→run_end; SQL/DB panels were clearly “not executed”, not someone else’s old rows.
- EI2: injected first malformed SQL proposal/repair valid S6→80.00; the screen sees both attempts,sanitised diagnostic, final SQL+bindings AndDB16000/2/2. Profile injected, Notlive generation pass.
- EI3: injected incomplete or transport timeout twice→PROVIDER_INCOMPLETE or PROVIDER_UNAVAILABLE; exact number attempts1/2, no fabricated answer, terminal trace. The controlled error DB is separate from E4 and is visible in the same screen view.

**Real-model generation lane:** requested/returned model/usage recorded, no injection/mocked provider. Six categories by 4 cases: aggregates/NULL; JOIN/four filters; dependent/ties; ambiguity+accepted continuation; negative data-availability N1–N4; Library schema. Each case runs 2 times; denominator **48 conversations**, not 48 separate calls. Ambiguity case includes response clarification and recorded scripted valid user selection, then real model SQL; otherwise incomplete conversation fail. All 48 outcomes are mandatory, mandatory offline/injected tests separately pass.
N1 “Medium C2 in S2?” F1→raw[0,0,0]→enrollment0,graded0,average=null,no_rows (Z1). N2 “Average C3 in S1?”→raw[0,0,1]→enrollment1,graded0,average=null,no_grades (Z2). N3 “Average student3 for all semesters?”→raw[0,0,1]→enrollment1,graded0,average=null,no_grades (same Z2 outcome, scope student3). N4 “Number of records on C3 for teacher11?”→count0 (count-only normal numeric0, exact empty_reason=null for count result). The exact field/text can be expressed otherwise only text natural-language, typed values/NULL/reason are required. These cases check for the absence of invented grades/results, **not artificial SQL/provider failure**. Refusal/timeout/invalidSQL, not corrected in the limit, at any of 48 - failed attempt, cannot be excluded from the denominator and cannot be replaced with best-of. Provider refusal on N1–N4 is not a valid alternative outcome.

24 development and 24heldout are preserved, N1–N4 are category prototypes here: heldout reviewer until freeze forms 4 new synthetic value/wording mutations with the same independently verified outcome classes, does not copy expanded F1 questions. The exact frozen fixture/wording/expected is written before live, not determined by model result. The set is currently **not yet created**, examples are template criteria, not “sealed suite already exists”. All generations/repeats/cost counted; unchanged conservative ceiling480calls/5.76M input/.96M output=$1.056 at cited Luna rates, proposed $2cap; injections add0calls. Real UI smoke outside48 requires a separate approved remaining cap, or is carried out on the same logged eval conversations; not unaccounted paid tail.

### UI1: Adopting a simple screen (required, not new platform)
Question/answer or error/clarification and expanders **SQL with secure bindings**, **DB typed columns/rows/truncation**, **full sequence of events of the same run including all attempts, errors and resume** are available on the local screen. Seq/run_id/trace_id are the same as JSONL. You can reveal every attempt and the result of every step, not just the final one. Payloads synthetic, export redaction by contracts; do not publish secret/raw exceptions.
Success S6/M1: from the UI find SQL,16000/2/2 or M1 intermediate rows, final80.00/95.00 and run_end; rows/run mismatch or unavailable trace - fail. Clarification C1: before selecting options1/3, a pause trace and “SQL has not yet been executed” is shown; after resume the original input, clarification, resume, SQL/rows/86.67 of one run are visible. EI2 error+repair: both attempts are available, do not hide the first; terminal EI1/EI3 shows full error chain, no answer/no DB claims. Opaque ID without an available view, old rows of another run, disappeared attempts during resume - fail. Evidence `artifacts/e2e/UI1/` screenshots opened panels + same-run exported trace + profile/fault provenance. This is a future real UI test; B specification only.


## B2-R1: separate future check of raw SQL and adapter
- **DB-Z (actual SQLite integration, future):** on F1 scalar C2/S2 SQL with aggregate-level `COALESCE(SUM(grade_units),0)`/COUNT(grade_units)/COUNT(*) returns integer components[0,0,0]; C3/S1 and student3/all return[0,0,1]. A separate minimal synthetic fixture with one enrollment grade_units=0 returns[0,1,1]. Check exactly the real raw typed columns and row_count1 before the adapter. NULL instead of integer0 in sum_units - fail, even if the formatter can hide the defect. Evidence `artifacts/tests/db/DB-Z.json`: DB version, fixture/query hash, actual components/types, independent expected. This is supplement S10/N1–N3/V1.
- **UNIT-Z (pure domain adapter unit, future):** submit three full DBResult Z1/Z2/Z3 from contracts without DB/model; exact normalized Answer is equal to examples: null/no_rows;null/no_grades;"0.00"/null respectively, counts0/0;0/1;1/1. Additional invalid mutation Z1 sum_units=null → RESULT_CONTRACT_INVALID, not auto-correction. Evidence `artifacts/tests/domain/UNIT-Z.json`.
- Pass requires **both** directions; unit normalization does not prove raw SQLite outputs, DB output does not prove formatter/empty_reason. In B, only document negotiation/JSON syntax checks are performed; DB-Z/UNIT-Z **not-run**. Isolated reviewer aggregate probes remain evidence reviewers, not product tests Planner.
