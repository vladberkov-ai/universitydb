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
