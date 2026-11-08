# H016 preliminary independent code review — REQUEST CHANGES

Selected actual native messages from `/root/code_review` (code-reviewer), not
performer self-review or a complete private transcript. Root records this
orchestration evidence. Final verification/review remains pending.

Independent ordinary Agent.run/temp SQLite/scope-consuming scripted transport
reproduced HIGH no-silent-filter defects, on inspected working source revisions:

1. `Count open loans for "Zephyr".` succeeds with scope={} and all Ada/Bob rows,
   two calls. `library.py:116–120` target lexer ignores quoted shorthand. Validate
   complete quoted target against catalog; test known/unknown/ambiguous forms.
2. `Show mean in course ID with teacher ID 10.` succeeds with teacher10 only,
   silently omitting course. `domain_support.py:56` target context recognizes only
   for/of, classifying missing ID as projection. Reject malformed target contexts,
   preserving genuine output-column mentions.
3. Reviewer additionally confirms `Show mean for course ID 1 excluding student ID 2.`
   becomes equality student2/course1, the opposite requested population. Current
   accepted scalar-filter grammar is equality-only. Root requests narrow rejection
   of unsupported negated identity filters, not new operator semantics; accepted
   `excluding ungraded enrollments` prose must remain valid.

Architect's separate four findings remain independently tracked. Root routed all
new findings to regression-first repair. No full-suite/test count waives them;
final APPROVE withheld until source repair and complete final evidence.

## Re-review — first findings fixed, same quoted-form HIGH remains

Original two HIGH examples and unsupported negated identity now fail closed with
zero calls; accepted excluding-ungraded prose succeeds. Both reviewers independently
confirm plain entity+quoted unknown suffix still selects the known prefix:
student "Bea Nobody" / reader "Ada Nobody". Strict exact quoted validation applies
only to named/=, inconsistent with recognized natural quoted forms. Generalize
full quoted-span validation rather than special-casing these example strings.

Root additionally reproduced a cross-channel span-ownership bug: on a temporary
teacher-name S1 mutation, explicit teacher named "S1" also injects semesterS1.
Ownership must govern ID-token extraction as well as catalog-name matching. Root
routed public-Agent regression proof and common-boundary correction to performer.

## Typed-span classification MEDIUM at source re-review

Five outstanding negative examples now fail INVALID_INPUT before calls and accepted
grade-exclusion prose succeeds. Reviewer independently found a valid-fixture type
collision: rename teacher10 label to text `11`; natural teacher ID11 is then
misread as both scalar ID11 and catalog-name teacher10, causing false conflict.
Explicit ID-value spans must not contribute catalog-name candidates, even in the
same role. Explicit quoted numeric names remain names. Root requested narrow
regression-first typed-span repair before final freeze, not an alias workaround.
