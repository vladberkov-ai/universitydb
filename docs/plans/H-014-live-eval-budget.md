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

Use full payload and maximum output even if typical replies are smaller. At rates
5.50/11.00 the arithmetic is R=USD0.426448; smoke30R=USD12.793440;
full240R=USD102.347520; combined270R=USD115.140960. These numbers are
**historical-rate illustrations pending fresh official dated rate evidence**, not
approved cap or permission. Root integrates separately researched official current
Standard/caching/regional/long-context rate evidence before final readiness receipt.
Do not claim cached discount or select a lower rate without authority; actual
tier/model mismatch stops. Long-context multipliers and taxes/fees/account terms
need explicit treatment. No payload-size assumptions beyond the unchanged product
gate; if gate does not fit M1, record failure rather than raise it.

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
