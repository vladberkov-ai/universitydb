# Prompt provenance and coverage

Owner: repo. Updated: 2026-11-07. Current stage: H-006 B documentary delivery; H-004/H-005 and earlier blocker cutoffs below are historical.

OMX session: `omx-1794006222700-y9rw23`.
Native session: `01a1b31a-d9cc-7d00-b9d6-4118c6e46f49`.

These IDs are unchanged: H-005 is a new **logical task stage in the same native session**, not a fabricated second session or a claim that the native conversation was closed after H-004.

| Set | Actual/template | Source → public artifact | Coverage |
|---|---|---|---|
| Leader task in this session | **actual**, not a template | Native session task message → [received prompt projection](omx/H-004-actual-prompt.txt) | Entire task wording retained except four private-path substitutions and terminal LF; hashes/redactions in [receipt](omx/H-004-prompt-receipt.json) |
| H-004 completed-stage export | actual messages | Installed OMX JSON → [completed logical-stage export](omx/H-004-session-export-completed.json) | Actual task + all 4 assistant messages, including later preparation update and final answer (line 253); excludes next H-005 task at line 260; tools/instruction full coverage not claimed |
| Original H-004 cutoff | historical actual selected messages | [Unchanged partial export](omx/H-004-session-export.json), [historical receipt](omx/history/H-004-prompt-receipt-cutoff.json) | Task + two progress messages; preserved byte-for-byte, not silently replaced |
| H-005 leader task | **actual**, not template | Native user entry line 260 → [actual prompt](omx/H-005-actual-prompt.txt), [receipt](omx/H-005-prompt-receipt.json) | Complete task wording except private vault path substitution and terminal LF; H-005 package is read context, not this prompt |
| H-005 export | actual cutoff | [Task + first progress export](omx/H-005-session-export-cutoff.json) | Current cutoff only; later H-005 preparation/progress/final not in this checkpoint, as explicitly allowed by H-005 |
| User-provided initial AGENTS/environment bundle | actual instruction context, not task text | Private native transcript; hashed omission in selected export | Not exported wholesale; not claimed covered by the short task file |
| Installed instructions / wiki skill / runtime overlay | read context, not additional task prompts | [Context hashes](omx/H-004-instruction-context.json) | Versions/hashes and roles recorded; not a full public instructions transcript |
| H-004 v2 and 25 inputs | read context, **not** received task prompt | [Input evidence](../operations/input-verification.json) | All read and hashed; original PDF read on all 4 pages; only four permitted snapshots exported |
| H-005 and current inputs | read context, **not** received task prompt | [Current input/baseline evidence](../operations/H-005-input-verification.json) | 10/10 vault hashes + 3/3 workspace baselines; old H-004 vault hashes are historical, not a gate against agreed chat updates |
| Workers and child agents | not-applicable | None | No workers, Team or native children launched; no fictitious prompts/files |
| CHAT-001..011 history | prior actual user messages, pointer queue only | Private chat register / H-005 inputs, table below | Not copied; full chat transcript absent; no claim of full historical coverage |
| Runtime application prompts | not-yet-created | None | No placeholders masquerading as actual runtime prompts; no application created |
| Future architecture/implementation/review/eval prompts | not-yet-created | None | Outside this stage; not templates presented as execution history |

## Export method, cutoff and omissions
Checked `omx session --help` and `omx session export --help` on installed OMX **0.21.46** before using:

```text
omx session export 01a1b31a-d9cc-7d00-b9d6-4118c6e46f49 --format json --output .omx/H-004-session-private.json
```

The original export was moved into ignored private **session-specific export storage** inside `.omx/preparation/`; the native private session transcript remains the source of truth. It was not copied into public docs. The CLI exporter excludes system/developer instructions and reasoning by design; `--include-tools` was not requested. Export reports `skipped_records = 0`, but that does **not** imply full transcript or instruction coverage. The public derivative omits the initial instruction/environment bundle and replaces private vault/legacy paths with named placeholders. It keeps original timestamps/line numbers for retained messages and the original export hash. The task `.txt` was extracted from the actual exported user entry, not reconstructed from the handoff or starter template.

The command above produced the **historical H-004 partial snapshot**, ending with the Git-blocker progress update. H-005 checked the installed interface again and ran:

```text
omx session export 01a1b31a-d9cc-7d00-b9d6-4118c6e46f49 --format json --output .omx/preparation/H-005/session-cutoff-private.json
```

The refreshed source export contains the actual H-004 final answer and subsequent H-005 task/progress. Its safe H-004 derivative includes all H-004 user-task/assistant messages after the omitted initial instruction bundle, stopping immediately before the actual H-005 task. The H-005 derivative starts at that exact user task. Both preserve timestamps/line numbers; original relative Markdown links inside message text are interpreted from the workspace root. Tools were not requested; system/developer/reasoning are excluded by the exporter. `skipped_records=0` does not change these limits. The H-004 prompt receipt points to the completed-stage export and retains the previous receipt/hash/cutoff as history.

No secrets/contact details were found in retained task/progress/final text; the initial instruction bundle remains excluded wholesale with its hash. H-005's not-yet-existing final answer is not required inside the current checkpoint and is not reconstructed. Eventual all-tools/instructions/full-native-session coverage remains unclaimed. Stable command/results evidence is in the stage reports and validation manifests; private native transcripts and raw exports remain private.

## Historical queue (no export performed)

All source pointers below are **vault-relative attributions**, not broken public hyperlinks.

| ID | Private source | Actual known coverage from verified input register | Public status |
|---|---|---|---|
| CHAT-001 | `raw/chat/CHAT-001.md` | User text, whitespace normalized | pending separate selection/review |
| CHAT-002 | `raw/chat/CHAT-002.md` | User text, whitespace normalized | pending separate selection/review |
| CHAT-003 | `raw/chat/CHAT-003.md` | User text, whitespace/HTML normalized | pending separate selection/review |
| CHAT-004 | `raw/chat/CHAT-004.md` | User text, whitespace/HTML normalized | pending separate selection/review |
| CHAT-005 | `raw/chat/CHAT-005.md` | Exact received user text, LF | pending separate selection/review |
| CHAT-006 | `raw/chat/CHAT-006.md` | Exact received user text | pending separate selection/review |
| CHAT-007 | `raw/chat/CHAT-007.md` | Exact received user text | pending separate selection/review |
| CHAT-008 | `raw/chat/CHAT-008.md` | Exact user text; read/hash verified here | not exported |
| CHAT-009 | `raw/chat/CHAT-009.md` | Exact user text; read/hash verified here | not exported |
| CHAT-010 | `raw/chat/CHAT-010.md` | Exact user text per current overview; original not loaded here | pointer queue only |
| CHAT-011 | `raw/chat/CHAT-011.md` | Exact user text; read/hash verified as H-005 input | not exported |

Only CHAT-008/009 (H-004) and CHAT-011 (H-005) were read as required raw inputs; other raw chats were **not** loaded wholesale. Earlier assistant answers exist as synthesis, not proven verbatim transcripts. Public completeness U-01 remains partially covered, not closed. Workers in both preparation stages are not-applicable; runtime application prompts are not-yet-created. App runtime versions/models and any future worker sessions must be added only when they actually exist.

## H-006-v4 provenance / A cutoff
The native session is now `01a1b356-8b0a-7b40-8c40-293841f31670`; OMX selector remains `omx-1794006222700-y9rw23`. These selectors do not establish advisory runtime ownership.
- [Actual task](omx/H-006-actual-prompt.txt), [A receipt](omx/H-006-prompt-receipt-A.json), [A cutoff export](omx/H-006-session-export-A-cutoff.json): actual received task, not reconstructed from the handoff. Initial AGENTS/environment and attached skill contexts omitted with hashes; task retains engineering text with private vault path redacted.
- [H-005 completed-stage export](omx/H-005-session-export-completed.json) supplements the old immutable cutoff/receipt: actual task + all four assistant messages, including final line 394, read from the exact previous native session export.
- [H-006 read inputs](../operations/H-006-input-verification.json): 19/19 hashes, PDF all 4 pages; previous H-006 packages not used. Sources remain read-only.
A has no subagents. B coverage must list each actual role/task/session/result if and when launched. Application runtime prompts not-created. Current H-006 final/tool/instruction full coverage is not claimed.

## H-006 blocked B cutoff
A committed at `8931d832d49311ac0d63c3a7a359b4293058da89`; B stopped before canonical Advisory activation, no subagents/review/research/gates. [Current coverage receipt](omx/H-006-prompt-coverage-blocker.json) and [blocker-cutoff export](omx/H-006-session-export-blocker-cutoff.json) supplement, not overwrite, A cutoff. Final response/tool/instruction full coverage remains unclaimed. [Blocker report](../reports/H-006-advisory-blocker.md) separates readiness diagnostics from architecture review, which did not run.

## H-006 B — current documentary delivery (supersedes historical blocker as current status)

The preceding H-006 blocked-B section is an immutable historical cutoff, not current execution status.
- Prior readiness/actual prompts: [D](omx/H-006-v5-D-prompt-coverage.json), [D2](omx/H-006-v5-D2-prompt-coverage.json), [first B attempt](omx/H-006-v5-B-prompt-coverage.json).
- Historical research: [researcher actual calls/final](omx/H-006-v5-B-researcher-evidence.json), [dependency-expert actual calls/final](omx/H-006-v5-B-dependency-expert-evidence.json), [actual delegation calls](omx/H-006-v5-B-actual-delegation-calls.json). Reused dated evidence, not rerun or B2 reviewer approvals; encrypted parent arguments are not plaintext task coverage.
- B2 actual root task and received child tasks: [actual projections](omx/H-006-B2-blocker-actual-prompts-2.json), [coverage](omx/H-006-B2-blocker-prompt-coverage-2.json). **7/7 children**, one Planner with three iterations, six separate Architect/Critic reviews, no execution workers. Received-task self-projections are not byte equality to encrypted parent tool arguments. Incomplete unsuffixed evidence is retained as history; canonical complete set is suffix `-2`.
- Approved **proposed** Planner baseline: [public bundle](omx/H-006-B2-iteration-3-plan-bundle.md), [revision 2](omx/H-006-B2-iteration-2-changes.md), [revision 3](omx/H-006-B2-iteration-3-changes.md). Link rebasing only in public bundle; source/public hashes and transformations in [provenance](../operations/H-006-B2-delivery/packaging-provenance.json).
- Packaging-only current session: [actual task](omx/H-006-B-delivery-actual-prompt.txt), [actual selected export](omx/H-006-B-delivery-session-cutoff.json), [read context / coverage / redactions](omx/H-006-B-delivery-prompt-coverage.json). No children/workflow; later checks/commit/final outside export cutoff.
- [Review, closeout and repair verification](../reports/H-006-architecture-review.md). Earlier blocker files and source hashes are preserved, not silently rewritten.

H-005 completed final remains [here](omx/H-005-session-export-completed.json), not re-exported. System/developer/reasoning, full inherited/private instructions and all-tools/full-history coverage remain unclaimed; U-01 is not closed globally. Application runtime prompts **not-created**; this design bundle is not application runtime prompts. No new templates masquerade as actual prompts.
