---
title: "Register of requirements"
updated: 2026-11-07
status: accepted
owner: chat
visibility: public-ready
sources: ["PDF; CHAT-001; CHAT-002; CHAT-003"]
---

# Register of requirements

Assignment source: original PDF (private source; not exported), extracted text (private source; not exported).
Custom sources: CHAT-001 (private source; not exported), CHAT-002 (private source; not exported), CHAT-003 (private source; not exported).

| ID | Source | Commitment | Proof of Completion | Status |
|---|---|---|---|---|
| R-01 | PDF p1 | SQL: Teachers, Students, Courses; name of each student and teacher | schema + seed + constraints/tests | open |
| R-02 | PDF p1 | Course delivery by teacher during the semester, student notes, grades | ERD, SQL, link tests | open |
| R-03 | PDF p1 | LangGraph: natural question → SQL → execution → clear answer | graph code + live example | open |
| R-04 | PDF p1 | Aggregates, JOIN, filters by semester/course/teacher/student, multi-step | proven complex examples | open |
| R-05 | PDF p2 | Circuit-independent, domain-specific, modular kernel | ADR + boundary code + adaptation check | open |
| R-06 | PDF p2 | Full trace Input → Nodes → SQL → DB Results → Answer; yours or LangSmith | route export + demonstration | open |
| R-07 | PDF p2 | Detecting and Handling SQL Errors, Null/Inconsistent Data, and Ambiguity | negative scenarios + debugging analysis | open |
| R-08 | PDF p2 | Query/JOIN, NL→SQL and E2E agent tests | tests and actual results | open |
| R-09 | PDF p2-3 | Clean, modular, explainable DB/agent/prompts/tracing structure | code + review + architectural diagram | open |
| R-10 | PDF p3 | Explain production: reliability, scaling, monitoring/traces, security, deployment | production.md with the boundaries of the implemented | open |
| R-11 | PDF p3 | Transfer SQL schema and seed data | SQL/data files in public repo | open |
| R-12 | PDF p3 | Submit LangGraph code and tests | code and tests in public repo | open |
| R-13 | PDF p3 | Documentation of design decisions with explanation | architecture + ADR in public repo | open |
| R-14 | PDF p3 | Examples of requests and results, execution traces | examples + traces in public repo | open |
| R-15 | PDF p3 | Public GitHub repo with the entire kit before the interview | URL + visibility + SHA + non-login verification | open |
| R-16 | PDF p3-4 | Show the system, code, architecture, traces; explain and defend choice | rehearsal protocol | open |
| R-17 | PDF p4 | A small working, explainable and debuggable solution; AI is acceptable | scope and self-defense | open |
| U-01 | CHAT-001 | Provide actually used prompts | chat/OMX prompt index + exports + runtime prompts | open |
| U-02 | CHAT-001 | Due by Saturday evening; defense on Sunday | November 7/8, local time; check exact time | open |
| U-03 | CHAT-002 | Use OMX; one stage - one environment | stages + handoff + CLI results | open |
| U-04 | CHAT-003 | Record all architectural decisions with justifications in repo | ADR-CHAT and ADR-OMX, common index | open |
| U-05 | CHAT-003 | UniversityDB by LLM-Wiki, chat results without copies of OMX results | vault + sources + connections + repo pointers | open |
| U-06 | CHAT-003 | Define commit/push and periodic OMX commit in advance | Git protocol + sync log | open |
| U-07 | CHAT-004 | Complete the preparatory chat and transfer the context via LLM-Wiki to the new | Closeout + H-002; opening a chat by a user | verified |
| U-08 | CHAT-004 | Fix the order of familiarization with the results and their deep understanding | result-understanding.md + subsequent parsing protocols | proposed |

The open status refers to the fulfillment/acceptance of the entire obligation, not to the presence of this table.
U-05: structure created; The continuity of management is still checked in further stages.
U-06: protocol proposed, not executed. R-15 cannot be closed by a local git commit.

## Suggestions, not PDF requirements
P-01: Second small subject diagram as evidence of R-05.
P-02: read-only connection, resource and attempt limits, SQL checking outside the prompt.
P-03: 25–40 evaluation cases with independent expected results and delayed sampling.
P-04: Short contracts and end-to-end prototype to detailed specification.
P-01 is accepted as part of the scope of CHAT-006. The remaining points should not be considered entirely accepted by this confirmation. Cloud/Kubernetes/UI of a particular type are not required by PDF.

Each closure requires a reference to the artifact/commit/review. Review and assistant self-assessment are not a substitute for evidence.

Addition CHAT-004: Transition request (private source; not exported).
U-07: the transition took place via CHAT-005: the user started a meaningful chat, packet H-002 was read. U-08: Procedure proposed, understanding checks not yet performed.

CHAT-005: new request (private source; not exported). U-07 is confirmed by the very start of a new chat and reading the packet.
Brief and criteria (private source; not exported) proposed, R-01..17 not closed. OMX launch and implementation are delayed until outcome/acceptance is agreed upon.

CHAT-006: adopted compact volume according to [ADR-CHAT-002](decisions/ADR-CHAT-002-result-scope.md), including the second scheme and dependent script. Acceptance does not close R-01..17; subject rules and criteria are included in [draft contract](planning/acceptance-contract.md).

CHAT-007: PDF reconciliation p1-4. [The corrected matrix](planning/acceptance-contract.md) separates the obligatory from the methods of proof. Additional subject rules and the 27/30 threshold are not accepted; the threshold has been removed from the current proposal. The accepted volume CHAT-006 has not been cancelled. The execution statuses of R-01..17 remain open.

CHAT-008 (2026-11-07): The corrected matrix was confirmed by the user as being appropriate for the task. Prepared H-004 for repo preparation phase. The implementation requirements remain open; subject rules/stack/numeric eval thresholds are not approved.

CHAT-009: ADR-CHAT-003 (private source; not exported) captures placement and OMX method selection. U-03/U-05 are specified, mandatory R and acceptance criteria are not changed; launch is prohibited in this chat.

CHAT-010: preparatory certificates R-09/R-13/U-01/U-03/U-04/U-05/U-06 partially verified against artifacts; these obligations are not completely closed. There is no Git checkpoint; grocery R remain open. Parsing (private source; not exported).

CHAT-011: H-005 continues U-01/U-03/U-04/U-05/U-06 and R-13/R-15 preparation; The application criteria do not change. All product results remain open.

---
Projection H-004 v2: derivative chat-owned shot, unedited original. Private dependencies are not exported; SHA-256 and change log are in the repo receipt. Application execution statuses are not changed by this projection.
