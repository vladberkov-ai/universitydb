# H015 collector: implemented offline preparation

Scope: CP-L1 infrastructure only, no product tuning or candidate execution in tests.
The private H015 handoff is read context, not an actual received prompt. This
implementation lane received the root's bounded CP-L1 task projection; the root
records actual prompt provenance separately. No child workflow lifecycle mutations,
credentials, live requests, canonical monetary writes, push or oracle scoring occur
in this lane.

## Entry point and prospective registration

`python tools/eval/collector.py --registration REGISTRATION --output NEW_DIRECTORY`
uses the normal OpenAIProvider, Agent's real compiled graph and fresh SQLite DB.
There is no live test-mode switch, injected transport option, evaluator retry,
resume or alternative model. Private Python function seams exist solely for
no-network tests; the CLI never obtains them from input/environment.

The registration's closed fields are:

- `version`: `h015-collector-v1`;
- `campaign_id`: a Python identifier;
- `candidate_sha`: exact HEAD at collection;
- `files`: repository-relative path to SHA256 map, covering all tracked
  `src/`, `resources/`, `tools/eval/` and both exports;
- `conversations_path`: conversation-only harness export, exact 48 repeat-major
  A/J/D/C/E/L IDs and original question text pinned by its hash;
- `fixtures_path`: separate trusted setup descriptors, no oracle;
- `ledger_path`: the canonical source-checkout authority, never fixture-local;
- `policy_sha256`: the reviewed monetary policy identity;
- `ledger_baseline_sha256`: immutable historical monetary source identity.

Root separately pins oracle/scorer/rubric/rates in the prospective receipt. The
collector never opens oracle/heldout package paths, including for hash checking.
The root creates conversation/setup exports outside this process. Strict allowlists
reject extra export fields; fixture descriptor/resource hashes are checked. Only
question text and registered selection scalars enter Agent calls. IDs, setup names,
case metadata and oracle do not enter conversation payloads.

Before each untouched case the collector revalidates source/export hashes and SHA,
canonical ledger identity, historical source anchor, reviewed policy, unresolved
holds/stop and call counts. OpenAIProvider independently validates and atomically
reserves the canonical ledger before each dispatch; fixture/root isolation cannot
create fresh authority. Accounted reservations enforce the aggregate 240 maximum.
Application counters additionally enforce 5 generation/4 SQL per conversation.
Existing Agent repair/transient retry is unchanged; there is no collector retry.

## Durable experiment evidence

A stable global collector lock serializes campaign start. Its durable nonempty
marker refuses another campaign; an existing output directory is never resumed or
overwritten. A crash after `started.json` is not automatically retried.

- Campaign: immutable `registration.json`, `planned.json` (all48 not-run), final
  `summary.json` with every status, aggregate application-attempt count and stop.
- Each run ID: fsynced immutable `started.json` before DB/provider actions,
  `database-before.json`, fresh `fixture.sqlite3`, `exchanges.json` (all original
  Agent envelopes/events/step results), `graph-state.json` (actual compiled graph
  snapshot), `database-after.json`, `completed.json`; or safe `abort.json`.
- Original `traces/<UUID>.jsonl` and per-attempt
  `provider/<UUID>-request.json` / `-response.json` retain full safe provider wire,
  response and model/usage facts without environment/headers/credentials.
- Completion records hash original traces and full provider files. Hashes, exact
  trace/result agreement, artifact confinement/count and before/after DB census
  are verified before the next conversation. Known-accounted failure evidence
  is read from original error payloads; successful evidence comes from usage.

All fixture setup uses pinned schema/seed/trusted mutations in DELETE mode, with
foreign-key and integrity validation. Generated SQL permissions are unchanged.
Rejected `UNSAFE_SQL` is an ordinary failed proposal, not proof of unsafe execution;
actual DB mutation, integrity/trace/fabricated-success-envelope failure, wrong
execution profile or unhealthy monetary authority stops collection immediately.
Ordinary accounted refusal/invalid/semantic failures remain completed denominator
members, not discarded. Exhausted protocol selections can leave a product
clarification; that is retained as a failed measurement, not answered by guessing.
Independent observation still determines semantic/mandatory/safety/privacy checks;
collector integrity checks do not certify those checks or general accuracy.

Unexpected exceptions are recorded by class only, never exception text that might
include secrets. An abort preserves started/not-run and original files. A hard
interrupt may leave no summary, but immutable plan/started and trace evidence
remain. No automatic cleanup or rerun is provided.

## Fresh no-network verification

`pytest -q tests/test_h015_collector.py`: 19 passing tests, using independent
existing S6 development proposals and synthetic campaign IDs, never candidate
questions/oracle execution. Tests cover closed exports, wrong order/domain/type,
fixture/schema/hash/SHA drift, historical anchor/canonical authority, fresh DB and
journal, all48 ordinary rejected failures, actual writes stop, predispatch drift,
interrupted started persistence/no rerun, sanitized exception retention, full
request/response evidence hash/confinement, real compiled graph, and normal
OpenAIProvider with mocked worker: known-accounted refusal or successful plan/SQL then next untouched
case. Synthetic/injected results are not real-model evidence or live accuracy.

`ruff check tools/eval/collector.py tests/test_h015_collector.py`: passed.
Root owns full offline/static checks, prospective freeze, independent reviews,
secure activation, actual collection/observer scoring and final report.

## Bounded ai-slop-cleaner helper

Loaded installed `ai-slop-cleaner/SKILL.md`. Behavior lock before cleanup: all19
collector regressions passed. Plan: inspect only collector, its tests and this
implementation note; resolve masking fallbacks first, then dead code, duplication,
error/naming and missing-test smells. Do not refactor product or other lanes.

Fallback inventory/classification: broad outer exception handler is a grounded
fail-closed external boundary (records abort and stops, never claims success or
retries; secret-text sanitization tested). Optional compiled-state inspection is
a test seam for synthetic fake agents; live factory always returns actual Agent,
not a fallback provider. Failure and success evidence locations are both real
Agent contracts, covered by normal-provider refusal and successful-graph tests.
No masking fallbacks, dependency additions, speculative compatibility, UI scope,
or dead/debug code found. Passes1–3 therefore no-op; pass4 confirmed existing
19test lock rather than adding duplicate tests. No code changed in cleanup.

Quality: focused collector lint passed; targeted collector regression passed.
Root owns full tests/static/type checks and genuine independent reviewer approval;
this writer's cleanup inspection is not independent approval. Remaining risk:
real-model quality has not been measured by these synthetic checks.

## Independent-review correction: durable replay marker

Both independent code-reviewer and architect identified a HIGH replay defect in
CLI startup: `open('a+')` initially positions the stream at EOF, so `read()` failed
to see a prior campaign marker. Earlier synthetic function-level no-overwrite
checks did not prove the CLI's global replay refusal. No live collection occurred
before correction; prior implementation and cleanup claims above retain their
historical verification scope rather than substituting for this review.

Bounded correction plan: lock down both ordinary-return and interrupted-start CLI
replay using two distinct output directories and a temporary runtime; then seek
to offset0 under the held exclusive lock before reading, and fsync the marker's
parent directory after flushing/fsyncing the marker. Keep the durable append-only
marker after any attempt, including interruptions. No other behavior changed.
The new regression failed in both variants before the fix (second dispatch
appended a duplicate marker), and passes after it. It also verifies one ledger
check/dispatch total, unchanged marker bytes, parent-directory fsync and no second
output directory. Normal collection is mocked at this startup-only test boundary;
there are no credentials, actual monetary reads/writes or network calls.

Fresh focused verification after correction: `pytest -q
tests/test_h015_collector.py` →21passed; `ruff check` and `ruff format --check`
on collector/test →passed. Root owns independent re-review and broader gates.

Architect durability addendum: collection now also fsyncs `output.parent` immediately
after linking the new campaign directory, and fsyncs `output` immediately after
linking each case directory, before `started.json` or factory/provider action.
The existing immutable-file persistence fsync handles immediate file parents;
these additional fsyncs cover the newly linked directory ancestors. A no-network
ordering spy regression checks the linked campaign/case names were present during
the corresponding parent fsync before the factory runs. Fresh collector suite:
22passed; focused Ruff check passed. Marker inode is never removed/replaced.
