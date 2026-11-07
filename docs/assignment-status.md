# Assignment deliverables and verification status

Updated2026-11-08 for the published I2+I3 offline checkpoint. The four-page assignment
is represented below; its private source PDF is not redistributed. Development
prompt preservation is an additional owner requirement.

| Requirement | Delivered evidence | Remaining boundary |
| --- | --- | --- |
| Students/teachers/courses/names, semesters/offerings/enrollments/grades | University schema+seed under resources/; integrity/oracle tests | Synthetic data |
| LangGraph NL→SQL→DB→readable answer | src/universitydb, historical I1 live proof, H-013 compiled-graph tests | Broad current real-model accuracy not run |
| Aggregates/JOIN/filters/dependent questions | Q1–Q12,16filter scopes,M1 F1/F2/tie actual refs | Offline verified; live evaluation pending |
| Schema-independent core | Library resources/adapter and final same-core proof | SQLite only |
| Full traces and debugging | examples/,H-013 m1-final and browser JSONL/screenshots | No fabricated live records |
| SQL/data/empty/ambiguity failures | Typed validation, clarification, bounded repair, negative/replay tests | Runtime safety is not full semantic proof |
| Query/JOIN/NL-SQL/E2E tests |410offline tests,157oracle,AppTest,actual browser | Clean-environment readiness and expanded live eval pending |
| Modular code | agent/contracts/db/domain/library/provider/tracing/UI | Local process design |
| Production discussion | plans/production-considerations.md | No production deployment claim |
| Design decisions and rationale | adr/README.md; ADR008–012 scoped decisions | Earlier ADR003–007 proposals remain labeled |
| Examples and execution traces | ../examples/README.md and H-013 report | Offline/live provenance separate |
| Public code/schema/seed/tests/docs/prompts | This repository and root README navigation | Publication is not full readiness acceptance |
| Interview explanation/defense | Artifacts available for walkthrough | Owner rehearsal pending |
| Actual prompts, RU/EN reader bundles | ai/PROMPTS-RU.md,ai/PROMPTS-EN.md,ai/README.md | Selected source coverage; not complete private transcripts |

[H-013 delivery report](reports/H-013-I2-I3-offline.md) remains the detailed source:
tested product f4b775ce2680f6282ebd2f9c449d1f27a2c85ee0, APPROVE/CLEAR, native
COMPLETE/strict PASS13/13. Historical partial cutoffs remain in Git/reports; they do
not describe today's functionality. H-014 now audits readiness/clean reproduction and prepares the separate live
decision; see the current section below. Prior publication authority is exhausted
for this stage: new push and live calls are forbidden. Defense follows readiness.

## H-014 v2 current readiness cutoff

[Report](reports/H-014-readiness-offline.md) is the authoritative current bounded
offline-readiness status, distinct from historical H013 product410tests/157oracle.
Named-target scope-loss defect repaired with14regressions; frozen candidate
331eb5a61648bccb7fa66eecb58d9cc284eda2a0 adds readiness/eval harness33tests.
Final corrected-candidate clean full regression/browser/independent reviews are pending.
R01–14/U01/U03–06 are mapped in the report; R15 new publication awaits authority,
R16/17 owner defense deferred, U02 deadline unknown. I4 real-model/I5 live acceptance
not-run: proposed24×2/48cases and44/48,≥7/8/category await approval, not an accuracy
claim. [Protocol](plans/H-014-live-eval-protocol.md), [budget](plans/H-014-live-eval-budget.md).
