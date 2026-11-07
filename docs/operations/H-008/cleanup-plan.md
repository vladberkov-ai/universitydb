# H-008 bounded change / cleanup plan
Writer: delegated performer. Independent reviewers remain root-owned, not self-approval.

Baseline behavior lock:75 tests passed9.86s before edits. Preserve graph/DB/formatter, exact S6, stable-lock ledger, existing evidence. Scope: central configuration, provider/worker, graph attempt accounting and directly affected tests/docs. No dependency changes or paid calls.

1. Replace duplicated token/time/model policy literals with one frozen validated operation policy. Reject unknown operations/model/config and schema mismatch before client/network. Keep repair through sql+previous_error; trace logical repair explicitly.
2. Pass exact reasoning effort/default service tier/store false/strict typed schemas to Responses. Synchronize parent watchdog, SDK timeout, run/call/token ceilings and pre-call reservations.
3. Preserve ledger version1 monetary profile and all old holds; per-attempt reserve accepts policy token bounds without resetting history. Test continuation under unchanged monetary profile, reject rate/model/cap drift.
4. Reinforce mocked payload/retry/repair/no-call/timeout/accounting tests; full offline checks; bounded cleanup pass only on changed files.

Fallback inventory: explicit transient retry and syntax repair are grounded counted external fail-safe paths; missing credentials/config, malformed ledger and trace errors fail closed. No masking model fallback or hidden canned result. UI/design unchanged. No new abstractions beyond the requested small configuration boundary; no new dependencies.

## Bounded cleanup result (writer, not approval)
Resolution gate: no new fallback/model substitution; explicit billable retries remain counted and uncertain holds retained. Dead-code pass: no unrelated deletion justified. Duplicate-policy pass: removed scattered output/timeout literals from graph/provider/worker into one profile; default legacy reserve bounds intentionally remain in Spending for tested old-format continuation, while production calls pass reviewed operation bounds explicitly. Naming/error pass: logical repair is explicit; returned profile mismatch and known incomplete/refusal usage preserve accounting. Test reinforcement adds exact SDK/strict schema/config/no-call/continuation/error/retry/repair limits; full fresh suite follows. UI/design unchanged. No new dependencies, generic framework, swallowed ledger corruption or author self-approval. Remaining risks: provisional live limits, heuristic token estimate requiring live preflight verification, local trusted synchronous I/O and narrow NL resolver; independent root reviewers must assess this writer's plan/diff separately.
