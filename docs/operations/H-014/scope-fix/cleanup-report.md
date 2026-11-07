# Scoped behavior-lock / cleanup report

Scope: `src/universitydb/{domain,library}.py`, `tests/test_readiness_scope.py`.
No shared core, SQL, formatter, prompts, dependency or domain semantics change.

Plan written before source edits: [plan.md](plan.md). Independent parent review:
APPROVE bounded tests-first fail-closed adapter repair; no fallback/new abstraction.
Writer and plan reviewer are separate agents; final product reviewers remain separate.

Behavior lock: initial four compiled-graph controls **2 failed, 2 passed** before
source edits ([log](pre-fix-pytest.txt)). An intermediate combined run found the
Library regex branch masking `does NAME have`: **1 failed, 189 passed in 87.79s**.
Parent independently identified that overlap; explicit non-overlapping branches
repair it. This intermediate attempt is not claimed as pass. Final named-scope
regressions **14 passed in 2.84s** ([log](final-named-scope-pytest.txt)). Retained final
traces are indexed by [manifest](trace-manifest.json).

Fallback inventory: old unknown-target omission was masking scope loss; repaired
at adapter boundary. No exception swallowing, retry, fallback/global answer,
compatibility shim or alternate provider path added. Existing semantic-word guards
are bounded grammar vocabulary, not fallback execution.

Passes: dead-code and abstraction inspection no additional changes needed;
duplicate/needless-helper inspection retains existing adapter ownership; error
handling remains explicit INVALID_INPUT; reinforcement adds both unknown and known
forms plus common valid Library prose. UI/design N/A (no UI edits).

Fresh scoped ruff check/format, mypy (14 source files), compileall passed. Broad
ruff check passed; a concurrent eval test format failure was reported to its owner,
not edited here. Root runs full clean candidate verification after integration.

Remaining limitation: bounded supported English forms, not universal NLP or
real-model quality. No live/count/credentials/monetary changes. Original completed
results/locks untouched. No dependency added.

Committed failure text removes trailing whitespace/NUL bytes from overlapping console
capture; original ignored .log files remain local. The intermediate broad run used
an in-flight earlier regex; its failed status is preserved, not substituted for
final named-scope evidence. Broad final source/test ruff check/format now PASS
(34 files); clean full suite remains parent-owned.
