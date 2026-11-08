"""Single bounded I1 Responses policy; monetary approval is a separate live gate."""

import json
from dataclasses import dataclass
from typing import Any, Literal, TypedDict

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


# H015 is an explicit fixed successor authorization, never an environment cap override.
H015_POLICY: Literal["h015-practical-v1"] = "h015-practical-v1"


class H015Authorization(TypedDict):
    version: Literal[2]
    policy: Literal["h015-practical-v1"]
    authority: str
    cap_usd: Literal["120"]
    dispatch_threshold_usd: Literal["110"]
    buffer_usd: Literal["10"]
    model: str
    service_tier: Literal["default"]
    input_rate: Literal["5.50"]
    output_rate: Literal["11"]
    max_generation_calls: Literal[240]
    reserved_input_tokens: Literal[12000]
    reserved_output_tokens: Literal[32768]


H015_AUTHORIZATION: H015Authorization = {
    "version": 2,
    "policy": H015_POLICY,
    "authority": "CHAT053/CHAT054/ADR-CHAT007",
    "cap_usd": "120",
    "dispatch_threshold_usd": "110",
    "buffer_usd": "10",
    "model": PROFILE.model,
    "service_tier": PROFILE.service_tier,
    "input_rate": "5.50",
    "output_rate": "11",
    "max_generation_calls": 240,
    "reserved_input_tokens": 12000,
    "reserved_output_tokens": 32768,
}
