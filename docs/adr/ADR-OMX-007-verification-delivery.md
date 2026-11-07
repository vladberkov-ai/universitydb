# ADR-OMX-007 - Independent oracle, live gate and delivery evidence

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
Mocked graph does not measure NL-SQL. Previously proposed 27/30 withdrawn; percentage does not replace mandatory R/U. Saved/committed/public are different.

## Options
Singlesuccess percentage; onlyunit mocks; layered checks+independent fixtures+small strict live suite/manual/public gates.

## Recommendation
S/C/E/T/L+D/V/W/UI1 mandatory tests; EI1–EI3 deterministic injected UI lane with provenance and 0 paid calls separately, 24dev+24heldout×2 counted runs; proposed48/48 **real-model conversations** semantic passes, including 4negative-data cases×2, without injected faults in denominator without unsafe/privacy failures; <=$2 approved cap; manual protection and public SHA separately.

## Rationale
The small demonstrator must reproduce every promised scenario; strict repetition detects instability, but is not a statistical guarantee for arbitrary questions.

## Consequences
Gate may require prompt/model refinement and fresh heldout; best-of/relabel failures are not allowed. Budget/key/public authority are missing yet; B docs only.

## Verification
test-plan oracle/manual disclosedSQL/DB/full trace path, N1–N4 real-model no-data outcomes vs injected E1–E7/EI1–EI3; unexpected provider failures count failed live attempts, all attempts+hashes/usage, clean clone, remote SHA anonymous access, observed owner explanation; current application checks not-run.

## Revision triggers
Owner-approved revised scope to eval, token-rate changes, dataset contamination, new model/prompt/schema or observed failure pattern.

Related [architecture](../plans/architecture-proposal.md), [contracts](../plans/contracts.md), [checks](../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
