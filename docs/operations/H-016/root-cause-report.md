# H016 CP1 — demonstrated pre-provider scope failures

Status: regression-first diagnosis, before product repair. Historical H015 results
are unchanged: original frozen assessment 2/48; separately corrected assessment
10/48. These are exposed end-to-end observations, not pure model accuracy. This
report neither replays nor rescales that campaign.

## Complete historical mapping

[Machine-readable map](root-cause-map.json) contains **38 rows: 19 cases × 2
repetitions, 13 distinct natural strings**. First failing entity: course 16,
student 12, teacher 2, reader 8. Repeated conversations are not independent defects;
fixture variants can have identical wording and different expected data outcomes.
Each row pins actual graph-state, completed receipt and fixture hashes, original
question, persisted scope, recomputed lexical tokens, actual catalog entries,
exact frozen-source site, contract expectation and causal family.

The graph states record `INVALID_INPUT` at `resolve_scope`; all 38 completed
receipts record zero provider calls and zero SQL attempts. No model behavior can
cause these failures. The scope key is absent because resolution raised before
returning a scope; recomputed lexical diagnostics are explicitly **not** recorded
runtime tokens or a partially committed scope.

## Proven common mechanism

On frozen product `ecb7f5c81c705d970dc64adb910ed2a5020cb28b`, shared
`src/universitydb/domain_support.py:36–41` accepts canonical `student_id=2`
syntax and numeric shorthand such as `student 2`, but not `student ID 2`.
The fallback at lines 95–99 treats a capitalized word following an entity noun as
a possible unknown name. It captures **ID** or **IDs** from these valid requests
and raises `Unknown <entity> name` when no previously extracted ID/catalog name
exists. This is one lexical intent-separation defect with two observed families:

| Family | Historical rows | Required distinction |
|---|---:|---|
| Numeric ID marker misread as a name | 18 | `course ID 3` supplies an identity filter; extract then validate numeric 3 against catalog |
| ID/IDs projection misread as a name | 20 | `student IDs` / `reader ID` declares output, not a filter or unknown identity |

Some questions contain both families. The map classifies the **first actual
failing entity**, not all potential downstream failures; J04/E03 first fail on
student projection, masking their later course-ID filter. Library's first
`reader` occurrence does not match a capitalized name, but the same search finds
its later `reader ID` projection. Catalog reads from every retained fixture
confirm actual registered IDs/labels; expected IDs exist. Neither missing catalog
wiring nor model routing explains the failures. Both adapters call this shared
resolver through `Agent.run` → compiled `load_schema` → `resolve_scope` →
`domain.catalog` / `domain.resolve`, before `plan`.

Defaults are not the historical cause: semester tokens are recognizable, but
scope never returns. They remain a repair invariant: no semester means all
semesters; projection-only entity nouns must not introduce filters. Unknown,
malformed and conflicting identities must still fail rather than disappear.

## Regression-first proof and prior coverage gap

The independent [NL regression coverage](regressions/independent-coverage.md) and
[pre-fix output](regressions/independent-pre-fix.txt) establish **21 failures,
15 passes** through ordinary `Agent.run(question)`, compiled production parsing,
real temporary SQLite and persisted traces. Inputs were independently authored,
not imported from H015. The transport is explicitly scripted at the provider
boundary and derives SQL from **actual production-resolved scope**, never a test
scope injected into the graph. This proves the scope defect and downstream
mechanics, not real-model planning/NL→SQL quality. Negative failures include
known-name/numeric-ID conflicts that incorrectly succeeded because `ID N` was
ignored; those are additional manifestations, not extra historical failure rows.

Earlier offline counts were real but insufficient evidence of natural wording:

- `tests/test_i2_domains.py:249–287` runs the real compiled graph, but its
  `graph_result` builds default questions from canonical `key=value` scopes and
  scripts the intended plan/SQL. Its 16-filter oracle coverage exercises semantics
  without the failing lexical grammar. Some direct `execute_spec` tests instead
  provide prestructured scope at the adapter/DB boundary.
- `tests/test_library.py:29–39` calls SQL/result adapters directly with scope;
  the compiled smoke uses `Count open loans per reader`, and ambiguity/resume
  uses `Open loans Ada`, neither containing the ID projection marker.
- Historical H013 410, H014 485 and later H015 610 check counts include many safety,
  typed contract, UI and assessment checks. Their breadth does not establish a
  natural-input lexical matrix; actual passing mechanics must not be relabelled
  fabricated or bypassed wholesale. The narrow question/fixture assumptions
  explain why those suites did not distinguish ID markers from names/projections.

## Repair acceptance, not a diagnostic stop

CP2 must fix general extraction/catalog/confirmation separation, not questions,
case IDs, fixture values or oracle answers. Numeric identity, projection,
unknown/malformed/conflicting input and ambiguity must have distinct outcomes.
Then CP3 must exercise downstream plan/SQL validation, read-only execution,
NULL/zero/empty/ties/dependencies, answer/trace and both-schema UI. Full suite,
independent oracle, browser, clean reproduction and independent review remain
pending at this CP1 cutoff. No API/count/probe, credentials, monetary mutation,
push or historical evidence writes occurred in this documentation operation.
