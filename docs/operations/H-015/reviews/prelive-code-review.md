# H-015 independent prelive code review

## Initial review — source under preparation

Read-only independent code-reviewer lane; only this artifact is reviewer-owned.
Baseline `60e8ffc`, initial documentation checkpoint `333b0fe`; source initially
reviewed as an uncommitted working diff. No live/API/count calls, credentials,
canonical monetary writes, workflow/state/lock changes, Git mutations or Obsidian
writes were performed. The private task handoff was read in full as read context,
not as an actual received prompt or full transcript. Root owns separate architecture
review, custom gates, full offline execution and all activation decisions.

### Confirmed initial finding

**[HIGH] Durable campaign marker is read from EOF, permitting evaluator reruns.**
Location: `tools/eval/collector.py:379–384` (initial source).
`open("a+")` initially positions the file at EOF. Consequently `lock.read()` is
empty even when an earlier campaign ID is already present. A second CLI launch
with a different new output directory passes the existing-campaign guard, contrary
to the expressly single-campaign/no-evaluator-rerun contract. The shared ledger
still limits total spending/calls, but does not prevent duplicated conversations
or spending the remaining allowance on a second unauthorized campaign.
Fix: seek to offset zero under the exclusive lock before inspecting the marker;
retain the immutable marker, durably create its directory entry, and add a startup
regression proving that a second CLI invocation with a distinct output cannot
reach collection. Verify concurrent startup and crash persistence as well.
Reported to root before any live dispatch; root acknowledged and assigned author
follow-up. This section remains as initial history after correction.

### Initial status

**REQUEST CHANGES (provisional)**. Observer authoring and final source/test receipts
were still pending. Runtime tests deliberately not run while author lanes were
executing narrow tests. No approval inferred from implementation-lane assertions.

## Corrected-source follow-up — before full-suite receipt

The author repaired the primary contract directly: `lock.seek(0)` now precedes
marker inspection under the exclusive flock (`collector.py:389–393`); marker file
and parent-directory fsync precede collection (`:395–402`). Campaign/case directory
entries are fsynced before started/provider actions (`:234–264`). Regressions cover
second startup with a distinct output after normal completion and KeyboardInterrupt,
and directory durability ordering. No bypass, compatibility fallback or evaluator
retry was introduced. Initial HIGH finding is **resolved in inspected source**.

Confirmed corrected collector SHA256:
`257225495bcd22efaa697d7a8038820294c0f595bc1fa366e2d937cbd3038081`.
Collector tests SHA256:
`f98cf10c177e12ed3afdcb11d161fdbe8accad3929c718b35fcf2410be8bf086`.
Final observer SHA256:
`a47a50f935f493e24796ad353eff88de1a24509979699328f230aa35ecbb7f14`.

### Specification and root-cause guard

- Fixed typed H015 authorization uses aggregate120/dispatch110/reserve10, fixed
  exact model/tier/rates/envelope and global240 new attempts. Migration locks the
  same stable inode as reservations; validates exact baseline/count/obligations;
  backs up original bytes privately; preserves historical entries, stop and rate
  interpretation; appends authorization; atomically fsync/replaces; validates replay.
  Missing/corrupt/drifting authority fails closed. Reservations retain old obligations,
  and settlement uses max(reservation, observed), never credits reservation excess.
- Canonical source-checkout authority is independent of DB/UI fixture roots; provider
  rejects noncanonical H015 paths and missing migration. Unknown usage, rate/profile
  anomalies and accounting stops prevent subsequent dispatch. Only matching-profile,
  within-envelope known-usage semantic terminal failures may continue. Legacy policy
  is explicit, separately tested compatibility, not an automatic budget fallback.
- Collector CLI constructs normal provider/compiled graph and fresh DELETE-mode DBs;
  imports neither oracle nor scorer. Closed conversation exports send question and
  protocol selections only. Registration pins source/export/fixture identities and
  order. Started is durable before action; no resume/evaluator retry exists. Original
  trace/provider artifacts, graph state, DB before/after and terminal failures are
  retained. Rejected UNSAFE_SQL proposals are not mislabeled unsafe execution.
- Observer reads artifacts after collection, not the provider. It preserves strict
  typed values, NULL/zero/duplicates/ties and actual upstream dependency rows/binds.
  Choices normalize to oracle order only after strict typed-set validation. The
  prospective metric-specific average→mean alias and requested-column projection
  are representation mapping, not numerical repair or copying expected answers.
  Six checks require independently reviewed hash-bound annotations; absent proof
  remains false. Trace/call/DB/adapted-answer inconsistencies cannot become passes.
- No product prompts/domain semantics were changed or tuned to candidate questions.
  No new dependency, fallback model, count/probe, LLM judge, hidden SDK retry or
  silent error-to-success path was introduced. Sanitized collector exceptions stop
  rather than conceal failure or continue; unknown outcomes are not replayed.

### Independent modified-file diagnostics

Fresh reviewer commands, corrected source, all exit0:

- Ruff `check --no-cache` on all ten scoped Python files: **All checks passed**.
- Ruff `format --check --no-cache` on the same ten files: **10 already formatted**.
- Strict mypy on config/llm/llm_worker/ui with isolated `/tmp` cache:
  **Success: no issues found in 4 source files**.
- `git diff --check`: clean.

Reviewer did not launch concurrent tests. Root reported109 combined monetary/
collector/legacy tests passing before the marker fix; author reported22 corrected
collector tests passing and38 observer tests passing. These attributed results are
not substituted for the pending exact-candidate serialized full-suite receipt.

### Operational limits, not code approval claims

Source-relative authority assumes the approved checkout. Another clone must not be
used for paid execution; this scope does not establish account-global enforcement
against a different imported source tree. This boundary was escalated to root for
architecture/preflight, rather than silently deciding a new cross-checkout design.
Root must freeze and verify the canonical checkout/ledger/source identities, exact
candidate SHA, rate/account routing and observer/reviewer artifacts before live.
Independent annotation truth/privacy inspection and real-model quality remain
post-collection obligations. No prelive approval claims live48 completion, quality
acceptance, actual monetary migration, account access or owner acceptance.

## Actual received delegated task projection

The following is this reviewer's received child task, with only the private vault
prefix replaced by `[private-vault]`. It is not the owner's original prompt,
application runtime prompt, or a full transcript:

> Independent H015 prelive code review, read-only except your own review artifact docs/operations/H-015/reviews/prelive-code-review.md. Repo /home/dev/projects/universitydb, follow AGENTS. No recursive delegation. Root new H015 active, monetary/collector authors separate; baseline60e8ffc, initial docs333b0fe, source currently working diff. Read full [private-vault]/handoffs/H-015-full-live-eval.md, H015 brief/ADR014/design/authorizations, H014 protocol/budget; review source config.py,llm.py,llm_worker.py,ui.py, tools/eval/collector.py,tools/eval/observe.py, new tests/test_h015_{budget,collector,observer}.py and SDK-double-only2line existing test_sol_profile changes. Observer author still finishing tests/doc; root will signal final source and full test receipts shortly; begin monetary/collector audit now, don't final approve incomplete observer. Must validate security/accounting/history/rates/shared authority/atomic migration/drift/concurrency/cap+global240/unknown stops/known-error continue/full wire safe evidence/oracle isolation/48fixed source order+no reruns/started persistence/privacy and deterministic independent observation typed checks/no fabricated evidence. No product sample tuning, no fallback/count/probes/LLM judge. Critical rejected UNSAFE_SQL proposal is not actual unsafe execution. H015 budget C120/D110/reserve10 includes14entries5.970272, no hold release. Full measurement may quality-fail; partial cannot complete. Root runs full offline serial; do not start tests while implementers run narrow tests (read/static okay); later ask root if any targeted runtime reproduction needed. No live/API/credentials/monetary/workflow/runtime/locks/Obsidian/git mutation or paid calls. Inspect original ledger only if needed read-only, no private contents/paths in report. Report concrete severity findings file:line, spec compliance, tests gaps, recommendation APPROVE/REQUEST CHANGES/COMMENT; not architecture approval. Preserve initial findings and corrected followup as append history. Exact task projection with private vault prefix redacted; no full transcript claim.

## Final corrected-candidate review

### Code Review Summary

**Files Reviewed:** 10 Python source/test files (plus the specification, design,
authorization, protocol, freeze and validation references above).
**Total Issues:** 0 unresolved; 1 initial HIGH finding repaired and preserved above.

### By Severity — unresolved

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0

### Reviewed source scope

`src/universitydb/config.py`, `llm.py`, `llm_worker.py`, `ui.py`;
`tools/eval/collector.py`, `tools/eval/observe.py`;
`tests/test_h015_budget.py`, `tests/test_h015_collector.py`,
`tests/test_h015_observer.py`, `tests/test_sol_profile.py`.

Complete context of these files and their relevant product/trace/contracts/harness
interfaces was inspected. Stage1 specification compliance and Stage2 security,
accounting/correctness, maintainability and performance checks are addressed;
root-cause fallback guard is clear after the direct startup-marker correction.
No unresolved concrete defect was found in this bounded reviewed candidate.

### Exact evidence verified

- Tested/reviewed candidate: **`ecb7f5c81c705d970dc64adb910ed2a5020cb28b`**.
- Root's [offline verification receipt](../offline-verification.json) and all six
  referenced log SHA256s independently checked by this reviewer. Full suite log
  ends **576 passed in150.83s**, Ruff passed, format41 passed, strict mypy14 passed,
  independent oracle157 checks reported no historical writes. Root also records
  compileall/diff PASS and source45/preservation13/history688/vault23/package17
  invariants unchanged. Preservation counts are attributed root evidence; this
  reviewer did not reread private ledgers or reproduce the full preservation scan.
- Exact HEAD and all ten reviewed source/test hashes match the prospective freeze.
  Reviewer independently rehashed **all68 frozen files** and the freeze receipt
  identity `21a1eeb16fb6bff8cd1e807938adf8cfa4a272531e3ec5c79295df173c85eb67`;
  all match. No source drift observed after author correction.
- Reviewer-owned fresh Ruff/format10, strict mypy4 and diff diagnostics passed as
  recorded above. Runtime tests were serialized by root, not duplicated by reviewer.

### Recommendation

**APPROVE — code-review lane, bounded prelive technical candidate only.**

The initial HIGH is resolved, not waived. This does not independently supply the
architect lane's verdict or configured-gate synthesis. Root still owns supported
active-scope confirmation, exact approved-checkout/account routing and secure
credential gates, migration release, collection, independent original-artifact
annotations/scoring, final artifact reviews and workflow completion. No live48,
model/account access, usage, real migration, quality pass, owner acceptance or
publication is certified by this prelive code approval. A partial critical/budget
stop cannot become full measurement completion; quality failure must remain honest
in the fixed denominator and cannot authorize a paid rerun.

## Prelive metadata v2 addendum — APPROVE

Bounded root-requested follow-up: dependency-input registration hardening only;
no source, live, migration, credentials, state or Git changes by this reviewer.
Compared preserved `collector-registration-v1.json` / `prospective-freeze-v1.json`
with active metadata and `registration-amendment-v2.json`.

Independent stdlib validation confirmed:

- Preserved originals match the previously reviewed v1 hashes exactly.
- Active collector registration adds **only** the already externally frozen
  `uv.lock` and `pyproject.toml` hashes; every prior field/hash is unchanged.
- External freeze changes only the active registration hash and adds the explicit
  provenance amendment (prior identities/paths, date, reason, before-results flag).
  Initial strict comparison flagged that new amendment field; after inspecting its
  documented provenance, the permitted-delta comparison passed. This was a checker
  assumption, not a metadata defect or waived validation failure.
- All68 active external-freeze hashes and every collector file hash match actual
  files. Original48 questions/selections/order, fixtures, rubric, budget/policy,
  model, code/tests and candidate `ecb7f5c81c705d970dc64adb910ed2a5020cb28b`
  are unchanged. No further runtime tests were needed or run.

Active registration SHA256:
`413fb669246b10e9112af0cb20d1922b46dc5db9e2bdc858a695e7771ac004d9`.
Active external freeze SHA256:
`adba96e727cd97b452ed6f2b21f6b7b85c691913edb189e7318b1636e4aef61b`.

**APPROVE remains the code-review recommendation; zero unresolved findings.**
The576-test/static/157-oracle evidence remains source-valid. V1 receipts retain
historical v1 identities intentionally; this addendum identifies the active v2
metadata. Prelive technical approval still does not certify account access,
monetary migration, live quality, acceptance or lifecycle completion.
