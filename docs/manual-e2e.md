# Manual E2E — supported I1 scope

Follow the root README to select offline or live mode. The server is local-only and
is not hosted by this repository. Record tested commit, mode, question, answer,
run_id and downloaded JSONL for a failure report; never attach credentials.

## 1. Original S6 (both modes)
```
What is the average grade for Bea (student_id=2) in DB (course_id=1) with Kim (teacher_id=10) in semester S1?
```
Click "Run". Expected 80.00; two enrollment grades 6000 and 10000 hundredths,
sum_units16000, graded_count2, enrollment_count2. The average is 16000/2/100.

## 2. Independent changed input (LIVE only)
```
What is the average grade for Alex (student_id=1) in DB (course_id=1) with Kim (teacher_id=10) in semester S1?
```
Expected 90.00; raw 9000/1/1. The explicit student ID matters: the seed has two Alex
students. Offline fixture responses are fixed to case 1 and do not test this variation.

## 3. Trace inspection (both modes)
Expand “SQL and safe parameters”, “DB typed rows” and “Full same-run trace”.
Check Enrollments JOIN Offerings, bound student/course/teacher/semester predicates,
raw rows consistent with the answer, and one run_id across input/nodes/attempts/SQL/
DB/answer/terminal result. Download «JSONL trace». In live mode inspect effective
Sol model/effort/usage; offline traces must remain labeled injected. A different
run_id or missing final result is a failure, even if the answer text looks correct.

## 4. Error clears previous success (both modes)
After a successful answer enter `unsupported` and submit. Expect INVALID_INPUT,
no stale 80.00/90.00 success panel, and no SQL/DB execution for that failed run.
This input has no four-filter scope, so the model should not be called. Restore case 1
to check recovery; that new successful live submission is another paid run.

## Scope and diagnosis
Only the explicit four-filter scalar mean is supported. Arbitrary counts/rankings,
implicit semesters, ambiguous-name conversations and multi-step questions are future
work; a plausible answer to them is not evidence of support.
PROVIDER_UNAVAILABLE: check key presence/model/explicit live gates locally without
printing the key. RESOURCE_LIMIT/BUDGET_EXCEEDED: inspect safe trace/ledger, retain
holds and stop; do not reset the ledger. A timeout may have incurred a charge.
SQL_INVALID: inspect proposal/error/repair attempts. No-data/NULL semantics have
offline coverage but are not part of the two published live success cases.

The owner reported these four live checks passed on 2026-11-07. Instrumented earlier
live evidence and screenshots are linked from examples/README.md; these are separate
sources, not a replay or fabricated record of the owner's actions.

The questions above are English translations for reviewer use. The preserved live evidence contains the original Russian questions; no new English live pass is claimed. Offline acceptance of the English default question is checked separately.

## H-013 offline checkpoint foundation (current local development)
The historical I1 instructions/results above remain preserved, not replayed. Current
CP-B UI has a University/Library dataset selector, retained agent within the selected
server session, and separate disposable DBs. Use the README's **temporary offline
root** before AppTest/browser checks; never direct test setup at the actual runtime
ledger. A normal profile never falls back to fixtures. Explicit test mode accepts a
legacy scripted list or schema-keyed lists (`university-v1`, `library-v1`), and
controlled `injected_error` objects are test-only failure provenance, not question inputs.

Inspect SQL/bindings, raw typed DB rows, adapted step results/dependency bindings and
full same-run JSONL. New questions/errors/dataset changes clear prior answers.
Checkpoint clarification and browser M1/Library/repair/error proof are later H-013
checkpoints, **not claimed by this foundation note**. The offline tests use real
SQLite/compiled graph with scripted proposals; no real-model accuracy is inferred.

### CP-C actual offline continuation and errors
With a fixture prepared for the requested scope, “What is the average grade for
Alex?” offers Alex IDs1/3 before generated SQL/provider calls. Select ID1 and click
“Continue this run”:86.67, same run and a visible resume event. “Current semester”
offers configured catalog semesters rather than inferring a date; TTL900s and
server-session/schema/data/policy identities bound continuation. No restart recovery
is promised. Switching dataset clears the prior answer and uses its own default
question; Library duplicate labels expose IDs, counts remain unscaled including zero.

The UI SQL panel now shows **proposals as proposals**, including rejected/repaired
SQL, separately from validated/executed statements. Inspect every attempt plus raw
rows, adapted results/dependency bindings and full same-run download. Controlled
refusal/missing-DB/expired continuation errors never display a prior success.
[CP-C browser receipt](operations/H-013/browser/cp-c-attempt3/browser-receipt.json)
records actual injected success/clarification/repair/error with focused panels;
[prior socket-blocked attempt](operations/H-013/browser/cp-c-attempt1/browser-receipt.json)
remains provenance. These are not live/model-quality claims. Final frozen-candidate
M1/Library/browser/review proof remains CP-D/E, not conferred by this note.

### H-013 repaired-candidate current verification cutoff
The operative local offline candidate is `f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0`:410
offline tests121.29s plus Ruff/format32/mypy14/compile/diff passed. Earlier CP-C/CP-D
cutoffs above remain history, not the present capability limit. Actual same-process
M1 F1/F2/tie/checkpoint-resume and Library portability are in the final manifest;
request identity/TTL/owner-trace/DELETE-journal/DB availability repairs respond to
actual independent blockers, not waived by the earlier383pass. Final frozen-source browser passed six classes/seven captures; fresh
independent code-reviewer APPROVE and architect CLEAR received; root native COMPLETE/strict PASS (13/13) now confirmed. No real-model
NL accuracy/live/count/credentials/spending/push claim; I4+verification-I5/publication/
defense remain later.
[Exact-process structured proofs](operations/H-013/m1-final/manifest.json).
