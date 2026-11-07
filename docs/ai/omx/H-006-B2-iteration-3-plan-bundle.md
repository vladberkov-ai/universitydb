# H-006 B2 iteration 3: immutable Planner review baseline

Status: proposed. No implementation or execution authorization.


<!-- BEGIN FILE: ADR-OMX-003-minimal-stack.md -->
# ADR-OMX-003 - Minimal Local Stack

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
We need real LangGraph, SQL, a simple screen and a full trace, limited time. There are no product dependencies yet.

## Options
SQLite/direct LangGraph/OpenAI SDK/Streamlit/local JSONL; PostgreSQL+API/UI+LangSmith; CLI-only.

## Recommendation
First option; candidate Python3.13/LangGraph1.2.20/openai3.46.0/Streamlit1.67.0, still check compatibility. Luna baseline, snapshot Mini or Sol individual evaluation profiles.

## Rationale
A minimum of services and obvious diagnosability. The CLI doesn't cover the screen; The server option is viable, but redundant now.

## Consequences
Own trace contract, lack of HA/remote auth and stable model alias; key/access/budget unknown. Prices/pins from dated research, not a guarantee.

## Verification
Clean lock/install+security audit, real vertical slice S6, versions/usage/trace, full E2E. An explicit budget is required before live execution; no calls are made during B.

## Revision triggers
Concurrent writers/remote users, measured low Luna quality, changed API/prices or restart requirement.

Related [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md), [checks](../../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
<!-- END FILE: ADR-OMX-003-minimal-stack.md -->


<!-- BEGIN FILE: ADR-OMX-004-domain-semantics.md -->
# ADR-OMX-004 - Identities and Domain Arithmetic

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
PDF requires names, courses/semesters/teachers/enrollments/grades, but does not specify scale/retakes/weights/ties.

## Options
Normalized Offering/Enrollment; a separate Course row for each offering; co-teaching junction; credit weights/latest-retake-only.

## Recommendation
Students/Teachers names nonunique, stable ID; Course→Offering with one teacher/semester; grade nullable integer hundredths from 0 to 10000; external decimal0..100; equal weights graded enrollments, all-retakes, all exact ties, all-semesters default.

## Rationale
Separates a course from a particular offering, prevents silent identity merge, arithmetic is explainable by small fixtures without hidden weights/current date.

## Consequences
Retakes within offering/co-teaching are not modeled; The average of the course is not the average of the averages. NULL not 0. Any change in the rules changes oracle.

## Verification
S1–S14 real DB constraints/aggregates, C1 duplicate-name clarification, exact rational tie comparisons, documented fixtures.

## Revision triggers
The owner selects credit-weighted/latest-only/co-teaching/history or another default semester.

Related [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md), [checks](../../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
<!-- END FILE: ADR-OMX-004-domain-semantics.md -->


<!-- BEGIN FILE: ADR-OMX-005-bounded-graph-contracts.md -->
# ADR-OMX-005 - Bounded graph, clarification and security

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
We need meaningful multistep, errors and continuation; LLM proposals are untrusted, interrupt restarts node.

## Options
Free agent loop; fixed chain without clarification; bounded graph with typed state and checkpoint.

## Recommendation
Bounded LangGraph bycontracts v1: static validate_plan acceptstyped symbolic refs bydeclared ResultSpec; runtime bind_results requirescompleted/consistent/nontruncated dependencies, error→no downstream. InMemorySaver forlocal demo, session-bound idempotent resume, 3 steps+1 repair,5calls,2clarifications; DB readonly/authorizer/limits/watchdog, deterministic formatter.

## Rationale
Limited errors/cost explained by dependencies; free loop is more difficult to debug, chain without clarification violates scope.

## Consequences
After restart resume expired; safety does not prove semantic correctness; limiter/policy also require actual DB testing; We do not promise arbitrary SQL correctness.

## Verification
D1–D3,V1,W1–W3,C1–C5,E1–E7,SQL-policy integration,M1 sensitivity; no pre-interrupt side effects; pause budgets preserved.

## Revision triggers
Durable restart/multi-user requirement, newoperations/dialect, complex>3step legitimate cases.

Related [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md), [checks](../../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
<!-- END FILE: ADR-OMX-005-bounded-graph-contracts.md -->


<!-- BEGIN FILE: ADR-OMX-006-schema-boundary-tracing.md -->
# ADR-OMX-006 - Schema boundary and own traces

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
R05/R06 require adaptability and a complete Input→Nodes→SQL→Results→Answer chain; do not require a specific platform.

## Options
Domain names embedded in core; descriptor+domain adapter; generic arbitrary-dialect abstraction. JSONL or LangSmith.

## Recommendation
Minimum ResultSpec+domain result adapter: metric/group keys/typed aliases/unit/scale/components, exact sum_units+graded_count for averages/ties; nonnull integer sum_units via aggregate-level COALESCE(SUM(grade_units),0), distinguishing void/NULL-only/real0 by denominator/enrollment_count; core doesn't guess University by names. SQLite-specific DB adapter, schema-agnostic core and University/Library descriptors; local versioned JSONL by contracts with full synthetic rows, redaction/public export separate.

## Rationale
The second schema is a real limited transfer test; do not claim support for all dialects. Local traces do not require an account/network service.

## Consequences
Its own completeness check/retention, library scope is just the same dialect. Full real PII is not allowed in demo. LangSmith requires a separate billing/retention solution.

## Verification
L1 same core hash+DB+live+E2E; V1–V2 units/grain/denominator failures; DB-Z actual raw components and separately UNIT-Z normalization of three zero cases; T1/T2+UI1 chain/completeness/screen access/secret exclusion; trace failure not success.

## Revision triggers
New dialect, real personal data, remote centralized tracing/retention/SLO requirement.

Related [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md), [checks](../../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
<!-- END FILE: ADR-OMX-006-schema-boundary-tracing.md -->


<!-- BEGIN FILE: ADR-OMX-007-verification-delivery.md -->
# ADR-OMX-007 - Independent oracle, live gate and delivery evidence

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
Mocked graph does not measure NL-SQL. Previously proposed 27/30 withdrawn; percentage does not replace mandatory R/U. Saved/committed/public are different.

## Options
Singlesuccess percentage; onlyunit mocks; layered checks+independent fixtures+small strict live suite/manual/public gates.

## Recommendation
S/C/E/T/L+D/V/W/UI1 mandatory tests; EI1–EI3 deterministic injected UI lane with provenance and 0 paid calls separately, 24dev+24heldout×2 counted runs; proposed48/48 **real-model conversations** semantic passes, including 4negative-data cases×2, without injected faults in denominator without unsafe/privacy failures; <=$2 approved cap; manual protection and public SHA separately.

## Rationale
The small demonstrator must reproduce every promised scenario; strict repetition detects instability, but is not a statistical guarantee for arbitrary questions.

## Consequences
Gate may require prompt/model refinement and fresh heldout; best-of/relabel failures are not allowed. Budget/key/public authority are missing yet; B docs only.

## Verification
test-plan oracle/manual disclosedSQL/DB/full trace path, N1–N4 real-model no-data outcomes vs injected E1–E7/EI1–EI3; unexpected provider failures count failed live attempts, all attempts+hashes/usage, clean clone, remote SHA anonymous access, observed owner explanation; current application checks not-run.

## Revision triggers
Owner-approved revised scope to eval, token-rate changes, dataset contamination, new model/prompt/schema or observed failure pattern.

Related [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md), [checks](../../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
<!-- END FILE: ADR-OMX-007-verification-delivery.md -->


<!-- BEGIN FILE: adr-index-additions.md -->
# Suggested additions ADR index

All entries proposed 2026-11-07; Save ADR-OMX-001/002 and existing chat snapshots without rewriting. Only after closeout the leader integrates the lines into docs/adr/README.md, preserving the baseline bytes/hash.

- [ADR-OMX-003: Minimum local stack](../../adr/ADR-OMX-003-minimal-stack.md) - proposed.
- [ADR-OMX-004: Identities and domain arithmetic](../../adr/ADR-OMX-004-domain-semantics.md) — proposed.
- [ADR-OMX-005: Bounded graph, clarification and security ](../../adr/ADR-OMX-005-bounded-graph-contracts.md) — proposed.
- [ADR-OMX-006: Schema boundary and own traces](../../adr/ADR-OMX-006-schema-boundary-tracing.md) - proposed.
- [ADR-OMX-007: Independent oracle, live gate and delivery evidence](../../adr/ADR-OMX-007-verification-delivery.md) - proposed.
<!-- END FILE: adr-index-additions.md -->


<!-- BEGIN FILE: architecture-proposal.md -->
# UniversityDB: architectural proposal

Date 2026-11-07. **Proposed**, not accepted by owner, not implemented. Base: adopted matrix R-01..17/U-01..08, compact scope ADR-CHAT-002 (simple screen, dependent scenario, second circuit). Requirement sources: [safe snapshot](../../chat/requirements.md), [scope](../../chat/decisions/ADR-CHAT-002-result-scope.md). More recent private requirements have been read; private paths/raw are not published. All product requirements remain open; U-07 previously verified, this is not result B.

## RALPLAN-DR
Principles: (1) minimal explainable system; (2) calculates the database, not the model; (3) ambiguity is revealed, not guessed; (4) security, semantics and evidence are different checks; (5) the kernel does not know the names of the domain tables.
Three drivers: required LangGraph and demonstrated full path; limited time/cost of local demonstration; reproducible error diagnosis.

| Option | Benefit | Cost/Risk | Conclusion |
|---|---|---|---|
| SQLite + direct LangGraph + OpenAI SDK + Streamlit + local JSONL | one process/DB file, minimum services, simple traces | local concurrency restrictions, custom trace validator | recommend |
| PostgreSQL + LangGraph + separate web API/UI + LangSmith | server access, ready tracing, path to multi-user | additional services, credentials, billing/retention, more code | viable for production, not for the first slice |
| SQLite + CLI without screen | less UI code | does not cover accepted simple screen | auxiliary diagnostic CLI only, not the main option |

## Stack and outer bases
Used **previously completed research inputs 2026-11-07 around 09:20 UTC**, not new research/reviewer verdicts: researcher and dependency-expert in docs/ai/omx/H-006-v5-B-*-evidence.json. The versions below are candidates, not installed/tested together. When implementing: Python 3.13 with a current verified patch, built-in sqlite3 (write down the SQLite version); LangGraph 1.2.20 (MIT), openai 3.46.0 (Apache-2.0), Streamlit 1.67.0 (Apache-2.0). Python patch and transitive lock are determined by a separate compatibility check; no settings in B.

We recommend OpenAI Responses `gpt-6-luna`, `store=False`, strict structured output; alias without a fictitious snapshot. Price according to dated research: $0.10 input/$0.50 output for 1M tokens; cached $0.01 input. 4k input+1k total output = $0.0009 per challenge, 100 questions ×3 challenges ≈$0.27 before additional attempts. Alternatives: `gpt-5.4-mini-2026-03-17` ($0.75/$4.50) for snapshot reproducibility; `gpt-6.1-sol` ($2/$10) separate eval profile for measured Luna deficiency, **not automatic fallback**. Account access is unknown, OPENAI_API_KEY is missing in the verified environment. Don't allow live until there is an explicit budget. `store=False` is not zero retention. All retries/reasoning tokens are included in the price.

Official primary links of dated research: [LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api), [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts), [PyPI LangGraph](https://pypi.org/project/langgraph/), [SDK](https://pypi.org/project/openai/), [Streamlit](https://pypi.org/project/streamlit/), [SQLite](https://docs.python.org/3.13/library/sqlite3.html), [SQLite security](https://www.sqlite.org/security.html), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [pricing](https://developers.openai.com/api/docs/pricing), [data controls](https://developers.openai.com/api/docs/guides/your-data), [LangSmith pricing](https://www.langchain.com/pricing). Their presence does not prove SQL quality/compatibility/access. LangSmith retention is not selected due to the pricing/compliance discrepancy noted in the research. Before lock - scoped [advisory audit](https://github.com/langchain-ai/langgraph/security/advisories).

## Components and Boundaries
Screen → application request/continuation → LangGraph core → schema/domain adapter, LLM adapter, SQL validator, DB adapter → deterministic answer formatter → Screen. All nodes → local trace sink. A simple screen shows answer, SQL/safe bindings, typed DB columns/rows and **full same-run trace/attempts** in local expanders; An ID without accessible content is not sufficient. The UI does not generate SQL; LLM does not execute it. Prompts are future versioned adapter resources, not created in B. DB does not contain API keys. The application has one active request for the UI session, only a local loopback; shared multi-user deployment out of job.

## Proposed model and ERD (not executable SQL)
Students(student_id PK integer, name nonempty text); Teachers(teacher_id PK integer, name nonempty text); Courses(course_id PK integer, code unique text, title nonempty text); Semesters(semester_id PK text, starts_on date, ends_on date); Offerings(offering_id PK integer, course_id FK, teacher_id FK, semester_id FK, section text); Enrollments(student_id FK, offering_id FK, grade_units nullable integer 0..10000). Conceptualgrade in documents= grade_units/100, physical SQL usesgrade_units.

Students 1—0..* Enrollments *..0—1 Offerings; Courses/Teachers/Semesters every 1—0..* Offerings. Offering has exactly one Course, Teacher, Semester; Enrollment — exactly one Student/Offering. Unique(course,semester,section); PK Enrollment(student_id,offering_id). The name is not a key and not unique; trim-non-empty, Unicode preserved, exact normalized whitespace/casefold search, no fuzzy merging. Multiple matches require a selection ID; teachers too.

We offer grade 0..100 inclusive, maximum 2 decimal places; NULL = no final grade yet, not zero. One final grade per enrollment; a mulligan in another offering is acceptable and is recorded as a separate entry; history of attempts inside offering outside scope. Course is different from Offering; the same course in two semesters, not one entry. The semester is specified by an explicit ID, dates start<=end; there is no silent "current": a request without time means all semesters with a scope signature. If the user says “current”, if there is no clear setting, clarify.

AVG = sum of non-NULL grade / number of graded enrollments; no credit weights, no mean-of-means, no rounding to last formatting. Counts are explicitly separated by enrollment_count, graded_count, distinct_student_count. For the “average student” all of his graded enrollments are of equal weight; “at rate” - all corresponding enrollments of all selected offerings. Top returns **all** tied by exact average (comparing rational sum/count), ID order for stability, NULL is not involved. Zero graded → null average and explanation, not 0. Decimal arithmetic/precise storage in future implementation check: preference to store integer grade hundredths, externally decimal (see contracts); names/semesters not from the current date.

Alternatives: credit-weighted requires credit data; latest-retake-only changes the meaning without asking; teacher co-teaching requires junction; current semester default hides scope. These options are not “wrong,” but they extend the model and require reconciliation. Unambiguous domain restrictions are not proof of the semantic correctness of any SQL.

## Graph and meaningful dependent path
START → validate_input → load_schema → resolve_scope → [clarify/plan] → validate_plan → bind_results → generate_sql → validate_sql → execute → inspect_result → [next_step/answer/error] → END. Clarify: interrupt + checkpoint → resume validation → resolve_scope. SQL repair returns generate_sql at most once, not an infinite loop; provider transient retry maximum one. Refusal, incomplete, unsafe SQL, incoherent results, depleted budget are error. Empty/no grades - normal with explanation. Clarify limit 2 for the entire conversation.

Example: “In S1, choose the course with the highest average final grade; then show his students’ averages across all their courses in S1.” Step1 DB returns exact integer sum_units/graded_count/enrollment_count for all courses; University domain result adapter selects all tied course IDs without rounding; step2 uses **obtained** rather than guessed IDs for cohort distinct student IDs; step3 aggregates all S1 enrollments of the selected students. The plan stores typed symbolic references on the declared ResultSpec outputs of its predecessors; validate_plan validates the DAG to values, bind_results materializes only completed/consistent/nontruncated results immediately before the dependent call; even if the optimizer combines operations, fixture mutation must change the cohort. Regular queries are not forced to do 3 SQL. The limit is 3 executed logical SQL steps, except for the only repair; counters are shared via resume.

## Schema-agnostic proof
Core sees versioned SchemaDescriptor: tables/columns/types/keys/allowed functions/semantic metrics/entity disambiguation metadata, not Students or grade. University adapter supplies the semantics above and the final registry ResultSpec/domain result adapter (units/grain/components); core doesn't guess semantics based on column names. Library replaces registry/adapter/descriptor, not core; This is not a universal query compiler. Second adapter Library: Readers(reader_id,name), Books(book_id,title), Loans(loan_id,reader_id,book_id,returned boolean); metric open_loans = count returned=false. The same SQLite dialect/driver/graph/validator/trace/UI. Replacing only DB fixture and descriptor/domain vocabulary; We do not promise other SQL dialects. Check: core tree hash is unchanged, test L1 from test-plan is passed by real DB and separately by live NL. If you need to edit core by table name - R-05 fail.

## Pre-mortem (3)
1. Beautiful answer, incorrect JOIN/mean-of-means. Measures: independent sum/count oracle, adversarial unequal groups, distinct cohort, mandatory regression; fail semantic eval even with valid SQL.
2. Interrupt repeated toll calls/issued someone else's resume. Measures: side-effect-free clarify node, server-bound session/run/checkpoint, consumed request IDs, stale/version checks, global budgets; tests C1–C4.
3. Demo ready locally, submission/explanation not proven. Measures: clean clone, public access+remote SHA only with separate permission, owner rehearsal; R-15/16 do not close docs commit.

Related [contracts](../../plans/contracts.md), [tests](../../plans/test-plan.md), [stages](../../plans/implementation-plan.md), [production](../../plans/production-considerations.md), [matrix](../../plans/requirements-test-matrix.md). Stop: return the proposed package to the chat; B does not provide execution authorization.
<!-- END FILE: architecture-proposal.md -->


<!-- BEGIN FILE: changes-from-iteration-1.md -->
# Changes after iteration 1

Planner revision, 2026-11-07. **Proposed**, not Architect/Critic approval. Full completed reviews iteration1 Architect→Critic read; their iterate verdict is preserved, old bytes are not changed. The fixes are documentary, there are no applications or new dependencies.

| Finding | Change | Check/future pass criterion |
|---|---|---|
| B1 static/runtime dependencies | contracts: validate_plan by typed declared ResultSpec and DAG; bind_results only completed/consistent/nontruncated; PLAN_INVALID/DEPENDENCY_INVALID/RESULT_TOO_LARGE; full M1 JSON + exact mutations; architecture phases agreed | D1 accepts full plan up to SQL, cycle/missing alias rejects; D2 materializes changed cohort; D3 blocks downstream. Now a documentary walkthrough has been completed, not a graph run |
| B2 units/grain/aggregate boundary | final ResultSpec registry+DomainResultAdapter, integer sum_units/graded_count/enrollment_count, exact rational ties+round half-up2; typed examples S6/M1/ties/Library and malformed spec/results; core without University heuristics | V1 16000/2/100→80.00, ties both courses, library1/1, wrong unit/denom/grain fail; V2 emphasizes the need for independent oracle |
| B3 real model vs injected faults | E/EI deterministic lane with profile/fixture/injection provenance and 0paid calls; real48conversation gate with N1–N4 no-data instead of the required refusal/SQL errors; unexpected failures count fail | No injected result is live accuracy; budget unchanged conservative480calls/$1.056+$2proposedcap; test-plan/matrix/ADR007/I4 approved |
| B4 accepted screen | local expanders answer+SQL/bindings+typed DB rows+full same-run trace/attempts; clarification/resume/error explicit noSQL states | UI1 success/resume/EI multiple attempts checklist, opaque ID fail; architecture/I1/I4/R06/R17 agreed upon|
| A1 strict provider wire | bounded closed Binding array, explicit discriminated nullable slots Anddeterministic SQLite map; duplicate/placeholder/type checks | W1 valid map, malformed rejects; SDK compatibility future not claimed; no new library |
| A2 resources | byte/token accounting distinction, SQL/param/input/single-value boundaries, residual SQLite pre-fetch memory risk | W2/W3 boundaries; no hard tokenizer/memory isolation claim; production residual risk retained|

Saved: proposed owner decisions; all17R+8U; independent fixture numbers; three pre-mortem; production distinctions; A/history/research; no live calls/SQL executable/test code/runtime prompts/UI implementation. No additional research was required. Exact candidate package compatibility/security audit and owner budget remain future gates.

Mapping old: six main docs→docs/plans; ADR003–007→docs/adr; additions→separate index-additions and subsequent integration by the leader; changes-from-iteration-1→docs/ai/omx/H-006-B2-iteration-2-changes.md. Bundle includes full bytes of all 13 constituents; manifest hashes raw, non-OMX domain-separated lifecycle digests. After freeze changes only the new iteration. The next step of the leader is a separate Architect→separate Critic→customized gates, not execution handoff.
<!-- END FILE: changes-from-iteration-1.md -->


<!-- BEGIN FILE: changes-from-iteration-2.md -->
# Small revision after iteration 2

Planner, 2026-11-07. Status proposed; not approval/closeout. Full completed Architect2/Critic2 read; both iterate with a single residual blocker B2-R1. The remaining previously tested solutions were not changed; changes-from-iteration-1.md is saved byte-by-byte as correction history.

| Finding | Edit | Verification / disposition |
|---|---|---|
| B2-R1: row-level COALESCE does not normalize empty scalar SUM | normative contracts sum → aggregate-level COALESCE(SUM(grade_units),0), integer0; nonnull ResultSpec saved; three complete typed raw DBResult→Answer examples Z1/Z2/Z3 | [0,0,0]→null/no_rows;[0,0,1]→null/no_grades;[0,1,1]→"0.00"/null. Documentary JSON/type/consistency checks done; addressed pending new independent reviews |
| Consistency oracle/test scope | S10/N1–N3/V1 refer to exact raw components; DB-Z separately actual SQLite raw-output integration, UNIT-Z separately pure adapter normalization | Both future checks are required and do not replace each other; invalid nullable raw sum→RESULT_CONTRACT_INVALID. No product tests were performed |
| Decision traceability | ADR-OMX-006 clarifies aggregate normalization and DB-Z/UNIT-Z | Minimal changes to the existing proposed boundary, without nullable raw schema expansion/new dependency |

The alternative nullable raw sum + normalization to typed validation is rejected as unnecessary complication: outer COALESCE preserves the current strict ResultSpec and bounds. Scalar row_count1 with enrollment_count0 is clearly different from the original rows; grouped missing rows are not automatically promised. Units/counts/rounding/NULL policies are preserved.

Iteration1/2 and reviews immutable. Bundle includes all14constituents in full bytes, manifest raw SHA256; This is not an OMX domain-separated lifecycle digest. Mapping of six main documents/ADR former; this file→docs/ai/omx/H-006-B2-iteration-3-changes.md after supported closeout. New research, SQL probe, executable schema/seed, application/tests/UI/runtime prompts, dependencies, paid calls were not executed. The next step is separate Architect3→Critic3, not execution authorization.
<!-- END FILE: changes-from-iteration-2.md -->


<!-- BEGIN FILE: contracts.md -->
# Contracts v1 - proposed

Date 2026-11-07; not implementation. All JSON objects are closed (`additionalProperties:false`), the specified fields are required, nullable means explicit null; UTF-8, finite numbers, no NaN/Infinity. IDs opaque non-empty strings <=128; timestamps UTC RFC3339. Unsupported version - error INVALID_INPUT before LLM/DB. The future external JSON schema and strict provider schema are separate implementations of the same contract, not an assumption of full JSON Schema support for the provider.

## Input and continuation
NewRequest: {version:"1", kind:"new", request_id:ID, schema_id:ID, question:string 1..2000}. Session identity comes from the server-side UI session, not trusted by the user field. request_id for idempotency; the same ID/bytes in the same session returns the saved response without repeated calls; another payload with the same ID → REPLAY_CONFLICT.
ResumeRequest: {version:"1",kind:"resume",request_id:ID,run_id:ID,checkpoint_id:ID,clarification_id:ID,selection:string}. selection only one of option.value; freeform with field=semester is allowed only after descriptor validation. On v1, all clarifications have final options, which means arbitrary freeform is rejected.

Valid new: `{"version":"1","kind":"new","request_id":"q1","schema_id":"university-v1","question":"Average byC1 VS1?"}`.
Valid resume: `{"version":"1","kind":"resume","request_id":"q2","run_id":"r1","checkpoint_id":"cp1","clarification_id":"cl1","selection":"student:1"}`.
Invalid: `{"version":"1","kind":"new","request_id":"q1","schema_id":"university-v1","question":"","sql":"DROP TABLE Students"}` - empty question and extra sql, without accessing the model. Invalid resume selection student:99 with options 1/3 - INVALID_SELECTION, the existing pause is not consumed.

Resume is tied to the current server session, run, last checkpoint, clarification, schema/content hash and policy_version. Mismatch owner → RESUME_FORBIDDEN (without revealing the existence of someone else's run); old checkpoint or schema hash → STALE_RESUME; 15 min expired/restart InMemorySaver → RESUME_EXPIRED, create a new question on explicit UI action. On accepted resume consumed atomically; exact request replay returns the previous response; another request after consumption → STALE_RESUME. Graph thread_id is server-side and the same with Command(resume); do not take an arbitrary thread from the client. The calls/SQL/clarifications and elapsed active work counters are not reset. The Interrupt node does not make LLM/DB calls until interrupt: LangGraph restarts it from the beginning.

## Output envelope
{version:"1",run_id:ID,status:"ok"|"clarification"|"error",answer:Answer|null,clarification:Clarification|null,error:Error|null,trace_id:ID}.
Exactly corresponding non-null status branch. Answer: {text:string,columns:[{name:string,type:"string"|"integer"|"decimal"|"boolean"}],rows:array<array<scalar|null>>,scope:string,empty_reason:null|"no_rows"|"no_grades",truncated:boolean}. decimal in JSON as a string with canonical decimal digits (for example "83.33"); numbers are integers for counts/IDs, do not round internal amounts. NULL does not mean empty row. The tabular normal form and the explanation are always the same; The answer is template, without a separate LLM number generator.
Clarification: {clarification_id:ID,checkpoint_id:ID,field:string,prompt:string,options:[{value:string,label:string}],expires_at:timestamp}; options >=2, unique values, labels distinguish records by ID/context. Error: {code:enum,message:string,retryable:boolean,failed_node:string}; does not expose raw exception provider/paths/credentials. retryable means the user can start a new request, rather than allowing an additional internal retry.

Valid normal: `{"version":"1","run_id":"r1","status":"ok","answer":{"text":"C1, S1: 83.33 (3 assessments).","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"}],"rows":[["83.33",3]],"scope":"C1; S1","empty_reason":null,"truncated":false},"clarification":null,"error":null,"trace_id":"t1"}`.
Valid clarification: `{"version":"1","run_id":"r2","status":"clarification","answer":null,"clarification":{"clarification_id":"cl1","checkpoint_id":"cp1","field":"student","prompt":"WhichAlex?","options":[{"value":"student:1","label":"Alex (1)"},{"value":"student:3","label":"Alex (3)"}],"expires_at":"2026-11-07T12:15:00Z"},"error":null,"trace_id":"t2"}`.
Valid error: `{"version":"1","run_id":"r3","status":"error","answer":null,"clarification":null,"error":{"code":"SQL_TIMEOUT","message":"Request exceeded time limit.","retryable":true,"failed_node":"execute"},"trace_id":"t3"}`.
Invalid envelope: status ok with answer=null or error non-null; decimal JSON number instead of string; row length != columns; NaN; unknown code; extra property. Error in own output → INTERNAL_CONTRACT, fail closed, without fabricated answer.

## Internal state and adapters
GraphState required: version, run_id, session_ref (private), request_id, schema_id, schema_hash, policy_version, question, phase (node enum from architecture), resolved_scope (map entity→IDs / semester IDs), plan (Step[]), current_step integer, results (map step ID→Result), counters {llm_calls,sql_attempts,repairs,clarifications,graph_steps,input_tokens,output_tokens}, active_ms integer, deadline_at timestamp, checkpoint_id nullable, clarification_id nullable, consumed_request_ids[], terminal nullable Output. Persist only bounded state, not provider client/DB handle. InMemorySaver onlylocal demo; after restart no recovery promise.
Step={step_id:ID,depends_on:ID[],purpose:Text,result_refs:Reference[],result_spec:ResultSpec}; DAG, <=3 logical steps, symbolic references to the declared outputs of DAG predecessors are accepted before execution; The static and runtime phases are defined below. LLM Request receives question, descriptor, explicit scope, completed step references and budgets; not raw DB dump. LLM SqlProposal={version:"1",step_id:string,result_spec:ResultSpec,sql:string<=8000,parameters:array<Binding>,expected_columns:[string],result_kind:"rows"|"aggregate",explanation:string<=1000}. All fields are required. This is a hypothesis, not a permission. Model cannot add steps outside validated plan. Parameter placeholders for values; identifiers only descriptor allowlist.
SchemaDescriptor={version:"1",schema_id,content_hash,dialect:"sqlite",tables:[{name,columns:[{name,type,nullable}],primary_key:[string],foreign_keys:[{columns,table,target_columns}]}],entities:[{name,table,id_column,name_column}],metrics:[{name,definition,unit,null_policy,grain}],allowed_functions:[string],policy_version}. Strings definitions — domain context, Notexecutable instructions. Hash covers canonical descriptor+domain policy; identifiers verified against DB metadata. Descriptor loading andintegrity scan required untilrequests.
DB Result={step_id,result_spec,columns:[{name,type}],rows:array,row_count:int,truncated:bool,elapsed_ms:int}; SQL adapter should return typed values ​​and not recalculate averages after truncation. SQL Validator must check single statement, allowedlisted schema/functions, readonly operations and resolved entity/scope references; authorizer deny DML/DDL/ATTACH/DETACH/PRAGMA/nonallowlisted reads/functions and extension loading; URI mode=ro. Don't use regex as proof. If the secure parser/compiled authorization does not allow you to set the required property - reject, do not run. Query-only is an additional layer, not a replacement for read-only. Repair is only allowed for recoverable syntax/unknown column, not unsafe SQL and not semantic mismatch.
Answer formatter checks column types, count>=0, graded<=enrollment, grade/average range, declared grain and scoped IDs; inconsistency → DATA_INCONSISTENT. Integrity scan checks FK, duplicate keys, grade range. It is impossible to deterministically prove arbitrary NL→SQL; plausibly invalid SQL is detected by oracle eval, not the promised runtime "understanding".

## Budgets, errors and truncation
For the entire conversation: 2 clarification pauses, 3 logical SQL steps + 1 repair execution =4 SQL attempts; maximum of 5 provider calls, including transient retry and repair (whichever ends first). 12k input accounting ceiling (pre-call byte gate and caveat below)/2k total output tokens per call; total 60k/10k; graph recursion_limit=32 supersteps plus own persisted graph_steps<=64 via resume. One provider timeout 15s, one transient retry with 1s backoff, SDK auto-retries disabled so that they do not multiply. SQL cooperative timeout 2s progress handler; lock wait <=0.5s. Total active work 60s, does not include waiting person; watchdog completes DB worker at 3s, entire run at 60s. Worker isolation is a future implementation, not a guaranteed Python progress handler. Trace failure before execution → TRACE_UNAVAILABLE, do not execute a non-traceable query.
Results: maximum 100 displayed rows, read 101 for detection, <=64KiB/result, <=128KiB retained run result payload. For aggregates, the cap is applied **after aggregation**, not LIMIT input enrollments. Exact scalar aggregates count all scoped rows. Truncated grouped/top/cohort result cannot be used as a full dependency: RESULT_TOO_LARGE and a proposal to narrow the scope, without partial final claims. For a normal list, normal truncated=true is allowed with an explicit "first 100" signature, a deterministic ORDER BY, and no full-count statement. Oversize string/result → RESULT_TOO_LARGE.
Error codes: PLAN_INVALID, DEPENDENCY_INVALID, RESULT_CONTRACT_INVALID, RESOURCE_LIMIT, INVALID_INPUT, REPLAY_CONFLICT, INVALID_SELECTION, RESUME_FORBIDDEN, STALE_RESUME, RESUME_EXPIRED, CLARIFICATION_LIMIT, UNSAFE_SQL, SQL_INVALID (after1 repair), SQL_TIMEOUT, DB_UNAVAILABLE, DATA_INCONSISTENT, PROVIDER_UNAVAILABLE (after1 transient retry), PROVIDER_REFUSAL (0 retry), PROVIDER_INCOMPLETE (0 retry), PROVIDER_INVALID_OUTPUT (0 retry), BUDGET_EXCEEDED, RESULT_TOO_LARGE, TRACE_UNAVAILABLE, INTERNAL_CONTRACT. Withoutrows normal no_rows; enrolled/no grades normal no_grades Andnull avg/0 graded. Credentials absence → PROVIDER_UNAVAILABLE to networkcall. Allterminal errors savelast successful steps Vtrace, but they don't provide them as a complete answer.

## Trace v1
Event required: version:"1",trace_id,run_id,event_id,seq:int>=1,parent_event_id:null|ID,request_id,node,kind (input|node_start|llm_attempt|sql_validated|sql_attempt|db_result|clarification|resume|node_end|answer|error|run_end),attempt:int>=0,timestamp,duration_ms:null|int,payload:object. Each attempt has its ownevent_id; immutable append, monotonic seq, couplesstart/end orerror; run_end exactly one forterminal run (pause Notterminal). LLM payload: requested/returned model IDs, prompt/template hashes, schema/data versions, input/output token usage, provider request ID safe orredacted. SQL payload: SQL, sanitized bound params, validation decision; DB payload: columns/rows/truncated/row_count/hash. Complete chaininput→nodes→SQL→DB rows→answer orerror; trace Andvisible answer have onerun_id.
Locally only synthetic fixtures: full question/SQL/rows is acceptable. Do not log keys, auth headers, env, private paths, hidden chain-of-thought, raw provider diagnostics. Real personal data is not included in the demo: stop/edit on ingress; public export whitelist fields + PII review, redaction marker + hash of the original local payload, do not promise repeatability of redacted contents. Public examples are synthetic only. Trace budget 1MiB/run; exceeding → BUDGET_EXCEEDED with a minimal terminal event in the reserved 4KiB, failure entry → UI reports trace unavailable and run is not considered evidence.

## Clarification of internal message types (normative v1)
In the compact signatures above, each field is required; Below, exhaustive aliases remove ambiguity. ID=string1..128, Hash=64 lowercase hex, Text=string<=2000, Name=string1..128, UInt=integer>=0, Scalar=string|integer|boolean|null, Decimal=canonical string matching -?[0-9]+(.[0-9]+)?, no exponent. SQL parameters boolean is passed as integer0/1; In v1 numeric grade bindings only integer grade_units; numeric decimal-string bindings are not allowed (text Binding remains plain text). Grade physical column **grade_units INTEGER NULL** in Enrollments, constrained0..10000. The name grade in the conceptual ERD/fixtures is the external semantic projection grade_units/100; generated SQL works with grade_units, decimal formatter translates to sum_units/count/100. Metric descriptor reports unit and formula. You cannot mix 90 with 9000. If a future implementation retains conceptual `grade` as the physical name, it is a separate reviewed contract revision, not a silent replacement.

GraphState: version literal"1"; run_id/session_ref/request_id/schema_id ID; schema_hash Hash; policy_version Name; question Text; phase enum(validate_input,load_schema,resolve_scope,clarify,plan,validate_plan,bind_results,generate_sql,validate_sql,execute,inspect_result,next_step,answer,error,end); resolved_scope map<Name,array<ID>>; plan array<Step>0..3; current_step UInt; results map<ID,DBResult>; counters object with the listedUInt; active_ms UInt; deadline_at RFC3339; checkpoint_id/clarification_id ID|null; consumed_request_ids array<ID> max16; terminal Output|null. Missing values before calculation:empty maps/arrays, counters0, nullable fields null; Notomission. session_ref never published. Counters.persisted includes failed attempts, challengesplan generation Same.
Step: step_id ID; depends_on array<ID> max2; purpose Text; result_refs array<Reference> max3; result_spec ResultSpec; references are statically checked against the declared ResultSpec of the predecessor; values ​​are bound only in runtime bind_results. PlanProposal={version:"1",steps:array<Step>1..3,needs_clarification:boolean,clarification_field:Name|null}; if needs_clarification true steps=[] (min1 exception), field non-null; false field=null. Prevent LLM from returning arbitrary options: the entity resolver creates options from a known bounded directory.
LLMRequest={version:"1",operation:"plan"|"sql"|"repair",run_id:ID,attempt:UInt,model_id:Name,question:Text,descriptor:SchemaDescriptor,scope:map<Name,array<ID>>,plan:arra y<Step>,completed_results:map<ID,DBResult>,previous_error:SafeDiagnostic|null,budget:{remaining_calls:UInt,max_input_tokens:UInt,max_output_tokens:UInt},prompt_hash:Hash}. SafeDiagnostic={code:Name,message:Text}; not raw exception. Response for operation plan is strictly PlanProposal, for sql/repair is strictly SqlProposal. In a normal simple query, is fused plan+SQL acceptable? **Not in v1**: plan call + sql call; dependent3 steps require 4 calls, the fifth for retry/repair, both can exhaust the budget at the same time. Failure BUDGET_EXCEEDED is more honest than the hidden sixth call. Prior state and schema descriptor are considered part of the input token budget. Truncated completed_results are prohibited for dependent step.
SchemaDescriptor: version literal"1"; schema_id ID; content_hash Hash; dialect literal"sqlite"; tables array<Table>1..32; entities array<Entity>0..16; metrics array<Metric>0..32; allowed_functions array<Name>0..32; policy_version Name. Table={name:Name,columns:array<Column>1..64,primary_key:array<Name>1..8,foreign_keys:array<ForeignKey>0..16}; Column={name:Name,type:"integer"|"text"|"boolean",nullable:boolean}; ForeignKey={columns:array<Name>1..8,table:Name,target_columns:array<Name>1..8}, lengths equal; Entity={name:Name,table:Name,id_column:Name,name_column:Name}; Metric={name:Name,definition:Text,unit:Name,null_policy:"exclude"|"include",grain:array<Name>1..8}. Content hash excludes own hash field, canonical UTF8 JSON sorted keys; includes all other fieldsdescriptor Anddomain policy versioned text. IndependentDB content hash recordedrun trace metadata, does not replaceschema hash.
DBResult: step_id ID; result_spec ResultSpec (copiesverified spec fromexecution adapter, Notprovider metadata); columns array<{name:Name,type:"string"|"integer"|"decimal"|"boolean"}>; rows array<array<Scalar>> (decimal subtype serialized string), row_count UInt equals returned rows.length; truncated boolean; elapsed_ms UInt. No nullable fields besides row scalar. SQLProposal version literal"1",step_id ID,result_spec ResultSpec,sql string1..8000,parameters array<Binding>0..100,expected_columns array<Name>1..32,result_kind enum rows/aggregate,explanation string0..1000. Everycolumn nullable by resultSQL, not onlyphysical column; formatter checkszero-denominator/null cases separately.
Startup adapter integrity scan builds a bounded entity catalog (<=1000 entities/schema, otherwise unsupported demo dataset) with IDs and normalized names from the DB; it is included in the data snapshot hash. resolve_scope reads this directory, does not generate SQL and does not pay LLM to select duplicate names. Dataset read-only and immutable entire process lifetime; changing DB/descriptor reload invalidates catalog/checkpoints. Therefore, C1 “0 SQL before selection” refers to request execution after startup, and not to initial DB metadata/catalog reads; startup reads are recorded separately as a diagnostic trace and are not hidden in request budgets. Atomic resolve of arbitrary production datasets outside scope. Students/Teachers ambiguity is determined before the plan call; LLM can also return needs_clarification, then only the field being checked and deterministic options, otherwise INVALID_INPUT.

## Two-phase DAG and minimum ResultSpec (iteration 2, normative)
The contracts in this section clarify the Step/ResultSpec and responsibility of the adapter; do not introduce a query compiler or a new dependency. All fields required/closed; unfamiliar fields/metric IDs are rejected. SQL still generates the real model; an independent oracle is still needed.

ResultSpec={metric_id:Name,shape:"rows"|"aggregate"|"top",group_keys:array<Name>0..4,columns:array<ResultColumn>1..16,components:{sum:Name|null,denominator:Name|null,count:Name|null},unit:Name,scale:integer>=1}. ResultColumn={name:Name,type:"integer"|"string"|"boolean",nullable:boolean}. Reference={from_step:ID,column:Name,type:"integer"|"string"|"boolean",bind_as:Name}; bind_as unique within step; source column must exist and match type, cannot nullable for ID dependency. All these schemesclosed, components present even with threenull.
DomainResultAdapter receives {spec:ResultSpec,raw:DBResult,scope:resolved_scope} and returns {columns:Answer.columns,rows:Answer.rows,dependency_rows:typed rows,empty_reason:nullable enum}. This object is internal, fields required; dependency_rows satisfies ResultSpec columns and does not contain fabricated values. Core checks schema/types, DAG/limits and calls the registered adapter by schema_id+metric_id; **does not recognize University by name sum_units/grade**. The adapter checks the exact equality spec with one of the registered shapes, keys/uniqueness/ranges/components and normalizes. Metric IDs - final registry, not arbitrary DSL; support for new metric - change domain adapter/test cases, not core.
University registry: `u.grade_mean.v1` shape aggregate, keys[] or[student_id]/[course_id]/[teacher_id]/[offering_id] fromallowlist; integer sum_units,graded_count,enrollment_count, unit grade_hundredth,scale100, components sum=sum_units,denominator=graded_count,count=enrollment_count. `u.top_course.v1` the samegrade shape withgroup_keys=[course_id], shape top; `u.student_ids.v1` shape rows, group_keys=[student_id], the only onenonnull integer student_id, unit identifier,scale1, components all null. For detailsJOIN allowed`u.enrollment_rows.v1`: keys=[student_id,offering_id], columns student_id/offering_id/course_id/teacher_id integers, student_name/course_title/teacher_name/semester_id strings, grade_units integer nullable; unit grade_hundredth,scale100, components all null. Count-only `u.enrollment_counts.v1` shape aggregate, approved group key sets Howmean, columns enrollment_count/graded_count/distinct_student_count nonnull integers, unit count,scale1, components sum=null,denominator=null,count=enrollment_count. Metricsfixture S1–S14 are implemented by theseshapes; combinedcount/mean conclusionsformatter receives through registeredmean extension withdistinct_student_count (explicitly allowedinteger alias, not freeextra field).
Library registry: `l.open_count.v1` shape aggregate, group_keys=[reader_id], columns reader_id integer,name string,open_count integer nonnull; unit count,scale1, components sum=null,denominator=null,count=open_count. Registry and second DB - domain-only changes. If set to 0, each reader's row is saved; count does not turn into average.
For mean SQL should return integer COALESCE(SUM(grade_units),0) (aggregate-level normalization with integer zero), COUNT(grade_units), COUNT(*) by scoped enrollment relation (enrollment_count); zero denominator requires sum_units=0, output average=null, no_grades for enrollment>0 and no_rows otherwise. sum_units>=0, graded_count<=enrollment_count and sum_units<=10000*graded_count. Average and top comparison performs **University result adapter** exact rational arithmetic: sum_units/(100*graded_count), cross multiplication comparison without rounding, for final display decimal half-up2. Top adapter gets all candidate aggregates, excludes denom0 and leaves all exact maximal ties; truncated candidates → RESULT_TOO_LARGE, SQL rounded LIMIT1 is not allowed. group keys are unique; extra keys/columns or missing denominator → RESULT_CONTRACT_INVALID before answer/downstream. DB wrapper checks raw names/types/rows against spec; SQLite itself does not return unit metadata, so the verified spec copied from the accepted step, the SQLProposal spec must match it exactly. Incorrect arithmetic in SQL with plausible aggregates is still possible: runtime bounds do not prove query semantics, oracle checks this separately.

Phase `validate_plan`: before the first SQL, after plan call - unique step IDs, <=3, acyclic, array topological order, depends_on preceded, each Reference.from_step is listed in depends_on, declared aliases/types/nonnull compatible; ResultSpecs belong to registry. **Predecessor values ​​are not needed yet.** DAG/reference/shape error → PLAN_INVALID, failed_node=validate_plan; no downstream SQL/provider calls (plan call is already taken into account).
Phase `bind_results`: before generate_sql of each dependent step - all dependencies completed+domain-validated+untranched; alias/type are actually present, runtime values ​​are deduplicated and sorted by typed ID. Missing result/column/type/consistency → DEPENDENCY_INVALID, failed_node=bind_results; truncated → RESULT_TOO_LARGE in bind_results; no calls downstream. Empty dependency → short-circuit normal empty answer/no_rows, not an “all students” query or SQL IN(). DB shape failure of the original step → RESULT_CONTRACT_INVALID in inspect_result before bind_results. Cases runtime type mismatch test corrupted injected state, which is unattainable through the correct inspect_result, but fail closed protection is required.

### Full JSON examples (documents, failed calls)
Valid M1 PlanProposal is accepted by validate_plan to results:
```json
{
  "version": "1",
  "steps": [
    {
      "step_id": "top",
      "depends_on": [],
      "purpose": "Average coursesS1, select all maximum",
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
      "purpose": "Distinct students selected coursesS1",
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
      "purpose": "Averages of selected students across all coursesS1",
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

M1 top raw F1 → adapter dependency_rows [[2,10000,1,1]], Notcourse1:
```json
{"step_id":"top","result_spec":{"metric_id":"u.top_course.v1","shape":"top","group_keys":["course_id"],"columns":[{"name":"course_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"course_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,25000,3,4],[2,10000,1,1],[3,0,0,1]],"row_count":3,"truncated":false,"elapsed_ms":1}
```

Tie fixture top raw → dependency_rows both lines course1/course2, equality27000*1=9000*3:
```json
{"step_id":"top","result_spec":{"metric_id":"u.top_course.v1","shape":"top","group_keys":["course_id"],"columns":[{"name":"course_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"course_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,27000,3,4],[2,9000,1,1],[3,0,0,1]],"row_count":3,"truncated":false,"elapsed_ms":1}
```

M1 final raw F1 → student1 average95.00:
```json
{"step_id":"means","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":["student_id"],"columns":[{"name":"student_id","type":"integer","nullable":false},{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"student_id","type":"integer"},{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[1,19000,2,2]],"row_count":1,"truncated":false,"elapsed_ms":1}
```

Library raw → names/counts Ada1,Bob1 withoutgrade normalization:
```json
{"step_id":"library","result_spec":{"metric_id":"l.open_count.v1","shape":"aggregate","group_keys":["reader_id"],"columns":[{"name":"reader_id","type":"integer","nullable":false},{"name":"name","type":"string","nullable":false},{"name":"open_count","type":"integer","nullable":false}],"components":{"sum":null,"denominator":null,"count":"open_count"},"unit":"count","scale":1},"columns":[{"name":"reader_id","type":"integer"},{"name":"name","type":"string"},{"name":"open_count","type":"integer"}],"rows":[[1,"Ada",1],[2,"Bob",1]],"row_count":2,"truncated":false,"elapsed_ms":1}
```

Invalid examples are specified by the exact JSON Patch-like mutations of valid full examples (not a separate wire type):
- M1 `steps[0].depends_on=["means"]` and `steps[0].result_refs=[{"from_step":"means","column":"student_id","type":"integer","bind_as":"x"}]` create a loop → PLAN_INVALID/validate_plan,0 SQL.
- M1 `steps[1].result_refs[0].column="missing_id"` → PLAN_INVALID/validate_plan,0 SQL.
- B successfullycompleted top aftervalidation injected `truncated=true` → RESULT_TOO_LARGE/bind_results; cohort provider/SQL calls0.
- S6 result_spec.unit="grade" or scale=1 with the expected grade_hundredth/100 → RESULT_CONTRACT_INVALID/inspect_result (if this is a SQLProposal mismatch, the same code/validate_sql before execution).
- S6 columns/row exclude graded_count (row=[16000,2]) → RESULT_CONTRACT_INVALID/inspect_result; denominator2 cannot be accepted by position.
- S6 result_spec.group_keys=["student_id"] at declared[] → RESULT_CONTRACT_INVALID/inspect_result; duplicate student_id in per-student result → tot že code.
- Injected corrupted top column course_id type string aftercompletion → DEPENDENCY_INVALID/bind_results. Normal typed result failure caught earlierinspect_result.

### A1: strict provider bindings
Provider SQLProposal wire uses **only bounded closed array**, not dynamic map:
Binding={name:Name,type:"integer"|"text"|"null",integer_value:integer|null,text_value:string|null}. All fourfields required, additionalProperties=false; integer → integer_value nonnull/text_value null, text → the opposite,null → bothnull. Name matches [A-Za-z_][A-Za-z0-9_]{0,63}. Parameters<=100; text_value<=2000 UTF8 bytes; totalUTF8 encoded JSON bindings<=8192 bytes. duplicate names/type mismatch/unused or missing SQL placeholders → PROVIDER_INVALID_OUTPUT toDB; actual provider schema compatibility smoke morefuture. Fortext we usetype=text (NotSQL Column type), grade units onlyinteger. Dynamic maps VLLMRequest scope/completed_results — interiortrusted input, Notprovider output schema.
Example wire: `[{"name":"student_id","type":"integer","integer_value":2,"text_value":null},{"name":"semester","type":"text","integer_value":null,"text_value":"S1"}]` → deterministic internal sqlite bindings `{"student_id":2,"semester":"S1"}`; placeholders :student_id,:semester. ID-list materialization {1,2} → named placeholders :course_ids_0,:course_ids_1 and two integer Binding, not comma-string. All SQL placeholders are checked against accepted bindings; IDs are checked against resolved scope/materialized dependency. No concatenation of user values ​​in SQL. 100 values ​​max; larger materialized list RESULT_TOO_LARGE before generate_sql.

### A2: resource boundary, no promise of hard memory sandbox
SQL UTF8 bytes<=8000 and chars<=8000; provider output with oversized SQL/bindings → RESOURCE_LIMIT before SQL execution. Request question max2000 chars; encoded provider input general<=12000 UTF8 bytes as a conservative **local byte gate**, not an exact tokenizer. Separately, max_input_tokens12000 remains accounting contract: usage>12000 unexpected→BUDGET_EXCEEDED, no subsequent calls. Byte gate does not prove provider-specific token bound; framing/provider-added tokens are unknown, so the hard pre-call token guarantee is not declared, the projected worst-case token budget is reserved for all 5 calls. Unverified tokenizer dependency is not added. Single DB text value>8192 UTF8 bytes→RESULT_TOO_LARGE when fetch; result64KiB/retained128KiB/trace1MiB as before. SQLite can allocate memory before fetch/progress: hard memory isolation **not implemented/guaranteed by v1 design**; only local synthetic DB and bounded workload, OS memory ceiling/worker resource limits separate production risk/check before remote deployment. Time watchdog is not proof of memory bound.


Additional status link: `GraphState.results` stores only completed **validated dependency DBResult**: ResultSpec/columns/elapsed_ms saved, rows=DomainResultAdapter.dependency_rows, row_count recalculated, truncated=false. The full raw DBResult is written to trace before adaptation; top raw candidates and selected exact ties are visible as separate node_end payloads. Therefore bind_results reads the already selected top IDs, and not all candidates. The derived Answer fields do not overwrite the raw result trace. No-grades per-row annotations are generated by domain adapter; for several rows empty_reason envelope=null, NULL in the corresponding average cell and text explanation; for single all-null scalar empty_reason=no_grades. Count-only metric even if 0 returns numeric0 and empty_reason=null. Scope entity IDs in external resume opaque (`student:1`); resolver by descriptor converts them into real typed primary keys for SQL bindings, does not do blind string→integer conversion.


## B2-R1: scalar empty, NULL-only and true zero evaluation

The standard sum is normalized **after SUM**: documentary formula `COALESCE(SUM(grade_units),0)`, integer0; denominator=`COUNT(grade_units)`, enrollment_count=`COUNT(*)` by already filtered enrollment relation. Do not use row-level COALESCE as a replacement for aggregate-level normalization: to relation without rows SUM otherwise NULL. For a grouped request, the missing group is not created automatically; these examples refer to scalar aggregate without GROUP BY. Nullable raw sum is not allowed or “corrected” by the formatter. These are documentary messages not executed by SQL/application calls.

### Z1: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — linescalar aggregate, not a numberenrollments):
```json
{"step_id":"z1","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,0,0]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (external average in scale 0..100, decimal string or null):
```json
{"text":"No entries forC2 VS2; average not determined.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[null,0,0]],"scope":"C2; S2","empty_reason":"no_rows","truncated":false}
```

### Z2: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — linescalar aggregate, not a numberenrollments):
```json
{"step_id":"z2","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,0,1]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (external average in scale 0..100, decimal string or null):
```json
{"text":"One entry without final grade; average not determined.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[null,0,1]],"scope":"C3; S1","empty_reason":"no_grades","truncated":false}
```

### Z3: raw DBResult → normalized Answer
Raw (sum_units — integer hundredths, scale100; counts — integer counts; row_count1 — linescalar aggregate, not a numberenrollments):
```json
{"step_id":"z3","result_spec":{"metric_id":"u.grade_mean.v1","shape":"aggregate","group_keys":[],"columns":[{"name":"sum_units","type":"integer","nullable":false},{"name":"graded_count","type":"integer","nullable":false},{"name":"enrollment_count","type":"integer","nullable":false}],"components":{"sum":"sum_units","denominator":"graded_count","count":"enrollment_count"},"unit":"grade_hundredth","scale":100},"columns":[{"name":"sum_units","type":"integer"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[[0,1,1]],"row_count":1,"truncated":false,"elapsed_ms":1}
```
Normalized Answer (external average in scale 0..100, decimal string or null):
```json
{"text":"One final grade0; average0.00.","columns":[{"name":"average","type":"decimal"},{"name":"graded_count","type":"integer"},{"name":"enrollment_count","type":"integer"}],"rows":[["0.00",1,1]],"scope":"synthetic single enrollment grade 0","empty_reason":null,"truncated":false}
```

Z1 normal no_rows, no error: raw aggregate contains one row of components with zero initial enrollments. Z2 enrollment exists, but denominator0→no_grades. Z3 denominator1→exact0/(100*1)=0, final half-up2="0.00", empty_reason=null. For N3/student3 Z2 with the corresponding scope is valid. NULL average is not declared0; true grade0 is not declared as no grade.
<!-- END FILE: contracts.md -->


<!-- BEGIN FILE: implementation-plan.md -->
# Plan for future implementation - proposed, without execution handoff

Goal: compact working and explainable demonstrator according to [matrix](../../plans/requirements-test-matrix.md), not production service. The current B ends up returning to chat. scope/simple screen/dependent scenario/second schema accepted; domain semantics, stack and eval gate are just recommendations. A don't repeat. This document does not allow installation, paid calls, remote or push creation.

## Sequence after individual acceptance/instruction
| Stage | Dependencies/resources | Deliverables and verification | Commit/manual gate |
|---|---|---|---|
| I0 Record decisions and budget | chat review of this bundle/ADR003–007 | accepted/changed semantics, model, eval cap, deadline; presence-only key availability; versions/advisory audit/lock candidate compatibility | separate docs decision commit; stop without permission live/budget |
| I1 First real vertical slice | I0; future src/universitydb/{db,agent,llm,tracing,ui}, resources/schema+seed, prompts/; F1 | minimal real LangGraph question S6→Responses→validated SQLite→80.00→JSONL→Streamlit with available SQL/bindings/typed DB rows/full same-run trace+attempts; smoke trace+actual prompts; read-only/timeout boundaries to first generated SQL | small feat+tests commit, owner walkthrough success/SQL guard; not first large catalog of abstractions |
| I2 Semantics, queries andfailure paths | I1; schema/domain adapter/contracts | fullF1, S1–S14 oracle DB tests; D1–D3 two-phaserefs, V1–V2 domain result spec/units, W1–W3 bounds; C1–C4 checkpoint/resume; E1–E7 bounded faults; contract unit tests; incremental small commits | targeted tests at first,compile/lint/typecheck after;chat review average/ties/retakes/clarification |
| I3 Dependency and tolerance| I2; graph plan/results, library adapter/F1L | M1 F1/F2+tie sensitivity; L1 unchanged core hash, mocked and actual DB tests; traces completeness/redaction | feat portability commit; owner predicts mutation without agent |
| I4 Live eval Andfull screen E2E | I3, credentials, explicit spending cap; versioned datasets/prompts | development then sealed heldout 48 counted runs; category coverage, all attempts/cost; manual live S6/M1/C1/L1+UI1, separatelyoffline injected EI1–EI3 withprovenance (Notlive score); no hidden fallback | eval evidence commit; failures→defect+new version+rerun, not lowering the threshold|
| I5 Packaging/clean clone/defense | I4 pass; docs/examples/traces/prompt coverage, README | clean install offline suites and approved live smoke; independent manual explanation; public-safe checklist; unresolved requirements remain open | local release docs commit, then separateremote/push authorization; verify remote SHA+anonymous access toR15 closure |

With each code step: inspect diff→targeted regression→all offline tests→compile/lint/typecheck available selected tools→explicit staged paths→diff --check→commit→SHA receipt. No blanket staging, no amend/reset foreign changes. Tests must exist before semantic fixes. Prompt changes versioned along with regression and eval evidence. Future commands are defined in test-plan; exact entrypoints are confirmed when the code is created, and are not currently passed off as existing. Future dependencies are only allowed by a new implementation instruction; B not installation.

## Minimal blockers and questions for the owner
1. Accept the proposed grade hundredths/0..100/NULL, all-retakes, equal enrollment weights, all ties? We recommend yes for explainable arithmetic; credit/latest-only require other fixtures.
2. Accept all-semesters default with an explicit signature and the “current” clarification? We recommend without hidden current date.
3. Accept SQLite+direct LangGraph+Streamlit+local trace, InMemorySaver and absence of resume after restart? We recommend yes for local demonstration; SQLite checkpointer separate future dependency upon restart requirement.
4. Accept Luna profile and cap $2 for the proposed development+heldout plan? The key is not in the current env, account availability is unknown. Live is stopped without permission/credentials, offline progress can be assigned separately.
5. Accept strict 48/48 small-suite gate (not population claim), manual obligations separately? If not, agree before the results, not retroactively.
6. Exact delivery time, acceptable public kit, GitHub owner/remote? Don't make things up. Public publication and paid calls require separate permissions.

## Handoff Andstop
Leader B: after real sequential reviews and supported terminal closeout, packs safe copies, saves provenance/review hashes/actual prompt coverage, doc checks, separate docs commit B and report. Only then does the user discuss the proposed solutions. Executor does not start automatically under this plan. The future implementation completes only with evidence of the entire matrix; if public/credentials/owner rehearsal are missing - partial report with a specific blocker, not “ready”. This review is not a product test.
<!-- END FILE: implementation-plan.md -->


<!-- BEGIN FILE: production-considerations.md -->
# Production considerations — project

Proposed 2026-11-07; The application has not yet been created, **not production-ready**. "On task" below means a planned, uncompleted property.

| Topic | Plan for a compact task | Before production additionally |
|---|---|---|
| Reliability | typed contracts, bounded retries/timeouts, no unsafe fallback, independent oracle, InMemorySaver with explicit expiry after restart | durable checkpoints with secure serialization, migrations/backups/restore drills, failure recovery, HA/SLO/error budgets, provider outage strategy |
| Scalability | local read-only SQLite, one active request/UI session, small result/token caps | workload benchmark, queue/admission control, tenant quotas, connection pools; for concurrent writers, consider PostgreSQL and the new dialect adapter/test suite; do not migrate SQLite security policy blindly |
| Monitoring/tracing | local complete versioned JSONL Andscreen expanders SQL/bindings/typed results/full trace, attempts/usage/cost/latency/error codes, synthetic public exports | searchable centralized storage, retention/access policy, dashboards/alerts p95 latency/errors/token spend, trace sampling doesn't loseaudit/security events, on-call ownership |
| Security/privacy | loopback only, synthetic data, no keys in logs/repo, mode=ro+authorizer/allowlists+limits, process SQL watchdog, ingress/output checks | authentication/authorization/row-level access, tenant isolation, secret manager/rotation, dependency supply-chain audit, privacy/legal review, encrypted data/checkpoints, sandbox resource isolation, threat model/pentest |
| Deployment | reproducible Python+dependency lock/version receipt, clean clone instructions, local config presence checks | container/hardened runtime, CI/CD signed artifacts, rollout/rollback/migration gates, TLS/network policies, infra access controls, production cost governance |

Read-only ≠ semantic correctness; JSON schema ≠ correct SQL; trace completeness ≠ permission/publication; store=False ≠ zero retention. Progress handler cooperative, hard worker kill/memory enforcement must be separately implemented/measured. Lack of authentication is acceptable only loopback synthetic demo; do not publish the UI as a service available to everyone. LangSmith optional future alternative after retention/billing/privacy review, optional dependency.

Future check: owner explains each tradeoff and shows planned vs actual evidence; failed production feature is not masked in assignment readiness. Revision triggers: real personal data, remote multi-user access, DB entry, concurrent workloads, durable resume/recovery or new provider/SQL dialect. Then we need a new ADR/threat model, not a mechanical increase in limits. See [architecture](../../plans/architecture-proposal.md), [tests](../../plans/test-plan.md).

Iteration2 clarification: bounded SQL/bindings/input byte gates and oversized-value tests W1–W3 do not prove hard memory isolation. SQLite can allocate memory before the fetch/progress handler; in the local synthetic demo this is clearly a residual risk. Before remote/untrusted production, OS worker memory/resource policy and real adversarial verification are required; the new dependency/parser/tokenizer in B is not selected.
<!-- END FILE: production-considerations.md -->


<!-- BEGIN FILE: requirements-test-matrix.md -->
# Requirements → future evidence

Proposed test mapping, 2026-11-07. Not a single line of R is covered by this design review. Source: accepted matrix (PDF/explicit instructions; secure [snapshot](../../chat/requirements.md)); U-07 previously verified, U-08 procedure proposed. Save actual future results with tested commit SHA, versions and failures; the paths below do not yet exist. The exact fixtures/scenarios are revealed in [test-plan](../../plans/test-plan.md).

| ID/commitment | Script, data/precondition | Exact expected and pass/fail | Level | Future evidence |
|---|---|---|---|---|
| R-01 SQL Students/Teachers/Courses, names | F1; attempt empty name/duplicate PK | 4 students/2 teachers/3 courses; two Alex are saved separately; empty name and duplicate PK rejected; otherwise fail | DB integration + schema review | artifacts/tests/db/R01.json |
| R-02 offerings/semesters/enrollments/grades | F1; orphan offering/enrollment, duplicate(1,O1), grade101 | 5 offerings/8 enrollments, precise connections; violations rejected; NULL accepted; S9 retake80.00 | DB integration | artifacts/tests/db/R02.json |
| R-03 LangGraph NL→SQL→execution→answer | live S6, real provider/DB/graph | “S1 C1 Kim student2”→O1/O5→80.00, full graph trace, not mock | live NL + E2E | artifacts/e2e/R03/ |
| R-04 aggregate/JOIN/4 filters/multistep | S1–S14 and M1 F1/F2, D1–D3/V1 | all results match the oracle table; M1 95.00→{95,80,50} with mutation; no filters are missing | DB + mocked graph + live NL | artifacts/tests/coverage/R04.json |
| R-05 schema-agnostic/modular | L1 library descriptor/DB swap | counts1/1; all-returned0/0; core hash unchanged;Library result adapter counts1/1 without grade scaling; no University identifiers in core; otherwisefail | code review + DB + live/E2E | artifacts/tests/portability/L1/ |
| R-06 full trace | T1/UI1 success M1, C1/resume and injected EI1–EI3 | input→nodes→SQL→DB typed results→answer/error, single run, attempts/seq, no secrets; screen reveals SQL/bindings/DB rows/full same-run trace; opaque ID/missing link fail | integration + manual trace walkthrough | examples/traces/R06/ |
| R-07 errors/emptiness/contradictions/ambiguity | S10, C1–C4, E1–E7, F3; injected EI1–EI3 separately; live N1–N4 | correct error codes/NULL/resume, bounded retries; EI provenance, N1–N4 no-data outcomes; unexpected provider errors fail live; plausible wrong SELECT limitation stated | unit + DB + graph + E2E | artifacts/tests/negative/R07.json |
| R-08 SQL/JOIN, NL-SQL, E2E tests | offline suites + sealed live48 + manual full path | All mandatory offline+injected suites pass, separately 48 real-model conversations pass; injections do not replace NL | multi-level tests/review | artifacts/tests/R08-summary.json |
| R-09 clean modules DB/agent/prompts/tracing | future src tree and M1 walkthrough | UI without SQL; core without table names; DB/LLM adapters are replaceable; prompts versioned; explicit imports review | code review | artifacts/reviews/R09.md |
| R-10 production explanation | production-considerations + owner discussion | all 5 topics reliability/scaling/observability/security/deploy, implemented/future are separated; production-ready is not allowed | document/manual | artifacts/reviews/R10.md |
| R-11 SQL schema/seed delivery | clean clone tested SHA | schema+seed are present, create F1 and constraints, no private data; absence of any fail | actual DB + public checklist | artifacts/delivery/R11.md |
| R-12 LangGraph code/tests delivery | clean clone no local caches | code compiles; offline suites execute, mandatory tests pass, public files available| integration/build + public | artifacts/delivery/R12.md |
| R-13 decisions with justification | ADR003+ and future revisions | each significant choice context/options/rationale/consequences/verification, proposed/accepted are distinguished; public index complete | document review + public | artifacts/reviews/R13.md |
| R-14 examples/results/traces | S6/M1/C1/E1 and tested SHA | every example input→exact output→same-run trace, synthetic/redacted; no fabricated runs | E2E + artifact review/public | examples/README.md |
| R-15 public repo complete set | separate remote/push permission, tested SHA | unauthenticated URL/raw access, remote SHA=tested SHA, all R11–14 paths; local commit is insufficient | public/manual | artifacts/delivery/public-check.md |
| R-16 show/explain/defend | owner himself performs M1,C1 and debugging E1 | oracle forecast and explanation of each transition/alternative, identified gaps fixed; agent speech does not pass | observed rehearsal | artifacts/defense/rehearsal.md |
| R-17 small working/debuggable result | clean clone + simple screen + scripts | success/clarification/failure/second schema are reproduced; UI1 expands SQL/data/full traces/attempts; owner explains agentless, scope without unnecessary services | E2E + manual | artifacts/delivery/scope-check.md |
| U-01 actual prompts | leader+every real child and future app prompts | index actual vs template/read context; hashes/redactions/cutoff/omissions, app prompts when created; incomplete history cannot be called complete | provenance/manual | docs/ai/README.md; artifacts/provenance/coverage.json |
| U-02 deadline/date of demonstration | owner confirms the exact hour and timezone | delivery timestamp before the agreed date; date of request November 7/8, 2026, exact time remains open; not verified without it | manual timeline | artifacts/delivery/timeline.md |
| U-03 OMX, one execution environment per stage | B native lifecycle receipts, future handoffs | verified sequential roles/terminal active:false without execution handoff; one canonical workspace/owner, not role by prompt label | runtime evidence review | docs/reports/H-006-architecture-review.md |
| U-04 all decisions in the repository | ADR index + feature decision audit | all significant choices including rejected alternatives are available, ADR001/002/history saved; missing decision fail | document review | artifacts/reviews/U04.md |
| U-05 memory/ownership | before/after hashes vault and snapshots; links repo-owned docs | vault read-only in B, four allowlisted snapshots are not turned into originals, OMX wiki links are not duplicate reports | provenance/hash review | docs/operations/H-006-B2-preservation.json |
| U-06 commit/push policy/checkpoints | A verified, B separate docs commit after closeout | A unchanged,explicit staged safe paths, B SHA recorded; saved/committed/pushed/public separated;no remote/push B | Git/document evidence | docs/operations/H-006-B2-commit-receipt.json |
| U-07 preparatory passage | historical CHAT004→005 and H002 evidence | the previously verified fact of the transition is saved with attribution; do not run a replay and do not declare a new result B | historical source review | artifacts/reviews/U07-history.md |
| U-08 procedure for understanding the result | future chat review + owner example/counterexample/independent explanation | protocol notes observed understanding/gaps for schema/graph/SQL/tracing/evals/portability, more than one “is clear” | manual/chat | artifacts/defense/understanding.md |

Current status: only documentary fixtures/expected and plan evidence. Runtime lifecycle/historical saving is checked by the leader separately; app tests, live eval, public access and owner rehearsal **not-run**. Missing credentials block future live execution, not documentary stage B.
<!-- END FILE: requirements-test-matrix.md -->


<!-- BEGIN FILE: test-plan.md -->
# Inspection plan and documentary fixtures - proposed

No application test is executed in B. Below are independent oracle and future commands/evidence, non-executable seed/SQL/test code. All names are synthetic. The exact rules are [architecture](../../plans/architecture-proposal.md), [contracts](../../plans/contracts.md). Any mandatory fail blocks acceptance regardless of the live eval percentage.

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
<!-- END FILE: test-plan.md -->
