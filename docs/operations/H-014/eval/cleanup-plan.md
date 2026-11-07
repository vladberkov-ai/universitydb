# Bounded harness cleanup plan

Scope: new tools/eval, tests/test_eval_harness.py and H-014 eval data/docs only.
Before cleanup, regression-lock payload/oracle separation, exact strict typing, duplicate/missing/unknown records, fixed denominator, noncompleted outcomes and safety failures. Then remove dead/duplicate code, simplify names/error handling and rerun targeted tests/static checks. No compatibility fallback, product prompt tuning, dependencies or product edits. Validation errors must propagate; no silent skip/default-to-pass. UI review N/A. Independent final approval belongs to root's reviewer lanes, not this author.
