# H-009: current official API rate references

## Request type and provenance

Current-pricing and implementation-reference research; documentation only. Retrieved 2026-11-07; research clock 17:16:36 UTC. Exact model remains `gpt-6.1-sol`, plan `high`, SQL/repair `medium`, explicit `service_tier="default"`. These are current, unversioned public docs, not an account receipt or pinned SDK reference. The [actual delegated task](../../ai/omx/H-009-rates-task.txt) records scope and omissions. Historical H-008 evidence is unchanged.

H-009 authority supplied by the parent replaces strict full-input/count-fee proof with an engineering estimate for the local payload, strict schema and framing. It prohibits the count endpoint and further free-count research. This receipt neither reinstates those gates nor claims a mathematical input/invoice bound. The same USD 10 total includes old spend and holds; USD 8 is the new-dispatch threshold and USD 2 the residual-uncertainty buffer, not extra allowance.

## Direct answer

The previously documented conservative **USD 5.50/M input and USD 11/M output** rate envelope is still supported for Standard short-context text generation: it covers the highest input category plus one 10% uplift. It does not mean ordinary input costs USD 5.50/M, or that the public default endpoint incurs a regional surcharge. Actual token volume and final invoice remain distinct from published rate evidence.

## Official docs evidence

### Published prices

[OpenAI API pricing](https://developers.openai.com/api/docs/pricing), Standard short-context, USD per million tokens:

| Category | Published | Including one 10% uplift |
| --- | ---: | ---: |
| Ordinary input | 2.00 | 2.20 |
| Cached input/read | 0.10 | 0.11 |
| Cache write, 30 minutes | 2.50 | 2.75 |
| Cache write, 12 hours | 5.00 | 5.50 |
| Output | 10.00 | 11.00 |

The pricing page applies a 10% uplift to regional-processing endpoints for models released on/after March 5, 2026, and to FedRAMP endpoints. Inclusion here is conservative arithmetic, not proof that either applies to this account. Other providers, custom contracts, taxes and separately priced services are not certified by this table.

### Model, efforts and long context

[GPT-6.1 Sol model](https://developers.openai.com/api/docs/models/gpt-6.1-sol) confirms `medium` and `high` effort, Structured Outputs, a 1,050,000-token context window and 128,000 maximum output tokens. API prompts **above 272K input tokens** multiply input/cache rates by 2 and output by 1.5 for the whole request. Thus long-context ordinary/read/write30m/write12h/output rates derive as **4 / 0.20 / 5 / 10 / 15**, or **4.40 / 0.22 / 5.50 / 11 / 16.50** with one 10% uplift. The short-context envelope is not valid for such requests. Local engineering estimates are not authoritative token counts; H-009 accepts that residual uncertainty rather than requiring a counting call. No model substitution is proposed.

### Cache categories and reconciliation

[Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) establishes the default 30-minute write lifetime and optional 12-hour lifetime in Responses. Input categories are exclusive, not additive: ordinary tokens, cached reads, 30-minute writes and 12-hour writes. `cache_write_tokens_details.ttl_30m_tokens` and `ttl_12h_tokens` sum to `cache_write_tokens`; `cached_tokens` excludes writes. Compute ordinary tokens as total input minus reads minus writes. Do not add the write total again after its lifetime components. A token covered by overlapping writes is billed once at the longest applicable lifetime. The model card's single write price summarizes 30-minute writes; the pricing/caching pages establish the additional 12-hour category.

### Endpoint, processing tier and output budget

The official [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning) demonstrates `https://api.openai.com/v1/responses` with the exact model. Reasoning tokens are billed as output; `max_output_tokens` covers reasoning, visible output and non-visible formatting. An incomplete response may still consume billable input/reasoning without visible output. Do not add reasoning tokens a second time to reported total output.

[Create response, Python reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create) defines explicit `service_tier="default"` as Standard pricing/performance. Omission means `auto`, following project settings. The returned `service_tier` identifies actual processing and can differ from the requested value. Endpoint and tier documentation do not establish account permission, actual routing or structured-generation success. This lane made no provider calls and inspected no endpoint configuration or credentials; the root/executor owns local validation and response checks.

## Supporting example — arithmetic only

For an engineering input estimate `E` and configured total output limit `O`, the conservative short-context token-cost reservation is:

```text
(E * 5.50 + O * 11.00) / 1_000_000 USD
```

For example, `E=12000`, `O=32768` gives USD 0.426448. This is an illustrative estimate using published rates, **not** a guaranteed whole-request ceiling or permission to dispatch. Preserve historical monetary obligations and uncertain holds. Application ledger/threshold implementation and actual dispatch evidence are outside this research lane.

## Version note, ambiguity and verification

- Official pages were searched and opened before repository evidence was read. The generic Create response page failed retrieval because of its size; the official Python reference opened successfully and supplied the tier evidence.
- Fresh pricing, exact-model and caching pages agree on applicable Standard rates. Search results for other tiers/older cached pages were not used as the Standard rate table.
- No application/provider/count requests, count-fee research, credentials/environment reads, dependency changes, runtime/goal/Git mutations or Obsidian writes occurred. No source-reference, OSS or third-party evidence was necessary.
- Published default-tier rates are established; actual account access, invoice totals, local request composition and live S6/UI outcomes are **not** established here. Only the two assigned new documents were written.

## Reusable takeaway

Keep exact `gpt-6.1-sol` high/medium/medium and explicit default tier. The USD 5.50/M-input, USD 11/M-output short-context envelope remains conservative. Use H-009's accepted engineering estimate and shared USD 10 policy without a count request, ledger reset, model fallback or claim of invoice certainty.
