# H-008 — $10 continuation authority / native-resume blocker

2026-11-07. **Docs-only checkpoint; same I1/G004 blocked, I1 not complete.** The user approved one total **10 USD** continuation cap, including old recorded spend/holds and every smoke, S6, mutation, UI, retry, failure and access-check attempt. This is not a fresh allowance per launch. Exact model remains **gpt-6.1-sol**, plan **high**, SQL/repair **medium**; no further model-choice or budget request is needed. [Actual user task and path-redaction receipt](../ai/omx/H-008-cap10-prompt-receipt.json) preserve this authority. The previous [H-008 report](H-008-sol-profile-I1-continuation.md) stays unchanged as historical evidence; its missing-cap/access wording is superseded only by the observations below.

## First gate: native goal did not resume

[Root-attributed observations](../operations/H-008/cap10-resume/root-observations.json) distinguish actual root checks from this docs performer's work:

- Root's actual native `get_goal` still returned **blocked** for the existing aggregate. CLI reconciliation returned exactly **`Codex goal status mismatch: expected active, got blocked.`**
- Exposed goal controls read/create or update to complete/blocked/paused; none exposes resume/active. No owner-UI automation control was available. A session/CLI resume is not proof of native goal activation.
- G001–G003 remain complete; existing G004 is in-progress, attempt1, with a blocked checkpoint. Root reports a supported annotation of that existing G004 with the current authority/evidence; this does not reactivate the native goal.
- No replacement goal/plan, fabricated IDs, manual state edits, repeated identical restarts, competing leader, OMX repair or closed H-006 lifecycle action was used.

**Minimal conditional owner step:** if the existing thread actually exposes a native goal **Resume** control, its owner can use that control. Root must then read the same goal and observe **active** before proceeding. This report does not assert that the control exists or that using it will fix the mismatch. If it is not exposed, the blocker is an **unsupported owner/runtime resume capability in the available interface**, not missing model or budget approval. No invented slash command or hidden API is offered.

## Credentials and shared budget

User reports a rotated private credentials file and revocation of the old key. Root reports sourcing it only in the launching shell after disabling xtrace and clearing the inherited key, with stdout/stderr suppressed; the only printed result was **key presence TRUE**. This establishes neither usable account/model access nor repaired native state. This performer did not open/source the credentials file. No file contents, key, environment dump or headers are included in documentation, exports, logs or Git.

For any later authorized application launch, keep that secure launch rule: load the rotated **private credentials file** in the actual launching shell with tracing disabled, do not reuse a possibly stale inherited key, suppress source output and check presence only. Keep the path private. Do not send the file to a model. No application was launched for this checkpoint.

Root observed **`runtime/spending.json` absent**: local recorded spend **0 USD**, effective holds **0 USD**, remaining under the approved total cap **10 USD**, paid requests **0**. No ledger was created, reset, migrated or deleted. This is the reported local recorded-ledger state, **not** an independently verified provider invoice/account history. Preserve all earlier monetary records and uncertain holds; any discovered prior amounts count against the same 10 USD, not an additional allowance. No automatic rate migration or reset is authorized.

Current rates, selected-tier applicability, full-request input coverage and reservations were **not verified**, because the user requires native resume first. No `BILLING_VERIFIED` assertion was made. A key plus approval does not prove model access. After a real active native status is verified, these billing/input/access gates still apply before paid requests, all within the same total cap.

## Checkpoint evidence and limits

Starting HEAD was `5c127c526852277d7989b744e777fb1f38c1f65f` on main; [baseline](../operations/H-008/cap10-resume/baseline.json) pins protected documents and pre-existing untracked locks/receipts. A/B, configuration checkpoint `cfaf8601b8b985687b45ae4f9792891ee75064f4`, later H-008 checkpoint and all historical evidence are preserved. No reset/clean/amend, remote/push, vault write, dependency/configuration/source/runtime-prompt change or monetary spending-ledger mutation was performed. The local docs checkpoint does not complete I1 or change the blocked native status. Its actual commit SHA is recorded only after a successful commit, in a separate untracked receipt.

[Prompt coverage](../ai/README.md#h-008-cap10-native-resume-cutoff) distinguishes the selected actual root task from the actual received performer-task projection; full tool/private instruction/child history is not claimed. U-01 remains partial. [Targeted documentation validation](../operations/H-008/cap10-resume/document-validation.json) records JSON, local links, whitespace, privacy-pattern, diff and preservation checks. No application/provider/SDK probes, product tests, repeated offline setup or old H-008 input-manifest validation ran: this checkpoint changes documentation only.

**Not run:** live S6, independently changed live example, live UI screenshot, full live trace, real usage or final live acceptance gates. Existing offline evidence is not new live accuracy. I1 stays **not complete**; R-15 publication stays open. No I2–I5, defense, remote/push or Obsidian writes. Stop after the verified local docs checkpoint/report; root owns the supported blocked checkpoint and final report.
