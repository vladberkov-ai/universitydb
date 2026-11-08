# H016 offline replay and independent lexical matrix

## Meaning and boundary

`tests/test_h016_offline_replay.py` contains **55 parameterized cases**:

- All **24 development-known H015 original questions**, once each: aggregates/NULL/zero, joined filters, counts/listings, top exact ties, dependent M1, clarification, empty cases, Library zero/returned mutations. The original second repetitions are not independent questions or defects; historical 48-conversation measurement remains unchanged.
- **7 independently authored paraphrases**: M1 on changed fixture and all-tied fixture with output-ID prose, top ties, combined names+IDs/four filters, count objects, empty listing with projected IDs, filtered Library zero.
- **16 optional natural-language filter subsets**, not canonical `student_id=` inputs: each subset of student ID2, course ID1, teacher ID10 and S1 enters normal production parsing.
- **5 grouping grains** with natural output-ID projections: student/course/teacher/offering/semester.
- **3 count-object phrases** with combined natural course/teacher/semester filters.

All tests call ordinary `Agent.run(question)` on actual compiled LangGraph and freshly rebuilt temporary SQLite. Clarification cases consume the actual normal continuation via `resume`, never preselected scope. The provider is an explicitly named **injected offline transport**: the test chooses a registered plan family, while SQL is generated from the **actual production payload scope and validated actual upstream references**. Expected scopes/rows never enter Agent or transport inputs. No production case-ID dispatch or answer fixture is added.

Independent stdlib SQLite queries construct raw expectations without calling adapter query/adapt_result; Fraction selects all exact top ties and Decimal checks public two-place means. Every actual raw step, selected dependency rows, final rows, downstream refs, actual scopes, provider-call count, unchanged fixture SHA and persisted terminal trace are asserted. NULL/no_grades, no_rows and zero have explicit checks. The original frozen fixtures are not opened for mutation: trusted schema/seed/registered mutation descriptors are read and rebuilt privately. Historical collector/observer/scorer/corrector modules are not imported or run. There is no new score or live evidence.

The replay module denies `socket.connect`, `connect_ex`, `create_connection` and DNS resolution for every test using pytest monkeypatch. Tests instantiate only ScriptedProvider subclasses, never OpenAIProvider; no credential loading, canonical monetary files or product-network dispatch occurs.

## Affected UI tests

`tests/test_h016_ui.py`: **8 AppTest cases**, real Streamlit/graph/temporary SQLite and production parsing. Covers natural four-filter mean, natural ID-output enrollment listing with NULL, same-run duplicate-name clarification with ID-output prose, Library reader-ID filter followed by global reader-ID/name/count projection, and unknown/conflicting IDs clearing previous success for both schemas. Existing `isolated_app` moves all app resources/runtime into tmp, disables live/tracing and verifies repository runtime hashes unchanged. Fixed SQL/plan proposals are explicit UI fixture boundaries, not natural-language model accuracy. Ordinary text_area input remains untouched; proposals must agree with independently resolved scope to validate. UI exposes same-run trace and SQL, with no retained stale answer after errors.

## Provenance and interpretation

Actual selected test-lane assignments: [initial](../prompts/regression-task.txt), [followups](../prompts/regression-followups.txt). These are prompt projections with explicit omissions, not full transcripts. Read source/contracts/test helpers are context. All old expectations are preserved. New assertions may change only for a demonstrated accepted-contract error, not to hide regression.

Initial diagnostic runs and hash-timing limitations: [receipt](replay-initial-receipt.json), [first31cases](replay-initial.txt), [expanded55cases](replay-matrix-initial.txt), [UI8cases](replay-ui-initial.txt). Expanded diagnostic run overlapped authorized production edits and is not a frozen candidate validation. Final stable-source rerun with before/after hashes is required for candidate claims.

## Remaining uncertainty

These are offline parser/core/SQLite/UI proofs. They do not establish that a real model will select the scripted plan family or generate accepted SQL, service acceptance, live44/48, or new real-model accuracy. Root-owned full suite, actual browser, clean-run, preservation and independent reviews remain separate mandatory H016 gates.

## Iteration findings (not hidden or weakened)

First postrepair run: 101 passed/7 failed across 108 tests. The parser source changed during this diagnostic run, explicitly recorded in `replay-postrepair-receipt.json`. New negative boundaries added 8 malformed identity/projection-mixing cases and 1 compact-identity no-silent-unfilter case, bringing replay module to64tests. Six genuine failures were sent to production owner: `Which course IDs ...` projection misclassified malformed, independent M1 `mean over` misclassified unknown name, and malformed explicit semester IDs hidden by another valid bare S1. One failed listing assertion was an **independent test-oracle bug**, not a product mismatch: using ResultSpec.group_keys indiscriminately grouped `enrollment_rows` by student_id and collapsed repeated offerings. Oracle grouping is now restricted to registered aggregate/top families; enrollment_rows preserves its accepted student+offering row grain and independent expected retake rows. No production assertion or historical expectation was relaxed.

## Stable-source final targeted verification

Command:

`H016_REPLAY_EVIDENCE=docs/operations/H-016/regressions/replay-cases .venv/bin/pytest -q tests/test_h016_natural_scope.py tests/test_h016_offline_replay.py tests/test_h016_ui.py`

**108 passed in 27.63s; pytest exit0.** Breakdown:36 independent natural-scope +64 replay/matrix/boundary +8 affected AppTest cases. All source Python, runtime-prompt and these three test-file hashes were identical immediately before and after the run. Fresh evidence: [output](replay-stable.txt), [before/after hash receipt](replay-stable-receipt.json), [31 detailed case proofs](replay-cases/) covering24development-known original conversations and7independent variants. The hash receipt's HEAD is the commit observed at test completion, not a claim that the then-uncommitted repaired product was already that commit; root must bind final tested candidate commit to these exact source/test hashes.

All six genuine parser findings from the prior diagnostic run were repaired by the separate production owner; no success assertion or accepted historical expectation was weakened. The independent oracle correction preserved listing retakes and was itself exercised by the green original J04 and new UI listing tests.

This targeted result is not the root-owned full offline suite, actual browser, clean-run or independent review gate. No real-model provider/API/count call, credential loading, monetary mutation or push was run by this test lane; the next live campaign still needs separate authority.

## Retained full-trace export (final artifact-only test extension)

At root's request, the test evidence branch now additionally retains exact full same-run `.jsonl` trace bytes, rather than relying solely on hashes of temporary traces. No parsing, plan, SQL, expected outcome or runtime behavior changed. Prior stable108 evidence is preserved. A separate fresh run:

`H016_REPLAY_EVIDENCE=docs/operations/H-016/regressions/replay-final-cases .venv/bin/pytest -q tests/test_h016_offline_replay.py`

**64 passed in17.60s, exit0**, source/prompts/test hashes unchanged throughout. [Final output](replay-final.txt), [final hash/export receipt](replay-final-receipt.json), [31 proof JSON and full trace pairs](replay-final-cases/). Each of the31 exported traces exactly matches its proof's SHA256 and ends in run_end; original24 plus7independent paraphrases are independently auditable after temp cleanup. The remaining33 matrix/boundary tests validate their traces in-process but are not exported as individual proof pairs. Root must perform final full/static checks and bind the candidate commit after this artifact-only test edit.
