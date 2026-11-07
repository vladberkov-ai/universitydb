"""Bounded, fsynced local JSONL: no success until answer and run_end persist."""

import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from universitydb.contracts import Failure


class Trace:
    def __init__(self, directory: Path, run_id: str, *, limit: int = 1048576) -> None:
        self.run_id = run_id
        self.path = directory / f"{run_id}.jsonl"
        self.events: list[dict[str, Any]] = []
        self.bytes = 0
        self.limit = limit
        self.terminal = False

    def emit(self, node: str, kind: str, payload: dict[str, Any], attempt: int = 0) -> None:
        if self.terminal:
            raise Failure("TRACE_UNAVAILABLE", "Trace is already terminal.")
        event = {
            "version": "1",
            "trace_id": self.run_id,
            "run_id": self.run_id,
            "event_id": str(uuid.uuid4()),
            "seq": len(self.events) + 1,
            "parent_event_id": None,
            "request_id": self.run_id,
            "node": node,
            "kind": kind,
            "attempt": attempt,
            "timestamp": datetime.now(UTC).isoformat(),
            "duration_ms": payload.get("elapsed_ms"),
            "payload": payload,
        }
        line = json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n"
        reserve = 4096 if kind not in ("error", "run_end") else 0
        if self.bytes + len(line.encode()) > self.limit - reserve:
            raise Failure("BUDGET_EXCEEDED", "Trace size limit exceeded.")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf8") as stream:
                stream.write(line)
                stream.flush()
                os.fsync(stream.fileno())
        except OSError as exc:
            raise Failure(
                "TRACE_UNAVAILABLE", "Trace persistence failed; run is not successful."
            ) from exc
        self.events.append(event)
        self.bytes += len(line.encode())
        self.terminal = kind == "run_end"
