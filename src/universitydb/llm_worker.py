"""One SDK attempt; parent owns spending and kill/reap wall-clock watchdog."""

import json
import sys
from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI
from pydantic import ValidationError

from universitydb.config import PROFILE
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
        with OpenAI(max_retries=0, timeout=payload["timeout"]) as client:
            response = client.responses.parse(
                model=payload["model"],
                store=False,
                max_output_tokens=policy.output_tokens,
                reasoning={"effort": policy.effort},
                service_tier=PROFILE.service_tier,
                instructions=payload["prompt"],
                input=payload["input"],
                text_format=output_type,
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
    failure = None
    if response.status == "incomplete":
        failure = ("PROVIDER_INCOMPLETE", "Provider output was incomplete.")
    elif any(
        getattr(part, "type", "") == "refusal"
        for item in response.output
        for part in getattr(item, "content", [])
    ):
        failure = ("PROVIDER_REFUSAL", "Provider refused the request.")
    elif response.output_parsed is None:
        failure = ("PROVIDER_INVALID_OUTPUT", "No parsed structured output.")
    elif response.usage is None:
        failure = ("BUDGET_EXCEEDED", "Provider usage missing; reservation retained.")
    if failure:
        return {"error": failure[0], "message": failure[1], "usage": usage}
    assert response.output_parsed is not None  # Established by the failure branch above.
    return {"output": response.output_parsed.model_dump(), "usage": usage}


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
