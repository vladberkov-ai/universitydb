# I2-offline acceptance contract

Accepted H-011 v2 / CHAT-043 / ADR-CHAT-006; repo-owned safe synthesis. Implementation evidence pending. [Decision](../adr/ADR-OMX-011-I2-offline-semantics.md). Historical contracts v1 remain proposed outside this explicit scope.

## Independent frozen seed oracle
The eight records and expectations below were transcribed from accepted scope before dependent code. No production formatter/query generator is the oracle.

| Case | Scope | Exact raw components / expected |
|---|---|---|
| Q1 | All | 50000/6/8 →83.33; 4 distinct students |
| Q2 | S1; C1 all; Kim10 all; student1 all | 35000/4/6→87.50;40000/5/6→80.00;25000/3/5→83.33;26000/3/3→86.67 |
| Q3 | Bea2/C1/Kim10/S1; student1 same others | 16000/2/2→80.00;9000/1/1→90.00 |
| Q4 | Course groups/S1 | C1 25000/3/4→83.33;C2 10000/1/1→100.00;C3 0/0/1→null |
| Q5 | Counts C1/S1 | enrollments4;graded3;distinct students3 |
| Q6 | Listing C1/S1 | (1,1,9000),(2,1,6000),(3,1,null),(2,5,10000); correct Student/Course/Teacher/Semester labels |
| Q7 | student1/C1 all; S2 | 16000/2/2→80.00;7000/1/1→70.00 |
| Q8 | C2/S2;C3/S1;isolated zero | [0,0,0] no_rows;[0,0,1] no_grades;[0,1,1]→0.00;count0 remains0 |
| Q9 | Top course S1; exact tie | C2; mutate student2/O1=8000 and student1/O2=9000→C1,C2 both90;250/3 not equal83.33 |
| Q10 | Average Alex choices | exactly student1/3; select1→86.67;select3→null/no_grades; no generated SQL before choice |
| Q11 | Current semester; ID/name conflict; unknown; vague count | known choices; explicit conflict/unknown; count object choice, no fabricated ID |
| Q12 | Each group + optional filters | group keys course/student/teacher/offering/semester; all 16 four-filter subsets against independent seed oracle, discriminating mutation for every key/filter |

## Contracts and failure proofs
Accepted Step.result_spec, not global domain.spec, controls result shape/types including NULL and empty lists. Registry identifies mean, count, listing, grouped variants and top, unit/scale/components/grain. No extra fields/aliases/bindings; exact scope bindings, duplicates/type errors/unknown unit or grain rejected. Integrity scans check grade ranges/types, foreign keys, duplicates, names/catalog consistency. AST allowlist and SQLite read-only authorizer independently deny unsafe SQL. Oracle detects plausible wrong JOIN/aggregation independently of runtime safety.

Use real in-memory LangGraph checkpoint/interrupt and server session identity. Resume binds session/run/checkpoint/clarification/schema/data/policy; TTL900seconds, pauses≤2. Exact replay returns original result without calls, changed same-ID payload conflicts. Reject stale/foreign/invalid/expired before downstream dispatch, preserve all call/token/spend/active-work counters and trace across reruns, exclude human wait. Restart expires; no durable promise.

One parse/unknown-column repair only, unsafe/semantic mismatch terminal. DB missing/locked/timeout, provider refusal/incomplete/invalid/unknown usage and trace/resource failures return no fabricated answer. Unknown usage accounting_stop prevents retry and preserves monetary history. Result≤100 rows/64KiB, no truncation for any I2 shape; trace≤1MiB and complete SQL/raw typed rows/answer or error, same run. Existing profile/output/time/call ceilings unchanged. Full wire includes instructions, payload, schema/framing and is checked offline; no count endpoint.

## Required evidence
Targeted tests per unit, full offline regression/static checks, strict-wire tests, real DB semantic oracle/mutations and corruption/security/bounds, compiled graph checkpoint/replay/failures, isolated AppTest, real offline browser success/clarification/repair/error screenshots and same-run traces. Cleaner then rerun verification; independent code-reviewer APPROVE+architect CLEAR and configured blocking gates; invariant audit and prompt/source/hash provenance, CP1–CP4 plus separate receipt commit. Offline never claimed live accuracy. Live/push/I3–I5/defense excluded, not blockers.
