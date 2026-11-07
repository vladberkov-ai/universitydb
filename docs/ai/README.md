## H-011 current coverage
[Actual received prompt](omx/H-011-actual-prompt.txt), [provenance/cutoff](../operations/H-011/prompt-receipt.json), [I2 readiness report](../reports/H-011-I2-offline.md). Preparation only; no I2 runtime prompt/model consumption or full transcript claim. Earlier stage cutoffs below are preserved.

# Prompt provenance and coverage

**Current navigation:** [prompt catalogue](PROMPTS.md) lists runtime prompts, actual live requests and saved development records. I1 is complete; earlier not-created/no-live statements below are historical cutoffs. Full transcript coverage remains partial.

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

## H-007 I1 — new limited implementation task / preparation cutoff
Historical sections above remain unchanged stage evidence, not current prohibitions on the new user-authorized I1. [Actual received task](omx/H-007-actual-prompt.txt) and [selected leader export](omx/H-007-leader-cutoff.json) were extracted using installed `omx session export` from exact native session `01a1b649-9f9b-7e32-8c71-138ac3328f7e`; not reconstructed from a starter template. [Coverage/hash/redaction receipt](omx/H-007-prompt-coverage.json) records cutoff and omissions: initial AGENTS/environment, skill context, system/developer/reasoning, tools, later work/final and child transcripts are not covered wholesale. Private vault prefix only is redacted; full source remains ignored/private.

[Researcher's actual received task and persistence instruction](omx/H-007-research-task.txt) are separate child self-projections, not an assertion of plaintext equality to encrypted delegation arguments. [Reference result](../operations/H-007-api-references.md) records fetched sources and limitations. Performer/reviewer actual task/result coverage will be appended after real work; no fictitious full child export is claimed. Application runtime prompts are not created at this pre-code cutoff and must be versioned/hashed when implemented. U-01 is partially covered, not globally closed. ADR003–007 remain proposed; [ADR008](../adr/ADR-OMX-008-I1-scoped-implementation.md) is only the scoped I1 decision.

### H-007 G002 runtime prompts (actually created, offline exercised)
Versioned application instructions now exist at [plan](../../src/universitydb/prompts/plan.txt) and [SQL](../../src/universitydb/prompts/sql.txt). They are application prompts, not reconstructed user/child transcripts. Offline injected graph tests exercise the plan/SQL contract; no real provider consumed these prompts yet. Actual hashes, lock/fixture identities and offline check outputs are recorded in `docs/operations/H-007/G002-validation.json`. Later performer/reviewer task/result projections and final cutoff remain pending, not silently included in the G001 export.

### H-007 performer and final review coverage
[Performer selected received tasks](omx/H-007-performer-task-projection.json) and [coverage receipt](omx/H-007-performer-coverage.json) are actual native collaboration self-projections. Installed exact child-session default export retained inherited root messages only and omitted collaboration tasks/followups; private export hash and explicit omissions are recorded, not reconstructed. Selected stage-defining tasks do not claim complete diagnostic/tool/instruction history. [Initial independent code findings](../operations/H-007/reviews/initial-code-review.md) and [initial architect BLOCK/WATCH](../operations/H-007/reviews/initial-architecture-review.md) are bounded leader-received result projections persisted by the performer, not full source transcripts or self-approval. Final reviewer task/result projections and verdicts remain pending at this draft cutoff.

### H-007 final evidence cutoff
[Final independent review receipt](../operations/H-007/reviews/final-review-receipt.json) and attributed code/architecture projections preserve initial REQUEST CHANGES/BLOCK and corrected APPROVE-offline/WATCH, combined COMMENT. These are bounded actual received-result summaries, not full source exports or verbatim reviewer task equality. Runtime prompt hashes and final source/fixture/lock hashes are in [postreview validation](../operations/H-007/G003-postreview-validation.json). Final own task/commit/report and later root goal checkpoint are outside earlier immutable export cutoffs; no full-history U-01 closure is claimed. Live model/account/cap approval absent; runtime prompts have not been used in a real provider request.

## H-008 continuation coverage
Accepted model configuration is not a new application-prompt rewrite: existing versioned plan/SQL prompts remain unchanged; logical repair uses SQL prompt with previous_error. Hashes and offline checks are in `docs/operations/H-008/validation.json`. Zero live requests have consumed them. [Performer coverage](omx/H-008-performer-coverage.json) contains selected actual received collaboration excerpts with explicit omissions, not reconstructed missing transcripts or plaintext equality to encrypted task arguments. [Research task](omx/H-008-research-task.txt) and [official references](../operations/H-008/api-references.md) are separate evidence. Root-owned exports/review projections are additional bounded artifacts when actually produced; no full U-01 closure is claimed.

### H-008 final review cutoff
[Review coverage](omx/H-008-review-coverage.json) and [independent receipt](../operations/H-008/reviews/final-review-receipt.json) preserve initial code REQUEST CHANGES/architect BLOCK and corrected code APPROVE-offline/architect WATCH, combined COMMENT. Actual result summaries are attributed projections, not full task/tool transcripts or author approval. The initial local checkpoint and later correction/evidence checkpoint remain separate; root's subsequent native snapshot is a later cutoff. U-01 remains partial.

### H-008 actual root task source
[Actual task](omx/H-008-actual-prompt.txt) was extracted from entry15/line903 of the supported root session export, not reconstructed from the starter/handoff. [Receipt](omx/H-008-prompt-receipt.json) pins private export SHA, entry timestamp, redacted private vault prefix and destination SHA; exported task newlines are preserved, terminal LF added. Default export20entries/skipped0 does not cover full tools/instructions/reasoning/child collaboration or the later final answer. Private full export remains ignored, not published.

### H-008 cap10 native-resume cutoff
[Actual new user task](omx/H-008-cap10-actual-prompt.txt) is extracted from entry 22/line 1399 at 2026-11-07T16:35:55.016Z of the supported private root export, verified SHA and 26 entries/skipped0. [Receipt](omx/H-008-cap10-prompt-receipt.json) pins source/session/entry/destination hashes and three substitutions: private credentials path twice, private vault input path once, plus terminal LF. It preserves the one-total-10-USD authority and native-resume-first order; redacted shell text is historical prompt content, not an executable example. The private full export is not copied. [Performer task projection](omx/H-008-cap10-performer-projection.json) records selected actual received collaboration excerpts only, not reconstructed unknown history or equality to encrypted arguments. Root goal/credentials/ledger observations are [attributed](../operations/H-008/cap10-resume/root-observations.json), not fabricated performer stdout. Tools, full inherited/private instructions, reasoning, other messages, complete children and later final/checkpoint are outside this cutoff. U-01 remains partial; no application runtime prompts changed or real-provider prompt consumption occurred.

### H-008 active-goal no-call preflight coverage

[Actual performer selected-task projection](../operations/H-008/live-preflight/performer-prompt-projection.md) records received delegation/follow-ups with explicit paraphrase/privacy/full-transcript gaps. [Research actual task](omx/H-008-live-billing-research-task.txt) and [technical receipt](../operations/H-008/live-preflight/no-call-technical-preflight.md) distinguish documentation/SDK inspection from API execution. No new live runtime prompt or complete-export claim; U-01 remains partial.

[Initial no-call performer delegation actual text](omx/H-008-g004-no-call-performer-task.txt) preserves the received message with exactly one private-path redaction; [coverage/hash receipt](../operations/H-008/live-preflight/performer-prompt-receipt.json). Follow-ups remain selected paraphrase, not complete transcripts.

## H-009 practical-policy continuation
[Actual current user task projection](omx/H-009-actual-user-prompt.txt) is received user text, not the starter template; only the private vault prefix is redacted. [Documents performer's actual received delegation](omx/H-009-documents-received-task.txt) is separate from root task. [Coverage receipt](../operations/H-009/prompt-coverage.json) records self-projection method and gaps: no full-history/tools/instructions/child exports, no encrypted-argument equality assertion. Private CHAT034/ADR005 read/hash only, not copied. Other actual role-task projections and results are linked by the H009 report as produced. Existing plan/sql application prompt files remain templates until an actual authorized live request is captured; no live requests at this offline cutoff. U-01 remains partial.

## H-009 actual live requests / bounded closeout
[Current coverage](../operations/H-009/closeout/prompt-coverage.json) distinguishes actual request JSON (instructions/input/strict schema/model/reasoning), safe responses/usage and full graph traces from unchanged prompt templates. [Actual closeout delegation](../operations/H-009/closeout/documents-received-task.txt) is a received-task self-projection, not encrypted-argument equality/full transcript. [Live closeout](../reports/H-009-live-I1-closeout.md) links actual S6/mutation evidence and marks actual UI and fresh final independent reviews with honest coverage; full root/child/tools/instructions/history coverage remains unclaimed, U01 partial.

## H-013 actual task and scoped child coverage
[Actual received Russian user prompt](omx/H-013-actual-prompt.txt) is preserved separately from H-013/H-011/H-012 read context, [root receipt](../operations/H-013/prompt-receipt.json). [CP-A actual delegated task/follow-up and bounded coverage](../operations/H-013/cp-a-task.txt) and [checkpoint-reference child task](../operations/H-013/checkpoint-reference-task.txt) are distinct source projections. Root/child task projections are not full private/system/developer/tool/reasoning transcripts or encrypted-argument equality; omissions remain explicit. [RU reader navigation](PROMPTS-RU.md) and [EN synopsis](PROMPTS-EN.md) do not replace original evidence. Runtime prompt versions/provenance must be updated with dependent implementation; no live request occurred in this preparation. H-013 scope is whole I2+I3 offline, not renewed I1 authority.

### H-013 CP-B runtime prompt update and UI lane
[Prompt source hashes](../operations/H-013/cp-b-prompt-receipt.json) pin policy v2 plan/SQL source templates for bounded per-step DAG proposals, actual typed dependency binding and shared adapter grammar. Scripted-provider tests are offline consumption, not live request/accuracy evidence. [Actual UI delegation/follow-up projection](../operations/H-013/ui-task.txt) records this lane's scope/coverage and explicit omissions. Historical prompt files/evidence are not overwritten; actual CP-C continuation/browser coverage remains pending.
