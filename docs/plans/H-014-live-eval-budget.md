# H-014 proposed live budget decision — no spending authority

Date2026-11-08. Exact model/efforts remain Sol high/medium/medium. No credentials,
access/count/generation calls, ledger/cap/hold changes or push in this preparation.

## Concrete choices

| Option | Conversations | Category coverage | Maximum generation calls |
|---|---:|---|---:|
| Small smoke |6, one each A01/J01/D03/C01/E01/L01, repeat1 only|6/6, not acceptance|30|
| Full |24cases ×2 repeats=48|6categories ×8 conversations|240|

Smoke is optional prospective triage, never a cheaper replacement for mandatory
classes, full denominator or44/48and7/8thresholds. If smoke cases are also later
collected in full, count their actual costs separately; do not reuse smoke results
as untouched full observations or hide duplicated spending. Smoke+full max270calls.
Internal planning/SQL/one repair across a bounded DAG share max5calls per
conversation, max4SQL attempts,180seconds active. No automatic retries/best-of.

## Reservation arithmetic and uncertainty

Current unchanged product Profile allows12000estimated input tokens per full
assembled request and32768output tokens per generation. Full payload includes
instructions, question, schema/catalog, strict JSON output schema, previous state,
dependency rows, choices, repair diagnostics, metadata/history/tools if present;
`payload_estimate` measures serialized UTF8JSON bytes plus1024framing. Above
12000estimate admission fails, not truncated or ceiling-raised. This is the accepted
practical engineering estimate, **not exact tokenization or invoice guarantee**.
No count endpoint is needed/authorized. Bill reasoning within output, not twice.
Per-call conservative reserve is:

`R = (12000 × input_USD_per_M + 32768 × output_USD_per_M) / 1_000_000`.

Use full payload and maximum output even if typical replies are smaller.
[Fresh exact-model official research](../operations/H-014/eval/official-rates.md)
(opened2026-11-07UTC/2026-11-08local) establishes Standard short-context ordinary
input2/cache-read0.10/30m-write2.50/12h-write5 and output10 USD/M. Cache write
replaces ordinary input, not adds; take maximum5 and one10%regional/FedRAMP uplift:
**5.50input/11output**. Do not rely on discounts; reasoning is within output.
Thus **R=USD0.426448**, smoke30R=12.793440, full240R=102.347520,
combined270R=115.140960. These independently re-established coefficients happen
to match history; historical rates alone were not evidence.

This is a **conditional practical short-envelope**, not exact tokenization,
strict BILLING_VERIFIED or an invoice guarantee. Complete wire bytes+1024≤12000
is an engineering estimate, not proof of billed input/short tier. Owner must accept
named practical-policy residual risk, reconfirm Standard/direct API/account and
single applicable uplift before future activation. Combined uplifts/taxes/fees/
reseller terms are unestablished and excluded from these API planning envelopes.
Long context>272000input has2×input/cache,1.5×output; conservative11/16.50 at the
same planning allowances yieldsR0.672672 as **rate sensitivity only**, not an upper
bound for an actual>272Krequest. Actual tier/model/category/usage mismatch stops
immediately for a reviewed decision; no silently enlarged payload or spend gate.

## Concrete proposed owner decision — before results

| Option | Aggregate total C | Dispatch D | Reserved contingency C−D | Max calls / retained H+new reserves |
|---|---:|---:|---:|---:|
| Smoke only, not acceptance |USD22|USD20|USD2|30 / USD18.763712|
| Full protocol (recommended for full evidence) |USD120|USD110|USD10|240 / USD108.317792|
| Separate smoke then full, if both desired |USD140|USD125|USD15|270 / USD121.111232|

All are **proposed, not authorized** aggregate planning caps including historical
H=USD5.970272. Contingency is not automatically spendable. Owner may instead defer
or request a versioned replacement; thresholds remain separately proposed44/48 and
≥7/8/category plus100%mandatory behavior/zero unsafe/privacy/fabricated success.
Smoke is not full acceptance. Approving a cap alone does not authorize source,
case or policy migration, credential loading or live dispatch without final gates.

Forecast **scenarios**, not measurements or usage predictions:112generation calls
(2ordinary calls,4M1; actual clarification/repair/refusal differs), each6000input+
2048output at5.50/11, givesUSD6.219136. Sensitivity144calls×(12000input+4096output)
givesUSD15.992064. Neither replaces maximum reservation nor guarantees fit; no live
usage was collected, no failures dropped, no savings inferred as quality evidence.

## History-preserving future cap decision

Existing totalUSD10 and practical admissionUSD8/reservedUSD2 belong to prior
I1authority, not permission for this eval. Existing monetary ledger SHA256 is
`2753fe2fdf1dc366ffecdb5a86dcd9cf184d83707a00da0de62a8a4e4963f125`;
root read-only preservation receipt verifies bytes. At this snapshot all14entries
retain conservative reserved/effective USD5.970272; observed USD0.1648460 is not
a credit to release. All14have usage, uncertain_attempts0, stopnull; the reservation
excess remains retained. Existing USD8dispatch threshold therefore leaves
USD2.029728admission headroom, versus USD4.029728nominal total-cap headroom;
USD2contingency is not automatically spendable. No assumption of zero historical
obligations, no hold release and no reset. Reverify before any authorized live gate.

Future approval must state aggregate total cap C including old accounted/held H,
a lower dispatch threshold D, reserved contingency C−D, named practical policy and
rates. Require D≥H+N×R for intended maxNcalls; otherwise package must explicitly
accept potential early budget-stop/incomplete evaluation. Reserve next R atomically
before every sequential dispatch and admit iff accounted/held+R≤D. Settlement is
max(reservation, observed conservative bill), not sum; missing usage/timeout leaves
hold. Usage/routing/model/tier anomalies stop immediately; never auto-spend
contingency, release old holds, migrate rates/reset ledger or create independent
per-launch balances. Provider-side billing remains separate from local estimates.

If cap/policy migration is needed, prepare a versioned owner-approved append-only
migration: capture old bytes/hash and obligations, record authorization/rate version
and new aggregate limits, preserve all historical entries/holds, regression-test
with synthetic ledgers, and independently review before live activation. Current
controller constructor is pinned to totalUSD10/model and historical policy; changing
an environment cap value alone is not a valid migration. Preserve all14entries
and the historical rate segment. This package does not alter it or claim
a new cap is already executable. Owner can approve full, smoke only, a reviewer
replacement or defer; no old cap20example is authority. No live acceptance claim
until full approved run and all mandatory gates finish.
