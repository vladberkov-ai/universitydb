# H-007 I1 API reference research

## Scope and status

Read-only implementation-reference research retrieved on **2026-11-07** for the
already chosen OpenAI Python SDK, LangGraph, and Streamlit technologies. This note
does not select a model, authorize spending, accept proposed architecture ADRs,
or establish a working live S6. No provider requests, installations, compatibility
tests, or application changes were performed by this research lane.

The exact delegated task and subsequent persistence instruction are recorded in
[H-007-research-task.txt](../ai/omx/H-007-research-task.txt).

## Official documentation evidence

- **Structured output:** `client.responses.parse(..., text_format=YourPydanticModel)`
  exposes parsed output as `response.output_parsed`. Structured output can still
  contain semantic mistakes; refusal, incomplete output, and absence of parsed
  data must not be interpreted as validated SQL. Source:
  [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
- **Retries and timeouts:** use explicit `OpenAI(max_retries=0, timeout=seconds)`
  when the application owns its attempt budget. Documented defaults are two
  retries and a ten-minute timeout. Source:
  [OpenAI Python SDK reference](https://developers.openai.com/api/reference/python).
  Opening that page repeatedly timed out; its indexed documentation and the
  fetched publisher-maintained [PyPI description](https://pypi.org/project/openai/)
  supplied matching retry/timeout evidence. A numeric timeout avoids relying on
  a transport-specific timeout class; current SDK documentation describes HTTPX2.
- **Usage:** Responses includes `usage.input_tokens`, `output_tokens`,
  `total_tokens`, and token details; `max_output_tokens` is an output limit, not
  monetary authorization. Source:
  [Responses API reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create).
- **LangGraph execution:** construct `StateGraph(State)`, register nodes and
  edges with `START` and `END`, call `.compile()`, then execute the compiled graph
  with `.invoke(initial_state)`. Nodes return state updates. Source:
  [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api).
- **Streamlit input:** a form batches widget inputs until submit. Source:
  [st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form).
- **Streamlit trace display:** `st.code(..., language="sql")` displays SQL and
  `st.json(...)` displays structured trace data. Sources:
  [st.code](https://docs.streamlit.io/develop/api-reference/text/st.code),
  [st.json](https://docs.streamlit.io/develop/api-reference/data/st.json).
- **Offline UI assertions:** `AppTest.from_file(...).run()` supports inspecting
  a simulated app without a browser. It does not prove live-provider execution
  or visual browser correctness. Source:
  [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).

## Registry version observations

These are observed candidate releases, not dependency-selection decisions,
installation evidence, account access, or model availability. All three were
listed as released on November 5, 2026 when retrieved on November 7.

| Package | Observed release | Declared Python requirement |
| --- | --- | --- |
| [openai](https://pypi.org/project/openai/3.46.0/) | 3.46.0 | >=3.10 |
| [langgraph](https://pypi.org/project/langgraph/1.2.20/) | 1.2.20 | >=3.10 |
| [streamlit](https://pypi.org/project/streamlit/1.67.0/) | 1.67.0 | >=3.11 |

The implementation lane must independently resolve, pin, and test its actual
environment. No wheel hashes or installed-version assertions are made here.

## Supporting official example

The [OpenAI per-run spending-controller example](https://developers.openai.com/cookbook/articles/per_run_spending_controller_responses_api)
illustrates reserving budget before dispatch, reconciling usage, disabling SDK
retries, and retaining uncertain charges after ambiguous failures. Its example
rates are explicitly unsuitable for live use. This is supplemental example
guidance, not a verified price quote, approved budget, or required architecture.

## Limitations and handoff

- No concrete model, account access, current model-specific pricing, or spending
  authorization was established. Application inference: keep network dispatch
  blocked until those conditions are explicitly satisfied.
- The fetched `st.json` documentation displayed version 1.66.0; form, code, and
  AppTest pages displayed 1.67.0. Verify the used APIs against actual installed
  pins rather than treating these moving documentation pages as a lockfile.
- The OpenAI generic Responses creation reference failed retrieval because of
  page size; the Python-specific creation reference was fetched successfully.
  The attempted SDK `.md` URL returned 404. No missing page was treated as read.
- No upstream source-code lookup or third-party OSS implementation was needed.
  Search results outside official documentation/PyPI were not used as evidence.
- Research covered external APIs only, not repository usage, SQL-validation
  design, package adoption, implementation correctness, or existing H-006 work.
- Real LangGraph with an offline model fixture is distinct from authorized
  real-model execution. Neither documentation nor package versions prove live S6.

## Activity provenance

The researcher read the installed `openai-docs` skill, retrieved the cited
documentation and registry pages, and returned the findings to the parent.
Only this note and its task record were subsequently created on explicit parent
instruction. No Obsidian access, advisory restart, workflow-state mutation,
child delegation, paid call, Git staging, or Git commit was performed by this lane.

## Addendum — SQLGlot SQLite AST reference, 2026-11-07

### Request and evidence boundary

This follow-up documents the performer's already selected narrow AST parser;
it is not a dependency comparison, architecture approval, or security verdict.
No package was installed or executed by this research lane. Previous research
above is preserved unchanged. The exact follow-up appears in the task record.

### Official API facts

- `parse(sql, read="sqlite")` returns a collection of syntax trees. Current
  `parse_one` documentation describes a single tree for one statement and a
  `Block` for multiple statements; do not infer one-statement enforcement from
  its name. Specify the source dialect instead of relying on SQLGlot's generic
  dialect. The FAQ explicitly warns that parsing is lenient and is not SQL
  validation. Comments are preserved only on a best-effort basis.
  [SQLGlot API and FAQ](https://sqlglot.com/sqlglot.html)
- `Select` includes `expressions`, `from_`, `with_`, `into`, and query modifiers.
  `Join` includes `this`, `on`, `side`, `kind`, `using`, and `method`, among other
  arguments. Recognizing these classes alone does not restrict their arguments.
  [Query expression API](https://sqlglot.com/sqlglot/expressions/query.html)
- `Column` carries column identity and optional `table`, `db`, and `catalog`.
  `EQ` is a binary predicate with left/right operands. `Placeholder` is distinct
  from `Parameter`; its `name` is the stored name or `?`. Check the installed
  parser's representation of the exact placeholder syntax accepted by the app.
  [Core expression API](https://sqlglot.com/sqlglot/expressions/core.html)
- SQLite has its own dialect and tokenizer behavior, including comment and
  identifier handling. Generic-dialect acceptance does not prove SQLite
  acceptance. [SQLite dialect API](https://sqlglot.com/sqlglot/dialects/sqlite.html)
- Python `sqlite3.execute(sql, parameters)` binds values and accepts a single
  statement; multiple statements raise `ProgrammingError`. `executescript` is
  the multi-statement interface and is not appropriate for model query
  execution. Named placeholders use dictionaries, qmark placeholders sequences.
  [Python 3.12 sqlite3](https://docs.python.org/3.12/library/sqlite3.html)

### Application-policy implications (inferences, not SQLGlot guarantees)

For the scoped S6 contract, require exactly one nonempty parsed statement with
an approved `Select` root and validate the complete allowed structure: projection,
known tables and aliases, join conditions/types, and the four required predicates
with their exact typed parameters. Reject unapproved AST arguments and nested
constructs rather than accepting every query composed of familiar node classes.
A bag of four `EQ` nodes is insufficient: boolean structure, operand identities,
and placeholder mapping determine whether those filters actually constrain rows.

Do not strip comments with an ad-hoc regular expression or treat absent AST
comments as proof that the input had none. If comments are prohibited by policy,
check that separately using an appropriately tested lexical boundary. Test
comment-only suffixes, extra/empty statements, quoted delimiters, and the exact
SQLite placeholder forms. SQL text must not be interpolated with user values;
parameter binding is distinct from identifier/AST validation. Preserve SQLite
read-only/authorizer and resource-limit defenses independently of parser success.
These are review/test implications for the performer, not a claimed implementation.

### Version and retrieval caveats

[Publisher registry release sqlglot 30.30.0](https://pypi.org/project/sqlglot/30.30.0/)
was observed as the latest release, dated November 6, 2026, requiring Python
>=3.9. The registry reported no upload provenance for this release; this is a
registry observation, not a vulnerability finding or adoption decision.
Moving API documentation may differ from an installed version. In particular,
recheck `parse_one` multiple-statement behavior and AST argument names against
the actual pin in offline tests. No source-file claims requiring a pinned Git
SHA are made; evidence here is official generated API documentation and PyPI.

The unversioned Python sqlite3 documentation initially resolved to 3.15.2; the
3.12 documentation was then explicitly fetched for a version-specific reference.
No provider calls, product edits, runtime-state changes, vault access, staging,
or commits were performed during this follow-up.
