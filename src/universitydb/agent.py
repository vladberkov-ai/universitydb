"""Schema-agnostic real compiled LangGraph orchestration for bounded typed dependent steps."""

import hashlib
import json
import time
import uuid
from copy import deepcopy
from itertools import pairwise
from pathlib import Path
from threading import RLock
from typing import Any, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import ValidationError

from universitydb import db
from universitydb.config import PROFILE, logical_operation, payload_estimate, wire_payload
from universitydb.contracts import (
    AgentOutput,
    Answer,
    Failure,
    PlanProposal,
    RunError,
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
    choices: dict[str, Any]
    clarification: dict[str, Any] | None
    counters: dict[str, int]
    active_ms: int
    created_at: float
    session_id: str
    run_id: str
    request_id: str


class Agent:
    def __init__(
        self,
        domain: Any,
        database: Path,
        provider: Provider,
        trace_directory: Path,
        *,
        session_id: str | None = None,
    ) -> None:
        self.domain, self.database, self.provider = domain, database, provider
        self.trace_directory = trace_directory
        self.repaired: bool = False
        self.retried: bool = False
        self.calls = self.sql_attempts = self.reserved_tokens = 0
        self.session_id = session_id or str(uuid.uuid4())
        self.saver = InMemorySaver()
        self._runs: dict[str, dict[str, Any]] = {}
        self._requests: dict[str, dict[str, Any]] = {}
        self._mutex = RLock()
        self.input_tokens = self.output_tokens = self.pauses = self.graph_steps = 0
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
        graph.add_node("clarify", self._clarify)
        graph.add_conditional_edges("clarify", lambda state: "resolve_scope")
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
            if name in ("resolve_scope", "validate_plan"):
                graph.add_conditional_edges(
                    name, self._after_resolution if name == "resolve_scope" else self._after_plan
                )
                continue
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
        return graph.compile(checkpointer=self.saver)

    def _after_resolution(self, state: State) -> str:
        if state.get("error"):
            return "error"
        if state.get("clarification"):
            return "clarify"
        return "validate_plan" if state.get("plan", {}).get("steps") else "plan"

    def _after_plan(self, state: State) -> str:
        if state.get("error"):
            return "error"
        return "clarify" if state.get("clarification") else "bind_results"

    def _clarify(self, state: State) -> State:
        # No trace, counter or provider effect before interrupt: this node is re-entered.
        selection = interrupt(state["clarification"])
        field = state["clarification"]["field"]  # type: ignore[index]
        plan = dict(state.get("plan", {}))
        if plan:
            plan.update(needs_clarification=False, clarification_field=None)
        self.trace.emit(
            "clarify", "clarification_resumed", {"field": field, "selection": selection}
        )
        return {
            "choices": {**state.get("choices", {}), field: selection},
            "clarification": None,
            "plan": plan,
            **self._counter_state(),
        }

    def _counter_state(self) -> State:
        return {
            "counters": {
                "llm_calls": self.calls,
                "sql_attempts": self.sql_attempts,
                "repairs": int(self.repaired),
                "clarifications": self.pauses,
                "graph_steps": self.graph_steps,
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "reserved_tokens": self.reserved_tokens,
                "transient_retries": int(self.retried),
            },
            "request_id": self.trace.request_id,
            "active_ms": max(
                0, int((PROFILE.run_seconds - max(0.0, self.deadline - time.monotonic())) * 1000)
            ),
        }

    def _pause(self, state: State, details: dict[str, Any], prompt: str) -> State:
        if self.pauses >= 2:
            raise Failure("CLARIFICATION_LIMIT", "At most two clarification pauses are allowed.")
        field, options = details.get("field"), details.get("options")
        if (
            not isinstance(field, str)
            or not isinstance(options, list)
            or not 2 <= len(options) <= 100
        ):
            raise Failure("INVALID_SELECTION", "No bounded grounded clarification choices.")
        seen: list[Any] = []
        for option in options:
            if (
                not isinstance(option, dict)
                or type(option.get("value")) not in (int, str)
                or option["value"] in seen
                or not isinstance(option.get("label"), str)
            ):
                raise Failure("INVALID_SELECTION", "Invalid grounded clarification options.")
            seen.append(option["value"])
        self.pauses += 1
        clarification = {
            "field": field,
            "options": options,
            "prompt": prompt,
            "clarification_id": str(uuid.uuid4()),
        }
        self.trace.emit("clarify", "clarification_required", clarification)
        return {"clarification": clarification}

    def _after_result(self, state: State) -> str:
        if state.get("error"):
            return "error"
        return "bind_results" if state["step_index"] < len(state["plan"]["steps"]) else "answer"

    def _node(self, name: str) -> Any:
        def invoke(state: State) -> State:
            try:
                self._check_deadline()
                self.graph_steps += 1
                if self.graph_steps > 64:
                    raise Failure("BUDGET_EXCEEDED", "Persisted graph-step budget exceeded.")
                self.trace.emit(name, "node_start", {})
                update = self._action(name, state)
                self.trace.emit(name, "node_end", dict(update))
                return {**update, **self._counter_state()}
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
                        **self._counter_state(),
                    }
                error = {
                    "code": exc.code,
                    "message": exc.message,
                    "failed_node": name,
                    "retryable": False,
                }
                RunError.model_validate(error)
                self.trace.emit(name, "error", error)
                return {"error": error, **self._counter_state()}

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
                "budgets": {
                    "calls_remaining": PROFILE.calls - self.calls,
                    "sql_remaining": 4 - self.sql_attempts,
                    "repair_available": not self.repaired,
                },
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
                self._check_deadline()
                result, usage = self.provider.call(
                    operation,
                    payload,
                    output_type,
                    timeout=min(policy.timeout, self.deadline - time.monotonic()),
                )
                self._check_deadline()
                if (
                    not isinstance(usage, dict)
                    or any(
                        type(usage.get(key)) is not int or usage[key] < 0
                        for key in ("input_tokens", "output_tokens", "total_tokens")
                    )
                    or usage["total_tokens"] != usage["input_tokens"] + usage["output_tokens"]
                    or usage.get("accounting_stop")
                ):
                    raise Failure(
                        "PROVIDER_INVALID_OUTPUT",
                        "Provider usage is unknown or inconsistent.",
                        details={"accounting_stop": True},
                    )
                if (
                    usage["input_tokens"] > PROFILE.input_tokens
                    or usage["output_tokens"] > policy.output_tokens
                ):
                    raise Failure(
                        "BUDGET_EXCEEDED",
                        "Provider usage exceeded request bounds.",
                        details={"accounting_stop": True},
                    )
                self.input_tokens += usage["input_tokens"]
                self.output_tokens += usage["output_tokens"]
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
            try:
                scope = self.domain.resolve(
                    state["question"], self.domain.catalog(self.database), state.get("choices", {})
                )
            except Failure as exc:
                if exc.code != "CLARIFICATION_REQUIRED":
                    raise
                return self._pause(state, exc.details, exc.message)
            return {"scope": scope, "clarification": None}
        if name == "plan":
            return {"plan": self._call("plan", state, PlanProposal).model_dump()}
        if name == "validate_plan":
            plan = PlanProposal.model_validate(state["plan"])
            if plan.needs_clarification:
                field = plan.clarification_field
                if not field or field in state.get("choices", {}):
                    raise Failure("PLAN_INVALID", "Repeated or missing clarification field.")
                for step in plan.steps:
                    self.domain.accept_spec(step.result_spec)
                options = self.domain.clarification_options(
                    field, self.domain.catalog(self.database)
                )
                return self._pause(
                    state,
                    {"field": field, "options": options},
                    "Choose an explicit value for " + field + ".",
                )
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
            try:
                Answer.model_validate(adapted["answer"])
            except ValidationError as exc:
                raise Failure(
                    "INTERNAL_CONTRACT", "Adapter answer violates the public contract."
                ) from exc
            dependency = {
                **state["result"],
                "rows": adapted["dependency_rows"],
                "row_count": len(adapted["dependency_rows"]),
            }
            completed = {**state["completed"], step.step_id: dependency}
            step_results = [
                *state["step_results"],
                {"step_id": step.step_id, "raw": state["result"], **adapted},
            ]
            retained = {
                "result": state["result"],
                "completed": completed,
                "step_results": step_results,
                "answer": adapted["answer"],
            }
            if len(json.dumps(retained, ensure_ascii=False, allow_nan=False).encode()) > 131072:
                raise Failure("RESOURCE_LIMIT", "Retained run result payload exceeds byte limit.")
            self.trace.emit(name, "adapted_result", {"step_id": step.step_id, **adapted})
            return {
                "answer": adapted["answer"],
                "completed": completed,
                "step_results": step_results,
                "step_index": state["step_index"] + 1,
            }
        if name == "answer":
            self.trace.emit(name, "answer", state["answer"])
            return {}
        return {}

    def _now(self) -> float:
        return time.time()

    def _identity(self) -> tuple[str, str]:
        descriptor = json.dumps(self.domain.descriptor(), sort_keys=True)
        schema = hashlib.sha256(descriptor.encode()).hexdigest()
        prompts = "".join(
            (Path(__file__).parent / "prompts" / f"{op}.txt").read_text() for op in ("plan", "sql")
        )
        policy = hashlib.sha256((descriptor + prompts + str(PROFILE)).encode()).hexdigest()
        return schema, policy

    def _failure(self, code: str, message: str, run_id: str = "") -> dict[str, Any]:
        error = RunError.model_validate(
            {"code": code, "message": message, "failed_node": "resume", "retryable": False}
        )
        return {
            "version": "1",
            "run_id": run_id,
            "trace_id": run_id,
            "status": "error",
            "answer": None,
            "clarification": None,
            "error": error.model_dump(),
            "events": [],
            "step_results": [],
            "execution_profile": self.provider.profile,
        }

    def _fingerprint(self, payload: dict[str, Any]) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, allow_nan=False).encode()
        ).hexdigest()

    def _request(self, request_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(request_id, str) or not 1 <= len(request_id) <= 128:
            raise Failure("INVALID_INPUT", "Invalid request identity.")
        existing = self._requests.get(request_id)
        if existing:
            if existing["fingerprint"] != self._fingerprint(payload):
                raise Failure(
                    "REPLAY_CONFLICT", "Request identity was reused with a different payload."
                )
            return dict(deepcopy(existing["result"]))
        return None

    def _remember(self, request_id: str, payload: dict[str, Any], result: dict[str, Any]) -> None:
        self._requests[request_id] = {
            "fingerprint": self._fingerprint(payload),
            "result": deepcopy(result),
        }
        while len(self._requests) > 32:
            del self._requests[next(iter(self._requests))]

    def _restore(self, context: dict[str, Any]) -> None:
        self.trace = context["trace"]
        self.trace.request_id = context["request_id"]
        snapshot = self.compiled.get_state(context["config"])
        state = snapshot.values
        counts = state.get("counters", {})
        if state:
            expected = {
                "llm_calls",
                "sql_attempts",
                "repairs",
                "clarifications",
                "graph_steps",
                "input_tokens",
                "output_tokens",
                "reserved_tokens",
                "transient_retries",
            }
            if (
                not isinstance(counts, dict)
                or set(counts) != expected
                or any(type(value) is not int or value < 0 for value in counts.values())
                or counts["llm_calls"] > PROFILE.calls
                or counts["sql_attempts"] > 4
                or counts["repairs"] > 1
                or counts["clarifications"] > 2
                or counts["transient_retries"] > 1
                or counts["graph_steps"] > 64
                or counts["reserved_tokens"] > PROFILE.run_tokens
                or counts["input_tokens"] + counts["output_tokens"] > PROFILE.run_tokens
            ):
                raise Failure("BUDGET_EXCEEDED", "Checkpoint counters are inconsistent.")
            if (
                type(state.get("active_ms")) is not int
                or state["active_ms"] < 0
                or state["active_ms"] >= PROFILE.run_seconds * 1000
            ):
                raise Failure("BUDGET_EXCEEDED", "Checkpoint active-work budget is exhausted.")
            if (
                state.get("session_id") != self.session_id
                or state.get("run_id") != context["run_id"]
            ):
                raise Failure("RESUME_FORBIDDEN", "Checkpoint is not bound to this server run.")
        self.calls = counts.get("llm_calls", 0)
        self.sql_attempts = counts.get("sql_attempts", 0)
        self.reserved_tokens = counts.get("reserved_tokens", 0)
        self.repaired = bool(counts.get("repairs", 0))
        self.retried = bool(counts.get("transient_retries", 0))
        self.pauses = counts.get("clarifications", 0)
        self.graph_steps = counts.get("graph_steps", 0)
        self.input_tokens = counts.get("input_tokens", 0)
        self.output_tokens = counts.get("output_tokens", 0)
        self.deadline = time.monotonic() + max(
            0, PROFILE.run_seconds - state.get("active_ms", 0) / 1000
        )
        self.snapshot = context.get("data_sha256", "")

    def _execute_graph(self, context: dict[str, Any], graph_input: Any) -> dict[str, Any]:
        self.trace = context["trace"]
        run_id = context["run_id"]
        state: dict[str, Any] = {}
        error = None
        answer = None
        clarification = None
        try:
            self._restore(context)
            if isinstance(graph_input, dict):
                self.trace.emit(
                    "input",
                    "input",
                    {
                        "question": graph_input["question"],
                        "execution_profile": self.provider.profile,
                        "real_provider_called": False,
                        "fixture_sha256": getattr(self.provider, "fixture_hash", None),
                    },
                )
            else:
                self.trace.emit("resume", "resume", {"request_id": context["resume_request_id"]})
            state = self.compiled.invoke(graph_input, context["config"])
            error = state.get("error")
            if state.get("startup"):
                context["data_sha256"] = state["startup"]["db_sha256"]
                context["schema_sha256"], context["policy_sha256"] = self._identity()
            if state.get("__interrupt__"):
                snapshot = self.compiled.get_state(context["config"])
                schema, policy = self._identity()
                context["data_sha256"] = state["startup"]["db_sha256"]
                clarification = {
                    **state["clarification"],
                    "session_id": self.session_id,
                    "run_id": run_id,
                    "checkpoint_id": snapshot.config["configurable"]["checkpoint_id"],
                    "schema_sha256": schema,
                    "data_sha256": context["data_sha256"],
                    "policy_sha256": policy,
                    "expires_at": context["created_at"] + 900,
                }
                context["continuation"] = deepcopy(clarification)
                self.trace.emit("clarify", "checkpoint_paused", clarification)
            else:
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
                context["terminal"] = True
        except (
            Failure,
            ValidationError,
            GraphRecursionError,
            OSError,
            ValueError,
            KeyError,
            TypeError,
        ) as exc:
            error = {
                "code": exc.code
                if isinstance(exc, Failure)
                else "BUDGET_EXCEEDED"
                if isinstance(exc, GraphRecursionError)
                else "INTERNAL_CONTRACT",
                "message": exc.message if isinstance(exc, Failure) else "Run failed safely.",
                "failed_node": "trace"
                if isinstance(exc, Failure) and exc.code == "TRACE_UNAVAILABLE"
                else "run",
                "retryable": False,
            }
            context["terminal"] = True
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
        result = {
            "version": "1",
            "run_id": run_id,
            "trace_id": run_id,
            "status": "error" if error else "clarification" if clarification else "ok",
            "answer": answer if not error else None,
            "error": error,
            "clarification": clarification if not error else None,
            "events": deepcopy(self.trace.events),
            "execution_profile": self.provider.profile,
            "step_results": state.get("step_results", []),
        }
        try:
            AgentOutput.model_validate(result)
        except ValidationError:
            # Adapter answers are validated before success tracing; this protects envelope assembly.
            result = self._failure(
                "INTERNAL_CONTRACT", "Output envelope violates its contract.", run_id
            )
            result["events"] = deepcopy(self.trace.events)
        context["result"] = deepcopy(result)
        return result

    def _validate_replay_binding(self, run_id: str) -> None:
        context = self._runs.get(run_id)
        if context is None:
            raise Failure("RESUME_EXPIRED", "Request context was evicted.")
        if not context.get("terminal") and self._now() > context["created_at"] + 900:
            raise Failure("RESUME_EXPIRED", "Paused request replay has expired.")
        if context.get("data_sha256"):
            schema, policy = self._identity()
            if schema != context["schema_sha256"] or policy != context["policy_sha256"]:
                raise Failure("STALE_RESUME", "Schema or policy changed since request.")
            if not self.database.is_file() or db.file_hash(self.database) != context["data_sha256"]:
                raise Failure("DATA_INCONSISTENT", "Database changed since request.")

    def run(
        self, question: str, *, request_id: str | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        with self._mutex:
            request_id = request_id or str(uuid.uuid4())
            payload = {"kind": "run", "question": question, "session_id": self.session_id}
            try:
                if session_id is not None and session_id != self.session_id:
                    raise Failure("RESUME_FORBIDDEN", "Request belongs to another server session.")
                if not isinstance(question, str):
                    raise Failure("INVALID_INPUT", "Question must be a string.")
                replay = self._request(request_id, payload)
                if replay is not None:
                    self._validate_replay_binding(replay["run_id"])
                    return replay
                # Retain at most eight session runs. Evict only exact owned terminal/expired threads.
                if len(self._runs) >= 8:
                    candidates = [
                        key
                        for key, value in self._runs.items()
                        if value.get("terminal") or self._now() > value["created_at"] + 900
                    ]
                    if not candidates:
                        raise Failure("RESOURCE_LIMIT", "Too many pending session runs.")
                    old = candidates[0]
                    self.saver.delete_thread(old)
                    del self._runs[old]
                    for key in list(self._requests):
                        if self._requests[key]["result"]["run_id"] == old:
                            del self._requests[key]
                run_id = str(uuid.uuid4())
                context = {
                    "run_id": run_id,
                    "trace": Trace(self.trace_directory, run_id),
                    "created_at": self._now(),
                    "request_id": request_id,
                    "config": {"configurable": {"thread_id": run_id}, "recursion_limit": 32},
                }
                self._runs[run_id] = context
                result = self._execute_graph(
                    context,
                    {
                        "question": question,
                        "choices": {},
                        "created_at": context["created_at"],
                        "session_id": self.session_id,
                        "run_id": run_id,
                    },
                )
                self._remember(request_id, payload, result)
                return result
            except (Failure, TypeError, ValueError) as exc:
                return self._failure(
                    exc.code if isinstance(exc, Failure) else "INVALID_INPUT",
                    exc.message if isinstance(exc, Failure) else "Invalid request.",
                )

    def resume(
        self,
        continuation: dict[str, Any],
        selection: int | str,
        *,
        request_id: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        with self._mutex:
            submitted_run_id = (
                continuation.get("run_id", "") if isinstance(continuation, dict) else ""
            )
            run_id = (
                submitted_run_id
                if isinstance(submitted_run_id, str) and len(submitted_run_id) <= 128
                else ""
            )
            context: dict[str, Any] | None = None
            terminal_binding_failure = False
            try:
                if (
                    not isinstance(continuation, dict)
                    or continuation.get("session_id") != self.session_id
                    or session_id is not None
                    and session_id != self.session_id
                ):
                    raise Failure(
                        "RESUME_FORBIDDEN", "Continuation belongs to another server session."
                    )
                context = self._runs.get(run_id)
                if context is None:
                    raise Failure(
                        "RESUME_EXPIRED", "Checkpoint is absent or expired after restart."
                    )
                if self._now() > context["created_at"] + 900:
                    raise Failure("RESUME_EXPIRED", "Clarification has expired.")
                schema, policy = self._identity()
                if context.get("schema_sha256") != schema or context.get("policy_sha256") != policy:
                    terminal_binding_failure = True
                    raise Failure("STALE_RESUME", "Schema or policy changed since checkpoint.")
                if (
                    continuation.get("schema_sha256") != schema
                    or continuation.get("policy_sha256") != policy
                ):
                    raise Failure("STALE_RESUME", "Submitted schema or policy identity is stale.")
                if not self.database.is_file() or db.file_hash(self.database) != context.get(
                    "data_sha256"
                ):
                    raise Failure("DATA_INCONSISTENT", "Database changed since checkpoint.")
                payload = {
                    "kind": "resume",
                    "continuation": continuation,
                    "selection": selection,
                    "session_id": self.session_id,
                }
                replay = self._request(request_id, payload)
                if replay is not None:
                    return replay
                if context.get("terminal") or continuation != context.get("continuation"):
                    raise Failure(
                        "STALE_RESUME", "Continuation is not the latest pending checkpoint."
                    )
                snapshot = self.compiled.get_state(context["config"])
                if not snapshot.interrupts or snapshot.config["configurable"][
                    "checkpoint_id"
                ] != continuation.get("checkpoint_id"):
                    raise Failure("STALE_RESUME", "Checkpoint is not pending.")
                if type(selection) not in (int, str) or not any(
                    type(option["value"]) is type(selection) and option["value"] == selection
                    for option in continuation["options"]
                ):
                    raise Failure(
                        "INVALID_SELECTION", "Selection is not one of the offered choices."
                    )
                context["resume_request_id"] = request_id
                context["request_id"] = request_id
                result = self._execute_graph(context, Command(resume=selection))
                self._remember(request_id, payload, result)
                return result
            except (Failure, OSError, ValueError, KeyError, TypeError) as exc:
                result = self._failure(
                    exc.code if isinstance(exc, Failure) else "INVALID_SELECTION",
                    exc.message if isinstance(exc, Failure) else "Invalid continuation.",
                    run_id,
                )
                if context is not None:
                    trace = context["trace"]
                    if not trace.terminal:
                        trace.request_id = (
                            request_id
                            if isinstance(request_id, str) and 1 <= len(request_id) <= 128
                            else "invalid"
                        )
                        try:
                            trace.emit("resume", "resume_rejected", result["error"])
                            if terminal_binding_failure or result["error"]["code"] in {
                                "RESUME_EXPIRED",
                                "DATA_INCONSISTENT",
                                "TRACE_UNAVAILABLE",
                            }:
                                trace.emit("end", "run_end", {"status": "error"})
                                context["terminal"] = True
                        except Failure:
                            result = self._failure(
                                "TRACE_UNAVAILABLE", "Rejection trace failed.", run_id
                            )
                            context["terminal"] = True
                    result["events"] = deepcopy(trace.events)
                return result
