# Independent round1 — bounded core repair receipt

Root supplied actual independent REQUEST_CHANGES and authorized repairs only after
the frozen976e candidate's full process exited (383passed131.61s/static pass).
That historical pass was not review approval. Root owns existing aggregate/G013,
Git checkpoint, final candidate/full/browser/re-review and completion. This lane
changed no workflow/native/Git, monetary, credential, live or vault state.

## Before-code decisions / minimal changes
Current acceptance contract/ADR012 notes were written by the separate docs lane
before dependent code. No new budget, dependency, domain semantics or broad
framework. Product changes are confined to agent.py, db.py, db_worker.py.

1. **Immutable bounded replay identities.**32 frozen identity records hold original
   fingerprint/run ID/expiry; separate bulky cached results may expire, identities
   never FIFO-reset.8 unexpired contexts are retained even when terminal; unknown
   ninth run fails RESOURCE_LIMIT. Expired exact payload returns RESUME_EXPIRED,
   changed payload REPLAY_CONFLICT; full32 records fail closed for unknown run or
   resume IDs before dispatch. Explicit new Agent/session is the recovery, not an
   automatic reset. Exact owned expired saver threads/results are deleted while
   tombstones remain; trace readback derives only from trusted server-issued IDs.
2. **One owning rejection path.** Both run replay and resume failures preserve owned
   run/trace identity and full events. Pending expiry or actual data/schema/policy
   changes terminalize the trace; already terminal JSONL is immutable. Foreign
   session rejection occurs before lookup and exposes neither ID nor events.
3. **Inclusive TTL.** Every accepted record, including terminal replies and resume
   receipts, expires at original run creation+900; equality is expired. Human wait
   still does not consume active-work budget; shared counters/bounds unchanged.
4. **SQLite operational errors are not SQL repair.** Base/extended BUSY, LOCKED,
   CANTOPEN, IOERR return DB_UNAVAILABLE; CORRUPT/NOTADB/SCHEMA/CONSTRAINT return
   DATA_INCONSISTENT; only true syntax/incomplete-input/unknown-column is SQL_INVALID.
   Existing authorizer and cooperative timeout precedence remain. Real post-startup
   exclusive locking and direct worker locking prove no repair/provider redispatch.
5. **Main-file identity requires supported DELETE journal mode.** Trusted startup
   rejects WAL/non-DELETE; replay/resume/execute recheck mode with0.5s read-only
   inspection before relying on main-file hash. No journal mutation or concurrent
   snapshot feature. Temporary WAL regression demonstrates actual visible grade
   mutation while main-file hash stays unchanged, then startup rejection0calls;
   mode change after a pause is also rejected before remaining provider work.

## Behavior locks and actual verification
- Before product edits: new10-case regression set →8failed/2passed, concretely
  exposing context eviction, expiry/replay identity/trace and WAL/lock issues.
- After first repair:35 targeted tests passed11.21s.
- Expanded intermediate run42passed/9failed10.99s:9 test-fixture NameErrors from an
  import removed by earlier unused-import cleanup; restored the required import.
  No product assertion weakened. Fresh next51tests passed14.02s.
- Final serialized command: `pytest -q tests/test_review_repairs.py
  tests/test_i2_continuation.py
  tests/test_practical_budget.py::test_uncertain_live_failure_never_application_retried
  tests/test_provider_worker.py::test_whole_graph_deadline_bounds_stalled_provider`
  → **54passed16.13s**. Original accounting-stop/whole-run deadline assertions remain
  unchanged. All commands use writable temporary uv cache and isolated DB/runtime.
- Owned-path Ruff/format(4 files), strict mypy(3 product modules), diff check pass.
  No concurrent heavy test or UI/browser process from this lane.

## M1 actual checkpoint composition
New real compiled-graph test pauses AFTER the accepted planning call and BEFORE SQL,
then resumes S1 using the retained plan. Actual dependencies bind course[2] then
student[1], answer95.00, same-run trace, total4provider calls/3SQL/1clarification;
exact accepted resume replay adds0calls. [Proof](m1-resume.json), matching full
[JSONL](m1-resume.jsonl) and source hashes [manifest](manifest.json) are captured from
that same54-pass process, not a separate fabricated/canned trace. Provider is
explicitly offline/injected, not real-model NL-to-SQL accuracy. Final root candidate
must recapture exact source after any later changes rather than relabel this proof.

Source/tests are frozen for root's candidate checkpoint and independent re-review.
No APPROVE/CLEAR, final tested SHA, final browser or native completion is claimed by
this performer. Prior failure evidence/checkpoints/I1/ledger/locks remain unchanged.
