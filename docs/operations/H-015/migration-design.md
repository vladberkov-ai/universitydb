# Prospective collector / monetary-boundary design

H015 authorization replaces aggregate cap10/dispatch8 with cap120/dispatch110,
not an additional account. Preserve original monetary bytes in ignored private
backup and hash them. Preserve legacy profile/14entries exactly in the new ledger;
append a typed fixed H015 policy authorization and versioned rate segments.
Validate each entry using its original segment. Sum all obligations across segments.
Use existing stable spending.json.lock, fsync/atomic replace, exact expected old
hash/entries/total guard. Replay validates same authorization, never credits twice.
No automatic legacy or arbitrary environment migration. Unknown holds remain stops.

Reuse normal provider; optional safe evidence directory records actual complete
assembled wire and actual response body/usage (no headers/env/credentials).
Collector consumes pre-exported conversations and fixture setup, never oracle.
All fixtures use one explicitly bound canonical monetary path; UI and standalone
must not derive independent balances from temporary DB roots. Normal known-usage
refusal/invalid/incomplete outcomes do not poison the campaign accounting stop;
unknown usage, model/tier mismatch and critical accounting retain fail-closed stop.
Provider observations must not inject fixture/case metadata into model payload.

No product semantic/prompt tuning. No new dependency. Before dependent edits,
lock old and new behavior using synthetic regression tests. Then implement one
boundary at a time, targeted/full offline/static tests and independent review.
Tests never open or migrate canonical monetary ledger. Cleaner/reviewer separated;
root integrates, freezes and alone authorizes actual migration/dispatch after gates.
Detailed implemented format and verified invariants will be appended as evidence,
not retroactively substituted for this prospective design.
