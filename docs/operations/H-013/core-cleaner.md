# AI SLOP CLEANUP REPORT — core bounded pass

Scope: `src/universitydb/contracts.py:materialize_refs` and directly affected
`tests/test_i2_contracts.py`. Installed ai-slop-cleaner skill read before execution.
Plan writer: separate UI/docs performer, [cleaner plan](cleaner-plan.md). Independent
plan reviewer: root, explicit [bounded APPROVE](cleaner-plan-review.md). This core
performer implements the approved slice only; it does not self-approve cleanup or
replace final independent code-reviewer/architect gates.

## Behavior lock and cleanup
CP-D verified checkpoint before cleanup: `f4611ed592f6353471ab5786eed58d601d2a246e`;
root full370pass/static evidence is separate. Added12 malformed-row-width cases
covering short/long/non-list rows on both trusted accepted-spec and lower-level
helper surfaces before deleting code. Existing real M1 corrupt-upstream tests prove
no downstream provider/SQL dispatch.

Pre-change command `pytest -q tests/test_i2_contracts.py tests/test_i3_dependencies.py::test_invalid_actual_upstream_stops_before_any_downstream_dispatch`
→43passed3.09s. Removed **only** the second identical row-width check inside the
value extraction loop; the earlier all-row width guard and full type validation
remain. No new helper, abstraction, dependency, domain/budget/accounting change or
other dead-code pass. The second value-type check was deliberately not selected.

## Fallback disposition / selected passes
- Grounded fail-safe output/trace/DB boundaries and initial-only counter defaults:
  preserved, as classified in the independently reviewed plan. No swallowing,
  successful fallback, validator removal or hidden provider retry introduced.
- Historical lower-level untyped DB/direct I1 wrappers and optional trusted-spec
  helper surface: preserved; production core still supplies accepted per-step
  specs and typed validation. No compatibility migration added.
- Dead-code pass: no proven branch selected. Duplicate removal: completed.
  Naming/UI pass: not this lane's scope. Test reinforcement:12 cases added.
- UI/design: N/A in core; separate UI owner executed its independently approved
  required-prompt boundary slice.

## Post-cleanup evidence and remaining gates
Same43-test command →43passed3.14s after deletion.
Owned-path Ruff/format, strict contracts mypy and diff check pass. No broad/heavy
suite overlap or product bounds raised. Full regression/static/final candidate
browser and fresh independent review remain root's next serialized gates; this
narrow report is not whole-goal completion or security/real-model accuracy proof.

Known continuation review questions remain explicit: TTL equality semantics,
expired initial-request replay trace visibility and bounded-context eviction versus
request-ID replay lifetime. This cleanup does not silently approve or alter them.
No live/count/credentials/ledger/I1/locks/vault/native/Git writes by this lane.
