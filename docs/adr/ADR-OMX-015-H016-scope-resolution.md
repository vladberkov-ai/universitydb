# ADR-OMX-015 — H-016 shared natural identity resolution

2026-11-08. Scoped offline implementation decision under CHAT-058. Accepted
ADR-CHAT-006 semantics, ADR012 limits and the Sol profile remain unchanged.

## Context

H-015's retained pre-provider failures expose a shared input-contract mismatch:
the numeric recognizer accepts `course 3` and `course_id=3`, not `course ID 3`;
the separate unknown-name recognizer then mistakes `ID`/`IDs` for a proper name.
The same helper serves University and Library. Catalog loading is not the cause.
Simply excluding `ID` from unknown-name detection would silently lose the filter,
including when another known name masks a contradictory ID. CP1 regression-first
and the complete retained-input map are recorded separately under H-016.

## Decision and alternatives

Keep three explicit stages in the existing shared helper: extract supported
identity syntax; validate every extracted identity against the adapter catalog;
then resolve one identity or request a catalog-backed clarification. Natural
`entity ID N` (case-insensitive, optional `:`/`=`/`#`) joins the existing compact
and named-key syntax. An explicit malformed/unknown value fails before provider
calls. Identifier projection prose is not a name or an identity constraint;
closed projection syntax must be distinguished before unknown-name validation.
Every explicit mention is checked, even alongside a known name or user choice.
Contradictory distinct IDs fail, and conflicting catalog names/IDs fail; ambiguous
catalog labels retain the existing session-bound clarification.

Reject model-based extraction, fixture/eval aliases, exact-question branches,
provider retry and absent-filter fallback. A blanket `ID` skip is also rejected:
it conceals the missing extraction instead of fixing the contract boundary.
No SQL/template replacement, registry/metric change, dependency, budget/deadline,
SQL safety or clarification ownership change is needed.

## Consequences and validation

This remains bounded supported-form parsing, not general natural-language
understanding. Unknown entities must remain errors and output-column mentions
must not become filters. Regression tests cover case/punctuation, combined
filters, multiple mentions, malformed values, unknown names and catalog ambiguity
for both adapters, through the ordinary Agent entry/compiled graph plus focused
helper tests. Scripted offline plan/SQL transport proves mechanics only; it does
not prove real-model generation or a new live score. Independent review and the
full offline suite remain completion gates owned by root.
