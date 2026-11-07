# H-013 CP-D — actual dependent M1 and portability integration

Root's serialized final pipeline: **370passed in203.03s**, Ruff check, format31files,
mypy14sources, compileall and diff-check all exit0. [Source/verification receipt](cp-d-verification.json)
pins frozen product/test/resource hashes at CP-C base+current diff; committed-blob
comparison follows after local checkpoint. [Core receipt](core-cp-d.md), [domain receipt](domain-cp-d.md),
[UI receipt](ui-cp-d.md), [coverage/invariant audit](invariant-audit.md).

Actual dynamic provider/real compiled graph/SQLite tests prove top-course IDs → union
cohort IDs → all-course S1 student means, using actual validated upstream rows rather
than three fixed queries: F1 top2/cohort1/final95; F2 top1/cohort1,2,3/final95,80,50;
exact ties top1,2/union1,2,3/final90,90,null. Empty top/cohort never removes filters;
missing/wrongtype/truncated/oversized upstream blocks downstream calls; partial failure
keeps prior trace/step results but no complete answer. Shared repair/retry/call/SQL/
active-work and retained payload bounds remain whole-run. UI fixed proposals separately
prove all3 step results/bindings are visible, not dynamic sensitivity by themselves.

Library realDB/compiled graph mutation/zero/ambiguity/FK/type/schema-session isolation
and integrated same-core test run in the same full suite. First structured M1 and
portability captures remain unchanged with their real earlier source cutoff.
[Current CP-D manifest](m1-cp-d/manifest.json) now captures actual F1/F2/tie proofs,
matching fullJSONLs and portability from the exact root370-test process; its source
hashes match current files, core tree22af58a4aa2643d959b248fda604d7dd881ad79ab40a63cb43a675e7dd9e3d47.
Final post-cleaner capture must still use a **new** directory and actual source hashes.

Safety gaps found by boundary tests were fixed before this checkpoint with contract/
ADR notes first: count every currentraw/completeddeps/raw+adaptedstep/currentanswer copy
under131072-byte retained payload cap; signedSQLite64 primitive provider/raw integers
before saver/SQL; direct nonstring question rejection before saver. No broad overflow
masking, domain semantic change, call/SQL ceiling raise or accounting relaxation.
Initial impossible-integer resource fixture and shorthand-negative failures remain
in owning-lane receipts, not reclassified as passed. All7 baseline ledger/I1/locks
hashes match; original evidence/dependency lock preserved; no live/count/credentials/
spending/vault/remote/push changes.

Still pending: root-approved bounded cleaner after this commit, repeated tests/static,
final frozen-source M1/Library/allcase browser/proofs, independent APPROVE+CLEAR,
configured gate refresh, every invariant audit and final report/receipts/native
completion. Known initial-request-expiry replay trace visibility detail is explicitly
retained for independent review, not self-approved. This is not whole-goal completion,
real-model NL→SQL accuracy, production readiness, publication or owner defense.
