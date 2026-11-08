"""Small shared adapter helpers; schema identifiers/policies are supplied by adapters."""

import re
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import sqlglot
from sqlglot import exp

from universitydb.contracts import Failure


def column(name: str, kind: str = "integer", nullable: bool = False) -> dict[str, Any]:
    return {"name": name, "type": kind, "nullable": nullable}


def clarify(field: str, options: list[dict[str, Any]], message: str) -> None:
    raise Failure("CLARIFICATION_REQUIRED", message, details={"field": field, "options": options})


def _compact_id_mentions(question: str, singular: str) -> Iterator[re.Match[str]]:
    return re.finditer(
        rf"\b{singular}(?:\s*#\s*([^\s,)]*)|\s+([-+0-9][^\s,)]*))",
        question,
        re.IGNORECASE,
    )


def _identity_tokens(question: str, key: str, id_pattern: str | None) -> list[str]:
    """Extract marked IDs without confusing requested ID columns with filters."""
    singular = key.removesuffix("_id")
    list_pattern = (
        rf"\b(?:{key}\s*=\s*|{singular}\s+IDs?\s*[:=#]?\s*|{singular}\s*#?\s*)"
        r"[0-9]+\s*(?:,|and\b|or\b)\s*[0-9]"
    )
    if re.search(list_pattern, question, re.IGNORECASE):
        raise Failure("INVALID_INPUT", f"Multiple {singular} IDs are not a scalar filter.")
    tokens = re.findall(rf"\b{key}\s*=\s*([^\s,)]*)", question, re.IGNORECASE)
    if id_pattern is None:
        for mention in _compact_id_mentions(question, singular):
            tokens.append(next((part for part in mention.groups() if part is not None), ""))
    else:
        tokens += re.findall(id_pattern, question, re.IGNORECASE)
    value_pattern = id_pattern or r"[0-9]+"
    for mention in re.finditer(rf"\b{singular}\s+ID(s?)\b", question, re.IGNORECASE):
        tail = question[mention.end() :].lstrip()
        marked = bool(tail and tail[0] in ":=#")
        if marked:
            tail = tail[1:].lstrip()
        token = re.match(r"[^\s,)]*", tail)
        assert token is not None
        value = token.group().rstrip("?.!;")
        if re.fullmatch(value_pattern, value, re.IGNORECASE):
            tokens.append(value)
            continue
        # These are column-list productions, not arbitrary names or absent IDs.
        prefix = question[: mention.start()]
        output_prefix = bool(
            re.search(
                r"\b(?:show|list|include|display|return|which|showing|by|per)\s+$",
                prefix,
                re.IGNORECASE,
            )
            or re.search(r"\b(?:rows?|enrollments)\s+(?:with|including)\s+$", prefix, re.IGNORECASE)
            or re.search(r"\bIDs?\s*(?:,\s*(?:and\s+)?|and\s+)$", prefix, re.IGNORECASE)
        )
        projection = not marked and (
            bool(
                re.match(
                    r"(?:in\s+(?:the\s+)?(?:output|results?)|as\s+(?:a\s+)?column)\b",
                    tail,
                    re.IGNORECASE,
                )
            )
            or (
                output_prefix
                and (
                    bool(re.match(r"(?:and|for|with|per|have|has)\b", tail, re.IGNORECASE))
                    or not value
                    or tail.startswith(",")
                )
            )
        )
        if not projection:
            raise Failure("INVALID_INPUT", f"Missing or malformed {key}.")
    if any(
        not re.fullmatch(value_pattern, token.rstrip("?.!;"), re.IGNORECASE) for token in tokens
    ):
        raise Failure("INVALID_INPUT", f"Missing or malformed {key}.")
    return tokens


def _validate_named_mentions(question: str, singular: str, entries: list[dict[str, Any]]) -> None:
    patterns = (
        rf"\b{singular}(?:_name)?\s*(?:=|named)\s*['\"]?([A-Za-z][\w-]*)",
        rf"\b(?i:{singular})[ \t]+(?:named[ \t]+)?['\"]?([A-Z][\w-]*)",
    )
    for pattern in patterns:
        for mention in re.finditer(
            pattern, question, re.IGNORECASE if pattern == patterns[0] else 0
        ):
            if pattern == patterns[1] and mention.group(1).casefold() in {"id", "ids"}:
                continue  # ID syntax has its own extraction/validation, not a name fallback.
            if not any(
                re.match(rf"{re.escape(label)}(?!\w)", question[mention.start(1) :], re.IGNORECASE)
                for entry in entries
                for label in entry.get("aliases", [entry["label"]])
                if label
            ):
                raise Failure("INVALID_INPUT", f"Unknown {singular} name.")


def _catalog_mentions(
    question: str,
    catalog: dict[str, list[dict[str, Any]]],
    fields: tuple[str, ...],
    id_patterns: dict[str, str],
) -> tuple[dict[str, dict[tuple[int, int], set[Any]]], dict[str, str], str]:
    """Extract owned spans once for catalog matching, ID lexing and name guards."""
    mentions: dict[str, dict[tuple[int, int], set[Any]]] = {key: {} for key in fields}
    owned: dict[tuple[int, int], set[str]] = {}
    typed_spans: set[tuple[int, int]] = set()
    for mention in re.finditer(r"\b(?:for|of)\s+(['\"])(.*?)\1", question, re.IGNORECASE):
        roles = {
            key
            for key in fields
            for entry in catalog.get(key, [])
            for label in entry.get("aliases", [entry["label"]])
            if mention.group(2).casefold() == label.casefold()
        }
        if not roles:
            raise Failure("INVALID_INPUT", "Unknown quoted target name.")
        owned.setdefault(mention.span(2), set()).update(roles)
    for key in fields:
        singular = key.removesuffix("_id")
        entries = catalog.get(key, [])
        for mention in re.finditer(
            rf"\b{singular}(?:_name)?(?:\s*(?:=|named)\s*|\s+)(['\"])(.*?)\1",
            question,
            re.IGNORECASE,
        ):
            if not any(
                mention.group(2).casefold() == label.casefold()
                for entry in entries
                for label in entry.get("aliases", [entry["label"]])
            ):
                raise Failure("INVALID_INPUT", f"Unknown {singular} name.")
            owned.setdefault(mention.span(2), set()).add(key)
        for mention in re.finditer(
            rf"\b(?:{key}\s*=\s*|{singular}\s+IDs?\s*[:=#]?\s*)([^\s,)]+)",
            question,
            re.IGNORECASE,
        ):
            value_pattern = id_patterns.get(key, r"[-+]?[0-9][^\s,)]*")
            if re.fullmatch(value_pattern, mention.group(1).rstrip("?.!;"), re.IGNORECASE):
                owned.setdefault(mention.span(1), set()).add(key)
                typed_spans.add(mention.span(1))
        if key not in id_patterns:
            for mention in _compact_id_mentions(question, singular):
                group = 1 if mention.start(1) != -1 else 2
                owned.setdefault(mention.span(group), set()).add(key)
                typed_spans.add(mention.span(group))
        for entry in entries:
            for label in entry.get("aliases", [entry["label"]]):
                if not label:
                    continue
                for mention in re.finditer(
                    rf"(?<!\w){re.escape(label)}(?!\w)", question, re.IGNORECASE
                ):
                    mentions[key].setdefault(mention.span(), set()).add(entry["id"])
                    if re.search(
                        rf"\b{singular}(?:_name)?(?:\s*(?:=|named)\s*|\s+)['\"]?$",
                        question[: mention.start()],
                        re.IGNORECASE,
                    ):
                        owned.setdefault(mention.span(), set()).add(key)

    def visible_question(key: str | None) -> str:
        visible = list(question)
        for (start, end), roles in owned.items():
            if key not in roles:
                visible[start:end] = " " * (end - start)
        return "".join(visible)

    return (
        {
            key: {
                (start, end): values
                for (start, end), values in spans.items()
                if not any(a <= start and end <= b for a, b in typed_spans)
                and not any(
                    a <= start and end <= b and key not in roles for (a, b), roles in owned.items()
                )
            }
            for key, spans in mentions.items()
        },
        {key: visible_question(key) for key in fields},
        visible_question(None),
    )


def resolve_entities(
    question: str,
    catalog: dict[str, list[dict[str, Any]]],
    choices: dict[str, Any],
    fields: tuple[str, ...],
    id_patterns: dict[str, str] | None = None,
) -> dict[str, Any]:
    scope: dict[str, Any] = {}
    id_patterns = id_patterns or {}
    all_mentions, field_questions, structural_question = _catalog_mentions(
        question, catalog, fields, id_patterns
    )
    if re.search(r"\b[A-Za-z_]\w*_id\s*(?:!=|<>|<=|>=|<|>)", structural_question, re.IGNORECASE):
        raise Failure("INVALID_INPUT", "Identity filters support equality only.")
    nouns = "|".join(re.escape(key.removesuffix("_id")) for key in fields)
    if re.search(
        rf"\b(?:not|excluding|except|without)\s+(?:(?:the|for|of)\s+)?(?:{nouns})(?:s|_id|_name)?\b",
        structural_question,
        re.IGNORECASE,
    ):
        raise Failure(
            "INVALID_INPUT", "Identity filters support equality only; exclusions are unsupported."
        )
    # A marked unsupported axis cannot silently disappear, but a requested output
    # column is not an identity filter (including registered grouping-only axes).
    for mention in re.finditer(r"\b([A-Za-z_]\w*)\s+IDs?\b", structural_question, re.IGNORECASE):
        key = mention.group(1).casefold() + "_id"
        if key not in fields and _identity_tokens(structural_question, key, None):
            raise Failure(
                "INVALID_INPUT", "Unsupported entity filter; no filter is silently ignored."
            )
    for key in fields:
        entries = catalog.get(key, [])
        singular = key.removesuffix("_id")
        tokens = _identity_tokens(field_questions[key], key, id_patterns.get(key))
        _validate_named_mentions(field_questions[key], singular, entries)
        ids: list[Any] = []
        for token in tokens:
            token = token.rstrip("?.!;")
            value: Any = (
                token.upper() if key in id_patterns else int(token) if token.isdigit() else token
            )
            if key in catalog and not any(e["id"] == value for e in entries):
                raise Failure("INVALID_INPUT", f"Unknown {key}: {value}.")
            if value not in ids:
                ids.append(value)
        mentions = all_mentions[key]
        # Prefer the full catalog label over a contained shorter label. Distinct
        # mentions remain independent constraints, not a union masking conflicts.
        mention_sets = [
            values
            for (start, end), values in mentions.items()
            if not any(a <= start and end <= b and (a, b) != (start, end) for a, b in mentions)
        ]
        compatible = set.intersection(*mention_sets) if mention_sets else set()
        candidates = {e["id"]: e for e in entries if e["id"] in compatible}
        conflict = (
            len(ids) > 1
            or bool(mention_sets and not compatible)
            or bool(ids and mention_sets and ids[0] not in compatible)
        )
        if conflict:
            raise Failure(
                "INVALID_INPUT",
                f"Conflicting {singular} identities; provide one consistent identity.",
            )
        if key in choices:
            chosen = choices[key]
            allowed = set(candidates) if candidates else {e["id"] for e in entries}
            if type(chosen) not in (int, str) or chosen not in allowed:
                raise Failure("INVALID_SELECTION", "Choice is not an offered catalog identity.")
            if ids and chosen not in ids:
                raise Failure("INVALID_SELECTION", "Choice conflicts with explicit ID.")
            scope[key] = chosen
            continue
        if ids:
            scope[key] = ids[0]
        elif len(candidates) == 1:
            scope[key] = next(iter(candidates))
        elif candidates:
            clarify(
                key,
                [{"value": e["id"], "label": e["label"]} for e in candidates.values()],
                f"Choose the intended {singular} identity.",
            )
    return scope


def normalize_sql(sql: str, tables: dict[str, list[str]]) -> exp.Select:
    if len(sql.encode()) > 8000:
        raise Failure("RESOURCE_LIMIT", "SQL exceeds byte limit.")
    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except sqlglot.errors.ParseError as exc:
        raise Failure("SQL_INVALID", "SQL could not be parsed.") from exc
    if len(statements) != 1 or not isinstance(statements[0], exp.Select):
        raise Failure("UNSAFE_SQL", "Exactly one supported SELECT is required.")
    tree = statements[0]
    if any(n.comments for n in tree.walk()):
        raise Failure("UNSAFE_SQL", "SQL comments are outside the supported subset.")
    relations = list(tree.find_all(exp.Table))
    aliases: dict[str, str] = {}
    for relation in relations:
        if relation.name not in tables or relation.db or relation.catalog:
            raise Failure("UNSAFE_SQL", "Unknown or qualified relation.")
        aliases[relation.alias_or_name] = relation.name
    for c in tree.find_all(exp.Column):
        table = aliases.get(c.table)
        if table is None:
            raise Failure("UNSAFE_SQL", "All columns require explicit relation aliases.")
        if c.name not in tables[table]:
            raise Failure("SQL_INVALID", "Unknown column in registered relation.")
        c.set("table", exp.to_identifier(table))
    for relation in relations:
        relation.set("alias", None)
    # Predicate order is not meaningful, but the closed conjunction members are.
    where = tree.args.get("where")
    if where:
        predicates = list(where.this.flatten()) if isinstance(where.this, exp.And) else [where.this]
        predicates.sort(key=lambda p: p.sql())
        tree.set("where", exp.Where(this=exp.and_(*predicates)))
    return tree


@contextmanager
def readonly_catalog_connection(path: Path) -> Iterator[sqlite3.Connection]:
    """Bounded trusted startup reads; generated queries use the separate DB worker."""
    try:
        connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.5)
        try:
            yield connection
        finally:
            connection.close()
    except sqlite3.Error as exc:
        raise Failure("DB_UNAVAILABLE", "Database catalog/integrity scan is unavailable.") from exc
