# H015 monetary/provider implementation (offline CP-L1)

## Actual delegated task projection

Root assigned this independent implementation lane only `config.py`, `llm.py`,
`llm_worker.py`, `ui.py`, `tests/test_h015_budget.py` and this record. The lane read
H015 handoff, repository brief/prospective migration design, current provider and
budget tests before editing. It performed no lifecycle mutation, live/API/count
request, credential loading, canonical ledger migration, commit or publication.
Root owns integration, independent review, prospective freeze and any real dispatch.

## Fixed versioned authority

`H015Authorization` is a typed fixed version-2 policy, `h015-practical-v1`,
CHAT053/054/ADR-CHAT007, aggregate120/dispatch110/contingency10, exact Sol/default,
input5.50/output11 USD per million. No environment value can change these values.
Rates must be independently reconfirmed by root before live; these code constants
are not evidence that any account or price was verified. Legacy practical-v1
behavior and constants remain unchanged.

`universitydb.llm.H015_POLICY_SHA256` hashes the policy using UTF-8 JSON with
`sort_keys=True,separators=(",", ":")` (ASCII encoding default; policy is ASCII).
`load_h015(path)` returns a validated `H015Spending`; `snapshot()` reads the complete
private record under the stable ledger lock without rewriting it. `inspect()`
returns safe policy hash, stop, uncertain attempt IDs, total/campaign calls and
reserved/observed/effective totals. These read APIs never initialize a new balance.

`migrate_h015(path, expected_sha256, backup_path, *, expected_calls=14,
expected_effective_usd="5.970272")` requires an existing practical-v1 ledger,
exact original byte hash/count/effective total and valid historical accounting.
It preserves original profile/attempts/stop and all totals, appends two authorization
segments and changes only the top-level active policy. Historical authorization
retains exact original UTF-8 JSON privately, its hash, original policy/profile/stop,
entry hash and count. Every dispatch revalidates that source, original entries,
original rates, current fixed policy and recomputed cross-segment totals. The
registration must pin the original source hash externally; an unsigned local JSON
file alone cannot defend against a coherent malicious rewrite of all its hashes.

The private backup is created exclusively mode0600, fsynced (including directory),
then the ledger is atomically fsync/replaced under the existing stable `.lock` inode.
Replay validates the same source hash/count/total and private original backup;
there is no second credit. Stale/missing/corrupt/drifted input rejects. Failed
replace leaves old authority intact; a verified backup supports retry. An interrupted
partial backup fails closed for explicit reconciliation, never silent overwrite.

All obligations use `max(reservation,observed)`; historical rates apply only to
historical entries. Uncertain holds and historical stops cannot be released.
Reservations are exactly12000input/32768output and admission permits equality with
110 but not overflow. Shared locked policy admits at most240 new attempts,
independent of processes/UI/fixture databases. The cap is aggregate120, not120extra;
contingency is never automatically dispatched.

## Shared authority and evidence

`canonical_budget_path()` anchors to the source checkout's `runtime/spending.json`,
not `UNIVERSITYDB_ROOT`; it fails closed if the checkout markers are unavailable.
UI always uses that path. H015 `OpenAIProvider` additionally rejects a different
explicit budget path; standalone/collector cannot obtain a new fixture balance.
Synthetic tests patch this helper to their own temporary path and never touch the
canonical ledger. `load_h015` requires explicit migration and never auto-upgrades.

`OpenAIProvider(prompts,budget_path,*,evidence_dir=None)` retains ordinary provider
behavior. Optional evidence uses exclusive mode0600 per-reservation files with
fsync, complete assembled wire JSON and worker response envelope containing the
actual SDK `response.model_dump(mode="json")` body. No headers, environment,
credential fields or transport exception values are serialized. Actual response
model/tier/token counts are validated and usage settled before semantic output
acceptance. SDK retries remain zero. Exact request/response byte hashes and paths,
plus attempt ID, appear in ordinary provider trace metadata (error payload directly;
success payload under `usage`). Timeout may have only a request artifact and keeps
its unknown reservation plus durable stop; no response is fabricated.

Only H015 known-usage, matching-profile, within-envelope refusal/incomplete/invalid
output is an ordinary accounted terminal failure (`accounting_stop=false`), allowing
the untouched next case. Unknown usage, profile/tier mismatch, accounting anomaly
or evidence-integrity error stops. Legacy practical-v1 keeps its former fail-closed
terminal-error behavior. Product prompts/domain semantics/ceilings are unchanged.

## Validation before root integration

Regression-first collection failed as expected on missing migration APIs before
implementation. Synthetic focused suite then passed84 tests across H015 migration,
legacy practical budget, provider worker and Sol profile. H015 tests cover private
backup/history/replay, stale/missing/corrupt source, crash-before-replace, pending
hold preservation, cross-segment rates, exact threshold equality/overflow,
fixed envelope, global240, independent-process and thread migration/reservation,
policy drift and known-terminal versus unknown/model/tier failures/evidence hashes.
Ruff checks/format and source mypy are separate recorded verification gates; root
runs full integration and independent reviews before any live authority use.

## Bounded ai-slop-cleaner plan (before edits)

Behavior lock: focused84 tests pass before this pass. Scope remains assigned files;
only SDK test doubles may be aligned with the actual SDK serialization interface.
Fallback inventory: legacy practical-v1 branch is grounded compatibility with
regressions; unknown-spend handling is intentional fail-safe, never a release.
The new `hasattr(model_dump)` empty-evidence branch is masking fallback slop:
the pinned real SDK always supplies the method, so remove it rather than conceal
an unsupported response interface. Duplicate atomic-save code should reuse the
existing new atomic helper with the original temp prefix. Dead code/UI slop none.
Plan order: remove masking fallback, retain legacy test-double interface explicitly,
reuse atomic writer, reinforce strict JSON-type policy drift tests, rerun focused
checks. Independent reviewer/architect approval remains root-owned and separate.

### Cleaner completion and fresh checks

Resolution gate/Pass1: no dead code; removed masking SDK serialization fallback.
Pass2: reused one fsync/atomic-replace helper for legacy and H015 writes, preserving
original temporary-file prefix and stable lock behavior. Pass3: fixed policy and
historical-profile comparisons use canonical JSON hashes (not Python's permissive
bool/int/float equality); call-count totals are likewise strictly typed. Pass4:
added numerical-type drift and noncanonical-provider-path rejection regressions.
The only legacy test edits give two SDK test doubles an explicit `model_dump`
interface; all pre-existing behavioral assertions remain unchanged. UI/design N/A.
No dependencies, abstractions or unrelated refactor were introduced. Fallback
classification/escalation complete; no masked fallbacks left in new evidence code.

Fresh command evidence: focused provider/budget/Sol suite89passed before the final
canonical-path regression; source mypy passed all4files; Ruff lint/format and
`git diff --check` passed. Final focused count and full integration are separately
reported to root; independent code-reviewer/architect have not approved this writer
pass by virtue of these checks. Remaining risks: actual rates/account/live evidence
and external registration source-hash pin are root-owned gates, not proven here.

Final CP-L1 focused verification: `pytest -q tests/test_h015_budget.py
tests/test_practical_budget.py tests/test_provider_worker.py tests/test_sol_profile.py`
→90passed; `mypy src/universitydb/{config,llm,llm_worker,ui}.py` →success4files.
