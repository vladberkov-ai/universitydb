# Research: H-008 Responses API and native goal-control references

## Request Type

Bounded implementation-reference and current official-documentation research; no implementation, model reselection, paid probe, or live model request.

## Direct Answer

Preserve the approved exact model `gpt-6.1-sol`: plan uses `reasoning={"effort": "high"}`; SQL and repair use `reasoning={"effort": "medium"}`. Both efforts and Structured Outputs are supported. Do not substitute a model. [Official model reference](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

Use Responses, strict structured parsing, `store=False`, explicit `service_tier="default"`, and bounded output/time limits. Omit pro reasoning mode: standard is the documented default. These are request-contract recommendations, not evidence of account access or successful generation. [Reasoning guide](https://developers.openai.com/api/docs/guides/reasoning), [standard-tier spending example](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api).

## Official Docs Evidence

### Request and response contract

- Python `client.responses.parse(..., text_format=YourPydanticModel)` returns `output_parsed`. The wire format is `text.format` with `type="json_schema"`, `strict=true`, and a supported schema. Object schemas require `additionalProperties=false`; all fields must be required (nullable types can express optional values). Reject refusals, incomplete responses, absent parsed output, and validation errors rather than treating them as SQL. Structured shape does not prove semantic correctness. [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
- `max_output_tokens` covers generated reasoning and visible output, not just JSON text. Reaching it can leave no usable answer. Generic initial experimentation guidance reserves at least 25,000 reasoning-plus-output tokens; it is not an operation-specific minimum or success guarantee. [Reasoning guide](https://developers.openai.com/api/docs/guides/reasoning).
- Non-visible formatting tokens also count toward output usage. Do not add reported reasoning tokens to `output_tokens` again. [Counting tokens](https://developers.openai.com/api/docs/guides/token-counting).
- Set `store=False` explicitly. This is not a Zero Data Retention claim: abuse-monitoring and feature-specific retention are separate controls. Avoid introducing background mode as a timeout workaround in this scope; it has temporary storage behavior. [Data controls](https://developers.openai.com/api/docs/guides/your-data).
- Omitted or `auto` service tier follows project defaults, which can be nonstandard; do not rely on omission to prevent premiums. Explicit `default` is the standard-tier pattern. Fast processing carries a premium. Inspect the returned tier when available. [Project tier settings](https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/projects/subresources/service_tier_settings/methods/retrieve), [Fast mode](https://developers.openai.com/api/docs/guides/fast-mode), [standard-tier example](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api).

### Time and retry behavior

The current Python reference documents a ten-minute default timeout, configurable with `timeout`, and two automatic retries by default, including timed-out requests. `max_retries=0` disables these retries. [Python SDK reference](https://developers.openai.com/api/reference/python).

No fetched official page specifies a guaranteed or mandatory timeout for `gpt-6.1-sol` at high effort. High effort prioritizes deeper work over latency. A short timeout therefore cannot establish model incompatibility. [Reasoning guide](https://developers.openai.com/api/docs/guides/reasoning).

### Input reservations and money accounting

Input includes instructions, history and tool schemas, not merely the user's text. A local word/character/byte heuristic is not an official exact token counter. The official input-count endpoint is documented, but was not called. [Counting tokens](https://developers.openai.com/api/docs/guides/token-counting).

H-008 recommendation/inference: include the serialized structured-output schema, complete messages and request framing in conservative input reservation; leave explicit headroom for provider-side framing. The fetched count guide does not establish an exact local formula for structured-output schema/framing overhead. Do not advertise a heuristic plus a constant cushion as a mathematically proven monetary ceiling. Unknown input-count coverage is a live-run gate, not permission to probe.

Reserve before every billable attempt; settle against complete usage only. On timeout, transport ambiguity, missing usage or unknown cache-write accounting, retain an unresolved reservation and stop rather than refunding it or retrying blindly. Automatic SDK retries would otherwise create attempts outside an application-level call counter. This follows the official cookbook's conservative spending-controller example, which is an example rather than a billing guarantee. [Per-run spending controller](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api).

### Dated pricing reference — not authorization

Retrieved **2026-11-07**, standard model-page text-token rates per million: ordinary input **$2.00**, cached input **$0.10**, cache writes **$2.50**, output **$10.00**. The page also documents long-context and regional premiums. Consequently ordinary-input-only reservation is not worst-case if cache writes apply. [GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

These rates are reference-only, not approved spend, verified account pricing, or a current live rate card. Refresh applicable rates, region, model access and tier after explicit account access and a total cost cap are confirmed. For a standard-tier small-context calculation with verified applicability, reserve input at the maximum applicable input category rate and output at the full output cap; do not double-count reasoning. Reconcile ordinary/cache-read/cache-write categories separately when supported. [Per-run spending controller](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api).

## Supporting Examples: provisional offline operation envelopes

The following are **research recommendations**, not implemented configuration, measured latency, accuracy evidence, API guarantees, or payment approval:

| Operation | Approved effort | Candidate `max_output_tokens` | Candidate SDK timeout |
| --- | --- | ---: | ---: |
| plan | high | 32,768 | 600 seconds |
| SQL | medium | 16,384 | 300 seconds |
| repair | medium | 8,192 | 300 seconds |

Rationale/inference: planning gets more headroom than the generic 25,000-token starting guidance; tightly scoped SQL and repair are cost-containment hypotheses below that generic guidance, with acknowledged truncation risk. Their adequacy is unproven without authorized live evidence. Offline tests can verify routing, exact request fields, bounded failure and trace accounting, not answer quality or adequate reasoning allowance. Keep effort fixed as approved; do not silently raise output caps, switch tiers/models, or introduce pro mode after failure. Stop on an exhausted cap; revisit limits only through a separately authorized budget decision. A simpler conservative alternative is 25,000 tokens for each operation if later authorized affordability permits.

Use no hidden SDK retries. A candidate workflow ceiling is one plan, one SQL and at most one explicitly budgeted repair (three requests); this is a proposed bound, not a claim about existing code. SDK transport timeouts alone are not a proven total wall-clock workflow deadline. A separate operation/run deadline and ambiguous-charge handling need implementation-owner verification. No timeout guarantees server-side cancellation or zero billing.

## Native Codex goal resume: documented surface versus unresolved transition

- Official user controls include `/goal` and `/goal resume`; the Goals cookbook specifically describes the latter for a **paused** goal. Resume is controlled by the user/system, not a model-invented state write. [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).
- The developer-command reference distinguishes goal controls from `codex resume`, which resumes an interactive **session**. Session resume is not proof of a goal's blocked-to-active transition. [Developer commands](https://learn.chatgpt.com/docs/developer-commands).
- The desktop goal progress row provides owner pause/resume/edit/clear controls. [Long-running work](https://learn.chatgpt.com/docs/long-running-work). A general use-case page mentions controls when work is blocked, but does not specify this native tool contract's `blocked` transition. [Follow a goal](https://learn.chatgpt.com/use-cases/follow-goals).

**Specific unresolved point:** no authoritative fetched documentation established that a plain-text resume request, `/goal resume`, or any available model tool transitions the leader's observed native `blocked` status to `active`. The current task reports that explicit user resume did not change status. The tool schema available to this researcher permits only `complete`, `blocked`, and `paused` through `update_goal`; it exposes no active/resume mutation. The researcher did not call goal tools because it does not own the leader's goal.

Minimal owner step: use the existing thread's native goal-control Resume action, if exposed for that goal, then have the leader verify with a fresh native `get_goal`. If unavailable or still blocked, report **native blocked-to-active control unavailable/unverified** and request the owning user/runtime's supported goal-control action. Do not create a replacement goal, clear it, fabricate IDs, mutate state files, call hidden APIs, run CLI repairs, or claim a successful resume. The documented paused-goal slash command is not offered as a proven blocked-goal fix.

## Version Note

- Retrieval date: 2026-11-07; public live documentation, not a pinned historical release snapshot.
- Model: exact approved API identifier `gpt-6.1-sol`; no model-selection work performed.
- Caller reports installed `openai==3.46.0`; this research did not inspect repository usage, upgrade it, or prove its exact serialization behavior. Implementation owner must verify the installed SDK contract offline. Current Python docs include `httpx2` examples; do not copy that import or add a dependency based solely on live docs. A numeric timeout avoids that documentation-version assumption.
- Goal docs mention availability from Codex 0.128.0, not compatibility proof for this session's native goal implementation. No CLI/version repair was performed.

## Source-Reference Evidence / OSS / Supplemental Evidence

None required or consulted. No pinned upstream code, third-party guidance, private transcripts, account identifiers, or credentials are included.

## Caveats / Retrieval Limits

The main Responses create reference exceeded the web fetch size limit; the CLI variant timed out, the Markdown variant was unsupported by the web fetcher, and a bounded shell fetch produced no file. The platform alias also exceeded the size limit. Service-tier findings instead use fetched project-settings, Fast-mode and official cookbook pages; search snippets alone were not treated as complete evidence. No paid API, token-count endpoint, account/access probe, or live model evaluation was executed. Documentation recommendations remain separate from implementation and live certification.

## Reusable Takeaway

Keep the approved model/efforts, strict Responses parsing, `store=False`, explicit standard tier and visible bounds. Account for reasoning, schema/framing, retries and ambiguous charges. Live access, rate verification and an explicit total cost cap remain prerequisites; offline success is not accuracy proof. Native blocked-to-active goal recovery remains an owner/runtime control issue, not a repository repair.
