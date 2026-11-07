"""Generic AST and exact binding boundary; adapters own relational semantics."""

from typing import Any

import sqlglot
from sqlglot import exp

from universitydb.contracts import Failure


def validate_sql(
    sql: str, parameters: dict[str, Any], tables: dict[str, list[str]], functions: list[str]
) -> None:
    if len(sql.encode()) > 8000:
        raise Failure("RESOURCE_LIMIT", "SQL exceeds byte limit.")
    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except sqlglot.errors.ParseError as exc:
        raise Failure("SQL_INVALID", "SQL could not be parsed.") from exc
    if len(statements) != 1 or not isinstance(statements[0], exp.Select):
        raise Failure("UNSAFE_SQL", "Exactly one SELECT is required.")
    tree = statements[0]
    if any(node.comments for node in tree.walk()):
        raise Failure("UNSAFE_SQL", "SQL comments are unsupported.")
    if len(list(tree.find_all(exp.Select))) != 1 or tree.find(exp.Subquery, exp.CTE):
        raise Failure("UNSAFE_SQL", "Subqueries and CTEs are unsupported.")
    for relation in tree.find_all(exp.Table):
        if relation.name not in tables or relation.db or relation.catalog:
            raise Failure("UNSAFE_SQL", "Relation is not in the adapter allowlist.")
    for function in tree.find_all(exp.Func):
        if isinstance(function, (exp.And, exp.Or)):
            continue
        name = function.name if isinstance(function, exp.Anonymous) else function.sql_name()
        if name.lower() not in functions:
            raise Failure("UNSAFE_SQL", "Function is not in the adapter allowlist.")
    placeholders = [placeholder.name for placeholder in tree.find_all(exp.Placeholder)]
    if set(placeholders) != set(parameters):
        raise Failure("PROVIDER_INVALID_OUTPUT", "SQL placeholders must match bindings exactly.")
    if any(not placeholder.name for placeholder in tree.find_all(exp.Placeholder)):
        raise Failure("PROVIDER_INVALID_OUTPUT", "Only named placeholders are supported.")
