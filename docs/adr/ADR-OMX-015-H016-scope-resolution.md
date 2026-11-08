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

## Implementation-boundary follow-up before candidate freeze

Independent regression/root attacks found further instances of the same silent
scope-loss class. Validate *each* ID assignment/named mention, not merely the
first or only when no known label exists. Keep present-but-empty catalogs distinct
from direct legacy `resolve(question)` with no catalog: an explicit ID cannot
exist in an empty catalog. Adapter unsupported-assignment checks casefold and
match case-insensitively; otherwise uppercase unsupported filters evade rejection.
Natural semester ID syntax uses the adapter's existing string-ID grammar, so a
valid standalone S1 cannot hide malformed `semester ID nonsense`.

The scalar-filter contract rejects compact/marked numeric lists rather than
binding only their first element. Terminal punctuation is consumed as punctuation,
not a reason to lose compact IDs. Projection continuation grammar is contextual:
`for/of entity ID` is a requested identity (missing value fails), while column-list
conjunctions, explicit output references and `Which course IDs have ...` are
projections. Ordinary `mean over ...` uses the same semantic preposition treatment
as existing `mean across ...`; no new metric or known-name alias is introduced.
These changes are backed by independent natural-entry graph tests, not question
IDs, H015-specific aliases or answer fixtures. Full independent review remains
root-owned.

## Independent architecture BLOCK repair

Before candidate commit the independent architect proved four additional failures
through ordinary Agent entry: malformed compact IDs disappearing, an unsupported
natural offering-ID filter disappearing, distinct explicit teacher names unioned
instead of constrained, and quoted unknown labels accepted by a known first-word
prefix. New controls first produced8failed/1passed; the already-rejected Library
book filter is retained as a negative control. Historical evidence is unchanged.

Repair compact extraction at its boundary (capture signed/hash-marked tokens for
validation, not just valid digits). Reuse the shared ID grammar to reject actual
unsupported adapter axes while leaving projection-only/grouping mentions alone.
Represent each matched catalog-label span by its candidate-ID set and intersect
independent spans; an explicit ID or user choice must belong to every set. Prefer
a full label over a contained shorter label. This preserves Alex's {1,3} ambiguity
and explicit-ID disambiguation but cannot silently discard Kim in a Lee+Kim
request. Validate the *entire* quoted explicit name against catalog aliases before
normal matching. New positive fixtures mutate both schemas to multiword catalog
labels, independently of H015 names/questions. These are general fail-closed
boundary repairs, not new domain rules or an accepted live result.

## Independent code-review HIGH repair

Further regression-first controls reproduced5failures: quoted for/of Library
shorthand unknowns unfiltered; missing ID values after `in` losing that filter;
and explicit excluding/except identities misread as equality. Retained RED output
is separate from the architect iteration. Whole quoted for/of targets now validate
against current catalog labels before per-entity resolution. Known/ambiguous
quoted targets use unchanged catalog choice/continuation.

Projection recognition now has positive output grammar (direct show/list/which/
include/display/return/showing, grouping by/per, enrollment-row column lists,
continued identifier lists or explicit output/column suffix). A generic earlier
`Show` is not proof that a later `in course ID` is output. This avoids indefinitely
adding target prepositions. Registered identity filters remain equality-only:
explicit not/excluding/except/without identity requests fail INVALID_INPUT rather
than invert intent into equality or implement a new operator. `excluding ungraded
enrollments` remains accepted grade prose, not an entity exclusion. No generated
SQL or domain metric changes follow.

## Explicit name-span role ownership

A second independent architect check mutated teacher11 to the student's existing
label Bea. `student Bea` incorrectly applied both student2 and teacher11 because
label matching was still global per field. Regression-first collision and
multiword-overlap controls failed2/3; requesting both roles explicitly was the
passing control.

Use one catalog-backed mention representation, keyed by adapter field and source
span with candidate-ID sets. An explicit role prefix (`student`, `teacher`, etc.,
including named/key forms) owns its catalog-label span. A different field cannot
claim a contained match from that owned span. Independent matches then feed the
same intersection/ID/choice validation; unqualified labels retain the existing
ambiguity behavior. Prefer this small shared extracted-span boundary to separate
cross-role exception scanners, changing catalog aliases, or silently dropping a
known label. Positive controls request both roles with the same text, mutate a
multiword student label containing the teacher label, and preserve Alex+explicitID.
No result schema, SQL, domain semantics, provider or budget change is needed.

## Unified quoted/typed span boundary

Independent review found two incomplete ownership channels: a teacher explicitly
named `S1` also leaked into standalone semester-ID extraction, and plain noun+
quoted forms still used prefix matching. One shared extracted-span boundary now
validates complete quoted values for all recognized role/name and for/of forms,
then supplies role-specific visible input to ID lexing, name guards and catalog
matching. Mask other-owned spans without changing offsets; a separately requested
semester outside the quoted name still applies. Do not add a second quote-only
bypass scanner or treat a matching first word as a full catalog identity.

Typed ID-value spans are also distinct from names, even in the same role: with a
teacher's label `11`, natural/canonical/compact teacher-ID11 must refer to ID11,
not also to the teacher whose *name* is `11`. Explicit `teacher named "11"`
continues to select that name. Compact-ID extraction is shared, not duplicated.
Canonical inequality operators (`!=`, `<>`, `<`, `>`, `<=`, `>=`) fail at the same
equality-only boundary, rather than disappearing. Regression-first failures and
positive mutation/ambiguity controls are retained separately under H016.
