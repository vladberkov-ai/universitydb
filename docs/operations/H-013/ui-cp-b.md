# H-013 CP-B UI foundation receipt

Scope: actual [UI delegation](ui-task.txt); no core/domain/DB/LLM implementation edits by this lane. Root owns workflow, integration and native checkpoints. This is a foundation receipt, **not whole I2+I3 completion**.

## Implemented
- Existing AppTests now create temporary roots/resources and clear key/live approval/tracing; actual runtime/monetary ledger is never their target. New tests compare actual repository runtime file hashes before/after each scenario.
- University/Library selector composes separate domain factories and resource directories outside core; each selected schema has its own temporary DB. Switching clears old result and discards the other context's agent.
- Retain Agent/provider in Streamlit server session across reruns, keyed by root/schema/test-mode/fixture content hash. Normal profile has no hidden fixture fallback. Scripted fixtures require explicit test environment, support schema-keyed output sequences and controlled injected Failure records; question text cannot enable injection.
- English answer/error/clarification view, SQL/bindings/all attempts, raw typed per-step DB rows, adapted step results/dependency bindings, complete same-run events and JSONL download. New request/error/context change clears prior answer. Actual graph continuation hooks are prepared but **not yet exercised before CP-C core API**.

## Fresh evidence
`env -u OPENAI_API_KEY UV_CACHE_DIR=/tmp/universitydb-h013-uv-cache UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_ui.py tests/test_i2_ui.py` → exit0,5 passed. Includes S6→80.00, retained agent/provider call count across rerun, actual Library SQLite→Ada1/Bob1 with separate DB, and injected refusal after success clearing stale answer/full same-run terminal trace. Not real-model NL→SQL accuracy.

Own `ruff check` and `ruff format` passed; `mypy src/universitydb/ui.py --ignore-missing-imports` passed; `git diff --check` passed. Initial default uv cache attempt failed EROFS before tests; temporary writable cache used next (no dependency/lock change). During concurrent domain implementation an intermediate S6 failed generic function allowlist; reported to domain owner, fixed there; final5 UI tests passed. Root runs final integrated regression/static checks on frozen product tree before commit.

Actual browser is not-run at CP-B. Cached isolated Playwright plus Chromium1228 readiness checked without launch or dependencies; CP-C/E require actual success/clarification/M1/Library/repair/error browser/screenshots/trace and exact owned-server shutdown. Historical live browser helper was read, never run. No live/count, credentials, spending/holds/ledger, vault, remote/push or runtime-ID mutations. Existing I1/H011 evidence and locks untouched.
