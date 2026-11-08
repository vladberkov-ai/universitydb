# H-015 — full real-model evaluation

**In progress: CP-L1 preparation only at this documentation cutoff. No H015 live
results, quality verdict, tested/frozen H015 candidate or completed eval is claimed.**
The owner authorized one full 48-conversation measurement without smoke, subject
to offline/review/freeze/accounting gates. Measurement completion is separate from
quality pass and final owner acceptance. Obsidian remains read-only; push is not run.

## Authority, identity and scope

- Published starting main and fresh remote main in the [baseline](../operations/H-015/baseline.json):
  `60e8ffcefb3614f7a754459722b14a7a2c6a1074`.
- Historical H014 tested product: `98345ad6ce5757c71d44ba1ce59a683d46e0d910`;
  H014 offline COMPLETE / strict5/5,485tests/157oracle are historical evidence,
  not a fresh full run of H015 collector/migration changes.
- Actual H015 prompt, CHAT053/054 and accepted ADR-CHAT007 authorize bounded
  CP-L1–L4; [authorization receipt](../operations/H-015/authorization-receipt.json),
  [input coverage](../operations/H-015/input-coverage.json),
  [ADR014](../adr/ADR-OMX-014-H015-full-live-eval.md) and
  [whole brief](../plans/H-015-full-live-eval-brief.md).
- [Binding readiness](../operations/H-015/binding-readiness.json) records root's
  actual current-native-owner check; [activation receipt](../operations/H-015/activation-receipt.json)
  records the new bounded scope. These do not resume or overwrite completed
  I1/H013/H014. Runtime IDs/pointers/locks are not manually edited.
- Exact new tested SHA, frozen candidate SHA, late-doc SHA and local checkpoint
  SHAs: **pending**. The published baseline is not the H015 frozen candidate.

## Prospective protocol and gates

Use exact H014v1 questions and original repeat-major order:24cases×2=48conversations,
max240generation attempts, max5generation/4SQL per conversation. Existing bounded
internal retry/repair counts within those limits. No smoke/access probe/count,
fallback, evaluator rerun, best-of, LLM judge, extra live UI generation or paid repair
campaign. Only useful A01-r1 may be the first paid request. No product prompt/logic
tuning against candidate queries/answers. Accepted ADR006 semantics and exact
`gpt-6.1-sol` plan high / SQL+repair medium / default Standard tier remain fixed.

Before results, the rubric is fixed at **≥44/48 overall AND ≥7/8 in every category**,
zero unsafe execution/privacy leak/fabricated success and 100% applicable mandatory
behavior. Ordinary failures/refusals/timeouts/invalid outcomes remain denominator48.
Started/not-run after a critical stop cannot constitute full completion. This exposed
acceptance sample is not an untouched holdout,48independent problem types or general
NL→SQL accuracy. CHAT054 explicitly selects scope/budget, not a separate verbatim
approval of every rubric phrase. Measured threshold is not final owner acceptance.

Collector, synthetic migration/no-network checks, full offline/static validation,
independent code-reviewer/architect reviews and prospective freeze remain pending.
The [prospective design](../operations/H-015/migration-design.md) requires normal
provider/compiled graph/SQLite, fresh trusted local fixtures, one shared canonical
spending ledger, durable started-before-action and original same-run evidence.
Oracle/answers/case metadata never enter model payloads. Independent non-model
observation/scoring occurs separately after collection. Full traces must retain
actual choices, typed M1 intermediates/bindings, raw/adapted rows and all failures.

## Budget and preservation

Aggregate **USD120 cap / USD110 dispatch / USD10 contingency** includes the original
**USD5.970272 across14entries**, not USD120 additional. Historical observed amount
USD0.1648460 does not release retained reservations. Baseline ledger SHA256:
`2753fe2fdf1dc366ffecdb5a86dcd9cf184d83707a00da0de62a8a4e4963f125`.

[Fresh official rate research](../operations/H-015/official-rates.md) supports the
conditional practical5.50input/11output USD/M envelope;12000input/32768output gives
USD0.426448 reservation, historical+240reserves USD108.317792≤110. This is
estimate-based policy, not strict BILLING_VERIFIED or an invoice guarantee. Account
routing, actual model/tier/usage and applied migration still require receipts.

At this preparation cutoff: H015 paid generation0/count0/access probes0; real ledger
migration not applied; actual H015 usage/cost/holds and remaining headroom after
collection **not measured**. Historical retained obligations are not new H015 cost.
Stop on budget/unknown spend/model-tier mismatch or critical safety/privacy/integrity;
retain holds, never automatically spend contingency, raise limits or release history.

Authorized migration/actual usage are the explicit monetary-preservation exception:
snapshot old bytes privately, preserve14entries/holds/rate history, append typed
policy authorization atomically under the shared lock and exact-baseline guard.
Completed I1/H013/H014 workflow artifacts, original evidence and locks must remain
unchanged; before/after proof is pending. No private ledger/backups/credential paths
or full private sessions are included in public evidence.

## All 48 planned statuses — preparation cutoff

These are original planned statuses, **not collected observations or zero scores**.
Each row names both original conversations. Score/category totals and independent
verdicts are not yet available. Fixed future denominator remains48.

| Case/category | Repeat1 status | Repeat2 status |
|---|---|---|
| A01 / aggregates/NULL | `A01-r1`: not-run | `A01-r2`: not-run |
| A02 / aggregates/NULL | `A02-r1`: not-run | `A02-r2`: not-run |
| A03 / aggregates/NULL | `A03-r1`: not-run | `A03-r2`: not-run |
| A04 / aggregates/NULL | `A04-r1`: not-run | `A04-r2`: not-run |
| J01 / JOIN/filters | `J01-r1`: not-run | `J01-r2`: not-run |
| J02 / JOIN/filters | `J02-r1`: not-run | `J02-r2`: not-run |
| J03 / JOIN/filters | `J03-r1`: not-run | `J03-r2`: not-run |
| J04 / JOIN/filters | `J04-r1`: not-run | `J04-r2`: not-run |
| D01 / dependencies/ties | `D01-r1`: not-run | `D01-r2`: not-run |
| D02 / dependencies/ties | `D02-r1`: not-run | `D02-r2`: not-run |
| D03 / dependencies/ties | `D03-r1`: not-run | `D03-r2`: not-run |
| D04 / dependencies/ties | `D04-r1`: not-run | `D04-r2`: not-run |
| C01 / clarification | `C01-r1`: not-run | `C01-r2`: not-run |
| C02 / clarification | `C02-r1`: not-run | `C02-r2`: not-run |
| C03 / clarification | `C03-r1`: not-run | `C03-r2`: not-run |
| C04 / clarification | `C04-r1`: not-run | `C04-r2`: not-run |
| E01 / empty/negative data | `E01-r1`: not-run | `E01-r2`: not-run |
| E02 / empty/negative data | `E02-r1`: not-run | `E02-r2`: not-run |
| E03 / empty/negative data | `E03-r1`: not-run | `E03-r2`: not-run |
| E04 / empty/negative data | `E04-r1`: not-run | `E04-r2`: not-run |
| L01 / Library | `L01-r1`: not-run | `L01-r2`: not-run |
| L02 / Library | `L02-r1`: not-run | `L02-r2`: not-run |
| L03 / Library | `L03-r1`: not-run | `L03-r2`: not-run |
| L04 / Library | `L04-r1`: not-run | `L04-r2`: not-run |

## Verification and independent verdicts

| Gate | Current evidence/status |
|---|---|
| Inputs/authority | Root-attributed reads; hashes match baseline; bounded omissions in input-coverage.json |
| Synthetic migration/collector | Pending, no canonical migration performed by documentation lane |
| Full offline/static | Pending for new candidate; H014485tests are historical only |
| Independent code-reviewer/architect | Pending; authoring this document is not independent approval |
| Prospective registration/freeze | Pending exact code/prompts/scorer/cases/oracle/fixtures/rates/policy hashes |
|48real conversations/full traces | Not-run at preparation cutoff |
| Independent observer/scorer/artifact review | Not-run; no score or quality verdict |
| Native completion/strict checkpoint | Not claimed; root-owned actual postconditions only |

## Requirement coverage and delivery boundary

- R03/R08: extended real-model measurement pending; historical limited I1 live
  examples remain distinct from this48-conversation sample.
- R04/R05/R06/R07: existing query breadth, shared core, full trace and
  clarification/error/safety contracts remain invariants to verify, not waived by a score.
- R13/U04: scoped alternatives/rationale in ADR014; earlier proposed ADRs unchanged.
- U01: [actual root task](../ai/omx/H-015-actual-prompt.txt) is a supported-export
  projection with one private-prefix substitution; [receipt](../operations/H-015/prompt-receipt.json).
  H-package is read context. Existing [RU](../ai/PROMPTS-RU.md) and
  [EN](../ai/PROMPTS-EN.md) bundles contain actual Russian text/labelled English
  reader translation, not a claim of an actual English input. Child tasks/results
  are selected attributed projections, not full transcripts. Runtime templates
  are separate from future actual full requests. U01 remains partial globally.
- U06: explicit-path local checkpoints authorized; SHAs/verification pending.
- R15: baseline already published; new H015 publication pending separate authority.
  Fresh remote main at start is60e8ffc; **push not-run**, no new push authority.
- R16/R17: final delivery/defense/rehearsal deferred, not completed by this eval.

The root continues the already-authorized internal checkpoints without a new consent
handoff. Final closeout must replace preparation-only claims with actual frozen/tested
identities, all statuses/scores/categories, traces, calls/costs/retained holds,
independent verdicts, preservation and local/remote receipts. No fabricated result,
partial/full confusion or failed-quality acceptance claim is permitted.
