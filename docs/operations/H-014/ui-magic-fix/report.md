# H-014 bounded UI magic repair — candidate evidence

## Result and root cause

Replaced only two bare conditional-expression rendering statements with explicit
`if/else` blocks in `ui.py`. Streamlit 1.67.0's installed `magic.py` transforms bare
expressions inside functions; `magic_funcs.transparent_write` invokes `st.write` on
their return values. `st.json` returns a DeltaGenerator (rendered as API help), while
`st.write` returns None (rendered as a stray `None`). Explicit statements retain
normal magic configuration and avoid rendering the return values at the source.

Actual AppTest uses the application file, not an imported renderer/mock: initial
regression inventory in pre-fix-pytest.txt recorded 1 failed/1 passed. After correcting
the assertion to Streamlit's installed `help_info` element and recognizing backticked
None, pre-fix-pytest-complete.txt recorded **3 failed**. Source was unchanged through
both failure captures. Failure assertions detect help, clarification empty-panel None,
and refusal empty-panel None independently.

## Verification and exact limitations

- Post-fix actual-magic + existing University/Library/clarification/M1 UI suite:
  **15 passed in 6.49s** (post-fix-pytest.txt).
- A later duplicate run concurrent with the slow single-file mypy check recorded
  **9 failed / 6 passed in 200.02s** (post-fix-pytest-final.txt); M1 failure payloads
  explicitly report SQL_TIMEOUT / database worker watchdog termination. Other failures
  were absent-success assertions. Resource contention is an inference, not proven
  cause. No watchdog/test timeout ceilings were modified.
- After that mypy process exited, the same scoped tests recorded **15 passed in 6.00s**
  (post-fix-pytest-serialized.txt), without source/behavior changes. Preserve all runs.
- Scoped ruff check/format, source mypy, compileall and git diff-check passed; see
  static-checks.txt, final-static-checks.txt and standard-mypy.txt.
- Browser harness now asserts no DeltaGenerator/help or stray None, expanded/visible
  focused panels, actual raw columns and row values, adapted dependency rows and empty
  messages. JSON null/boolean checks use JSON rather than Python display spelling.
  Existing run/question/outcome/full downloaded same-run trace checks remain.
- Local browser attempt 1 failed before launch: local product venv lacks Playwright.
  Attempt 2 used the existing separate tool site-packages/browser but sandbox socket
  creation raised EPERM before server/browser launch. Neither is product acceptance
  evidence; no server/browser was started, and no browser success is claimed here.
  Root owns actual browser evidence from the exact clean candidate SHA.

## AI slop cleaner bounded pass

Plan predates source edits; root reviewed it separately (plan-review.json).
Fallback inventory: retained explicit no-DB/no-adapted-result messages are grounded
fail-safe presentation; neither suppresses traces/errors. No new fallback, global
magic override, hidden/cropped content, dependency or abstraction. Dead-code,
duplication and naming/error-handling passes found no additional in-scope action;
test reinforcement adds actual-magic and visible browser evidence checks.

No accepted architecture/metric/Sol/budget changes. Original historical evidence,
monetary ledger, locks and other agents' changes are outside staging scope.
No live/count/credential loading/vault write/push performed. Root owns final
independent code-reviewer/architect verdicts, clean full integration run and offline
acceptance. This checkpoint is a testing candidate, not independent self-approval.

Evidence logs replace local canonical checkout and pytest temporary-root prefixes
with placeholders and normalize trailing whitespace; no private credential paths or values were read or exported.
