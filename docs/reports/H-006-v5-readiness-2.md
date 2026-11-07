# H-006-v5 D2 - readiness after local OMX repair

Date: 2026-11-07T10:22:48.750545+00:00. Mode: solo diagnostics. **ready-for-direct-invocation**, not executed B.

- Git root `/home/dev/projects/universitydb`, `main`, HEAD `8931d832d49311ac0d63c3a7a359b4293058da89`. A was not repeated. Staging is empty, there are no remotes; The working tree is initially dirty.
- All **78/78** source files of the repair baseline, including research/blocker/evidence, are unchanged. Seven mandatory SHA-256s are retained; Git index matches the repair baseline. The old documents and Obsidian have not changed.
- Codex **0.162.1**, OMX **0.21.46 + local compatibility patch**, Node **22.23.2**. Repo launcher and `/home/dev/.omx/runtime/bin/omx` are identical and point to a verified installed runtime.
- In sandbox doctor: **17/0/3**, `spawnSync EPERM`, PID not visible, `stale-dead/bad_selectors=CODEX_SESSION_ID`. Standard allowed read-only host check: **20/0/0**; binding `session-authority/usable`, the same owner PID and identity are checked. This is a context difference, not a current ID mismatch. Neither selectors nor pointer/tracker were fixed.
- Native hooks **9/9** are registered, enabled and have matching trust hashes, including `UserPromptSubmit`, `SubagentStart`, `SubagentStop`. Actual D triage delivered; built-in minimal doctor smoke is successful. `hooks status` separately shows 0 plugins and does not replace native checks.
- Planner, Architect, Critic, researcher, dependency-expert: TOML installed/valid; the roles are present in the current native `agent_type` schema. **Nobody started in D**. Adapted-authority preflight is not applicable.
- Local ralplan/plan have been read. Additional quality gates: `[]`; Mandatory sequential reviewers are not canceled by this.
- There is no new Ralplan state - normal until a direct call. The old generation `0748daa2-4c89-4a84-a305-486ed1f480a3` canceled/abandoned, was not renewed. Current tracker leader matches the native ID of the new pointer.

## Limitations and Observations

Of the 8 installed-manifest hashes, 7 matched; the only semantic addition to config after repair is `service_tier=fast`; hooks/trust are not changed. The frozen vault manifest matched 20/25: five status/workflow/index/review/question pages contain a follow-up CHAT-022 about research and cancellation. Their current hashes are saved; requirements/contract/PDF without drift. The old next-step in these pages is historical regarding the current direct order for repairs. Full Subject Reading/PDF delayed until B.

New Advisory activation, real reviewers and the entire closeout after the renovation **not yet verified**. The doctor's success does not prove the entire lifecycle. After a separate direct call in the same leading session, you need to confirm the new advisory variant/generation/session/root/turn to Planner. IDs should not be assigned manually. The rights to the future B commit were not checked by the record.

## Artifacts and border

- [Structured diagnostics](../operations/H-006-v5-readiness-2.json).
- [Baseline and original SHA-256](../operations/H-006-v5-readiness-2-evidence/baseline.json).
- [Host binding/hooks/roles](../operations/H-006-v5-readiness-2-evidence/host-binding-hooks-roles.json), [host doctor](../operations/H-006-v5-readiness-2-evidence/host-doctor-command.json), [sandbox commands](../operations/H-006-v5-readiness-2-evidence/commands.json).
- [Actual prompt](../ai/omx/H-006-v5-D2-actual-prompt.txt), [coverage/redactions](../ai/omx/H-006-v5-D2-prompt-coverage.json).

Saved locally, **not committed**, not pushed/public. Setup/update/repair, activation, subagents, design, application and paid/live calls were not performed. Product tests not-run: D does not create applications. No blockers for direct calls have been identified; the diagnostic restrictions above are retained. **Stops until separate direct call.**
