# UniversityDB — limited I1/S6 demonstrator

**Published checkpoint: I1 complete; I2–I5 pending.** Native completion and strict checkpoint are recorded in [the final receipt](docs/operations/H-009/closeout/postcheckpoint-goal-receipt.json). The owner subsequently reported all four manual live checks passed; [acceptance record](docs/reports/I1-owner-manual-acceptance.md). Historical phase instructions below describe their original execution context, not a requirement to reopen the completed I1 goal.

**Limited I1 application/live acceptance gates passed.** Real compiled LangGraph → exact Sol plan/SQL → checked readonly SQLite → deterministic **80.00** passed, plus independent changed input **90.00**. Normal browser UI80.00, expanded SQL/typed DB/full trace and stale-answer failure checks passed; fresh final independent reviews APPROVE/CLEAR passed; root native completion/strict-checkpoint proof follows separately, not pre-claimed here. One total USD10 practical authority, USD8 new-dispatch threshold and USD2 contingency remain **not a strict invoice guarantee**. [Live closeout/evidence](docs/reports/H-009-live-I1-closeout.md); ADR003–007 stay proposed, [scoped ADR008](docs/adr/ADR-OMX-008-I1-scoped-implementation.md)/[ADR010](docs/adr/ADR-OMX-010-I1-practical-budget-policy.md). No I2–I5 or full-service acceptance.

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

### Real provider — practical policy and required launch gates

Approved model remains **gpt-6.1-sol**, plan **high**, SQL/repair **medium**, default service tier. Before any live launch root must observe fresh native `get_goal=active` for the same existing aggregate goal and passing offline policy checks. If still blocked after the offline checkpoint, enter **`/goal resume` in the composer of this same Codex session**. A supported OMX story handoff is not native resume. Do not create a new plan/goal or repeat G001–G003.

Use `UNIVERSITYDB_BUDGET_POLICY=practical-v1`, `UNIVERSITYDB_RATES_CONFIRMED=yes` only after current applicable-rate review, `UNIVERSITYDB_LIVE_APPROVED=yes`, exact approved model, total cap10 and documented conservative rates5.50/M input and11/M output from `.env.example`. Rates-confirmed attests rate review, not exact tokenization or a guaranteed invoice. **Do not set `UNIVERSITYDB_BILLING_VERIFIED=yes`: the former strict input/count-fee proof was replaced, not achieved.** No count endpoint or content-free paid access probe is allowed; first authorized generation must contribute to live S6. Presence of a key does not prove model access. Current rate/endpoint evidence: [H-009 references](docs/operations/H-009/api-references.md). `.env` is not loaded automatically.

For every application launch, disable shell xtrace, clear the stale inherited API key and source the owner-provided private credentials file in the launching shell with output suppressed. Check presence only. Never expose the private path/file, values, environment, headers or raw exceptions in logs, prompts, exports, screenshots or Git. Do not send credentials to a model.

All submissions, failures, retries, UI launches and restarts share **one** `runtime/spending.json` with a stable separate lock. Atomically admit only `accounted_total + next_reservation <= USD8` and reserve before dispatch. Each attempt retains `max(reservation, observed estimated cost)`; never add the same hold twice, release old uncertain holds or reset history. USD2 is contingency, not automatic extra dispatch authority. Model/cap/rates are pinned; mismatches and invalid/nonfinite/negative accounting fail closed. Existing empty, malformed or missing-after-use ledgers fail closed. This is local accounting, **not provider-side billing enforcement or an invoice audit**.

Estimate the full assembled serialized request, including instructions, input, strict JSON schema and all present request fields, plus1024 framing allowance. Retain the12000-byte full-payload-plus-framing gate; the byte-derived estimate is **not exact tokenization/a proven bound**. Output reservation32768 includes reasoning and visible tokens. After every response preserve usage/model/tier; missing/invalid/excess usage or model/tier mismatch durably stops further dispatch and retries while retaining facts/hold. Lower-than-reserved usage is normal; reservation is not refunded. See [ADR010](docs/adr/ADR-OMX-010-I1-practical-budget-policy.md).

### Offline/injected evidence

`pytest` injects scripted proposals into the **real compiled graph and real SQLite**. Developer-only browser checks can supply `UNIVERSITYDB_TEST_MODE=1` plus `UNIVERSITYDB_TEST_FIXTURE=/absolute/path/to/scripted-proposals.json` (array of closed plan/SQL proposals). Normal UI never selects this from user question text. The yellow profile banner and trace explicitly label **offline/injected**, zero real provider calls. Do not use injected evidence as NL→SQL accuracy or live E2E acceptance.

[Offline screenshots, traces and browser receipt](docs/operations/H-007/evidence/) show S6 and unsupported-input failure. [Preparation/capability limits](docs/operations/H-007/preparation.md) distinguish working goal APIs from degraded phase-state persistence. A/B and historical evidence are preserved.

## Boundaries and limits

- Only one explicit four-filter scalar grade mean; no implicit semester, ambiguous names, free SQL, other metrics, multi-step, Library, resume, full eval48/48 or production deployment. Unsupported input fails; ID labels in text are not a full NL intent/identity validator.
- Core `agent.py` has no University table identifiers; `domain.py` owns descriptor, scope, exact aggregate subset and integer-hundredths formatter. This boundary is not proof of second-schema portability.
- SQLGlot parses **one** SELECT; domain validation requires the exact supported relation/aggregate/four bound predicates, no extra clauses/subqueries/writes. SQLite runs mode=ro with function/schema authorizer and extension denial in a disposable worker. Cooperative timeout2s plus independent process kill3s are tested. Safe SQL does not prove arbitrary NL semantics.
- Provider max retries0, application at most one transient retry and one syntax repair, ≤5calls/≤4SQL attempts; request≤2000chars, SQL≤8000bytes/chars, full serialized-payload plus1024 framing estimate gate12000, output≤32768tokens (reasoning+visible),100result rows/64KiB, trace1MiB. Provider SDK runs in a disposable subprocess with parent wall-clock kill/reap at min(plan60s or SQL/repair45s, remaining180s run deadline); stalled-worker termination and retained spending are tested offline. Deadline checks assume responsive trusted local storage: synchronous parent DB inspection/hashing, ledger/trace filesystem I/O and lock acquisition are not independently killed, so this is not a hard180s guarantee under every filesystem/lock failure. Synthetic loopback use only; no hard memory isolation/authentication/remote deployment claim.
- Central validated profile: `src/universitydb/config.py`; Responses explicitly sends store false, default tier and operation reasoning effort; no temperature/top_p. Strict JSON-schema requests and completed Pydantic validation are tested offline against the installed SDK; raw failure status/usage is captured before typed parsing. Unknown operation/config/schema fails before dispatch. Returned model/tier mismatch fails after preserving usage. Aggregate token envelope223840 includes every retry/repair; input quantities remain estimates, not a billing bound. These output/time envelopes succeeded for the measured S6/mutation/UI calls only and remain **provisional for other prompts/load/failures**, not general live sufficiency; see [ADR009](docs/adr/ADR-OMX-009-Sol-operation-profile.md) and [official reference research](docs/operations/H-008/api-references.md).
- Full JSONL includes actual nodes/attempts, hashes, typed rows, usage and terminal status. Answer and terminal event must persist before publishing success. No secrets/raw provider exceptions are exposed.

## Next gate / stop

[H-009 offline checkpoint](docs/reports/H-009-practical-budget-I1.md) is historical; [current live closeout](docs/reports/H-009-live-I1-closeout.md) records actual calls, passed live UI/final independent review and accounting; root lifecycle postconditions follow separately. Historical H-008 reports preserve earlier strict-proof blockers; **do not restart that proof search**. Only after native resume and passing practical-policy gates continue existing G004 with real S6→80.00, an independently changed example/different oracle, live UI screenshots and full same-run trace. Live S6/mutation are now proven in the [current closeout](docs/reports/H-009-live-I1-closeout.md); live UI and final independent reviews passed. Root native lifecycle proof follows separately. No mock/injected evidence substitutes for live. Final cleaner, independent code-reviewer/architect and invariant gate remain mandatory before I1 completion.

U-01 prompt coverage remains partial; U-04/R-13 rationale is scoped. R-15/public delivery remains a future obligation, not fulfilled by a local commit. No remote/push, defense or later implementation stage is authorized.
