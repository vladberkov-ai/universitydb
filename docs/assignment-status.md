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

## H-013 — current authorized work, not an implementation verdict
The current task combines I2+I3 offline: all University classes/filters, actual checkpoint clarification/bounded errors, typed step contracts, actual-result-dependent M1 and early Library on the same core, full trace/UI/tests/docs. See [whole brief](plans/I2-I3-offline-brief.md), [contract/full R/U mapping](plans/I2-I3-offline-contract.md), [ADR012](adr/ADR-OMX-012-I2-I3-offline-contracts.md). CP-A–E are internal verified local checkpoints, not further owner approvals. Previous I1 audit and H-011 partial/history are preserved, not relabeled complete. Offline scripted-provider results do not establish real-model accuracy; current implementation proof remains pending. I4+verification-I5, publication and defense are later blocks, not offline completion conditions. Live/count/credentials/spending changes/push prohibited. R10 production explanation remains maintained with explicit risks and implemented/future separation; final R15/owner-defense obligations remain open.

### H-013 verified checkpoint cutoff, not final acceptance
CP-C `b9f2eb66e20a3148485da2af62eaa4fc9d02d0cb` verifies real in-memory
clarification/resume, University breadth/typed results/failures, early Library and
trace/UI with311offline tests/static checks; [source identity and caveats](operations/H-013/cp-c-commit-receipt.json).
Independent actual-result M1/same-core proof and final whole-offline cleaner/browser/
review/gates are still CP-D/E at this cutoff. [Invariant audit](operations/H-013/invariant-audit.md)
and current requirements mapping retain every R/U obligation; production notes
explicitly separate implemented versus future. Offline scripted tests do not close
real-model NL accuracy, I4+verification-I5, final publication/push or owner defense.

### H-013 repaired-candidate current verification cutoff
The operative local offline candidate is `f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0`:410
offline tests121.29s plus Ruff/format32/mypy14/compile/diff passed. Earlier CP-C/CP-D
cutoffs above remain history, not the present capability limit. Actual same-process
M1 F1/F2/tie/checkpoint-resume and Library portability are in the final manifest;
request identity/TTL/owner-trace/DELETE-journal/DB availability repairs respond to
actual independent blockers, not waived by the earlier383pass. Final frozen-source browser passed six classes/seven captures; fresh
independent code-reviewer APPROVE and architect CLEAR received; root native COMPLETE/strict PASS (13/13) now confirmed. No real-model
NL accuracy/live/count/credentials/spending/push claim; I4+verification-I5/publication/
defense remain later.
[Exact-process structured proofs](operations/H-013/m1-final/manifest.json).
