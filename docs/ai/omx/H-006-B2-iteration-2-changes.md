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
