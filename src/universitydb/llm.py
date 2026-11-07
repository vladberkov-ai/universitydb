"""Explicit SDK adapter and persistent conservative application spending reservations."""

import fcntl
import hashlib
import json
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol, TypeVar

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


class Spending:
    """All UI submissions share one local ledger. Ambiguous failed charges stay reserved."""

    def __init__(
        self, path: Path, model: str, cap: Decimal, input_rate: Decimal, output_rate: Decimal
    ) -> None:
        if any(not v.is_finite() or v <= 0 for v in (cap, input_rate, output_rate)):
            raise Failure(
                "PROVIDER_UNAVAILABLE", "Positive finite approved cap and rates required."
            )
        self.path, self.model, self.cap = path, model, cap
        self.input_rate, self.output_rate = input_rate, output_rate

    def reserve(self) -> str:
        amount = (12000 * self.input_rate + 2000 * self.output_rate) / 1000000
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a+", encoding="utf8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.seek(0)
            text = stream.read()
            record: dict[str, Any] = (
                json.loads(text) if text else {"model": self.model, "reserved_usd": "0", "calls": 0}
            )
            if record["model"] != self.model:
                raise Failure("PROVIDER_UNAVAILABLE", "Budget ledger belongs to another model.")
            total = Decimal(record["reserved_usd"]) + amount
            if total > self.cap:
                raise Failure("BUDGET_EXCEEDED", "Projected total spend exceeds approved cap.")
            record.update(reserved_usd=str(total), calls=record["calls"] + 1)
            stream.seek(0)
            stream.truncate()
            json.dump(record, stream)
            stream.flush()
            os.fsync(stream.fileno())
        return str(amount)

    def record_usage(self, input_tokens: int, output_tokens: int) -> None:
        actual = (input_tokens * self.input_rate + output_tokens * self.output_rate) / 1000000
        with self.path.open("r+", encoding="utf8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            record = json.load(stream)
            record["observed_usd"] = str(Decimal(record.get("observed_usd", "0")) + actual)
            record["input_tokens"] = record.get("input_tokens", 0) + input_tokens
            record["output_tokens"] = record.get("output_tokens", 0) + output_tokens
            stream.seek(0)
            stream.truncate()
            json.dump(record, stream)
            stream.flush()
            os.fsync(stream.fileno())
        # Conservative holds are intentionally not freed even after known success.


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
        reserved = spending.reserve()
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
        spending.record_usage(usage["input_tokens"], usage["output_tokens"])
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
