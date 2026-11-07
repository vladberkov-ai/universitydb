# H-013 architecture/domain invariant audit — working matrix

This preserves the **seven exact invariant lines** from the accepted whole brief,
then maps implementation/test anchors. Mapping is not final proof or APPROVE/CLEAR.
Final state requires post-CP-D/cleaner serialized verification, exact candidate hashes,
actual frozen-source browser, independent reviewers and configured-gate refresh.
Historical failures/cutoffs remain in receipts; no live accuracy or native completion.

## I1: University domain semantics

Exact brief line:
> Equal graded-enrollment weights; every offering/retake; NULL distinct from zero; absent filters explicitly all including semesters; count objects distinct. Exact rational top ties before HALF_UP two decimals. Known catalog IDs/names only; ambiguous/current/conflicting/unknown scope explicit.

- Implementation: `domain.make_spec/resolve/adapt_result`, `domain_support.resolve_entities`; integer components and Fraction/Decimal top/normalization.
- Test anchors: `test_i2_domains` all16subsets/fivegroups/Q2Q3Q7Q8/top exactrational/compiledfiltermutations; `test_i2_oracle` wrongJOIN/meanofmeans; `test_i2_ui` Alex/currentsem.
- Evidence/status: CP-C311 current-source proof; final post-cleanup rerun/review pending.

## I2: Per-step specs and actual dependencies

Exact brief line:
> Every accepted step has a registered exact ResultSpec: shape, columns/types/nullability, components, grain, unit/scale. No first-row inference. Static DAG ≤3 steps, missing/cyclic/forward-invalid refs rejected before execution; materialized refs are checked typed bound values only, never SQL text. Preserve exact top selection and union de-duplication. Fail closed on truncated/oversized upstream and never silently remove empty filters.

- Implementation: `contracts.validate_dag/validate_result/materialize_refs`; `agent._action` validate_plan/bind_results/inspect_result; domain adapter exact registry selected dependency rows.
- Test anchors: `test_i2_contracts` staticrefs/types/trustedmetadata/empty; `test_i3_dependencies.py` dynamic M1 refs/sensitivity/negatives (CP-D current work, result not assumed); UI M1 F1/F2 mechanics tests passed in13-AppTest scheduled batch; fixed proposals do not replace dynamic core proof.
- Evidence/status: CP-C strict unit/core proof; CP-D actual sensitivity and final audit pending.

## I3: Bounded real continuation

Exact brief line:
> Actual in-memory LangGraph saver/interrupt, server session/run/checkpoint/clarification/schema/data/policy identity; ≤2 pauses, TTL900s. Exact replay idempotent; changed same-ID payload conflicts; invalid/stale/foreign/expired rejected before calls. Human wait excluded from active180s, other counters persist across resume; process restart expires explicitly.

- Implementation: `Agent.saver/_clarify/_restore/_execute_graph/run/resume`, retained server session/context and actual saver identity; UI retains Agent.
- Test anchors: `test_i2_continuation` realpause/replay/rejections/twopauses/counters/policy/data/requestIDs; `test_i2_ui` same-run/expiry/currentsem/Libraryforeign.
- Evidence/status: CP-C311 and actual earlier browserpause-resume; final candidate browser/review pending.

## I4: Model, budget and resource boundaries

Exact brief line:
> Exact gpt-6.1-sol plan high, SQL/repair medium, no fallback/judge. Existing ≤5 calls/run, ≤4 SQL attempts/run, plan60s/SQL45s, output32768; one repair spends shared remainder. Payload≤12000 UTF8 bytes, SQL≤8000 bytes/chars, ≤100 bindings, encoded bindings≤8192 bytes/text≤2000 bytes, results≤100 rows/64KiB, retained≤128KiB, trace≤1MiB. Never raise ceilings silently. Unknown usage/holds accounting remains terminal and unchanged.

- Implementation: `config.PROFILE/logical_operation/wire_payload`; `Agent._call/_check_deadline/_restore`; generic DB worker/result/trace limits; existing llm accounting unchanged.
- Test anchors: `test_sol_profile`, `test_bounds`, `test_provider_worker`, `test_practical_budget`, `test_i2_continuation` accountingstop/counter/recursion; `test_i2_core` fullwire.
- Evidence/status: CP-C311+static sourceproof and preserved monetary hash; full payload/count-negative audit/final rerun pending. No actual live calls authorized.

## I5: Read-only safety versus semantics

Exact brief line:
> AST allowlist + read-only SQLite authorizer + bound values/watchdog/integrity scan, unchanged DB hash. Safe SELECT is not semantic correctness: independent oracle detects wrong JOIN/aggregation. No hard memory-isolation or universal SQL claim.

- Implementation: `sql_policy.validate_sql`, adapter semantic grammar, `db.inspect/execute`, `db_worker` authorizer/progress/watchdog, adapter integrity scans.
- Test anchors: `test_db_domain`, `test_i2_domains` corruption/locked/missing/semanticmutants, `test_i2_core` sharedAST, `test_graph` unsafe/timeout; independent_oracle stdlib/tempSQLite.
- Evidence/status: CP-C311; final safety/static/invariant review pending. No hard memory sandbox or arbitrary semantic correctness claim.

## I6: Early Library same-core portability

Exact brief line:
> Library: Readers/Books/Loans, open=returned false; per-reader count includes zero, unit count scale1, separate schema/seed/descriptor/registry/result adapter/domain policy. Common core/DB safety/provider/graph/tracing/UI; both schemas exercise shared contracts early.

- Implementation: `library.Library` own schema/seed/descriptor/registry/catalog/adapter; neutral domain_support, generic Agent/DB/policy/provider/trace/UI composition.
- Test anchors: `test_library` baseline/zero/returned/FK/type/catalog/ambiguity/isolation/naturalwording; `test_i2_core` both adapters; `test_i2_ui` schema switch/countzeros; CP-D samecore tree proof pending.
- Evidence/status: Early CP-B both realDB/graph verified, CP-C regression; final same-tree hash and Library frozenbrowser pending.

## I7: Complete trace/UI and no stale results

Exact brief line:
> Trace all input/nodes/attempts/SQL/bindings/raw typed rows/adapted results/dependency binds/answer-or-error in one run, including resume. English UI reveals full trace and every step; failure/new question clears prior answer. Trace failure cannot produce untraced success.

- Implementation: `tracing.Trace.emit`; core node/provider/SQL/raw/adapted/bind/resume/requestID events and closed public outputs; `ui.render_result/main` allpanels/currentresultclear.
- Test anchors: `test_graph` fulltrace/early+latetracefail, `test_i2_continuation` requestID linkage, `test_i2_ui` reuse/staleclear/repair/allstepM1; browser harness currentrun/outcome/renderwait refinement notyetexecuted.
- Evidence/status: CP-C311 and actual prior5capture browser receipts; earlier repaint cutoff documented, final frozen allcase screenshot/trace proof pending.

## H-013/H-011 mandatory negative obligations (not dropped)
- Q1–Q12 breadth/combinedfilters/names/NULL/zero/top/mutations: exact mapped cases in
  `cp-c-coverage.json`; wrong-safe SQL stays independent oracle responsibility.
- C1–C4 real pause/foreign/stale/expiry/replay/changedpayload/twopauses/restart,
  before-choice0calls and preserved plan effects: continuation/UI/library suites.
- E1–E7 repair/exhaustion/unsafe/noexecution/providerrefusal/incomplete/malformed/
  accountingstop/DBmissinglockedtimeout/corruption/tracefailure and all caps:
  `test_graph`, `test_bounds`, providerworker, continuation, adapter/core suites.
- D1–D3 static bad refs versus runtime missing/type/truncated/oversized/empty actual
  results/downstream0calls; actual M1 F1/F2/tie/empty/partialfailure/replay/sharedbudgets:
  CP-D dynamic tests required, not replaced by fixed3queries or nodecount.
- V1/V2 typed units/grain/components/NULL/countscale and wrong-safe semantic mutants:
  contracts/domain/oracle suites; public optional per-row no_grades/no_rows reason.
- W1–W3 closedbindings/missingunusedduplicate/bool/100values/SQLbytes/textbytes/fullwire/
  usageoverrun/result/retained/trace caps: bounds/core/contracts/worker suites. No count
  endpoint/exacttokenizer or hardmemory claim.
- T1/T2/UI1 all ordered attempts/sourceSQL/rawtypedrows/adaptedbinds/answer-or-error,
  request/runlinkage, injection-as-data, no keys/private/nativeIDs, no stale UI, full
  download; final real offline browser six required classes remains CP-E.
- L1 Library1/1,readerzero/allreturned/mutation/FK/type/ambiguousname/schema-session
  isolation/samecore tree hash: actual DB+compiled graph+UI+frozenbrowser required;
  count never grade-scaled, no new dialect/librarymanagement scope.

## Cross-cutting completion and non-goals
All R01–17/U01–08 retained in current contract/matrix; R10 production explanation
maintained, R15 final publication permission/open, owner defense/understanding later.
Actual prompts distinct from read context/templates/RUEN synopses, scoped ADR rationale,
CP-A–E explicit local commits/late receipts/source identity/ledgerI1locks preservation
and final remote observation/pushnotrun remain mandatory. No live/API/count/credential
loading/spendchange/vaultwrite/remotechange/push/runtimepatch. I4+verificationI5 and
publication/defense do not block this offline goal. Native complete/strictcheckpoint
are real root-owned postconditions after final DoD, never inferred from this table.

## Supported invariant extraction annotation (root attribution)
Root's installed-source audit found a generic “Invariants” heading is not a strict
architecture/domain extraction heading. Supported `annotate_ledger` steering was
accepted to reassert the seven **unchanged** brief lines with “Architecture invariant:”
prefix. No invariant, scope or DoD was added/dropped/reworded; no child manually edited
plan/ledger/state. Root's final quality sourceArtifacts must reference nested-relative
`.omx/ultragoal/ledger.jsonl` and `.omx/ultragoal/brief.md`; proof entries use the same
normalized invariant text. Those runtime artifacts stay ignored, never product
staging. This note is attributed lifecycle evidence, not a child checkpoint/approval.

## CP-D safety-boundary clarifications (before dependent code)
Current contract/ADR012 now define the accepted131072-byte retained application
bundle across currentraw/proposedcompleteddeps/step_resultsraw+adapted/currentanswer,
not just completed rows; framework/transient allocations are not hard memory.
SQLite integer wire/raw primitives are strict signed64, scalepositive<=signed64 plus
exact registered values, checked before saver/dispatch instead of generic overflow
masking. Core targeted fixes/regressions and integrated root full verification have
separate evidence cutoffs; prior invalid retained-fault fixture and overflow findings
remain in core receipts. No cap/model/accounting/domain change follows.
