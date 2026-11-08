# H016 preliminary independent architecture review — BLOCK

Selected actual native message from independent `/root/architecture_review`
(architect). Root persists this orchestration review receipt; not author approval
or a complete private transcript. This precedes final source/full verification.

Independently reproduced through ordinary Agent.run, temporary SQLite and
scripted scope-consuming transport; no network/credentials/canonical mutations:

1. Explicit malformed compact identities disappear: `Show mean for course -1.`
   and `Show mean for course #abc.` return scope={} / global83.33; Library reader
   -1 returns all readers. `domain_support.py:33–38` captures only initial digits.
2. Unsupported natural axis `Show mean for offering ID 1.` returns unfiltered
   success. `domain.py:218–225` guards assignments only; shared filters exclude
   offering_id. Reject unsupported filters, preserve projections/grouping.
3. `Show mean for teacher Lee and teacher Kim, teacher ID 11.` accepts teacher11
   and drops Kim. Union-of-name candidates membership is insufficient:
   `domain_support.py:139–145`. Validate each explicit named mention independently;
   retain one ambiguous catalog label plus compatible ID disambiguation.
4. `student named "Bea Nobody"` / `reader named "Ada Nobody"` are accepted as
   Bea/Ada through prefix matching at named validator and global catalog lookup.
   Validate the complete explicitly quoted value, not its catalog-label prefix.

These violate the accepted no-silent-filter contract, not a demand for universal
NLP. Final CLEAR withheld. Root routed all four to repair with regression-first
proof before further source edits; no green count substitutes for resolution.

## Additional independently reproduced role-ownership BLOCK

After the first repairs, mutate temporary Teachers[11].name to Bea, then ordinary
`Agent.run("Show mean for student Bea in semester S1.")` returns scope
student2+teacher11+S1 and NULL/no_rows. Independent SQLite for requested student2/S1
returns [16000,2,2], mean80.00. Shared global catalog-label matching applies an
explicit student name span to every matching role. Extract owned explicit spans
and exclude them from unqualified matches in other roles; preserve unqualified
ambiguity, ID disambiguation and genuinely requested explicit student+teacher.
This is a demonstrated incorrect population, not a universal-language demand.

## Re-review of recognized quoted syntax — remaining BLOCK

Both independent review lanes confirm the first findings fixed, but the same
full-quoted-value defect remains for already-recognized plain noun forms:
`Show mean for student "Bea Nobody".` and
`Count open loans for reader "Ada Nobody".` select Bea/Ada instead of rejecting
unknown identities. Exact quoted validation recognizes only named/= while another
accepted parser recognizes noun+quoted. Apply one full-span validation contract
to every recognized quoted syntax; no prefix-label fallback.
