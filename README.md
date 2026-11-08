# University Database + LangGraph QA Agent

A local question-answering service using LangGraph, generated SQLite queries,
typed results and an inspectable Streamlit interface. Two synthetic datasets are
included: University and Library. This repository contains the assignment code,
schemas, seed data, tests, decisions, prompt collections and execution evidence.

## Current H016 offline repair

H016 is a separate, authorized **offline product repair**, not a rescore or rerun
of H015. CP1 maps all38pre-provider failures to a shared identity grammar defect:
`entity ID N` is not extracted and `ID`/`IDs` projections are mistaken for unknown
names. Catalog wiring is correct. Independent natural-input regressions first
failed through the ordinary compiled graph before any product repair.

[H016 report](docs/reports/H-016-scope-repair-offline.md) records the committed,
exact tested candidate **`58f2fe9b955eb25cb5a0ee2a9e1d967a60cdcc32`**:
**815offline tests/157independent oracle checks**, static checks, clean tracked-
archive reproduction and actual8state University/Library browser all pass.
All1632immutable historical targets are unchanged; original locks/money retained.
Independent final code APPROVE/architecture CLEAR have0unresolved issues/blockers;
root actual native COMPLETE/strict PASS4/4 now closes bounded H016offline DoD
([terminal receipt](docs/operations/H-016/native-strict-closeout.json)). The repair preserves filters, catalog validation, ambiguity,
read-only SQL, NULL/zero/empty/ties and actual-result dependencies. Scripted plan/
SQL tests prove mechanics, not real-model NL→SQL accuracy.

**Latest measured live sample remains corrected10/48, product quality FAIL, on
historical `ecb7f5c81c705d970dc64adb910ed2a5020cb28b`.** H016 may establish an
offline-repaired candidate only; real-model validation and service acceptance
remain pending. No new API/count/probe, credential loading, monetary mutation or
push is authorized. Publication remains pending; last remote observation below is
historical, not a fresh poll.

The first H016 candidate `f9251a7` failed its full suite on two quantified
ID-projection inputs; it is rejected, not a final pass. The new candidate also
aligns bounded listing verbs with the accepted listing contract. Independent final APPROVE/CLEAR and actual native COMPLETE/strict PASS4/4 are received; [retained attempts](docs/reports/H-016-scope-repair-offline.md#cp3--verification-and-independent-review)
explain the repair without weakening original expectations.

## Historical H015 measurement and correction

**H015:48original conversations collected; separate corrected offline score10/48;
product quality FAIL.** Frozen/tested product
`ecb7f5c81c705d970dc64adb910ed2a5020cb28b` produced10ok/38scope-resolution
`INVALID_INPUT` failures before the provider, with20generation calls. No questions
were rewritten or replayed; all48remain in the denominator.

Original frozen observer/scorer output2/48 is preserved, with eight confirmed
nullable-mean type false negatives. The authorized post-results correction changes
only those8type labels, then uses the unchanged frozen scorer after independent
paired-output acceptance: categories4/8,0/8,0/8,6/8,0/8,0/8; mandatory failures38,
critical failures0, threshold=false. This is separate corrected analysis, not the
original prospective result, general accuracy or acceptance. It is an exposed-sample
end-to-end conversation pass count, not pure model accuracy:38questions never
reached the provider. Actual-data final
code review APPROVES and resolves the HIGH for this separate assessment only;
actual-data architect CLEAR covers full bounded H015 measurement plus separatev2.
Root verifies **native COMPLETE/strict PASS5/5** for bounded measurement
([terminal receipt](docs/operations/H-015/corrected-assessment-v2/native-strict-closeout.json)).
C1 local checkpoint `7b58686e7c89304642c7030cd9730f4f08a54f82`; service acceptance
is not claimed. Publication/quality/product diagnosis remain separate; push not-run.
Preparation APPROVE/CLEAR is not actual-data approval.

Original evidence/ledger/history/locks are preserved. No new provider/API/count/
probe, credentials, live UI, replay, product repair, monetary mutation or push is
authorized in the correction. Historical610-test/static and72focused preparation
checks remain distinct from current actual-data review.
[H015 report](docs/reports/H-015-full-live-eval.md) ·
[original collection](docs/operations/H-015/collection-closeout.json) ·
[independent observation](docs/operations/H-015/observation/independent-observation.md).

The exact ecb7candidate passed **576offline tests/157independent oracle checks**
and static checks before collection. Historical H014 product
`98345ad6ce5757c71d44ba1ce59a683d46e0d910` passed485tests, clean reproduction,
AppTest and six offline-browser classes/seven captures, COMPLETE/strict5/5.
These are separate cutoffs; offline/bounded safety passes do not prove broad live
query quality. Live M1/ties/count-choice/Library/repair success was not demonstrated
by this campaign. The exposed24-question×2sample is not an untouched holdout or
general model-accuracy estimate. Earlier I1 live80.00/90.00 remains historical.

The owner authorized this single no-smoke full eval and history-preserving aggregate
USD120/dispatch110/reserve10, including old obligations.20new retained reservations
USD8.528960 plus historicalUSD5.970272 totalUSD14.499232; new observed conservative
usageUSD0.2776070 is not the invoice or a reservation refund. No extra campaign,
count/probe/fallback/judge/paid rerun/UI run or push occurred. H015 changes are local;
the last preserved remote observation was origin/main60e8ffc at2026-11-08T07:01:48UTC
([receipt](docs/operations/H-015/remote-closeout.json)); no fresh remote check is claimed.
[Requirement status](docs/assignment-status.md).

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
| Examples, outputs and traces | [examples](examples/README.md), [final M1 proofs](docs/operations/H-014/clean-run-final-attempt3/m1/manifest.json), [browser evidence](docs/operations/H-014/browser/final-983-attempt1/browser-receipt.json) |
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
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false uv run --locked pytest -q tests/test_i2_ui.py tests/test_i3_dependencies.py tests/test_library.py tests/test_readiness_scope.py tests/test_readiness_ui_magic.py tests/test_eval_harness.py
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked mypy src/universitydb --ignore-missing-imports
uv run --locked python -m compileall -q src tests
```

The frozen ecb7candidate passed576tests with the full `pytest -q` command from Install;
later offline instrument work is a separate validation cutoff. Graph tests
use compiled LangGraph and real SQLite with injected proposals; UI tests use
Streamlit AppTest. Actual browser evidence is separate and linked above. The H-014 browser driver dynamically discovers Chromium and records its toolchain.
Browser automation needs a separately provisioned Playwright/Chromium environment;
it is not required for pytest/AppTest. Manual browser reproduction uses the ordinary
local UI sequence above. Clean reproduction already passed with disclosed dependency
cache/browser reuse; it is not an all-fresh-download claim.

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
