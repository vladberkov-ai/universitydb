"""Small shared adapter helpers; schema identifiers/policies are supplied by adapters."""

import re
from typing import Any

import sqlglot
from sqlglot import exp

from universitydb.contracts import Failure


def column(name: str, kind: str = "integer", nullable: bool = False) -> dict[str, Any]:
    return {"name": name, "type": kind, "nullable": nullable}


def clarify(field: str, options: list[dict[str, Any]], message: str) -> None:
    raise Failure("CLARIFICATION_REQUIRED", message, details={"field": field, "options": options})


def resolve_entities(
    question: str,
    catalog: dict[str, list[dict[str, Any]]],
    choices: dict[str, Any],
    fields: tuple[str, ...],
    id_patterns: dict[str, str] | None = None,
) -> dict[str, Any]:
    scope: dict[str, Any] = {}
    id_patterns = id_patterns or {}
    for key in fields:
        entries = catalog.get(key, [])
        singular = key.removesuffix("_id")
        pattern = rf"\b{key}\s*=\s*([A-Za-z0-9]+)\b"
        tokens = re.findall(pattern, question, re.IGNORECASE)
        if key not in id_patterns:
            tokens += re.findall(rf"\b{singular}\s*#?\s*(\d+)\b", question, re.IGNORECASE)
        else:
            tokens += re.findall(id_patterns[key], question, re.IGNORECASE)
        ids: list[Any] = []
        for token in tokens:
            value: Any = (
                token.upper() if key in id_patterns else int(token) if token.isdigit() else token
            )
            if entries and not any(e["id"] == value for e in entries):
                raise Failure("UNKNOWN_ENTITY", f"Unknown {key}: {value}.")
            if value not in ids:
                ids.append(value)
        names = []
        for entry in entries:
            labels = entry.get("aliases", [entry["label"]])
            if any(
                re.search(rf"(?<!\w){re.escape(label)}(?!\w)", question, re.IGNORECASE)
                for label in labels
                if label
            ):
                names.append(entry)
        candidates = {e["id"]: e for e in names}
        if key in choices:
            chosen = choices[key]
            allowed = set(candidates) if candidates else {e["id"] for e in entries}
            if type(chosen) not in (int, str) or chosen not in allowed:
                raise Failure("INVALID_CLARIFICATION", "Choice is not an offered catalog identity.")
            if ids and chosen not in ids:
                raise Failure("INVALID_CLARIFICATION", "Choice conflicts with explicit ID.")
            scope[key] = chosen
            continue
        conflict = len(ids) > 1 or bool(ids and candidates and ids[0] not in candidates)
        if conflict:
            clarify(
                key,
                [{"value": e["id"], "label": e["label"]} for e in entries],
                f"Conflicting {singular} identities; choose explicitly.",
            )
        if ids:
            scope[key] = ids[0]
        elif len(candidates) == 1:
            scope[key] = next(iter(candidates))
        elif candidates:
            clarify(
                key,
                [{"value": e["id"], "label": e["label"]} for e in names],
                f"Choose the intended {singular} identity.",
            )
        # Explicit identity labels cannot silently turn unknown names into an absent filter.
        unknown = re.search(
            rf"\b{singular}(?:_name)?\s*=\s*['\"]?([A-Za-z][\w-]*)", question, re.IGNORECASE
        )
        if unknown and not names and not ids:
            raise Failure("UNKNOWN_ENTITY", f"Unknown {singular} name.")
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
