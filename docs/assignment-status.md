## Current accepted work
I1 complete. H-011 v2 / CHAT-043 accepts I2-offline implementation and CP1–CP4; passing implementation evidence pending. Live/API generation and push prohibited, not conditions of offline completion. I3–I5 and defense remain pending. The audit below describes baseline I1, not new I2 results.

# Assignment deliverables and current gaps

Audit date2026-11-07. Checked against the original four-page assignment. Original
private PDF is not redistributed; this is a faithful requirement summary. The prompt
history is an additional owner requirement, not an explicit PDF deliverable.

| Requirement | Current artifact/evidence | Status |
| --- | --- | --- |
| Students/Teachers/Courses with names, offerings/semesters/enrollments/grades | [schema](../resources/schema.sql), [seed](../resources/seed.sql), [DB tests](../tests/test_db_domain.py) | Implemented for synthetic fixture |
| LangGraph question→SQL→DB→readable answer | [agent](../src/universitydb/agent.py), [live evidence](reports/H-009-live-I1-closeout.md) | Implemented for explicit four-filter grade mean |
| Complex aggregation, JOIN, filters and multi-step | Mean/count components and JOIN with4filters | Partial; other intents/groupings and multi-step NOT implemented |
| Schema-agnostic core/modular schema logic | [domain adapter](../src/universitydb/domain.py), core without University table names | Partial; second-schema adaptation NOT demonstrated |
| Full traces input→nodes→SQL→rows→answer | [examples](../examples/README.md), UI download, JSONL | Implemented for I1 |
| SQL/data/empty/ambiguous errors and debugging | [graph tests](../tests/test_graph.py), read-only/typed guards, failure trace | Partial; broad ambiguity resolution and conversational clarification absent |
| Query/JOIN, NL-SQL and E2E tests | [tests](../tests),131 recorded passes;2distinct live inputs+browser | I1 coverage, NOT broad NL accuracy evaluation; injected and live distinguished |
| Clear modular structure | src/universitydb DB/agent/domain/LLM/prompts/tracing/UI | Implemented I1 boundaries |
| Production reliability/scaling/monitoring/security/deployment discussion | [production considerations](plans/production-considerations.md) | Document present; production implementation not claimed |
| Design decisions with reasons | [ADRs](adr/README.md), ADR008–010 implemented scope | Present; ADR003–007 remain proposed |
| Example queries and outputs, execution traces | [examples](../examples/README.md) | Present for I1 |
| Public GitHub with schema/seed/code/tests/docs/examples/traces | Repository main and relative links | Published checkpoint, NOT final feature-complete submission |
| Interview explanation and defense | Code/trace/decisions accessible | Owner preparation remains pending |
| Actual prompts (owner requirement) | [catalogue](ai/PROMPTS.md), [coverage](ai/README.md) | Runtime files+actual live requests present; development/root/child transcript coverage partial |

Missing functionality is not repaired by adding documents. Remaining work is I2
semantic/query/failure breadth, I3 dependent reasoning+portability, I4 broad evaluation,
I5 complete packaging/clean-environment verification/defense. The original assignment
does not mandate48cases,48/48, a particular model or a particular UI framework;
historical proposals are not accepted requirements. Never present this audit as proof
that every assignment requirement has passed.

This audit added reviewer-facing README, database guide, manual E2E, linked examples,
an offline fixture and a prompt catalogue. No application behavior or live budget changed.
Full private chat/system/developer/reasoning history is not published or reconstructed.
