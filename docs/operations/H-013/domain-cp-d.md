# CP-D domain edge policy and Library portability

After CP-C `b9f2eb66e20a3148485da2af62eaa4fc9d02d0cb`, the adapter adds **per-edge**, not a blanket three-step-only, policy. Independent registered steps remain valid, including independent multistep plans and the two-step top→cohort prefix. Claimed dependent edges require exactly one preceding registered source and exact metric/grain/column/type/binding:

- `u.top_course.v1`, grain course_id, integer course_id → `u.student_ids.v1`, binding course_ids.
- `u.student_ids.v1`, integer student_id → `u.grade_mean.v1`, grain student_id, binding student_ids.

Other/extra/missing claimed refs/dependencies fail PLAN_INVALID before any SQL. Generic DAG/order/spec validation stays core-owned. Library's sole registered family has no dependent variant and rejects either claimed refs or dependencies. Actual received task and root policy clarification are in `domain-cp-d-task.txt`.

## Fresh focused evidence
Serialized targeted command in `domain-cp-d-receipt.json`: **20passed16.99s**. Includes all independent registered variants, valid prefix/fullM1,12invalidfamily/refplans (one plan call, zero SQL), five frozen real-DB actual-result chains F1/F2/tie/empty/no_grades, four compiled Library baseline/zero/returned/all-returned mutations, and identical integrated core bytes across University and Library with foreign-adapter checkpoint rejection.

Frozen M1 expected/actual: F1 top[2]→cohort[1]→95.00; F2 top[1]→cohort[1,2,3]→95.00/80.00/50.00; tie top[1,2]→union[1,2,3]→90.00/90.00/null; empty/no-grades→emptyset, never removing the dependent filter. Core peer separately owns dynamic scripted provider/SQL/history/trace proof; this domain chain does not replace that required compiled-graph proof.

First targeted attempt had12failures because negative tests used shorthand “top course S1”, conservatively parsed as unknown course identity before planning. Correcting test input to accepted full M1 phrasing “top course **in S1**” reached the static validation and all12passed. Resolver policy was not loosened. This is an explicit bounded syntax/NL limitation; offline scripted evidence is not universal or real-model NL→SQL accuracy.

`domain-cp-d-portability-pre-retained-fix.json` preserves the actual passing test's integrated core file hashes, University83.33/Library1,1 and unchanged tree under switching. It is explicitly **before** the last core retained-payload safety fix. Root's final full/capture after that fix/cleaner must establish final tree identity; this earlier hash is not relabeled as final.

Four additional compiled negative tests (Library FK/flag/storage corruption and changing an existing paused agent's domain/schema) were added immediately before root freeze; static checks passed, execution **not-run here**, delegated to root's one serialized full run. All owned source/tests now frozen. Ruff/format4files, mypy2sources, scoped diff-check passed. No new dependencies, limit increases, provider/count/live calls, credentials, monetary/workflow/Git changes in this lane.
