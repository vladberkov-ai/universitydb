# Research: H-014 fixed Sol API rate evidence

## Request Type

Current official-documentation verification for the already selected
`gpt-6.1-sol`; not model selection or live authorization.

## Direct Answer

Fresh official documentation establishes the exact model's Standard API prices.
The proposed **short-context reservation envelope is USD 5.50 input / 11.00
output per million tokens**, including the highest documented cache-write class
and one 10% regional/FedRAMP uplift. This is an independently derived planning
envelope, not a new tariff, ledger migration, or permission to spend. It happens
to match the historical coefficients; history alone was not used as proof.

## Official Docs Evidence

All pages below were searched and actually opened on 2026-11-07 UTC
(2026-11-08 Asia/Jerusalem), not inferred from snippets.

| Standard API category | Ordinary input | Cached input | 30m write | 12h write | Output |
|---|---:|---:|---:|---:|---:|
| Up to 272,000 input tokens | $2.00 | $0.10 | $2.50 | $5.00 | $10.00 |
| More than 272,000 input tokens | $4.00 | $0.20 | $5.00 | $10.00 | $15.00 |

All prices are USD per million tokens, before regional uplift or account taxes.

- [GPT-6.1 Sol model reference](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
  establishes the exact identifier, ordinary/cached/30m/output prices and
  full-request long-context multipliers: 2x input/cache, 1.5x output above
  272K input. Its 1,050,000 context window is not the short-price boundary.
  It also states a 10% regional premium. Long-table numbers are arithmetic
  applications of these multipliers, not prices borrowed from another model.
- [API pricing](https://developers.openai.com/api/docs/pricing) corroborates
  the exact model's Standard short prices, explicitly including $5.00 for
  12h writes, and states 10% regional and FedRAMP uplifts. This envelope covers
  a single such uplift; combined uplifts or other account charges are not
  established here. Fast/Ultrafast and cloud-reseller billing are excluded.
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
  states 30m is the default lifetime at 1.25x ordinary input; 12h is 2.5x.
  Write prices replace ordinary input, not add to it. Input tokens fall into
  ordinary, cache-read or cache-write categories. Taking the largest input
  category avoids relying on cache hits. The envelope does not request 12h
  caching or change application retention.
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
  establishes that reasoning is billed as output, and `max_output_tokens`
  covers reasoning, visible output and non-visible formatting. Incomplete
  responses can still cost money. Reserve the entire output allowance;
  do not add reasoning a second time or treat empty visible output as free.

## Version Note

Retrieval clock observed `2026-11-07T23:06:00Z`; local task date 2026-11-08.
Evidence is mutable official documentation for API Standard processing, not
subscription pricing, account access proof or a frozen contractual quotation.
Revalidate before any separately authorized future live activation. Fixed
high/medium/medium efforts remain unchanged.

## Supporting Examples — proposed reservation arithmetic

Task-supplied policy inputs: complete assembled wire-JSON UTF-8 bytes plus
1,024 must be at most 12,000; reserve 12,000 input and 32,768 output per
dispatch; at most five dispatches per conversation. These are local proposed
practical-policy assumptions, **not official tokenizer guarantees**.

For the short envelope:

```text
input envelope = max(2.00, 0.10, 2.50, 5.00) * 1.10 = 5.50
output envelope = 10.00 * 1.10 = 11.00
R = (12000 * 5.50 + 32768 * 11.00) / 1000000 = USD 0.426448
```

| Proposed option | Conversations | Maximum calls | New reservation | Historical H + reservation |
|---|---:|---:|---:|---:|
| One conversation | 1 | 5 | $2.132240 | $8.102512 |
| Smoke | 6 | 30 | $12.793440 | $18.763712 |
| Full | 48 | 240 | $102.347520 | $108.317792 |
| Smoke then separate full | 54 | 270 | $115.140960 | $121.111232 |

H = USD 5.970272 is supplied by the existing budget draft; this research did
not open or modify the monetary ledger. These totals are required dispatch
headroom illustrations, not accepted caps. Additional contingency and applicable
taxes/account fees require an explicit future decision. The historical USD 8
dispatch threshold leaves only USD 2.029728 after H: insufficient for even one
five-dispatch worst-case conversation, much less the smoke/full envelope.
The historical USD 10 cap and USD 2 contingency remain unchanged.

## Caveats / Ambiguity Flags

- The complete-wire size gate is an accepted engineering estimate, not a proof
  of actual billable input or the short-context category. Selecting the short
  envelope is conditional on the named practical policy and its residual-risk
  acceptance. Never label this strict `BILLING_VERIFIED` evidence.
- Long-context rates exist and cannot be ignored when the category changes.
  The corresponding conservative rates are $11 input / $16.50 output after
  the same single uplift. Applying these rates to the **unchanged planning
  token allowances** yields R=$0.672672, smoke=$20.180160 and full=$161.441280.
  This is rate sensitivity only: it is **not** an upper bound for an actual
  >272K-token request, whose input allowance would also be wrong. Such a
  mismatch requires stopping and a new reviewed decision, not silently
  increasing the gate or spending.
- No exact-count endpoint, token-fee claim, account/model-access test, credential
  loading, API generation, app provider invocation, ledger/cap/hold mutation,
  Git push, or vault write occurred in this research. Offline calculations do
  not establish real-model accuracy or guarantee invoices.
- Search surfaced older pricing variants naming `gpt-6-sol`; they were not
  substituted. Current opened exact-model reference and canonical pricing
  page agree on relevant base prices. Other models' promotions are irrelevant.

## Reusable Takeaway

Integrate the dated sources and conditional USD 0.426448 short reservation
into the proposed live decision package. Preserve historical obligations;
request a separately explicit total-cap/dispatch-threshold/rate-policy decision
before any future live run. No live action is authorized by this artifact.

## Actual delegated task — verbatim projection

This is the research delegation actually received, not the root user prompt
or a runtime prompt; root prompt provenance is maintained separately.

> Bounded CP-R4 official rate verification ONLY for fixed gpt-6.1-sol default-tier API, no model choice. Own docs/operations/H-014/eval/official-rates.json or .md and actual task projection there. You are not alone; preserve others. Read installed /home/dev/.codex/skills/.system/openai-docs/SKILL.md and use docs-first official search+open, primary official OpenAI domains only. Need dated current exact named model input/cached/output rates, short/long context category thresholds, output reasoning billing relevance, source attribution and uncertainty. Do not probe API/count/access/load credentials, run app provider, change any budget/ledger/cap/holds/push/runtime/vault. Local chosen full request gate: complete assembled wire JSON bytes+1024 <=12000 estimate, reserve12000input/32768output per dispatch, max5calls/conversation; 48conversations/240calls max, smoke6/30. Historical ledger conservative5.50input/11output, cap10/threshold8, effective5.97027214entries; NOT automatically valid fresh rates. Need conservative applicable envelope from fresh official sources, if exact model absent say not established don't substitute another model, budget can be reviewable conditional rate decision. Return formula/sources/date and precise full/smoke values if substantiated. No recursive delegation. External documentation retrieval allowed, not paid model calls. Read existing budget draft for scope but do not rewrite it (eval author will integrate).

## Verification

Reservation arithmetic was recomputed with Python 3 `decimal.Decimal` only,
without application imports or network calls. Initial `python` command was not
installed; retry with `python3` succeeded. All above amounts are exact decimal
products of the stated planning inputs. No upstream-source, OSS, or third-party
evidence was needed.
