# ADR-OMX-008 — H-007 reversible I1/S6 implementation choices

Date: 2026-11-07. Owner: repo. Status: **adopted provisionally for I1 only**, by the new explicit H-007 user task. ADR003–007 remain proposed; closed Advisory is not execution authority.

## Context and boundary
H-007 authorizes one vertical slice: explicit four-filter question → actual compiled LangGraph → separate model plan and SQL proposals → validated read-only SQLite → deterministic answer → JSONL and Streamlit. F1 has four students, two teachers, three courses, five offerings, eight enrollments; S6 selects Bea2/DB1/Kim10/S1, offerings1/5, grades6000/10000. Independent oracle is sum16000/count2/enrollments2, average `80.00`. Runtime SQL and DB results must not be hardcoded from the question.

I2–I5, full multi-step compiler, Library, clarification/resume, full 48/48 live evaluation, production deployment and defense are not implemented by this decision. Unknown/unsupported shapes fail explicitly. No all-semesters default, retake/tie/weight policy beyond explicit S6 is adopted.

## Alternatives and decision
| Choice | Alternatives | Rationale and cost |
|---|---|---|
| SQLite + direct LangGraph + Streamlit + local JSONL | PostgreSQL/API/LangSmith; CLI-only | Small local explainable service with required visible path; own trace completeness and single-user limits, not production isolation. |
| Installed Python3.12.3 | Fetch proposed Python3.13 | Existing interpreter meets researched candidate package minimums; avoid unrelated runtime upgrade. Compatibility still requires real lock/install/import tests. |
| F1 normalized schema; grade integer hundredths, NULL separate | float grades; merged course/offering | Exact sum/count, explicit semester/course/teacher/student scope, avoids floating arithmetic and identity conflation. This does not accept every proposed domain rule. |
| S6-only typed ResultSpec registry and domain adapter | universal compiler; identifiers in graph core | Closed versioned contracts, exact scalar `u.grade_mean.v1` with keys[]; core carries descriptor and calls domain adapters without University table identifiers. Other shapes are unsupported, not stubs advertised as implemented. |
| Separate plan + SQL provider calls; deterministic formatter | fused call; LLM numeric answer | Matches scoped B contract and keeps arithmetic in SQLite/domain adapter; two calls have explicit budgets/trace. |
| SDK adapter candidate, injectable only for tests | hidden canned fallback; automatic alternate model | Missing credentials/configuration yields error before network. Offline injected profile is labeled and cannot count as live accuracy. No model selected or paid call authorized. |
| Read-only URI + SQLite compiled authorizer + constrained SQL validation + bound values + worker watchdog | regex-only guard; unrestricted execution | Fail closed on statements/functions/schema/scope outside supported path; test actual denial and unchanged DB hashes. Parser/tool additions require narrow justification, not speculative framework. |

## Operational contract for implemented path
Closed typed proposals/results; single SELECT statement, allowlisted identifiers/functions, parameter binding, no writes/DDL/ATTACH/PRAGMA/extensions. Explicit four-filter scope required; safe SQL is not proof of NL correctness. Model output/SQL/input byte bounds and typed component consistency are independently checked.

B bounds apply to the path: provider timeout15s, SDK retries0, at most one application transient retry with1s backoff and one recoverable SQL repair; no unsafe-SQL repair; total provider calls≤5, SQL attempts≤4, run active time≤60s; per-call input accounting≤12000/output≤2000 tokens; encoded input≤12000 bytes; SQL≤8000 bytes/chars; bindings≤100/8192 bytes; result≤100 rows/64KiB, retained≤128KiB, trace≤1MiB. DB progress timeout2s, lock wait≤0.5s, worker kill≤3s. No hard memory sandbox or exact pre-call tokenizer guarantee is claimed.

Same-run trace includes input, actual node starts/ends, all attempts, proposal SQL/safe params, typed DB rows, output/error, usage/timestamps/seq and terminal event. Trace failure cannot yield untraced success. UI clears previous answers on new/error runs and exposes SQL/DB/full trace. Local synthetic data and loopback only.

## Live gate
Concrete model, account access, current rates and explicit total smoke/retry monetary cap are absent at this checkpoint. Presence of a credential is not authorization. Zero paid calls. Before dispatch reserve conservative projected spend including retries, reconcile usage, retain uncertain spend on failures, and stop before cap; no costly fallback. Until approved, offline work proceeds and I1 remains incomplete.

## Consequences and verification
Reversible first implementation, deliberately not full project acceptance. Required evidence: reproducible lock/install/import; compiled graph+real DB offline scripted runs; F1 constraints/FK/ranges/NULL; independent S6 and four filter-discriminating mutations (Bea negative-control rows differing in exactly one course, teacher or semester with non80 grades; omitted-filter raw queries checked against manual components, not merely validator rejection); strict invalid proposals; actual unsafe SQL/timeout and trace failures; full offline suite/lint/type/compile; cleaner and independent code-reviewer+architect. Then actual approved model S6 plus changed input/data with independently different expected, browser screenshot of expanded SQL/DB/full trace and failure. AppTest alone is not browser/live E2E.

U-01 prompts/coverage remain explicitly partial; U-04/R-13 rationale captured here and future substantive changes need new evidence; R-15 public delivery remains open (remote/push forbidden). Review triggers: expanded scenarios, a different provider/dialect, real data, multi-user exposure, durable resume, semantic contradictions or failed safety/compatibility checks.
