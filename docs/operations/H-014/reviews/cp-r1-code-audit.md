# H-014 CP-R1 — independent code audit

## Scope, identity and actual delegated task

Role: independent code-reviewer; read-only product audit, not an implementation or
architecture verdict. Observed canonical HEAD: `6cc7ad3af426d0da6818281b035c5e683806f357`.
All 38 product/source/test/resource hashes in H-013's final manifest match both
working files and HEAD blobs. The historical fully tested product identity remains
`f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0`; this audit is not a new 410-test full run.

Actual delegated task received (verbatim; separate from inherited context):

> H-014 CP-R1 independent read-only audit of current candidate 6cc7ad3 (product f4b775c). Own docs/operations/H-014/reviews/cp-r1-code-audit.md only. You are not alone; preserve others' edits. Read full /mnt/d/Obsidian/UniversityDB/handoffs/H-014-v2-readiness-offline.md and relevant authority/requirements extracted assignment+provenance+ADR006 read-only. Audit actual src/tests/resources/pyproject/lock/runtime prompts against requirement→case→test→trace. Identify meaningful uncovered defects (not count-padding), all16filters/groups/count/null/ties, continuation, M1 empty/partial refs, Library isolation, safety/accounting and normal profile injection guards. Read H013 report and final evidence as comparison not current verdict. No live/count/credentials/ledger/IDs/pointers/locks/push changes; no product edits yet. Return actionable findings with file refs/severity, coverage gaps and explicit scoped verdict. Save actual delegated task + bounded result coverage in owned report (not full transcript). Do not recursively orchestrate. User explicitly authorizes independent reviewer lanes. Root handles clean-run/browser.

Coverage excludes hidden/private transcripts, root native lifecycle certification,
fresh clean-checkout/browser proof and future real-model quality. Only this report
was written; no product/test/history/ledger/native-state edits were made.

## Code Review Summary

**Files Reviewed:** 23 full product/config/resource files; test coverage and historical
proofs additionally inspected as described below.

**Total Issues:** 1 confirmed (same scope-loss root cause in both adapters).

### By Severity
- CRITICAL: 0
- HIGH: 1 (must fix before readiness approval)
- MEDIUM: 0
- LOW: 0

### Issues

**[HIGH] Unknown named target can silently become an unfiltered successful answer.**

Locations: `src/universitydb/domain.py:245-287`,
`src/universitydb/library.py:112-128`; shared explicit-form coverage is at
`src/universitydb/domain_support.py:87-100`.

The accepted contract requires unknown identities not to disappear into absent/all
filters (Q11, R04/R07). The University shorthand guard examines only the token
immediately following “average/mean”: in “What is the average grade for Zoe?” it
accepts `grade` as semantic vocabulary and never validates `Zoe`. Library's guard
recognizes “loans for Zoe” but not “loans does Zoe have”. The shared resolver only
rejects unknown targets attached to an explicit entity noun/name assignment.

Fresh isolated SQLite + actual compiled-graph reproduction, using a valid injected
global-mean plan/SQL proposal:

| Input/action | Actual baseline outcome |
| --- | --- |
| University resolver: `What is the average grade for Zoe?` | `{}` |
| University graph, same question | `status=ok`, global mean `83.33`, six grades/eight enrollments, all four scope filters `all` |
| University resolver: `What is the average grade for Bea?` | `{'student_id': 2}` |
| University resolver: `What is the average grade for student Zoe?` | `INVALID_INPUT` |
| Library resolver: `How many open loans does Zoe have?` | `{}` |
| Library resolver: `How many open loans for Zoe?` | `INVALID_INPUT` |
| Library resolver: `How many open loans does Ada have?` | `{'reader_id': 1}` |

Impact: substituting a nonexistent person in an otherwise accepted natural question
can produce a plausible answer about everyone. The SQL is safe and exactly
registered, so SQL safety cannot repair the dropped scope; the provider is required
to honor the already-empty authoritative scope. This is a deterministic input
contract defect, not an asserted live-model failure rate.

Specific fix: repair grounded resolution for the supported person-bearing
possessive/`for/of NAME`/`does NAME have` forms (or reject unresolved target-bearing
forms explicitly). Never replace an unresolved target with an absent filter; do not
add broad fallbacks or an LLM judge. Preserve known-name resolution, duplicate-name
clarification and explicit all/global queries. Add regressions pairing known and
unknown targets in **both** domains; unknowns must fail before provider/generated SQL,
with terminal trace and no stale answer. Re-run affected graph/UI/domain suites,
then the required clean full suite and independent re-review.

### Recommendation

**REQUEST CHANGES** for initial CP-R1 candidate. This is not the final H-014 verdict;
prior H-013 APPROVE/CLEAR are historical evidence, not substituted current approval.

## Requirement → case → test → trace assessment

The full runtime source (14 Python files + both runtime prompt files), all four SQL
resources, `pyproject.toml`, `.env.example` and README were read. Lock identity and
pinned dependency declarations were checked; no external dependency/security
advisory scan or package-registry verification was performed in this lane. Test
symbols and coverage mappings across the tracked suite were inspected, with detailed
contract/continuation/core/domain/oracle/dependency/review-repair/Library test review
and targeted execution. This is not a claim of exhaustive line-by-line review of
every historical test/document or a proof from test counts alone.

| Requirement/invariant | Grounded existing evidence | Remaining readiness obligation |
| --- | --- | --- |
| R01/R02/R11 schema, names, offerings, grades, retakes | Actual schema/seed; STRICT tables, FK/range/identity checks; `test_db_domain.py`, domain corruption tests | Root clean schema/seed initialization, repeat-init policy and row/hash receipts |
| R04 all 16 filter subsets, five group keys, three count objects | `test_i2_domains.py::test_all_16_filter_subsets_all_five_groups_and_counts`, `test_compiled_graph_all_16_filter_scopes_means_counts`, group/filter discriminating mutations; frozen independent oracle | No missing combinatorial class found; add meaningful named-target negatives above, not count padding |
| R04 NULL/zero/no rows, exact ties, all-semester scope | Exact components/typed registry; independent rational tie and rounding tests; nullable JOIN listings; explicit four-axis scope labels | Preserve semantics and real-model-not-run distinction |
| R04 M1 actual results | Typed static DAG vs materialization, exact metric/ref families; tests for F1/F2/tie/empty, duplicates, oversize/truncation/type/missing refs, no downstream dispatch, partial failure; final M1 JSONL manifest | Root fresh clean-environment M1 sensitivity/tie/resume proof, not relabeled H-013 captures |
| R05 Library | Independent adapter/schema/unit=1, LEFT JOIN zero, returned mutations, FK/types, cross-schema/session/resume isolation; final portability core hash | Root new clean University+Library runs and browser proof |
| R06 trace/UI | Ordered fsynced JSONL, all attempts/SQL/bindings/raw/adapted rows, fail-closed trace persistence, same-run replay/clarification request IDs; actual H-013 final browser receipt | New H-014 settled UI/screenshots/current question/run/trace evidence |
| R07 continuation | Real InMemorySaver/interrupt, server context + exact pending envelope, immutable request tombstones, inclusive TTL, bounded pauses/calls/SQL; final repair tests | New negative scope regression and clean checks; no restart-durability/auth claim |
| R07 safety/accounting | Independent AST + exact domain SQL + read-only URI/authorizer/watchdog; DELETE-only identity; SQL lock unavailable classification; durable shared synthetic-ledger holds/anomaly stops; no fallback/judge | No live/count/credentials/real monetary ledger mutation; future approval remains separate |
| R08/R09 quality/modularity | Core/adapter separation; fresh static checks and 108 targeted tests below | Full clean suite/static/oracle and independent final reviews required |
| R10/R12–14/U01/U04 | README/H-013 report/ADR012 explain implemented vs offline vs live/production limits; actual runtime prompts separate from translated RU/EN reader bundles | Root full current prompt/provenance/public-doc audit and readiness/eval package |
| R15/R16/R17/U02/U03/U05/U06 | Publication and owner defense remain distinct; deadline not invented; original H-013 evidence is comparison only | Root owns supported lifecycle/preservation/remote/checkpoints; no push/live/defense claim here |

Root-cause guard: no new fallback was introduced. Existing fail-closed worker,
accounting, typed result, trace and snapshot paths were inspected; the confirmed
scope-loss defect is the primary-contract repair needed rather than a broad retry
or compatibility workaround. Existing bounded SQL grammar is not universal NL/SQL
semantic correctness; wrong accepted metric selection remains a future model-eval
question, not something the read-only safety layer proves.

## Fresh validation and limitations

Environment: canonical checkout's existing `.venv`; disposable temporary DB/trace
folders. `OPENAI_API_KEY` removed; live approval `no`, both tracing flags `false`.
No live/count/credential-loading operation performed.

- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS, 32 files already formatted.
- `mypy src/universitydb --ignore-missing-imports`: PASS, 14 source files.
- `pytest -q tests/test_i2_contracts.py tests/test_i2_continuation.py tests/test_i3_dependencies.py tests/test_review_repairs.py tests/test_ui.py`: **108 passed in 15.96s**.
- Independent inline reproduction above: completed with fresh temporary University
  and Library DBs; it writes no test/source file. Temporary evidence was not retained
  as a public trace artifact; actual returned values are recorded above. Root should
  retain failing regression evidence before repair.
- 38 final H-013 product/source/test/resource hashes: match working files and HEAD
  blobs at this audit cutoff. No later docs SHA is represented as a new full test.
- Original private assignment PDF SHA256 independently matches provenance:
  `f60e6212307812a27430b2e28ad3bb027b752f50609f76d0bcb8578116ed7550`.
  Extracted assignment text and provenance were read in full; native PDF
  extraction/visual reading **not-run in this lane** because `pdftotext` and Python
  PDF readers are unavailable. No package installation attempted.
- Extracted assignment SHA256:
  `d71f3d2737059b857d4710a30acdbb4288c84b800e1f15fe85695e529b89f25c`.
- Assignment provenance SHA256:
  `6bae340063c847d372ea8c47879b8a1a360690af90d207141df49243ca5ce76d`.
- `uv.lock` SHA256:
  `de36cab6c73d37bde70cc13e019b9eb2552a0747e46fe5c8c3b7cedf5338378d`.
- Runtime plan/SQL prompt hashes match historical final manifest:
  `0b0260ee18016fc4716336d8e23230afb5484ffedab3ce79efd716bc4610af43` /
  `79fb9fb583d9e459d17a3cc0c57a2bb443df5e9dbdba2ab43d9ba18d6ac50adb`.

Clean install/full regression/oracle/browser, actual root native owner/goal
postconditions, preservation ledger checks, current remote observation, eval
protocol/budget and final independent re-review are root/other-lane obligations;
they are not certified by this bounded initial audit. No architecture verdict is
issued by this reviewer lane.
