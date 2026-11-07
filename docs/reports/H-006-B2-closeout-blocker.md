# H-006 B2 - real reviews completed, post-closeout blocker

Date: 2026-11-07. Result: **blocker; B is not complete, there is no commit B**.
This is a new attempt after the OMX overhaul, not a continuation of the canceled generation.
Base: H-006-v5 and separate direct user call Advisory;
[fresh diagnostics D2](H-006-v5-readiness-2.md) used, A was not repeated.

## Git and preservation

- A/HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, branch `main`, correct Git root.
- All **97** pre-B baseline files, including raw uncommitted documents and D2, retain SHA-256.
Another **9** historical private research/evidence files and **2** files of the canceled generation are unchanged.
- All **25** Obsidian inputs match the actual hashes at the start of B. Old frozen-manifest
the discrepancies in the five updated materials have already been explained by D2/CHAT-022, these are not new changes.
The PDF is read directly; Obsidian has not changed.
- Git index is unchanged, staging is empty, remotes are missing. No commit B, push or publish.
New files are diagnostic documents only; the existing docs/AGENTS/wiki indexes were not changed.
- Detailed hashes and commands: [preservation-and-validation.json](../operations/H-006-B2-closeout-blocker-evidence-2/preservation-and-validation.json).

## Activation and real roles

Direct native hook activated `workflow_variant=advisory`:

- generation: `ec3e1f0b-d751-4088-bfb2-ec386c08549c`;
- OMX session: `omx-1794046506930-56sf8c`;
- native root: `01a1b581-446d-70b0-84ac-3e5b449c1437`;
- native activation turn: `01a1b58c-206e-7472-bebe-165fab7636bc`.

The canceled `0748daa2-4c89-4a84-a305-486ed1f480a3` was not renewed.
Codex 0.162.1, OMX 0.21.46 with local repair, Node 22.23.2; no updates/setup/repair were performed.
Native `agent_type` is used for installed `planner`, `architect`, `critic`; models were not imposed.

| Iteration | Planner | Individual Architect | Separate Critic |
|---|---|---|---|
| 1 | Draft completed | ITERATE | ITERATE: current revision rejected |
| 2 | Revision completed ITERATE | ITERATE |
| 3 | Revision completed| APPROVE, 0 blocking | APPROVE, 0 blocking |

Planner reused for three iterations, reviewers - six separate native children, strictly
Architect→Critic sequentially. For **7/7** children, real native parents/root/role/generation have been verified
and `completion_source=native_stop_event`; later notify did not lose completion in the tracker.
This is local lifecycle evidence, not host-issued authority. Additional configured gates: **[]**,
tested after Critic; There are no fictitious gate verdicts.

Fixed: difference between static DAG and runtime bindings, final typed ResultSpec,
precise aggregate semantics/draws, separation of injected faults from real-model evaluation, full SQL/DB/trace
in the UI, diff no_rows/no_grades/real_zero and COALESCE outside SUM for empty input.
Old researcher/dependency-expert results are read and reused as historical inputs,
their exports/hashes are checked; they are not issued as new studies/reviewer approvals.
No new research gaps requiring additional agents were discovered.

[Native completions](../operations/H-006-B2-closeout-blocker-evidence-2/native-role-completions.json),
[accurate review projections](../operations/H-006-B2-closeout-blocker-evidence-2/review-evidence.json).

## What is prepared, but not packaged as a complete architecture

The final **proposed** documents remain in `.omx/plans/H-006-B2/iteration-3/`:
`architecture-proposal.md`, `contracts.md`, `test-plan.md`, `requirements-test-matrix.md`,
`implementation-plan.md`, `production-considerations.md`, ADR-OMX-003…007, additions/changelogs.
Full bundle: `.omx/plans/H-006-B2/iteration-3/plan-bundle.md`.
Raw SHA-256: `e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`.
Manifest SHA-256: `f903b9ca80b4fb74f4f17c04ae8b69004abccd879dd065dcd53e1c9cebf891d8`.
All manifest entries of three unchanged editions were checked: **13/14/15**, without any discrepancies.
Reviews: `.omx/plans/H-006-B2/reviews/iteration-{1,2,3}-{architect,critic}.md`.
Raw SHA-256 and domain-separated official Advisory digests are different presentation algorithms;
This is not file corruption.

Recommendations (unaccepted solutions): SQLite/direct LangGraph/OpenAI SDK/Streamlit/local JSONL;
integer hundredths of grades, separate NULL, all retakes, equal enrollment weights, exact ties;
a limited graph, a final result registry, and a second Library adapter without changing the kernel.
Versions/provider/model/budget - candidates, not installed and not live-tested stack.
All new ADRs remain **proposed until discussed in the chat**.

## Regular closure and new controversy

The command is executed **once**, via supported host permission:

```text
/home/dev/.omx/runtime/bin/omx ralplan advisory complete --json
exit=0
{"ok":true,"status":"closed","host_verified":false,"consensus_gate_complete":false,"execution_handoff_authorized":false,"return_to_caller":true}
```

The standard append-event reader shows `closed`, journal `committed`, `approved+proven`,
`corruption:null`. Mode `active:false/current_phase:complete`, run `active:false`;
review lifecycle `complete:true/sequence_valid:true/iteration:3`.
Evidence bundle digest: `57ddd777824da540443657e5f843e8fbd292ef1a528c7112080cd809e7ba5a90`.
Host verification, consensus gate and execution handoff are clearly **false** - this is expected for standalone Advisory.

**But after the usual next tool calls session `skill-active-state.json` again contains
`active:true`, `phase:reviewing`, same generation/root/turn and saved `completed_at`.**
Journal assigned him `active:false`, and `updated_at` later closeout.
`omx status` simultaneously shows `ralplan: inactive (phase: complete)` and `skill-active: ACTIVE`.
This is a post-closeout incompatibility, not a lack of reviewer approvals.

Raw base `fence.json` remains `pending_closeout` intentionally: append-only `fence-event-0001.json`
specifies a closed effective projection. The first check erroneously required terminal from raw base
and received an AssertionError; the correct official reader confirmed the closure without re-complete.

[Team](../operations/H-006-B2-closeout-blocker-evidence-2/closeout-command.json),
[terminal/current snapshots](../operations/H-006-B2-closeout-blocker-evidence-2/terminal-projections.json),
[status](../operations/H-006-B2-closeout-blocker-evidence-2/status-command.json).

Hypothesis on the established code: notify→`syncSkillStateFromTurn` re-infers the phase from the text
assistant and assigns active without checking the terminal Ralplan in this function. Accurate triggering payload
was not traced, so causality is not declared proven.
The following limited test for the integration maintainer: isolated fixture with terminal Advisory
and late authorized notify; all mode/run/session-skills must remain inactive.
[Code snippets and output restrictions](../operations/H-006-B2-closeout-blocker-evidence-2/source-guided-hypothesis.json).
Test/repair/replay did not run in this workspace.

## Prompt coverage, checks and stopping

- [Actual task + received-task projections](../ai/omx/H-006-B2-blocker-actual-prompts-2.json),
[coverage/cutoffs](../ai/omx/H-006-B2-blocker-prompt-coverage-2.json): all 7 neglected children,
three moves Planner, actual custom B prompt. Private exports saved, skipped records=0.
- Root actual prompt is extracted from the native transcript and hash matches activation. Child assignments
stored as self-projections of the actual text received; parent tool arguments are encrypted,
plaintext byte equality with ciphertext is not declared. System/developer/reasoning and full inherited
context is not published. Private vault/repair-output paths redacted; full transcripts are not exported to docs.
- JSON/links/privacy/preservation checks: [final check](../operations/H-006-B2-closeout-blocker-evidence-2/document-checks.json).
The first build of the diagnostic export stopped at the old form iteration1 observation;
its partial unsuffixed outputs are saved and marked incomplete. The canonical complete set is suffix `-2`.
- Product tests/evals **not-run**: no applications/schema/seed. Isolated schema-free
SQLite `:memory:` SELECT probes Architect2/Critic2 and documentary calculations are not
product tests, DB integration proof or real-model E2E.
- Credentials were only checked for presence: OPENAI_API_KEY was missing. The values ​​were not saved.
Account/model access, budget, dependency compatibility, public delivery, defense and production
not proven. R-15 open; the remaining future acceptance evidence is not replaced by the plan.

**According to the user's stop rule, packaging of the sustainable architecture in docs/ and commit B has not been started.**
No restarts, repeated closeout, manual editing of IDs/tracker/state, cancellation of closed generation
or execution authorization/handoff. Source materials, research and approved private design are preserved.
After the report, a stop for a separate user request.
