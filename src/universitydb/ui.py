"""Local synthetic-data UI; injected fixtures require explicit test configuration."""

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any

import streamlit as st

from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.db import initialize
from universitydb.domain import University
from universitydb.library import Library
from universitydb.llm import OpenAIProvider, Provider, ScriptedProvider

QUESTION = (
    "What is the average grade for Bea (student_id=2) in DB (course_id=1) "
    "with Kim (teacher_id=10) in semester S1?"
)
# Domain construction/provisioning belongs at the composition root, never graph core.
DOMAINS: dict[str, tuple[Any, str, str]] = {
    "University": (University, "university-v1", ""),
    "Library": (Library, "library-v1", "library"),
}


def provider(root: Path, schema_id: str) -> Provider:
    fixture = os.environ.get("UNIVERSITYDB_TEST_FIXTURE")
    if os.environ.get("UNIVERSITYDB_TEST_MODE") == "1" and fixture:
        data = json.loads(Path(fixture).read_text())
        values = data[schema_id] if isinstance(data, dict) else data
        # Explicit controlled faults, not a question-accessible production feature.
        outputs = [
            Failure(value["injected_error"]["code"], value["injected_error"]["message"])
            if isinstance(value, dict) and set(value) == {"injected_error"}
            else value
            for value in values
        ]
        return ScriptedProvider(outputs)
    return OpenAIProvider(Path(__file__).parent / "prompts", root / "runtime" / "spending.json")


def context_identity(root: Path, schema_id: str) -> str:
    fixture = (
        os.environ.get("UNIVERSITYDB_TEST_FIXTURE", "")
        if os.environ.get("UNIVERSITYDB_TEST_MODE") == "1"
        else ""
    )
    digest = hashlib.sha256(Path(fixture).read_bytes()).hexdigest() if fixture else "none"
    return json.dumps([str(root), schema_id, os.environ.get("UNIVERSITYDB_TEST_MODE"), digest])


def render_result(result: dict[str, Any]) -> None:
    st.caption(f"Run: {result['run_id']}; profile: {result['execution_profile']}")
    if result["status"] == "ok":
        st.success(result["answer"]["text"])
        st.json(result["answer"])
    elif result["status"] == "clarification":
        st.info(result["clarification"].get("prompt", "Choose an option to continue this run."))
    else:
        st.error(f"{result['error']['code']}: {result['error']['message']}")
    events = result["events"]
    with st.expander("SQL and safe parameters", expanded=True):
        queries = [e for e in events if e["kind"] in ("sql_validated", "sql_attempt")]
        if not queries:
            st.write("SQL was not executed.")
        for event in queries:
            st.caption(f"seq={event['seq']} attempt={event['attempt']} {event['kind']}")
            st.code(event["payload"]["sql"], language="sql")
            st.json(event["payload"]["parameters"])
    with st.expander("DB typed rows", expanded=True):
        results = [e["payload"] for e in events if e["kind"] == "db_result"]
        st.json(results) if results else st.write("DB query was not executed.")
    with st.expander("Adapted step results and dependency bindings", expanded=True):
        results = [
            {"node": e["node"], "seq": e["seq"], "payload": e["payload"]}
            for e in events
            if e["node"] in ("inspect_result", "bind_results") and e["kind"] == "node_end"
        ]
        st.json(results) if results else st.write("No adapted step results yet.")
    with st.expander("Full same-run trace", expanded=True):
        st.json(events, expanded=True)
        st.download_button(
            "JSONL trace",
            "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events),
            f"{result['run_id']}.jsonl",
            "application/x-ndjson",
        )


def main() -> None:
    st.title("University Database + LangGraph QA Agent")
    st.caption(
        "Local synthetic University and Library data. Offline fixtures are not model accuracy."
    )
    root = Path(os.environ.get("UNIVERSITYDB_ROOT", ".")).resolve()
    label = st.selectbox("Dataset", list(DOMAINS))
    factory, schema_id, resource_subdir = DOMAINS[label]
    database = root / "runtime" / f"{schema_id}.db"
    try:
        identity = context_identity(root, schema_id)
        if st.session_state.get("agent_identity") != identity:
            st.session_state.pop("result", None)
            st.session_state.pop("agent", None)
            st.session_state["agent_identity"] = identity
            st.session_state["session_id"] = str(uuid.uuid4())
            selected = provider(root, schema_id)
            if not database.exists():
                initialize(database, root / "resources" / resource_subdir)
            st.session_state["agent"] = Agent(
                factory(), database, selected, root / "runtime" / "traces"
            )
        agent = st.session_state["agent"]
    except (Failure, OSError, ValueError, KeyError, TypeError):
        st.session_state.pop("result", None)
        st.error("Local setup failed safely; no prior answer is displayed.")
        return
    st.warning(
        f"Execution profile: {agent.provider.profile}. Offline/injected is not live model accuracy."
    )
    with st.form("question"):
        question = st.text_area("Question", QUESTION)
        submitted = st.form_submit_button("Run")
    if submitted:
        st.session_state.pop("result", None)
        try:
            st.session_state["result"] = agent.run(question)
        except (Failure, OSError, ValueError, KeyError, TypeError):
            st.error("Run failed safely; no prior answer is displayed.")
    result = st.session_state.get("result")
    if result:
        if result["status"] == "clarification":
            continuation = result["clarification"]
            options = continuation["options"]
            # Values remain typed; labels distinguish same-name catalog identities.
            with st.form("clarification"):
                selection = st.selectbox(
                    "Clarification choice",
                    list(range(len(options))),
                    format_func=lambda i: options[i]["label"],
                )
                resume = st.form_submit_button("Continue this run")
            if resume:
                st.session_state.pop("result", None)
                try:
                    st.session_state["result"] = agent.resume(
                        continuation, options[selection]["value"], request_id=str(uuid.uuid4())
                    )
                except (Failure, OSError, ValueError, KeyError, TypeError):
                    st.error("Continuation failed safely; no prior answer is displayed.")
                result = st.session_state.get("result")
        if result:
            render_result(result)


if __name__ == "__main__":
    main()
