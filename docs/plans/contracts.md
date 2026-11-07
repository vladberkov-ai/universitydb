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
