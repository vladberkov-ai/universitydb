# Independent H016 natural-input regressions — regression-first

Author: native `nl_regressions` test-engineer lane. Actual delegated task: write only new tests for diverse natural-input IDs/projections, combined filters, unknown/malformed/conflicting inputs, ambiguity/resume and downstream proof. Context read: complete repository AGENTS.md, ADR-OMX-012, I2-I3 offline contract, actual resolver/domain adapters/compiled Agent, existing test helpers and fixture seeds. No H015 question/oracle/artifact imports; no credentials, network, canonical ledger or product-source edits.

## RED command and scope

`.venv/bin/pytest -q tests/test_h016_natural_scope.py`

Fresh pre-production-repair result: **21 failed, 15 passed in 6.12s**. Complete stdout/stderr: [independent-pre-fix.txt](independent-pre-fix.txt). The wrapper captured output with shell redirection; pytest reported failures (exit 1); the shell wrapper's final `tail` exited 0, which is not pytest success.

## Coverage (36 independently authored parameter instances)

- 10 University numeric natural-ID inputs: course/student/teacher, uppercase/mixed/lowercase ID markers, sentence punctuation, four combined filters and name+ID mixtures; real NULL/no-grades and empty intersections.
- 4 University enrollment projections: ID/IDs as declared columns rather than names; projection combined with semester or numeric course filters.
- 6 Library numeric-ID/projection inputs: case variants, reader name+ID, unfiltered per-reader projection.
- 14 negative cases: unknown IDs, signed malformed IDs, nonnumeric/missing ID values, duplicate conflicting IDs, known name conflicting with ID, unknown explicit names. Appropriate errors must have zero provider/SQL calls, not forced success.
- 2 ambiguity/resume cases: actual duplicate names in both schemas; normal Agent continuation binds the chosen catalog ID and real SQLite result; Library reader with no loans returns zero.

Every input enters `Agent.run(question)` without choices or prestructured scope. The compiled production graph resolves against the initialized temporary SQLite catalog before calling an explicitly injected transport. The transport builds scripted plan/SQL from **the actual payload scope**, never from expected test scope. Expected scope values are assertions and independent SQLite-oracle inputs only. Production SQL validation, execution, deterministic adaptation and persisted terminal JSONL remain active. Each successful query asserts actual payload scope and independent SQL rows; source database SHA stays unchanged. Trace assertions compare persisted and returned events and sequential terminal run_end.

## Observations from RED, not root-cause assumptions

Natural `entity ID N` and projection `entity ID/IDs` forms fail before SQL or lose scope. Critically, the known-name conflict cases (`Bea, student ID 1`; `Ada, reader ID 2`) return `ok` instead of rejecting inconsistent identities because the numeric natural-ID expression is not applied. Existing shorthand/canonical-key tests do not establish these behaviors. These independent cases supplement, not replace, the complete H015 failure map and mandatory broad integration/UI/safety/dependency checks owned by the leader.

## Limits

The injected transport supplies a declared plan family and adapter-valid SQL. This proves natural scope resolution plus downstream mechanics against real data, not real-model semantic interpretation/NL→SQL accuracy or new live score. No old expectations were weakened. New tests may be changed only for a demonstrated accepted-contract issue, not to make RED green. Integration classes outside this file remain separately required by H016.

Checkpoint formatting: terminal trailing horizontal whitespace was stripped from the two new pre-fix text logs for clean Git diff validation; failure text, counts and outcomes are unchanged. These are text projections, not byte-identical terminal capture claims.
