# ADR-OMX-006 - Schema boundary and own traces

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
R05/R06 require adaptability and a complete Input→Nodes→SQL→Results→Answer chain; do not require a specific platform.

## Options
Domain names embedded in core; descriptor+domain adapter; generic arbitrary-dialect abstraction. JSONL or LangSmith.

## Recommendation
Minimum ResultSpec+domain result adapter: metric/group keys/typed aliases/unit/scale/components, exact sum_units+graded_count for averages/ties; nonnull integer sum_units via aggregate-level COALESCE(SUM(grade_units),0), distinguishing void/NULL-only/real0 by denominator/enrollment_count; core doesn't guess University by names. SQLite-specific DB adapter, schema-agnostic core and University/Library descriptors; local versioned JSONL by contracts with full synthetic rows, redaction/public export separate.

## Rationale
The second schema is a real limited transfer test; do not claim support for all dialects. Local traces do not require an account/network service.

## Consequences
Its own completeness check/retention, library scope is just the same dialect. Full real PII is not allowed in demo. LangSmith requires a separate billing/retention solution.

## Verification
L1 same core hash+DB+live+E2E; V1–V2 units/grain/denominator failures; DB-Z actual raw components and separately UNIT-Z normalization of three zero cases; T1/T2+UI1 chain/completeness/screen access/secret exclusion; trace failure not success.

## Revision triggers
New dialect, real personal data, remote centralized tracing/retention/SLO requirement.

Related [architecture](../plans/architecture-proposal.md), [contracts](../plans/contracts.md), [checks](../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
