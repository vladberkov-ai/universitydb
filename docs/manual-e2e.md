## Publication update — 2026-11-08

The owner authorized publishing completed H015/H016 evidence and current English
reviewer documentation. The tested H016 executable remains `58f2fe9`; later
documentation commits do not claim a fresh full product run. New product API calls,
spending changes and a new live campaign remain outside this delivery. Historical
no-push/pending statements below describe their original cutoffs.

## H016 natural-input repair verification — 2026-11-08

[H016 report](reports/H-016-scope-repair-offline.md) is the current repair/evidence
index; the H013/H014 sequences below remain historical scripted fixtures, not
proof that arbitrary natural questions work. H016 tests must start with the
original natural question at `Agent.run` or the UI, without injecting expected
scope. The explicitly scripted boundary is provider plan/SQL only. A valid run
retains every filter, validates catalog identity, executes the compiled graph on
a temporary DB, and exposes actual SQL/bindings/raw/adapted rows and full trace.

The regression matrix includes numeric ID markers (case/punctuation/combined
filters), ID/IDs output projections, conflicting/unknown identities, ambiguous
names with session-bound resume, NULL/zero/empty results, all top ties and actual
upstream dependencies, University and Library. Unknown/malformed inputs should
fail correctly before provider calls, not be coerced to successful SQL. Do not
silently rewrite questions to canonical `student_id=2` to avoid the parser.

The8affected H016 AppTest checks passed at an intermediate pinned source; the3bcfull suite now passed815checks with157independent oracle/static.
The58f2candidate changes browser readiness/capture only; actual browser attempt3now passed8states with current question/run/trace
binding and owned process teardown. Exact58f2archive815full/static157oracle/clean-run and1632preservation passed.
Independent final APPROVE/CLEAR and root actual native COMPLETE/strict PASS4/4
are confirmed; real-model validation remains pending. Current repaired executable candidate is `58f2fe9b955eb25cb5a0ee2a9e1d967a60cdcc32`. Use only owned temporary fixtures/runtime; keep credentials absent, live
approval off and external tracing disabled. Do not read/copy/mutate the canonical
money ledger. Stop only servers/browser processes launched for this verification.
Historical H015 corrected10/48 is unchanged; offline regressions never establish
a replacement live score or authorize another campaign.

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
checks visibility, not dynamic generation sensitivity. [Final dynamic proofs](operations/H-014/clean-run-final-attempt3/m1/manifest.json)
cover F1/F2/tie and same-core Library. [Actual browser receipt](operations/H-014/browser/final-983-attempt1/browser-receipt.json)
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

## H-014 clean offline readiness verification

Use the exact frozen committed candidate and portable
[clean-run driver](operations/H-014/clean_run.py),
[targeted compiled-graph checks](operations/H-014/readiness_e2e.py) and
[actual browser driver](operations/H-014/browser_ui.py) with the documented
[isolated scope](operations/H-014/clean-run-scope.md). Read script CLI/README before
execution; never copy original runtime, spending ledger, .env or untracked evidence.
Both DBs initialize from tracked seeds; repeat init must refuse without mutation.
Registry install retries/cache/browser reuse are disclosed, not clean-download claims.
Keep OPENAI_API_KEY absent, UNIVERSITYDB_LIVE_APPROVED=no and tracing disabled.
Inspect current input/run/SQL/bindings/raw/adapted rows/full same-run trace for success,
group/top, clarification resume, M1 actual dependencies, Library, repair and terminal
error/no stale success. Normal profile must reject hidden test injection. Stop only
owned UI/browser. [Current receipts and gaps](reports/H-014-readiness-offline.md)
separate final corrected-candidate runs from historical H013 captures and initial
clean baseline; injected providers are never real-model accuracy.

### H014 exact983 fresh execution evidence

[Final isolated full run](operations/H-014/clean-run-final-attempt3/final-summary.json)
passed485tests80.36s/all7commands0/157oracle;
[actual browser](operations/H-014/browser/final-983-attempt1/browser-receipt.json)
passed six classes/seven captures with focused raw/adapted rows and no help/None.
Exact tested product98345ad6ce5757c71d44ba1ce59a683d46e0d910, not a later docs SHA.
Full values checked in DOM+trace, not all cells fit one screenshot. Processes stopped.
Final independent APPROVE/CLEAR received; root actual native COMPLETE/strict PASS5/5; live/push/defense not-run.

## Publication checkpoint — 2026-11-08

At the historical H014 publication, the baseline was 485 tests/157 oracle at 98345ad. New publication
permission does not authorize real-model calls. In addition to the sequence above,
run the named-scope/UI-magic/eval-harness regressions:

```bash
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_readiness_scope.py tests/test_readiness_ui_magic.py tests/test_eval_harness.py
```

Unknown named targets must not disappear into global scope. Grouped/each-reader
questions must retain their valid scope. Open raw/adapted panels must show actual
values, without DeltaGenerator help dumps or stray None. The eval harness tests
only offline plan/export/scoring; no live collector or live result is implied.

## Current H016 automated entry points

The README lists the current four H016 regression modules and the optional
`docs/operations/H-016/browser_ui.py OUTPUT --full` driver. The latter checks
natural four-filter input, clarification pause/resume, dependency execution, SQL
repair, refusal and two Library states. Its eight captures include the clarification
pause and resumed result separately. The original six-step manual fixture above
remains a reproducible demonstration, not an arbitrary-query model simulator.
Current full baseline: 815 tests / 157 independent oracle checks on 58f2fe9.
