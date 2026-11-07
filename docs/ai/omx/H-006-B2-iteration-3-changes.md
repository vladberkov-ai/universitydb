# Small revision after iteration 2

Planner, 2026-11-07. Status proposed; not approval/closeout. Full completed Architect2/Critic2 read; both iterate with a single residual blocker B2-R1. The remaining previously tested solutions were not changed; changes-from-iteration-1.md is saved byte-by-byte as correction history.

| Finding | Edit | Verification / disposition |
|---|---|---|
| B2-R1: row-level COALESCE does not normalize empty scalar SUM | normative contracts sum → aggregate-level COALESCE(SUM(grade_units),0), integer0; nonnull ResultSpec saved; three complete typed raw DBResult→Answer examples Z1/Z2/Z3 | [0,0,0]→null/no_rows;[0,0,1]→null/no_grades;[0,1,1]→"0.00"/null. Documentary JSON/type/consistency checks done; addressed pending new independent reviews |
| Consistency oracle/test scope | S10/N1–N3/V1 refer to exact raw components; DB-Z separately actual SQLite raw-output integration, UNIT-Z separately pure adapter normalization | Both future checks are required and do not replace each other; invalid nullable raw sum→RESULT_CONTRACT_INVALID. No product tests were performed |
| Decision traceability | ADR-OMX-006 clarifies aggregate normalization and DB-Z/UNIT-Z | Minimal changes to the existing proposed boundary, without nullable raw schema expansion/new dependency |

The alternative nullable raw sum + normalization to typed validation is rejected as unnecessary complication: outer COALESCE preserves the current strict ResultSpec and bounds. Scalar row_count1 with enrollment_count0 is clearly different from the original rows; grouped missing rows are not automatically promised. Units/counts/rounding/NULL policies are preserved.

Iteration1/2 and reviews immutable. Bundle includes all14constituents in full bytes, manifest raw SHA256; This is not an OMX domain-separated lifecycle digest. Mapping of six main documents/ADR former; this file→docs/ai/omx/H-006-B2-iteration-3-changes.md after supported closeout. New research, SQL probe, executable schema/seed, application/tests/UI/runtime prompts, dependencies, paid calls were not executed. The next step is separate Architect3→Critic3, not execution authorization.
