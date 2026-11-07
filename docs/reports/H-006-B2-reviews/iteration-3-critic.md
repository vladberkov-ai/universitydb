<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 3

**OKAY. Workflow verdict: `approve`.**

**Blocking findings: 0. No required fixes.** No new issues were found that would prevent Document Package B from being accepted for chat discussion.

B2-R1 fixed; previous fixes B1/B2/B3/B4 have been retained. The package is sufficiently specific and internally consistent for subsequent separate assignment of implementation after decisions are made by the owner. This is **not an implementation permission**, not a confirmation of the application's functionality, and not the end of the lifecycle.

Further `P/` means `.omx/plans/H-006-B2/iteration-3/`.

## Proven foundation

Read in full:

- `P/plan-bundle.md`: **773 lines, 124495 bytes**, all **14 constituent documents**, including both changes mappings;
- manifest Andbaseline receipt iteration 3;
- actual user task, grounded context, authoritative H-006-v5 package, current requirements/acceptance contract and accepted scope;
- applicable project instructions, local ralplan/plan skills, latest D2 report;
- complete Architect/Critic reviews iterations 1–2 and completed **Architect3 `approve`**;
- saved researcher/dependency-expert final texts as **dated reused research inputs 2026-11-07**, not new studies or reviewer verdicts.

No specific new external-research gap has been identified. Candidate pins are not considered installed, co-verified, or security audited.

### Fresh read-only checks

| Check | Result |
|---|---|
| Raw hashes and dimensions manifest iteration 3 | **15/15 matched** |
| Constituent documents versus corresponding bundle sections | **14/14 byte-equivalent** |
| Fenced JSON examples | **12/12 parsed** |
| Full M1: topology and types symbolic references | **pass**, no need for runtime values ​​|
| ThreeZ-couplesraw DBResult → Answer | **pass documentary consistency** |
| Current vault hashes against `inputs-observed.json.current_sha256` | **25/25 matches** |
| Previous iterations 1/2 vs their manifests | **13/13 and 14/14 saved** |
| Requirements Matrix | **17 R + 8 U** |
| Non-runtime source files vs B2 baseline | **95/95 unchanged** |
| Git index vs. baseline | **unchanged** |
| Git | canonical root, `main`, HEAD A saved; staging/remotes are empty |
| Additional quality gates | CLI returned `{"gates":[],"stage":"ralplan"}` |

Raw SHA-256 bundle before completion review:

`e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`

Raw SHA-256 read by Architect3 review:

`0914935a942be1c89c0c56d26f0be4371b795a674c590662ccd0939d3df4ce00`

HEAD:

`8931d832d49311ac0d63c3a7a359b4293058da89`

Manifest contains raw hashes; regular baseline - domain-separated lifecycle digest. The difference between these ideas is not taken as a substitution.

Original PDF did not re-decode on its own: the leader's clearly attributed `.omx/context/H-006-B2/pdf-read-receipt.json` about four pages was used; the current PDF hash has been verified. Architect3 completion observation is read as evidence of the leader, and is not passed off as an independently completed host lifecycle audit.

The files, Git, state, IDs, tracker and Obsidian were not changed by me. Didn't let the kids in.

## Summary

- **Clarity:** pass - component roles, types, verification phases, errors and execution boundaries are defined.
- **Verifiability:** pass - independent fixtures, exact expected, negative mutations, pass/fail and future evidence paths are specific.
- **Completeness:** pass - the required documents and all 25 R/U lines are present; previously detected blocking gaps have been eliminated.
- **Big Picture:** pass — compact local demonstrator corresponds to the accepted scope; proposed/accepted/actually-tested are not mixed.
- **Principle/Option Consistency:** pass - recommendations are consistent with minimalism, schema-agnostic boundary and safety/semantics/evidence separation.
- **Alternatives Depth:** pass - local and server options are considered fairly; The CLI is not issued as a sufficiently accepted screen.
- **Risk/Verification Rigor:** pass - retries/resources boundaries, shape/read-only checks insufficiency, live/injected distinction and public delivery are disclosed.
- **Deliberate Additions:** pass - three credible pre-mortem and extended unit/actual-DB/mocked-graph/live-NL/UI-E2E/trace/manual/public/defense checks are present.

## Verification previous comments

| Finding | Result Critic3 and evidence |
|---|---|
| **B1: static DAG vs runtime binding** | **Fixed.** `P/contracts.md`, "Two-Phase DAG..." section: `validate_plan` accepts typed symbolic references of predecessors; `bind_results` requires completed/domain-validated/nontruncated data. Full M1, cycle/missing-alias mutations and D1–D3 have precise failure phases and prohibit downstream calls. `GraphState.results` stores the selected dependency rows, raw candidates remain in the trace. |
| **B2: metric/unit/grain/result boundary** | **Fixed.** The final ResultSpec registry and DomainResultAdapter fix integer components, unit/scale, group keys, exact ties and half-up2. Library count does not pass grade normalization. Wrong unit/denominator/grain have certain errors. Evidence: `P/contracts.md`, ResultSpec/registry and JSON examples; `P/test-plan.md`, V1–V2. |
| **B2-R1: empty scalar SUM** | **Corrected completely at the document level.** Regulatory formula - `COALESCE(SUM(grade_units),0)`, not row-level COALESCE. Z1/Z2/Z3 contain full typed raw messages and normalized Answer. DB-Z and UNIT-Z test different boundaries. Evidence: `P/contracts.md`, “B2-R1...”; `P/test-plan.md`, S10/N1–N3/V1 and final section; `P/ADR-OMX-006-schema-boundary-tracing.md`. |
| **B3: live accuracy vs injected failures** | **Fixed.** EI1–EI3 are clearly injected, have provenance and 0 paid calls. Live denominator — 48 real-model conversations with continuation; N1–N4 check no-data outcomes. Unexpected failures are taken into account and are not removed from the denominator. Revealed prototypes are not named by the already created sealed suite. Evidence: `P/test-plan.md`, live gate and “Two different negative lanes”; ADR007. |
| **B4: received screen** | **Fixed.** SQL/bindings, typed DB rows and full same-run events/attempts are available from the screen. UI1 distinguishes between success, pause/resume, repair and terminal error; opaque ID, disappeared attempts and rows of another run - fail. Evidence: `P/architecture-proposal.md`, components; `P/test-plan.md`, UI1; matrix R06/R17; implementation I1/I4. |
| **A1: provider bindings** | **Enough fordocumentary B.** Closed bounded array, discriminator/type checks, deterministic SQLite mapping, duplicate/placeholder checks described. Actual SDK smoke remainsfuture. |
| **A2: resource boundaries** | **Enough with obvious residual risk.** W1–W3 distinguish between request/SQL/bindings/value boundaries and byte/token accounting. Watchdog is not issued for hard memory isolation; production gap saved. |

### B2-R1: Independent consistency check

| Case | Raw `[sum_units,graded_count,enrollment_count]` | Normalized Answer |
|---|---|---|
| Noenrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
| Enrollment exists, grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
| Real rating 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

In all three raw examples sum/counts are non-null integers, scalar `row_count=1`. The number of aggregate rows does not replace the number of original enrollments. Missing GROUP BY groups are not automatically promised. Nullable raw sum is prohibited and is not silently corrected by the formatter.

Future **DB-Z** requires valid SQLite components/types before adapter; **UNIT-Z** checks the conversion and deviation of `sum_units=null` separately. This removes the previous ability to validate the formatter without validating the raw query result.

No new SQL probe was required. These checks remain **documented**, DB-Z/UNIT-Z is **not-run**.

## Representative implementation walkthroughs

### 1. M1: dependency, mutation and ties

The full plan is accepted before the SQL. F1 top adapter selects course2, runtime binding gets cohort `{1}`, final mean - `95.00`. F2 changes top to course1, cohort - `{1,2,3}`, answers - `{95.00,80.00,50.00}`. Tie fixture selects both courses and union cohort, answers - `{90.00,90.00,null}`.

Truncated/corrupted dependency stops the next provider/SQL call. Core does not substitute all raw candidates for the selected top IDs.

**Conclusion:** the executor does not need to guess the references resolution phase or the semantics of the intermediate result.

### 2. Scalar mean: emptiness, NULL and real zero

Reception of ResultSpec, raw integer components and normal output are now consistent for all three cases. SQL is responsible for aggregate components, domain adapter is responsible for precise normalization/rounding; the model doesn't come up with numbers. Inappropriate raw shape is rejected.

**Conclusion:** the former mandatory no-rows scenario no longer requires breaking the contract.

### 3. Library and screen failure path

Library replaces DB/descriptor/domain adapter, not core. Counts `1/1` and all-returned `0/0` do not scale as grades. Unchanged-core hash, actual DB, mocked graph, live NL and UI evidence remain separate future checks.

Injected refusal indicates the absence of SQL/DB; injected repair shows both attempts and the final typed results. No such result becomes live accuracy evidence.

**Conclusion:** portability and UI/error acceptance are verifiable without extension B before implementation.

### Independent arithmetic reconciliation

Integer/rational recalculation of documentary fixtures confirmed:

- S1–S6 sums Vhundredths: `50000/35000/40000/25000/26000/16000`;
- corresponding graded/enrollment counts and averages;
- M1/F1, M1/F2 and tie outcomes listed above.

This is an expected calculation based on document strings, **not SQL/application/E2E test**.

## Completeness of requirements and boundaries

- **R01–R04:** ERD/names/offerings/semesters/grades, four filters, JOIN duplication trap, unequal groups, retakes and meaningful M1 are covered.
- **R05–R08:** Library unchanged-core transfer, full trace chain, ambiguity/resume, controlled errors, actual-model NL and E2E separated.
- **R09–R10:** DB/agent/prompts/tracing/UI responsibilities and all five production topics are covered without a production-ready claim.
- **R11–R15:** schema/seed/code/tests/examples/public kit, clean clone, remote SHA and anonymous access remain future commitments; local B commit does not close them.
- **R16–R17:** independent owner rehearsal and simple screen are provided, agent consent does not replace protection.
- **U01–U08:** actual/template/read-context and omissions are distinguished; deadline hour is open; native lifecycle is checked by the leader; ADR/history/ownership/A/B saved; historical U07 not assigned to B; deep understanding remains to be seen.

Owner acceptance, credentials/budget, future compatibility smoke and public authority are gates of relevant future actions, **not independent blockers documentary B**.

The recalled `27/30` has not been reinstated. The new `48/48` is clearly proposed, has a limited small-suite purpose and is not declared as a statistical guarantee.

## Alternatives, tradeoff Andsynthesis

**Strongest alternative:** for a small demonstrator, free read-only SQL with independent oracle and transparent traces is simpler; An overly typed IR can turn the job into its own compiler and delay the first real vertical slice.

**Real stress:** free result columns reduce adapter code, but force downstream to guess units/grain/dependencies. Strict ResultSpec takes the guesswork out of registry and boundary tests.

**Synthesis of the current package is sufficient:** final shapes/domain adapters, two-phase references and precise arithmetic while maintaining real SQL generation. A universal query compiler is not introduced. An independent semantic oracle remains necessary: ​​model/shape/read-only/trace completeness does not prove the correctness of SQL.

## Advisory observations - optional fixes

1. Save the final size of the ResultSpec registry during implementation; add new metrics via domain adapter and tests, not University heuristics in core.
2. When packaging, do not increase the level of evidence: candidate pins, walkthroughs, fixture arithmetic and review approval do not turn into executed compatibility/E2E/security evidence.
3. Save I0→I1 and the early real vertical slice; do not replace it with the preliminary construction of universal abstractions.

## Stop condition

**Critic3 review completed: `approve`, required corrections 0.**

The leader then checks the real native completion of this agent, records the result of configured gates and performs a supported Advisory closeout. An empty list of additional gates does not replace reviews.

Terminal state, `active:false`, explicit absence of execution authorization/handoff, prompt coverage, public-safe packaging, link/privacy/diff checks and a separate docs commit B **to be confirmed by the leader**. This verdict does not take credit for their results.

Application tests, actual SDK compatibility, live eval, UI execution, public delivery and owner rehearsal - **not-run**. All new architectural solutions remain **proposed until discussed in the chat**.

<!-- END_CRITIC_REVIEW -->
