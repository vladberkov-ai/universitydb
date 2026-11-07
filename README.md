# UniversityDB — limited I1/S6 demonstrator

**Partial: offline verified, not live accepted.** Real LangGraph + SQLite + Streamlit are implemented; no real model call has been authorized/run. This is only H-008 continuation of H-007 I1, not the complete assignment or I2–I5. ADR003–007 remain proposed; scoped rationale: [ADR008](docs/adr/ADR-OMX-008-I1-scoped-implementation.md).

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

Do not send a key in chat. Model already approved: **gpt-6.1-sol**, plan **high**, SQL/repair **medium**. Account access and an explicit total continuation cost cap remain required; verify current applicable rates and full-request input-token coverage. Do not ask for model choice again. Only then export local variables described in `.env.example`: API key, exact approved model, `UNIVERSITYDB_LIVE_APPROVED=yes`, total cap and conservative input/output USD-per-million rates. Set `UNIVERSITYDB_BILLING_VERIFIED=yes` only after verifying rates cover all applicable input categories (including cache writes/region premiums) and the full-request input bound; do not set it speculatively. `.env` is not automatically loaded. No fallback or inherited $2 authorization exists. A numeric cap or a key alone is not owner approval.

All submissions/retries share `runtime/spending.json` and a stable separate lock: each attempt reserves12000 input/32768 output tokens at verified conservative rates before dispatch; observed usage/cost estimates are added afterwards. Each attempt retains max(reservation, actual observed cost); unknown failed holds are never freed. Known actual excess durably increases effective spend and blocks further dispatch when the cap is exceeded. Atomic fsynced replacement under a stable separate lock prevents partial rewrites; existing empty/malformed/missing-after-use ledgers fail closed, never reset to zero. Model/cap/rates are pinned to that ledger profile. Keep that ledger across smoke/retry/mutation runs; deleting/changing it is not a budget-reset permission. Changing the operation policy preserves old per-attempt holds under the same monetary profile/cap; changed cap/model/rates fail closed, not a new independent budget. Rates exclude unverified taxes/fees; byte gates include prompt/payload/schema plus1024framing cushion but are not exact provider tokenization. Input coverage remains a required live gate and usage surprises fail closed. This is a conservative local spending controller, not provider-side billing enforcement.

### Offline/injected evidence

`pytest` injects scripted proposals into the **real compiled graph and real SQLite**. Developer-only browser checks can supply `UNIVERSITYDB_TEST_MODE=1` plus `UNIVERSITYDB_TEST_FIXTURE=/absolute/path/to/scripted-proposals.json` (array of closed plan/SQL proposals). Normal UI never selects this from user question text. The yellow profile banner and trace explicitly label **offline/injected**, zero real provider calls. Do not use injected evidence as NL→SQL accuracy or live E2E acceptance.

[Offline screenshots, traces and browser receipt](docs/operations/H-007/evidence/) show S6 and unsupported-input failure. [Preparation/capability limits](docs/operations/H-007/preparation.md) distinguish working goal APIs from degraded phase-state persistence. A/B and historical evidence are preserved.

## Boundaries and limits

- Only one explicit four-filter scalar grade mean; no implicit semester, ambiguous names, free SQL, other metrics, multi-step, Library, resume, full eval48/48 or production deployment. Unsupported input fails; ID labels in text are not a full NL intent/identity validator.
- Core `agent.py` has no University table identifiers; `domain.py` owns descriptor, scope, exact aggregate subset and integer-hundredths formatter. This boundary is not proof of second-schema portability.
- SQLGlot parses **one** SELECT; domain validation requires the exact supported relation/aggregate/four bound predicates, no extra clauses/subqueries/writes. SQLite runs mode=ro with function/schema authorizer and extension denial in a disposable worker. Cooperative timeout2s plus independent process kill3s are tested. Safe SQL does not prove arbitrary NL semantics.
- Provider max retries0, application at most one transient retry and one syntax repair, ≤5calls/≤4SQL attempts; request≤2000chars, SQL≤8000bytes/chars, input byte gate12000 including schema/framing cushion, output≤32768tokens (reasoning+visible),100result rows/64KiB, trace1MiB. Provider SDK runs in a disposable subprocess with parent wall-clock kill/reap at min(plan60s or SQL/repair45s, remaining180s run deadline); stalled-worker termination and retained spending are tested offline. Deadline checks assume responsive trusted local storage: synchronous parent DB inspection/hashing, ledger/trace filesystem I/O and lock acquisition are not independently killed, so this is not a hard180s guarantee under every filesystem/lock failure. Synthetic loopback use only; no hard memory isolation/authentication/remote deployment claim.
- Central validated profile: `src/universitydb/config.py`; Responses explicitly sends store false, default tier and operation reasoning effort; no temperature/top_p. SDK strict parsing is tested offline. Unknown operation/config/schema fails before dispatch. Returned model/tier mismatch fails after preserving usage. Aggregate reserved token bound223840 includes every retry/repair. These output/time envelopes are **provisional, not live-proven adequate**; see [ADR009](docs/adr/ADR-OMX-009-Sol-operation-profile.md) and [official reference research](docs/operations/H-008/api-references.md).
- Full JSONL includes actual nodes/attempts, hashes, typed rows, usage and terminal status. Answer and terminal event must persist before publishing success. No secrets/raw provider exceptions are exposed.

## Next gate / stop

H-008 configuration verification/review evidence is tracked in [current report](docs/reports/H-008-sol-profile-I1-continuation.md). Then authorized real-model S6 and changed input/data with different oracle, browser live screenshot and full trace. Until then **I1-not-complete/live-not-run**. U-01 prompt coverage remains explicitly partial; U-04/R-13 rationale is scoped, R-15 publication stays open. No remote/push, defense or later implementation stage is authorized.
