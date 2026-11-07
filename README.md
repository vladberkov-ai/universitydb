# University Database + LangGraph QA Agent

A local question-answering service using LangGraph, generated SQLite queries,
typed results and an inspectable Streamlit interface. Two synthetic datasets are
included: University and Library. This repository contains the assignment code,
schemas, seed data, tests, decisions, prompt collections and execution evidence.

## Current status

**I2+I3 implementation is complete and verified offline.** University supports
means, enrollment/graded/distinct-student counts, JOIN listings, grouping, exact
top-course ties, optional student/course/teacher/semester filters, ambiguous-name
clarification, and dependent multi-step questions. Library uses the same core to
answer open-loan counts. The UI shows every step's SQL, bindings, raw/adapted rows,
errors, repair attempts and full JSONL trace.

Product commit `f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0` passed **410 tests,
157 independent oracle checks**, static checks, AppTest and six actual offline-browser
scenario classes. Independent reviews returned APPROVE/CLEAR; the development goal
closed COMPLETE with strict PASS (13/13). Later documentation commits do not change
that tested product identity. [Report and evidence](docs/reports/H-013-I2-I3-offline.md).

**Offline verification is not real-model NL→SQL accuracy.** The earlier I1 slice has
real Sol evidence for 80.00 and 90.00; the expanded service still needs broad real-model
evaluation and clean-environment readiness verification. Publication makes these
results available; it does not certify those remaining checks or production readiness.
[Requirement-by-requirement status](docs/assignment-status.md).

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
| Examples, outputs and traces | [examples](examples/README.md), [final M1 proofs](docs/operations/H-013/m1-final/manifest.json), [browser evidence](docs/operations/H-013/browser/cp-e-final-attempt2/browser-receipt.json) |
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
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_i2_ui.py tests/test_i3_dependencies.py tests/test_library.py
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked mypy src/universitydb --ignore-missing-imports
uv run --locked python -m compileall -q src tests
```

Run the full `pytest -q` command from Install for all410 current tests. Graph tests
use compiled LangGraph and real SQLite with injected proposals; UI tests use
Streamlit AppTest. Actual browser evidence is separate and linked above. The
historical Playwright capture harness has a machine-specific browser path; it is
not required for these portable test commands. Manual browser reproduction uses
the ordinary local UI and the sequence above. New browser automation portability
and clean-install verification belong to the next readiness block.

## Live mode: configuration reference, no new evaluation claim

The normal provider uses `gpt-6.1-sol`: planning high, SQL/repair medium, no fallback.
Unset `UNIVERSITYDB_TEST_MODE` and `UNIVERSITYDB_TEST_FIXTURE` before using it. Follow
the documented settings in [.env.example](.env.example); `.env` is not auto-loaded.
The local credential helpers under `tools/local-credentials/` store the key outside
Git. Never print keys or include them in traces/issues.

Live use requires your own explicit spending authority and applicable rate review;
historical owner approval is not permission for a reviewer's account or this expanded
evaluation. The shipped policy is the earlier I1 cap$10/admission$8/contingency$2,
with a pinned shared `runtime/spending.json`; it must not be reset or bypassed by a new
checkout. Current expanded live evaluation is **not authorized/run**. See the
[dated budget policy](docs/adr/ADR-OMX-010-I1-practical-budget-policy.md). The controller
is conservative local accounting, not a guarantee about the final provider invoice.
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
