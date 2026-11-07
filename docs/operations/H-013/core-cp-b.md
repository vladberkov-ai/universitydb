# H-013 CP-B core implementation receipt

Scope: core executor, after root's verified CP-A `13411c8366d04b5300bbed5e4fbb7f22eb296cdb`. No lifecycle/Git/monetary/vault mutation by this lane. [Actual child task](core-task.txt); H013/brief/contract/ADR012/checkpoint reference read as context.

## Implemented bounded foundation
- Closed provider PlanProposal allows at most three static DAG steps; unique identities, exact declared dependency references, earlier registered columns/types and nonnullable reference values validated separately from actual runtime materialization.
- Actual dependency rows are checked, bounded and deduplicated; empty sets short-circuit without downstream provider or SQL calls. Selected adapted rows and original raw rows remain separately traceable.
- Real compiled graph iterates accepted steps, uses each accepted ResultSpec, traces bindings/raw/adapted results and retains at most128KiB step payload. Adapter registry/semantic policy remains outside core.
- SQLite optional accepted ResultSpec preserves declared types for NULL and empty results; values are checked against the accepted schema independently of worker's first-row inference used only by historical untyped callers.
- Generic read-only SELECT AST/table/function/placeholder boundary supplements adapter semantic SQL policy and SQLite authorizer. Full wire payload/schema/prompt/framing size gate applies to scripted and live providers, retaining12000 ceiling and existing call/token/time/SQL/repair limits.
- University AND Library real SQLite/compiled graph smoke plus wrong-adapter plan rejection use the same core; no core domain-table branches.

## Fresh checks
All commands use `UV_CACHE_DIR=/tmp/h013-uv-cache uv run --locked` and `login:false`, no credentials or network.
- `pytest -q tests/test_i2_core.py tests/test_i2_contracts.py`:19 passed (real DB+compiled graph both adapters, cross-schema spec isolation, full-wire rejection, strict refs/types/NULL/empty, AST negatives).
- Targeted baseline-inclusive batch before the final domain fixes:88 total,86 passed,2 domain regressions reported to owning lane (unsafe question pre-provider rejection; direct adapter UTF-8 SQL byte bound). A subsequent19-test fresh core run passes; root runs final integrated regression after all lanes freeze.
- `ruff check` on owned core modules and tests passed; `mypy` on five owned core modules passed before the last typed-row validation-only adjustment; root runs final full-tree checks. `git diff --check` passed.
- Earlier default uv cache attempt failed EROFS before tests; no bypass, switched writable temporary cache. One earlier44-test run had43pass/one3s worker watchdog timeout during host/tool slowdown; ceiling not raised, later real DB/graph tests finish normally.

## Not yet completion
CP-C real checkpoint/interrupt continuation and its rejection/bounds/idempotency tests remain next; CP-D M1 sensitivity and CP-E full UI/browser/reviews remain root-owned future checkpoint work. Current ambiguous-name test explicitly replaces historical I1 rejection with CLARIFICATION_REQUIRED/no calls; CP-C will require real pause/resume. Offline scripted-provider evidence is not real-model NL-to-SQL accuracy. No live/count/push, production readiness or final goal-completion claim.

Owned product paths: `agent.py`, `contracts.py`, `db.py`, `db_worker.py`, `sql_policy.py`, `prompts/plan.txt`, `prompts/sql.txt`; tests `test_i2_contracts.py`, `test_i2_core.py`, focused accepted-semantic updates in `test_graph.py`. No changes to other lanes' adapter/UI files. Root/integrator owns local commit and final tested SHA.

## CP-B final seam audit and fresh freeze evidence
Root review identified and this lane fixed strict metadata/reference seams before freeze: reference values sorted after typed deduplication; truncated/oversized dependencies fail RESULT_TOO_LARGE, missing/type/spec/count failures DEPENDENCY_INVALID; trusted accepted predecessor specs supplied separately from runtime copied metadata. All raw DBResults carry exact accepted spec/step identity, declared columns, strict integer row_count (bool rejected) and nonnegative integer elapsed_ms. Empty dependency uses elapsed_ms0 and separate explicit trace event, no fabricated extra DBResult property. `bind_results` is the contract node name. Added direct corruption regressions.

Final targeted command `pytest -q tests/test_i2_contracts.py tests/test_i2_core.py tests/test_graph.py tests/test_bounds.py tests/test_db_domain.py` → **95 passed in6.61s** after adapter-owner fixes. Owned-path Ruff → pass; five-core-file strict mypy → pass; `git diff --check` → pass. No timeout ceiling changed. Both adapters use real DB and compiled graph; tests are scripted transport only. Product/test paths frozen for CP-B integration commit; CP-C remains next, not completed here.
