# H-014 final invariant audit — exact candidate983 technical PASS

Exact tested candidate under final verification: `98345ad6ce5757c71d44ba1ce59a683d46e0d910`.
Later docs-only `ac998a9b411b6d15b7d4a555523e653c1f124197` does not mean a different
full product test. Final full clean/browser technical evidence **PASS**:485tests80.36s/all7commands0/
157oracle/28clean+53browserhashes, visible typed raw/adapted UI with nohelp/noNone.
Independent final verdicts and native/strict are **pending**.
This audit copies the seven original obligations unchanged, then maps actual source,
tests and bounded evidence. Read-only workflow brief is not modified by this lane.
Accepted ADR006/Sol profile stays unchanged; offline providers are not model accuracy.

## I01 — original obligation

> Equal graded-enrollment weights; every offering/retake; NULL distinct from zero; absent filters explicitly all including semesters; count objects distinct. Exact rational top ties before HALF_UP two decimals. Known catalog IDs/names only; ambiguous/current/conflicting/unknown scope explicit.

- Source anchors: `src/universitydb/domain.py; domain_support.py; resources/schema.sql`.
- Tests: `tests/test_i2_domains.py (all16filter subsets/five groups/counts), test_i2_oracle.py, test_readiness_scope.py`.
- Evidence/cutoff: 157oracle and group/top/M1 artifacts in clean-run-final-attempt2; unknown/known targets39focusedPASS. Exact983full485PASS,157oracle.
- Independent final verdict: pending; original findings retained, not waived.

## I02 — original obligation

> Every accepted step has a registered exact ResultSpec: shape, columns/types/nullability, components, grain, unit/scale. No first-row inference. Static DAG ≤3 steps, missing/cyclic/forward-invalid refs rejected before execution; materialized refs are checked typed bound values only, never SQL text. Preserve exact top selection and union de-duplication. Fail closed on truncated/oversized upstream and never silently remove empty filters.

- Source anchors: `src/universitydb/contracts.py; agent.py typed reference materialization; domain.py`.
- Tests: `test_i2_contracts.py; test_i3_dependencies.py::test_m1_actual_dependency_sensitivity, test_invalid_actual_upstream_stops_before_any_downstream_dispatch`.
- Evidence/cutoff: c631M1 F1/F2/tie/empty/oversize/partial failures; fresh983full/M1 actual reference proofPASS.
- Independent final verdict: pending; original findings retained, not waived.

## I03 — original obligation

> Actual in-memory LangGraph saver/interrupt, server session/run/checkpoint/clarification/schema/data/policy identity; ≤2 pauses, TTL900s. Exact replay idempotent; changed same-ID payload conflicts; invalid/stale/foreign/expired rejected before calls. Human wait excluded from active180s, other counters persist across resume; process restart expires explicitly.

- Source anchors: `src/universitydb/agent.py InMemorySaver/interrupt/context registry`.
- Tests: `test_i2_continuation.py::test_real_pause_resume_and_replay, test_resume_rejections_before_provider, test_two_pauses_wait_excluded_and_third_pause_terminal; test_review_repairs.py`.
- Evidence/cutoff: c631same-run resume/replay traces preserved; fresh983full/browserPASS.
- Independent final verdict: pending; original findings retained, not waived.

## I04 — original obligation

> Exact gpt-6.1-sol plan high, SQL/repair medium, no fallback/judge. Existing ≤5 calls/run, ≤4 SQL attempts/run, plan60s/SQL45s, output32768; one repair spends shared remainder. Payload≤12000 UTF8 bytes, SQL≤8000 bytes/chars, ≤100 bindings, encoded bindings≤8192 bytes/text≤2000 bytes, results≤100 rows/64KiB, retained≤128KiB, trace≤1MiB. Never raise ceilings silently. Unknown usage/holds accounting remains terminal and unchanged.

- Source anchors: `src/universitydb/config.py; llm.py; agent.py provider attempt accounting`.
- Tests: `test_bounds.py; test_practical_budget.py; test_provider_worker.py; test_i3_dependencies.py::test_transient_and_repair_share_remaining_calls`.
- Evidence/cutoff: Frozen source unchanged except two UI branches from c631. Full request practical estimate is NOT strict token/invoice proof; original monetary ledger untouched.983full485/staticPASS.
- Independent final verdict: pending; original findings retained, not waived.

## I05 — original obligation

> AST allowlist + read-only SQLite authorizer + bound values/watchdog/integrity scan, unchanged DB hash. Safe SELECT is not semantic correctness: independent oracle detects wrong JOIN/aggregation. No hard memory-isolation or universal SQL claim.

- Source anchors: `src/universitydb/sql_policy.py; db.py; db_worker.py`.
- Tests: `test_db_domain.py; test_bounds.py; test_review_repairs.py`.
- Evidence/cutoff: c631bothDBinit/safe repeat hash, corruption/DELETE-only/read-only regressions; independent oracle157;983full485/staticPASS.
- Independent final verdict: pending; original findings retained, not waived.

## I06 — original obligation

> Library: Readers/Books/Loans, open=returned false; per-reader count includes zero, unit count scale1, separate schema/seed/descriptor/registry/result adapter/domain policy. Common core/DB safety/provider/graph/tracing/UI; both schemas exercise shared contracts early.

- Source anchors: `src/universitydb/library.py; resources/library/schema.sql and seed.sql; shared core modules`.
- Tests: `test_library.py::test_library_baseline_zero_returned_mutations_and_scale; test_i2_ui.py::test_dataset_switch_clears_answer_and_uses_separate_db`.
- Evidence/cutoff: c631portability-proof and LibraryAda1/Bob1;983fresh browserPASS typedraw/zero/unit.
- Independent final verdict: pending; original findings retained, not waived.

## I07 — original obligation

> Trace all input/nodes/attempts/SQL/bindings/raw typed rows/adapted results/dependency binds/answer-or-error in one run, including resume. English UI reveals full trace and every step; failure/new question clears prior answer. Trace failure cannot produce untraced success.

- Source anchors: `src/universitydb/tracing.py; agent.py; ui.py explicit rendering branches`.
- Tests: `test_readiness_ui_magic.py; test_ui.py; test_i2_ui.py::test_m1_ui_all_actual_step_rows_bindings_and_final_means`.
- Evidence/cutoff: c631visualBLOCK despite mechanical capturePASS; actual magic3pre-fail then15serializedPASS6.00s after983fix. New actual983browser/nohelp/noNone/typedrows assertionsPASS.
- Independent final verdict: pending; original findings retained, not waived.

## Whole requirement coverage and remaining authority

[Full R/U mapping](../../reports/H-014-readiness-offline.md#requirement-and-invariant-audit)
covers R01/02/11 data/init; R03graph; R04filters/aggregates/groups/ties/M1; R05Library;
R06trace/UI; R07clarification/errors/safety/repair; R08multilevel checks; R09modules;
R10production discussion; R12/13/14tracked code/tests/decisions/examples. R15new
publication awaits authority; R16/17owner explanation/defense deferred; U02exact
deadline unknown. U01actual task/redaction/RUoriginal+ENreader translation and
bounded child coverage, U03supported separate workflow, U04ADR rationale, U05vault/
original preservation, U06explicit local checkpoints are separately evidenced.
No requirement is dropped because an extractor recognizes only seven lines.

## Review blockers and no masking

Initial unknown-name scope loss → actual failing tests → two adapter guards; then
group/exclusion/Library quantifier regression and intermediate bare-name loss →
contextual registered grammar39tests; then actual c631visualBLOCK → actual magic
3failure lock → two explicit UI branches plus browser assertions. c631482PASS/
157oracle/browser screenshots do not waive that visual blocker. Preserve all failed
attempts and initial/interim reviewer findings. Exact983full485/static157oracle and strengthened actual browser now close the
technical finding; independent final review/native completion remain pending.

No live/count/access/credential operation, spending migration, judge/fallback,
accepted-semantics change, new dependency, global magic override, screenshot masking
or raised time/call/token limit. Proposed live protocol threshold44/48 and≥7/8
remains unaccepted, all48not-run; oracle answers excluded from model payloads.

## Final technical receipt index
[Clean full summary](clean-run-final-attempt3/final-summary.json),
[actual browser](browser/final-983-attempt1/browser-receipt.json),
[current exact preservation/source/remote](final-983-preservation-remote.json).
All45source/test/resource/harness/config hashes match983Git blobs,263H013 historical
files/22vault inputs/10preservation targets unchanged or explicitly restored under
disclosed orchestration recovery.17eval package hashes and28clean/53browser hashes
verified. Owned server/browser stopped, temporary ledger absent, disposable tracked
checkout clean. These technical receipts do not invent final reviewer approval.

Independent architect final **CLEAR**, zero unresolved blockers: [actual receipt](reviews/final-architect.json). Final code-reviewer/native remain pending; no reused H013 verdict.
