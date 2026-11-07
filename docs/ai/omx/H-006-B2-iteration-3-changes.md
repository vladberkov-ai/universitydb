# Малая revision после iteration 2

Planner, 2026-11-07. Status proposed; не approval/closeout. Полные завершённые Architect2/Critic2 прочитаны; оба iterate с единственным остаточным blocker B2-R1. Остальные ранее проверенные решения не менялись; changes-from-iteration-1.md сохранён байт-в-байт как история коррекции.

| Finding | Edit | Verification / disposition |
|---|---|---|
| B2-R1: row-level COALESCE не нормализует пустой scalar SUM | contracts normative sum → aggregate-level COALESCE(SUM(grade_units),0), integer0; nonnull ResultSpec сохранён; три полных typed raw DBResult→Answer examples Z1/Z2/Z3 | [0,0,0]→null/no_rows;[0,0,1]→null/no_grades;[0,1,1]→"0.00"/null. Documentary JSON/type/consistency checks выполнены; addressed pending new independent reviews |
| Согласованность oracle/test scope | S10/N1–N3/V1 ссылаются на exact raw components; DB-Z отдельно actual SQLite raw-output integration, UNIT-Z отдельно pure adapter normalization | Оба future checks обязательны, не подменяют друг друга; invalid nullable raw sum→RESULT_CONTRACT_INVALID. Ни один product test не выполнялся |
| Decision traceability | ADR-OMX-006 уточняет aggregate normalization и DB-Z/UNIT-Z | Минимальная правка существующей proposed boundary, без nullable raw schema expansion/new dependency |

Альтернатива nullable raw sum + normalization до typed validation отвергнута как лишнее усложнение: outer COALESCE сохраняет текущий strict ResultSpec и границы. Scalar row_count1 при enrollment_count0 явно различён с исходными rows; grouped missing rows не обещаны автоматически. Units/counts/rounding/NULL политики сохранены.

Iteration1/2 и reviews immutable. Bundle включает все14constituents полными bytes, manifest raw SHA256; это не OMX domain-separated lifecycle digest. Mapping шести основных documents/ADR прежний; этот файл→docs/ai/omx/H-006-B2-iteration-3-changes.md после supported closeout. Новый research, SQL probe, executable schema/seed, application/tests/UI/runtime prompts, dependencies, paid calls не выполнялись. Следующий шаг — отдельные Architect3→Critic3, не execution authorization.
