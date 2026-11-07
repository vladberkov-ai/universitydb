# E2E verification — current University and Library service

Use the full offline fixture and isolated root in the README. This exact sequence
consumes scripted proposals in order within each dataset's retained session. It is
a real graph/SQLite/UI check, not a real-model language evaluation. Refreshing a page
is not a reliable fixture reset; use a fresh browser session/server for another sequence.

| Order | Dataset / question | Expected |
| --- | --- | --- |
| 1 | University: What is the average grade for Bea (student_id=2) in DB (course_id=1) with Kim (teacher_id=10) in semester S1? |80.00; raw16000/2/2 |
| 2 | University: What is the average grade for Alex? | Choose student1 from IDs1/3, Continue this run→86.67; same run ID |
| 3 | University: For students of the course with the highest mean in S1, show their mean across all S1 courses. | top course2→cohort student1→95.00 |
| 4 | University: repeat question1 | first SQL unknown-column error, one repair,80.00; both attempts visible |
| 5 | University: What is the average grade across all enrollments? | injected PROVIDER_REFUSAL; no previous success shown |
| 6 | Select Library; submit its default open-loan-count question | Ada1, Bob1; count units, no grade scaling |

For every result inspect proposed/validated/executed SQL with safe bindings, raw typed
rows, adapted step results/dependency bindings, and the full same-run trace. Download
JSONL and compare run_id/events/terminal status. During the Alex pause no generated
SQL should have executed; after selection the original question and resume belong to
one run. Dataset changes clear the old answer. Record commit, fixture hash, mode,
question, selection, answer/error and trace when reporting a failure.

M1 mutation/tie proofs and replay/no-extra-calls tests are automated in
[test_i3_dependencies.py](../tests/test_i3_dependencies.py). The fixed browser fixture
checks visibility, not dynamic generation sensitivity. [Final dynamic proofs](operations/H-013/m1-final/manifest.json)
cover F1/F2/tie and same-core Library. [Actual browser receipt](operations/H-013/browser/cp-e-final-attempt2/browser-receipt.json)
records six classes/seven captures on the frozen candidate. Those historical passes
do not claim that a new reviewer has already reproduced them.

## Automated checks

From the checkout, with dependencies installed:
```bash
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q
```

Tests use temporary DB/runtime roots. `test_ui.py`/`test_i2_ui.py` use AppTest; this is
distinct from opening a real browser. Offline provider failures are injected with
explicit provenance. Actual live SQL generation is a separate future evaluation.

## Diagnosing failure

Inspect scope→accepted ResultSpec→SQL/bindings→raw rows→adapter output→answer in the
same trace. Unsafe SQL must not execute; a safe query can still be semantically wrong.
Missing data, NULL grades and zero counts have different meanings. An expired or
foreign continuation fails closed; restart requires a new request. Unknown spending
usage stops dispatch and retains its hold. Never reset the monetary ledger to retry.

The earlier live I1 checks (80.00/90.00 and error/no-stale-result) remain in
[historical live report](reports/H-009-live-I1-closeout.md) and
[owner acceptance](reports/I1-owner-manual-acceptance.md). Their original Russian
questions are preserved; no English expanded-service live pass is implied.
