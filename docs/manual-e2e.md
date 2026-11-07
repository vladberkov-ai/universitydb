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
