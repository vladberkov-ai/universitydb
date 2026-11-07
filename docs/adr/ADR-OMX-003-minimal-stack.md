# ADR-OMX-003 - Minimal Local Stack

Date:2026-11-07. Owner: repo. **Status: proposed**, pending owner review. Not execution authorization.

## Context
We need real LangGraph, SQL, a simple screen and a full trace, limited time. There are no product dependencies yet.

## Options
SQLite/direct LangGraph/OpenAI SDK/Streamlit/local JSONL; PostgreSQL+API/UI+LangSmith; CLI-only.

## Recommendation
First option; candidate Python3.13/LangGraph1.2.20/openai3.46.0/Streamlit1.67.0, still check compatibility. Luna baseline, snapshot Mini or Sol individual evaluation profiles.

## Rationale
A minimum of services and obvious diagnosability. The CLI doesn't cover the screen; The server option is viable, but redundant now.

## Consequences
Own trace contract, lack of HA/remote auth and stable model alias; key/access/budget unknown. Prices/pins from dated research, not a guarantee.

## Verification
Clean lock/install+security audit, real vertical slice S6, versions/usage/trace, full E2E. An explicit budget is required before live execution; no calls are made during B.

## Revision triggers
Concurrent writers/remote users, measured low Luna quality, changed API/prices or restart requirement.

Related [architecture](../plans/architecture-proposal.md), [contracts](../plans/contracts.md), [checks](../plans/test-plan.md). These are future relative paths after packaging from the reviewed planning baseline.
