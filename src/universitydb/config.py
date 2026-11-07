"""Single bounded I1 Responses policy; monetary approval is a separate live gate."""

from dataclasses import dataclass
from typing import Any, Literal

from universitydb.contracts import Failure


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
