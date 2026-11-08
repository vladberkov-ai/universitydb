# ADR-OMX-014 — H-015 bounded full live measurement

2026-11-08. Adopted scoped implementation decision under the actual H-015 task,
CHAT053/054 and accepted ADR-CHAT007; dependent implementation and live evidence
remain subject to verification. This does not adopt proposed ADR003–007 or change
accepted ADR-CHAT006 semantics or Sol high/medium/medium.

## Context and authority

H-014 completed offline readiness, not broad real-model measurement. Published
baseline is `60e8ffcefb3614f7a754459722b14a7a2c6a1074`; historical tested product is
`98345ad6ce5757c71d44ba1ce59a683d46e0d910`. Its offline export/scorer is not a live
collector. The existing monetary authority retains USD5.970272 across 14 entries;
observed USD0.1648460 is not a credit against those reservations.

The owner chose **full evaluation immediately, without smoke**: original H014v1
24 cases × 2 repeats = 48 conversations, at most 240 generation attempts. New
aggregate limits are USD120 total / USD110 dispatch / USD10 contingency, **including
all historical obligations**, not USD120 additional. The reserve is not
implicitly spendable. [Authorization receipt](../operations/H-015/authorization-receipt.json)
and [baseline](../operations/H-015/baseline.json) identify the sources without
publishing private originals. This is a practical accounting policy, not strict
`BILLING_VERIFIED` or an invoice guarantee.

## Decision, alternatives and rationale

### One shared monetary authority; versioned atomic migration

Preserve the exact old ledger bytes/hash privately and all 14 historical entries,
holds, authorizations and rate/profile segment. Append the fixed typed H-015
policy/version and current segment. Validate each entry against its own historical
segment, sum all obligations, and revalidate the ledger before every dispatch.
Use the same stable lock for migration/reservation/settlement, atomic durable
replacement and an exact expected-baseline guard. Reject missing, corrupt, stale
or different baselines. Replay must validate the same authorization without a
second credit; concurrent processes must not obtain separate caps. Settlements
retain `max(reservation, observed)`; unknown usage/timeouts retain the hold and
stop. Tests use synthetic ledgers, never the canonical account.

Bind collector, standalone provider and UI to the same canonical spending ledger,
independent of temporary fixture DB roots. Reject reset/per-fixture ledgers,
environment-only cap changes, retroactive rate repricing and released historical
holds: each would conceal obligations or permit aggregate overspend. No new
monetary authority is created by a new process, fixture or workflow.

### Normal provider collector; oracle separation

Reuse the real compiled graph, SQLite and normal OpenAIProvider. Build each trusted
fixture locally in DELETE journal mode, outside generation. The collector reads
conversation/setup exports, never expected answers/oracle. Only original question
text and the prescribed selection at its interrupt enter the product conversation;
case IDs, fixture descriptions and oracle metadata do not enter model payloads.
No test transport, hardcoded answer/SQL, candidate-driven product tuning or new
dependency. A separate non-model observer/scorer receives the oracle after collection.

Persist `started` before provider action and retain original safe full wire/response,
model/tier/usage, full same-run JSONL, SQL/bindings/raw/adapted/dependency rows,
choices/selections/result/error and fixture DB hashes. Unknown started outcomes
must not be silently replayed. A mock collector would test plumbing but cannot
supply real-model evidence; an LLM judge adds cost and is expressly excluded.

### Prospective freeze and fail-closed collection

Before paid collection, independently review synthetic/targeted/full offline and
static evidence, then freeze exact tested code/scorer/prompts/cases/oracle/fixture/
rate/policy identities and original repeat-major 48-run order. Preserve historical
H014 files; append H015 evidence, do not rewrite old proposed/no-live cutoffs.
Fresh official rates and direct Standard routing need no paid access probe. The
first paid request must be useful A01-r1. Root owns secure credential loading only
after readiness gates; no credential values/paths/headers enter public evidence.

Enforce max five generation/four SQL attempts per conversation, existing bounded
internal repair/transient retry only, sequential dispatch and accounted + next
reserve ≤ USD110. No count endpoint, fallback, smoke, evaluator retry, best-of,
LLM judge, extra live UI run or paid repair campaign. Stop on budget/unknown spend,
model-tier mismatch or critical safety/privacy/integrity; do not consume contingency,
release holds or raise limits. Ordinary accounted terminal failures stay in the
fixed denominator and do not justify discarding/rephrasing their questions.

### Honest scoring, not an acceptance campaign

Fix H014v1 rubric before results: **at least 44/48 and at least 7/8 per category**,
zero unsafe/privacy/fabricated success and 100% applicable mandatory behavior.
Validate strict typed observations and choice sets before oracle-order normalization;
retain original trace order and actual M1 intermediates. No guessed evidence passes.
The owner explicitly chose scope/budget; this ADR does not attribute separate
verbatim approval of every rubric detail to CHAT054.

The dataset is exposed to authors/reviewers, not an untouched holdout. Two repeats
are not 48 independent problem types; measured threshold is not general accuracy,
production readiness or final owner acceptance. Completing all 48 terminal records
and independent scoring can complete honest measurement even if quality fails.
A critical stop with started/not-run records is partial, never full completion.

## Consequences and verification

Migration and collector preparation precede real ledger changes. Required proofs
include legacy preservation, equality/overflow, invalid/nonfinite values,
crash/replay/concurrency/stale drift, shared authority, payload isolation,
started/terminal persistence and complete traces. Independent code-reviewer and
architect reviews precede live freeze and follow final artifacts. Implementation
proof, exact frozen/tested SHA, actual outcomes/costs and verdicts are pending in
the [H015 report](../reports/H-015-full-live-eval.md), not implied by this ADR.

Root alone operates the new bounded workflow with explicit cwd; completed
I1/H013/H014 state, original evidence and locks remain unchanged. Authorized
monetary migration/actual usage are the explicit preservation exception, receipted
separately. Obsidian stays read-only. Local explicit-path checkpoints are allowed;
**push, final publication and defense are not authorized**.

## Post-results evidence cutoff — disclosed instrument limitation

Original exactecb7f5c collection has48terminal records,20known responses,
10product ok/38predispatch INVALID_INPUT. The frozen observer/scorer output2/48
is instrument-limited: eight additional numeric results otherwise match but computed
mean nullability is wrongly inferred from current cells. Final independent code
review REQUEST CHANGES/HIGH and architect WATCH supersede unqualified prelive
approval; prior APPROVE/CLEAR history remains. Quality FAIL is certain independently
from38product failures. No corrected score/full-DoD/native-completion claim follows.
A separately versioned append-only same-artifact offline correction is awaiting
scope clarification; original code/observations/score remain unchanged and no
provider/question rerun, product tuning or publication is authorized by this note.
See [qualified report](../reports/H-015-full-live-eval.md) for actual receipts.
