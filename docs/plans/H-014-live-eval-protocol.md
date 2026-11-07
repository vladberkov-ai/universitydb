# H-014 proposed real-model evaluation protocol v1

**Draft for one future owner decision; no live authority and no real-model results.**
Offline readiness and deterministic/injected evidence are a separate ledger from this
future real-model NL→SQL evaluation. Neither substitutes for the other. No model,
count/access probe, credential loading or monetary mutation is implemented by the
harness. Exact model remains `gpt-6.1-sol`, plan high, SQL/repair medium; no fallback,
LLM judge, best-of selection or accepted-architecture reapproval.

## Frozen candidate and exposure

[Candidate questions and independent oracle](../operations/H-014/eval/heldout-candidate-v1.json)
contains 24 cases, four per category: aggregates/NULL, JOIN/filters,
dependencies/ties, clarification, empty/negative data and Library. Two repeats
produce **48 conversations**, in fixed repeat-major then file case order: A01–A04,
J01–J04,D01–D04,C01–C04,E01–E04,L01–L04 for repeat1, then repeat2.
[Planned records](../operations/H-014/eval/planned-runs-v1.json) are all not-run;
no candidate executions or fake accuracy report is produced.

Candidate is authored and exposed to this implementation team's harness author and
reviewers, **not an untouched holdout**. Root integration specifically inspected
E01–E04/L01–L04 and scorer; fix lane reports no heldout/eval read and its independent
audit finding predates authoring. Some deliberately natural question forms (for example “course ID 2”) may not match
current lexical scope hints; record any resulting live failure, do not silently
rewrite questions or tune the product against this candidate. Product prompt/logic tuning against it is
forbidden. Its semantic expectations derive from accepted ADR006 and the earlier
independent frozen H013 oracle, not the production formatter. Independent reviewer
may prepare a sealed replacement before approval; that requires a version, hash,
exposure declaration and prospective threshold, never overwriting this candidate.
Dev/synthetic scorer fixtures are separate in `dev-v1.json`. Scorer tests consume
only this dev fixture, never run heldout against the product.

Resources (schema/seed), runtime prompts and oracle basis are pinned by SHA256 in
the package. Each local fixture has a canonical JSON descriptor SHA256 (UTF8,
keys sorted, compact separators, excludes its own sha256), explicit schema/seed
and mutation SQL. These fixture mutations are **trusted offline setup only**, not
provider SQL permissions. Rebuild a fresh DELETE-mode DB per conversation; never
copy original runtime, ledger or credentials. Record the resulting DB file SHA256
and row census before each future run. Deterministic fixture identity is descriptor
plus schema/seed hashes, not an assumption that SQLite files reproduce bytewise.

## Separation and execution contract

`tools/eval/harness.py` is stdlib-only offline export/plan/scoring. It imports no
product/provider and performs no network I/O. Run from repo root:

```bash
.venv/bin/python tools/eval/harness.py plan docs/operations/H-014/eval/heldout-candidate-v1.json
.venv/bin/python tools/eval/harness.py export docs/operations/H-014/eval/heldout-candidate-v1.json
# Only after later separately approved collection, use --records observations.json:
.venv/bin/python tools/eval/harness.py score docs/operations/H-014/eval/heldout-candidate-v1.json --records observations.json
```

Export allowlists case/run IDs, repeat, domain, local fixture name, question and
user selection sequence. **Only question text and, at the appropriate interrupt,
one selection go into the product conversation.** Do not send case IDs, fixture
names/descriptors, expected scope/values/choices or the package to any model. A
future live collector must consume the exported conversation-only list and local
setup, without opening the oracle file; scorer runs afterwards in a separate
process with the oracle. This harness deliberately contains no live collector.
The live activation implementation/configuration is a future approval prerequisite,
not hidden dispatch authority in this offline package.

Before collecting, pin this package/scorer hashes, exact candidate commit, dirty
status, product+runtime-prompt hashes, schema/seed/DB identity, model/efforts/tier,
policy/rate version, ordered48run IDs, proposed threshold and observer instructions
in a signed-off registration receipt. Current baseline source SHA is recorded by
root's final candidate evidence, not inferred from a docs SHA. Refuse drift after
freeze. Resume an interrupted experiment only for untouched not-run records;
started-but-unknown records remain denominator failures/uncertain charges, not
silently rerun. A separately approved repetition is a new version, not replacement.

## Independent observation and exact rubric

For each terminal run retain original full JSONL trace (path and SHA256), public
answer/error and per-step raw/spec/adapted rows/bindings, any clarification choices
and selection, provider attempt count and usage/cost facts. A reviewer produces a
closed `observed` record with exactly `scope, columns, types, rows, empty_reason,
choices, dependencies`; JSON types are strict (`bool`≠integer), decimals exact
two-place strings. Oracle ordering is numeric/text ID ascending; J04 sorts by
student_id then offering_id. A collector may sort rows and project explicitly
requested columns, but must preserve duplicates, NULLs, all exact ties and every
requested scalar component. No rounding away numerical errors or guessed columns.
Means are equal weighted graded enrollments, all offerings; absent filters include
all semesters. Decimal NULL, `no_grades`, `no_rows` and numeric0 are distinct.

Observation `scope` is the specified filter object (empty object explicitly means
all dimensions/all semesters), not a prose string; selected count object is retained.
`choices` is the ordered clarification field/value-set sequence (labels need not
match wording). Offered option sets must equal oracle sets; ordering inside values
is normalized by typed ID, never omit alternatives. Prechoice generated SQL must
be zero; startup catalog reads are not generated SQL. Same server session/run and
trace must survive selection. Alex choices1/3 and current semester S1/S2 are
mandatory. Count choices use actual registry IDs. D03/D04 dependencies must be
read from actual selected upstream rows and materialized typed bindings, never
inferred from final answers. Compare top IDs and union cohort IDs as well as final
values. For empty listing E03 require a typed schema despite no rows.

Each completed record includes outcome `success|failure|timeout|refusal|invalid|infra_abort`,
calls integer0..5, original trace artifact path/hash and six strict boolean checks:
`safe`, `private`, `trace_complete`, `scope_explicit`, `behavior_complete`,
`nonfabricated`.
Independent reviewer, not a model, verifies checks from original evidence. Hash
verification proves artifact retention, not semantic truth of reviewer annotations.
Safety includes zero writes/unsafe execution, unchanged fixture DB after run;
privacy includes no credentials/secrets/oracle leakage. Behavior includes all
applicable mandatory contracts (no prechoice SQL, correct session continuation,
actual M1 binds, NULL/zero/ties, error lane and no fabricated/stale success).
A recorded success passes only when every check and the full typed oracle match.
No partial credit, SQL-string matching or production-formatter oracle.

Every run requires exactly one record: `planned|not-run|started|completed`.
Noncompleted records contain only run_id/status; completed records use the closed
schema above, additionally `trace_path` and `trace_sha256`. Missing/duplicate/extra
IDs, invalid types/status/calls/hash/artifact or source/fixture drift fail scoring
closed, rather than dropping records. Failures/timeouts/refusals/invalid/abort
remain in denominator48. Internal repair consumes the same conversation/call cap,
not a free retry. Missing trace is an invalid record, never pass. Infrastructure
abort is explicitly retained; unresolved started/not-run forbids acceptance.

## Proposed acceptance, not approved

Draft thresholds: **≥44/48 overall AND ≥7/8 in each category**, zero unsafe
executions/privacy leaks/fabricated successes and **100% mandatory behavior checks**.
Semantic wrong values may account for up to four failures only if all mandatory
behavior gates remain satisfied; no post-results relaxation. Scorer reports
observed pass count, fixed planned denominator, status totals, category counts and
critical failures; it emits no statistical general-accuracy claim. Its
`proposed_threshold_met` flag is draft arithmetic, never owner acceptance.
With24 correlated cases and repeats this is a small convenience sample; repeats
are not48independent problem types. Sampling variability, fixture overlap,
implementation exposure and coverage bias preclude a credible general NL→SQL
accuracy or production claim. The mandatory deterministic negative/security and
browser suite remains a separate gate, not diluted into48easy success examples.

## Approval decision and budget

Approve together: candidate/exposure or reviewer replacement, smoke/full scope,
threshold/rubric, exact tested candidate, observer/collector design, rate snapshot,
aggregate cap/admission threshold, contingency and preservation migration. See
[budget draft](H-014-live-eval-budget.md). Until then all48are not-run, I4/I5-live
await authority; offline readiness can complete. Publication and defense remain
separate. Preserve originals and append versioned results after any later fix.
