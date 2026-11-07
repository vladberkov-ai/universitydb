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
