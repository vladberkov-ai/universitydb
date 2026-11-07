"""Explicit SDK adapter and persistent conservative application spending reservations."""

import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any, NamedTuple, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from universitydb.config import (
    API_BASE_URL,
    BUDGET_POLICY,
    BUFFER_USD,
    CAP_USD,
    DISPATCH_THRESHOLD_USD,
    PROFILE,
    logical_operation,
    payload_estimate,
    wire_payload,
)
from universitydb.contracts import Failure, PlanProposal, SQLProposal

T = TypeVar("T", bound=BaseModel)


class Provider(Protocol):
    profile: str

    def call(
        self,
        operation: str,
        payload: dict[str, Any],
        output_type: type[T],
        *,
        timeout: float = PROFILE.run_seconds,
    ) -> tuple[T, dict[str, Any]]: ...


class Reservation(NamedTuple):
    attempt_id: str
    amount: str


class Spending:
    """Durable per-attempt effective holds, serialized by a stable separate lock inode."""

    def __init__(
        self,
        path: Path,
        model: str,
        cap: Decimal,
        input_rate: Decimal,
        output_rate: Decimal,
        *,
        practical: bool = False,
    ) -> None:
        if any(not v.is_finite() or v <= 0 for v in (cap, input_rate, output_rate)):
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Positive finite approved cap and rates required."
            )
        if practical and (cap != Decimal(CAP_USD) or model != PROFILE.model):
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Practical I1 policy requires fixed cap 10 and Sol."
            )
        self.practical = practical
        self.threshold = Decimal(DISPATCH_THRESHOLD_USD) if practical else cap
        self.path, self.model, self.cap = path, model, cap
        self.input_rate, self.output_rate = input_rate, output_rate
        self.profile = {
            "version": 1,
            "model": model,
            "cap_usd": str(cap),
            "input_rate": str(input_rate),
            "output_rate": str(output_rate),
        }

    def _totals(self, attempts: list[dict[str, Any]]) -> dict[str, Any]:
        reserved = observed = effective = Decimal(0)
        input_tokens = output_tokens = 0
        ids: set[str] = set()
        for entry in attempts:
            if set(entry) != {
                "id",
                "reserved_usd",
                "observed_usd",
                "input_tokens",
                "output_tokens",
            }:
                raise ValueError("invalid attempt fields")
            if not isinstance(entry["id"], str) or not entry["id"] or entry["id"] in ids:
                raise ValueError("invalid attempt identity")
            ids.add(entry["id"])
            if type(entry["reserved_usd"]) is not str:
                raise ValueError("invalid reservation type")
            held = Decimal(entry["reserved_usd"])
            if not held.is_finite() or held <= 0:
                raise ValueError("invalid reservation")
            actual = Decimal(0)
            if entry["observed_usd"] is not None:
                values = [entry["input_tokens"], entry["output_tokens"]]
                if any(type(v) is not int or v < 0 for v in values):
                    raise ValueError("invalid usage")
                actual = (values[0] * self.input_rate + values[1] * self.output_rate) / 1000000
                if str(actual) != entry["observed_usd"]:
                    raise ValueError("usage accounting mismatch")
                input_tokens += values[0]
                output_tokens += values[1]
            elif entry["input_tokens"] is not None or entry["output_tokens"] is not None:
                raise ValueError("partial usage")
            reserved += held
            observed += actual
            effective += max(held, actual)
        return {
            "reserved_usd": str(reserved),
            "observed_usd": str(observed),
            "effective_usd": str(effective),
            "calls": len(attempts),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    @contextmanager
    def _transaction(self) -> Iterator[dict[str, Any]]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.path.with_name(self.path.name + ".lock")
        lock_existed = lock_path.exists()
        try:
            with lock_path.open("a+") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                if self.path.exists():
                    record = json.loads(self.path.read_text())
                    if not isinstance(record, dict) or record.get("profile") != self.profile:
                        raise ValueError("invalid or changed approval profile")
                    attempts = record.get("attempts")
                    if not isinstance(attempts, list):
                        raise ValueError("invalid attempts")
                    totals = self._totals(attempts)
                    extras = {"policy", "stop"} if "policy" in record else set()
                    if extras and (not self.practical or record["policy"] != BUDGET_POLICY):
                        raise ValueError("policy downgrade or drift")
                    if (
                        extras
                        and record["stop"] is not None
                        and not isinstance(record["stop"], dict)
                    ):
                        raise ValueError("invalid stop")
                    if set(record) != {"profile", "attempts", *totals, *extras} or any(
                        record[k] != v for k, v in totals.items()
                    ):
                        raise ValueError("invalid ledger totals")
                elif lock_existed:
                    raise ValueError("existing ledger is missing")
                else:
                    record = {"profile": self.profile, "attempts": [], **self._totals([])}
                if self.practical and "policy" not in record:
                    record.update(policy=BUDGET_POLICY, stop=None)
                    if any(a["observed_usd"] is None for a in record["attempts"]):
                        record["stop"] = {"reason": "legacy_unreconciled_hold"}
                yield record
                record.update(self._totals(record["attempts"]))
                temporary: str | None = None
                try:
                    with tempfile.NamedTemporaryFile(
                        mode="w", dir=self.path.parent, prefix=self.path.name + ".", delete=False
                    ) as stream:
                        temporary = stream.name
                        json.dump(record, stream)
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.replace(temporary, self.path)
                    temporary = None
                    directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
                    try:
                        os.fsync(directory)
                    finally:
                        os.close(directory)
                finally:
                    if temporary is not None:
                        Path(temporary).unlink(missing_ok=True)
        except (OSError, ValueError, TypeError, KeyError, ArithmeticError) as exc:
            raise Failure(
                "BUDGET_EXCEEDED", "Spending ledger unavailable or invalid; dispatch stopped."
            ) from exc

    def reserve(self, input_tokens: int = 12000, output_tokens: int = 2000) -> Reservation:
        if any(type(v) is not int or v <= 0 for v in (input_tokens, output_tokens)):
            raise Failure("BUDGET_EXCEEDED", "Invalid reservation token bounds.")
        amount = (input_tokens * self.input_rate + output_tokens * self.output_rate) / 1000000
        attempt_id = str(uuid.uuid4())
        with self._transaction() as record:
            if self.practical and record["stop"] is not None:
                raise Failure("BUDGET_EXCEEDED", "Durable accounting stop; no further dispatch.")
            if Decimal(record["effective_usd"]) + amount > self.threshold:
                raise Failure(
                    "BUDGET_EXCEEDED", "Projected accounted spend exceeds dispatch threshold."
                )
            record["attempts"].append(
                {
                    "id": attempt_id,
                    "reserved_usd": str(amount),
                    "observed_usd": None,
                    "input_tokens": None,
                    "output_tokens": None,
                }
            )
            if self.practical:
                record["stop"] = {"reason": "pending_usage", "attempt_id": attempt_id}
        return Reservation(attempt_id, str(amount))

    def record_usage(
        self,
        attempt_id: str,
        input_tokens: int,
        output_tokens: int,
        *,
        stop_reason: str | None = None,
    ) -> None:
        if any(type(v) is not int or v < 0 for v in (input_tokens, output_tokens)):
            raise Failure("BUDGET_EXCEEDED", "Invalid usage; uncertain hold retained.")
        exceeded = False
        with self._transaction() as record:
            matches = [a for a in record["attempts"] if a["id"] == attempt_id]
            if len(matches) != 1 or matches[0]["observed_usd"] is not None:
                raise Failure("BUDGET_EXCEEDED", "Usage does not match one unreconciled attempt.")
            actual = (input_tokens * self.input_rate + output_tokens * self.output_rate) / 1000000
            matches[0].update(
                observed_usd=str(actual), input_tokens=input_tokens, output_tokens=output_tokens
            )
            if self.practical:
                pending = record["stop"]
                if pending == {"reason": "pending_usage", "attempt_id": attempt_id}:
                    record["stop"] = None
                if stop_reason:
                    record["stop"] = {"reason": stop_reason, "attempt_id": attempt_id}
                if actual > Decimal(matches[0]["reserved_usd"]):
                    record["stop"] = {
                        "reason": "usage_exceeds_reservation",
                        "attempt_id": attempt_id,
                    }
            exceeded = Decimal(self._totals(record["attempts"])["effective_usd"]) > self.cap
        if exceeded:
            raise Failure(
                "BUDGET_EXCEEDED", "Observed effective spend exceeded cap; future dispatch stopped."
            )

    def stop(self, attempt_id: str, reason: str, facts: dict[str, Any]) -> None:
        """Persist only safe worker facts; retain every reservation and prior usage."""
        with self._transaction() as record:
            if self.practical:
                record["stop"] = {"attempt_id": attempt_id, "reason": reason, "facts": facts}


class OpenAIProvider:
    profile = "live"

    def __init__(self, prompts: Path, budget_path: Path) -> None:
        self.prompts, self.budget_path = prompts, budget_path

    def call(
        self,
        operation: str,
        payload: dict[str, Any],
        output_type: type[T],
        *,
        timeout: float = PROFILE.run_seconds,
    ) -> tuple[T, dict[str, Any]]:
        logical = logical_operation(operation, payload)
        policy = PROFILE.operation(logical)
        expected = PlanProposal if operation == "plan" else SQLProposal
        if output_type is not expected:
            raise Failure("PROVIDER_UNAVAILABLE", "Operation output schema mismatch.")
        # Check before client construction or any network operation; no credential values are logged.
        model = os.environ.get("UNIVERSITYDB_MODEL", "")
        if not os.environ.get("OPENAI_API_KEY") or model != PROFILE.model:
            raise Failure(
                "PROVIDER_UNAVAILABLE",
                "Missing API key or explicitly approved model; no network call.",
            )
        if os.environ.get("UNIVERSITYDB_LIVE_APPROVED") != "yes":
            raise Failure("PROVIDER_UNAVAILABLE", "Live spending is not explicitly enabled.")
        if (
            os.environ.get("UNIVERSITYDB_BUDGET_POLICY") != BUDGET_POLICY
            or os.environ.get("UNIVERSITYDB_RATES_CONFIRMED") != "yes"
        ):
            raise Failure(
                "PROVIDER_UNAVAILABLE",
                "Explicit practical policy and current applicable rates required.",
            )
        try:
            spending = Spending(
                self.budget_path,
                model,
                Decimal(os.environ["UNIVERSITYDB_CAP_USD"]),
                Decimal(os.environ["UNIVERSITYDB_INPUT_USD_PER_MILLION"]),
                Decimal(os.environ["UNIVERSITYDB_OUTPUT_USD_PER_MILLION"]),
                practical=True,
            )
        except (KeyError, ValueError, ArithmeticError) as exc:
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Approved cap and verified model rates required."
            ) from exc
        prompt = (self.prompts / f"{operation}.txt").read_text()
        encoded = json.dumps(payload, ensure_ascii=False)
        wire = wire_payload(operation, logical, model, prompt, encoded)
        payload_bytes, estimated_input = payload_estimate(wire)
        if estimated_input > PROFILE.input_bytes:
            raise Failure(
                "RESOURCE_LIMIT", "Full provider payload plus framing exceeds estimated input gate."
            )
        reservation = spending.reserve(PROFILE.input_tokens, policy.output_tokens)
        reserved = reservation.amount
        dispatch = {
            "budget_policy": BUDGET_POLICY,
            "cap_usd": CAP_USD,
            "dispatch_threshold_usd": DISPATCH_THRESHOLD_USD,
            "buffer_usd": BUFFER_USD,
            "input_estimate_method": "UTF-8 full wire JSON bytes + 1024 framing; not a bound",
            "payload_bytes": payload_bytes,
            "estimated_payload_input_tokens": estimated_input,
            "reserved_input_tokens": PROFILE.input_tokens,
            "api_base_url": API_BASE_URL,
            "accounting_stop": True,
            "requested_model": model,
            "logical_operation": logical,
            "reasoning_effort": policy.effort,
            "service_tier": PROFILE.service_tier,
            "max_output_tokens": policy.output_tokens,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "reserved_usd": reserved,
            "usage_status": "unknown",
            "dispatch_attempted": True,
            "real_provider_called": None,
        }
        wall_timeout = max(0.001, min(policy.timeout, timeout))
        request = {
            "operation": operation,
            "logical_operation": logical,
            "model": model,
            "prompt": prompt,
            "input": encoded,
            "timeout": wall_timeout,
        }
        try:
            try:
                with subprocess.Popen(
                    [sys.executable, "-m", "universitydb.llm_worker"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                ) as worker:
                    try:
                        output, _ = worker.communicate(json.dumps(request), timeout=wall_timeout)
                    except subprocess.TimeoutExpired as exc:
                        worker.kill()
                        worker.communicate()
                        raise Failure(
                            "PROVIDER_TRANSIENT",
                            "Provider wall-clock timeout; worker killed and reservation retained.",
                            details=dispatch,
                        ) from exc
                    if worker.returncode != 0:
                        raise Failure(
                            "PROVIDER_UNAVAILABLE",
                            "Provider worker failed; reservation retained.",
                            details=dispatch,
                        )
            except OSError as exc:
                raise Failure("PROVIDER_UNAVAILABLE", "Provider worker unavailable.") from exc
            try:
                data = json.loads(output)
                if not isinstance(data, dict):
                    raise TypeError("worker response must be an object")
            except (ValueError, TypeError) as exc:
                raise Failure(
                    "PROVIDER_INVALID_OUTPUT", "Provider worker response invalid.", details=dispatch
                ) from exc
            if "usage" not in data:
                raise Failure(
                    data.get("error", "PROVIDER_INVALID_OUTPUT"),
                    data.get("message", "Provider usage missing; reservation retained."),
                    details=dispatch,
                )
            usage = data["usage"]
            dispatch.update(real_provider_called=True)
            try:
                if any(
                    type(usage[k]) is not int or usage[k] < 0
                    for k in ("input_tokens", "output_tokens", "total_tokens")
                ):
                    raise ValueError("invalid usage")
            except (ValueError, KeyError, TypeError) as exc:
                raise Failure(
                    data.get("error", "PROVIDER_INVALID_OUTPUT"),
                    data.get("message", "Provider usage invalid; reservation retained."),
                    details={**dispatch, "usage": usage},
                ) from exc
            if usage["total_tokens"] != usage["input_tokens"] + usage["output_tokens"]:
                spending.stop(reservation.attempt_id, "invalid_usage_total", {"usage": usage})
                raise Failure(
                    "BUDGET_EXCEEDED",
                    "Provider usage total invalid; durable stop.",
                    details={**dispatch, "usage": usage},
                )
            dispatch.update(usage_status="known")
            excess = (
                usage["input_tokens"] > PROFILE.input_tokens
                or usage["output_tokens"] > policy.output_tokens
            )
            mismatch = (
                usage.get("returned_model") != model
                or usage.get("returned_service_tier") != PROFILE.service_tier
            )
            stop_reason = (
                "usage_exceeds_estimate"
                if excess
                else "returned_profile_mismatch"
                if mismatch
                else None
            )
            try:
                spending.record_usage(
                    reservation.attempt_id,
                    usage["input_tokens"],
                    usage["output_tokens"],
                    stop_reason=stop_reason,
                )
            except Failure as exc:
                raise Failure(exc.code, exc.message, details={**dispatch, "usage": usage}) from exc
            if excess:
                raise Failure(
                    "BUDGET_EXCEEDED",
                    "Provider usage exceeded bounds; reservation retained.",
                    details={**dispatch, "usage": usage},
                )
            if mismatch:
                raise Failure(
                    "PROVIDER_UNAVAILABLE",
                    "Returned provider profile mismatch; charge retained.",
                    details={**dispatch, "usage": usage},
                )
            if "error" in data:
                raise Failure(data["error"], data["message"], details={**dispatch, "usage": usage})
            try:
                parsed = output_type.model_validate(data["output"])
            except (ValueError, KeyError, TypeError) as exc:
                raise Failure(
                    "PROVIDER_INVALID_OUTPUT",
                    "Provider output invalid.",
                    details={**dispatch, "usage": usage},
                ) from exc
            dispatch.update(accounting_stop=False)
            return parsed, {
                **dispatch,
                **usage,
                "accounting": "practical estimate; max(reservation, usage) retained",
            }
        except Failure as exc:
            spending.stop(reservation.attempt_id, exc.code, exc.details or dispatch)
            raise Failure(
                exc.code, exc.message, details={**dispatch, **exc.details, "accounting_stop": True}
            ) from exc


class ScriptedProvider:
    """Test-only injectable transport; not selected by ordinary UI or question text."""

    profile = "offline/injected"

    def __init__(self, outputs: list[dict[str, Any] | Failure]) -> None:
        self.fixture_hash = hashlib.sha256(
            json.dumps(
                outputs, default=lambda e: {"error": e.code, "message": e.message}, sort_keys=True
            ).encode()
        ).hexdigest()
        self.outputs = iter(outputs)
        self.calls = 0

    def call(
        self,
        operation: str,
        payload: dict[str, Any],
        output_type: type[T],
        *,
        timeout: float = PROFILE.run_seconds,
    ) -> tuple[T, dict[str, Any]]:
        self.calls += 1
        try:
            value = next(self.outputs)
        except StopIteration as exc:
            raise Failure("PROVIDER_INVALID_OUTPUT", "Injected fixture exhausted.") from exc
        if isinstance(value, Failure):
            raise value
        try:
            result = output_type.model_validate(value)
        except ValidationError as exc:
            raise Failure(
                "PROVIDER_INVALID_OUTPUT", "Injected output rejected by typed contract."
            ) from exc
        return result, {
            "fixture_sha256": self.fixture_hash,
            "injection_point": "provider_transport",
            "fault_case": "scripted_fixture",
            "requested_model": "scripted-test",
            "returned_model": "scripted-test",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "real_provider_called": False,
        }
