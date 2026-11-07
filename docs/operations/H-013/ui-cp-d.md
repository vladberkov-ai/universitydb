# H-013 CP-D UI dependency visibility receipt

[Actual task/follow-ups](ui-task.txt). No core/domain implementation edits by this
lane. Root owns integration/workflow and actual lifecycle. CP-D UI proposals are
explicit offline fixtures; **dynamic actual-ref sensitivity proof belongs to core's
M1 tests/capture**, not the fixed fixture helper.

## Implemented/verified UI scope
Added shared test-only M1 proposal builder and two actual Streamlit AppTests, F1/F2.
Real compiled graph/SQLite produce three step outcomes (top/cohort/means); UI exposes
selected course IDs, union student IDs, all raw/adapted results, actual bound SQL and
same-run final means. F1→top[2]/cohort[1]/95.00; F2 actual DB insert(3,2,5000)→top[1]/
cohort[1,2,3]/95.00,80.00,50.00. Provider supplies4 planned proposals; no fabricated DB
result and no UI branch on M1/domain table names. Fixed proposals are UI mechanics,
not proof that downstream SQL generation responds dynamically; core's separate
provider reads actual resolved refs and proves that obligation.

Scheduled isolated command:
`env -u OPENAI_API_KEY UV_CACHE_DIR=/tmp/universitydb-h013-uv-cache UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_ui.py tests/test_i2_ui.py --basetemp=/tmp/h013-cpd-ui-targeted`
→ **exit0,13 passed in11.93s**. This includes all prior clarification/session/expiry/
Library/zero/repair/missingDB/stale-clear cases. Ruff on own UI/tests/browser helpers,
format-check4 UI/test files, UI mypy and diff-check → pass. No overlap with core/domain
heavy slots, no actual runtime/ledger mutation. All own product/tests frozen after
checks; root serialized full regression/static must verify the integrated candidate.

## Final browser harness boundary repair (not yet executed)
The harness now waits for the current Streamlit render to finish and validates
trace input question, unique new run (except same-run pause/resume), sequence and
terminal status/actual typed answer before taking screenshots. For errors it requires
DB-not-executed text and absence of old sum rows, avoiding a premature capture while
Streamlit replaces prior lower panels. Grouped M1 alert is a row-count summary;
95.00 is checked in actual typed answer/trace, not invented in the alert. Focused
SQL/DB/adapted/trace screenshots remain required. No final browser launch occurred
here; CP-E frozen-source allcases after cleaner/reverification is still mandatory.
Earlier actual CP-C captures/limitations remain unchanged.

No cleanup performed before CP-D commit: [bounded cleaner plan](cleaner-plan.md)
was written first and independently [approved](cleaner-plan-review.md), with source
cleanup scheduled afterwards. No live/count/API, credentials, new dependencies,
monetary history/cap/hold change, native state/IDs, vault write, remote/push or final
goal-completion claim by this lane.
