# ADR-OMX-004 - Identities and Domain Arithmetic

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
PDF requires names, courses/semesters/teachers/enrollments/grades, but does not specify scale/retakes/weights/ties.

## Options
Normalized Offering/Enrollment; a separate Course row for each offering; co-teaching junction; credit weights/latest-retake-only.

## Recommendation
Students/Teachers names nonunique, stable ID; Course→Offering with one teacher/semester; grade nullable integer hundredths from 0 to 10000; external decimal0..100; equal weights graded enrollments, all-retakes, all exact ties, all-semesters default.

## Rationale
Separates a course from a particular offering, prevents silent identity merge, arithmetic is explainable by small fixtures without hidden weights/current date.

## Consequences
Retakes within offering/co-teaching are not modeled; The average of the course is not the average of the averages. NULL not 0. Any change in the rules changes oracle.

## Verification
S1–S14 real DB constraints/aggregates, C1 duplicate-name clarification, exact rational tie comparisons, documented fixtures.

## Revision triggers
The owner selects credit-weighted/latest-only/co-teaching/history or another default semester.

Related [architecture](../plans/architecture-proposal.md), [contracts](../plans/contracts.md), [checks](../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
