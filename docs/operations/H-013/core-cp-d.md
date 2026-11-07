# H-013 CP-D core dependent M1 receipt

Root authorization followed verified CP-C `b9f2eb66e20a3148485da2af62eaa4fc9d02d0cb`. Core lane owns application-bound core fixes and offline tests/evidence, never native/Git/workflow/monetary/vault lifecycle.

## Proof, not node counting
`tests/test_i3_dependencies.py` implements a dynamic **offline/injected** transport. Each SQL proposal is computed from the accepted actual step, resolved scope and materialized actual upstream refs in the provider payload. It does not select predetermined SQL by fixture label/index or supply hard-coded cohort IDs. The graph/SQLite/adapter/result validation are real; the transport is not real-model NL-to-SQL accuracy.

- F1 actual top `[2]`, actual cohort `[1]`, final student1 `95.00`.
- F2 fixture mutation actual top `[1]`, cohort `[1,2,3]`, final `95.00/80.00/50.00`.
- Exact tie actual top `[1,2]`, deduplicated cohort `[1,2,3]`, final `90.00/90.00/null` with explicit `no_grades`.
- Every case checks actual provider refs, checked parameter values/placeholder SQL, raw/adapted dependency rows, independent frozen expected answer, unchanged database hash and exact request replay with0 extra calls.
- Empty/no-grades top short-circuits both downstream steps with0 downstream provider/SQL calls and explicit empty/no_rows. A separately labeled valid-shape empty-cohort injection proves the final filter never silently disappears; it is not presented as a naturally possible top-course fixture.
- Injected missing/type/spec/truncated/oversized/row_count corruption after a validated top step fails at bind_results before any downstream calls. Partial terminal refusal retains the successful prior step/trace but publishes no complete answer.
- One shared recoverable execution failure completes M1 within5 provider calls/4 SQL attempts; adding a prior transient exhausts the same remaining call budget before final dispatch, preserving prior successful steps but no fabricated answer.

## Core fixes
The active deadline is rechecked immediately before provider dispatch, after payload/wire/trace preparation; direct regression consumes the remainder during preparation and proves0 provider calls. Malformed untrusted run IDs are normalized into a valid error envelope, never unhashable lookup/unhandled exception; paused request replay after TTL returns RESUME_EXPIRED. No bounds raised, accounting weakened, or existing assertion changed. Domain-specific static M1 ref-family validation remains the separate adapter lane's responsibility.

## Fresh serialized validation
Root granted this lane the first serialized CP-D targeted slot, with all other heavy checks held. `UV_CACHE_DIR=/tmp/h013-uv-cache uv run --locked pytest -q tests/test_i3_dependencies.py tests/test_i2_contracts.py tests/test_i2_continuation.py` → **59 passed in24.05s**. Owned six-core-file strict mypy, Ruff and diff check pass. No live/count/credential/real-ledger/push access.

Actual F1/F2/tie proof documents and full matching JSONLs from that same59-pass process are persisted under [m1/](m1/README.md) with source/fixture/trace hashes, not left only in disposable pytest directories. Adapter owner confirmed no source edits during that run. `m1/capture.py` provides capture-only reproducibility; after later adapter changes root must regenerate evidence on the final frozen candidate rather than relabel old hashes. Earlier source-specific evidence stays historical in its checkpoint commit. Final full regression and tested SHA remain root-owned; CP-D is not whole-goal completion.

## Final retained-payload boundary correction
Root clarified the existing128KiB cap before dependent code in the current contract/ADR012. Core now bounds one UTF-8 JSON bundle containing the current raw result, proposed completed dependency results, step_results(raw+adapted) and current normalized answer before accepting retention or downstream work. This counts duplicate retained payload copies; scope/counters/transient work and LangGraph framework/history overhead are not a hard process-memory promise. No cap raised or raw/adapted metadata dropped to fit.

The first boundary test used impossible100-digit SQLite integers: the resource rejection occurred correctly, but checkpoint serialization of the invalid fixture obscured it. That failed fixture was replaced with valid SQLite strings (Library100rows with500-character names): individual raw result remains below64KiB while combined retained copies exceed128KiB. The real graph rejects RESOURCE_LIMIT at inspect_result with2provider calls/1SQL execution and no second step. The original desired failure-code/no-downstream assertions were not weakened. Narrow boundary+pre-dispatch deadline regressions →2passed1.75s, strict agent mypy/Ruff/format/diff →pass. Source frozen again; UI receives the next serialized slot.

Capture-only helper now accepts `--output-dir` only for a new, nonexistent directory and refuses to overwrite the existing manifest. First M1 evidence stays unchanged; root's final frozen candidate will be captured separately (`m1-final/` or another new directory), with exact observed verification text and source hashes. No later source hashes are retroactively attached to earlier actual traces.

## Strict integer wire boundary
Root treated the impossible-integer discovery as a concrete untrusted provider-wire gap, rather than relying on generic OverflowError masking. Following the current contract/ADR012 note before code, `Binding.integer_value` is now signed SQLite64 and `ResultSpec.scale` is positive up to signed64 (then exact registry1/100 acceptance). Shared raw/reference/Answer integer validation also enforces signed64 with bool excluded. Actual scripted provider graph regressions send100-digit plan scale and SQL binding: both return PROVIDER_INVALID_OUTPUT with0 SQL attempts and a terminal trace, before invalid values enter the saver. Exact min/max bindings pass; out-of-range raw integers fail their result contract.

Fresh serialized narrow integer-wire+contract+retained-bundle+pre-dispatch regressions →23passed2.33s; strict contracts/agent mypy passed. Source frozen and slot released to UI. Earlier first M1 proof remains source-specific; final candidate evidence must use the new capture output directory and actual source hashes after all lane changes/cleaner.

## Final public-input pre-saver guard
Root authorized a final narrow guard: non-string `run(question)` inputs are rejected with typed INVALID_INPUT before fingerprinting, context creation, saver or DB startup. Six direct regressions cover huge integer, nested list/dict, numeric/None/bool; no broad OverflowError catch. Normal string length checking/trace behavior remains in the graph input node. Fresh contract suite →25passed (see command result in root handoff); strict core mypy/diff passed. Product source immediately frozen for root's serialized full candidate.

Independent-review item retained openly: exact initial request replay after paused TTL returns typed RESUME_EXPIRED/no calls, but unlike normal `resume()` expiry it does not append a terminal owning-run trace. Root left that narrow replay visibility detail for independent review rather than silently changing behavior during the frozen candidate. Normal expiry/data/actual-policy resume errors are traced terminal; foreign requests do not disclose or modify another trace.
