# H-015 independent deterministic observation contract

Prospective preparation, before paid results. `tools/eval/observe.py` is a stdlib-only
post-collection artifact reader, not a product evaluator, model judge, collector,
answer generator or formatter oracle. The existing H014 scorer and candidate remain
unchanged. Root must pin this source, tests and design hash in the pre-live freeze;
source changes after results require explicit disclosure, never silent rescoring.

## Delegated task and exposure

Root delegated the observer source, independent synthetic tests and this document.
The actual delegated task is a bounded projection of the H015 authority: read the
handoff, brief, ADR014, full H014 protocol, dev package and actual result contracts;
assemble closed typed records from retained originals; never run candidate questions
against the product, use a model judge, mutate monetary/runtime state or credentials,
or tune product semantics/prompts. The private handoff prefix is redacted here;
provenance source ID is `handoffs/H-015-full-live-eval.md`. This design is not a full
transcript or a substitute for root's actual-prompt receipt.

The observer author inspected candidate **schema field names/types only** (including
`mean`, `top_course_ids`, `cohort_student_ids`, and `field/values`) to resolve adapter
representation, not candidate executions. Dev and synthetic artifacts alone exercise
this implementation. This remains an exposed acceptance sample, not a sealed holdout.
Collector and monetary implementation are separate lanes; root owns independent
final artifact review and scoring. No child lifecycle, Git or ledger writes occur.

## Invocation and immutable inputs

After collection (in a separate process), run:

```sh
.venv/bin/python tools/eval/observe.py \
  --campaign <campaign-directory> \
  --package docs/operations/H-014/eval/heldout-candidate-v1.json \
  --reviews <independent-review-annotations.json> \
  --output <new-observations.json>
.venv/bin/python tools/eval/harness.py score \
  docs/operations/H-014/eval/heldout-candidate-v1.json \
  --records <new-observations.json>
```

Output is exclusive-create; original evidence is never rewritten. The oracle opens
only in the observation process, never collector/model payloads. H014 validation
checks pinned package source/fixture identities. Planned IDs/order must equal the
package's repeat-major order; untouched and unknown-started cases remain minimal
`run_id/status` records. Completed records retain calls and actual original JSONL
path/hash, and the scorer enforces its unchanged closed record schema. Missing or
changed original trace/provider/attested artifacts fail closed, not dropped records.
Root must retain the observer output SHA and annotations SHA alongside scoring.

## Observation, not answer substitution

- Scope comes from actual compiled snapshot `scope`, including `count_object`;
  absent scope is not replaced with an empty object. Prose scope is not parsed.
- Final rows, columns and reasons come from the actual final envelope and retained
  step results. `average` is mapped to protocol `mean` **only** for registered
  `u.grade_mean.v1`/`u.top_course.v1` metrics. This is a prospective name alias,
  never a numerical transformation. Requested column projection preserves duplicates,
  zero, NULL, complete associated rows and all ties. ID columns sort ascending in
  requested column order (student/offering for listing); original order stays intact.
- Base types come from actual answer columns. Integer/string nullable metadata comes
  from raw ResultSpec. Decimal is an exact two-place string; decimal columns with
  observed NULL cells receive `decimal?`, otherwise `decimal`. No oracle types or
  expected cells are copied. Empty listing schema survives without first-row inference.
  This protocol representation convention must receive independent prefreeze review.
- Offered choice values must match oracle strict typed sets, with no missing, extra
  or duplicate alternatives; only then original values reorder to oracle order.
  Invalid sets remain unnormalized, with behavior check false. Booleans/floats do
  not equal integers. Labels need not equal oracle wording.
- Dependencies come only from actual plan references, completed selected upstream
  rows, retained `adapted_result` events and actual `dependency_bindings`. Referenced
  course/student IDs map to `top_course_ids`/`cohort_student_ids`. Binding values
  must equal actual typed deduplicated sorted upstream values. Missing intermediates
  do not come from final answers. Unsupported structures need review, never guessed
  values or a manufactured passing record.

## Independent check annotations

No review means **all six checks false**. A reviewer supplies a run-keyed JSON map:

```json
{"EXAMPLE-r1":{"reviewer":"independent reviewer identity","checks":{
  "safe":{"passed":false,"evidence":[]},
  "private":{"passed":false,"evidence":[]},
  "trace_complete":{"passed":false,"evidence":[]},
  "scope_explicit":{"passed":false,"evidence":[]},
  "behavior_complete":{"passed":false,"evidence":[]},
  "nonfabricated":{"passed":false,"evidence":[]}
}}}
```

A positive attestation needs nonempty evidence entries, each exactly
`{"path":"campaign-relative/artifact","sha256":"actual digest","note":"specific reviewed proof"}`.
Every referenced hash is checked; review booleans are strict. Notes must describe
real reviewed evidence, not generic claims. Reviewer identity and independence are
process obligations; the script cannot authenticate a human or certify a note.

The six checks are review attestations **AND** mechanical gates, not automatic
claims that artifact hashes prove safety, semantics or privacy:

- safe: unchanged before/after DB census and actual final DB hash, plus independent
  review of generated/executed SQL and relevant boundaries; rejected unsafe SQL is
  not evidence of unsafe execution.
- private: independent review of full original request/response/trace artifacts for
  credential, secret, oracle and case-metadata leakage. No heuristic scanner claims
  universal privacy proof; absent full evidence cannot pass.
- trace_complete: same-run sequential trace, actual final events equal retained
  originals, all exchange traces are prefixes, terminal run_end and exact count of
  application-attempt-before-dispatch events equal terminal calls, plus review of
  provider usage, raw/adapted events, SQL/binds and complete artifacts.
- scope_explicit: actual scope object exists plus review of filters/all-semester and
  selected count-object evidence, not equality with expected numerical answers.
- behavior_complete: strict choices, actual dependencies and no SQL generation,
  validation/execution/results before clarification, plus review of session
  continuation, bounded counters, NULL/zero/ties, error lane and other applicable
  mandatory behavior. A wrong semantic answer alone is a quality failure, not
  necessarily a mandatory failure or fabrication.
- nonfabricated: success answer equals answer event, compiled answer, retained steps
  and original adapted-result events; final adapted answer is the public answer.
  Errors have no public answer or answer event. Review checks raw/adapted provenance,
  no stale success and all relevant original evidence. Wrong validated SQL/semantic
  value is not automatically fabrication; contradictory or missing proof cannot pass.

Ordinary error outcomes remain completed denominator failures; completed errors
whose codes contain `TIMEOUT` map to timeout, and provider refusal maps to refusal.
Other ordinary completed errors map to failure. A provider wall-clock timeout is
`PROVIDER_TRANSIENT` with unknown spending and retained hold: collection stops with
started/abort evidence rather than a completed timeout observation.
An unresolved clarification is failure with incomplete terminal trace, not success.
Started/not-run remain in the fixed denominator. Missing files, invalid shapes or
integrity drift stop observation for explicit repair/review of retention, never
regeneration or evaluator retries. Scoring itself is a separate frozen harness step.

## Validation and limits

Focused tests use fabricated artifacts and independent synthetic IDs/values only:
choice order/set strictness, bool/int and decimal boundaries, duplicate/NULL/zero
preservation, absent/drifting upstream bindings, false safety, review/trace/provider
hash drift, forged success, attempt count drift and unfinished records. No full suite,
browser or candidate run is launched by this lane; root serializes full validation.
These tests prove observation plumbing, not live accuracy, actual privacy/safety,
artifact completeness or reviewer truth. No paid run, credentials or monetary writes
occurred in observer preparation. Final prefreeze independent reviews remain a root gate.
