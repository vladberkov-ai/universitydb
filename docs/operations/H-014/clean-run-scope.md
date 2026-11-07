# CP-R2/R3 verifier scope and evidence contract

The delegated verifier received ownership of clean-run/browser evidence and portable
readiness scripts only. Product fixes, workflow lifecycle, commits, documentation
bundles and final integration remain leader-owned. The task projection covers:
tracked-only disposable local clone; fresh frozen environment; isolated caches and
runtime; University and Library initialization/repeat-init; full tests/static/oracle;
actual compiled graph groups/top, M1 mutation/ties, clarification, repair, terminal
errors; fresh actual offline browser traces/screenshots; process cleanup.

The verifier read the full private H-014 v2 handoff as context, README,
`docs/manual-e2e.md`, `docs/database.md`, H-013 browser/fixture/oracle/M1 capture tools,
relevant tests, configuration and DB implementation. The full original owner prompt
and complete read-context register are leader-owned; this is a projection, not a
claim to retain a complete private transcript.

Initial clone identity: `6cc7ad3af426d0da6818281b035c5e683806f357`.
Disposable path: `/tmp/universitydb-h014-clean`, created with local Git clone
`--local --no-hardlinks --no-checkout`, then detached checkout of the exact SHA.
The clone has no inherited working-tree `.venv`, `.env`, `.omx`, runtime or untracked
fixtures. Its local-origin setting is verification plumbing, not a second canonical
repository and not publication. Package tools and browser are separate verification
infrastructure. No credentials, API generation/counting, monetary ledger/caps/holds,
remote push, runtime repair, or original evidence changes are authorized.

Installation attempt 1 failed sandbox DNS. Attempt 2 used supported escalation and
succeeded against frozen `uv.lock`. The isolated cache was initially empty but the
retry could reuse partial artifacts, so this is not an all-fresh-download claim.
Browser tooling is separately pinned Playwright 1.64.1 in a fresh `/tmp` tool venv;
existing provisioned browser binaries may be used and recorded explicitly. Product
dependencies and lockfile are not changed for browser tooling.

Final clean verification waits for a frozen committed candidate containing the
scoped fixes and these scripts. All final receipts record that tested SHA; later
documentation/evidence commits do not imply another complete product run.
