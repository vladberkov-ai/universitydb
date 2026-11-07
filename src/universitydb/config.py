"""Single bounded I1 Responses policy; monetary approval is a separate live gate."""

import json
from dataclasses import dataclass
from typing import Any, Literal

from universitydb.contracts import Failure, PlanProposal, SQLProposal


@dataclass(frozen=True)
class Operation:
    effort: Literal["high", "medium"]
    output_tokens: int
    timeout: float


@dataclass(frozen=True)
class Profile:
    model: str = "gpt-6.1-sol"
    service_tier: Literal["default"] = "default"
    input_bytes: int = 12000
    input_tokens: int = 12000
    run_seconds: float = 180.0
    calls: int = 5

    @property
    def run_tokens(self) -> int:
        return self.calls * (self.input_tokens + self.operation("plan").output_tokens)

    def validate(self) -> None:
        # Only this reviewed profile is supported; no hidden env overrides/fallback.
        if self != Profile():
            raise Failure("PROVIDER_UNAVAILABLE", "Unsupported provider configuration.")

    def operation(self, operation: str) -> Operation:
        self.validate()
        if operation == "plan":
            return Operation("high", 32768, 60.0)
        if operation in ("sql", "repair"):
            return Operation("medium", 32768, 45.0)
        raise Failure("PROVIDER_UNAVAILABLE", "Unsupported provider operation.")


PROFILE = Profile()


def logical_operation(operation: str, payload: dict[str, Any]) -> str:
    if operation not in ("plan", "sql"):
        raise Failure("PROVIDER_UNAVAILABLE", "Unsupported provider operation.")
    return "repair" if operation == "sql" and payload.get("previous_error") else operation


BUDGET_POLICY = "practical-v1"
CAP_USD = "10"
DISPATCH_THRESHOLD_USD = "8"
BUFFER_USD = "2"
FRAMING_ESTIMATE = 1024
API_BASE_URL = "https://api.openai.com/v1"


def wire_payload(
    operation: str, logical: str, model: str, prompt: str, encoded: str
) -> dict[str, Any]:
    """One wire shape for size estimation and dispatch; not an exact token counter."""
    policy = PROFILE.operation(logical)
    output_type = PlanProposal if operation == "plan" else SQLProposal
    return {
        "model": model,
        "store": False,
        "max_output_tokens": policy.output_tokens,
        "reasoning": {"effort": policy.effort},
        "service_tier": PROFILE.service_tier,
        "instructions": prompt,
        "input": encoded,
        "text": {
            "format": {
                "type": "json_schema",
                "name": output_type.__name__,
                "strict": True,
                "schema": output_type.model_json_schema(),
            }
        },
    }


def payload_estimate(payload: dict[str, Any]) -> tuple[int, int]:
    """UTF-8 JSON bytes plus framing estimate; engineering estimate, never a bound."""
    size = len(json.dumps(payload, ensure_ascii=False).encode())
    return size, size + FRAMING_ESTIMATE
