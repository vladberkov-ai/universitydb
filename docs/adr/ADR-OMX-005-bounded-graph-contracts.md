# ADR-OMX-005 - Bounded graph, clarification and security

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
We need meaningful multistep, errors and continuation; LLM proposals are untrusted, interrupt restarts node.

## Options
Free agent loop; fixed chain without clarification; bounded graph with typed state and checkpoint.

## Recommendation
Bounded LangGraph bycontracts v1: static validate_plan acceptstyped symbolic refs bydeclared ResultSpec; runtime bind_results requirescompleted/consistent/nontruncated dependencies, error→no downstream. InMemorySaver forlocal demo, session-bound idempotent resume, 3 steps+1 repair,5calls,2clarifications; DB readonly/authorizer/limits/watchdog, deterministic formatter.

## Rationale
Limited errors/cost explained by dependencies; free loop is more difficult to debug, chain without clarification violates scope.

## Consequences
After restart resume expired; safety does not prove semantic correctness; limiter/policy also require actual DB testing; We do not promise arbitrary SQL correctness.

## Verification
D1–D3,V1,W1–W3,C1–C5,E1–E7,SQL-policy integration,M1 sensitivity; no pre-interrupt side effects; pause budgets preserved.

## Revision triggers
Durable restart/multi-user requirement, newoperations/dialect, complex>3step legitimate cases.

Related [architecture](../plans/architecture-proposal.md), [contracts](../plans/contracts.md), [checks](../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
