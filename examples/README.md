## Publication update — 2026-11-08

The owner authorized publishing completed H015/H016 evidence and current English
reviewer documentation. The tested H016 executable remains `58f2fe9`; later
documentation commits do not claim a fresh full product run. New product API calls,
spending changes and a new live campaign remain outside this delivery. Historical
no-push/pending statements below describe their original cutoffs.

## Published H-014 readiness checkpoint — 2026-11-08

Current tested product98345ad:485offline tests,157oracle, clean tracked-only
University/Library reproduction, real offline browser7captures, APPROVE/CLEAR and
native COMPLETE/strict PASS5/5. Named-scope and UI-magic regressions are repaired.
H-013410-test/earlier candidate statements below are historical. This checkpoint
is authorized for publication; real-model quality and owner defense remain pending.
Live protocol/budget are proposed, not accepted or executed.

# Current offline examples — I2+I3

| Scenario | Result | Evidence |
| --- | --- | --- |
| University S6 |80.00 | [trace](../docs/operations/H-013/browser/cp-e-final-attempt2/success.jsonl) |
| Alex clarification |same-run selection→86.67 | [trace](../docs/operations/H-013/browser/cp-e-final-attempt2/clarification-resume.jsonl) |
| Dependent M1 |course2→student1→95.00 | [trace](../docs/operations/H-013/m1-final/F1.jsonl) |
| M1 mutations and exact ties |actual upstream IDs change downstream results | [manifest](../docs/operations/H-013/m1-final/manifest.json) |
| Library open loans |Ada1/Bob1 | [trace](../docs/operations/H-013/browser/cp-e-final-attempt2/library.jsonl) |
| Repair and terminal error |all attempts, no stale answer | [browser receipt](../docs/operations/H-013/browser/cp-e-final-attempt2/browser-receipt.json) |

These are offline/injected generation records with actual graph/SQLite results.
Follow the current [E2E guide](../docs/manual-e2e.md) to reproduce the UI sequence.
Historical live and intermediate evidence below retain their original cutoffs;
their no-push statements do not override the later publication authorization.

# Example questions, outputs and traces

| Case | Expected / recorded result | Evidence |
| --- | --- | --- |
| Bea/student2, DB/course1, Kim/teacher10, S1 |16000/2/2 →80.00 | [receipt](../docs/operations/H-009/live/s6/receipt.json), [trace](../docs/operations/H-009/live/s6/trace.jsonl) |
| Alex/student1, same remaining filters |9000/1/1 →90.00 | [pre-run oracle](../docs/operations/H-009/live/mutation-planned-oracle.json), [receipt](../docs/operations/H-009/live/mutation/receipt.json), [trace](../docs/operations/H-009/live/mutation/trace.jsonl) |
| Live browser S6 |80.00, full SQL/rows/trace | [receipt](../docs/operations/H-009/live/ui/browser-receipt.json), [trace](../docs/operations/H-009/live/ui/live-ui-success.jsonl), [screenshot](../docs/operations/H-009/live/ui/live-ui-sql.png) |
| Unsupported input after success |INVALID_INPUT; stale answer cleared | [trace](../docs/operations/H-009/live/ui/live-ui-failure.jsonl), [screenshot](../docs/operations/H-009/live/ui/live-ui-failure.png) |

[Manual steps and full questions](../docs/manual-e2e.md). These are actual preserved
I1 live records, not newly generated in the documentation audit. Runtime requests
including instructions/schema are in [plan request](../docs/operations/H-009/live/s6/request-01.json)
and [SQL request](../docs/operations/H-009/live/s6/request-02.json).

[offline-s6.json](offline-s6.json) is a newly packaged **scripted transport fixture**
derived from tests/conftest.py outputs(), not a captured live response. It enables
free UI/graph/SQLite smoke testing of S6 only and must remain labeled offline/injected.

## H-013 current offline browser examples (not real-model accuracy)
[CP-C actual browser receipt](../docs/operations/H-013/browser/cp-c-attempt3/browser-receipt.json)
links injected-proposal Streamlit/compiled-graph/SQLite captures: S6→80.00;
Alex ambiguity→real same-run checkpoint resume86.67; unknown-column repair→80.00;
provider refusal→terminal error without stale success. Per-case JSONL, screenshots
and visible body text are adjacent. Focused SQL/DB/adapted/trace views supplement the
main screenshot because Streamlit scrolls inside its app container. The owned server
and browser were stopped; temporary root isolated the actual monetary ledger.
[Fixture builder](../docs/operations/H-013/offline_ui_fixture.py) supplies SQL proposals,
not fabricated DB results or a production provider fallback. Historical I1 live
records above stay unchanged; CP-D/E final M1/Library/frozen-source evidence is separate.

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
[Exact-process structured proofs](../docs/operations/H-013/m1-final/manifest.json).
