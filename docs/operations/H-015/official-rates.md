# Research: H-015 exact Sol Standard API rate revalidation

## Request Type

Current official-documentation verification for the already selected
`gpt-6.1-sol`; not model selection, account verification, or spending authority.

## Direct Answer

Fresh official evidence supports retaining the H-014 **USD 5.50 input / 11.00
output per million tokens** conservative short-context envelope. This is a
derived practical-policy envelope, not a published tariff or invoice guarantee.
With the supplied historical obligation H=USD5.970272 and unchanged per-dispatch
allowances, **H + 240R = USD108.317792 ≤ USD110**. Remaining dispatch headroom
is USD1.682208; the separate USD10 contingency is not used by this arithmetic.

## Official Docs Evidence

Official-domain search followed by actual page opens was performed on
2026-11-08 UTC. Observed retrieval clock: **2026-11-08 06:27:30 UTC**;
follow-up page reads occurred in the same research turn.

| Standard API input category | Ordinary input | Cache read | 30m write | 12h write | Output |
|---|---:|---:|---:|---:|---:|
| Up to 272,000 input tokens | $2.00 | $0.10 | $2.50 | $5.00 | $10.00 |
| More than 272,000 input tokens | $4.00 | $0.20 | $5.00 | $10.00 | $15.00 |

Prices are USD per million tokens before applicable uplifts. The long-context
row is calculated from the documented full-request multipliers, not substituted
from another model.

- [GPT-6.1 Sol model reference](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
  establishes the exact identifier, Standard ordinary/read/30m/output rates,
  1,050,000-token context window, 128,000-token maximum output, and support for
  `high` and `medium` reasoning. Above 272K input, the entire request uses 2×
  input/cache and 1.5× output rates. The context-window size is not the price
  boundary. Accepted high/medium/medium efforts remain unchanged.
- [API pricing](https://developers.openai.com/api/docs/pricing) corroborates the
  short Standard row including $5/M for 12h writes. Regional processing and
  FedRAMP endpoints each have a stated 10% uplift. Cloud-provider billing is
  separate. The selected envelope covers at most one such uplift, not combined
  uplifts, account taxes, reseller charges, or unlisted fees.
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
  establishes 1.25× ordinary input for default 30m writes and 2.5× for 12h
  writes. Input categories are alternatives, not additive fees. Taking the
  highest category avoids relying on cache hits. This research neither enables
  12h caching nor changes retention settings.
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
  establishes output billing for reasoning and that `max_output_tokens` covers
  reasoning, visible output, and non-visible formatting. An incomplete response
  can incur charges without visible text. Reserve the whole output allowance;
  do not add reasoning twice or treat empty output as free.
- [Responses create: official CLI reference, Body parameters](https://developers.openai.com/api/reference/cli/resources/beta/subresources/responses/methods/create)
  establishes that explicit `service_tier: "default"` selects Standard pricing
  and performance; omission or `auto` follows project settings. Returned
  `service_tier` describes actual processing and may differ from the request.
  This is field-behavior evidence, not a recommendation to switch API surface
  or enable beta features.
- [Fast mode](https://developers.openai.com/api/docs/guides/fast-mode)
  corroborates that project settings can make requests without an explicit
  service tier use Fast, and that response tier identifies actual processing.
  Its HTTP example uses the direct `https://api.openai.com/v1/responses`
  endpoint. No example or endpoint was executed.

## Version Note

These are mutable official API documents retrieved on 2026-11-08, not account
access evidence, a contractual price quote, or subscription pricing. The exact
requested identifier is preserved; no alternate model or fallback is approved.
The model page lists `gpt-6.1-sol`, not a dated immutable model snapshot.

## Supporting Examples — independently verified reservation arithmetic

Task-supplied practical-policy assumptions: complete wire JSON UTF-8 bytes plus
1,024 must be at most 12,000; reserve 12,000 input and 32,768 output per call;
48 conversations and at most 240 generation calls. These are local engineering
assumptions, **not official tokenizer guarantees**.

```text
input envelope = max(2.00, 0.10, 2.50, 5.00) × 1.10 = 5.50
output envelope = 10.00 × 1.10 = 11.00
R = (12000 × 5.50 + 32768 × 11.00) / 1000000 = USD0.426448
240R = USD102.347520
H + 240R = 5.970272 + 102.347520 = USD108.317792
110 - (H + 240R) = USD1.682208
```

Python3 `decimal.Decimal` recomputed all amounts successfully without application
imports or API requests. H and the 14-entry count are supplied task inputs;
this researcher did not read or certify the canonical monetary ledger.
USD120 is the supplied aggregate cap, not an additional USD120. This document
does not migrate policy, release holds, or authorize contingency spending.

## Caveats / Ambiguity Flags

- Root must separately verify direct account routing, effective request model
  and tier, absence of paid hosted tools, and the intended account/project
  without exposing credentials. Public documentation cannot prove local
  account access, special terms, available balance, or actual invoice amounts.
- An explicit default-tier request avoids reliance on project-default settings;
  it does not replace checking actual response model/tier and usage. Under
  H-015, a mismatch or unknown-spend condition stops further dispatch rather
  than silently using another rate/model, retrying an evaluator, or consuming
  contingency. These stop rules come from the task, not a provider guarantee.
- The short envelope remains conditional on the accepted practical estimate.
  Do not label it strict `BILLING_VERIFIED`. Actual >272K input changes both
  price category and input size; the 12,000-token allowance is then invalid.
- The main Responses reference HTML open exceeded the retrieval tool's content
  limit; its Markdown URL was rejected as unsupported content type. The smaller
  official CLI reference was actually opened and inspected instead. No claim
  depends solely on a search snippet.
- Search surfaced older query-string pricing variants with `gpt-6-sol`;
  canonical current exact-model/pricing pages were used instead. The CLI
  reference's Ultrafast availability wording is narrower than the model page;
  no Ultrafast claim or price is used for this Standard-only decision.
- No generation/access/count probe, credential/account-file read, application
  provider invocation, ledger mutation, workflow mutation, Git operation, push,
  or Obsidian write occurred. This research does not establish real-model
  accuracy or eval acceptance. No upstream-source, OSS, or third-party evidence
  was necessary.

## Reusable Takeaway

Freeze this dated conditional 5.50/11 envelope with the prospective H-015 policy.
It preserves the arithmetic fit of the supplied full 240-call protocol under
USD110 including H, without spending the USD10 contingency. Root owns local
routing/account checks, history-preserving migration, collector verification,
dispatch authorization and subsequent actual-usage anomaly handling.

## Actual delegated task — verbatim projection

This is the research assignment actually received, not the actual root user
prompt, the H-package, or an application/runtime prompt.

> H-015 bounded official-documentation research for already chosen exact gpt-6.1-sol/default direct Standard API; no model selection. Read /home/dev/.codex/skills/.system/openai-docs/SKILL.md and docs/operations/H-014/eval/official-rates.md and docs/plans/H-014-live-eval-budget.md fully. Verify fresh official model/rates/cache/context/output-reasoning/tier and safe routing facts, only official OpenAI evidence and browse search+open. No paid/API/count/access probes, no credentials/account files, no ledger/workflow/runtime mutations or push, no recursive delegation. Own only docs/operations/H-015/official-rates.md plus safe research receipt if needed; you are not alone, preserve others. Need explicit dated evidence whether H014 5.50/11 envelope remains valid (12000 input/32768 output; H5.970272+240R≤110), uncertainties, no fabricated rates. If writes before root scope activation are not appropriate, return result only and root will persist. Actual delegated task projection and source links, no private input copying. Account direct routing local config is root responsibility.
