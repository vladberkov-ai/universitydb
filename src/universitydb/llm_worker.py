"""One SDK attempt; parent owns spending and kill/reap wall-clock watchdog."""

import json
import sys
from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI
from pydantic import ValidationError

from universitydb.contracts import Failure, PlanProposal, SQLProposal


def request(payload: dict[str, Any]) -> dict[str, Any]:
    output_type = PlanProposal if payload["operation"] == "plan" else SQLProposal
    try:
        with OpenAI(max_retries=0, timeout=15.0) as client:
            response = client.responses.parse(
                model=payload["model"],
                store=False,
                max_output_tokens=2000,
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
    if response.status == "incomplete":
        raise Failure("PROVIDER_INCOMPLETE", "Provider output was incomplete.")
    if any(
        getattr(part, "type", "") == "refusal"
        for item in response.output
        for part in getattr(item, "content", [])
    ):
        raise Failure("PROVIDER_REFUSAL", "Provider refused the request.")
    if response.output_parsed is None:
        raise Failure("PROVIDER_INVALID_OUTPUT", "No parsed structured output.")
    if response.usage is None:
        raise Failure("BUDGET_EXCEEDED", "Provider usage missing; reservation retained.")
    return {
        "output": response.output_parsed.model_dump(),
        "usage": {
            "returned_model": response.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
            "provider_request_id": response.id,
        },
    }


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
