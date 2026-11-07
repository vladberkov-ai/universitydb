# Prompt catalogue

Read the consolidated prompt texts in **[English](PROMPTS-EN.md)** or **[Russian](PROMPTS-RU.md)**. Each entry links to the authoritative original; translations are not claims of actual model input. Structured child/session records remain in the provenance index below.

Current I1,2026-11-07. Historical coverage records remain in [README](README.md).
This catalogue indexes actual saved files; it is not a claim of complete transcripts.

## Application prompts

| Task | Versioned instructions | Model / effort | Actual request example |
| --- | --- | --- | --- |
| Plan | [plan.txt](../../src/universitydb/prompts/plan.txt) |gpt-6.1-sol / high|[request01](../operations/H-009/live/s6/request-01.json)|
| SQL | [sql.txt](../../src/universitydb/prompts/sql.txt) |gpt-6.1-sol / medium|[request02](../operations/H-009/live/s6/request-02.json)|
| Repair | Same SQL instructions plus previous_error payload |gpt-6.1-sol / medium|Offline route tests; no invented live failure transcript|

Descriptor, scope, question, plan and previous_error are assembled by agent.py; strict
output schemas and reasoning configuration are assembled in config.py. A prompt file
alone is not the whole request. Formatter/SQL safety/numeric oracle have no separate LLM.

## Saved development tasks and coverage

These are saved root/child tasks, selected exports, projections and receipts from
H004–H009. Each file's own provenance/omissions controls its interpretation. Old cutoff
claims describe their stage, not the current runtime prompt state. Private chat queue
and missing full child/tool exports remain explicit gaps in README; no new prompts are
invented to fill them.

- [H-004-actual-prompt.txt](omx/H-004-actual-prompt.txt)
- [H-004-instruction-context.json](omx/H-004-instruction-context.json)
- [H-004-prompt-receipt.json](omx/H-004-prompt-receipt.json)
- [H-004-session-export-completed.json](omx/H-004-session-export-completed.json)
- [H-004-session-export.json](omx/H-004-session-export.json)
- [H-005-actual-prompt.txt](omx/H-005-actual-prompt.txt)
- [H-005-prompt-receipt.json](omx/H-005-prompt-receipt.json)
- [H-005-session-export-completed.json](omx/H-005-session-export-completed.json)
- [H-005-session-export-cutoff.json](omx/H-005-session-export-cutoff.json)
- [H-006-B-delivery-actual-prompt.txt](omx/H-006-B-delivery-actual-prompt.txt)
- [H-006-B-delivery-prompt-coverage.json](omx/H-006-B-delivery-prompt-coverage.json)
- [H-006-B-delivery-session-cutoff.json](omx/H-006-B-delivery-session-cutoff.json)
- [H-006-B2-blocker-actual-prompts-2.json](omx/H-006-B2-blocker-actual-prompts-2.json)
- [H-006-B2-blocker-actual-prompts.json](omx/H-006-B2-blocker-actual-prompts.json)
- [H-006-B2-blocker-prompt-coverage-2.json](omx/H-006-B2-blocker-prompt-coverage-2.json)
- [H-006-B2-blocker-prompt-coverage.json](omx/H-006-B2-blocker-prompt-coverage.json)
- [H-006-B2-iteration-2-changes.md](omx/H-006-B2-iteration-2-changes.md)
- [H-006-B2-iteration-3-changes.md](omx/H-006-B2-iteration-3-changes.md)
- [H-006-B2-iteration-3-plan-bundle.md](omx/H-006-B2-iteration-3-plan-bundle.md)
- [H-006-actual-prompt.txt](omx/H-006-actual-prompt.txt)
- [H-006-prompt-coverage-blocker.json](omx/H-006-prompt-coverage-blocker.json)
- [H-006-prompt-receipt-A.json](omx/H-006-prompt-receipt-A.json)
- [H-006-session-export-A-cutoff.json](omx/H-006-session-export-A-cutoff.json)
- [H-006-session-export-blocker-cutoff.json](omx/H-006-session-export-blocker-cutoff.json)
- [H-006-v5-B-actual-delegation-calls.json](omx/H-006-v5-B-actual-delegation-calls.json)
- [H-006-v5-B-actual-prompt.txt](omx/H-006-v5-B-actual-prompt.txt)
- [H-006-v5-B-dependency-expert-evidence.json](omx/H-006-v5-B-dependency-expert-evidence.json)
- [H-006-v5-B-leader-export-cutoff.json](omx/H-006-v5-B-leader-export-cutoff.json)
- [H-006-v5-B-prompt-coverage.json](omx/H-006-v5-B-prompt-coverage.json)
- [H-006-v5-B-researcher-evidence.json](omx/H-006-v5-B-researcher-evidence.json)
- [H-006-v5-D-actual-prompt.txt](omx/H-006-v5-D-actual-prompt.txt)
- [H-006-v5-D-messages-cutoff.json](omx/H-006-v5-D-messages-cutoff.json)
- [H-006-v5-D-prompt-coverage.json](omx/H-006-v5-D-prompt-coverage.json)
- [H-006-v5-D2-actual-prompt.txt](omx/H-006-v5-D2-actual-prompt.txt)
- [H-006-v5-D2-prompt-coverage.json](omx/H-006-v5-D2-prompt-coverage.json)
- [H-007-actual-prompt.txt](omx/H-007-actual-prompt.txt)
- [H-007-leader-cutoff.json](omx/H-007-leader-cutoff.json)
- [H-007-performer-coverage.json](omx/H-007-performer-coverage.json)
- [H-007-performer-task-projection.json](omx/H-007-performer-task-projection.json)
- [H-007-prompt-coverage.json](omx/H-007-prompt-coverage.json)
- [H-007-research-task.txt](omx/H-007-research-task.txt)
- [H-008-actual-prompt.txt](omx/H-008-actual-prompt.txt)
- [H-008-cap10-actual-prompt.txt](omx/H-008-cap10-actual-prompt.txt)
- [H-008-cap10-performer-projection.json](omx/H-008-cap10-performer-projection.json)
- [H-008-cap10-prompt-receipt.json](omx/H-008-cap10-prompt-receipt.json)
- [H-008-g004-no-call-performer-task.txt](omx/H-008-g004-no-call-performer-task.txt)
- [H-008-live-billing-research-task.txt](omx/H-008-live-billing-research-task.txt)
- [H-008-performer-coverage.json](omx/H-008-performer-coverage.json)
- [H-008-prompt-receipt.json](omx/H-008-prompt-receipt.json)
- [H-008-research-task.txt](omx/H-008-research-task.txt)
- [H-008-review-coverage.json](omx/H-008-review-coverage.json)
- [H-009-actual-user-prompt.txt](omx/H-009-actual-user-prompt.txt)
- [H-009-documents-received-task.txt](omx/H-009-documents-received-task.txt)
- [H-009-live-execution-task.txt](omx/H-009-live-execution-task.txt)
- [H-009-rates-task.txt](omx/H-009-rates-task.txt)
- [history/H-004-prompt-receipt-cutoff.json](omx/history/H-004-prompt-receipt-cutoff.json)

## Reviewer bundle audit

[Actual owner request](reviewer-bundle-actual-request.txt): verbatim received task with terminal newline; this is not a full session/tools transcript. Documentation/fixture packaging only, no new runtime prompts or paid calls.
