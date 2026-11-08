# H-015 v2 paired-output acceptance — independent BEFORE-SCORING review

## Decision

**APPROVE — paired-output/source/full-record-delta gate only.** No blocker found.
Actual field census is **8 changes in 8 records; 40 records unchanged**. This is
not a score, product-quality pass, final closure of the original HIGH, or permission
for a new campaign. Scoring remains a separately released root-owned next step.

This independent reviewer owns only this new review and
`corrected-assessment-v2/paired-output-acceptance.json`. The previously approved
source receipt remains immutable. No corrector/scorer/application/provider was
run by this reviewer, no oracle was read, and no lifecycle/Git/ledger mutation or
source edit occurred. Other agents' ongoing documentation edits were left alone.

## Exact identities and successful-execution evidence

Fresh local hashes agree with the prior independent provenance approval and root's
actual-output handoff, not merely with the self-generated correction manifest:

| Input/output | SHA256 |
|---|---|
| Reviewed corrector | `8560fcb2c7458ab778dbac1d55530f8b634561727f74281b4809c53bf6389908` |
| Independently approved source receipt | `6be34de5801a1e277a160796f4126db23cccc0555f6672a74463738d613908b7` |
| Frozen observer | `a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14` |
| Frozen scorer | `a14f11835ff3c67aa6ef6e7a95716613982a3c1799bfa2d734f4038c95a1c811` |
| Original records | `6b8b7126f3f20aa9cf6ec94e4d0e66436651e145f2473a150b25690572710c23` |
| Original score | `8b9be7800c9c1462d462106c789c47f76a88466adf4871973454ccd1ef7bb86a` |
| New records | `cfede7911e5d6e276e458e936e7b083291dfdd6f2ed35023e87d991d5e73f2c6` |
| New correction manifest | `8bd96e991cb476d7ba35bd320309514561f643b362f22378ae4fe211c76589f4` |
| New independent acceptance receipt | `59c43cbcd294a3aab304cb9de6005ec9a865bf96b31e1bdd1230cb2cabd3ad15` |

Read the retained exact `corrector-launch.json` and `corrector-execution.json`:
performer `/root/v2_execution`, canonical repository cwd, the reviewed tool and
original campaign/records/source receipt, distinct new records/manifest paths.
All launch fields agree with the execution receipt. The retained execution receipt
records integer **exit_code=0**, start/finish, unchanged inputs and exact output
hashes. Its log hash matches the actual empty execution log. Root independently
reports one released execution with exit0. This is attributed process evidence:
the reviewer did not personally launch/witness the process and does not pretend
that parsing files or an empty log alone proves successful execution. No retry or
alternate corrector was invoked in this review.

## Complete strict paired-manifest checks

Both complete output files parsed with duplicate-key and nonfinite-number
rejection; trailing/truncated JSON would fail the parser. The manifest has exactly:
`version`, `source_version`, `frozen_observer_sha256`, `correction_source_sha256`,
`source_receipt_sha256`, `input_sha256`, `output_sha256`, `artifacts`, `changes`,
`scope`. Version is `h015-mean-nullability-correction-v2`, source version is
`h015-observer-v1`, and scope is exactly
`post-results type-only correction; not a score or prospective evidence`.

Every source/input/output identity matches freshly rehashed files and independently
pinned identities above. The entire manifest artifact map is strictly equal to the
prior independently approved receipt: exactly **192** artifacts, **4 per 48 runs**.
Every entry was rehashed and compared with both that immutable receipt and the
original collection closeout, not trusted because the new manifest says so.
Original raw state/exchange/trace links were checked for each run again.

## Independent full-record delta and semantic applicability

A one-off stdlib audit compared all **48** original/new records recursively with
strict JSON types, identical object keys, list lengths and positional ordering.
It did not call the observer, corrector, scorer, product graph or oracle. The full
actual leaf delta, including its original run order, equals the manifest's exact
`changes` list. No additional changed key, value, type, list item or record exists.

| Changed run | Exact field | Old | New |
|---|---|---|---|
| A01-r1 | `/observed/types/0` | decimal | decimal? |
| A02-r1 | `/observed/types/0` | decimal | decimal? |
| C01-r1 | `/observed/types/0` | decimal | decimal? |
| C03-r1 | `/observed/types/0` | decimal | decimal? |
| A01-r2 | `/observed/types/0` | decimal | decimal? |
| A02-r2 | `/observed/types/0` | decimal | decimal? |
| C01-r2 | `/observed/types/0` | decimal | decimal? |
| C03-r2 | `/observed/types/0` | decimal | decimal? |

Applicability is established from retained product contracts, not run identifiers,
oracle expected types, observed NULL occurrence, or desired score:

- All **10** original successful scalar means retain exact registered
  `u.grade_mean.v1`, aggregate shape, no group keys, three nonnullable integer raw
  components (`sum_units`, `graded_count`, `enrollment_count`), registered component
  mapping, grade_hundredth unit and scale100. The domain source still matches its
  original prospective-freeze hash. Read-only inspection of
  `src/universitydb/domain.py:42–96,507–526` establishes that the derived mean is a
  decimal string **or NULL** independently of whether this sample currently has
  a NULL, while raw component columns are not the derived mean's schema.
- For each successful scalar result, retained final answer and step results equal
  compiled state and final-step answer. Its raw step equals the compiled completed
  entry and original db_result event; adapted_result and answer events agree.
  Terminal trace hashes and events equal the retained final exchange. Each changed
  projected `mean` column maps to that actual derived `average`; its observed rows
  and empty reason equal the original retained answer. No arithmetic was rerun.
- Both already-null scalar records remain wholly unchanged. All **38 original
  failure records** and all **8 Library records** remain recursively identical,
  including false mandatory/scope checks. No Library success or grade semantics is
  invented. Every record outside the eight named deltas is unchanged.

All numeric/string/NULL values, counts, scope, reasons, choices, dependencies,
checks, statuses/outcomes, calls and trace identities are unchanged. Denominator48
and original order remain intact. This repairs the primary nullable-mean contract
representation; no relaxed grader, swallowed failure, fabricated success, fallback
answer path or alternate observer is introduced.

## Preservation and diagnostics

Fresh direct rehashes of **all1139 targets** in root's independently retained
`before-preservation.json` match before and after this review, including427original
collection files,688historical operation files,12nonmonetary targets,4original
observation files and the additional source/protocol/registration/monetary targets.
Before-receipt SHA256 is
`325b3d5778a4ae5f5e92e372c1a90ecbaba8670dc54baf7b2f201adcfccfb028`.
Only hashes/counts are reported; no private monetary content or credentials are
exported. No permitted current-H015 lifecycle exception was needed for this scan.

Strict JSON/schema/closed-manifest/source/hash/192artifact/full-recursive-delta and
1139preservation checks all passed in one successful audit. No executable file was
modified, so lint/typecheck/product test execution is not applicable to this lane.
Existing preparation test/static evidence remains attributed to the preparation
performer, not represented as tests freshly executed by this reviewer.

## Code Review Summary

**Files Reviewed:** both actual paired outputs, launch/execution/log receipts,
immutable source receipt and provenance review, original48records,192referenced
artifacts, domain contract and1139preservation targets.

**Total Issues:** 0 for paired-output acceptance.

### By Severity

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0

### Recommendation

**APPROVE — BEFORE-SCORING paired-output gate.** Root may separately release the
unchanged frozen scorer under the current owner authority. No score has been
computed or inferred by this lane. The original actual-assessment HIGH remains
open until actual score evidence and final independent code/architecture reviews.
Product quality failure, exposed/correlated-sample caveat, prospective rubric and
separate owner acceptance/publication boundaries are unchanged.
