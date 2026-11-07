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
