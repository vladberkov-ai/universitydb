<!-- BEGIN_CRITIC_REVIEW -->
# Critic review — H-006 B2, iteration 1

**REJECT current edition; workflow verdict: `iterate`.**

The package is comprehensive, but does not yet allow you to implement the required scenarios without guesswork. Three blocking findings by Architect have been independently confirmed; Another gap concerns the already accepted composition of the demo screen. A documentary Planner revision and a new complete Architect → Critic cycle are required. This review does not allow implementation, publication, paid calls or execution handoff.

## Proven foundation

The actual task, grounded context, authoritative H-006-v5 package, current requirements and acceptance contract, all 12 constituent documents in the bundle, completed Architect review, saved researcher/dependency-expert final texts have been fully read. Research used as **historical entries from 2026-11-07**, not new research or approvals.

Read-only checks:

- All **13/13** raw hashes and sizes from `iteration-1/manifest.json` matched.
- All **12/12** constituent documents byte-equivalent to the corresponding sections of the bundle.
- Raw SHA-256 bundle until review is complete:
  `b83dadcc0ea53f63afea1e2bfe7da3b562dba5313cc06cbe8b6c114961755fc6`.
- Raw SHA-256 read by Architect review:
  `2b6aec6d1b8b68926e53c5ba42d08e7a3df81e03825ec4a5fed35bfba73b9e3e`.
- **25/25** current vault hashes coincided with `inputs-observed.json.current_sha256`. Five differences from the historical manifest are already explained by D2; These are not new requirements changes.
- HEAD remains `8931d832d49311ac0d63c3a7a359b4293058da89`.
- Matrix contains **17 R + 8 U** rows.
- `omx quality-gates list --stage ralplan --json` returned `gates:[]`. This does not replace the required reviews.
- Read the implementation of the installed `digestAdvisoryArtifacts`: standard artifact/manifest digests use domain-separated `hashParts`, so they do not have to be equal to raw `sha256sum`. The difference between baseline digest and raw hash **is not a substitute found**.

Documentary fixtures are independently recalculated using integer/rational arithmetic:

- S1–S6: amounts in physical hundredths `50000/35000/40000/25000/26000/16000`; counts and averages correspond to the table.
- M1/F1: top C2, cohort `{1}`, result `95.00`.
- M1/F2: top C1, cohort `{1,2,3}`, results `{95.00,80.00,50.00}`.
- Tie mutation: top `{C1,C2}`, results `{90.00,90.00,null}`.

This is **not running SQL, application or product tests**. The Original PDF was not decoded again on its own: the explicitly provided leader receipt for reading four pages was used, verified against the PDF hash. The files, Git, tracker, state and Obsidian were not changed by me; subagents did not start.

Further `P/` means `.omx/plans/H-006-B2/iteration-1/`.

## Summary

- **Clarity:** the main decisions are specific; The dependency validation phases and the semantics of the transmitted result are ambiguous.
- **Verifiability:** independent fixtures and sensitivity are strong; live fault cases are not yet reproducible.
- **Completeness:** documents and all R/U lines are present; The four indicated joints are not yet closed.
- **Big Picture:** compact local demonstrator corresponds to the accepted direction; proposed/accepted/actually-tested are separated correctly.
- **Principle/Option Consistency:** **fail locally** - unit/grain boundary does not provide the declared independence of the core; mixing live generation and injected faults weakens the principle of evidence separation.
- **Alternatives Depth:** **pass** - minimal local and server options are considered in detail; The CLI is rightly excluded as the only interface.
- **Risk/Verification Rigor:** **fail to B1–B4**; Security restrictions, semantic correctness, and public delivery are otherwise described fairly.
- **Deliberate Additions:** three credible pre-mortem and extended unit/DB/mock/live/E2E/observability/manual/public/defense plan **present**. Their presence does not eliminate the contradictions of specific scenarios.

## Blocking findings

### B1 - A complete dependent plan contradicts the “references only to completed steps” rule

**Evidence:** `P/contracts.md:27,45–46`; `P/architecture-proposal.md`, section “Graph and meaningful dependent path”.

`PlanProposal` is created before the SQL is executed and contains the entire DAG. However, references are only allowed on completed steps and existing typed columns; `Step` doesn't even declare an output circuit.

**Simulation:** when receiving M1, the correct link of the second step to the first cannot yet indicate a completed result. A literal implementation will reject M1; another implementation will defer the check at its own discretion.

**Minimum Planner fix:**

1. Separate static plan validation and runtime result binding.
2. In the static phase, resolve unresolved symbolic references to DAG predecessors, checking IDs, acyclicity, direction and declared output columns/types.
3. Before dependent SQL, require a completed non-trunked result and materialize typed values.
4. Assign exact failure codes and failure phase for missing column/type mismatch/truncated dependency.
5. Add a specific valid M1 plan and negative cycle/missing-column/runtime-overflow examples.

**Pass:** M1 plan is accepted before SQL; its links are linked only after matching results; each negative example stops at the specified phase without a downstream call.

With Architect B1 **I agree based on my own reading**.

### B2 - Metric/grain/unit are not related to the result, although the formatter is required to check them

**Evidence:** `P/contracts.md:28–30,42,45,47–48`; `P/architecture-proposal.md`, sections of subject arithmetic and schema-agnostic boundary.

`Metric` has a description of /unit/grain, but neither Step, nor SQLProposal, nor DBResult normatively associate a specific result with this metric. `expected_columns` specifies only names. Formatter must check grain, units, counts and perform normalization.

**Simulation S6:** DBResult with column `average` and decimal row does not tell whether the numbers mean physical hundredths or external estimates. It is impossible to reconstruct an exact comparison of ties from an already rounded average. Library count requires another rule, but where to implement it is not defined.

**Minimum Planner fix:**

- Add a small result specification or an explicit domain-result-adapter contract: metric/result-shape ID, group keys, typed aliases, unit/scale, necessary aggregate components.
- For average/top, fix integer `sum_units` and `graded_count`, owner of exact comparisons and final rounding, zero-denominator/NULL behavior.
- Do not transfer University-specific checks to core through column name recognition.
- Show concrete messages and expected for S6, M1/ties, Library count and wrong unit/missing denominator/wrong grain errors.

**Pass:** messages are unambiguously converted to `80.00`, the correct set of ties and Library counts without heuristics named `average`. Invalid forms give the specified error, not a plausible answer.

I **agree** with Architect B2. A full typed SQL compiler is not required.

### B3 - Live generation suite requires errors that cannot be reproducibly obtained from the model

**Evidence:** `P/test-plan.md:64–72,82–92`; related `P/requirements-test-matrix.md` R-07/R-08, `P/ADR-OMX-007-verification-delivery.md`.

E3 deterministic refusal/incomplete/malformed responses are then included in full E2E with the actual model. Category `failure/refusal/invalid SQL` is also included in the mandatory 24 held-out cases ×2, but the mechanism of action is not defined.

**Counterexample:** the real model generates correct SQL instead of incorrect one. SQL error handling has not been tested, but this is not a NL→SQL defect. Replacing the transport fixture answer and counting it as live generation is a reverse methodological error.

**Minimum Planner fix:**

1. Leave all provider/SQL failure branches as mandatory controlled injected tests.
2. Separately identify UI/E2E fault-injection lane with provenance of impact; do not include it in the live generation score.
3. Live negative cases should be specified by user queries with specific acceptable outcomes, not a requirement to intentionally obtain an erroneous generation.
4. Explicitly designate unexpected provider failures as unsuccessful live attempts.
5. Agree on categories, denominator, repetitions, budget and ADR/matrix after separation.

**Pass:** for each negative case it is clear which component is real, what exactly is injected and which property the result proves. Mocks/injections are not considered NL→SQL accuracy.

I **agree** with Architect B3. I do not reject the proposed strict small-suite threshold itself: it is honestly proposed and is not called a statistical guarantee.

### B4 - Screen with one trace ID does not cover already received SQL/data/full trace

**Evidence:** accepted `docs/chat/decisions/ADR-CHAT-002-result-scope.md`, section “Solution”; `P/test-plan.md:84,102`; `P/requirements-test-matrix.md` R-06/R-17.

The accepted scope includes a screen with the response, SQL, data and the full trace. The specific acceptance screen lists question/answer/clarification/error/**trace ID**, but not viewing SQL, typed DB rows and the entire chain of events.

**Counterexample:** the screen shows the correct answer and an opaque ID; The JSONL exists on disk, but the demonstrator prevents it from being opened from the consistent interface. The current screen checklist allows this result.

This is Architect A3, which I'm **raising to blocking** due to straight accepted scope rather than a new UI preference.

**Minimum Planner fix:**

- It is standard to specify a simple local expander/view or an accessible link that opens SQL with secure bindings, DB columns/rows and a full trace of the same run.
- Add manual/E2E pass-fail for success, clarification/resume and error with multiple attempts.
- Agree on R-06/R-17, implementation I1/I4 and scope walkthrough.

**Pass:** A screen observer can trace a specific question back to the SQL, the actual lines, and the answer/error; run/trace IDs match; trace ID without available content - fail. A separate tracing platform and UI implementation are not needed in B.

## Advisory, not independent blockers

1. **Strict provider wire representation.** `P/contracts.md:3,27,48`: closed objects and dynamic parameter map require explicit wire/domain mapping before compatibility smoke. A small example of bounded list bindings with deterministic conversion is useful; the specific view is selected by Planner. According to archival research, one cannot state that the candidate stack is already installed or is obviously incompatible.

2. **Resource boundary coverage.** `P/contracts.md:33–34`; `P/production-considerations.md`: Add separate future boundary tests for input-token limit, SQL/parameter size and large single DB value. Timeout/result caps should not be passed off as hard memory isolation; the current residual risk is indicated honestly.

No new external research calls are required for B1–B4. If revision selects a new parser, tokenizer or provider-fault mechanism, the invoice for it should be checked separately, and not added from memory.

## Packet coverage check

| Region | Evaluation |
|---|---|
| R-01/02: ERD, names, offerings, semesters, grades | Sufficient suggested design and concrete fixtures; domain rules are not passed off as PDF |
| R-03/04: LangGraph, JOIN/filters, dependent reasoning | Oracle/sensitivity strong; B1/B2 block unambiguous execution contract |
| R-05: portability | There is a specific Library schema and unchanged-core check; result boundary requires B2 |
| R-06: full traces | Contents/attempts/errors/redaction provided; screen demo requires B4 |
| R-07/08: errors, SQL/NL/E2E | The levels are mostly separated correctly; B3 breaks reproducibility of live negative scenarios |
| R-09/10: modules and production | Responsibilities and five production topics are revealed; production-ready is not declared |
| R-11..15: kit and public delivery | Future evidence/clean clone/SHA/anonymous access is provided; local commit does not replace public proof |
| R-16/17: explainable demonstrator/defense | Observable owner rehearsal is provided; B4 is needed for full demo scope |
| U-01 | Actual/template/read-context and omissions are distinguished; the attached received-task projection does not mean full native transcript coverage |
| U-02 | Dates saved; exact hour honestly open |
| U-03 | The real lifecycle must be confirmed by the leader; reviews are not replaced by prompt labels |
| U-04 | ADR003–007 contain options/rationale/consequences/test/revision |
| U-05/06 | Ownership, saving A/history, separate B commit and remote/push ban reflected |
| U-07 | Historical verified transition is not given as a new result B |
| U-08 | Future deep dive/self-explanation envisioned but not yet completed |

Lack of credentials, owner acceptance and public authority **does not block documentary B**; it blocks corresponding future live/public actions. Proposed domain decisions are not a disadvantage in themselves: recommendations and alternatives are presented.

## Strongest alternative and synthesis

Steelman against strengthening contracts: for a small training SQL agent, read-only SQL, independent Oracle and transparent traces may be sufficient; too rich an IR will turn the demonstrator into its own query compiler and break minimality.

Real tension: free SQL gives simplicity and expressiveness, but free units/grain/references forces the downstream to guess. The full compiler is overkill.

**Synthesis:** keep the proposed stack and free SQL generation, add only two-phase references and a small result contract for supported shapes. An independent oracle remains required; runtime validation is not declared as proof of arbitrary NL semantics.

## Stop condition Andhandoff

Submit **this complete review and completed Architect review Planner**. Fix B1–B4 in a new immutable iteration, agreeing on contracts/examples/test-plan/matrix/ADR/implementation, then execute a new separate Architect → separate Critic cycle and actual configured gates. Do not patch reviewed baseline.

**There is no approval for the current iteration.** Until passing reviews, do not consider B approved and do not close it as an approved/proven architecture. Supported closeout, native completion/provenance, prompt packaging and commit are checked by the leader. No execution authorization has been created.

<!-- END_CRITIC_REVIEW -->
