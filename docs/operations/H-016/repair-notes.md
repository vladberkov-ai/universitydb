# H-016 repair implementation notes

Scope: shared adapter identity parsing and directly affected adapter guards;
no provider/API/count/credentials, money, historical-evidence or lifecycle writes.
ADR015 was recorded before implementation. Source changes wait for root's CP1
regression-first checkpoint confirmation. Tests and final results are appended
here after execution; root owns campaign integration and final verification.

## Pre-code cleanup/repair plan and independent design review

1. Lock the boundary with natural Agent-entry regressions before source edits:
   `test_h016_resolution_edges.py` adds 28 independent punctuation/case/repeated-
   identity and masked-unknown variants; pre-fix **8 failed, 20 passed**, retained
   in `repair-edges-before.txt`. Root's separate matrix is independently owned.
2. Inventory existing fallbacks: absent entity mentions intentionally mean all;
   explicit malformed/unknown mentions may not take that path. Existing global
   name lookup and catalog ambiguity/choice logic remain, but every extracted
   mention must validate before selection. No new permissive fallback.
3. Repair one smell: inconsistent identity grammars in numeric extraction and
   unknown-name detection. A small shared parser/helper owns ID-marker handling;
   no blanket `ID` skip, new dependency, eval alias or provider workaround.
4. Rerun new/old boundary and graph tests, inspect the focused diff, and remove
   duplication/debug residue without changing unrelated behavior. Final cleaner
   can be a documented no-op if no actionable smell remains; rerun regressions
   after the review.

Independent root design review (native message, 2026-11-08): root read ADR015 and
approved its bounded design pending the CP1 regression-first checkpoint. Source
edits remain prohibited until root confirms that checkpoint. This is design
review, not the final independent code/architecture verdict.
