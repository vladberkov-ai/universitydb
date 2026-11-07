# ADR-OMX-013 — H-014 named-target fail-closed boundary repair

2026-11-08. Scoped defect repair under H-014 v2, not a new domain/architecture
acceptance. Accepted ADR-CHAT-006 semantics and ADR012 contracts remain unchanged.

## Context and evidence

Independent CP-R1 audit found unknown target shorthand becoming an absent filter:
`What is the average grade for Zoe?` and `How many open loans does Zoe have?`.
Before source edits, actual compiled graph/SQLite regressions returned unfiltered
success for both unknowns while both known controls passed: **2 failed, 2 passed**.
See [recorded failure](../operations/H-014/scope-fix/pre-fix-pytest.txt).

## Choice, alternatives and rationale

Extend the existing adapter-owned bounded target guards: optional grade(s) in
mean/average for/of forms; possessive grade/loan forms; explicit Library does NAME
have and for/of forms. Validate captured target vocabulary against current catalog
labels/aliases; preserve existing catalog identity/ambiguity processing and reject
unknown targets before planning/generated SQL. Preserve common non-target Library
prose by retaining the original capitalized bare-name shorthand branch.

Do not add a generic NLP layer, model-based resolver, fallback/global query or
provider retry. Those alternatives expand scope or permit precisely the silent
scope loss being repaired. No new dependency, accepted metric, budget or limit.

## Consequences and validation

This is a closed supported-form boundary, not a claim of universal language
understanding or real-model accuracy. Unknown supported targets terminate
INVALID_INPUT with no answer/provider/SQL and terminal JSONL trace; known controls
retain scoped success. Existing ambiguity/current-semester/filter combinations,
Library zero/unit/isolation and real graph/continuation/UI suites remain required.
Root owns independent final re-review and exact clean-checkout full verification.
