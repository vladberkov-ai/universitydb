# H009 bounded cleanup and behavior lock
Only change the live spending gate and shared payload construction. Preserve operation limits,
SQL/domain behavior and historical spending entries. Run baseline suite, add failing practical
budget regression tests, implement, then inspect changed files and rerun full checks.
No network/count/credential access in this lane. Payload bytes plus 1024 framing is an engineering
input-token estimate, not a mathematical tokenizer bound. Reserve 12000 estimated input tokens.

## Fallback smell inventory and selected pass
- Boundary duplication: worker constructed the wire body separately from parent estimate.
  Selected: one shared wire_payload function, no tokenizer dependency or alternate endpoint.
- Unsafe success boundary: spending reconciliation could precede returned profile validation.
  Selected: compute stop_reason first and commit usage + stop atomically.
- Repeated condition: excess/mismatch recomputed twice in provider. Selected: reuse booleans.
- State-machine safety: unknown live response could use historical transient retry.
  Selected: accounting_stop short-circuit before legacy offline retry behavior.
- Deferred: legacy Spending compatibility is required for old receipts/history; no broad rewrite,
  new budget manager, transport abstraction, fallback provider or ledger reset.

Behavior lock: baseline 108 tests passed; first four new practical tests failed before code
with missing practical constructor argument. Expanded targeted tests lock new behavior.
