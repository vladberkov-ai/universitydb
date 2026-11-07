"""Loopback-only Streamlit view. Normal profile never falls back to scripted output."""

import json
import os
from pathlib import Path

import streamlit as st

from universitydb.agent import Agent
from universitydb.contracts import Failure
from universitydb.db import initialize
from universitydb.domain import University
from universitydb.llm import OpenAIProvider, Provider, ScriptedProvider

QUESTION = (
    "What is the average grade for Bea (student_id=2) in DB (course_id=1) "
    "with Kim (teacher_id=10) in semester S1?"
)


def provider(root: Path) -> Provider:
    fixture = os.environ.get("UNIVERSITYDB_TEST_FIXTURE")
    if os.environ.get("UNIVERSITYDB_TEST_MODE") == "1" and fixture:
        return ScriptedProvider(json.loads(Path(fixture).read_text()))
    return OpenAIProvider(Path(__file__).parent / "prompts", root / "runtime" / "spending.json")


def main() -> None:
    st.title("UniversityDB — I1/S6")
    st.caption("Local synthetic data only. I2–I5, Library and resume not implemented.")
    root = Path(os.environ.get("UNIVERSITYDB_ROOT", ".")).resolve()
    database = root / "runtime" / "university.db"
    selected = provider(root)
    st.warning(
        f"Execution profile: {selected.profile}. Offline/injected is not live model accuracy."
    )
    with st.form("question"):
        question = st.text_area("Question", QUESTION)
        submitted = st.form_submit_button("Run")
    if submitted:
        st.session_state.pop("result", None)
        try:
            if not database.exists():
                initialize(database, root / "resources")
            st.session_state["result"] = Agent(
                University(), database, selected, root / "runtime" / "traces"
            ).run(question)
        except (Failure, OSError, ValueError):
            st.error("Local setup failed safely; no prior answer is displayed.")
    result = st.session_state.get("result")
    if result:
        st.caption(f"Run: {result['run_id']}; profile: {result['execution_profile']}")
        if result["status"] == "ok":
            st.success(result["answer"]["text"])
            st.json(result["answer"])
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
        with st.expander("Full same-run trace", expanded=True):
            st.json(events, expanded=True)
            st.download_button(
                "JSONL trace",
                "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events),
                f"{result['run_id']}.jsonl",
                "application/x-ndjson",
            )


if __name__ == "__main__":
    main()
