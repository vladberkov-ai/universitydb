"""Schema-agnostic real compiled LangGraph orchestration for bounded typed dependent steps."""

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
from universitydb.config import PROFILE, logical_operation, payload_estimate, wire_payload
from universitydb.contracts import (
    Failure,
    PlanProposal,
    SQLProposal,
    Step,
    bindings,
    materialize_refs,
    validate_dag,
    validate_result,
)
from universitydb.llm import Provider
from universitydb.sql_policy import validate_sql as validate_safe_sql
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
    step_index: int
    completed: dict[str, dict[str, Any]]
    step_results: list[dict[str, Any]]
    resolved_refs: dict[str, list[Any]]
    skip_step: bool


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
            "bind_results",
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
            "bind_results",
            "generate_sql",
            "validate_sql",
            "execute",
            "inspect_result",
            "answer",
        ]
        for name, following in pairwise(flow):
            if name == "bind_results":
                graph.add_conditional_edges(
                    name,
                    lambda s: (
                        "error"
                        if s.get("error")
                        else ("inspect_result" if s.get("skip_step") else "generate_sql")
                    ),
                )
                continue
            if name == "inspect_result":
                graph.add_conditional_edges(name, self._after_result)
                continue
            graph.add_conditional_edges(
                name,
                lambda s, n=following: (
                    "error" if s.get("error") else ("generate_sql" if s.get("repair_needed") else n)
                ),
            )
        graph.add_edge("answer", END)
        graph.add_edge("error", END)
        return graph.compile()

    def _after_result(self, state: State) -> str:
        if state.get("error"):
            return "error"
        return "bind_results" if state["step_index"] < len(state["plan"]["steps"]) else "answer"

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
            if self.calls >= PROFILE.calls:
                raise Failure("BUDGET_EXCEEDED", "Provider call budget exceeded.")
            payload = {
                "question": state["question"],
                "descriptor": state["descriptor"],
                "scope": state["scope"],
                "step": state["plan"]["steps"][state.get("step_index", 0)]
                if operation == "sql"
                else None,
                "resolved_refs": state.get("resolved_refs", {}),
                "previous_error": state.get("repair_error"),
            }
            if len(json.dumps(payload, ensure_ascii=False).encode()) > PROFILE.input_bytes:
                raise Failure("RESOURCE_LIMIT", "Provider payload exceeds byte gate.")
            logical = logical_operation(operation, payload)
            prompt = (Path(__file__).parent / "prompts" / f"{operation}.txt").read_text()
            wire = wire_payload(
                operation, logical, PROFILE.model, prompt, json.dumps(payload, ensure_ascii=False)
            )
            _, estimated = payload_estimate(wire)
            if estimated > PROFILE.input_bytes:
                raise Failure("RESOURCE_LIMIT", "Full provider wire exceeds estimated input gate.")
            policy = PROFILE.operation(logical)
            projected = PROFILE.input_tokens + policy.output_tokens
            if self.reserved_tokens + projected > PROFILE.run_tokens:
                raise Failure("BUDGET_EXCEEDED", "Run token reservation limit exceeded.")
            self.reserved_tokens += projected
            self.calls += 1
            self.trace.emit(
                operation,
                "llm_attempt",
                {
                    "execution_profile": self.provider.profile,
                    "real_provider_called": False,
                    "phase": "application_attempt_before_dispatch",
                    "logical_operation": logical,
                    "requested_model": PROFILE.model
                    if self.provider.profile == "live"
                    else "scripted-test",
                    "reasoning_effort": policy.effort,
                    "service_tier": PROFILE.service_tier,
                    "max_output_tokens": policy.output_tokens,
                    "reserved_run_tokens": self.reserved_tokens,
                },
                self.calls,
            )
            try:
                result, usage = self.provider.call(
                    operation,
                    payload,
                    output_type,
                    timeout=min(policy.timeout, self.deadline - time.monotonic()),
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
                if exc.details.get("accounting_stop"):
                    raise
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
            self.domain.inspect_data(self.database)
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
            return {
                "scope": self.domain.resolve(state["question"], self.domain.catalog(self.database))
            }
        if name == "plan":
            return {"plan": self._call("plan", state, PlanProposal).model_dump()}
        if name == "validate_plan":
            plan = PlanProposal.model_validate(state["plan"])
            validate_dag(plan)
            self.domain.validate_plan(plan)
            if self.calls + len(plan.steps) > PROFILE.calls:
                raise Failure("BUDGET_EXCEEDED", "Plan exceeds remaining call budget.")
            return {"step_index": 0, "completed": {}, "step_results": []}
        if name == "bind_results":
            step = Step.model_validate(state["plan"]["steps"][state["step_index"]])
            refs = materialize_refs(
                step,
                state["completed"],
                {
                    entry["step_id"]: Step.model_validate(entry).result_spec
                    for entry in state["plan"]["steps"]
                },
            )
            self.trace.emit(name, "dependency_bindings", {"step_id": step.step_id, "values": refs})
            empty = any(not values for values in refs.values())
            update: State = {
                "resolved_refs": refs,
                "repair_error": {},
                "repair_needed": False,
                "skip_step": empty,
            }
            if empty:
                update["result"] = {
                    "step_id": step.step_id,
                    "result_spec": step.result_spec.model_dump(),
                    "columns": [{"name": c.name, "type": c.type} for c in step.result_spec.columns],
                    "rows": [],
                    "row_count": 0,
                    "truncated": False,
                    "elapsed_ms": 0,
                }
                self.trace.emit(name, "dependency_empty", {"step_id": step.step_id})
            return update
        if name == "generate_sql":
            return {
                "proposal": self._call("sql", state, SQLProposal).model_dump(),
                "repair_needed": False,
            }
        if name == "validate_sql":
            proposal = SQLProposal.model_validate(state["proposal"])
            if proposal.step_id != state["plan"]["steps"][state["step_index"]]["step_id"]:
                raise Failure("PROVIDER_INVALID_OUTPUT", "SQL step does not match accepted plan.")
            step = Step.model_validate(state["plan"]["steps"][state["step_index"]])
            if proposal.result_spec != step.result_spec:
                raise Failure("RESULT_CONTRACT_INVALID", "SQL spec differs from accepted step.")
            validate_safe_sql(
                proposal.sql,
                bindings(proposal.parameters),
                self.domain.tables,
                self.domain.functions,
            )
            parameters = self.domain.validate_sql(
                proposal, state["scope"], step=step, resolved_refs=state["resolved_refs"]
            )
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
                result_spec=SQLProposal.model_validate(state["proposal"]).result_spec,
                step_id=state["proposal"]["step_id"],
                watchdog=min(3.0, self.deadline - time.monotonic()),
            )
            result["step_id"] = state["proposal"]["step_id"]
            result["result_spec"] = state["proposal"]["result_spec"]
            self.trace.emit(name, "db_result", result, self.sql_attempts)
            return {"result": result}
        if name == "inspect_result":
            step = Step.model_validate(state["plan"]["steps"][state["step_index"]])
            validate_result(state["result"], step.result_spec)
            adapted = self.domain.adapt_result(
                state["result"]["rows"], step.result_spec, state["scope"]
            )
            dependency = {
                **state["result"],
                "rows": adapted["dependency_rows"],
                "row_count": len(adapted["dependency_rows"]),
            }
            completed = {**state["completed"], step.step_id: dependency}
            if len(json.dumps(completed).encode()) > 131072:
                raise Failure("RESOURCE_LIMIT", "Retained step results exceed byte limit.")
            self.trace.emit(name, "adapted_result", {"step_id": step.step_id, **adapted})
            return {
                "answer": adapted["answer"],
                "completed": completed,
                "step_results": [
                    *state["step_results"],
                    {"step_id": step.step_id, "raw": state["result"], **adapted},
                ],
                "step_index": state["step_index"] + 1,
            }
        if name == "answer":
            self.trace.emit(name, "answer", state["answer"])
            return {}
        return {}

    def run(self, question: str) -> dict[str, Any]:
        run_id = str(uuid.uuid4())
        self.trace = Trace(self.trace_directory, run_id)
        self.deadline = time.monotonic() + PROFILE.run_seconds
        self.calls = self.sql_attempts = self.reserved_tokens = 0
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
            "step_results": state.get("step_results", []) if "state" in locals() else [],
        }
