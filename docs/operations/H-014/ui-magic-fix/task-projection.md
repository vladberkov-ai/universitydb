# Received delegated task projection

Source: root native delegation to ui_magic_fix, H-014 v2 readiness workflow.
This is the received bounded worker assignment, not a replacement user prompt or
H-packet read context. No credentials/private source paths were supplied in this task.

> Implement ONLY minimal H014 UI magic defect repair. Own src/universitydb/ui.py
> (2 standalone ternaries 87/94), tests/test_readiness_ui_magic.py (or scoped existing
> test_i2_ui append if better), docs/operations/H-014/browser_ui.py ONLY new no help/
> no None + focused rows assertions as needed, docs/operations/H-014/ui-magic-fix/**,
> ADR013 addendum rationale if needed (coordinate writer finished; source fix finished).
> You are not alone, preserve others. Root Conductor owns goal/runtime, other final
> reviewer readonly. Actual independent architect BLOCK on c631 at success-db.png and
> success-visible.txt 164–190/487–513: st.json(results) if results else st.write(...),
> analogous step results, are bare ast.IfExp expressions; installed Streamlit magic
> wraps return of ternary → massive DeltaGenerator API help (success) or None (error),
> raw rows/traces still intact. Primary 2 explicit if/else statements fix. DO NOT
> disable magic globally/hide in test config/merely screenshot around it. BEFORE code
> write bounded plan/failing AppTest regression and record failure, preserve positive/
> empty/error messaging/no stale/correct rows/trace. AppTest must exercise actual magic
> path; inspect installed Streamlit source/existing AppTest patterns if needed.
> Extend actual browser harness to fail on DeltaGenerator/help dump/stray rendered None
> and verify focused typed rows visible while panel open, not just current question/
> run/outcome. Preserve original H013/browser331/c631 evidence immutable.
> User H014 v2 full offline scope read hand-off relevant, no live/count/credentials/
> ledger/cap/holds/push/vault/runtime IDs changes, no new deps. Run targeted test/ruff/
> mypy/compile, save distinct fail/pass + actual task projection redacting private
> prefix, cleanup plan/report with fallback inventory (no masking). Local explicit
> SCOPED commit authorized after checks; others docs commit currently 4b9c2e47 parent
> includes all product c631 unchanged. Do not stage unrelated reviews/clean outputs.
> Send new exact freeze SHA when source/tests/harness stable for final clean regression
> + browser; no source changes after freeze. Final independent reviews root will re-run;
> not self approve.

Follow-up received before freeze: do not require local browser launch; final actual
browser must use the new exact clean SHA after serialized full suite. AppTest failure/
pass plus static checks is sufficient for this scoped checkpoint. Root owns final
independent review and cleaner-plan review; no worker self-approval.
