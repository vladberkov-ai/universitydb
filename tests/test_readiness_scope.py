"""H-014 scope-loss regressions: injected transport is not model accuracy."""

import json
from pathlib import Path

import pytest
from test_i2_core import scripted_step

from universitydb import db
from universitydb.agent import Agent
from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library
from universitydb.llm import ScriptedProvider


@pytest.mark.parametrize(
    "kind,question,known_id",
    [
        ("university", "What is the average grade for Zoe?", None),
        ("library", "How many open loans does Zoe have?", None),
        ("university", "What is the mean of Zoe?", None),
        ("university", "What is Zoe's average grade?", None),
        ("library", "Count open loans of Zoe", None),
        ("library", "Count Zoe's open loans", None),
        ("university", "What is Bea's average grade?", 2),
        ("library", "Count Ada's open loans", 1),
        ("university", "What is the average grade for Bea?", 2),
        ("library", "How many open loans does Ada have?", 1),
    ],
)
def test_named_scope_compiled_graph(tmp_path, kind, question, known_id):
    domain = University() if kind == "university" else Library()
    spec = make_spec("grade_mean") if kind == "university" else LIBRARY_SPEC
    field = "student_id" if kind == "university" else "reader_id"
    resources = Path(__file__).resolve().parents[1] / "resources"
    database = tmp_path / "data.db"
    db.initialize(database, resources if kind == "university" else resources / "library")
    # A valid unfiltered proposal would previously produce misleading global success.
    scope = {} if known_id is None else {field: known_id}
    sql, params = domain.query(spec, scope)
    provider = ScriptedProvider(list(scripted_step(spec, sql, params)))
    agent = Agent(domain, database, provider, tmp_path / "trace")
    result = agent.run(question)
    if known_id is None:
        assert result["status"] == "error", result
        assert result["error"]["code"] == "INVALID_INPUT"
        assert result["answer"] is None
        assert provider.calls == 0
        assert not any(e["kind"] in ("sql_attempt", "db_result") for e in result["events"])
    else:
        assert result["status"] == "ok", result
        assert f"{field}={known_id}" in result["answer"]["scope"]
        assert provider.calls == 2
    assert result["events"][-1]["kind"] == "run_end"
    traces = list((tmp_path / "trace").glob("*.jsonl"))
    assert len(traces) == 1
    persisted = [json.loads(line) for line in traces[0].read_text().splitlines()]
    assert persisted[-1]["kind"] == "run_end"


@pytest.mark.parametrize(
    "question",
    [
        "Count open loans per reader",
        "Count open loans including readers with zero loans",
        "Count open loans that are not returned",
        "Count open loans by reader_id=1",
    ],
)
def test_library_non_target_prose_preserved(tmp_path, question):
    database = tmp_path / "library.db"
    db.initialize(database, Path(__file__).resolve().parents[1] / "resources/library")
    scope = Library().resolve(question, Library().catalog(database))
    assert scope == ({"reader_id": 1} if "reader_id=1" in question else {})
