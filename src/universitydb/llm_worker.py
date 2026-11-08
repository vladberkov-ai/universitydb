"""One SDK attempt; parent owns spending and kill/reap wall-clock watchdog."""

import json
import sys
from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI
from pydantic import ValidationError

from universitydb.config import API_BASE_URL, PROFILE, wire_payload
from universitydb.contracts import Failure, PlanProposal, SQLProposal


def request(payload: dict[str, Any]) -> dict[str, Any]:
    operation = payload["operation"]
    logical = payload["logical_operation"]
    policy = PROFILE.operation(logical)
    if (operation, logical) not in (("plan", "plan"), ("sql", "sql"), ("sql", "repair")):
        raise Failure("PROVIDER_UNAVAILABLE", "Invalid worker operation mapping.")
    if payload["model"] != PROFILE.model or not 0 < payload["timeout"] <= policy.timeout:
        raise Failure("PROVIDER_UNAVAILABLE", "Unsupported worker configuration.")
    output_type = PlanProposal if operation == "plan" else SQLProposal
    try:
        with OpenAI(max_retries=0, timeout=payload["timeout"], base_url=API_BASE_URL) as client:
            response = client.responses.create(
                **wire_payload(
                    operation, logical, payload["model"], payload["prompt"], payload["input"]
                )
            )
    except (APITimeoutError, APIConnectionError) as exc:
        raise Failure(
            "PROVIDER_TRANSIENT", "Provider transport failed; reservation retained."
        ) from exc
    except APIStatusError as exc:
        code = (
            "PROVIDER_TRANSIENT"
            if exc.status_code in (429, 500, 502, 503, 504)
            else "PROVIDER_UNAVAILABLE"
        )
        raise Failure(code, "Provider request failed; reservation retained.") from exc
    except (ValidationError, ValueError) as exc:
        raise Failure(
            "PROVIDER_INVALID_OUTPUT", "Provider output did not match strict schema."
        ) from exc
    usage = {
        "returned_model": response.model,
        "returned_service_tier": getattr(response, "service_tier", None),
        "provider_request_id": response.id,
    }
    if response.usage is not None:
        usage.update(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        )
    raw = {"raw_response": response.model_dump(mode="json")}
    failure = None
    if response.status == "incomplete":
        failure = ("PROVIDER_INCOMPLETE", "Provider output was incomplete.")
    elif any(
        getattr(part, "type", "") == "refusal"
        for item in response.output
        for part in getattr(item, "content", [])
    ):
        failure = ("PROVIDER_REFUSAL", "Provider refused the request.")
    elif response.status != "completed":
        failure = ("PROVIDER_INVALID_OUTPUT", "Provider response did not complete.")
    elif response.usage is None:
        failure = ("BUDGET_EXCEEDED", "Provider usage missing; reservation retained.")
    if failure:
        return {**raw, "error": failure[0], "message": failure[1], "usage": usage}
    try:
        parsed = output_type.model_validate_json(response.output_text)
    except (ValidationError, ValueError):
        return {
            **raw,
            "error": "PROVIDER_INVALID_OUTPUT",
            "message": "Provider output did not match strict schema.",
            "usage": usage,
        }
    return {**raw, "output": parsed.model_dump(), "usage": usage}


def main() -> None:
    try:
        result = request(json.load(sys.stdin))
    except Failure as exc:
        result = {"error": exc.code, "message": exc.message}
    except (OSError, TypeError, KeyError, ValueError):
        result = {"error": "PROVIDER_UNAVAILABLE", "message": "Provider worker failed safely."}
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
