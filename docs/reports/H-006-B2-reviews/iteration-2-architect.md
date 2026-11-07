<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 2

**Verdict: `iterate`.**
**Role:** separate Architect, not Critic.
**Status:** documentary advisory; solutions remain proposed. Implementation and execution handoff are not allowed.

## Summary

Iteration 2 meaningfully fixes B1, B3, B4, and most of B2. However, in the normative contract of the mean there remains a specific contradiction for the **empty set**: the prescribed `SUM(COALESCE(grade_units,0))` returns NULL, whereas the ResultSpec requires the integer `sum_units=0`. This breaks the intended normal outcome S10/N1 in the literal implementation of the contract.

We need a small documentary amendment and three precise zero-case examples, **not a change of architecture, not a SQL compiler, and not an application implementation**.

Further `P/` means `.omx/plans/H-006-B2/iteration-2/`.

## Proven foundation

Completely read by `P/plan-bundle.md`: **713 lines, 114166 bytes**, all 13 constituent documents, including changes mapping. The actual task/context, authoritative H-006-v5 handoff, current requirements/acceptance contract, accepted screen scope, completed Architect1/Critic1 reviews, Planner2 completion receipt, baseline receipt, fresh D2 report and both saved research-final have been read.

Read-only checks:

- **14/14** manifest entries matched in raw SHA-256 and size.
- **13/13** constituent files byte-equivalent to the corresponding sections of the bundle.
- **13/13** iteration 1 files saved according to its manifest.
- **25/25** current vault hashes coincided with `inputs-observed.json.current_sha256`.
- All **6** JSON blocks of the bundle have been parsed.
- Matrix contains **17 R + 8 U**.
- `omx quality-gates list --stage ralplan --json` returned `gates:[]`; this does not replace reviews.
- HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, branch `main`.

Raw SHA-256 bundle before and after review:

`fe92a07802c9ba497948b0f22f9f4fdb2031ed83273062ae76765d6d99974e86`

The standard baseline receipt uses another, domain-separated digest; it is not replaced by raw SHA-256.

An independent recount of documentary fixtures confirmed:

- S1–S6: sums in hundredths `50000/35000/40000/25000/26000/16000`, consistent counts/averages.
- M1/F1: top `{2}`, cohort `{1}`, answer `95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, answers `{95.00,80.00,50.00}`.
- M1/ties: top `{1,2}`, cohort `{1,2,3}`, answers `{90.00,90.00,null}`.
- Calculation of the proposed token-rate estimate: `$1.056`.

This is arithmetic document checking, **not application execution or SQL integration tests**. Original PDF did not re-decode on its own: an explicitly attributed leader receipt was used to read four pages; current PDF hash checked among inputs.

Researcher/dependency-expert materials are used as **historical inputs from 2026-11-07**, not new research and not reviewer approvals. Candidate pins do not mean installation/compatibility/security proof. No new external studies were conducted.

Files, Git, state, IDs, tracker and Obsidian did not change; didn't let the kids in.

## Verification comments from the previous cycle

| Finding | Independent result |
|---|---|
| **B1 - static DAG / runtime binding** | **Fixed at project level.** `validate_plan` allows symbolic refs on declared outputs; `bind_results` requires completed/domain-validated/nontruncated data. Full M1 DAG, cycle/missing-column/runtime corruption mutations and prohibition of downstream calls are specific. The last state bundle saves the already selected top dependencies, separately from the raw candidate trace. Evidence: `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **B2 - metric/grain/unit/result boundary** | **The main boundary is fixed, the rest is below blocking.** There is a final registry, ResultSpec, domain result adapter, exact integer components, rational ties, half-up2, Library count without grade scaling and negative unit/denominator/grain examples. Core is not required to guess domain semantics from column names. Evidence: `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **B3 — injected faults / real-model score** | **Fixed.** EI1–EI3 have injected provenance and 0 paid calls; The actual-model suite separately counts 48 conversations, including continuation. Unexpected failures are not removed from the denominator, N1–N4 require no-data outcomes, not an artificial generation error. The disclosed examples are not honestly called sealed suite. Evidence: `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **B4 - full screen** | **Fixed.** SQL/bindings, typed DB rows and all same-run events/attempts are available through expanders; success, clarification/resume, repair and terminal error are provided, other people's old rows are excluded. Opaque ID clearly fails. Evidence: `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`; `P/implementation-plan.md:9–12`. |
| **A1 — closed wire bindings** | **Sufficient for the documentary stage.** Bounded closed array, nullable slots, discriminator validation, exact placeholder/name checks and deterministic conversion are specified. The future SDK compatibility smoke remains honestly a future, not a blocker B in itself. Evidence: `P/contracts.md:238–241`; `P/test-plan.md:114–115`. |
| **A2 - resource boundaries** | **It is enough with an explicitly saved residual risk.** There is SQL/input/bindings/single-value boundary tests; byte accounting is not issued for exact tokenizer, watchdog is not for memory isolation. Evidence: `P/contracts.md:243–244`; `P/test-plan.md:115–116`; `P/production-considerations.md:13–17`. |

## The only blocking finding

### B2-R1 - Inner COALESCE does not normalize SUM of empty set

**Priority:** P2; mandatory minor documentary amendment.
**Confidence:** high, confirmed by isolated local diagnostics.

**Evidence:**

- `P/contracts.md:54–58`: mean registry requires integer components, and the normative rule prescribes `SUM(COALESCE(grade_units,0))` and at the same time requires `sum_units=0` with a zero denominator.
- `P/contracts.md:204–207`: concrete S6 ResultSpec declares `sum_units` non-nullable.
- `P/test-plan.md:45,125`: empty C2/S2 should return normal `average=null`, `no_rows`, enrollment/graded count 0.
- `P/contracts.md:29,58`: damaged result shape is rejected; semantic mismatch is not allowed by SQL repair.

**Counterexample to literal implementation:**

1. For N1, select scalar `u.grade_mean.v1`.
2. Scoped relation C2/S2 does not contain rows.
3. The prescribed `SUM(COALESCE(grade_units,0))` returns NULL: there is no row to which the internal COALESCE would be applied.
4. Raw tuple turns out to be `[null,0,0]`, not `[0,0,0]`.
5. ResultSpec validation rejects it, although the required expected value is normal `no_rows`.

This is not a proven application defect: there is no application. This is a **contradiction between a regulatory specification and a specific mandatory scenario**.

### Isolated aggregate semantics check

Executed only schema-free SELECT on temporary SQLite `:memory:`; without tables, schema/seed, files and application. Local SQLite: **3.45.1**, not declared as future target version.

For expressions:

`SUM(COALESCE(x,0)), COALESCE(SUM(x),0), COUNT(x), COUNT(*)`

received:

| Login | Result |
|---|---|
| Zero lines | `(NULL, 0, 0, 0)` |
| One line with `x=NULL` | `(0, 0, 0, 1)` |

This is an **isolated diagnostic of the behavior of the unit, not a product/DB integration test**.

### Minimal fix

It is preferable to keep the current non-null integer ResultSpec and replace the normative sum rule with **aggregate-level normalization**, for example the documentary `COALESCE(SUM(grade_units),0)` with integer zero.

Addconcrete raw-result → normalized-answer examples:

| Case | `[sum_units,graded_count,enrollment_count]` | Expected |
|---|---|---|
| Noenrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
| Eatenrollment, grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
| There is a real rating of 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

Align S10/N1–N3 and V1 with these messages. Future DB integration should check **real SQL outputs**, and unit adapter tests should separately convert them.

The alternative - allowing nullable raw sum and normalizing in the adapter before checking another form - is possible, but extends the contract unnecessarily. For a selected small system, outer COALESCE is easier.

**Pass for the next edition:** no-row path does not require breaking a nullable contract or changing normal outcome to error; All three cases have been documented; further product checks remain in the future.

## Architectural assessment of the rest of the package

- **ERD/semantics agreed:** Course/Offering, nonunique names, FK/cardinalities, integer grade units, NULL, retakes, all-semesters scope and exact ties explained as proposed. Not assigned to PDF. Evidence: `P/architecture-proposal.md:25–34`; `P/ADR-OMX-004-domain-semantics.md:5–24`.
- **Bounded orchestration is specific:** global budgets are saved via resume; plan calls, provider retry and repair are taken into account; interrupt-node does not repeat paid work before pausing. Evidence: `P/contracts.md:5–13,32–35,44–49`.
- **Portability is reasonably limited:** Library changes domain adapter/descriptor/DB, not core; the promise does not apply to arbitrary SQL dialects. Unchanged-core verification requires actual DB/live/E2E evidence. Evidence: `P/architecture-proposal.md:41–42`; `P/test-plan.md:76–84`.
- **Obligations are not covered by paper review:** matrix distinguishes between SQL/app/live/public/manual/defense/provenance; local commit does not replace R-15. Evidence: `P/requirements-test-matrix.md:3–33`; `P/implementation-plan.md:3–26`.
- **Deliberate additions are present:** five principles, three drivers, meaningful alternatives, three pre-mortem and an extended unit/DB/graph/live/E2E/observability/manual/public plan. Evidence: `P/architecture-proposal.md:5–14,44–49`; `P/test-plan.md:54–103`.
- **Production boundaries are fair:** five required topics, planned versus actual, no production-ready/security/memory guarantees. Evidence: `P/production-considerations.md:3–17`.

### Principles

B1/B3/B4 no longer generate previously detected boundary violations and evidence. Residual B2-R1 violates the consistency of the principle **“computes the database, not the model”** with the promised typed normal outcome: the bottom layer must produce a representation that the top layer is entitled to accept.

This is a local contract defect, not a reason to reject the selected stack or require a universal semantic validator.

## Consensus addendum

**Antithesis - strongest steelman:** for a compact training solution, free read-only SQL, independent oracle and transparent traces might be sufficient. Additional typed shapes risk growing into their own query compiler and pushing aside the real vertical slice.

**Tradeoff tension:** free results are easier to generate, but force the formatter to guess units/grain/NULL; strict ResultSpec eliminates guesswork, but requires careful coordination of real SQL edge cases with the wire contract.

**Synthesis:** keep the accepted compromise of iteration-2 - a small final ResultSpec registry and domain adapter, not a full compiler. Fix exactly the aggregate normalization of emptiness and add three precise examples. An independent semantic oracle remains required; runtime shape checks do not prove the correctness of arbitrary SQL.

Proposed owner decisions, unknown credentials/budget and future SDK smoke **are not independent blockers documentary B**. No new external research calls are required for this amendment.

## Recommendations and stop condition

1. Pass this completed review to **separate Critic iteration 2** without skipping the current sequence.
2. When B2-R1 is confirmed, perform a small Planner revision in **new immutable iteration**, then again separate Architect → Critic and configured gates. Do not correct already reviewed bytes.
3. Do not require the implementation of an application or live calls in order to accept a documented amendment.
4. Lifecycle/native completion/closeout, prompt packaging and commit remain the responsibility of the leader; my review does not certify them.

**Review completed: `iterate`, one blocking finding B2-R1.**
Application tests, live eval, actual provider compatibility, UI execution, public delivery Andowner rehearsal — **not-run**. Execution authorization/handoff absent.

<!-- END_ARCHITECT_REVIEW -->
