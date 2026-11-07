# H-008 live preflight: official API billing references

## Scope and provenance

- Request type: implementation-reference and current-pricing research, not an access probe or implementation authorization.
- Retrieved: 2026-11-07; research clock: 2026-11-07 16:52:59 UTC.
- Exact model: `gpt-6.1-sol`; requested operation profile remains plan `high`, SQL/repair `medium`; explicit generation `service_tier="default"`.
- Parent reports the existing I1/G004 goal is active. This research did not inspect or change goal/runtime state and does not independently certify that report.
- One total USD 10 continuation cap includes historical spend, uncertain holds, access checks and continuation attempts. No reset or extra allowance is implied.
- Actual delegated task is preserved in [the task record](../../../ai/omx/H-008-live-billing-research-task.txt). Earlier research and historical evidence are unchanged.

## Direct answer

**Full-request input counting has an official server-side surface; free/unbilled counting is not established by the retrieved documentation.** Use the exact model-facing input configuration with `client.responses.input_tokens.count(...)`, then require an integer `input_tokens <= 12000` before generation. The official guide explicitly covers schemas and message framing, unlike the previous bytes-plus-cushion gate. This is documentation of the mechanism, not evidence that any particular application request has passed it. [Counting tokens](https://developers.openai.com/api/docs/guides/token-counting)

**Published generation rates support a conservative USD 5.50/M input and USD 11/M output envelope** for Standard short-context text requests, including the highest published cache-write category and one 10% regional/FedRAMP uplift. Applicability to the actual endpoint/account and exclusion of other charges still require verification. Unknown count-endpoint billing remains a separate unresolved question; do not declare the entire billing gate verified from this rate table alone. [Pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true)

## Official docs evidence

### 1. Exact model and rate scope

[GPT-6.1 Sol model](https://developers.openai.com/api/docs/models/gpt-6.1-sol) lists `high` and `medium` reasoning, Structured Outputs, a 1,050,000-token context window and 128,000 maximum output tokens. Prompts above 272K input tokens incur 2x input/cache and 1.5x output pricing for the entire request. A proven 12,000-token input bound is below that threshold. The chosen 32,768 output limit is also below the published model limit. Neither fact establishes account access.

[Current expanded pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true), Standard/short-context, USD per million tokens:

| Category | Published | With 10% uplift |
| --- | ---: | ---: |
| Ordinary input | 2.00 | 2.20 |
| Cached input | 0.10 | 0.11 |
| 30-minute cache write | 2.50 | 2.75 |
| 12-hour cache write | 5.00 | 5.50 |
| Output | 10.00 | 11.00 |

The pricing page states regional processing and FedRAMP uplift. This is not evidence that a particular account uses either. No combined/custom-account surcharge is established here. Restrict verification to the actual permitted endpoint; do not silently expand this envelope to a different tier, provider, tool or account contract.

### 2. Cache accounting is not additive

[Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) states input tokens use ordinary, cached, or cache-write rates; write prices are total prices, not extra fees. The default GPT-6 cache TTL is 30 minutes, costing 1.25x ordinary input; 12 hours costs 2.5x. Overlapping selected writes bill a token once, at the longest applicable TTL. Thus charging every input token at USD 5.50/M is a conservative rate envelope across the documented categories, not a claim that all input actually receives a 12-hour write.

### 3. Exact input count and field coverage

[Counting tokens](https://developers.openai.com/api/docs/guides/token-counting) says the endpoint returns the model's exact input count and includes formatting such as message roles and boundaries. It explicitly addresses tools, schemas, instructions, conversation state and model-specific tokenization. Local text tokenization or serialized byte length plus a fixed cushion does not establish equivalent coverage.

[Python count reference](https://developers.openai.com/api/reference/python/resources/responses/subresources/input_tokens/methods/count) exposes `responses.input_tokens.count`, HTTP `POST /responses/input_tokens` under the API's `/v1` prefix. Supported parameters include `model`, `input`, `instructions`, `reasoning`, `text`, tools/tool choice, conversation/previous-response references and truncation. The response schema has only `input_tokens` and `object="response.input_tokens"`; no generated output, model identity, service tier or billing usage is documented there.

[Full count schema](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count) includes `text.format` with `type="json_schema"`, schema, name, description and strictness. Preserve that whole object and the same `reasoning` and model fields in count and generation requests. Do not count only user text or omit instructions/schema. If conversation history or tools are used, they must also match. Count validation must fail closed on missing, boolean, negative or otherwise invalid counts, oversize inputs, request mutation after counting, or unsupported count parameters. These fail-closed checks are research handoff recommendations, not verified local implementation facts.

### 4. Generation-only controls and output ceiling

[Create response reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create) defines explicit `service_tier="default"` as standard pricing/performance. Omitting it uses `auto`, which can follow project settings. The returned tier records actual processing and can differ from the request. Check it rather than assume it. `max_output_tokens` bounds visible and reasoning tokens. A 32,768 limit is therefore a total generation ceiling, not an additional reasoning allowance. Usage output already includes reasoning; do not charge reasoning twice.

For the current stated bounds, the proposed conservative model-token reservation is:

```text
(12000 * 5.50 + 32768 * 11.00) / 1000000 = USD 0.426448
```

This arithmetic is an inference from published rates and requested limits. It excludes an unknown count-endpoint charge and any separately priced service. It is not a new budget or permission to call.

## Supporting example, not a billing guarantee

The official [per-run spending-controller cookbook](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api) demonstrates counting shared model/input fields before generation; it says to include other supported input fields in both requests and to send `max_output_tokens`, `service_tier`, and `store` only to generation. It uses maximum input-category pricing, disables automatic retries, retains unresolved reservations after interrupted requests, and checks returned model/tier/usage. Its prices and models are expressly fictional. Its example excludes other/account-specific charges and does **not** establish that token-count requests are unbilled. Reuse the pattern only with actual verified local request coverage and the existing global ledger; do not use its example prices or reset the run's historical obligations.

## Count endpoint billing and account-access ambiguity

No explicit free/unbilled guarantee, per-count tariff, or count billing usage receipt was found in the opened counting guide, count references, pricing or cookbook. Targeted official-domain searches for count billing/free/charge wording did not resolve this. The pricing page's general statement that Responses API is not separately priced does not explicitly specify whether this count subresource consumes billable model input. Absence of a separate price or `usage` field is not proof of zero cost.

Accordingly, do not settle count calls at zero from their `input_tokens` result alone. A conservative bookkeeping hold may be retained as **uncertain**, but choosing an arbitrary amount does not prove a financial upper bound. Before a strict-cap live preflight, require authoritative zero-price evidence or a justified finite applicable charge ceiling; otherwise the unresolved fee remains a blocker. The retrieved material alone cannot establish that ceiling. Preserve earlier holds and count every authorized attempt against the same USD 10 authority; do not reset, retry automatically or label the full billing gate verified to work around missing evidence.

[Retrieve model](https://developers.openai.com/api/reference/python/resources/models/methods/retrieve) documents basic model metadata and permissioning, not structured-generation capability testing or billing. A successful metadata request would evidence metadata access only. A successful count request would evidence acceptance of that count payload, not an echoed model identity or successful structured generation. Only an authorized generation and validated response can demonstrate that requested operation's actual structured-output compatibility. These distinctions follow from the documented response surfaces, not live observations.

## Version note and validation limits

- Sources are current, unversioned official pages fetched on 2026-11-07, not pinned SDK release documentation. `openai==3.46.0` is task-supplied context, not independently inspected here. The executor should verify the installed count signature offline; no dependency update or new tokenizer is justified by this research.
- Generic count-reference wording still says reasoning is for GPT-5/o-series, while the exact GPT-6.1 Sol page explicitly lists reasoning efforts. Treat this as documentation drift; do not replace the requested model. No live compatibility claim follows.
- The model card summarizes 30-minute cache writes; the expanded pricing and caching guide additionally establish 12-hour writes. Do not mistake the summary for an exhaustive ceiling.
- The first generic Create response fetch failed due to page size. The official Python Create response page was then opened successfully and used instead.
- No credentials, private files, environment values, app/provider requests, SDK execution, product tests, runtime/goal/Git mutations or Obsidian changes were performed. No source-code, OSS or third-party evidence was needed.

## Reusable takeaway

Documented exact full-request counting can replace heuristic input attestation; default-tier generation can be conservatively reserved at USD 5.50/M input and USD 11/M output under the stated scope. The count endpoint's own billing remains unproven, and account/model/structured-generation evidence remains outstanding. This research does not set `BILLING_VERIFIED=yes` or authorize a live call.
