# Domain CP-C continuation and breadth evidence

Authority: root CP-C authorization after verified CP-B `f522fb4f3b0c56fccd5b8dd404960fef8f88d532`; actual received follow-up saved separately in `domain-cp-c-task.txt`. Same owned adapters/helpers/tests; core/UI/lifecycle/Git/ledger untouched by this lane.

## Changes and policy
- Deterministic `clarification_options(field,catalog)` on both adapters grounds provider-requested clarification in actual catalog identities; University also exposes registered count-object choices. Unknown requested fields fail closed, never accept model-provided options.
- ID/name conflicts are terminal `INVALID_INPUT` before provider/SQL, rather than offering an impossible choice. Unknown names (explicit and supported natural shorthand), nonexistent/malformed IDs and unsupported entity filters also fail before dispatch; no silent filter removal. Invalid choices use accepted `INVALID_SELECTION`; unknown input stays accepted enum `INVALID_INPUT` with explicit reason (CP-B historical intermediate codes are not rewritten).
- Library has an explicit limited open/unreturned-loan-count intent gate. University grades/write intent, unrelated Library metrics and returned/all-loan requests fail, rather than silently returning open counts. Natural mandatory UI wording “How many open loans does each reader have?” is tested; grammatical words do not become invented reader names. Symmetric University unsupported-domain inputs fail.
- Both owned catalog/integrity scans use a shared read-only URI connection, timeout0.5s, explicit sqlite.Error→DB_UNAVAILABLE while propagating domain Failure unchanged; connections close deterministically. Catalog queries have LIMIT1001 and reject total>1000 schema entities before constructing name dictionaries. This is bounded demo support, not hard memory isolation.

## Expected/actual coverage
- Q1/Q2/Q3/Q12: all16filter subsets through real compiled graph + scripted provider + SQLite for exact mean and all3counts; frozen raw/mean/distinct expectations. Bea four-filter80.00 and student1variant90.00. Named Bea/DB/Kim/S1 and consistent AlexID produce same expected results.
- Q4/Q12: each of five grouped means through compiled graph before/after independently frozen grade mutation; S1 course groups83.33/100.00/null. Each of four optional filters independently changes expected compiled-graph aggregate after mutation. All16×all5group real-DB combinations retained from CP-B.
- Q5/Q6: combined counts labeled enrollment/graded/distinct, and real compiled JOIN listing with correct student/course/teacher labels and nullable grade.
- Q7/Q8: student1/C1 all80.00 vs S2 70.00; empty no_rows, NULL-only no_grades, true gradezero0.00 and countzero remain distinct at DB/graph boundaries.
- Q9: compiled S1 topC2, mutated exact tiesC1/C2 both90.00; rounded-equal but exact-unequal250/3 versus83.33 selects onlyC1. Adapter raw candidates and selected dependency rows remain distinct.
- Q10/Q11: real same-run checkpoint/resume Alex→student3null/no_grades, currentsemester→S1 87.50, vaguecount→explicit object8/6/4; provider calls0 before selection and2after. Core continuation suite separately tests replay/session/checkpoint/expiry/shared counters. Library duplicateAda→reader3zero, same-run resume/replay and0extra calls; schema isolation/regression retained.
- Negative: malformed/unknown/conflicting/unsupported input0calls/0SQL, closed spec/types/counts/range/duplicates, catalog>1000 and missing/locked owned reads. Library FK/type/range/returned mutations and same-core smoke retained.

## Fresh validation and honest iteration history
All product tests use temporary DB/runtime/trace state and offline scripted provider, not real-model NL→SQL accuracy. No credentials/live/count calls or monetary changes.
- Initial compiled breadth run overlapped core's intermediate Agent write and produced37AttributeError failures (`Agent.run` temporarily absent),51passes. This is recorded as failed/not acceptance; reruns after stabilization below supersede it.
- Focused compiled filters/names/clarification/unknown/Library regression:19passed4.59s; unsupported input11passed1.10s.
- Complete first stable domain/Library/oracle/continuation suite:127passed70.53s.
- Catalog bounded/missing reads plus S1groups/rounded-nontie graph:3passed1.03s.
- Accepted-enum aligned `.venv/bin/pytest -q tests/test_i2_domains.py tests/test_library.py tests/test_i2_oracle.py tests/test_i2_core.py tests/test_i2_continuation.py`:143passed66.25s before final UI-wording/unsupported-filter regressions were added.
- Focused final mandatory Library wording/unknown readers/locked owned reads:6passed2.90s.
- `.venv/bin/ruff check` owned adapters/helpers/tests, `ruff format`, `mypy` three source files and scoped `git diff --check`:passed. Final complete rerun recorded below when finished.

CP-D actual M1 end-to-end sensitivity is deliberately not claimed here; root owns its subsequent authorization/checkpoint. Root owns full UI/browser evidence and final integrated static/full regression/checkpoint receipts.

## Final freeze and serialized integration handoff
Further final fixes: explicit unsupported entity-filter assignments fail rather than disappearing; missing ID values fail. Library natural wording and unknown reader forms retain accepted `INVALID_INPUT` external enum with explicit reason. Both adapters' final owned startup/catalog connection tests cover actual exclusive lock and missing files, bounded catalog overflow.

- Fresh final small pure-domain/unit/catalog/result batch: `.venv/bin/pytest -q tests/test_i2_domains.py tests/test_library.py -k 'resolve_catalog or exact_rational or invalid_result or spec_registry or owned_reads or catalog_bound or provider_clarification_options_grounded or adapter_clarification_options_are_catalog_grounded or null_and_boolean_results_rejected'` -> **19passed,103deselected in2.44s**.
- Narrow compiled empty/no_grades/means rerun `test_compiled_graph_q2_q7_q8_mean_states` -> **5passed1.39s**.
- Final Ruff check and format-check six owned source/test files, mypy three source files, scoped diff-check -> **passed**.
- Final broad rerun overlapped other heavy suites/core public-contract edits and slowed drastically, producing eight failures in partial output. Root ordered serialization; this lane terminated its exact broad session before a complete failure summary, preserving `/tmp/h013-domain-cpc-freeze.txt` rather than claiming pass. A narrow unknown/resolution batch passed15tests137.22s during the same stalled interval. Core independently observed an actual3s worker watchdog failure; this lane does not infer all eight causes without traces. Product limits remain unchanged. Earlier full143pass is a prior cutoff, not final-current proof.
- All owned product sources/tests frozen now; no outstanding test processes in this lane. Root's single serialized integrated full regression is required before CP-C commit. No M1 CP-D completion claimed; no new provider/SQL call bounds or dependencies.
