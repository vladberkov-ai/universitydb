# Bounded UI magic repair plan

Independent architect found Streamlit magic rendering the return of bare conditional
expressions in the DB and adapted-results panels. Scope: two statements in ui.py,
actual-magic AppTest regressions, and browser assertions. Preserve existing H013 and
all earlier H014 evidence; new attempts go here or root-owned fresh run directories.

1. Add/run regression against unchanged source: positive typed rows, empty rows,
   refusal after success (no stale rows), complete same-run trace, no help/None.
2. Replace only the two bare expression ternaries with explicit if/else statements.
   Do not disable magic, suppress output or modify test Streamlit configuration.
3. Strengthen browser checks for actual visible focused rows and no help/stray None.
4. Run regression/UI suites, lint/typecheck/compile, review bounded diff and checkpoint.

Fallback inventory: existing no-DB/no-adapted-result messages are grounded explicit
fail-safe presentation, not masking fallbacks; retain and test them. Browser executable
selection remains the existing explicit/PATH/managed boundary, unchanged. No new fallback,
exception suppression, dependencies, hidden panels or global magic setting is permitted.
Root owns fresh independent review and clean-checkout/browser final validation.
