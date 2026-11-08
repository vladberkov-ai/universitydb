# H-015 corrected offline assessment v2 — independent source provenance

## Decision and scope

**APPROVE — source provenance and closed input receipt only.** No provenance blocker
was found. This does not approve a corrected output, authorize scoring by itself,
resolve the original actual-assessment HIGH, or certify evaluation completion.
The actual-output paired-manifest/delta acceptance review must precede scoring.

Read AGENTS.md and the exact actual owner message CHAT-056 read-only: it permits a
separate corrected offline assessment with originals preserved and independent
review, but no new API calls or push. Its SHA256 is
`0b15b2b81267ce2fcb6503535dc9506f788b540b071b37fba4712964c896d141`.
Root reports the existing H015 native goal ACTIVE/current-owner usable; this lane
neither independently operates nor changes lifecycle state. No child delegation.
Only the new source receipt and this new review are written by this lane.

## Reviewed source identities

| Source | SHA256 |
|---|---|
| Frozen `tools/eval/observe.py` | `a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14` |
| Original `observation/observations.json` | `6b8b7126f3f20aa9cf6ec94e4d0e66436651e145f2473a150b25690572710c23` |
| Original `observation/score.json` | `8b9be7800c9c1462d462106c789c47f76a88466adf4871973454ccd1ef7bb86a` |
| Original `observation/reviews.json` | `a035b32b42264c6a7766e2f639219c4a708f94d76639bd17a4e749c4f9c62d96` |
| Original `observation/independent-observation.md` | `951090b11306811e833694c936ad2b6f10de2e78da8f43ce335c04425074dad4` |
| Frozen `tools/eval/harness.py` | `a14f11835ff3c67aa6ef6e7a95716613982a3c1799bfa2d734f4038c95a1c811` |
| Reviewed corrector | `8560fcb2c7458ab778dbac1d55530f8b634561727f74281b4809c53bf6389908` |
| Original collection closeout | `e6180fc126a3f28d8623d66ccc1297e284358b9eaef74bc53893a49a97492a59` |
| Active prospective freeze | `adba96e727cd97b452ed6f2b21f6b7b85c691913edb189e7318b1636e4aef61b` |
| New `corrected-assessment-v2/source-receipt.json` | `6be34de5801a1e277a160796f4126db23cccc0555f6672a74463738d613908b7` |

These were freshly computed locally, not copied into an unverified receipt.
The original observation report's recorded hashes and commands, root's prior
`postresults-preservation.json`, and independent final/preparation reviews were
read. All four original observation files and original collection closeout also
match the bytes already retained at historical evidence checkpoint
`2b7e94c1e255feedd393c4153989e1013207e4e1` through read-only `git show`.
The prospective freeze binds the actual frozen observer/scorer identities, and its
hash and active collector-registration hash match the original collection closeout.
This historical/documentary chain supplements today's content hashes; it is not
an assertion that hashing alone authenticates evidence or reviewer independence.

## Direct linkage checks, beyond hash consistency

A one-off stdlib provenance audit, with no observer/corrector/scorer/product import
or execution, completed exit0 and established:

- **427/427** original collection files match the original closeout map exactly,
  including ignored original fixtures; no missing or additional collection file.
  Provider artifact bytes were rehashed, not re-sent or interpreted as new calls.
- Original planned order, summary terminal IDs, observation IDs, annotation IDs and
  scorer outcome IDs cover the same **48 unique runs** in original repeat-major
  order. All are completed; none is replaced, omitted, or converted to not-run.
- Each observation's calls, original absolute trace path and trace SHA bind its own
  completed receipt. Exactly one terminal trace exists per run; all **48 distinct
  original run identities** match their retained graph state and every exchange.
  Trace events equal final-exchange events; intermediate exchanges are exact
  prefixes. Event sequence is consecutive, event IDs are unique, and the final
  run_end status/calls agree with final exchange and completed receipt. Application
  attempt events agree with the original calls; no graph was executed by this audit.
- All **10 original ok envelopes** retain identical final/compiled answers and step
  results. Each completed raw step equals its original db_result event and compiled
  completed entry; its adapted result and answer events agree with retained data.
  All **38 original errors** remain INVALID_INPUT at resolve_scope with no answer,
  db_result or adapted_result event and retain outcome=failure. These are original
  product statuses, not a corrected score or alternative pass tally.
- Each observation scope equals its retained state scope (including absent scopes
  represented as null). Original six strict boolean checks equal the original
  named independent annotations. All **1088** attestation references have substantive
  notes and match actual closeout-bound original bytes. References are same-run,
  except the documented shared collection `registration.json` used for read-only
  safety provenance. This lane corroborates linkage; it does not freshly rerun a
  comprehensive privacy/safety adjudication or claim universal detection.
- Original totals corroborate **20 calls, 10 SQL attempts, 6 clarification exchanges**.
  The original score's same 48 completed records retain **2 strict passes**, zero
  critical-failure records, 38 mandatory-failure records and threshold=false. This
  is inspection of frozen scorer output, **not scorer execution** or recomputation.

The initial provenance assertion incorrectly required every annotation path to
start with its run ID; inspection identified the legitimate shared registration
reference. The corrected assertion explicitly permits only that one closeout-bound
shared file. No input was repaired or silently ignored. An initial bare `python`
command was unavailable; subsequent audits used the existing `.venv/bin/python`.
These were reviewer-command assumptions, not campaign defects or fallback behavior.

## Exact closed receipt contract

Read the complete reviewed `correct_mean_nullability_v2.py`, correction design,
development receipt, final-code-review and preparation code/architecture reviews.
The new receipt has exactly these four top-level keys:

- `source_version`: `h015-observer-v1`;
- `observer_sha256`: frozen observer identity above;
- `records_sha256`: unchanged original observations identity above;
- `artifacts`: **192** campaign-relative paths mapped to original SHA256 values.

For every one of 48 completed records the map contains exactly its `completed.json`,
`graph-state.json`, `exchanges.json` and the single original terminal-receipt trace:
**4 × 48 = 192**, with no oracle/provider/DB/registration/other unconsumed entry.
All map entries come from the independently rehashed original closeout, not new or
regenerated artifacts. Paths are relative to `docs/operations/H-015/collection`.
The observed completed record is the corrector's closed eight-field schema; its
`observed` object has the seven required fields and its six checks are strict bools.
The receipt was exclusive-created, strict-parsed with duplicate/nonfinite rejection,
and its schema/count/content rechecked. It is suitable as the exact reviewed
source receipt for the existing tool, not an ownership or execution token.

## Root-cause guard and outstanding acceptance boundary

The proposed correction repairs contract-owned scalar-mean representation, rather
than hiding failures or relaxing values/checks. No second observer was created,
no frozen observer helper called, no values or checks recalculated, no oracle
loaded, no corrector or scorer invoked, and no output/manifest or replacement score
produced in this lane. No provider/API/count/probe/credentials/live UI/question
replay/application execution/product repair/monetary/Git mutation/push occurred.
Original v1 source, observations, annotations, score and collection remain unchanged.

Original `final-code-review.md` HIGH/REQUEST CHANGES is **still open**. Root must
retain successful corrector exit0, strict complete paired outputs, exact reviewed
source/input/output/receipt/artifact identities, and obtain independent full-record
type-only delta approval before providing anything new to the frozen scorer.
Do not infer any corrected score from this provenance approval. Preserve original
v1 instrument output, failed product quality, exposed/correlated-sample caveat,
prospective rubric, and separate owner acceptance/publication boundaries.

## Code Review Summary — provenance gate only

**Files Reviewed:** complete corrector and frozen observer source; correction design
and development receipt; original report/final/preparation reviews and receipts;
427 collection artifacts by hash; 48 original observation/annotation/scorer records
and same-run terminal trace/state/exchanges linkage; the new 192-entry receipt.

**Total Issues:** 0 in the new provenance receipt; original instrumentation HIGH
remains outside this gate's closure authority.

### By Severity — provenance gate

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0

### Recommendation

**APPROVE — provenance only.** JSON/schema/hash/linkage diagnostics PASS. No modified
executable file exists in this lane, so lint/typecheck/product tests are not
applicable and were not run. Actual delta acceptance and subsequent independently
reviewed corrected assessment remain pending root handoff.
