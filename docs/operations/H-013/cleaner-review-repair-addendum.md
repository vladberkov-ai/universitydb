# Cleaner inventory addendum — repaired candidate, no-op proposed

Written **after core repair freeze**, before final repaired-candidate full verification.
Scope: actual new `Agent` request/tombstone/owner-rejection/expiry helpers, trusted
DELETE-journal DB identity gate and worker error taxonomy; no new source edits by
this inventory writer. Prior two approved smell removals remain done. The original
383-test cleaned-candidate pass is superseded, **not proof of these later repairs**.
Root independently reviews this addendum; proposed selection is **no additional
cleanup**, pending real final review/full/browser evidence.

## Actual fallback/boundary inventory
| Actual helper/change | Classification and grounding | Disposition/behavior locks |
|---|---|---|
| `Agent._request/_remember` immutable request fingerprints/tombstones; distinct `_responses` payload cache | Grounded fail-closed identity boundary, not cache-eviction fallback.32 identities cannot silently disappear/reexecute; expiry removes bulky response but retains ID fingerprint/run/expiry. Capacity error names explicit new-session recovery. | Preserve. `test_32_immutable_identities_survive_expired_context_cleanup`, `test_full_registry_resume_fails_closed_before_dispatch`; no FIFO/reset/shim added. |
| `_prune_expired_contexts` inclusive900 expiry + supported saver.delete_thread on exact owned run;8 unexpired-context capacity | Grounded bounded cleanup of expired application state, not native state/ID manipulation or unexpired-context eviction. Same accepted identity is still tombstoned. | Preserve.8context test, inclusive TTL/replay tests, expired cleanup test. No durable restart/cross-session identity promise. |
| `_owned_events/_owner_rejection` exact server-issued owning run, bounded persisted JSONL read/sequence/run/end validation, live rejection diagnostic vs immutable terminal history | Grounded fail-safe evidence recovery after bulky expired-context cleanup, not a fabricated new run or untrusted arbitrary file read. Missing/corrupt/oversize trace yields TRACE_UNAVAILABLE, never success; foreign requests do not touch/disclose target trace. | Preserve. `test_start_replay_actual_binding_change_has_owner_trace`, exact-run TTL/owner tests, foreign nondisclosure test. Final independent reviewers assess trace/envelope semantics; no self-approval. |
| `_check_journal/validate_identity` DELETE-only trusted gate reused before execute/resume/replay | Grounded restriction closing demonstrated main-file/WAL identity gap; no conversion of user's mode, fallback to unsupported journal, query-authorizer relaxation or concurrent-writer feature. | Preserve. Actual temporary WAL stable-mainhash/changed-visible-data, startup/resume/execute and binding-change tests. Main SHA only meaningful behind this declared supported-mode boundary. |
| `db_worker.run` SQLite primary-code taxonomy; fallback unknown DB error→terminalDB_UNAVAILABLE | Grounded external availability/integrity/resource boundary. Actual lock cannot be disguised as repairable SQL; only syntax/incomplete/unknown-column subset yields SQL_INVALID. Authorizer denial/timeout remain distinct. Unknown SQLite failure is terminal, not retry/success. | Preserve. Real post-startup worker BUSY, code taxonomy and repairable-subset tests. No generic successful fallback/OverflowError swallowing. |
| M1 plan/checkpoint continuation proof added | Behavior proof, not production fallback or fixedquery substitute: completed plan retained, actual downstream refs/SQL/rows and common counters verified on real saver/SQLite. | Preserve. `test_m1_plan_checkpoint_resume_keeps_actual_dependencies_and_budgets`, matching durable proof/JSONL. Final exact-source capture remains required after full run. |

## Smells/selection
No concrete dead branch, redundant validation or needless new abstraction was proven
in this bounded repaired surface. New small helpers centralize previously duplicated
ownership/identity boundaries with explicit failure paths. **Select no-op**, not
speculative deletion/large Agent context refactor. Keep typed errors, exact field/
size checks and all baseline accounting/safety assertions. Capacity/expiry are explicit
contract failures, not hidden reset behavior. UI/design unchanged.

## Evidence and next gate
Core's actual frozen repair batch:54targeted tests passed16.13s (continuation,
accounting/deadline, registry/owner/TTL/WAL/lock/M1proof); Ruff/format4/mypy3/diff passed.
This is targeted evidence, not full repaired-candidate verification. Root's independent
addendum verdict must precede a no-op-cleaner acceptance; then pin exact repaired SHA,
serialized full/static tests, frozen allcase browser and structured M1/portability/
resume proof, fresh independent code-reviewer/architect verdicts and configured gates.
No product/source cleanup or new dependency was made by this document. No live/API/
count/credentials/monetary/I1/locks/vault/native writes. Prior failures/383pass and
REQUEST CHANGES/BLOCK remain historical evidence, not retroactive final success.
