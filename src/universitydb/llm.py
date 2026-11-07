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

from universitydb.contracts import Failure

T = TypeVar("T", bound=BaseModel)


class Provider(Protocol):
    profile: str

    def call(
        self,
        operation: str,
        payload: dict[str, Any],
        output_type: type[T],
        *,
        timeout: float = 15.0,
    ) -> tuple[T, dict[str, Any]]: ...


class Reservation(NamedTuple):
    attempt_id: str
    amount: str


class Spending:
    """Durable per-attempt effective holds, serialized by a stable separate lock inode."""

    def __init__(
        self, path: Path, model: str, cap: Decimal, input_rate: Decimal, output_rate: Decimal
    ) -> None:
        if any(not v.is_finite() or v <= 0 for v in (cap, input_rate, output_rate)):
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Positive finite approved cap and rates required."
            )
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
                    if set(record) != {"profile", "attempts", *totals} or any(
                        record[k] != v for k, v in totals.items()
                    ):
                        raise ValueError("invalid ledger totals")
                elif lock_existed:
                    raise ValueError("existing ledger is missing")
                else:
                    record = {"profile": self.profile, "attempts": [], **self._totals([])}
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

    def reserve(self) -> Reservation:
        amount = (12000 * self.input_rate + 2000 * self.output_rate) / 1000000
        attempt_id = str(uuid.uuid4())
        with self._transaction() as record:
            if Decimal(record["effective_usd"]) + amount > self.cap:
                raise Failure("BUDGET_EXCEEDED", "Projected effective spend exceeds approved cap.")
            record["attempts"].append(
                {
                    "id": attempt_id,
                    "reserved_usd": str(amount),
                    "observed_usd": None,
                    "input_tokens": None,
                    "output_tokens": None,
                }
            )
        return Reservation(attempt_id, str(amount))

    def record_usage(self, attempt_id: str, input_tokens: int, output_tokens: int) -> None:
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
            exceeded = Decimal(self._totals(record["attempts"])["effective_usd"]) > self.cap
        if exceeded:
            raise Failure(
                "BUDGET_EXCEEDED", "Observed effective spend exceeded cap; future dispatch stopped."
            )


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
        timeout: float = 15.0,
    ) -> tuple[T, dict[str, Any]]:
        # Check before client construction or any network operation; no credential values are logged.
        model = os.environ.get("UNIVERSITYDB_MODEL", "")
        if not os.environ.get("OPENAI_API_KEY") or not model:
            raise Failure(
                "PROVIDER_UNAVAILABLE",
                "Missing API key or explicitly approved model; no network call.",
            )
        if os.environ.get("UNIVERSITYDB_LIVE_APPROVED") != "yes":
            raise Failure("PROVIDER_UNAVAILABLE", "Live spending is not explicitly enabled.")
        try:
            spending = Spending(
                self.budget_path,
                model,
                Decimal(os.environ["UNIVERSITYDB_CAP_USD"]),
                Decimal(os.environ["UNIVERSITYDB_INPUT_USD_PER_MILLION"]),
                Decimal(os.environ["UNIVERSITYDB_OUTPUT_USD_PER_MILLION"]),
            )
        except (KeyError, ValueError, ArithmeticError) as exc:
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Approved cap and verified model rates required."
            ) from exc
        prompt = (self.prompts / f"{operation}.txt").read_text()
        encoded = json.dumps(payload, ensure_ascii=False)
        if len((prompt + encoded).encode()) > 12000:
            raise Failure("RESOURCE_LIMIT", "Provider input exceeds byte gate.")
        reservation = spending.reserve()
        reserved = reservation.amount
        dispatch = {
            "requested_model": model,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "reserved_usd": reserved,
            "usage_status": "unknown",
            "dispatch_attempted": True,
            "real_provider_called": None,
        }
        request = {"operation": operation, "model": model, "prompt": prompt, "input": encoded}
        try:
            with subprocess.Popen(
                [sys.executable, "-m", "universitydb.llm_worker"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            ) as worker:
                try:
                    output, _ = worker.communicate(
                        json.dumps(request), timeout=max(0.001, min(15.0, timeout))
                    )
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
            if "error" in data:
                raise Failure(data["error"], data["message"], details=dispatch)
            parsed = output_type.model_validate(data["output"])
            usage = data["usage"]
            if any(
                type(usage[k]) is not int or usage[k] < 0
                for k in ("input_tokens", "output_tokens", "total_tokens")
            ):
                raise Failure("PROVIDER_INVALID_OUTPUT", "Invalid provider usage.")
        except (ValueError, KeyError, TypeError) as exc:
            raise Failure(
                "PROVIDER_INVALID_OUTPUT", "Provider worker response invalid.", details=dispatch
            ) from exc
        try:
            spending.record_usage(
                reservation.attempt_id, usage["input_tokens"], usage["output_tokens"]
            )
        except Failure as exc:
            raise Failure(exc.code, exc.message, details={**dispatch, "usage": usage}) from exc
        if usage["input_tokens"] > 12000 or usage["output_tokens"] > 2000:
            raise Failure(
                "BUDGET_EXCEEDED",
                "Provider usage exceeded bounds; reservation retained.",
                details={**dispatch, "usage": usage},
            )
        return parsed, {
            **usage,
            "requested_model": model,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "reserved_usd": reserved,
            "accounting": "conservative reservation retained including unused tokens",
            "real_provider_called": True,
        }


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
        timeout: float = 15.0,
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
