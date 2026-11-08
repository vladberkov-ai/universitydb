# H-015 independent observation — frozen-v1 result and limitation

## Outcome first

**All 48 original conversations have terminal collected records; frozen-v1 strict
scoring returns 2/48 and fails the prospective quality rubric. A post-results
representation defect prevents interpreting 2/48 as valid semantic accuracy or
claiming fully correct evaluation DoD.** Root's independent code/architecture
adjudication and final measurement-completion judgment remain pending.

There are **38 actual pre-provider `INVALID_INPUT` failures**, plus **8 additional
strict-score failures caused solely by observation nullability representation**.
The latter eight have exact matching actual rows, scope, choices, dependencies and
reasons: the frozen observer emits `decimal`, whereas the fixed oracle schema is
`decimal?`. They are not eight wrong numerical answers. `C02-r1/r2`, with actual
NULL mean and `no_grades`, match `decimal?` and are the two strict passes.

No alternative score, post-results normalization, source/scorer/oracle modification,
expected-type/value copying, product tuning, collection replay, paid rerun or LLM
semantic grading was performed. This report preserves the first frozen observation
and score artifacts; it does not promote a diagnostic comparison into a new score.
The sample is exposed and correlated (24 questions × 2), not an untouched holdout
or general accuracy measurement. Completing terminal collection is distinct from
quality pass, valid observation and final owner acceptance.

## Independent evidence audit

The observer lane is separate from product, monetary and collector authors. It
reviewed all 48 original started/completed/exchanges/compiled-state records,
full same-run traces, DB before/after census and fixture identities, all 20 complete
provider requests and 20 raw/parsed returned responses/usage records. All **427**
collection artifacts match root's original closeout manifest hashes. Original
artifacts were read only; only this observation directory was written.

Concrete per-run hash-bound notes are in `reviews.json`; no blanket pass annotation
was supplied. Mechanical assertions and evidence inspection establish:

- Forty-eight unchanged DB hashes/censuses; 10 executed read-only SELECTs each
  matched its prior validated SQL/bindings event. Frozen SQLite worker opens mode=ro,
  query_only and restricted authorizer. Other 38 runs never generated/executed SQL.
- Each original trace has consecutive unique events, matching run/trace identity,
  current terminal run_end, final-envelope equality, retained exchange-prefix history
  and exact application-attempt counts. No missing provider response or unknown spend
  is shown in these artifacts.
- Complete model payloads contain only registered question/descriptor/scope/step/
  refs/error/budgets, pinned runtime instructions and strict output schemas. No oracle,
  expected values, evaluation case/run metadata, credential values or headers enter
  those payloads. SDK raw response metadata and opaque provider-encrypted reasoning
  are retained as originals, not decrypted or republished here. This is evidence-
  bounded review, not a universal secret detector or provider-internal privacy claim.
- All 10 successes have actual raw ResultSpec/rows equal original DB result events,
  adapted answer equal original adapted_result/answer events and compiled/retained
  state, consistent integer-component arithmetic and exact NULL/empty reasons.
  All 38 errors have no answer, raw/adapted result or stale success.
- The 6 successful clarification conversations retain actual typed Alex alternatives
  1/3 or S1/S2, original order, prescribed selections, zero prechoice SQL generation,
  same-run/session/checkpoint pause and resume evidence. Oracle-set equality is checked
  before the frozen normalizer orders original values. No count-choice/M1/ties proof
  is manufactured for rejected conversations: those required behaviors are absent.

All 38 error runs have `scope_explicit=false` because no actual compiled scope
object exists, and conservative `behavior_complete=false` because requested
mandatory task-specific behavior is unproven. Their ordinary error handling is honest;
these false checks do **not** classify INVALID_INPUT as unsafe or fabricated success.
All 48 safe/private/trace_complete/nonfabricated checks are true from specific original
evidence; scope_explicit/behavior_complete are true only for the 10 actual successes.
Missing scope/M1/choices/results never become synthetic successful observations.

## Exact frozen outcome

| Field | Value |
|---|---:|
| Planned denominator / completed | 48 / 48 |
| Started / not-run / planned remaining | 0 / 0 / 0 |
| Product ok / error | 10 / 38 |
| Strict frozen passes | 2 |
| aggregates_null / joins_filters / dependencies_ties | 0 / 0 / 0 |
| clarification / empty_negative / library | 2 / 0 / 0 |
| Mandatory-failure records / critical-failure records | 38 / 0 |
| Threshold ≥44/48 AND ≥7/8 each category plus gates | NOT MET |

`score.json` retains the unchanged historical harness warning string ("Offline
scorer output is not live accuracy; thresholds proposed, not accepted."). That text
is frozen scorer metadata; these inputs are the actual H015 collection, not offline
injected observations. H015 prospective authority/rubric and the representational
limitation are documented separately, without rewriting historical source.

### Every run and failure

Each table row names both original repeats; calls are application attempts per repeat.
No failed or inconvenient formulation was rephrased, excluded or rerun.

| Run IDs | Category | Calls r1 / r2 | Result / failure |
|---|---|---:|---|
| A01-r1, A01-r2 | aggregates_null | 2 / 2 | Representation-only failure: observed decimal vs oracle decimal?; rows/scope/choices/reasons otherwise exact. |
| A02-r1, A02-r2 | aggregates_null | 2 / 2 | Representation-only failure: observed decimal vs oracle decimal?; rows/scope/choices/reasons otherwise exact. |
| A03-r1, A03-r2 | aggregates_null | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| A04-r1, A04-r2 | aggregates_null | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| J01-r1, J01-r2 | joins_filters | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| J02-r1, J02-r2 | joins_filters | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| J03-r1, J03-r2 | joins_filters | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| J04-r1, J04-r2 | joins_filters | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| D01-r1, D01-r2 | dependencies_ties | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| D02-r1, D02-r2 | dependencies_ties | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| D03-r1, D03-r2 | dependencies_ties | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| D04-r1, D04-r2 | dependencies_ties | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| C01-r1, C01-r2 | clarification | 2 / 2 | Representation-only failure: observed decimal vs oracle decimal?; rows/scope/choices/reasons otherwise exact. |
| C02-r1, C02-r2 | clarification | 2 / 2 | Exact frozen record passes. |
| C03-r1, C03-r2 | clarification | 2 / 2 | Representation-only failure: observed decimal vs oracle decimal?; rows/scope/choices/reasons otherwise exact. |
| C04-r1, C04-r2 | clarification | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| E01-r1, E01-r2 | empty_negative | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| E02-r1, E02-r2 | empty_negative | 0 / 0 | INVALID_INPUT — Unknown teacher name. Scope/required task behavior not established. |
| E03-r1, E03-r2 | empty_negative | 0 / 0 | INVALID_INPUT — Unknown student name. Scope/required task behavior not established. |
| E04-r1, E04-r2 | empty_negative | 0 / 0 | INVALID_INPUT — Unknown course name. Scope/required task behavior not established. |
| L01-r1, L01-r2 | library | 0 / 0 | INVALID_INPUT — Unknown reader name. Scope/required task behavior not established. |
| L02-r1, L02-r2 | library | 0 / 0 | INVALID_INPUT — Unknown reader name. Scope/required task behavior not established. |
| L03-r1, L03-r2 | library | 0 / 0 | INVALID_INPUT — Unknown reader name. Scope/required task behavior not established. |
| L04-r1, L04-r2 | library | 0 / 0 | INVALID_INPUT — Unknown reader name. Scope/required task behavior not established. |

Error messages across both repeats:
- `Unknown course name.`: 16 records.
- `Unknown reader name.`: 8 records.
- `Unknown student name.`: 12 records.
- `Unknown teacher name.`: 2 records.

## Accounting distinctions and bound on interpretation

20 application attempts = 20 monetary reservations = 20 known returned responses;
10 conversations reached the model with 2 attempts each, and 38 conversations had
zero calls. Ten SQL attempts occurred. Actual provider usage totals 38,858 input
and 5,808 output tokens (reasoning counted inside output), with all 20 returned
model IDs `gpt-6.1-sol` and tiers `default`. These low call totals do not mean the
other 38 were unrun: they are real terminal product failures in denominator48.

Root's separately retained monetary closeout records old14 obligations preserved,
new20 retained reservations USD8.528960, historical USD5.970272 and aggregate retained
USD14.499232. New observed conservative usage USD0.2776070 is not a credit releasing
reservations. This lane read collection receipts only, did not inspect credentials
or mutate the canonical ledger; independent monetary finalization remains root-owned.

## Reproducible verification and identity

Frozen/tested candidate: `ecb7f5c81c705d970dc64adb910ed2a5020cb28b`.
Active registration SHA256: `413fb669246b10e9112af0cb20d1922b46dc5db9e2bdc858a695e7771ac004d9`.
Active freeze SHA256: `adba96e727cd97b452ed6f2b21f6b7b85c691913edb189e7318b1636e4aef61b`.
No source, tests, original collection, frozen package, Git, runtime, lifecycle or ledger
writes occurred in this observation pass. Original48 IDs/order and all trace hashes
were freshly validated, and every completed record retains its own original artifact.

Commands (both exit0; output files exclusive-created on their first invocation):

```sh
.venv/bin/python tools/eval/observe.py --campaign docs/operations/H-015/collection --package docs/operations/H-014/eval/heldout-candidate-v1.json --reviews docs/operations/H-015/observation/reviews.json --output docs/operations/H-015/observation/observations.json
.venv/bin/python tools/eval/harness.py score docs/operations/H-014/eval/heldout-candidate-v1.json --records docs/operations/H-015/observation/observations.json
```

The second stdout was saved as `score.json` via an exclusive-create wrapper. Source
hashes were checked before observation. No test suite/model campaign was rerun.

| Artifact | SHA256 |
|---|---|
| `tools/eval/observe.py` | `a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14` |
| `tools/eval/harness.py` | `a14f11835ff3c67aa6ef6e7a95716613982a3c1799bfa2d734f4038c95a1c811` |
| `docs/operations/H-014/eval/heldout-candidate-v1.json` | `af1c7cafce466f58065fb96de9dd997565b2e3b940855fb9f48faa4559753ae5` |
| `docs/operations/H-015/observation/reviews.json` | `a035b32b42264c6a7766e2f639219c4a708f94d76639bd17a4e749c4f9c62d96` |
| `docs/operations/H-015/observation/observations.json` | `6b8b7126f3f20aa9cf6ec94e4d0e66436651e145f2473a150b25690572710c23` |
| `docs/operations/H-015/observation/score.json` | `8b9be7800c9c1462d462106c789c47f76a88466adf4871973454ccd1ef7bb86a` |

## Stop condition and remaining uncertainty

The frozen initial outputs are preserved. Quality failure is certain from 38 actual
product errors regardless of the eight representation-only mismatches. Exact semantic
accuracy and correct full-evaluation DoD are **not certified** by this frozen strict
score. Root must resolve the schema-contract defect through independent code and
architecture review and conservatively report measurement validity; no source repair
or alternate rescoring is authorized in this observation lane. No safety/privacy/
fabricated-success incident is evidenced, but unexecuted M1/ties/empty-list/Library
behaviors cannot be claimed as real-model successes. Final root artifact review and
lifecycle status remain distinct, pending owner-lane decisions.
