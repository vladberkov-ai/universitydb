# H-004 v2 - preparation report

Date: 2026-11-07, Asia/Jerusalem. Owner: repo. Mode: **solo/direct**, `understand → execute → verify → report` according to local OMX instructions. Result: **preparatory documents saved; The Git part is blocked; the stage has not been declared fully completed**.

## 1. Border and entrances

Only the actual H-004 v2, SHA-256 `69d0fc4b467f4272504d9e6366ee25c5e53607bef30e92975a8fde320ea9335b` (observed hash) was read; no independent expected hash of the packet itself was sent. All **25/25** SHA-256 from the table matched. Full list of paths/sizes/expected/actual - [input-verification.json](../operations/input-verification.json). All listed text inputs are read in full. Source PDF read in its entirety: **4 pages**, all text glyph IDs resolved via built-in ToUnicode CMaps. `pdfinfo`/`pdftotext` and Python PDF libraries are missing; Direct reading of objects/Flate streams of the original PDF was used without installing dependencies and without exporting its text. The R/U matrix is ​​verified with the original.

H-004 v1 has not been opened or used; old H-001/H-003 were not executed. Historical references in indexes are not accepted as valid orders. Additionally, the latest log events, local/installed AGENTS, instructions from the previous candidate and the installed wiki skill were read. Inputs/Obsidian/manifest/old materials were not changed. The full chat history and hiring context were not loaded.

Application architecture, diagram/seed, graph, code, UI, runtime prompts, product tests and dependencies were not created; application/live or paid eval did not launch. Workers, Team and native subagents did not start.

## 2. Placement and canonical evidence

Selected **canonical target/working folder**: `/home/dev/projects/universitydb`, `pwd` and `realpath` matched. `WSL_DISTRO_NAME=UbuntuD`; `/etc/os-release`: Ubuntu 24.04.1 LTS. There is no corresponding path to D: for Linux repo. **The initialized canonical Git repo has not yet been proven or created.**

Initially in the working folder: runtime `.omx/` and empty protected `.git`, `.agents`, `.codex`, `.aws`; there was no project AGENTS/docs/application. `.git`: `dr-xr-xr-x`, separate `tmpfs`, mount option `ro`, mode `555`. `git rev-parse --show-toplevel`, `git status --short --branch`, `git worktree list --porcelain`, `git remote -v` returned **fatal: not a git repository**. Original branch/HEAD/status: unavailable, not a “pure repo”.

Checked the preferred Linux path, project names in `/home/dev/projects` and at a depth of 3 in the directory of previous candidates, metadata of the old Genpact, as well as project-related OMX pointers. Genpact contains AGENTS and private bootstrap/tmp/backup materials; `.git`/`.gitmodules` not found, Git root missing. Nothing has been transferred from there. The identified candidate with the name Codevalue has been verified **only by Git metadata/names**: unborn `main`, no commits/remotes, three untracked private interview materials; their contents were not read. This is not a proven copy of UniversityDB; materials are not touched. Other Git directories found with unrelated names; their contents were not read.

OMX session metadata points to the current working folder. This is diagnostic evidence of placement, **not authority** to change runtime or protected mount points. No competing repo copy related to UniversityDB was identified in the checked paths; the global absence of copies on all disks is not declared. Therefore, independent documents are prepared here, but Git dependent activities are stopped. The second repo, separate git-dir, transfer of other people's files, sandbox bypass, chmod/unmount were not performed.

## 3. OMX / Wednesday

- Actual launcher: repo-local `.omx/runtime/bin/omx` (not the previous intended launcher). Version **0.21.46**, Node **22.23.2**, Linux x64; updates/setup were not performed.
- `omx doctor`: **17 passed, 0 warnings, 3 failed**. Failures: launching Codex CLI from diagnostics - EPERM; native-hook smoke - EPERM/ETIMEDOUT in two observations; state/session binding - stale-dead and bad selector `CODEX_SESSION_ID`. This is not a completely healthy environment; don't hide behind the success of team doctor.
- `omx doctor --team`: all team checks passed; workers were not launched, this is not a test of the application.
- `omx status`: listed runtime modes inactive. `omx session lock inspect --cwd ... --json`: lock absent, `safeToRecover=false`; recovery was not performed. Foreign/unconfirmed session selectors/state were not changed.
- Despite the diagnostic failures, the usual `omx --version`, help, status and precise session export actually worked. Therefore, the use of OMX is not simulated; unavailable capabilities are not used.
- Git identity was discovered via `git var GIT_AUTHOR_IDENT` without publishing its value; global config has not changed. Commit does not block identity, but read-only `.git`.

## 4. Saved artifacts and diff summary

New local files, not Git diff of existing repo:

- `AGENTS.md`, `.gitignore`: boundaries, ownership, protection of private/runtime/secrets/venv/caches/binary databases.
- **Exactly four** safe projections: [requirements](../chat/requirements.md), [acceptance-contract](../chat/planning/acceptance-contract.md), [ADR-CHAT-001](../chat/decisions/ADR-CHAT-001-memory-ownership.md), [ADR-CHAT-002](../chat/decisions/ADR-CHAT-002-result-scope.md).
- [chat-export-receipt.json](../operations/chat-export-receipt.json): vault-relative source paths, hashes of actual source/destination bytes, redactions, links. Vault manifest is not updated. ADR-CHAT-003/PDF/raw/brief/nested dependencies not exported.
- [Prompt index](../ai/README.md), actual prompt, selected OMX export, prompt receipt i relativeinstruction context V`docs/ai/omx/`.
- [Single index ADR](../adr/README.md), [ADR-OMX-001](../adr/ADR-OMX-001-preparation-boundary.md): preparatory selection only, alternatives/causes/consequences/checks, no application architecture.
- [Git checkpoints](../operations/git-checkpoints.md): current conditional docs commit resolved H-004 v2; future policy **proposed**, not automatically accepted.
- [omx_wiki/index.md](../../omx_wiki/index.md), OMX’s own session memory and the lint log created by `omx wiki`; links to repo-owned documents, not a copy of Obsidian.
- This report, [input evidence](../operations/input-verification.json), [validation manifest](../operations/preparation-validation.json) and [command evidence](../operations/environment-checks.json).

The private auxiliary build/validation script and the original session export remain ignored by `.omx/preparation/` and are not included in the public structure. `.git` and other protected directories are not changed. The exact composition and final hashes of public-safe files are recorded by the validation manifest; manifest itself is excluded from its own hash set to avoid self-referencing.

## 5. Commands and checks

Actually done: reading via `cat`/Python, SHA-256 via `hashlib`, bounded `find` names/metadata only, `pwd`/`realpath`/`stat`/`findmnt`, Git metadata probes, `omx --version`, `omx --help`, `omx session --help`, `omx session export --help`, `omx doctor`, `omx doctor --team`, `omx status`, `omx session lock inspect`, real JSON session export. Details of repeated Git/diff/no-index checks and exit codes are in the command evidence/validation manifest; the results should be read in conjunction with the limitations below.

| Check | Result |
|---|---|
| Package and all required inputs | Read; 25/25 hashes match; PDF p1–4 |
| Original Wiki structural lint | `PYTHONDONTWRITEBYTECODE=1 python3 <private-vault>/scripts/lint_wiki.py`: **0 errors**, no vault entry |
| Sources after preparation | Re-checked for all 25 hashes; manifest/sources not changed |
| Four source/destination hashes | Re-checked against saved bytes, receipt agreed |
| Markdown/local Wiki links and composition | Validator and OMX wiki lint verified; specific counters in validation manifest |
| Private paths/secrets/public composition | Automatic verification and manual review of selected texts; no private raw/PDF/full vault; this is a scoped review, not universal proof of the absence of any secrets |
| Accepted/proposed/withdrawn semantics | Scope and corrected matrix accepted; domain rules/stack/eval open; 27/30 not returned |
| Git root/status/branch/worktrees/remotes | FAILED: `.git` Notrepo; metadata read-only |
| `git diff --check` | BLOCKED/FAILED without Git repo; no-index whitespace check of each new safe file was performed separately |
| Staging / staged diff / docs commit | NOT-RUN: There is no Git prerequisite; blanket staging was not used |
| App tests / typecheck / build / live eval | NOT-RUN: Application and dependencies are not created by this step |
| Remote change / push / public check | NOT-RUN, prohibited by stage |

`omx wiki wiki_lint --json`: 0 broken refs / 0 contradictions, **1 informational orphan** for a single content-page (a link from index is not counted as a link to another content-page). Manual index→page check passes. CLI lint added its own repo-local `omx_wiki/log.md`; the extra empty EOF string detected by the whitespace check is normalized without removing entries. When setting up an independent validator, two errors in the checker itself were fixed: processing the future self-excluded validation manifest and the expected exit 1 no-index diff with an empty file; the final run is recorded separately; initial assertion failures are not reported as green checks.

## 6. Prompts / redactions / spaces

Leader: The short message actually received is extracted from the actual session export, not replaced by H-004 or starter template. The public version removes four private paths, not the engineering essence. The source UTF-8 hash and destination hash are in the prompt receipt. The public session export contains the task and two progress messages before the cutoff; the original AGENTS/environment bundle is excluded entirely with a hash/reason. System/developer/reasoning are excluded by the exporter itself, tools are not requested; later actions and final response are missing. This is a **partial export**, not a full transcript. The private transcript remains in the session's private storage.

Workers coverage: **not-applicable**, no one was launched. CHAT-001..009: pointers/queue, not wholesale export; the normalized early history is not passed off as an accurate transcript. Runtime prompts: **not-yet-created**. The completeness of U-01 remains open. Snapshot redactions: private dependency links replaced with secure attribution or local links to included files; visibility refers only to the projection, chat owner/accepted/proposed/open are not replaced. Details - receipts and prompt index.

## 7. Matrix R-01..17 / U-01..08

Not a single application requirement is satisfied by the presence of a report. “Partially prepared” means only the basis/accounting, not acceptance of the product.

| ID | Status of this stage | What's there/what's next |
|---|---|---|
| R-01 | next stage | Teachers/Students/Courses and names are checked against PDF; schema/seed missing |
| R-02 | next stage | Offerings/semester/enrollment/grades taken into account; model and cardinality open |
| R-03 | next stage | NL→SQL→DB→the answer is fixed by a matrix; LangGraph was not created |
| R-04 | next stage | JOIN/aggregates/4 filters/multi-step taken into account; we need real examples and tests |
| R-05 | next stage | Circuit independence of the kernel and a coherent second circuit are taken into account; no proof of transfer |
| R-06 | next stage | The full trace chain is taken into account; application traces missing |
| R-07 | next stage | SQL/empty/inconsistent/ambiguous cases taken into account; no processing and running |
| R-08 | next stage | All three directions of tests are taken into account; not-run product tests |
| R-09 | partially by preparation | Separated owners of docs/prompts/memory; application code and modularity not verified |
| R-10 | next stage | Reliability/scalability/monitoring/security/deployment to be explained later |
| R-11 | next stage | Schema/seed was not created or published |
| R-12 | next stage | LangGraph code/tests missing |
| R-13 | partially by preparation | Single ADR index + preparation ADR; architectural solutions and public delivery are open |
| R-14 | next stage | There are no real examples/outputs/execution traces |
| R-15 | next stage | Public GitHub remains open; no local commit/remote/push/public proof |
| R-16 | next stage | There was no demonstration/independent defense/rehearsal |
| R-17 | next stage | The compact scope was accepted earlier, the application has not yet been proven to work |
| U-01 | partially by preparation | Actual task/selected export/coverage/redactions yes; history and runtime gaps explicit |
| U-02 | already confirmed fact (term only) | By entrance: evening November 7 / defense November 8, 2026, Asia/Jerusalem; exact time unknown, delivery not confirmed |
| U-03 | partially by preparation | OMX CLI is actually used; CLI only stage; doctor failures revealed |
| U-04 | partially by preparation | General indexing/preparatory ADR; app architecture open |
| U-05 | partially by preparation | Ownership saved, 4 safe snapshots and own omx_wiki; vault not replaced/changed |
| U-06 | partially by preparation | Checkpoint protocol recorded with proposed future status; Git execution blocked |
| U-07 | already confirmed fact on inputs | A new meaningful chat was started earlier on CHAT-005; here the transition was not repeated and was not independently reproduced |
| U-08 | next stage | The result-understanding procedure has been read, what remains is proposed; no comprehension checks were carried out |

## 8. Questions for the next architectural stage (not solutions)

1. **Data/semantics:** grading scale, NULL, mulligans/attempts, cardinality of offerings, average weight, default semester, namesakes/ties; previously proposed values ​​are not accepted.
2. **SQL engine:** choice and reasons, limitations/dialect, reproducible run; do not promise support for all dialects.
3. **Graph/contracts:** state, DB/schema-specific logic boundaries, continuation of refinements, dependent complex scenario; multiple nodes/SQL by themselves do not prove reasoning.
4. **Model/budget:** provider, version, cost/number of live runs, acceptable errors; Don't come up with a budget.
5. **UI/tracing:** a simple screen is already in scope, the library/backend is not selected; full Input→Nodes→SQL→Results→Answer, debugging, redaction and availability traces.
6. **SQL validation/limits:** possible read-only/time/row/retry limits and external SQL validation are engineering proposals, not verbatim PDF requirements; mechanisms and risks to be justified.
7. **Portability:** what is the small second circuit and what changes, what actual run/diff will prove the immutability of the kernel.
8. **Test/eval plan:** independent expected results for SQL/JOIN, NL→SQL, E2E; negative cases, all filters/aggregates/multi-step; justified metrics/set/thresholds, without the revoked 27/30 and without substitution of coverage percentage.

Architecture/contracts/plan require a separate CLI order, then analysis in chat **before implementation**.

## 9. Final statuses / blockers / transfer

- **Saved:** public-safe files are recorded and verified. **Committed:** not-committed — `.git` is an empty read-only mount, not a Git repository. `git init` did not try to get around this fact. Initial/final HEAD and branch: unavailable; status: not-a-repository, not clean. After preparation, the metadata blocker did not change.
- **Remote URL/SHA:** unavailable (the target workspace does not have a repo/config); remote was not created/modified. **Push:** not-run. **Public check:** not-run. R-15 is open.
- **Canonical blocker:** preferred target is justified by bounded check; Git identity/history/branch/worktree canonical repo is not installed due to protected metadata. Don't declare the canonical Git repo ready.
- **Environment caveat:** doctor failures EPERM/native smoke/stale session binding. Didn't update the tool, didn't simulate a healthy environment, didn't fix unproven runtime proficiency.
- **Open:** regular writable `.git` in the same target before the remaining Git preparation, owner/name/branch/publishing permissions, full historical/session export, exact deadline hour and questions §8. Publication is only a separate future assignment; the exact next step is described in Git checkpoints.

**The only next action is to transfer this report and artifacts to the chat. Stop after the final answer.**
