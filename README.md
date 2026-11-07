# UniversityDB — limited I1/S6 demonstrator

**Partial: offline verified, not live accepted.** Real LangGraph + SQLite + Streamlit are implemented; no real model call has been authorized/run. This is only H-007 I1, not the complete assignment or I2–I5. ADR003–007 remain proposed; scoped rationale: [ADR008](docs/adr/ADR-OMX-008-I1-scoped-implementation.md).

## Install and verify (repository root, Python 3.12)

```bash
uv sync --locked
uv run --locked pytest -q
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked mypy src/universitydb --ignore-missing-imports
uv run --locked python -m compileall -q src
```

Test dependencies are in the locked dev group. `.venv`, binary DB, local traces, credentials and spending ledger are ignored. SQL is source-controlled in `resources/schema.sql` and `resources/seed.sql`; first UI submission creates `runtime/university.db` without overwriting an existing database. Run from this checkout so those resources are available.

## Run local UI

```bash
uv run --locked streamlit run src/universitydb/ui.py \
  --server.address=127.0.0.1 --server.port=8501 --server.headless=true \
  --browser.gatherUsageStats=false
```

Open `http://127.0.0.1:8501`. The default question explicitly specifies `student_id=2`, `course_id=1`, `teacher_id=10`, semester `S1`. Two F1 enrollments have6000/10000 units; independently expected raw components16000/2/2 and answer **80.00**. The graph first asks for a typed plan, then a separate SQL proposal; it never switches to a canned answer. Without locally supplied approved configuration the UI shows `PROVIDER_UNAVAILABLE`, not80.00. SQL/parameters, typed rows and complete same-run trace are expandable/downloadable; failures clear prior answers.

### Real provider gate — not yet exercised

Do not send a key in chat. First obtain explicit approval of the **specific model**, account access and total smoke/retry cost cap; verify current model-specific API compatibility/rates. Only then export local variables described in `.env.example`: API key, model, `UNIVERSITYDB_LIVE_APPROVED=yes`, total cap and input/output USD-per-million rates. `.env` is not automatically loaded. No model default, fallback or inherited $2 authorization exists.

All submissions/retries share `runtime/spending.json`: each attempt reserves12000 input/2000 output tokens at supplied rates before dispatch; observed usage/cost estimates are added afterwards. Reservations, including failed/uncertain requests and unused successful capacity, are deliberately not freed. Keep that ledger across smoke/retry/mutation runs; deleting/changing it is not a budget-reset permission. Rates exclude unverified taxes/fees; byte gates are not exact provider tokenization and usage surprises fail closed. This is a conservative local spending controller, not provider-side billing enforcement.

### Offline/injected evidence

`pytest` injects scripted proposals into the **real compiled graph and real SQLite**. Developer-only browser checks can supply `UNIVERSITYDB_TEST_MODE=1` plus `UNIVERSITYDB_TEST_FIXTURE=/absolute/path/to/scripted-proposals.json` (array of closed plan/SQL proposals). Normal UI never selects this from user question text. The yellow profile banner and trace explicitly label **offline/injected**, zero real provider calls. Do not use injected evidence as NL→SQL accuracy or live E2E acceptance.

[Offline screenshots, traces and browser receipt](docs/operations/H-007/evidence/) show S6 and unsupported-input failure. [Preparation/capability limits](docs/operations/H-007/preparation.md) distinguish working goal APIs from degraded phase-state persistence. A/B and historical evidence are preserved.

## Boundaries and limits

- Only one explicit four-filter scalar grade mean; no implicit semester, ambiguous names, free SQL, other metrics, multi-step, Library, resume, full eval48/48 or production deployment. Unsupported input fails; ID labels in text are not a full NL intent/identity validator.
- Core `agent.py` has no University table identifiers; `domain.py` owns descriptor, scope, exact aggregate subset and integer-hundredths formatter. This boundary is not proof of second-schema portability.
- SQLGlot parses **one** SELECT; domain validation requires the exact supported relation/aggregate/four bound predicates, no extra clauses/subqueries/writes. SQLite runs mode=ro with function/schema authorizer and extension denial in a disposable worker. Cooperative timeout2s plus independent process kill3s are tested. Safe SQL does not prove arbitrary NL semantics.
- Provider max retries0, application at most one transient retry and one syntax repair, ≤5calls/≤4SQL attempts; request≤2000chars, SQL≤8000bytes/chars, input byte gate12000, output≤2000tokens,100result rows/64KiB, trace1MiB. Provider SDK runs in a disposable subprocess with parent wall-clock kill/reap at min(15s, remaining60s run deadline); stalled-worker termination and retained spending are tested offline. Synthetic loopback use only; no hard memory isolation/authentication/remote deployment claim.
- Full JSONL includes actual nodes/attempts, hashes, typed rows, usage and terminal status. Answer and terminal event must persist before publishing success. No secrets/raw provider exceptions are exposed.

## Next gate / stop

Complete cleaner and independent code-reviewer/architect checks, then authorized real-model S6 and changed input/data with different oracle, browser live screenshot and full trace. Until then **I1-not-complete/live-not-run**. U-01 prompt coverage remains explicitly partial; U-04/R-13 rationale is scoped, R-15 publication stays open. No remote/push, defense or later implementation stage is authorized.
