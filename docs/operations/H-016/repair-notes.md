# H-016 repair implementation notes

Scope: shared adapter identity parsing and directly affected adapter guards;
no provider/API/count/credentials, money, historical-evidence or lifecycle writes.
ADR015 was recorded before implementation. Source changes wait for root's CP1
regression-first checkpoint confirmation. Tests and final results are appended
here after execution; root owns campaign integration and final verification.

## Pre-code cleanup/repair plan and independent design review

1. Lock the boundary with natural Agent-entry regressions before source edits:
   `test_h016_resolution_edges.py` adds 28 independent punctuation/case/repeated-
   identity and masked-unknown variants; pre-fix **8 failed, 20 passed**, retained
   in `repair-edges-before.txt`. Root's separate matrix is independently owned.
2. Inventory existing fallbacks: absent entity mentions intentionally mean all;
   explicit malformed/unknown mentions may not take that path. Existing global
   name lookup and catalog ambiguity/choice logic remain, but every extracted
   mention must validate before selection. No new permissive fallback.
3. Repair one smell: inconsistent identity grammars in numeric extraction and
   unknown-name detection. A small shared parser/helper owns ID-marker handling;
   no blanket `ID` skip, new dependency, eval alias or provider workaround.
4. Rerun new/old boundary and graph tests, inspect the focused diff, and remove
   duplication/debug residue without changing unrelated behavior. Final cleaner
   can be a documented no-op if no actionable smell remains; rerun regressions
   after the review.

Independent root design review (native message, 2026-11-08): root read ADR015 and
approved its bounded design pending the CP1 regression-first checkpoint. Source
edits remain prohibited until root confirms that checkpoint. This is design
review, not the final independent code/architecture verdict.

## Prompt coverage

`prompts/repair-task.txt` preserves the exact initial received task projection
(native root-to-repair message). No secret/private path was present. Later native
followups are summarized here: root approved design then authorized source edits
after CP1 `5bbce8c`; requested context-sensitive projection/compact punctuation
negatives, full downstream browser harness, and this prompt record. Hidden system
instructions, tool logs and full native conversation are not exported. Context
files are read evidence, not additional actual user instructions.

## Implemented shared boundary and verification

Source changes are limited to `domain_support.py` plus case-insensitive unsupported
assignment guards in both adapters and University's ordinary `over` scope
preposition. The shared parser handles natural numeric/string-ID markers,
case/punctuation, compact forms and identifier-column prose. Every extracted
identity/named mention validates before selection/clarification; malformed,
conflicting, unknown, empty-catalog and unsupported partial-list identities fail
closed. No runtime prompts, SQL/result registry, model, limits or money changed.

The empty-catalog defect was reproduced against CP1's actual helper: explicit
`student_id=1` with `{"student_id": []}` returned `{"student_id": 1}`; repaired
helper rejects `Unknown student_id: 1`. The no-catalog direct-call compatibility
remains, but real Agent startup always supplies the catalog.

Fresh checks during repair:
- New natural/edge matrix after punctuation/target repair:69passed/12.59s.
- Existing domain/readiness/Library/DB subset:220passed/68.05s.
- Expanded integrated subset:297passed/75.21s (before final five numeric-list
  negatives; not represented as final full suite).
- Final focused edge suite:46passed/5.87s.
- Ruff check/format and mypy of all three changed production modules passed.
- Independent test-engineer stable108 suite:108passed/27.63s with unchanged
  source/runtime-prompt/test hashes across run (separate retained receipt).

## Bounded ai-slop-cleaner result

Installed skill read and applied after the pre-code plan and independent root
review. Scope: three production modules, assigned edge tests and NEW browser
harness. Masking fallbacks addressed by root-cause repair: ID skip without parsing,
known-name masking of malformed/unknown mention, empty-catalog acceptance and
first-value-only scalar filter loss. Intentional absent-filter all-scope and
no-catalog direct-call compatibility remain narrow, documented and tested.
Passes1–3 found no dead code, speculative abstraction or safely removable duplicate
production branch after repair; **no-op cleanup**, avoiding late behavioral churn.
Pass4 reinforced negatives before the final check. The copied browser run/capture
is deliberate test-only reuse of frozen H014 behavior: importing its monolithic
closure cannot extend a second Library case safely. The historical file stays
unchanged; no new shared framework is introduced. UI/design cosmetic findings:N/A.
Final source is frozen for root's independent review/full checks; real-model
quality and unsupported free-form language remain risks, not fallback excuses.

The NEW H016 browser harness has not been run by this lane: natural questions pass
ordinary UI parsing, injected proposal fixtures remain an explicit downstream
boundary, outbound browser requests abort, all screenshots/downloads go only to
requested new output, and owned server/browser teardown and canonical-runtime
hash preservation are inherited from the proven harness. Root controls execution
after candidate commit and static/full checks.

Post-cleaner fresh verification: **82passed/12.34s** in
`regressions/repair-final-focused.txt`; Ruff check PASS,5files format PASS,
mypy3production modules PASS, Python compile PASS. Production freeze SHA256 is in
`regressions/repair-source-freeze.sha256`. Root's later full/clean-run and browser
results must identify their exact executable commit separately; these focused
checks are not a full-suite or live-accuracy claim.

## Independent architect blocker iteration

The previous source freeze was preliminary and is superseded by this iteration;
its evidence files remain unchanged. Root forwarded independent architect BLOCK
findings, and new tests were written/run **before** dependent source edits:
`architect-boundaries-before.txt` records8failed/1passed. Finding→repair/tests:
- Compact negative/hash-malformed tokens: capture malformed marked tokens for
  validation, not only digit-starting valid tokens.
- Unsupported natural ID axis: shared adapter-fields guard rejects an actual
  identity constraint, preserves projection-only/grouping syntax.
- Multiple name mentions: retain per-label-span candidate sets/intersection;
  Lee+Kim cannot union into a silently selected teacher. Alex's same-label
  ambiguity and compatible explicitID remain covered by positive controls.
- Quoted unknown name with known prefix: whole quoted-label equality, with new
  positive multiword labels in both schemas and no fixed-name alias list.

Additional bounded cleaner review after repairs: no new masking fallback or
unnecessary compatibility layer; no-op style cleanup after regression-first
boundary changes. No browser run or commit occurred while findings were open.

## Independent code-review HIGH iteration

Additional RED5failures were retained before dependent changes in
`code-review-boundaries-before.txt`: quoted shorthand unknowns, missing ID after
`in`, explicit excluding/except identity operators. The shared resolver validates
full quoted for/of targets, uses *positive* output-column grammar rather than a
growing target-preposition list, and rejects unsupported identity exclusions
instead of converting them to equality. Known/ambiguous quoted Library targets
have real graph pause/resume positive controls. The existing supported grade
exclusion wording remains untouched.

After this repair the focused99case matrix passed/12.95s; one final quoted
positive/resume control was then added. The architect subset314passed/72.71s was
an intermediate run, not a final candidate proof (source advanced during the
review iteration). Final integrated output is retained separately in
`review-boundaries-final.txt`. Root owns independent verdicts and commit freeze.
The bounded cleaner was reapplied as a no-op after these fixes: two named-mention
grammars serve distinct explicit-name and generic-target boundaries, not a
permissive fallback. No debug or fixture-specific product branches remain.

## Explicit role-ownership iteration

Independent architect found that global label matching still applied one explicit
student-name span to a same-named teacher. Before repair, collision/multiword
controls produced2failed/1passed (`role-ownership-before.txt`); the passing control
explicitly requested both roles. Replaced duplicate per-field global scans with
shared catalog-backed role/span/candidate-ID extraction. Declared role owns its
span, preventing other fields from claiming a contained label; unqualified labels
and per-mention intersections preserve ambiguity/compatible explicit IDs. This
is the final general name-resolution mechanism, not merely an ID-regex skip.
The cleaner pass removed the now-redundant per-field scanner while keeping
separate lexical malformed/unknown-name validation and catalog choices. No broad
fallback, new dependency or exact-question branch was added.

## Final unified span boundary

Remaining independent findings were locked before repair:
`unified-ownership-before.txt`3failed/1passed (plain nounquoted suffix unknowns,
quoted S1-name leaking into semester); `equality-operators-before.txt`4failed
(canonical unsupported operators); `typed-id-name-before.txt`3failed/1passed
(natural/canonical/compact ID11 mistaken for the different teacher named11,
explicit quoted numeric name remains valid).

One extraction now owns complete recognized quoted-name spans and explicit typed
ID-value spans, supplies role-specific visible input to both ID lexer/name guard,
and filters catalog-name matches. Typed ID spans never become name candidates,
even in the same role. Compact-ID regex is reused by extraction and ownership.
Explicit numeric-looking quoted names remain names. Natural nounquoted variants
and duplicate-label continuation are positive controls in both schemas.

`unified-ownership-focused-after.txt` is an **intermediate invalid evidence log**:
two own process attempts overlapped while one repair advanced and wrote the same
path, producing NUL/duplicate output. It is preserved, not proof of final status.
Final tests use the unique `final-typed-owned-focused.txt` after all earlier own
processes finished; no masking, timeout increase or broad process kill was used.
Root observed concurrent scheduling delay independently; no unsupported causal
claim is made. Final static/hash records follow below. No browser/full suite was
launched in this worker lane while root serialized final verification.

Final worker freeze proof: **118passed/14.18s** in the unique final focused log;
Ruff check PASS,5files format PASS,mypy3production modules PASS,compile PASS and
diff whitespace PASS. `final-candidate-components.sha256` records all executable
source/test/browser harness hashes. Independent code-reviewer inspected the latest
shared helper and reported **CLEAR_TO_CHECKPOINT** for all known source findings,
conditional on these checks. Independent architect previously closed the known
architecture findings through27targeted passing checks; root retains final
APPROVE/CLEAR/full/browser/clean-run/preservation gates. No final live claim follows.
