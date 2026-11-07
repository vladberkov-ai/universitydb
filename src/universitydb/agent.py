"""Schema-agnostic real compiled LangGraph orchestration for one bounded scalar step."""

import hashlib
import json
import time
import uuid
from itertools import pairwise
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from universitydb import db
from universitydb.contracts import Failure, PlanProposal, SQLProposal
from universitydb.llm import Provider
from universitydb.tracing import Trace


class State(TypedDict, total=False):
    question: str
    scope: dict[str, Any]
    descriptor: dict[str, Any]
    startup: dict[str, Any]
    plan: dict[str, Any]
    proposal: dict[str, Any]
    parameters: dict[str, Any]
    result: dict[str, Any]
    answer: dict[str, Any]
    error: dict[str, Any]
    repair_error: dict[str, str]
    repair_needed: bool


class Agent:
    def __init__(
        self, domain: Any, database: Path, provider: Provider, trace_directory: Path
    ) -> None:
        self.domain, self.database, self.provider = domain, database, provider
        self.trace_directory = trace_directory
        self.repaired: bool = False
        self.retried: bool = False
        self.compiled = self._compile()

    def _compile(self) -> Any:
        graph = StateGraph(State)
        for name in (
            "validate_input",
            "load_schema",
            "resolve_scope",
            "plan",
            "validate_plan",
            "generate_sql",
            "validate_sql",
            "execute",
            "inspect_result",
            "answer",
            "error",
        ):
            graph.add_node(name, self._node(name))
        graph.add_edge(START, "validate_input")
        flow = [
            "validate_input",
            "load_schema",
            "resolve_scope",
            "plan",
            "validate_plan",
            "generate_sql",
            "validate_sql",
            "execute",
            "inspect_result",
            "answer",
        ]
        for name, following in pairwise(flow):
            graph.add_conditional_edges(
                name,
                lambda s, n=following: (
                    "error" if s.get("error") else ("generate_sql" if s.get("repair_needed") else n)
                ),
            )
        graph.add_edge("answer", END)
        graph.add_edge("error", END)
        return graph.compile()

    def _node(self, name: str) -> Any:
        def invoke(state: State) -> State:
            try:
                self._check_deadline()
                self.trace.emit(name, "node_start", {})
                update = self._action(name, state)
                self.trace.emit(name, "node_end", dict(update))
                return update
            except Failure as exc:
                if (
                    exc.code == "SQL_INVALID"
                    and name in ("validate_sql", "execute")
                    and not self.repaired
                ):
                    self.repaired = True
                    self.trace.emit(
                        name, "error", {"code": exc.code, "message": exc.message, "repair": True}
                    )
                    return {
                        "repair_needed": True,
                        "repair_error": {"code": exc.code, "message": exc.message},
                    }
                error = {
                    "code": exc.code,
                    "message": exc.message,
                    "failed_node": name,
                    "retryable": False,
                }
                self.trace.emit(name, "error", error)
                return {"error": error}

        return invoke

    def _check_deadline(self) -> None:
        if time.monotonic() >= self.deadline:
            raise Failure("BUDGET_EXCEEDED", "Run active-work deadline exceeded.")

    def _call(self, operation: str, state: State, output_type: Any) -> Any:
        transient_retried = False
        while True:
            self._check_deadline()
            if self.calls >= 5:
                raise Failure("BUDGET_EXCEEDED", "Provider call budget exceeded.")
            payload = {
                "question": state["question"],
                "descriptor": state["descriptor"],
                "scope": state["scope"],
                "plan": state.get("plan"),
                "previous_error": state.get("repair_error"),
            }
            if len(json.dumps(payload, ensure_ascii=False).encode()) > 12000:
                raise Failure("RESOURCE_LIMIT", "Provider payload exceeds byte gate.")
            self.calls += 1
            self.trace.emit(
                operation,
                "llm_attempt",
                {
                    "execution_profile": self.provider.profile,
                    "real_provider_called": False,
                    "phase": "application_attempt_before_dispatch",
                },
                self.calls,
            )
            try:
                result, usage = self.provider.call(
                    operation,
                    payload,
                    output_type,
                    timeout=min(15.0, self.deadline - time.monotonic()),
                )
                self._check_deadline()
                self.trace.emit(
                    operation, "llm_attempt", {"phase": "response", "usage": usage}, self.calls
                )
                return result
            except Failure as exc:
                self.trace.emit(
                    operation,
                    "error",
                    {"code": exc.code, "message": exc.message, **exc.details},
                    self.calls,
                )
                if exc.code == "PROVIDER_TRANSIENT" and not transient_retried and not self.retried:
                    transient_retried = self.retried = True
                    time.sleep(1)
                    continue
                if exc.code == "PROVIDER_TRANSIENT":
                    raise Failure("PROVIDER_UNAVAILABLE", "Transient retry exhausted.") from exc
                raise

    def _action(self, name: str, state: State) -> State:
        if name == "validate_input":
            question = state["question"]
            if not isinstance(question, str) or not 1 <= len(question.strip()) <= 2000:
                raise Failure("INVALID_INPUT", "Question must have 1..2000 characters.")
            return {}
        if name == "load_schema":
            metadata = db.inspect(self.database, self.domain.tables)
            self.snapshot = metadata["db_sha256"]
            descriptor = self.domain.descriptor()
            lock = Path(__file__).resolve().parents[2] / "uv.lock"
            metadata["lock_sha256"] = db.file_hash(lock) if lock.exists() else None
            return {
                "descriptor": descriptor,
                "startup": {
                    **metadata,
                    "schema_sha256": hashlib.sha256(
                        json.dumps(descriptor, sort_keys=True).encode()
                    ).hexdigest(),
                },
            }
        if name == "resolve_scope":
            return {"scope": self.domain.resolve(state["question"])}
        if name == "plan":
            return {"plan": self._call("plan", state, PlanProposal).model_dump()}
        if name == "validate_plan":
            self.domain.validate_plan(PlanProposal.model_validate(state["plan"]))
            return {}
        if name == "generate_sql":
            return {
                "proposal": self._call("sql", state, SQLProposal).model_dump(),
                "repair_needed": False,
            }
        if name == "validate_sql":
            proposal = SQLProposal.model_validate(state["proposal"])
            if proposal.step_id != state["plan"]["steps"][0]["step_id"]:
                raise Failure("PROVIDER_INVALID_OUTPUT", "SQL step does not match accepted plan.")
            parameters = self.domain.validate_sql(proposal, state["scope"])
            self.trace.emit(name, "sql_validated", {"sql": proposal.sql, "parameters": parameters})
            return {"parameters": parameters}
        if name == "execute":
            self.sql_attempts += 1
            if self.sql_attempts > 4:
                raise Failure("BUDGET_EXCEEDED", "SQL execution budget exceeded.")
            self.trace.emit(
                name,
                "sql_attempt",
                {"sql": state["proposal"]["sql"], "parameters": state["parameters"]},
                self.sql_attempts,
            )
            result = db.execute(
                self.database,
                state["proposal"]["sql"],
                state["parameters"],
                self.domain.tables,
                self.domain.functions,
                expected_hash=self.snapshot,
                watchdog=min(3.0, self.deadline - time.monotonic()),
            )
            result["step_id"] = state["proposal"]["step_id"]
            result["result_spec"] = self.domain.spec.model_dump()
            self.trace.emit(name, "db_result", result, self.sql_attempts)
            return {"result": result}
        if name == "inspect_result":
            if state["result"]["columns"] != [
                {"name": c.name, "type": c.type} for c in self.domain.spec.columns
            ]:
                raise Failure("RESULT_CONTRACT_INVALID", "DB columns do not match accepted spec.")
            return {"answer": self.domain.answer(state["result"]["rows"], state["scope"])}
        if name == "answer":
            self.trace.emit(name, "answer", state["answer"])
            return {}
        return {}

    def run(self, question: str) -> dict[str, Any]:
        run_id = str(uuid.uuid4())
        self.trace = Trace(self.trace_directory, run_id)
        self.deadline = time.monotonic() + 60
        self.calls = self.sql_attempts = 0
        self.retried = False
        self.repaired = False
        answer: dict[str, Any] | None = None
        try:
            self.trace.emit(
                "input",
                "input",
                {
                    "question": question,
                    "execution_profile": self.provider.profile,
                    "real_provider_called": False,
                },
            )
            state = self.compiled.invoke({"question": question}, {"recursion_limit": 32})
            error = state.get("error")
            self.trace.emit(
                "end",
                "run_end",
                {
                    "status": "error" if error else "ok",
                    "llm_calls": self.calls,
                    "sql_attempts": self.sql_attempts,
                },
            )
            answer = None if error else state["answer"]
        except (Failure, ValidationError, OSError, ValueError, KeyError, TypeError) as exc:
            error = {
                "code": exc.code if isinstance(exc, Failure) else "INTERNAL_CONTRACT",
                "message": exc.message if isinstance(exc, Failure) else "Run failed safely.",
                "failed_node": "trace"
                if isinstance(exc, Failure) and exc.code == "TRACE_UNAVAILABLE"
                else "run",
                "retryable": False,
            }
            if not self.trace.terminal and error["code"] != "TRACE_UNAVAILABLE":
                try:
                    self.trace.emit("run", "error", error)
                    self.trace.emit("end", "run_end", {"status": "error"})
                except Failure:
                    error = {
                        "code": "TRACE_UNAVAILABLE",
                        "message": "Terminal trace could not persist.",
                        "failed_node": "trace",
                        "retryable": False,
                    }
        return {
            "version": "1",
            "run_id": run_id,
            "trace_id": run_id,
            "status": "error" if error else "ok",
            "answer": answer,
            "error": error,
            "clarification": None,
            "events": self.trace.events,
            "execution_profile": self.provider.profile,
        }
