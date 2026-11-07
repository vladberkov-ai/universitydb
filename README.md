# University Database + LangGraph QA Agent

**Current release: working I1 demonstrator; the full assignment is not finished.**
Real Sol + LangGraph + SQLite + Streamlit passed S6 **80.00**, an independent changed
example **90.00**, full trace inspection and error/no-stale-answer checks. The owner
also passed all four manual live checks. The recorded full suite has **131 tests**.
[Live evidence](docs/reports/H-009-live-I1-closeout.md) ·
[owner acceptance](docs/reports/I1-owner-manual-acceptance.md) ·
[completion receipt](docs/operations/H-009/closeout/postcheckpoint-goal-receipt.json).

Today the supported question is **a scalar grade mean with four explicit filters**:
student, course, teacher and semester. Arbitrary natural-language questions, multiple
dependent steps, conversational clarification/resume and a second database adapter
are not implemented. See the [assignment audit](docs/assignment-status.md) for the
complete distinction between delivered artifacts and missing functionality.

## Reviewer navigation

| Deliverable | Location |
| --- | --- |
| SQL schema and synthetic seed | [schema.sql](resources/schema.sql), [seed.sql](resources/seed.sql), [database guide](docs/database.md) |
| LangGraph agent and domain adapter | [agent.py](src/universitydb/agent.py), [domain.py](src/universitydb/domain.py) |
| DB, model and tracing layers | [db.py](src/universitydb/db.py), [llm.py](src/universitydb/llm.py), [tracing.py](src/universitydb/tracing.py) |
| Runtime and development prompts | [English prompts](docs/ai/PROMPTS-EN.md), [Russian prompts](docs/ai/PROMPTS-RU.md), [provenance/coverage](docs/ai/README.md) |
| Tests | [tests](tests), [manual E2E](docs/manual-e2e.md) |
| Design decisions | [ADR index](docs/adr/README.md); implemented scope: [ADR008](docs/adr/ADR-OMX-008-I1-scoped-implementation.md), [ADR009](docs/adr/ADR-OMX-009-Sol-operation-profile.md), [ADR010](docs/adr/ADR-OMX-010-I1-practical-budget-policy.md) |
| Queries, outputs and execution traces | [examples](examples/README.md) |
| Production discussion | [production considerations](docs/plans/production-considerations.md) (future work, not production readiness) |

Earlier design documents/ADR003–007 are proposals. Their old model/budget/eval settings
do not override the implemented I1 profile. Historical OMX goal/resume instructions
are development records, **not prerequisites for running the application**.

## Install

Tested environment: Ubuntu 24.04 / WSL2, Python **3.12**, `uv`. Windows users can run
these Bash commands in UbuntuD. Install Python3.12 and uv before continuing.

```bash
git clone https://github.com/vladberkov-ai/universitydb.git
cd universitydb
uv sync --locked
uv run --locked pytest -q
```

Run commands from the repository root: schema/seed and prompts are repository resources;
installation as a standalone wheel outside the checkout is not a supported deployment.
`uv.lock` pins dependencies. No external SQL server is required. The first submitted UI
question creates `runtime/university.db` from the schema and seed if absent; it never
overwrites an existing DB. Runtime DB/traces, dependencies and credentials are not committed.

## Start without an API key (offline E2E)

```bash
export UNIVERSITYDB_TEST_MODE=1
export UNIVERSITYDB_TEST_FIXTURE="$PWD/examples/offline-s6.json"
export UNIVERSITYDB_ROOT="$PWD"
uv run --locked streamlit run src/universitydb/ui.py \
  --server.address=127.0.0.1 --server.port=8501 --server.headless=true \
  --browser.gatherUsageStats=false
```

Open **http://localhost:8501** and keep the default question. Expect **80.00**.
The banner must say `offline/injected`: the graph, SQL validator, SQLite, formatter
and UI are real, but model responses are fixed. This is **not live NL-to-SQL accuracy**;
the fixed fixture is for S6 only. Do not expect changing the student to test the model.
Stop the foreground server with **Ctrl+C**. No goal, OMX installation or API key is needed.

## Start with real Sol (paid, optional)

Use an API project with access to `gpt-6.1-sol`. Configure your own local key securely:

```bash
bash tools/local-credentials/setup-universitydb-key.sh
set +x
source "$HOME/.universitydb-secrets/credentials.env"
unset UNIVERSITYDB_TEST_MODE UNIVERSITYDB_TEST_FIXTURE UNIVERSITYDB_BILLING_VERIFIED
set -a
source .env.example
set +a
# .env.example clears the key; reload the private value, without printing it.
source "$HOME/.universitydb-secrets/credentials.env"
export UNIVERSITYDB_ROOT="$PWD"
```

An existing credential file is preserved; use `replace-universitydb-key.sh` only for
intentional rotation. Never commit or print your key. `.env` is **not** auto-loaded.

Before enabling requests, explicitly accept the practical spending policy and review
applicable current API rates. The shipped rate values **5.50/M input and11/M output**
are a conservative dated envelope, documented [on 2026-11-07](docs/operations/H-009/api-references.md),
not a permanent provider tariff. If the applicable rates differ, configure them before
first use; an existing ledger's monetary profile is pinned and must not be reset to change it.
Only after that review and your own spending authorization:

```bash
export UNIVERSITYDB_RATES_CONFIRMED=yes
export UNIVERSITYDB_LIVE_APPROVED=yes
uv run --locked streamlit run src/universitydb/ui.py \
  --server.address=127.0.0.1 --server.port=8501 --server.headless=true \
  --browser.gatherUsageStats=false
```

Check the banner is `live`. Each submitted supported question normally makes two
generation calls (plan high, SQL medium); repair also uses medium. No silent fallback.
Missing configuration fails with `PROVIDER_UNAVAILABLE`, not a canned success.

The I1 profile is fixed: total cap **$10**, admission threshold **$8**, **$2 contingency**.
All requests/retries/restarts share `runtime/spending.json`; successful reservations
are conservatively retained. Do not delete it or create a fresh checkout to evade a
budget stop. The counter is not a provider invoice and **does not guarantee a hard
financial ceiling**. The old `BILLING_VERIFIED` proof flag is not used. The repository's
historical owner approval does not authorize spending on a reviewer's account.
The original owner's remaining allowance must be read from the existing ledger, not
inferred from historical receipts. No live request is needed to inspect shipped evidence.

## Check through E2E

Full copy/paste questions and expectations are in [manual-e2e.md](docs/manual-e2e.md).

| Check | Expected | Mode |
| --- | --- | --- |
| Default Bea/student2, DB/course1, Kim/teacher10, S1 | **80.00**, raw16000/2/2 | offline or live |
| Alex/student1, same course/teacher/semester | **90.00**, raw 9000/1/1 | live only |
| Expand SQL, typed rows, trace; download JSONL | Four bound filters, consistent rows and one run_id | both |
| Submit `unsupported` after success | `INVALID_INPUT`; previous answer disappears | both; this failure makes0LLM calls |

Offline automated checks (no credentials, no real provider calls):

```bash
uv run --locked pytest -q
uv run --locked pytest -q tests/test_db_domain.py tests/test_graph.py tests/test_ui.py
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked mypy src/universitydb --ignore-missing-imports
uv run --locked python -m compileall -q src tests
```

`test_ui.py` uses Streamlit AppTest, not a real browser. Graph tests run actual LangGraph
and SQLite with injected provider responses. Real-model/browser evidence is separately
linked under examples; do not count mocked tests as live model evaluation.

## Architecture and limits

UI → validate input/load schema/resolve scope → plan → validate plan → generate SQL →
validate SQL → execute read-only SQLite → inspect result → deterministic answer.
Failure routes terminate with a structured error; one bounded SQL repair is possible.
Every stage/attempt is written to JSONL before success is shown. Debug a wrong answer
by comparing scope, SQL bindings, DB rows, result specification and final arithmetic
in that same run, rather than looking only at the final text.

The core graph avoids University table names; domain-specific schema, scope and result
rules live in `domain.py`. A second-schema adaptation has **not** been demonstrated.
SQLGlot checks one tightly restricted SELECT; SQLite authorizer/read-only mode and worker
timeouts add protection. This is a synthetic loopback demo, not a general SQL sandbox.
Output: 32768 tokens, ≤5attempts/run, plan 60s / SQL-repair 45s / run 180s; synchronous local I/O
assumes a responsive filesystem, so 180s is not a universal hard deadline. These limits
have been measured for I1 cases, not all workloads. No authentication, remote deployment,
hard memory isolation, multi-step orchestration or durable conversational resume is claimed.

## Documentation language and provenance

Reviewer documentation and UI are in English. Prompt texts are collected separately in English and Russian. Original prompt files, machine-readable execution/provenance records and screenshots retain the language actually used; they are evidence, not translated replay results. Historical document hashes refer to the original pre-translation versions in Git. See the [translation record](docs/operations/english-translation-manifest.json). Translated chat snapshots are a presentation layer; they do not change the private authoritative wiki or create an automatic two-way sync.

Reviewer documentation and UI are in English. Prompt texts are collected separately in English and Russian. Original prompt files, machine-readable execution/provenance records and screenshots retain the language actually used; they are evidence, not translated replay results. Historical document hashes refer to the original pre-translation versions in Git. See the [translation record](docs/operations/english-translation-manifest.json). Translated chat snapshots are a presentation layer; they do not change the private authoritative wiki or create an automatic two-way sync.
