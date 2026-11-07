# ADR-OMX-010 — practical I1 budget policy

- Date: 2026-11-07. Owner: repo. Status: **adopted only for existing I1/G004**.
- Authority: explicit H-009 user task and accepted private ADR-CHAT-005 / CHAT-034 (verified hashes in [input receipt](../operations/H-009/input-hashes.json)); safe summary, not a copy of private sources.
- Supersedes only H-008's mandatory exact input-bound/count-fee proof and native-active prerequisite for independent offline budget-policy edits. All other scope, model, privacy, live and final acceptance gates survive. ADR003–007 remain proposed.

## Context and decision

Strict full-input/count-endpoint billing proof blocked all live work. The owner now accepts a practical estimate-based local controller, **not a mathematical guarantee that the provider invoice is at most USD10**. One shared continuation authority remains USD10; **new dispatches stop when accounted total plus the next reservation would exceed USD8**. USD2 stays unspent contingency: the application does not unlock it automatically.

Use a named practical policy, not `BILLING_VERIFIED=yes` under its former strict-proof meaning. Model remains exact `gpt-6.1-sol`, Responses `service_tier=default`, plan high, SQL/repair medium, `store=false`. No count endpoint, fallback model, extra LLM or new tokenizer dependency. Current applicable conservative rates and their date/source must be documented independently; see [official reference evidence](../operations/H-009/api-references.md).

Estimate the complete assembled request: instructions, input, strict output JSON schema, metadata/history/tools when present, and conservative framing allowance. Retain the full serialized-payload size gate. The byte-derived token estimate and framing allowance are engineering approximations, not exact tokenization or a universal input bound. Both estimate and reservation method must be explicit in trace, code and tests.

Before every sequential network dispatch, atomically validate the pinned shared ledger and reject invalid/negative/nonfinite money; then check `accounted_total + next_reservation <= 8` and durably reserve. Preserve all historical entries and unknown holds, with each attempt accounted as `max(reservation, observed estimated cost)` (not their sum). No retroactive release, independent per-run cap, silent ledger/profile migration or reset. Retain max output32768 including reasoning, operation timeouts60/45seconds, run180seconds, five generation attempts and SDK retries0.

After each response, preserve returned model/tier and numeric usage before typed processing. Usage below the estimate is expected. Usage above reservation, missing/invalid usage or model/tier mismatch preserves facts/hold and stops further dispatch, including automatic retries. A timeout/unknown bill also remains an uncertain hold, never zero. First later authorized generation must be useful S6 work, not a content-free access probe.

## Alternatives and rationale

1. **Retain strict proof blocker**: rejected by owner for this limited I1; unavailable proof prevented useful acceptance work.
2. **Treat an old billing flag as new authority**: rejected because it would falsely imply the old proof was achieved.
3. **Raise cap, free unknown holds, per-launch budgets or consume USD2 automatically**: rejected; none is authorized and all weaken aggregate accounting.
4. **Count endpoint or new tokenizer**: not required and endpoint explicitly forbidden by H-009. A local engineering estimate is the chosen tradeoff, not a claim of exactness.

## Consequences and verification

Residual invoice uncertainty, provider taxes/fees, tokenizer/framing differences and response anomalies remain explicit. USD8 is a local conservative admission threshold, not provider-side enforcement. This policy is I1-only; production needs separate assessment, including the previously required effect of additional LLM stages before adding any.

Offline changes and independent review may proceed with native goal blocked. **Live still requires fresh root `get_goal=active` for the same aggregate**, presence-only secure credential loading, explicit practical policy authority/rates and passing checks. If blocked after the offline checkpoint, the exact owner action is `/goal resume` in the composer of this same Codex session; no fabricated API or manual state/ID edit.

Required regression evidence: USD8 equality and overflow including prior holds, cross-run/restart sharing, reservation-before-dispatch atomicity, invalid config/missing authority/no-network, timeout holds, excess/missing/invalid usage stop, no count call, unchanged old ledger history. [H-009 report](../reports/H-009-practical-budget-I1.md) records actual results and independent verdicts. Real S6→80.00, changed oracle, live UI/full same-run trace and final independent gates remain unproved until performed. No I2–I5, remote/push, OMX update or public-delivery claim.
