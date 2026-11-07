---
title: "Criteria for the original task"
updated: 2026-11-07
status: accepted
owner: chat
visibility: public-ready
sources: ["PDF pages 1-4", "CHAT-007", "CHAT-006", "CHAT-008"]
---

# Source criteria: fix CHAT-007

Reread original PDF (private source; not exported), all four pages.
Correction source: CHAT-007 (private source; not exported).
CHAT-008 confirmed the compliance of the corrected matrix with the task and instructed to prepare a CLI package. The matrix is ​​adopted as the basis of transmission; This is not confirmation of checks performed.
Previous version (private source; not exported) saved for history.

## Correction
The previous answer replaced the discussion of compliance with the task with the agreement of a number of additional
subject rules and numerical threshold. These rules have been marked proposed but are not
conditions of the original task. The 27/30 threshold is not justified PDF and cannot allow non-compliance
mandatory requirement. It has been withdrawn from the current offer of acceptance.
The latest short list also did not explicitly cover the names of students/teachers, independence
kernels from circuits, conflicting results and production considerations.

## Mandatory requirements and suggested evidence

| Source | PDF Requirement | How to check execution |
|---|---|---|
| p1, R-01/02 | SQL DB: Teachers, Students, Courses; the name of each student and teacher; the teacher teaches the course during the semester; students sign up for offerings and get grades | Schema/seed, connections and constraints, example data and validation |
| p1, R-03 | LangGraph application: natural question → SQL → execution → clear answer | End-to-end run, code and actual result |
| p1, R-04 | Aggregates, JOIN, filters by semester/course/teacher/student, multi-step reasoning | Separate coverage of each type and complex examples with independent expected answers |
| p2, R-05 | The kernel is independent of a specific circuit; adaptation to another database/scheme is simple; subject logic isolated | Boundary code, explanation of changes; consistent second scheme as a method of proof |
| p2, R-06 | Full trace Input → Nodes → SQL → DB Results → Answer; yours or LangSmith | Available full traces and self-analysis for interviews |
| p2, R-07 | Detect and handle invalid SQL, empty/inconsistent results, ambiguous questions; show faulty output diagnostics | Scenarios of each type, routes, explanation of the reason and treatment; detection limits are stated honestly |
| p2, R-08 | Query/JOIN tests, SQL generation from NL and E2E LangGraph | Executable tests of all three directions and their actual results |
| p2-3, R-09 | Clean, modular, understandable code; clear responsibilities DB/agent/prompts/tracing | Code structure and walkthrough |
| p3, R-10 | Explain the path in production: reliability, scalability, monitoring/tracing, security, deployment | Document and explanation of implemented and future work |
| p3, R-11..15 | SQL schema/seed, code, tests, solutions, examples/answers, execution traces; everything on public GitHub before the interview | Full set, repository availability and compliance with the verified version |
| p3-4, R-16/17 | A working, explainable and debuggable solution; showing system, code/architecture, tracing and choice protection | Self-demonstration and rehearsal |

The PDF calls the test section Unit Tests and includes E2E there. Division into unit/integration/E2E
acceptable as an organization of checks, but does not cancel any direction.
Multi-step reasoning does not necessarily mean a fixed number of SQL queries; several nodes
The graphs themselves do not prove reasoning. You need a meaningful, complex example with explainable steps.

## Selected sources of liabilities
User agreed scope (CHAT-006 / ADR-CHAT-002): simple screen, dependent script,
second small diagram. These are demonstration methods, not verbatim PDF terms.
User requirements: actual prompts, all architectural decisions with reasons,
wiki/CLI-ownership, Git evidence and deadline on the evening of November 7; The PDF itself requires publication prior to the interview.
Previously proposed procedures clean clone/manual E2E and SHA checks are ways to confirm delivery,
rather than literal source lines.

## What should not be stated now
PDF does not specify a 0-100 scale, NULL tolerance, single final grade, retake policy,
a rule for choosing a default semester, an average weight, an exact table scheme, or a quantitative eval threshold.
The phrase about the course instructor for the semester must be supported by the model; full set of cardinalities
and restrictions must be justified when designing, without attributing it to the source.
Read-only/limits - engineering security proposals; PDF requires explanation security,
but does not specify a specific mechanism.

## Next step according to plan
Use this matrix as a basis for requirements and evidence, maintaining the accepted scope.
When preparing an independent CLI task, list underdefined subject rules
as questions for an architectural proposal with options/reasons. Architecture is back
in the chat for analysis before implementation. If necessary, justify the numerical eval plan separately;
the success rate does not cover the missing mandatory behavior.
H-003 remains the old, unmodified draft; a new, up-to-date package is needed before transfer.
Implementation and OMX do not run in this fix.

---
Projection H-004 v2: derivative chat-owned shot, unedited original. Private dependencies are not exported; SHA-256 and change log are in the repo receipt. Application execution statuses are not changed by this projection.
