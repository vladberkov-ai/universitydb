# Initial independent code review — bounded leader-received projection

Date2026-11-07. Independent native role `code-reviewer`, separate fresh clean-context lane launched by root after cleaner. Source: leader's received native-result summary delivered to performer; performer persisted this summary, not reviewer-owned source bytes or a full transcript. No claim of plaintext equality to encrypted delegation arguments. Source scope: frozen H007 I1 after65offline tests, based on code commit c34e8868d44ac81f60ff66c2f9b1b29b9f01c2d8 plus cleaner diff.

Verdict: **REQUEST CHANGES**, **2 HIGH** spending-boundary findings. Not approval.

1. `src/universitydb/llm.py:58` in the reviewed version guarded new reservations only by reserved_usd, ignoring known actual usage above the estimate. Reproduction: cap0.03, reserve0.014, record_usage(30000,1000) at1/1 rates→observed0.031; next0.014 reservation was wrongly allowed. Risk: already known overrun does not stop subsequent paid dispatch. Fix: durable effective per-attempt holds max(reservation,observed), preserve uncertain failed holds, stop future dispatch after known overrun; regression before implementation.
2. Existing empty spending ledger was treated as first use with zero spend. Risk: truncate/crash can reset budget state. Fix: existing empty/malformed/missing-after-use must fail closed, atomic durable replacement and stable separate locking, never lock a replaceable inode as coordination authority; regression before implementation.

Both original reproductions failed in the performer regression run before edits. Bounded fixes and additional corruption/concurrency/atomic-failure tests were then implemented. Re-review required; this historical REQUEST CHANGES is retained and cannot be converted to approval by the author. Final independent verdict pending at this receipt cutoff.
