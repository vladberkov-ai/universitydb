# University Database + LangGraph QA Agent

A local question-answering service using LangGraph, generated SQLite queries,
typed results and an inspectable Streamlit interface. Two synthetic datasets are
included: University and Library. This repository contains the assignment code,
schemas, seed data, tests, decisions, prompt collections and execution evidence.

## Current status

**The expanded service is implemented and repaired offline. Real-model validation
of the repaired version is still pending.** University supports means/counts,
JOIN listings, grouping, exact ties, optional filters, clarification and dependent
questions. Library exercises the same graph, SQL safety, tracing and UI core.

The exact tested executable is `58f2fe9b955eb25cb5a0ee2a9e1d967a60cdcc32`:
**815 tests, 157 independent SQLite oracle checks, static checks, AppTest,
eight actual offline browser states and tracked-only clean reproduction passed.**
Independent code review: APPROVE; architecture: CLEAR. H016 native COMPLETE / strict
PASS 4/4 closes the offline repair task, not final service acceptance. Clean
reproduction reused the locked installed environment; it was not a fresh download.

The shared resolver previously confused numeric ID markers and requested ID
columns with entity names. H016 fixes extraction, catalog validation, role ownership,
conflicts and quantified listings without changing the model or runtime prompts.
[H016 report](docs/reports/H-016-scope-repair-offline.md) ·
[root cause and decisions](docs/adr/ADR-OMX-015-H016-scope-resolution.md) ·
[browser evidence](docs/operations/H-016/browser/final-58f2-attempt3/browser-receipt.json).

**The latest live measurement remains 10/48 on the older `ecb7f5c` candidate.**
Thirty-eight conversations failed before the provider. The initial instrument's
2/48 output is preserved; a separately reviewed post-results correction changed
eight nullable-type labels, not answers, producing 10/48. This is an exposed-sample
end-to-end result, not pure model accuracy. It does not score the repaired candidate.
[H015 report](docs/reports/H-015-full-live-eval.md) ·
[corrected assessment](docs/operations/H-015/corrected-assessment-v2/score-v2.json).

This delivery includes completed H015/H016 results and historical evidence.
Publication does not authorize another live campaign or spending-policy change.
Earlier failed attempts remain explicitly labelled in the reports.
[Assignment coverage](docs/assignment-status.md).

## Defense presentation

[Editable English slide deck](docs/defense/UniversityDB-defense.pptx) ·
[Speaker notes and demo guidance](docs/defense/speaker-notes.md) ·
[Presentation overview](docs/defense/README.md).

The deck explains architecture, development decisions and evidence, including the
difference between offline verification and the pending new-candidate live check.

## Deliverables

| Item | Files |
| --- | --- |
| University schema and seed | [schema](resources/schema.sql), [seed](resources/seed.sql) |
| Library schema and seed | [schema](resources/library/schema.sql), [seed](resources/library/seed.sql) |
| Data model and initialization | [database guide](docs/database.md) |
| Graph and typed contracts | [agent](src/universitydb/agent.py), [contracts](src/universitydb/contracts.py) |
| Domain adapters | [University](src/universitydb/domain.py), [Library](src/universitydb/library.py) |
| SQL, provider, tracing and UI | [DB](src/universitydb/db.py), [SQL policy](src/universitydb/sql_policy.py), [provider](src/universitydb/llm.py), [trace](src/universitydb/tracing.py), [UI](src/universitydb/ui.py) |
| Prompts in two languages | [English](docs/ai/PROMPTS-EN.md), [Russian](docs/ai/PROMPTS-RU.md), [source coverage](docs/ai/README.md) |
| Automated and manual E2E | [tests](tests), [E2E guide](docs/manual-e2e.md) |
| Examples, outputs and traces | [examples](examples/README.md), [final M1 proofs](docs/operations/H-014/clean-run-final-attempt3/m1/manifest.json), [browser evidence](docs/operations/H-016/browser/final-58f2-attempt3/browser-receipt.json) |
| Architecture and rationale | [ADR index](docs/adr/README.md), [current contracts/decisions](docs/adr/ADR-OMX-012-I2-I3-offline-contracts.md) |
| Production considerations | [reliability, security, scaling and deployment](docs/plans/production-considerations.md) |

## Install

Use Python **3.12**, `uv`, and Bash on Linux/WSL (development environment: Ubuntu24.04).
No external SQL server, API key or OMX installation is needed for offline tests.

```bash
git clone https://github.com/vladberkov-ai/universitydb.git
cd universitydb
uv sync --locked
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q
```

Run from the checkout root; this is not a standalone-wheel deployment. `uv.lock`
pins dependencies. Runtime databases, traces, credentials and spending state are
local and excluded from Git. Schema/seed SQL is the reproducible database deliverable.

## Start the offline UI

These commands prepare the **full scripted E2E sequence** (not arbitrary model answers)
and isolate its databases and traces from any real spending ledger:

```bash
unset OPENAI_API_KEY
export UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false
offline_root="$(mktemp -d)"
cp -R resources "$offline_root/resources"
uv run --locked python docs/operations/H-013/offline_ui_fixture.py "$offline_root/injected.json" --full
export UNIVERSITYDB_ROOT="$offline_root"
export UNIVERSITYDB_TEST_MODE=1 UNIVERSITYDB_TEST_FIXTURE="$offline_root/injected.json"
uv run --locked streamlit run src/universitydb/ui.py \
  --server.address=127.0.0.1 --server.port=8501 --server.headless=true \
  --browser.gatherUsageStats=false
```

Open **http://localhost:8501**. The banner must identify **offline/injected** mode.
Follow the exact [E2E sequence](docs/manual-e2e.md): S6→80.00, Alex clarification→86.67,
M1→95.00, repaired S6→80.00, injected refusal, then Library→Ada1/Bob1.
SQLite and the graph compute actual results; scripted proposals do not measure
language understanding. Start a new browser session/restart the isolated server to
reset the scripted sequence. Stop with **Ctrl+C**; do not delete an existing real
spending ledger when cleaning up the owned temporary folder.

## Automated E2E and regression

```bash
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_i2_ui.py tests/test_i3_dependencies.py tests/test_library.py tests/test_h016_natural_scope.py tests/test_h016_resolution_edges.py tests/test_h016_offline_replay.py tests/test_h016_ui.py
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked mypy src/universitydb --ignore-missing-imports
uv run --locked python -m compileall -q src tests
```

Run the full `pytest -q` command from Install for the complete suite. The current
815-test baseline belongs to the exact H016 executable above. Graph tests exercise
the ordinary natural-question entry, compiled LangGraph and real temporary SQLite;
provider proposals are injected. UI tests use Streamlit AppTest. They do not measure
real-model language understanding.

For optional actual browser automation, provision Playwright and a compatible
Chromium separately, then run from the checkout:

```bash
browser_evidence="$(mktemp -d)"
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked python docs/operations/H-016/browser_ui.py "$browser_evidence" --full
```

The driver creates isolated fixtures, checks eight states across both schemas,
binds downloaded traces to current run IDs, and stops its owned server/browser.
It discovers a provisioned browser; it does not install one. This optional harness
is separate from pytest/AppTest. See the [E2E guide](docs/manual-e2e.md).

## Live mode: configuration reference, no new dispatch authority

The normal provider uses `gpt-6.1-sol`: planning high, SQL/repair medium, no fallback.
Unset `UNIVERSITYDB_TEST_MODE` and `UNIVERSITYDB_TEST_FIXTURE` before using it. Follow
the documented settings in [.env.example](.env.example); `.env` is not auto-loaded.
The local credential helpers under `tools/local-credentials/` store the key outside
Git. Never print keys or include them in traces/issues.

Live use requires explicit spending authority and applicable rate review; H015's
single-campaign owner authority is not permission for a reviewer's account or more
experiments. The original I1 policy remains a historical segment; the reviewed
H015 policy is aggregate$120/dispatch$110/contingency$10 including all history,
with one canonical `runtime/spending.json` independent of fixture roots. Migration
preserves history; it is not an environment-only cap override, account reset or
permission to release holds/spend contingency. See [ADR014](docs/adr/ADR-OMX-014-H015-full-live-eval.md)
and [actual accounting](docs/reports/H-015-full-live-eval.md#calls-usage-retained-obligations-and-limits).
Do not rerun the completed collection. The controller is conservative practical
accounting, not strict BILLING_VERIFIED or a provider-invoice guarantee.
Requests may use a plan plus up to three SQL steps, repair/retry sharing the maximum
five-call budget. Starting the UI does not establish model accuracy.

## Architecture and limits

UI → grounded scope/clarification → plan → static dependency validation → per-step
SQL generation/validation → read-only execution → typed result inspection → actual
dependency binding → deterministic answer. The domain adapters supply schema,
metrics and result semantics; the common core does not infer University semantics
from table names. Library demonstrates portability within SQLite, not all databases.

Session-bound LangGraph checkpoints survive UI reruns within the process, not server
restart. Maximum two clarification pauses/15minutes; up to three planned steps and
five provider attempts per run; plan60s, SQL/repair45s, active work180s. SQL safety
does not prove semantic correctness; independent oracles test that separately.
SQLite DELETE journal only, synthetic local data, no authentication/concurrent-writer
or production deployment claim. See [production considerations](docs/plans/production-considerations.md).

## Language and evidence

Current documentation/UI are English. The two prompt collections provide Russian
and English reader versions, with explicit source/translation/summary labels.
Original prompts, machine-readable receipts, traces and screenshots retain their
actual bytes/language; translating them would invalidate provenance. Historical
cutoffs are preserved and do not override current status. Full private transcripts, credentials and the original private assignment PDF are not published.
