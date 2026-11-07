---
title: "ADR-CHAT-001: Memory Mastery"
updated: 2026-11-06
status: accepted
owner: chat
visibility: public-ready
sources: ["chat:2026-11-06"]
---

# ADR-CHAT-001: memory ownership

## Context and source
CHAT-003 (private source; not exported): Want to store chat results in UniversityDB and avoid OMX duplication.

## Solution
Vault is the authoritative original of chat results. Repo - original OMX code and results.
For delivery, selected chat pages are transferred to the repo as verified snapshots indicating the source and hash.

## Options considered
1. Copy the entire work in both places: rejected due to discrepancies between the two edited versions.
2. Store everything only in repo: does not correspond to the one selected by the Obsidian user.
3. Separate owners and use links/snapshots: the chosen way to implement the requirement.

## Consequences and verification
OMX does not edit exported chat pages. Chat does not overwrite OMX ADR.
When the source changes, the snapshot becomes stale until the hashes are verified again.
Check on transfer: source, owner, destination, SHA-256, commit, push result.
The boundary requirement is accepted by the user; specific commit/push intervals remain a protocol proposal.

---
Projection H-004 v2: derivative chat-owned shot, unedited original. Private dependencies are not exported; SHA-256 and change log are in the repo receipt. Application execution statuses are not changed by this projection.
