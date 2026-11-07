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

## H-014 clean-readiness follow-up — preserve grade prose and quantifiers

The clean readiness runner on candidate `331eb5a` caught a regression not covered
by its 457-test full unit/static pass: `Show mean grade grouped by course across
all enrollments` became INVALID_INPUT before calls. Independent architect also
reproduced teacher grouping, `Mean grade excluding ungraded enrollments` and
Library `for each reader` / `for every reader` regressions relative to `6cc7ad3`.
These are fresh readiness findings, not held-out eval tuning or semantic changes.

Before follow-up source edits, compiled graph/resolver controls demonstrated
**8 failed, 23 passed**. See [failure evidence](../operations/H-014/scope-fix/grouped-quantifier-pre-fix.txt).
Root cause: optional consumption of `grade(s)` exposed arbitrary following grade
prose as a supposed name; Library explicit target capture treated quantifiers as
unknown names. Do not fix by adding arbitrary prose words to a growing allowlist.

Choose explicit mean/average [grade(s)] for/of NAME first, original immediate
mean/average token shorthand second, possessive form third. Because explicit target
forms match first, Zoe cannot be hidden behind semantic `grade`. Ordinary grouped
or exclusion grade prose preserves the original immediate semantic token behavior.
Library consumes only explicit each/every quantifiers ahead of the target token;
reader(s) remains semantic vocabulary, while `for each Zoe` still fails closed.
No general NLP platform, global-answer fallback, metric change or dependency.

Known-valid group/grade/count controls and original unknown/known identity controls
must pass together. Parent independently re-runs tracked clean-readiness E2E/full
suite/browser on the next exact source candidate; prior failed captures remain.

Independent code-reviewer then caught that the first proposed split lost the bare
`Mean grade Zoe` / `Average grades Zoe` guard. New compiled unknown/known controls
before the second edit showed **2 failed, 35 passed**, separately preserved in
[bare-grade failure](../operations/H-014/scope-fix/bare-grade-pre-fix.txt).
The corrected grammar therefore retains a grade(s)+target branch. Only contextual
`grouped by <GROUPS-derived noun>` and `excluding ungraded enrollments` match a
prior semantic-grade branch. Malformed `grade grouped Zoe` / `grade excluding Zoe`
remain INVALID_INPUT before provider calls. GROUPS supplies registered nouns;
there is no growing allowlist of arbitrary prose words and no global-name fallback.
