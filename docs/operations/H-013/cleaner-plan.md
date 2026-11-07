# H-013 bounded cleaner plan — writer proposal, review pending

Author: UI/docs performer. Skill loaded: installed `ai-slop-cleaner/SKILL.md`.
This is the **plan before cleanup**, not permission to refactor or a completed
cleaner report. Root is the independent plan reviewer; source owners execute only
approved scoped changes after CP-D behavior is locked. Final code-reviewer/architect
remain independent. No nested workflow, new dependency or changed product bounds.

## Scope and evidence cutoff
Changed H-013 product files: agent/contracts/DB worker/domain/domain_support/library/
SQL policy/UI/tracing/prompts plus affected tests. Inspect actual current code, not
only pattern hits. CP-A–C history, original frozen oracle, monetary ledger/I1/locks
and source receipts remain untouched. Exact candidate identity/review cutoff is
recorded by later verification receipt; this inventory is against CP-C plus ongoing
bounded CP-D tests, not a full security/code review.

Existing behavior locks: CP-C root serialized311passed/full static and exact36-file
committed source proof at b9f2eb66e20a3148485da2af62eaa4fc9d02d0cb. Prior308pass/2fail
closed-error regression stays in evidence. CP-D dynamic dependency/portability tests
must pass before cleanup; offline script proposals are not real-model accuracy.

## Fallback inventory and classification
| Location/pattern | Classification/evidence | Proposed handling |
|---|---|---|
| `agent._execute_graph` typed boundary catches and terminal trace failure conversion; `db_worker.main` typed failure response | **Grounded fail-safe**: no success on unknown internal/trace/DB error; preserves safe diagnostic and terminal outcome. Existing graph late trace failure, malformed typed output, DB timeout and primary accounting-stop regressions lock behavior. | Preserve; no broad exception swallowing, additional retry or replacement answer. Independent final reviewers inspect primary-error preservation. |
| `AgentOutput.model_validate` final envelope guard → INTERNAL_CONTRACT | **Grounded fail-safe**, not an alternate successful path. Earlier enum omission was a real defect already fixed and retained as failure evidence. | Preserve validator and corrected registry; do not remove guard to make tests pass. |
| `agent._restore` `.get(...,0)` on fresh empty snapshot | **Grounded initialization**, not masking a broken persisted counter: nonempty snapshots require exact keys/nonnegative types/limits and session/run binding before restore. Continuation counter-corruption tests prove rejection. | Preserve; do not turn this into generalized compatibility migration/defaulting. |
| `db.execute` optional accepted spec / worker historical inference; `University.spec` and `answer(rows,scope)` wrapper | **Grounded retained lower-level/I1 API path**: production graph always supplies accepted per-step spec; direct baseline DB/domain callers use existing interface, wrapper delegates to same adapter. Tests cover both typed NULL/empty and baseline direct path. | Preserve in this stage; no speculative deletion/callsite rewrite or whole-core redesign. Document no first-row inference in accepted graph. |
| `materialize_refs(...,trusted_specs=None)` | **Grounded lower-level validation surface**: core supplies actual accepted registry specs; helper validates row widths/types even without trusted metadata. Unit tests exercise both. | Preserve parameter behavior; final invariants verify core cannot omit accepted specs. No silent fallback to untrusted production metadata. |
| `ui.provider` explicit TEST_MODE+fixture otherwise OpenAIProvider | **Grounded explicit test injection**, not fallback: normal profile never selects scripts due to errors/question text. Missing-key normal UI test proves no hidden mock. | Preserve exact gate; no live calls or credential loading for cleanup. |
| `ui.render_result` missing clarification prompt → generic prompt via `.get` | **Unnecessary masking-like display default** after a required closed Clarification field; could hide a broken producer if validation boundary were bypassed. Normal core output already requires prompt. | Candidate remove `.get` default and read required `prompt` after a regression confirms closed Clarification rejects omission. No invented prompt or new schema compatibility path. Root may defer if broadening UI error handling would be required. |
| UI missing `step_id` caption on sql_validated/sql_attempt | **Grounded presentation label**, these trace payloads intentionally have SQL/parameters while step identity remains in accepted plan/full trace; does not manufacture a DB result or bypass validation. | Preserve explanatory caption; final UI/M1 proof must show every accepted step/raw result/bind, not only this caption. |
| `.get` on optional entity aliases/choices/absent filters/optional row reasons | **Grounded explicit absence semantics**, not fallbacks from errors: absent filters mean all, empty dependency remains separate empty-set. | Preserve with all16filters/NULL/count/empty/ref tests. Do not conflate missing and empty scope. |

## Selected smallest smell-focused passes (pending independent root review)
1. **Behavior lock first.** Confirm CP-D dynamic actual-ref tests and existing strict
   result/ref/typed envelope/UI tests pass on frozen candidate. Add a focused closed
   Clarification missing-prompt rejection case if absent, before deleting UI default.
   Preserve all existing assertions and failure receipts.
2. **Dead code pass:** inventory found no proven unreachable product branch to delete.
   Report not-selected rather than inventing cleanup work.
3. **Duplicate validation pass (core owner):** `contracts.materialize_refs` currently
   checks every dependency row width/types once before its value loop, then repeats
   the identical row-width guard inside that loop. Remove only the second identical
   width check after tests confirm the first guard; retain all type/column/truncation/
   trusted-spec/limit checks. No new helper/abstraction. Optional removal of its second
   equivalent value-type check is **not selected** for this bounded pass.
4. **Naming/error-handling pass (UI owner):** if approved, replace required-prompt
   `.get` fallback with direct access after the closed-field behavior lock. No changes
   to generic fail-safe catches, provider retry, model, bounds, monetary accounting,
   public error enum or domain semantics.
5. **Test reinforcement/verification:** targeted contracts/ref/continuation/UI tests
   per selected change, then serialized full offline pytest, Ruff/format/mypy/compile/
   diff/static invariant scan, final frozen-candidate browser after cleanup. Preserve
   Library regression and actual M1 dependencies. Root schedules heavy suites one at
   a time; never raise product timeouts to suppress a failure.

## UI/design and deferred concerns
Existing compact neutral Streamlit UI has dataset/question/status and explicit
SQL/raw/adapted/trace panels. No new layout/theme/icon/dependency redesign selected.
Test-only fixed M1 proposal fixtures are UI mechanics, not the dynamic upstream
sensitivity oracle. Browser harness waits/current-run/DOM hardening is a separately
requested evidence-boundary fix, not a claim old captures equal final candidate.
Large agent/state dictionaries and possible future typed context refactor are
**deferred**: broad architecture change exceeds this bounded cleanup and needs
separate evidence, not speculative abstractions during final gates.

## Acceptance and report
Root records independent plan verdict before source cleanup. Performers report
exact files/deletions, behavior locks, fallback disposition, passes completed versus
not-selected, targeted/full static/regression/browser evidence and remaining risk.
No cleanup-complete claim until fresh post-cleanup evidence. Final independent
APPROVE/CLEAR/configured-gate and invariant verdicts are separate. Current configured
gate observation from root is `{gates:[],stage:"code-review"}`; refresh at final gate,
not falsely report a nonempty runner or treat no configured gates as no reviews.
