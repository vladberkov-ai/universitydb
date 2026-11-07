<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 2

**REJECT current edition; workflow verdict: `iterate`.**

Iteration 2 fixes the previous B1/B3/B4 and the main part of B2. Independently confirmed residual **B2-R1**: normative sum expression is incompatible with non-null integer ResultSpec for an empty scalar aggregate. A small documentary revision is required, then a new sequential Architect → Critic cycle. No other blocking gaps were found when reading the current package completely.

All architectural solutions remain **proposed**. Review does not allow implementation, paid calls, publication or execution handoff.

Further `P/` means `.omx/plans/H-006-B2/iteration-2/`.

## Proven foundation

Read the actual task and grounded context, full authoritative H-006-v5 handoff, current requirements and acceptance contract, scope/ownership ADR, local ralplan/plan instructions, fresh D2 report, all 13 constituent documents of the current bundle, manifest and changes mapping. Read the complete Architect1/Critic1 and **Architect2** reviews, baseline and Architect2 completion observation.

Saved researcher/dependency-expert final texts read as **dated reused inputs from 2026-11-07**, not new studies or approvals. Candidate pins are not considered installed or verified together. No specific new external-research gap has been identified.

Read-only checks:

- **14/14** manifest entries match raw SHA-256 and size.
- **13/13** constituent documents byte-equivalent to the corresponding sections of the bundle.
- All **6** JSON blocks of the bundle have been parsed.
- **25/25** current vault hashes match `inputs-observed.json.current_sha256`.
- The matrix contains **17 R + 8 U**.
- `omx quality-gates list --stage ralplan --json` returned `gates:[]`; this does not replace the required reviews.
- HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, branch `main`.
- Bundle raw SHA-256 before and after review:

  `fe92a07802c9ba497948b0f22f9f4fdb2031ed83273062ae76765d6d99974e86`

- Read Architect2 review raw SHA-256:

  `445bcc65db20c1a1d5ec983cbc6aa41509dcdb394c1510f9b1dbecf2992a4fd8`

The standard baseline uses domain-separated lifecycle digest, and manifest uses raw hashes. The difference between these digests **is not a sign of substitution**.

Original PDF did not re-decode on its own: an explicitly attributed leader receipt was used to read four pages; current PDF hash checked among 25 inputs. Completion observation Architect2 was read as evidence of a leader, but was not presented as an independent host lifecycle audit conducted by me.

An independent integer/rational check of documentary fixtures confirmed:

- S1–S6: sums of hundredths `50000/35000/40000/25000/26000/16000` and corresponding counts.
- M1/F1: top `{2}`, cohort `{1}`, result`95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, totals `{95.00,80.00,50.00}`.
- Tie mutation: top `{1,2}`, cohort `{1,2,3}`, results`{90.00,90.00,null}`.

This is an arithmetic document check, **not an application test**. The files, Git, state, IDs, tracker and Obsidian were not changed by me; the children did not start.

## Summary

- **Clarity:** high level of specificity; There is only one contradiction left: empty-aggregate representation.
- **Verifiability:** independent fixtures, exact expectations, sensitivity and future evidence are specific.
- **Completeness:** required documents and all R/U are present; B2-R1 blocks the consistency of a mandatory no-rows script.
- **Big Picture:** compact local demonstrator corresponds to the accepted scope; proposed/accepted/tested are separated.
- **Principle/Option Consistency:** **fail locally to B2-R1** — DB result must satisfy the declared typed normal path. Other previous violations have been corrected.
- **Alternatives Depth:** **pass** - local/server stack and simplified CLI are considered fairly; The CLI does not appear to be a sufficiently accepted screen.
- **Risk/Verification Rigor:** **pass except for specific B2-R1**; safety, semantic correctness, live quality and public delivery are not mixed.
- **Deliberate Additions:** **pass** - three credible pre-mortem and extended unit/DB/mock/live/E2E/trace/manual/public/defense checks are present.

## Verification iteration 1 fixes

| Finding | Result of Critic2 |
|---|---|
| **B1 - static/runtime dependencies** | **Fixed by documentation.** Full M1 allows symbolic references before results; `validate_plan` checks declared outputs/DAG, `bind_results` checks completed/consistent/nontruncated values. Corrupted runtime state has separate negative cases. `GraphState.results` stores already selected dependency rows, raw candidates remain in the trace. Evidence: `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **B2 - metric/grain/unit boundary** | **The main boundary has been corrected.** The final ResultSpec registry, domain adapter, integer components, exact ties, half-up2 and Library count normalization are specific. One remaining blocking defect is shown below. Evidence: `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **B3 – live vs injected faults** | **Fixed.** EI tests have injection provenance and 0 paid calls; live denominator - 48 real-model conversations, including continuation. N1–N4 check for no-data outcomes, not intentional model error; unexpected failures are not excluded. The set has honestly not yet been created and is not named sealed yet. Evidence: `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **B4 - accepted screen** | **Fixed.** SQL/bindings, typed DB rows and full same-run trace/attempts are available from the screen; success/resume/error are checked separately. Opaque ID and other people's old rows - fail. Evidence: `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`; `P/implementation-plan.md:9–12`. |
| **A1 - strict provider bindings** | **Enough for documentary B.** Closed bounded array, discriminator validation and deterministic SQLite mapping are described; actual SDK smoke remains future. Evidence: `P/contracts.md:238–241`; `P/test-plan.md:114–115`. |
| **A2 - resource boundaries** | **Enough with obvious residual risk.** There are byte/input/SQL/bindings/single-value boundaries; byte gate is not issued for exact tokenizer, watchdog is not for memory isolation. Evidence: `P/contracts.md:243–244`; `P/test-plan.md:115–116`; `P/production-considerations.md:13–17`. |

## The only blocking finding

### B2-R1 - Inner COALESCE does not normalize empty scalar SUM

**Priority:** P2. **Confidence:** high. **Fix route:** Planner; small documentary revision.

**Evidence:**

- `P/contracts.md:58` requires integer `SUM(COALESCE(grade_units,0))`, at the same time requires `sum_units=0` with a zero denominator.
- `P/contracts.md:204–207` shows `sum_units` as non-null integer in scalar mean ResultSpec.
- `P/test-plan.md:45,125` requires for C2/S2 normal `average=null`, `no_rows`, enrollment/graded count 0.
- `P/contracts.md:29,58,61` requires rejecting the broken result contract, and not guessing a correction.

**Specific Simulation N1:**

1. Accepted scalar `u.grade_mean.v1` for C2/S2.
2. Scoped relationship is empty.
3. Internal `COALESCE` does not process a single row; scalar `SUM` returns NULL.
4. Raw components become `[null,0,0]`.
5. Non-null integer ResultSpec rejects the result instead of the required normal `no_rows`.

Thus, the literal implementation of a normative rule cannot follow the intended normal path. This is a **specification consistency defect**, an undetected application bug: the application does not exist yet.

### Independent local verification

Performed only schema-free SELECT in SQLite `:memory:`, no tables, schema/seed, files or application. Local SQLite **3.45.1**, undeclared target version.

For expressions

`SUM(COALESCE(grade_units,0)), COALESCE(SUM(grade_units),0), COUNT(grade_units), COUNT(*)`

received:

| Input relation | Result |
|---|---|
| Empty | `(NULL,0,0,0)` |
| One line with NULL | `(0,0,0,1)` |
| One line with real 0 | `(0,0,1,1)` |

This is an **isolated diagnostic of aggregate semantics**, not a product/DB integration test. Finding Architect2 is independently verified.

### Minimal fixes

1. **Agree the normative formula with the ResultSpec.** It is preferable to preserve non-null integer components and use aggregate-level normalization, for example, the documentary `COALESCE(SUM(grade_units),0)`. No need to change the stack or build a SQL compiler.
2. **Add three concrete raw → normalized examples:**

| Case | `[sum_units,graded_count,enrollment_count]` | Expected |
   |---|---|---|
| Noenrollments | `[0,0,0]` | `average=null`, `empty_reason=no_rows` |
| Enrollment There is,grade NULL | `[0,0,1]` | `average=null`, `empty_reason=no_grades` |
| Real rating 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

3. **Specify V1/S10/N1–N3 verification:** The future real-DB check receives valid raw SQL components, and a separate adapter unit test converts them into a normal answer. Do not replace the first with the second and do not require a product launch in B.

A valid alternative—nullable raw sum with an explicitly specified normalization phase—is more complex and is not needed for the selected small contract.

**Pass as follows:** no-row mean gets valid integer components and normal `no_rows`; NULL-only and real-zero are different; there is no need to violate ResultSpec, throw error instead of normal outcome, or silently guess the rule.

## Representative implementation walkthroughs

### 1. M1 dependency Andmutation

The full plan is accepted before the SQL. F1 top adapter leaves course2, runtime binding gets cohort student1, final mean is 95.00. F2 changes top to course1 and cohort to 1/2/3. `GraphState.results` does not substitute all raw candidate IDs for the selected top IDs. Truncated or corrupted result stops downstream to provider/SQL.

**Bottom Line:** The old B1 no longer requires guesswork from the performer.

### 2. Scalar empty / NULL / zero

For N1, the ResultSpec requires an integer sum, but the prescribed SQL returns NULL. N2/N3 with an existing NULL-grade string and a real grade0 give different counts and should remain different normal outcomes.

**Result:** B2-R1 is a real local blocker; the three cases must be agreed together.

### 3. Transfer to Library and on-screen failure path

Library changes descriptor/domain adapter/fixture, not core; count1/1 and all-returned0/0 do not scale like grades. EI refusal/repair has injected provenance, does not fall into the real-model score; the screen shows the absence of SQL or all real same-run attempts and typed results. Mandatory DB/live/E2E/core-hash proofs remain in the future.

**Bottom Line:** Portability, UI evidence and evaluation methodology are now concrete enough for planning.

## Coverage and no additional blockers

- **R-01/02:** proposed ERD, identities, names, cardinalities, semester/retake/NULL semantics and independent fixtures; they are not assigned to PDF.
- **R-03/04:** real LangGraph/provider/DB vertical slice, four filters, JOIN traps, unequal groups and M1 sensitivity are provided.
- **R-05:** Library and unchanged-core boundary are verifiable; arbitrary SQL dialect support is not promised.
- **R-06/07/08:** traces/attempts/errors, controlled failures, actual-model generation and UI coverage are separated; empty mean requires B2-R1.
- **R-09/10:** responsibilities of modules and five production topics are revealed; memory/authentication/retention limitations are preserved.
- **R-11..15:** actual schema/seed/code/tests/examples/public access/SHA - future obligations; local B commit does not close them.
- **R-16/17:** manual walkthrough and independent owner defense are provided separately from agent review.
- **U-01:** actual prompts/read context/templates/coverage omissions are distinguished; the current review does not certify full native transcript coverage.
- **U-02:** the exact hour remains open.
- **U-03:** native provenance, terminal lifecycle and absence of handoff are checked by the leader.
- **U-04..06:** proposed ADR003–007, ownership, saving A/history and separate B docs commit reflected.
- **U-07:** historical verified transition is not declared as a new result B.
- **U-08:** discussion and observed understanding are yet to come.

Unknown credentials/budget, owner acceptance and public authority **not independent blockers documentary B**. They block related future actions. Withdrawn27/30 not restored; new48/48 gate clearly proposed.

## Alternatives Andsynthesis

**Strongest steelman:** free read-only SQL with independent oracle and transparent traces is easier for a small educational project; Over-typed IR can turn demonstrator into its own compiler.

**Real stress:** free result columns simplify generation, but force formatter to guess units/grain/NULL. A small ResultSpec eliminates guesswork, but must match valid aggregate edge cases.

**Synthesis:** save the current final registry/domain adapter and free SQL generation; fix exactly empty-sum normalization and three boundary examples. An independent oracle remains necessary: ​​typed shape does not prove SQL semantics.

## Stop condition

Submit this review and the completed Architect2 review Planner. Create **new immutable iteration**, do not change reviewed bytes; after a small correction, run a new separate Architect → separate Critic cycle and configured gates within max5.

Current iteration **not approved**. Supported closeout, native completion/provenance, `active:false`, prompt packaging and commit remain the responsibility of the leader after passing reviews. This review does not assign them.

Application tests, actual SDK compatibility, live eval, UI execution, public delivery Andowner rehearsal — **not-run**. Execution authorization/handoff absent.
<!-- END_CRITIC_REVIEW -->
