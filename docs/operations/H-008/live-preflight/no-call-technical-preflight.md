# G004 no-call technical preflight

2026-11-07. Performer lane `/root/g004_live_performer`; repository HEAD observed `af8cd2455442c7decbbb766f02ebe68b7c1cb430`. Root reports the existing native goal is now active; this performer did not inspect or mutate native goals, OMX state, IDs or the durable goal ledger. Historical blocked receipts remain unchanged.

## Received task and coverage

The actual parent task assigned this lane bounded G004 implementation/evidence/docs, initially **no-call technical preparation only**, with no network/API/live application dispatch or billing-verification flag until root's evidence-backed clearance. It explicitly required preservation of A/B, existing commits/receipts/unrelated files; no repeated G001–G003; one shared total USD 10; exact `gpt-6.1-sol` plan high/SQL-repair medium; no credential reading, dumping or publication. A later parent message directed no speculative count-endpoint/budget plumbing without fee proof and requested inspection of rigorous local/context-ceiling alternatives. Private credential location is deliberately omitted. This paragraph is a selected actual-task projection, not a full transcript or runtime prompt.

Read: repository README; H-008 continuation report; H-007 and H-008 handoffs (Obsidian read-only); current provider, worker and profile; current [researcher's official-source receipt](api-billing-references.md). No product source, tests, dependencies, application runtime prompts or spending files were modified. No key-file contents or credential/environment values were inspected.

## Offline findings

1. Installed `openai==3.46.0` provides `InputTokens.count` at `POST /responses/input_tokens`. Its inspected signature supports `model`, `input`, `instructions`, `reasoning`, `text`, conversation, tools and truncation. The model-facing strict `text.format` schema can therefore match generation. Existing worker instead calls only `responses.create`; it has no exact-count preflight.
2. The current parent byte gate counts prompt, encoded payload and serialized schema plus a 1024-byte cushion. This is not an exact token count or proven upper bound on model-specific framing. Current profile and reservations require at most 12,000 full input tokens; post-response overrun rejection cannot retroactively bound an already incurred charge.
3. No local `tiktoken` package is installed in the application virtual environment. Even installing a text tokenizer would not by itself prove model-specific complete request framing/schema coverage. No package installation or dependency change was attempted.
4. Official research establishes exact request counting but **does not establish its fee or a finite fee ceiling**. Reserving an arbitrary amount for that call, or assuming free from absent usage fields, would not prove the shared cap. No count request or access probe was sent.

## Rejected whole-context alternative

This arithmetic is a conservative inference from the model context ceiling and current rates cited in the research receipt, not evidence that these small actual prompts approach the ceiling:

- Context: 1,050,000 tokens; requested total output: 32,768. Even assuming the shared context subtracts output, the remaining input ceiling is 1,017,232 tokens.
- Long-context maximum documented input category including one 10% uplift: USD 11/M; output with 1.5x long-context multiplier and uplift: USD 16.50/M.
- One attempt: `(1017232 * 11 + 32768 * 16.50) / 1000000 = USD 11.730224`, already above the entire USD 10 cap.
- Even the non-cache ordinary long-context input rate USD 4.40/M yields USD 5.0164928 per attempt and USD 10.0329856 for the two plan/SQL calls alone, before mutation, UI, retries or unknown holds. It also does not cover every applicable cache category.

This is the full 12-hour-cache-plus-uplift envelope, not proof that every possible context-based reservation exceeds USD10. A separately established 30-minute-only cache profile could lower one-attempt cost, but that narrower applicability is unproven here and cannot silently replace the accepted monetary/profile policy. Using the entire context as input instead of subtracting output is still more expensive for the same rates. This alternative also changes the reviewed 12,000-input profile, its usage acceptance, and aggregate reservation policy; no silent profile substitution was made.

## Decision / exact blocker

**No safe code change is justified yet.** Keep `BILLING_VERIFIED` unset/not verified. The exact-count operation is a documented technical mechanism, but its own cost ceiling is unresolved; the available full-context fallback does not fit the shared cap. Thus this lane cannot prove pre-dispatch full-request input <=12,000 and bounded charges for both preflight and inference. Model/account structured-generation access, actual live S6, independently changed oracle and live UI/full trace remain untested.

A supported next step requires authoritative count-endpoint zero-fee/finite-ceiling evidence, or an authoritative local complete-request token-bound mechanism that covers instructions, strict schema, reasoning configuration and framing. Neither a new key, an arbitrary hold, byte heuristic nor a successful metadata probe supplies this missing proof. Root owns final stop/checkpoint and any supported goal transition. No new budget, model, plan or goal is requested by this receipt.

## Checks actually performed

- Read-only installed SDK signature/source inspection; no SDK request/client execution.
- Decimal arithmetic above reproduced locally with Python; no network.
- `git rev-parse HEAD` returned the SHA above; tracked and staged diffs were empty before this new documentary receipt. Existing unrelated untracked files were preserved.
- No application/product test rerun: no code changed and no regression was identified. This is not a repeat of G001–G003, nor new live acceptance evidence.
- No application launch, model/count/access request, credential source, spending reservation, Git staging/commit, OMX/goal mutation or Obsidian write occurred in this lane. Incremental lane spend/holds: USD 0; this lane does not independently certify root's aggregate ledger totals.
