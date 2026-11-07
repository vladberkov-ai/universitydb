# H-013 — I2 + I3 offline acceptance contract

Current authority CHAT-045/H-013 extends H-011-v2/CHAT-043/ADR-CHAT-006 without reapproving ADR003–007. [Whole bounded brief](I2-I3-offline-brief.md), [scoped decisions](../adr/ADR-OMX-012-I2-I3-offline-contracts.md). Implementation evidence is pending; this contract is not a passed-test report. Historical [I2 contract](I2-offline-contract.md), [contracts](contracts.md) and [test plan](test-plan.md) stay unchanged; historical live thresholds, timeouts and truncation proposals are not current authority.

## Exact result registry and dependency boundary
Each accepted step carries exact registered ResultSpec, not a global domain spec. Registry fixes metric, shape, ordered columns/type/nullability, components, group keys, unit/scale. SQL/result metadata must equal accepted spec; no aliases/units/grain invented by provider, no first-row type inference. Registry families (implementation can encode group as registered variant):

| Metric family | Grain | Raw components/columns | Unit/scale |
|---|---|---|---|
| u.grade_mean.v1 | scalar or one of course_id/student_id/teacher_id/offering_id/semester_id | optional registered group key + sum_units integer nonnull, graded_count integer nonnull, enrollment_count integer nonnull | grade_hundredth/100 |
| u.enrollment_counts.v1 | scalar or registered group key | optional key + enrollment_count/graded_count/distinct_student_count integer nonnull; count object explicit in answer | count/1 |
| u.enrollment_rows.v1 | student_id/offering_id | student_id integer, student_name string, offering_id integer, course_id integer, course_title string, teacher_id integer, teacher_name string, semester_id string, grade_units integer nullable | grade_hundredth/100 for grade only; IDs unscaled |
| u.top_course.v1 | course_id | course_id + sum_units/graded_count/enrollment_count as above | grade_hundredth/100 |
| u.student_ids.v1 | student_id | student_id integer nonnull unique | identifier/1 |
| l.open_count.v1 | reader_id | reader_id integer nonnull, name string nonnull, open_count integer nonnull | count/1 |

Group IDs are nonnull typed schema keys (semester_id string; other keys integer). Group/list empty results keep declared schema. Mean scalar components [0,0,0]→null/no_rows; [0,0,1]→null/no_grades; [0,1,1]→0.00. Group per-row no_grades stays explicit. Counts including0 stay numeric0, not grade-normalized. Top excludes denominator0, compares exact integer cross-products and retains all ties sorted by ID; rounded-equal non-ties fail selection. Raw candidates and adapted selected dependency rows both traceable.

Plan≤3 steps, unique IDs, topologically ordered static DAG; missing/cyclic/forward-invalid refs, undeclared dependencies/column/type/metric/grain rejected before execution. Static validation does not require future results. Runtime binding separately reads completed validated result rows, checks exact type and ≤100 values, de-duplicates cohort IDs and materializes named bound values. Never SQL text/string-concatenated fragments. Missing/type mismatch/truncated/oversized result fails before downstream provider/SQL, counters unchanged. Explicit empty upstream is empty-set/no-result semantics, never removal of filter. SQLProposal bindings closed typed array and strict SQL placeholder correspondence; no missing/unused/duplicate binding or bool-as-integer coercion.

## University Q1–Q12 (all mandatory)
Q1 global [50000,6,8]→83.33. Q2 S1 [35000,4,6]→87.50; C1 all[40000,5,6]→80.00; Kim10 all[25000,3,5]→83.33; student1 all[26000,3,3]→86.67. Q3 explicit I1 four-filter Bea2→80.00 and student1→90.00. Q4 course/S1 C1[25000,3,4]→83.33,C2[10000,1,1]→100.00,C3[0,0,1]→null. Q5 C1/S1 enrollment4/graded3/distinct3. Q6 exact C1/S1 labeled JOIN listing (1,1,9000),(2,1,6000),(3,1,null),(2,5,10000). Q7 student1/C1 across offerings→80.00, S2→70.00. Q8 empty C2/S2, all-null C3/S1 and true zero distinct. Q9 topS1 C2; exact tie mutation C1/C2 both90; 250/3≠83.33. Q10 Alex options1/3, selecting1→86.67,3→no_grades, no generated SQL before choice. Q11 current semester known choices, ID/name conflicts, unknown entities, vague count object explicit. Q12 every group key and optional/combined student/course/teacher/semester scopes (all16 subsets) with independent expected and discriminating mutations. Names/IDs not silently conflated; absent scope explicitly all including semesters.

Independent [frozen oracle](../operations/H-013/frozen-oracle.json) and [stdlib validation](../operations/H-013/independent_oracle.py) contain all-subset grouping expectations, counts/listing/top and fixture definitions. Product formatter/query generator is never the oracle. Semantic tests must catch plausible safe wrong JOIN/average-of-means.

## M1 — actual data dependency proof
Question: for students of the course with highest mean in S1, show their mean across all S1 courses. Step top returns selected course IDs; cohort computes union of enrolled students; means computes each student's S1 sum/graded/enrollments from actually bound IDs. F1 top[2],cohort[1],final1=95.00. F2 adds (student3,offering2,5000): top[1],cohort[1,2,3],final95.00/80.00/50.00; independently recomputed before freeze, not inferred from documentary label “tie”. Exact-tie fixture changes (2,1)→8000,(1,2)→9000: top[1,2],cohort[1,2,3],final90.00/90.00/null(no_grades). Empty/no-top and empty cohort explicit; duplicate IDs union once. Capture differing actual upstream rows, materialized bindings, downstream SQL/results, full same-run trace; fixed three-query/node-count proof fails. Cover missing/type/oversized/truncated upstream, partial failure, resume/replay with no repeated side effects; downstream calls0 on invalid dependency.

## Library early portability proof
Independent fixtures Readers Ada1/Bob2, Books X10/Y11, Loans (1,1,10,false),(2,1,11,true),(3,2,10,false): counts Ada1/Bob1. Add reader3 with no loans→0; returned mutation loan1 true→Ada0/Bob1; all returned→0/0. FK corruption, wrong returned type/range, duplicate reader names/clarification and schema/session/resume isolation required. Separate schema/seed/descriptor/registry/adapter/domain policy; same core graph/DB safety/provider/tracing/UI tree when switching. No core branch on domain table names, no count division by100. Prove real DB AND compiled graph at CP-B, then regression throughout C/D; report same integrated core hash under both domains, not old I1 hash.

## Continuation, errors, bounds, trace/UI
Real installed in-memory saver/interrupt, server-session/run/checkpoint/clarification/schema/data/policy bound. Max2pauses/TTL900s, human wait not active work; shared counters/run deadline persist. Same accepted request replay returns prior result with0 calls; changed payload conflict. Reject foreign/stale/expired/invalid/schema-data-policy changed before calls. Restart explicit expiry. Do not replay pre-interrupt provider/SQL.

One repair for parse/unknown-column only; exhaustion terminal, unsafe/semantic mismatch no repair. Provider timeout/refusal/incomplete/invalid/unknown-usage, DB missing/lock/timeout/inconsistent data, trace sink/payload/result failure must not fabricate answer. Unknown usage retains holds and stops next dispatch, no ScriptedProvider-only accounting weakening. Shared calls≤5,SQL attempts≤4,active180s,plan60s/SQL45s/output32768 and existing payload/result/trace ceilings; no reset on resume, no silent limit increase. Oversized/truncated aggregates/top/dependencies fail closed.

Trace ordered input/nodes/all provider and SQL attempts/bindings/raw typed rows/adapted results/binds/answer-or-error/run_end, one run identity with unique sequence, no secrets/headers/private payload. English UI answer/error/clarification plus SQL/bindings/types/rows of every step, all attempts/resume and full trace; new request/failure clears stale answer. Trace failure precludes success. Real temporary offline browser success/clarification/M1/Library/repair/error + isolated AppTest mandatory, not live accuracy.

## Coverage, levels and blocking gates
Every Q/negative requirement above at unit, real SQLite, compiled-graph scripted and UI levels as relevant. Negative suites: bad fields/types/bindings/spec/units/grain, NULL/empty/list typing, duplicates/FK/grade/type corruption; SQL writes/DDL/ATTACH/PRAGMA/extension/multistatements/subquery evasion denied and DB hash unchanged; bad refs and dependency sensitivity; all resume rejection/replay/expiry/bounds; repair exhaustion/unsafe no execution; DB/provider/trace/resource/full-wire failures. Full offline pytest/Ruff/format/mypy/compileall/diff and independent oracle; cleaner then rerun, independent code-reviewer APPROVE + architect CLEAR/configured gates and invariant audit. Record actual commands/exits/tested SHA/case expected-actual and gaps. Offline scripted proof is not real-model NL→SQL accuracy. No live or push needed for this offline DoD.

| Requirements | Current-block obligation and evidence |
|---|---|
| R01,R02,R11 | University schema/seed/integrity/labels/retakes/NULL; real SQLite oracle + corruption/security tests |
| R03,R04 | Compiled graph all classes/filters/M1 actual binds; offline only, live quality remains separate |
| R05 | Early Library same-core tree identity, both adapters/DB/graph/mutations/isolation |
| R06 | Complete trace and accessible same-run English UI, attempts/resume/binds/raw rows |
| R07 | Clarification, empty/NULL/zero, bounded failures/repair/accounting/safety |
| R08 | Unit/SQLite/graph/AppTest/browser/full offline regression, honest live not-run |
| R09 | Domain/core separation, registry/contracts/ref validation, independent review |
| R10 | Maintain production explanation and implemented-versus-future risks, no production readiness claim |
| R12,R13,R14 | Code/tests/ADR rationale/prompts/examples/traces/source identity and local receipts |
| R15 | Final publication pending separate permission; fresh remote observation, push not-run |
| R16,R17 | Offline working/debuggable service proof now; owner defense/explanation later |
| U01,U04 | Actual received prompts separate from read context/templates, root-child omissions and RU/EN attribution; scoped ADR decisions/alternatives |
| U02 | Exact deadline not invented |
| U03 | One actual owner; supported new scoped workflow after binding, genuine reviewer lanes |
| U05 | Vault read-only, original evidence/I1/ledger/locks byte-preserved |
| U06 | CP-A–E explicit scoped local commits + separate late receipt, no reset/amend/force/push |
| U07 | Preserve historical verified preparatory passage, do not replay |
| U08 | Owner understanding/defense deferred, not self-certified |

Completion requires the whole CP-A–E brief, not only this preparation. I4+verification-I5/publication/defense are next blocks, not hidden offline completion conditions.

### CP-C scoped public per-row reason extension
Before dependent closed-output validation, H-013 adopts optional `Answer.row_reasons`:
when present it is a typed list of `null | "no_rows" | "no_grades"` with exactly the same length
as normalized `Answer.rows`. This makes a grouped all-NULL student's result visible
in the public answer without confusing NULL with zero. Scalar empty/no-grade reasons
remain the required `empty_reason` envelope; optional per-row `no_rows` preserves
the existing scalar empty proof without changing semantics.
Counts and Library may omit this optional field; omission preserves prior envelope
compatibility. This is an explicit scoped representation extension for the current
H-013 contract, not a rewrite of historical v1 examples or a semantic/model/bounds
change. Annotations only in private/internal step results were rejected because
public UI/typed answer consumers must see the reason without inferring from NULL.

### CP-C actual in-process continuation representation
The current application API is `Agent(..., session_id=None)`,
`run(question, *, request_id=None, session_id=None)` and
`resume(continuation, selection, *, request_id, session_id=None)`. The Streamlit
server creates/retains the Agent and session identity; users select only an offered
choice in that server session. This is local in-process API/UI scope, not a public
HTTP authentication protocol or durable-restart contract.

The current closed `Clarification` contains required `field`, `options`, `prompt`,
`clarification_id`, `checkpoint_id`, `session_id`, `run_id`, `schema_sha256`,
`data_sha256`, `policy_sha256`, `expires_at`. Options are closed `{value:int|string,
label:string}` records,2–100 choices; IDs retain their actual domain type rather
than historical proposed `student:1` strings. UI labels include ID for duplicate
names. `expires_at` is a server-generated Unix-seconds float (run creation+900),
not historical proposed RFC3339 text. These are explicit H-013 representation
choices; older proposed v1 envelopes/examples remain historical, not silently
rewritten or treated as implementation evidence.

`resume` receives an untrusted echo of this continuation plus typed selection and
new request ID. Echoing a session ID/checkpoint/hash is **not authority**: the Agent
compares its own retained server session, stored pending run/context, exact latest
continuation, actual saver checkpoint/interrupt, current descriptor/policy and DB
content hash before dispatch. IDs/hashes/expiry in the returned envelope are local
application diagnostics/binding values, never native OMX owner/session IDs. A user
cannot obtain ownership by submitting them. Optional method `session_id` is an
additional equality check against retained server identity, never a switch to a
client-chosen owner. Invalid selections/foreign/stale/expired echoes fail before
provider/SQL; exact accepted replay is checked against server-recorded request
payload/result and does not repeat side effects. Schema/policy/data changes expire
or terminate the stored continuation as documented by the error lane.

Only the known local UI extensions (`execution_profile`, complete `events`, typed
`step_results`) accompany the closed public run envelope; they are not provider
output schema fields. Raw/dependency rows stay tied to accepted per-step ResultSpec.
No native/runtime IDs, credentials or private host binding records belong in this
application wire or trace.

### CP-C primary error preservation
The closed current error registry preserves the existing terminal
`PROVIDER_TRANSIENT` diagnostic when `accounting_stop`/uncertain usage forbids retry
(`retryable=false`); it is not recast as `INTERNAL_CONTRACT` or permission to retry.
An actual expired active-work deadline remains `BUDGET_EXCEEDED`. Closed output
validation must not erase an already valid primary failure. These are preserved
baseline error semantics, not relaxed accounting, additional calls or new budget.

### CP-D retained-payload accounting boundary
Before accepting retention or allowing downstream dispatch, enforce the existing
**131072-byte (128KiB)** retained application-payload ceiling over the serialized
UTF-8 JSON bundle containing **current raw result + proposed completed validated dependency
results (including the current step) + step_results (raw and adapted copies) + current answer**. Counting only
completed dependency rows omits retained duplicates and is insufficient. This is a
safety repair of the accepted ceiling, not a cap increase or changed domain/budget
policy. Oversize fails closed as `RESOURCE_LIMIT` with no downstream provider/SQL call and
no partial success. Scope/counters are outside this retained-result bundle.
LangGraph checkpoint/history storage, serializer internals and transient
Python/SQLite allocations are not a hard process-memory isolation guarantee; that
production limitation remains explicit.

### CP-D SQLite integer wire/retention boundary
Untrusted `Binding.integer_value` and declared raw `integer` cells must be strict
Python integers in SQLite's signed64 range **−9223372036854775808..9223372036854775807**;
booleans are not integers. `ResultSpec.scale` must be positive and at most
9223372036854775807, while the exact domain registry still permits only its approved
scale1/100 variants. Enforce these primitive bounds before accepting provider/state
values into LangGraph checkpoint serialization or SQLite dispatch. Arbitrary Python
big integers are not supported wire values: do not allow msgpack overflow to bypass
the typed error lane, and do not mask that defect with a generic OverflowError catch.
This aligns the existing SQLite typed contract with its actual representation, not
a higher budget/limit or altered grade/count/domain meaning. Regression must send
oversized provider binding and scale values and verify safe typed rejection before
checkpoint retention/SQL; raw injected integer boundary checks are separate.
