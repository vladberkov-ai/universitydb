# UniversityDB defense — speaker guide

Use slides 1–22 for the main talk; slides 23–24 are Q&A appendices. All examples distinguish offline fixtures from live evidence.

## 1. University Database + LangGraph QA Agent

Open with the engineering objective: an inspectable local natural-language QA service. The current repaired candidate is verified offline, but broad real-model acceptance is pending. Present the historical live failure transparently and explain how it drove a general repair. Suggested delivery: 18–22 minutes, then a 5–8 minute offline demo. This deck describes the publication after H016, not a new live campaign.

Sources: [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md)

## 2. The assignment: accurate, explainable database answers

Explain the source assignment: clean university schema, SQL generated through a real LangGraph agent, complex queries, modular schema-specific logic, full run traces, error handling, tests and public delivery. A compact local system is acceptable; the requirement is explainability and correctness. Do not claim that all natural language or all SQL dialects are supported.

Sources: [docs/assignment-status.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/assignment-status.md), [docs/database.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/database.md)

## 3. Development followed three delivery blocks

A and B prepared repository and architecture. I1 established one working four-filter mean query. The accepted combined plan then grouped I2/I3 functionality, I4 and verification I5 readiness, and final delivery/defense. H015 was completed as measurement even though quality failed. H016 closed the repair loop offline. Completion is scoped: it does not automatically mean acceptance of the whole product.

Sources: [docs/reports/H-013-I2-I3-offline.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-013-I2-I3-offline.md), [docs/reports/H-014-readiness-offline.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-014-readiness-offline.md), [docs/reports/H-015-full-live-eval.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-015-full-live-eval.md), [docs/reports/H-016-scope-repair-offline.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-016-scope-repair-offline.md)

## 4. The workflow separated decisions, execution and review

The owner sets scope, permissions and semantics. The chat maintains project memory and standalone handoffs. CLI OMX implements within a bounded ultragoal and records checkpoints. Independent code and architectural review challenge the result. This was not one unchecked batch: failed candidates and preliminary BLOCK/REQUEST CHANGES reviews remained visible. Operational workflow state is not a Git commit. Native token usage is not product API spending.

Sources: [docs/ai/README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/ai/README.md), [docs/operations/H-016/prompt-receipt.json](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/prompt-receipt.json), [docs/operations/H-016/reviews/code-final.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/reviews/code-final.md)

## 5. The schema models offerings, not just courses

A course is a stable subject. An offering ties it to a teacher, semester and section. Enrollments connect students to offerings, allowing repeat enrollments across different offerings. Primary keys, foreign keys, nonblank names, grade bounds and unique offering identities are enforced. All data is synthetic. University seed: 4 students, 2 teachers, 3 courses, 2 semesters, 5 offerings, 8 enrollments.

Sources: [resources/schema.sql](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/resources/schema.sql), [resources/seed.sql](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/resources/seed.sql), [docs/database.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/database.md)

## 6. Grade semantics are explicit and deterministic

Explain why raw SQL averages alone can conceal semantic choices. Grade units are integer hundredths; the mean equally weights graded enrollments across selected offerings and retakes. NULL is missing, never zero. Absent filters include all applicable dimensions and semesters. Exact top ties are retained before rounding. These choices were accepted before implementation and are tested independently.

Sources: [docs/database.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/database.md), [docs/adr/ADR-OMX-012-I2-I3-offline-contracts.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/adr/ADR-OMX-012-I2-I3-offline-contracts.md), [src/universitydb/domain.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/domain.py)

## 7. A shared core sits between the UI and domain adapters

The UI owns user interaction and displays evidence. Agent orchestrates the real compiled StateGraph. Typed contracts prevent free-form model output from becoming executable state. The provider returns proposals; it does not own execution authority. Domain adapters provide schema and metrics. SQL policy and the read-only worker enforce execution boundaries. Library demonstrates schema portability within SQLite, not universal database support.

Sources: [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py), [src/universitydb/contracts.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/contracts.py), [src/universitydb/domain.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/domain.py), [src/universitydb/library.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/library.py)

## 8. The graph makes control flow explicit

This is an actual StateGraph compiled with InMemorySaver, not a diagram wrapped around a single prompt. Input/schema/scope lead to planning and plan validation. Each step binds earlier results, generates and validates SQL, executes, and inspects its typed result. Clarification interrupts and resumes the same run. A bounded repair returns to generation; the per-run ceilings still apply. Errors terminate explicitly, and answer formatting is deterministic.

Sources: [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py)

## 9. Typed contracts constrain model proposals

A plan is a bounded dependency graph of registered operations, not an unrestricted agent program. The accepted ResultSpec defines columns, types and semantics. SQL proposals carry text and typed parameters, with validation before execution. Actual results are inspected and adapted before dependencies are materialized. The state retains completed results, resolved references, counters and identity, which makes causal debugging possible.

Sources: [src/universitydb/contracts.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/contracts.py), [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py)

## 10. Dependent questions use actual upstream rows

Use the M1 example: identify the top course in S1, derive its enrolled students, then compute their means across all S1 courses. The final query must not keep the top-course filter unintentionally; it uses the derived student IDs and the requested S1 scope. Tests mutate fixtures and introduce ties/empty sets, which demonstrates dependency sensitivity beyond one happy fixture. Demo fixture yields course2, student1 and95.00. This is a fixture example, not a general hardcoded answer.

Sources: [tests/test_i3_dependencies.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/tests/test_i3_dependencies.py), [docs/manual-e2e.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/manual-e2e.md), [src/universitydb/contracts.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/contracts.py)

## 11. Clarification preserves identity and scope

The seed intentionally has two Alex students with distinct IDs. The server presents catalog-backed choices rather than asking the model to guess. The same run resumes after selection, before generated SQL has executed. The in-memory saver survives Streamlit reruns within the process, not server restarts. Limits are two clarification pauses and fifteen minutes. Foreign, expired or replayed continuation cannot silently change scope.

Sources: [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py), [tests/test_i2_ui.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/tests/test_i2_ui.py), [docs/manual-e2e.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/manual-e2e.md)

## 12. One model, distinct planning and SQL budgets

This slide documents the implemented project profile, not a recommendation or claim about current API pricing. Exact configured model is gpt-6.1-sol on default tier. Planning uses high effort; SQL and repair use medium. Strict JSON schema and Pydantic validate proposals. Deterministic formatting avoids an additional model call that could invent prose. No model fallback and no LLM judge. Budgets bound calls/time; they do not guarantee semantic quality.

Sources: [src/universitydb/config.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/config.py), [src/universitydb/llm.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/llm.py), [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md)

## 13. Execution safety is layered

Prompt instructions alone are insufficient. The application validates SQL structure, allowed tables/functions and parameters; a separate read-only SQLite worker enforces database access and time bounds. SQLite DELETE journal mode is supported; WAL and concurrent writers are outside the current design. Monetary accounting uses stable locking and retained holds, with unknown usage stopping dispatch. A safe SELECT can still answer the wrong question, so semantic oracles and live evaluation remain necessary.

Sources: [src/universitydb/sql_policy.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/sql_policy.py), [src/universitydb/db_worker.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/db_worker.py), [src/universitydb/llm.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/llm.py)

## 14. A trace explains both answers and failures

Walk the interviewer through one downloaded JSONL trace. Show the original input and run ID, resolved scope and registered plan, generated SQL and parameters, raw rows, adapted results and dependency bindings, then the final answer or typed error. Use the same ID throughout. For repair, compare both attempts; for a scope failure, show that no provider call occurred. Trace failure cannot be relabeled as success. Raw secrets and headers are excluded from public evidence.

Sources: [src/universitydb/tracing.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/tracing.py), [src/universitydb/ui.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/ui.py), [docs/manual-e2e.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/manual-e2e.md)

## 15. Verification separates mechanics from model quality

815 is the total offline suite, not the number of live questions. 157 oracle checks independently use SQLite and precise arithmetic. AppTest is a UI testing surface; the eight browser captures are actual rendered UI states with trace identity checks. Clean archive reproduction reused the installed locked virtual environment, so do not claim a fresh dependency download. Independent review and preservation add evidence but are not substitutes for a new live evaluation.

Sources: [docs/reports/H-016-scope-repair-offline.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-016-scope-repair-offline.md), [docs/operations/H-016/native-strict-closeout.json](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/native-strict-closeout.json)

## 16. The live experiment exposed a product defect

The H015 campaign collected 48 terminal conversations from 24 known questions repeated twice. Thirty-eight failed in scope resolution before calling the model. Ten succeeded, requiring20calls. The observer initially gave2/48 because it inferred nullability from sample values; eight correct numeric answers were false negatives. A separately reviewed correction changed only type labels. Do not call this an untouched holdout, a pure-model accuracy estimate or a measurement of H016. The44/48 and7/8/category threshold was not met.

Sources: [docs/reports/H-015-full-live-eval.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-015-full-live-eval.md), [docs/operations/H-015/corrected-assessment-v2/score-v2.json](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-015/corrected-assessment-v2/score-v2.json)

## 17. H016 repaired the shared resolver

The defect was systematic: entity ID markers and requested ID projections were interpreted as names. The first failure often masked later filters. Nineteen repeated cases had thirteen distinct strings, so avoid inflating the defect count. The repair introduced typed, role-owned spans and catalog validation. Independent negative controls caught name conflicts, missing IDs, numeric-looking names, unsupported comparisons and cross-role collisions. A later full run caught quantified listing forms missed by focused tests. Three product modules changed, with no runtime prompt or dependency addition.

Sources: [docs/operations/H-016/root-cause-report.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/root-cause-report.md), [docs/adr/ADR-OMX-015-H016-scope-resolution.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/adr/ADR-OMX-015-H016-scope-resolution.md)

## 18. Library tests the portability boundary

DB-agnostic here means isolating schema-specific logic from the orchestration core. Library uses Readers, Books and Loans; counts only unreturned loans and retains readers with zero open loans. The same Agent, provider, safety, tracing and UI are used. Adding a schema still needs a descriptor, registered metrics, adapters and tests. This is not automatic support for arbitrary databases or SQL dialects.

Sources: [resources/library/schema.sql](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/resources/library/schema.sql), [src/universitydb/library.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/library.py), [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py)

## 19. Key design trade-offs

Discuss these as implemented choices with practical rationale, not universal best practices. SQLite keeps the assignment reproducible but limits deployment assumptions. A bounded graph makes failure states inspectable at the cost of unrestricted agent flexibility. Catalog grounding avoids guessing IDs but created lexical brittleness that needed NL regression coverage. A deterministic answer avoids an extra generative failure surface. In-memory checkpoints keep local demo complexity low but do not survive restart.

Sources: [docs/adr/README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/adr/README.md), [docs/adr/ADR-OMX-015-H016-scope-resolution.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/adr/ADR-OMX-015-H016-scope-resolution.md), [docs/plans/production-considerations.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/plans/production-considerations.md)

## 20. Production work remains explicit

Do not claim this unauthenticated local synthetic-data app is production ready. The implementation includes strong bounded controls for the assignment, but production needs authentication, tenant permissions, isolated execution, persistence, quotas, trace retention and monitoring, and a deployment/rollback strategy. Semantic regression and live quality tracking remain necessary even after infrastructure hardening. No production deployment was performed.

Sources: [docs/plans/production-considerations.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/plans/production-considerations.md), [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md)

## 21. Current delivery and next acceptance gate

The public source checkpoint for this presentation is f43c2b1, which packages H015/H016 and refreshed README/E2E/prompts. The exact executable tested is58f2fe9. A later documentation commit is not another test run. Current offline implementation and repair are complete; a new authorized real-model evaluation is still required. Known evaluation questions should be disclosed as regressions and separated from independently authored fresh evidence. Final acceptance and owner rehearsal are not implied by native workflow completion.

Sources: [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md), [docs/operations/H-016/next-live-plan.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/next-live-plan.md)

## 22. Demo: inspect one run, then change the scenario

Use the README isolated offline UI instructions and the exact six-step fixture sequence in docs/manual-e2e.md. The sequence is consumed in order within each dataset session: simple mean, Alex pause/resume, M1, repair, refusal, then Library. Say clearly that provider proposals are injected; the graph and SQLite execute for real. In H016 automated browser, a filtered Library case is added before the global case. Do not mix these fixture sequences. Do not enter arbitrary questions into a fixed scripted queue and present the result as model interpretation. No new live calls are authorized.

Sources: [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md), [docs/manual-e2e.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/manual-e2e.md), [docs/operations/H-016/browser_ui.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/operations/H-016/browser_ui.py)

## 23. Code walkthrough map

Use this slide as an appendix or jump to the files during questions. Start at Agent._compile for the orchestration; show the typed proposal contracts and domain-owned ResultSpec. For the H016 fix, show domain_support role/ID parsing and its independent natural-scope tests. For execution safety show sql_policy plus db_worker. The repository README links all deliverables, source decisions and actual traces.

Sources: [src/universitydb/agent.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/agent.py), [src/universitydb/contracts.py](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/src/universitydb/contracts.py), [README.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/README.md)

## 24. Questions to be ready to defend

Suggested answers, not claims of a completed rehearsal. Why LangGraph? Explicit state transitions, inspectable execution and interrupt/resume. Why a deterministic resolver? Catalog-grounded validation and bounded semantics, with a documented lexical trade-off. Does815pass prove accuracy? No; injected proposals test mechanics. What did the live test teach? Pre-provider parsing and the observer were both failure sources; preserved evidence separated them. What is next? A prospectively frozen live check of the repaired candidate, with known and fresh questions distinguished.

Sources: [docs/reports/H-015-full-live-eval.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-015-full-live-eval.md), [docs/reports/H-016-scope-repair-offline.md](https://github.com/vladberkov-ai/universitydb/blob/f43c2b1158f480e59f1a3d9cc33c3f632c91a747/docs/reports/H-016-scope-repair-offline.md)
