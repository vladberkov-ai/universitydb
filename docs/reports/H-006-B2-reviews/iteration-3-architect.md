<!-- BEGIN_ARCHITECT_REVIEW -->
# Architect review — H-006 B2, iteration 3

**Verdict: `approve`.**
**Scope:** documentary architectural proposal; separate Architect, not Critic.
**Blocking findings:** none. Mandatory corrections are not required until the next review. All architectural solutions remain **proposed**.

Further `P/` means `.omx/plans/H-006-B2/iteration-3/`.

## Summary

B2-R1 corrected: normative aggregate-level normalization matches non-null integer ResultSpec, and no records, no grades, and true zero grade have different, consistent normal outcomes. A full re-read of the packet revealed no new blocking inconsistencies; previous fixes to dependency binding, domain boundary, live/injected evidence and screen scope have been retained.

Approval refers only to the architectural consistency of documents. It does not involve the owner making decisions, performing product inspections, or authorizing sales.

## Proven foundation

Completely read by `P/plan-bundle.md`: **773 lines, 124495 bytes**, all **14 constituent documents**, including both changes mappings. The actual task/context, complete H-006-v5 handoff, current requirements/acceptance contract, accepted scope, local planning instructions, D2 report, manifest, baseline receipt, Planner3 completion observation and complete Architect/Critic reviews iterations 1–2 have been read.

Saved researcher/dependency-expert final texts read as **dated reused inputs from 2026-11-07**, not new studies or reviewer approvals. Their applicability to the unchanged proposed stack remains; no new specific research gap was discovered. Candidate pins are not considered installed, co-verified, or security audited.

### Fresh read-only checks

- **15/15** manifest entries iteration 3 matched in size and raw SHA-256.
- **14/14** constituent documents byte-equivalent to the corresponding sections of the bundle.
- Manifest entries iterations 1 and 2 saved: **13/13** and **14/14**.
- All **12 fenced JSON blocks** are parsed.
- Full M1 is statically checked: topological dependencies and references types are allowed without runtime values.
- Three Z-pairs checked for integer/non-null raw components, counts, normalized rows and empty reasons.
- The matrix contains **17 R + 8 U**.
- **25/25** current vault hashes coincided with `inputs-observed.json.current_sha256`.
- `omx quality-gates list --stage ralplan --json` returned `gates:[]`; it does not replace reviewers.
- Git root - current UniversityDB, branch `main`, HEAD **`8931d832d49311ac0d63c3a7a359b4293058da89`**; staging and the remotes list are empty.

Raw SHA-256 bundle before and after checks:

`e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`

The standard baseline receipt uses domain-separated lifecycle digest; raw hash manifest does not replace this digest. Native lifecycle observation Planner is read as evidence of the leader, not as an independently performed host audit by me.

The Original PDF was not re-decoded on its own: the attributed leader receipt of four pages was used; the current PDF hash is checked among 25 inputs.

## B2-R1: fix confirmed

### Root cause and elimination

The previous problem was at the SQL aggregate → typed result boundary: row-level COALESCE did not provide a non-null sum for a relation without rows.

Now `P/contracts.md:58,250–284` sets:

- `COALESCE(SUM(grade_units),0)` with integer zero;
- `COUNT(grade_units)` for denominator;
- `COUNT(*)` by scoped enrollment relation for enrollment count;
- ban on correcting nullable raw sum silently in formatter;
- distinguishing between scalar aggregate row count and the number of initial enrollments;
- no promise to automatically create missing GROUP BY groups.

Concrete examples agreed:

| Case | Raw components | Normalized outcome |
|---|---|---|
| Noenrollments | `[0,0,0]` | `average=null`, `no_rows` |
| Enrollment There is,grade NULL | `[0,0,1]` | `average=null`, `no_grades` |
| Real grade 0 | `[0,1,1]` | `average="0.00"`, `empty_reason=null` |

Typed DBResult and Answer are presented in full, without extending the nullable contract or heuristically recovering lost data.

**Verification boundary has also been corrected:** `P/test-plan.md:45,112,125,134–137` matches S10/N1–N3/V1 and separately requires:

- **DB-Z:** valid raw SQLite outputs/types to adapter;
- **UNIT-Z:** pure conversion of three typed messages and rejection of `sum_units=null`.

One test clearly does not replace the other. ADR006 fixes the same boundary: `P/ADR-OMX-006-schema-boundary-tracing.md:11–21`.

No new SQL probe was required. A documentary check has been carried out here; DB-Z/UNIT-Z remain **not-run**.

## Full architectural cross-check

| Region | Conclusion and evidence |
|---|---|
| **ERD and Subject Rules** | Course/Offering, mandatory connections, nonunique names with stable IDs, integer hundredths, NULL, all-retakes, equal weights, exact ties and all-semesters scope are consistent with fixtures. The rules are explicitly proposed, not attributed to PDF. `P/architecture-proposal.md:25–34`; `P/ADR-OMX-004-domain-semantics.md:5–24`. |
| **Static DAG → runtime binding** | `validate_plan` accepts typed symbolic references by declared outputs; `bind_results` requires completed/domain-validated/nontruncated data. `GraphState.results` contains the selected dependency rows, and the raw candidates are stored separately in the trace. Cycle/missing alias/type/truncation have specific stops before downstream calls. `P/contracts.md:54–61,64–201,229–236,247`; `P/test-plan.md:109–111`. |
| **Metric/unit/grain boundary** | The final ResultSpec registry and DomainResultAdapter eliminate the need to recognize University semantics in core by column names. Integer components preserve exact comparison of ties; Library count does not scale like grade. Shape validation is not passed off as proof of SQL semantics. `P/contracts.md:54–58,204–236,247`; `P/test-plan.md:112–113`. |
| **Clarification/resume and budgets** | Session-bound resume, replay/conflict/stale/expiry branches, side-effect-free interrupt and common counters through resume are consistent. Plan calls, transient retry and repair are included in the limit; sixth call is not hidden. `P/contracts.md:5–13,32–35,44–49`; `P/test-plan.md:59–70`. |
| **Safety/resources** | Read-only/authorizer/allowlists are separated from semantic oracle. Closed Binding array and placeholder checks are specific. Byte gate is not declared as an exact tokenizer; watchdog is not declared memory isolation. Residual memory risk is clearly preserved. `P/contracts.md:29–39,238–244`; `P/test-plan.md:74,114–116`; `P/production-considerations.md:13–17`. |
| **Portability** | Library has specific data, expected counts and zero-return variant; unchanged-core evidence plus DB/mock/live/UI checks are required. Arbitrary-dialect portability is not promised. `P/architecture-proposal.md:41–42`; `P/test-plan.md:76–84`. |
| **Live versus injected evidence** | EI1–EI3 are clearly injected, with provenance and zero paid calls; real-model denominator - 48 conversations, including continuation. N1–N4 require no-data outcomes rather than intentional model error. Unexpected failures are taken into account; disclosed examples are not called a ready-made sealed suite. `P/test-plan.md:87–92,118–127`; `P/ADR-OMX-007-verification-delivery.md:11–24`. |
| **Screen and full track** | SQL/bindings, typed DB rows and all same-run events/attempts are available from the screen. Success, clarification/resume, repair and terminal error have pass/fail; opaque ID and old rows of another run - fail. `P/architecture-proposal.md:22–23`; `P/test-plan.md:129–131`; `P/requirements-test-matrix.md:12,23`. |
| **Delivery and requirements** | All R/U are linked to the corresponding future DB/app/live/manual/public/defense/provenance evidence. Local commit does not close R-15; historical U-07 is not assigned to B. `P/requirements-test-matrix.md:3–33`. |
| **Implementation and production** | The first real vertical slice precedes further expansion. Owner decisions, budget, compatibility and public authority are included in future gates. Five production topics are covered without the production-ready statement. `P/implementation-plan.md:5–26`; `P/production-considerations.md:3–17`. |

### Independent arithmetic reconciliation of fixtures

Integer/rational recalculation of document strings confirmed:

- S1–S6: sums hundredths `50000/35000/40000/25000/26000/16000` and corresponding counts/averages.
- M1/F1: top `{2}`, cohort `{1}`, answer `95.00`.
- M1/F2: top `{1}`, cohort `{1,2,3}`, answers `{95.00,80.00,50.00}`.
- M1/tie fixture: top `{1,2}`, cohort `{1,2,3}`, answers `{90.00,90.00,null}`.
- The proposed token-rate arithmetic is `$1.056`; it is not a measurement of value or a spending permission.

This is **document testing, not SQL/application/E2E tests**.

## Deliberate principles and risks

Five principles, three drivers, meaningful alternatives and three pre-mortems are present: `P/architecture-proposal.md:5–14,44–49`. The extended test plan covers unit, actual DB, mocked graph, live NL, UI E2E, observability, manual/public/defense checks.

**No new violations of principles were found.** The previous B2-R1 contradiction was eliminated without expanding the architecture. The principle of “computes the database, not the model” remains: SQL returns the components being checked, the domain adapter performs accurate normalization/comparison, rather than making up numbers.

## Advisory observations - optional fixes

1. **Keep the final size of the registry during implementation.** ResultSpec solves specific units/grain/dependency problems; turning it into a generic SQL compiler would violate minimality. New metrics should have their own domain tests, not heuristics in core.
2. **Do not increase the level of evidence when packaging.** Candidate pins, documentary walkthroughs, fixture arithmetic and this approval cannot be renamed compatibility, executed E2E or production evidence.
3. **Keep the proposed order I0→I1.** Credentials, budget, owner acceptance, SDK smoke and public authority remain future gates, but are not independent blockers of documentary B.

Withdrawn `27/30` is not restored. The new `48/48` remains clearly **proposed**, not a statistical guarantee and not a replacement for mandatory requirements.

## Trade-offs and consensus to be added

**Antithesis - strongest steelman:** For a small educational demonstrator, free read-only SQL, an independent oracle and a transparent trace could be sufficient. A redundant typed IR increases implementation and may delay the first true end-to-end launch.

**Tradeoff tension:** free result columns are easier to generate, but they force downstream to guess units/grain/NULL/dependencies. A strong contract eliminates guesswork but requires careful negotiation of SQL edge cases.

| Option | Plus | Price |
|---|---|---|
| Free SQL/result shape | Less adapter code | Ambiguous downstream semantics |
| Full typed query compiler | Stronger structural check | Excessive scope and expressibility limitation |
| **Final ResultSpec + domain adapter** | Explicit boundaries while maintaining true SQL generation | Small registry and mandatory boundary tests |

**Synthesis:** the current package implements a sufficient compromise: finite shapes, two-phase references, exact arithmetic and now correct empty-sum normalization. An independent semantic oracle remains necessary; runtime shape and readonly checks do not prove the correctness of arbitrary SQL.

## Stop condition

**Architect review completed: `approve`, blocking findings 0.**

The next step of the leader is to check the native completion of this agent, then transfer immutable iteration 3 and this full review to a separate Critic3**, after which configured gates. My verdict does not replace Critic, lifecycle closeout or owner acceptance.

Native provenance/completion, supported terminal closeout, `active:false`, lack of execution handoff, prompt packaging and commit B remain the responsibility of the leader. I don't assign them.

Files, Git, state, IDs, tracker and Obsidian did not change; didn't let the kids in. Application tests, SDK compatibility, live eval, UI execution, public delivery and owner rehearsal - **not-run**. There is no Execution authorization.
<!-- END_ARCHITECT_REVIEW -->
