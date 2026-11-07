from decimal import Decimal
from unittest.mock import patch

import pytest
from conftest import QUESTION, SCOPE, outputs
from pydantic import ValidationError

from universitydb.agent import Agent
from universitydb.contracts import Binding, Failure, PlanProposal, SQLProposal, bindings
from universitydb.domain import University
from universitydb.llm import ScriptedProvider, Spending
from universitydb.tracing import Trace


def test_binding_closed_and_byte_bounds():
    with pytest.raises(ValidationError):
        Binding(name="x", type="integer", integer_value=True, text_value=None)
    with pytest.raises(Failure):
        bindings([Binding(name="x", type="text", integer_value=None, text_value="é" * 1001)])
    one = Binding(name="x", type="integer", integer_value=1, text_value=None)
    with pytest.raises(Failure):
        bindings([one, one])
    with pytest.raises(Failure):
        bindings([Binding(name="x", type="integer", integer_value=None, text_value=None)])


def test_sql_size_and_closed_proposal():
    value = outputs()[1]
    value["sql"] = "x" * 8001
    with pytest.raises(ValidationError):
        SQLProposal.model_validate(value)
    value = outputs()[1]
    value["sql"] = "é" * 4001
    with pytest.raises(Failure) as error:
        University().validate_sql(SQLProposal.model_validate(value), SCOPE)
    assert error.value.code == "RESOURCE_LIMIT"
    value = outputs()[1]
    value["extra"] = True
    with pytest.raises(ValidationError):
        SQLProposal.model_validate(value)


def test_provider_call_limit_and_deadline(database, tmp_path):
    agent = Agent(University(), database, ScriptedProvider(outputs()), tmp_path / "traces")
    agent.trace = Trace(tmp_path / "traces", "limit")
    agent.deadline = float("inf")
    agent.calls = 5
    with pytest.raises(Failure) as error:
        agent._call("plan", {}, PlanProposal)
    assert error.value.code == "BUDGET_EXCEEDED"
    agent.deadline = 0
    with pytest.raises(Failure):
        agent._check_deadline()


def test_trace_budget_persists_terminal_error(database, tmp_path):
    original = Trace.__init__

    def limited(self, directory, run_id, **kwargs):
        original(self, directory, run_id, limit=5000)

    with patch.object(Trace, "__init__", limited):
        result = Agent(
            University(), database, ScriptedProvider(outputs()), tmp_path / "traces"
        ).run(QUESTION)
    assert result["status"] == "error" and result["answer"] is None
    assert result["events"][-1]["kind"] == "run_end"


def test_budget_actual_usage_reconciled_without_releasing_hold(tmp_path):
    import json

    ledger = tmp_path / "spend.json"
    budget = Spending(ledger, "test", Decimal(".1"), Decimal(1), Decimal(2))
    reservation = budget.reserve()
    budget.record_usage(reservation.attempt_id, 100, 50)
    record = json.loads(ledger.read_text())
    assert record["reserved_usd"] == ".016" or Decimal(record["reserved_usd"]) == Decimal(".016")
    assert Decimal(record["observed_usd"]) == Decimal(".0002")
    assert record["input_tokens"] == 100 and record["output_tokens"] == 50


def test_graph_core_has_no_university_table_identifiers():
    from pathlib import Path

    core = Path("src/universitydb/agent.py").read_text()
    for name in (
        "Students",
        "Teachers",
        "Courses",
        "Semesters",
        "Offerings",
        "Enrollments",
        "grade_units",
    ):
        assert name not in core


def test_actual_usage_overrun_durably_stops_next_reservation(tmp_path):
    budget = Spending(tmp_path / "spend.json", "test", Decimal(".03"), Decimal(1), Decimal(1))
    reservation = budget.reserve()
    with pytest.raises(Failure):
        budget.record_usage(reservation.attempt_id, 30000, 1000)
    with pytest.raises(Failure):
        budget.reserve()


def test_existing_empty_ledger_fails_closed(tmp_path):
    ledger = tmp_path / "spend.json"
    ledger.touch()
    budget = Spending(ledger, "test", Decimal(".03"), Decimal(1), Decimal(1))
    with pytest.raises(Failure):
        budget.reserve()


def test_effective_holds_preserve_unknown_attempt_plus_positive_actual_excess(tmp_path):
    ledger = tmp_path / "spend.json"
    budget = Spending(ledger, "test", Decimal(".05"), Decimal(1), Decimal(1))
    known = budget.reserve()
    budget.reserve()  # Second attempt remains uncertain, not free.
    budget.record_usage(known.attempt_id, 30000, 1000)
    with pytest.raises(Failure):
        budget.reserve()
    import json

    record = json.loads(ledger.read_text())
    assert Decimal(record["effective_usd"]) == Decimal(".045")
    assert Decimal(record["reserved_usd"]) == Decimal(".028")
    assert Decimal(record["observed_usd"]) == Decimal(".031")


@pytest.mark.parametrize("contents", ["", "not-json", "{}", "[]"])
def test_existing_bad_ledger_never_resets_to_zero(tmp_path, contents):
    ledger = tmp_path / "spend.json"
    ledger.write_text(contents)
    budget = Spending(ledger, "test", Decimal(".05"), Decimal(1), Decimal(1))
    with pytest.raises(Failure):
        budget.reserve()
    assert ledger.read_text() == contents


def test_ledger_deleted_after_use_and_approval_profile_drift_fail_closed(tmp_path):
    ledger = tmp_path / "spend.json"
    budget = Spending(ledger, "test", Decimal(".05"), Decimal(1), Decimal(1))
    budget.reserve()
    with pytest.raises(Failure):
        Spending(ledger, "test", Decimal(".05"), Decimal(".1"), Decimal(1)).reserve()
    ledger.unlink()
    with pytest.raises(Failure):
        budget.reserve()


def test_atomic_replace_failure_preserves_old_ledger_and_lock(tmp_path):
    from unittest.mock import patch

    ledger = tmp_path / "spend.json"
    budget = Spending(ledger, "test", Decimal(".05"), Decimal(1), Decimal(1))
    budget.reserve()
    before = ledger.read_bytes()
    inode = (tmp_path / "spend.json.lock").stat().st_ino
    with (
        patch("universitydb.llm.os.replace", side_effect=OSError("test failure")),
        pytest.raises(Failure),
    ):
        budget.reserve()
    assert ledger.read_bytes() == before
    assert (tmp_path / "spend.json.lock").stat().st_ino == inode
    assert sorted(p.name for p in tmp_path.iterdir()) == ["spend.json", "spend.json.lock"]


def test_concurrent_process_reservations_share_stable_lock(tmp_path):
    import subprocess
    import sys

    ledger = tmp_path / "spend.json"
    script = (
        "from universitydb.llm import Spending;from universitydb.contracts import Failure;"
        "from pathlib import Path;from decimal import Decimal;"
        f'b=Spending(Path({str(ledger)!r}),"test",Decimal(".028"),Decimal("1"),Decimal("1"));'
        '\ntry: b.reserve();print("ok")\nexcept Failure: print("blocked")'
    )
    workers = [
        subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, text=True)
        for _ in range(6)
    ]
    outcomes = [worker.communicate(timeout=10)[0].strip() for worker in workers]
    assert outcomes.count("ok") == 2 and outcomes.count("blocked") == 4
    assert all(worker.returncode == 0 for worker in workers)
