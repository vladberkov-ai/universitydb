# H-008 initial independent review — preserved findings

2026-11-07. Scope: frozen checkpoint `cfaf8601b8b985687b45ae4f9792891ee75064f4`, baseline470bc3e. Source: root's actual received independent native results delivered to performer; this is a bounded attributed summary, not a full reviewer transcript or reconstructed task export. Author does not approve itself.

- **code-reviewer: REQUEST CHANGES; two MEDIUM findings**: known-response errors retain stale usage_status unknown / real_provider_called null; installed SDK eager `responses.parse` can raise on truncated/incomplete or invalid-completed JSON before worker receives known status/usage/model/tier. Reviewer independently ran102tests14.13s before correction.
- **architect: BLOCK; SDK ordering HIGH, stale flags MEDIUM**, not flattened to the code-reviewer's severity. Existing holds remain conservative, so no proven monetary cap leak; the blocker is lost known failed-attempt accounting/diagnostics and incorrect failure classification. Architect independently ran102tests13.69s before correction. Trusted parent I/O/narrow intent resolution remain nonblocking concerns.
- Root integration independently102passed13.17s, Ruff/format18files/mypy11files/compile/diff all0 before correction; ordinary passing tests did not expose real SDK ordering.

## Regression-first correction evidence
Performer added real installed openai3.46/httpx2.MockTransport tests (zero external network): incomplete truncated JSON should preserve PROVIDER_INCOMPLETE and known100/32768 usage; completed invalid JSON should preserve known usage before PROVIDER_INVALID_OUTPUT. Both failed before product edits: incomplete became INVALID_OUTPUT, completed-invalid ledger had output_tokens0 despite known32768. Existing simple mocked parsed objects missed this behavior. No dependency update.

Primary path now uses supported Responses.create with explicit strict text.format JSON schema, extracts raw response status and safe known usage, then validates completed output with strict Pydantic. No permissive parsing fallback/schema relaxation. Parent reconciles known usage before rejection; trace flags known/true, while missing usage preserves primary code and returned model/tier metadata with unknown hold; true transport timeouts stay unknown/null. Tests add exact SDK payload, real installed-SDK wire, incomplete/invalid/missing-usage, parent ledger and graph trace assertions. Fresh validation and independent re-review required; this historical REQUEST CHANGES/BLOCK is not rewritten as approval.

Root supported annotation retained findings on existing G004. record-review-blockers was not run because installed gate requires native active while actual goal remained blocked. No fabricated runtime transition or manual state write.
