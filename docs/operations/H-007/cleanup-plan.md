# G003 bounded cleaner plan (writer lane)

Scope: only H007 I1 changed source/tests/docs. Installed ai-slop-cleaner skill was read before this helper; no nested workflow, new dependency or broader refactor. Root owns workflow APIs. Independent final reviewers will assess this author's cleanup; author does not self-approve.

## Behavior lock before edits
G002 commit c34e8868d44ac81f60ff66c2f9b1b29b9f01c2d8:64offline tests pass, lint/format/type/compile pass. Regression covers main/changed result, AST/authorizer safety, bounded workers, transient retry/syntax repair, missing credentials, trace fail-before and late terminal, stale answer clearing, explicit offline provenance. Re-run this lock before modifying source.

## Fallback inventory/classification
- Missing key/model/approval → explicit PROVIDER_UNAVAILABLE before worker/network: grounded fail-closed boundary, not canned fallback.
- One transient retry or recoverable syntax repair: grounded bounded behavior with counted attempts, traces and tests; unsafe SQL is never repaired/accepted.
- ScriptedProvider only in tests/developer double-gated UI configuration: explicit injected provenance, not runtime model fallback; no live score.
- DB/SDK subprocess safe errors and kill/reap timeout: grounded external boundary, no raw diagnostics or recovered success; retained uncertain cost.
- Trace failure → no success and only available events returned: grounded fail-safe; late answer/run_end failure tests lock behavior. Terminal-trace secondary failure changes error to TRACE_UNAVAILABLE rather than swallowing a success.
- UI setup failure clears prior result and reports error: grounded fail-safe. No silent alternative DB/provider/model.
No masking compatibility shim, hidden expensive model fallback or synthetic answer found. Any cross-layer/architecture concern goes to active final review, not a new ralplan.

## Planned passes
1. Dead state fields: remove unpopulated State counter declarations that actual code keeps in per-run controller; preserve real budgets and trace counters.
2. Duplication: unify duplicate success/error response-envelope construction at Agent.run's single return boundary. No public behavior change, new abstraction or protocol.
3. Naming/error handling: inspect only; retain distinct explicit failure paths rather than combining away diagnostics.
4. Test reinforcement: run64offline behavior lock after each selected pass and complete checks afterwards. Missing regression discovered while inspecting requires a narrow test before any semantic fix.

UI/design: keep simple native Streamlit layout, explicit profile banner and expanded SQL/rows/trace; no cosmetic redesign. Residual limits remain as documented: synthetic loopback, no hard memory isolation or live acceptance, no second schema/full project.
