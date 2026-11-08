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

## CP3 full-suite repair: quantified projection

The first root full pipeline on exact CP2f9251a7 failed2/800cases (D03/D04), with
all original evidence retained in verification/final-1. Inspected actual public-
entry JSONL: resolve_scope INVALID_INPUT missingstudent_id,0provider/SQLattempts.
The shared positive output grammar did not admit `show each student ID`, so this
is a deterministic parser regression, not a provider failure. The118focused
proof missed this output form; all64replay cases must accompany edge tests.

Regression-first `quantified-projection-before.txt`:8failed/4passed, comprising
D03/D04, six independently phrased quantified output-column questions in both
schemas, and four missing-target negatives. The minimal grammar edit permits an
optional determiner immediately after a recognized output verb; it does not
restore a global Show fallback or silently ignore a missing target identity.
All four H016 modules and relevant old domain/readiness tests run together before
this iteration's freeze. Root's full/browser/clean-run remain separate gates.
Cleaner check: same existing helper, no new abstraction/dependency/duplication or
fallback; no-op cleanup beyond the bounded grammar repair. Historical frozen
sources/evidence, canonical money, native lifecycle and original locks untouched.

First complete post-fix420test run:419passed/1failed85.60s. D03/D04 and all prior
replay cases passed. The only failure was the newly authored independent control
`Display all student IDs...`: actual trace reports pre-existing unsupported
University query intent, before ID parsing. Correct the *new control's wording*
to supported `Show all student IDs...`, keeping its all-quantifier, projection,
scope and assertions unchanged. No historical expectation or product intent guard
is weakened/expanded. Preserve that attempt in quantified-projection-after.txt;
rerun all420tests to a unique second log, not overwrite it.

The temporary Show-variant run passed420/420 in86.98s, but root requested an
independent contract review before accepting a wording substitution. Both real
reviewer lanes agreed the accepted listing class is not a literal show/list API
(contract metric/listing sections); shared projection grammar already admits
Display/Return/Include. **Supersede the temporary substitution decision**:
restore the Display positive, align University's bounded word-boundary intent
verbs, add Return/Include positives and cross-domain/write negatives. Do not add
metrics, SQL operators, generic by/per intents or new aliases. The final run uses
all four H016 modules plus prior graph/readiness/Library/DB checks; root will run
the entire repository suite again on the new committed candidate.

Final listing-consistency verification: **328passed/45.21s**, including all four
H016 modules (all64replay cases, independent NL/edge controls and AppTest), plus
prior graph/readiness/Library/DB checks. Ruff check/3files format/mypy2production
modules/compile/diff checks PASS. Source/test/harness component SHA256 values are
recorded in listing-consistency-components.sha256. Both independent reviewer
lanes accepted the bounded grammar/intent rationale at source level; root owns
new exact-SHA full suite, browser, clean-run, preservation and final verdicts.
The prior f9251a7 full failure and all intermediate attempts remain preserved.

## Actual browser attempt1: transition harness repair

Attempt1 on3bc1088 passed six University states, then timed out waiting for Ada in
Library-filter. Its receipt proves owned browser/server stopped, canonical runtime
unchanged and no temporary spending ledger. Preserve the entire attempt unchanged.
The failed Library question/body/server log were not retained in that attempt, so
its exact submitted question and a race as the actual cause cannot be established.

A concrete harness defect is proven independently: the previous error question
`What is the average grade across all enrollments?` already satisfies the old
`"Bea" not in textbox` assertion before selecting Library. UI source uses
schema-specific `question_{schema_id}` keys and clears prior result/agent on schema
identity change. A focused temporary AppTest reproduced that old guard's false
positive, then verified the new Library key/default, cleared result and successful
readerID1→Ada1 execution after the actual synchronous dataset rerender.

NEW H016 harness only: wait positively for the exact Library default question,
absence of the prior runID in body, and idle render before filling/submitting the
filter. No arbitrary sleep, retry, skipped question, timeout-ceiling change or
product code repair. Preserve future failure DOM/body/current question/screenshot
and available downloaded trace before closing the browser; persist server log and
failed temporary JSONL traces before removing the temporary directory. Diagnostics
capture errors are recorded and the original browser failure is re-raised.
Original H014 harness, product source and attempt1 evidence remain unchanged.

Verification: existing H016 AppTest suite8passed/3.19s; exact prior-error→Library
transition proof1passed/1.77s. The temporary test's source/output are retained as
regression evidence (`browser-harness-transition-proof-source.txt` and matching
output); it is not a new product test or a real browser pass. Ruff/format/compile
and diff checks pass. Independent code-reviewer reports CLEAR_TO_CHECKPOINT for
this bounded harness fix; root must run a fresh actual browser attempt and exact-
SHA clean/full verification before final acceptance. The attempted browser cause
remains unproven until new diagnostics/evidence, not retrospectively relabeled.

## Actual browser attempt2: generic new-run capture boundary

Attempt2 preserved diagnostics prove a different harness defect: seven states,
including readerID1→Ada, passed; `library.jsonl` still contains that prior filtered
question/runID while failure_question is the newly filled all-reader question.
Both results contain Ada, so matching the expected alert and observing an already
idle status widget can accept stale pre-submit output. No product failure is
inferred from that stale downloaded trace. Attempt2 evidence remains unchanged.

Repair every new-run submission through one helper: retain the currently rendered
run UUID, fill/verify the question, click Run, wait for the previous UUID to leave
the rendered body, positively await a run caption, then await idle and require a
different UUID. Retain that submitted UUID and require the downloaded trace to
match it in addition to existing question/outcome/sequence checks. First runs
require a positive caption too. Clarification resume remains deliberately outside
this new-run helper and must keep its original run UUID. No sleeps, retries,
question edits, product edits, weaker assertions or timeout increase.

Focused scheduling regression executes the actual helper AST with a fake browser
that keeps the prior Ada result visible after click:2passed/0.77s (same-answer
replacement and initial submission), with source/output preserved under
regressions/browser-new-run-proof*. This tests harness control flow, not an actual
browser pass. Ruff/format/compile/diff pass. Root owns fresh actual browser and
tracked-archive full/static/oracle/seed/preservation verification on the new SHA.
Independent code-reviewer inspected the generic UUID readiness/binding delta and
reported conditional CLEAR_TO_CHECKPOINT; final real browser evidence is pending.
