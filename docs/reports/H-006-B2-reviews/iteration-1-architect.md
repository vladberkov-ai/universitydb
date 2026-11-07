<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 1

**Verdict: `iterate`**
**Role:** individual Architect; not Critic.
**Decision status:** proposed; this review does not authorize the implementation or closure of the Advisory.

## Summary

The recommended minimum stack, domain model, and most independent benchmarks are architecturally sound. However, three interfaces require documented fixes: dependent plan validation, transfer of aggregate semantics between adapters, and reproducibility of negative live/E2E checks. That's why I'm not giving **APPROVE** now.

## Verified baseline and evidence boundaries

Read `.omx/plans/H-006-B2/iteration-1/plan-bundle.md` in full: 465 lines, all 12 constituent documents.

**Raw SHA-256:**
`b83dadcc0ea53f63afea1e2bfe7da3b562dba5313cc06cbe8b6c114961755fc6`

Verified:

- `.omx/plans/H-006-B2/iteration-1/manifest.json`: all **13/13** files are the same size and SHA-256; includes bundle.
- All **12/12** constituent documents match the corresponding sections of the bundle.
- Repeated raw hash bundle before completing review matched.
- **25/25** current vault inputs match `current_sha256` to `.omx/context/H-006-B2/inputs-observed.json`.
- Current HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`.
- Read the full authoritative H-006-v5 handoff, actual task, context/activation/Planner completion/baseline receipts, fresh D2, accepted current R/U matrix, acceptance contract, scope/ownership ADR and both saved research-final.
- Original PDF was not independently re-decoded: the leader-provided `.omx/context/H-006-B2/pdf-read-receipt.json` was used, capturing the reading of four pages. This is **not Architect's own PDF revalidation**.
- Researcher/dependency-expert materials from 2026-11-07 are used as **previously completed research**, not new research or reviewer approvals.

Performed independent recalculation of documentary fixtures using integer/rational arithmetic - **not SQL, not product test**. S1–S6, M1/F1 `95.00`, M1/F2 `{95.00,80.00,50.00}` and tie mutation `{90.00,90.00,null}` were confirmed.

The files, Git, runtime state, tracker and Obsidian were not changed by me. Review is transmitted to the leader by text to save a separate immutable artifact.

## Positive architectural implications

1. **The subject model is consistent with most standards.** Course is separated from Offering; names are not keys; NULL, mulligans between offerings, equal weights, all-semesters default and exact ties explicitly proposed. Fixtures distinguishes between a row average and an average of averages, and M1 is tested by changing the data, changing the intermediate cohort.
   Evidence: `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:25–39`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:27–52`.

2. **Orchestration is truly bounded at the project level.** There are common call/SQL/repair/clarification budgets, disabling SDK retries, separate provider branches, session-bound resume, replay protection, restart expiry and prohibition of side effects before interrupt. The well-known feature of restarting interrupt-node has been taken into account.
   Evidence: `.omx/plans/H-006-B2/iteration-1/contracts.md:5–13,32–35,44–49`.

3. **Security is not passed off as semantic correctness.** Read-only, authorizer, allowlists and watchdog are separated from oracle-based response validation; plausible wrong SELECT honestly remains a limitation. Trace failure does not turn into success.
   Evidence: `.omx/plans/H-006-B2/iteration-1/contracts.md:29–39`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:64–74`.

4. **Porportability has a verifiable limited scope.** Library is a specific second scheme, with expected and zero-return variant; the immutability of the core hash and real DB/live/E2E checks are provided. Support for arbitrary SQL dialects is not stated.
   Evidence: `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:41–42`; `.omx/plans/H-006-B2/iteration-1/test-plan.md:76–84`.

5. **Documentary lifecycle is not mixed with product readiness.** All 17 R and 8 U have future evidence lines; public access, owner defense, real prompts and Git separately from the application. ADR003–007 contain options, causes, consequences, tests, and revision conditions. Three pre-mortem and extended levels of checks are present.
   Evidence: `.omx/plans/H-006-B2/iteration-1/requirements-test-matrix.md:3–33`; `.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:44–49`; `.omx/plans/H-006-B2/iteration-1/plan-bundle.md:6–165`.

## Blocking findings

### B1 - Static checking of DAG and runtime binding results are not separated

**Priority:** P1. **Correction:** minor/medium, documented.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/contracts.md:27,45–46`
`.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:37–39`

The contract requires that references point only to already completed steps, prohibits future references, and requires existing typed columns. At the same time, the only initial `PlanProposal` must contain the entire plan before SQL execution, and `Step` does not declare the schema of its result.

**Counterexample:** the required M1 must contain in advance the dependency step2 on `step1.course_id`, and step3 on `step2.student_id`. At the moment of accepting `PlanProposal`, no result exists yet. A literal check of the contract will reject a valid M1; another implementation will silently defer the check, although the normative moment for its execution is not defined.

This is not a requirement to know future **values** in advance. It is necessary to distinguish between a planned link and a binding that is allowed to be executed.

**Minimum correction:**

- When accepting a plan, check the unique IDs, DAG, topological direction and declared output names/types of previous steps.
- Resolve future results of previous DAG steps as **unresolved symbolic references**.
- Immediately before generating/executing dependent SQL, require a complete, consistent, untrunked result and materialize the reference into typed values.
- Define a failure code for a missing/incorrectly typed column and prohibit downstream calls in case of an error.
- Add valid full M1 PlanProposal, invalid cycle, missing column and runtime truncated-reference examples with expected.

**Checking the fix:** Documentary M1 goes through both phases, but cycle, missing column and oversized cohort stop at the explicitly stated phase without the following SQL.

### B2 - Formatter/validator promise semantic checks, but the result is not related to metric/grain/unit

**Priority:** P1. **Correction:** average, no stack change.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/contracts.md:27–30,42,45–48`
`.omx/plans/H-006-B2/iteration-1/architecture-proposal.md:32,42`

Formatter should check grain, scoped IDs, `graded<=enrollment`, ranges and translate `sum_units/count/100`. But the normative `SQLProposal`/`DBResult` carry free names of columns and scalar types, not a mandatory connection with a metric, unit, aggregate components or grain. `Metric` contains a description, but the result does not indicate which Metric record it applies to.

**Counterexample:** `expected_columns=["average"]` and decimal result are legal by contract. From them it is impossible to determine whether the column contains the average in physical hundredths, an already normalized estimate, or another decimal metric. It is impossible to restore the exact `sum/count` for a tie comparison if only the rounded average is returned. Likewise, it is not defined which adapter must implement University-specific checks so that the core does not begin to recognize the names `grade`/`graded_count`.

This is **not** a requirement to prove arbitrary NL→SQL semantics. We are talking about the stated deterministic rules of units, results and domain boundaries.

**Minimum correction - one of two options:**

1. Small `ResultSpec` at the step: metric/result-shape identifier, group keys, typed aliases, unit/scale and required aggregate components; or
2. Explicit domain result adapter contract, which receives the verified specification and DBResult, performs domain validation/normalization and returns a unified Answer.

For average/top, define the required integers `sum_units` and `graded_count`, owner of exact comparison/final rounding, zero denominator rules. Core should not implement University-specific semantics for column names.

**Fix check:** show concrete messages for S6, M1/ties and Library count, including invalid unit/missing denominator/unexpected grain. They should have unambiguous results without heuristics based on the free column name.

**Principles:** The provision of principles 2 and 5 - “computes the database, not the model” and schema-agnostic core - has not yet been completed. This is a design boundary gap, an unproven defect in existing code.

### B3 - Negative live/E2E cases do not have a reproducible mechanism of action

**Priority:** P1. **Correction:** minor/medium, test-plan.

**Evidence:**
`.omx/plans/H-006-B2/iteration-1/test-plan.md:64–72,82–92`

E3 requires refusal/incomplete/malformed output. These cases are correctly provided for by scripted-provider graph tests. However, then E3 is included in **full E2E with actual model**, and category `failure/refusal/invalid SQL` is included in the required 24 held-out real-model cases with two successful repetitions.

It is not specified which faults are caused by the real provider, which are introduced by the test transport/adapter, and which are normal negative user issues. Intentionally receiving invalid SQL or refusal from a real model is a non-reproducible fault-injection contract.

**Counterexample:** a real provider responds with a correct structured proposal instead of the expected artificial SQL error. The error handling check did not formally take place, but this does not indicate bad NL→SQL. The reverse error is to replace the response and then count the result as live generation evidence.

**Minimum correction:**

- Leave all E3 branches in mandatory deterministic injected tests.
- For UI/E2E, explicitly mark injected provider/transport faults and save the source of the impact; do not include them in the real-model generation score.
- In the live suite, define specific negative-user-request classes and acceptable observable outcomes; Don't require the model to generate erroneous SQL in order to pass the test.
- If you need a separate live provider-failure experiment, describe the mechanism, expected and cost; Do not promise unverified API behavior.
- Clarify denominator/category mapping and budget after division. The proposed strict threshold itself is not rejected.

**Checking the correction:** for each negative case it is clear what is actually being called, what is being replaced, and what property is being proven.

**Principle:** The current mix risks violating Principle 4 - separation of security, semantics and evidence.

## Advisory findings

### A1 - Strict provider schema mapping should be defined explicitly

`contracts.md:3` declares private JSON objects, and `contracts.md:48` uses a dynamic `parameters` map. The research I've already read warns about the JSON Schema subset and private objects.

The external/provider schema split is recognized, but the conversion has not yet been described. Explicit wire representation is recommended - for example, a limited array `{name,value}` with uniqueness check - and deterministic conversion in DB bindings. We need an example of strict SQLProposal schema/normalization and future compatibility smoke. This is **not a statement** that the selected candidate packages are no longer compatible.

### A2 - Resource limits require separate future boundary tests

`contracts.md:33–34` does a good job of limiting calls, timing, and bytes returned, but these caps themselves do not limit SQLite memory before the first row is returned. `production-considerations.md:13` honestly leaves hard memory enforcement as a separate job.

Before I1, you should select scoped SQLite limits/worker resource policy or explicitly retain the residual risk. Add tests for input-token overflow, SQL/parameter size and very large single value. Do not consider passing the regular timeout test as proof of memory isolation.

### A3 — Clarify the visibility of SQL/data/trace on the demo screen

`test-plan.md:84` lists the trace ID, but the accepted scope includes showing the response, SQL, data and the full trace (`docs/chat/decisions/ADR-CHAT-002-result-scope.md`, Solution section). A simple ID is not enough for a practical walkthrough without a specific way to open the corresponding events. A local expander/view or an explicit accessible link is sufficient; A separate tracing platform is not needed.

## Root cause

The documents describe the components individually well, but in some places they replace the **transfer contract between components** with a promise of behavior: “check typed reference”, “check grain”, “show real-provider failure”. What is needed is not a new architecture, but several normative links with specific messages and verification phases.

## Trade-offs and consensus to be added

### Antithesis — strongest steelman

For a small training demonstrator, a free read-only SQL agent, independent fixtures and a transparent route may be sufficient. Adding a rich typed query/result IR risks turning a short project into its own SQL compiler and worsening the principle of minimalism. One cannot demand a universal proof of NL semantics, which the plan itself rightly does not promise.

### Real tradeoff tension

| Option | Benefit | Price |
|---|---|---|
| Free SQL and free result columns | Minimum adapter code, wide NL scope | Ambiguous units/grain/dependencies; formatter is forced to guess |
| Full typed query IR with SQL generation | Strong structural verifiability | Significant volume, expressibility limitation, scope creep risk |
| **Minimum ResultSpec + two-phase references** | Clear units/aggregate outputs and dependent transitions; saves real NL→SQL | Small additional contract and domain adapter tests |

### Synthesis

Keep the proposed minimum stack and free SQL generation inside a verifiable secure subset. Add only a small result contract for supported metrics and separate symbolic plan references from runtime bindings. Semantic oracle remains model independent; no contract is claimed to be proof of arbitrary SQL correctness.

Proposed owner decisions - scale, retakes, default semester, model, budget, strict small-suite gate - **not blockers in themselves**: recommendations, alternatives and revision conditions are presented.

## Recommendations and stop condition

1. Correct B1/B2 in contracts and agree on M1/S6/Library examples; do not create an application or executable schema.
2. Correct B3 in test-plan and corresponding matrix/ADR references.
3. Transfer this review to a separate Critic of the current cycle; my verdict does not replace his verification. The subsequent revision should be carried out through the provided full cycle.
4. No additional research is required for these documented corrections. Choosing a specific parser/tokenizer or a new provider-failure mechanism will require a separate scoped verification if Planner decides to add it.

**Review completed; verdict `iterate`.** Product tests/live/API compatibility/security execution - **not-run**. Terminal lifecycle, native completion and closeout are checked by the leader after the actual completion of this agent. There is no Execution authorization.

<!-- END_ARCHITECT_REVIEW -->
