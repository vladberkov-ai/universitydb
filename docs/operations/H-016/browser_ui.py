"""Actual temporary offline browser/Streamlit/compiled-graph/SQLite evidence.

Only explicit injected proposals, no API generation or credentials. Owns and stops
its exact temporary server/browser. Preserve every attempt in a new output dir.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "H-013"))
from offline_ui_fixture import fixture as historical_fixture
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect, sync_playwright
from ui_fixtures import plan, proposal, step

from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library

ROOT = Path(__file__).resolve().parents[3]


def browser_path():
    """Explicit path, PATH browser, then Playwright's installed default."""
    explicit = os.environ.get("UNIVERSITYDB_BROWSER_EXECUTABLE")
    if explicit:
        path = Path(explicit).resolve()
        if not path.is_file():
            raise ValueError("Explicit browser executable does not exist")
        return str(path)
    return next(
        (
            p
            for name in ("chromium", "chromium-browser", "google-chrome")
            if (p := shutil.which(name))
        ),
        None,
    )


QUESTIONS = {
    "success": "What is the average grade for student ID 2 in course ID 1 with teacher ID 10 in semester ID S1?",
    "clarification": "What is the average grade for Alex with student ID in output?",
    "m1": "For students of the course with the highest mean in S1, show student IDs with their mean across all S1 courses.",
    "repair": "What is the average grade for student ID 2 in course ID 1 with teacher ID 10 in semester ID S1?",
    "error": "What is the average grade across all enrollments?",
    "library-filter": "How many open loans for reader ID 1?",
    "library": "Show reader IDs, names and open loan counts per reader.",
}


def fixture(full=False):
    """Reuse unchanged H013 fixture sequence; add one genuinely filtered Library run."""
    result = historical_fixture(full)
    result["library-v1"] = [
        plan(step(LIBRARY_SPEC)),
        proposal(Library(), LIBRARY_SPEC, {"reader_id": 1}),
        *result["library-v1"],
    ]
    return result


def wait_for_library_dataset(page, previous_run_id):
    """Wait for a positive schema-specific render, not absence of a prior name."""
    question = page.get_by_role("textbox", name="Question", exact=True)
    expect(question).to_have_value("How many open loans does each reader have?", timeout=120000)
    expect(page.locator("body")).not_to_contain_text(previous_run_id, timeout=120000)
    page.get_by_test_id("stStatusWidget").wait_for(state="hidden")
    return question


def submit_new_run(page, question):
    """Wait for a new rendered run identity, even when answer text stays equal."""
    pattern = re.compile(r"^Run: ([0-9a-f-]{36}); profile: ")
    caption = page.get_by_text(pattern)
    assert caption.count() <= 1
    previous = pattern.match(caption.inner_text()).group(1) if caption.count() else None
    textbox = page.get_by_role("textbox", name="Question", exact=True)
    textbox.fill(question)
    expect(textbox).to_have_value(question)
    page.get_by_role("button", name="Run", exact=True).click()
    if previous is not None:
        expect(page.locator("body")).not_to_contain_text(previous, timeout=120000)
    expect(caption).to_have_text(pattern, timeout=120000)
    page.get_by_test_id("stStatusWidget").wait_for(state="hidden")
    current = pattern.match(caption.inner_text()).group(1)
    assert current != previous
    return current


def capture_failure(page, out, receipt):
    """Preserve diagnostic state before browser teardown; never mask the failure."""
    errors = {}
    for name, capture in (
        (
            "body",
            lambda: (out / "failure-visible.txt").write_text(page.inner_text("body", timeout=5000)),
        ),
        (
            "question",
            lambda: receipt.update(
                failure_question=page.get_by_role(
                    "textbox", name="Question", exact=True
                ).input_value(timeout=5000)
            ),
        ),
        (
            "screenshot",
            lambda: page.screenshot(path=str(out / "failure.png"), full_page=True, timeout=5000),
        ),
    ):
        try:
            capture()
        except (OSError, PlaywrightError) as exc:
            errors[name] = type(exc).__name__
    try:
        trace = page.get_by_role("button", name="JSONL trace", exact=True)
        if trace.count():
            with page.expect_download(timeout=5000) as download:
                trace.click(timeout=5000)
            download.value.save_as(str(out / "failure-current.jsonl"))
    except (OSError, PlaywrightError) as exc:
        errors["trace"] = type(exc).__name__
    receipt["failure_capture_errors"] = errors


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(out, full):
    out.mkdir(parents=True, exist_ok=False)
    before = {
        str(p.relative_to(ROOT)): digest(p) for p in (ROOT / "runtime").rglob("*") if p.is_file()
    }
    receipt = {
        "profile": "offline/injected",
        "real_provider_called": False,
        "paid_calls": 0,
        "browser_network_policy": "Abort every non-loopback browser request",
        "reuse": "H014 run/capture harness copied; historical file immutable; H013 fixture imported",
        "browser_executable": browser_path() or "Playwright managed default",
        "base_HEAD": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "source_sha256": {
            str(p.relative_to(ROOT)): digest(p)
            for p in sorted((ROOT / "src/universitydb").rglob("*"))
            if p.is_file() and "__pycache__" not in str(p)
        },
        "cases": {},
        "server_stopped": False,
        "browser_closed": False,
        "claim": "Actual browser+Streamlit+compiled graph+SQLite with injected proposals, NOT real-model NL-to-SQL accuracy",
    }
    with tempfile.TemporaryDirectory(prefix="h016-offline-ui-") as folder:
        temp = Path(folder)
        shutil.copytree(ROOT / "resources", temp / "resources")
        fixture_file = temp / "injected.json"
        fixture_file.write_text(json.dumps(fixture(full), indent=2) + "\n")
        receipt["fixture_sha256"] = digest(fixture_file)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        env.update(
            UNIVERSITYDB_ROOT=str(temp),
            UNIVERSITYDB_TEST_MODE="1",
            UNIVERSITYDB_TEST_FIXTURE=str(fixture_file),
            UNIVERSITYDB_LIVE_APPROVED="no",
            LANGSMITH_TRACING="false",
            LANGCHAIN_TRACING_V2="false",
        )
        with (temp / "server.log").open("w") as log:
            server = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    str(ROOT / "src/universitydb/ui.py"),
                    "--server.address=127.0.0.1",
                    f"--server.port={port}",
                    "--server.headless=true",
                    "--browser.gatherUsageStats=false",
                ],
                cwd=ROOT,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            browser = None
            try:
                for _ in range(120):
                    if server.poll() is not None:
                        raise RuntimeError("Owned offline UI server exited before readiness")
                    try:
                        with urlopen(
                            f"http://127.0.0.1:{port}/_stcore/health", timeout=1
                        ) as response:
                            if response.status == 200:
                                break
                    except OSError:
                        time.sleep(0.25)
                else:
                    raise RuntimeError("Owned offline UI server readiness timeout")
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(
                        executable_path=browser_path(), headless=True, args=["--no-sandbox"]
                    )
                    try:
                        page = browser.new_page(viewport={"width": 1440, "height": 1100})
                        page.route(
                            "**/*",
                            lambda route: (
                                route.continue_()
                                if urlsplit(route.request.url).hostname
                                in {"127.0.0.1", "localhost", "::1"}
                                else route.abort()
                            ),
                        )
                        page.set_default_timeout(120000)
                        page.goto(f"http://127.0.0.1:{port}")
                        page.get_by_text(
                            "Execution profile: offline/injected.", exact=False
                        ).wait_for()

                        seen_runs = {}
                        submitted_runs = {}

                        def capture(case, expected, status="ok"):
                            # Grouped means have a summary alert; exact values are in the
                            # typed answer/trace rather than repeated in that heading.
                            alert_text = "grade_mean" if case == "m1" else expected
                            page.get_by_test_id("stAlert").filter(
                                has_text=alert_text
                            ).first.wait_for()
                            # Wait for the whole current render, not merely its early alert.
                            # Otherwise Streamlit can still be replacing prior lower panels.
                            page.get_by_test_id("stStatusWidget").wait_for(state="hidden")
                            with page.expect_download() as download:
                                page.get_by_role("button", name="JSONL trace", exact=True).click()
                            download.value.save_as(str(out / f"{case}.jsonl"))
                            events = [
                                json.loads(line)
                                for line in (out / f"{case}.jsonl").read_text().splitlines()
                            ]
                            run_ids = {event["run_id"] for event in events}
                            assert len(run_ids) == 1
                            run_id = next(iter(run_ids))
                            question_key = (
                                "clarification" if case.startswith("clarification-") else case
                            )
                            assert run_id == submitted_runs[question_key]
                            assert [e["seq"] for e in events] == list(range(1, len(events) + 1))
                            expected_question = QUESTIONS.get(
                                question_key, "How many open loans does each reader have?"
                            )
                            assert events[0]["kind"] == "input"
                            assert events[0]["payload"]["question"] == expected_question
                            if case == "clarification-resume":
                                assert run_id == seen_runs["clarification-pause"]
                            else:
                                assert run_id not in seen_runs.values()
                            seen_runs[case] = run_id
                            if status != "clarification":
                                assert events[-1]["kind"] == "run_end"
                                assert events[-1]["payload"]["status"] == status
                            if status == "ok":
                                expected_scope = (
                                    {
                                        "student_id": 2,
                                        "course_id": 1,
                                        "teacher_id": 10,
                                        "semester_id": "S1",
                                    }
                                    if case in {"success", "repair"}
                                    else {"reader_id": 1}
                                    if case == "library-filter"
                                    else {"student_id": 1}
                                    if case == "clarification-resume"
                                    else {"semester_id": "S1"}
                                    if case == "m1"
                                    else {}
                                )
                                actual = [
                                    e["payload"] for e in events if e["kind"] == "sql_attempt"
                                ]
                                assert actual
                                # Parameters are generated fixture output but production validation
                                # requires exact equality to actual resolved scope/dependency values.
                                for attempt in actual:
                                    for key, value in expected_scope.items():
                                        assert attempt["parameters"][key] == value
                                assert expected in json.dumps(
                                    [e["payload"] for e in events if e["kind"] == "answer"]
                                )
                            elif status == "error":
                                assert any(
                                    e["kind"] == "error" and e["payload"].get("code") == expected
                                    for e in events
                                )
                                assert not any(e["kind"] == "db_result" for e in events)
                            page.get_by_test_id("stStatusWidget").wait_for(state="hidden")
                            body = page.inner_text("body")
                            assert "offline/injected" in body and run_id in body
                            assert "DeltaGenerator" not in body
                            assert page.get_by_test_id("stDocstring").count() == 0
                            assert not any(line.strip() == "None" for line in body.splitlines())
                            if status == "error":
                                assert (
                                    page.get_by_test_id("stAlert").filter(has_text="80.00").count()
                                    == 0
                                )
                                db_section = (
                                    page.get_by_test_id("stExpander")
                                    .filter(has_text="DB typed rows")
                                    .first
                                )
                                assert "DB query was not executed." in db_section.inner_text()
                                assert "sum_units" not in db_section.inner_text()
                            page.get_by_role(
                                "textbox", name="Question", exact=True
                            ).scroll_into_view_if_needed()
                            page.screenshot(path=str(out / f"{case}.png"), full_page=True)
                            # Streamlit has an internal scroll container: focus every panel.
                            for panel, label in [
                                ("sql", "SQL and safe parameters"),
                                ("db", "DB typed rows"),
                                ("adapted", "Adapted step results and dependency bindings"),
                                ("trace", "Full same-run trace"),
                            ]:
                                section = (
                                    page.get_by_test_id("stExpander").filter(has_text=label).first
                                )
                                assert section.locator("details").get_attribute("open") is not None
                                section.scroll_into_view_if_needed()
                                assert section.is_visible()
                                if panel in ("db", "adapted"):
                                    assert "DeltaGenerator" not in section.inner_text()
                                    assert not any(
                                        line.strip() == "None"
                                        for line in section.inner_text().splitlines()
                                    )
                                    if status == "ok":
                                        raw_results = [
                                            e["payload"] for e in events if e["kind"] == "db_result"
                                        ]
                                        assert raw_results
                                        assert section.get_by_test_id("stJson").count() > 0
                                        # Inspect expanded JSON strings, not only the alert/trace.
                                        # Each raw result must expose its column names and values.
                                        panel_text = section.inner_text()
                                        assert "rows" in panel_text
                                        if panel == "db":
                                            for raw in raw_results:
                                                for column in raw["columns"]:
                                                    assert column["name"] in panel_text
                                                for row in raw["rows"]:
                                                    for value in row:
                                                        rendered = (
                                                            json.dumps(value)
                                                            if value is None
                                                            or isinstance(value, bool)
                                                            else str(value)
                                                        )
                                                        assert rendered in panel_text
                                        else:
                                            assert "dependency_rows" in panel_text
                                    else:
                                        empty_message = (
                                            "DB query was not executed."
                                            if panel == "db"
                                            else "No adapted step results yet."
                                        )
                                        assert empty_message in section.inner_text()
                                page.screenshot(path=str(out / f"{case}-{panel}.png"))
                            (out / f"{case}-visible.txt").write_text(body)
                            receipt["cases"][case] = {
                                "expected": expected,
                                "status": status,
                                "run_id": run_id,
                                "events": len(events),
                                "trace_sha256": digest(out / f"{case}.jsonl"),
                                "screenshot_sha256": digest(out / f"{case}.png"),
                                "current_question_run_outcome_verified": True,
                                "render_settled_before_screenshots": True,
                                "no_magic_help_or_none": True,
                                "focused_open_typed_rows_verified": status == "ok",
                            }
                            return events

                        def submit(case):
                            submitted_runs[case] = submit_new_run(page, QUESTIONS[case])

                        submit("success")
                        capture("success", "80.00")
                        submit("clarification")
                        page.get_by_role("button", name="Continue this run", exact=True).wait_for()
                        paused = capture("clarification-pause", "Choose", "clarification")
                        assert not any(e["kind"] == "sql_attempt" for e in paused)
                        page.get_by_role("button", name="Continue this run", exact=True).click()
                        resumed = capture("clarification-resume", "86.67")
                        assert paused[0]["run_id"] == resumed[0]["run_id"]
                        assert any(e["kind"] == "resume" for e in resumed)
                        if full:
                            submit("m1")
                            multi = capture("m1", "95.00")
                            assert len([e for e in multi if e["kind"] == "db_result"]) == 3
                        submit("repair")
                        repaired = capture("repair", "80.00")
                        assert any(
                            e["kind"] == "error" and e["payload"].get("repair") for e in repaired
                        )
                        submit("error")
                        failed = capture("error", "PROVIDER_REFUSAL", "error")
                        assert not any(e["kind"] == "db_result" for e in failed)
                        if full:
                            dataset = page.get_by_role("combobox", name="Dataset", exact=True)
                            dataset.scroll_into_view_if_needed()
                            dataset.click()
                            (out / "dataset-options-visible.txt").write_text(
                                page.locator("body").inner_text()
                            )
                            page.screenshot(path=str(out / "dataset-options.png"))
                            page.get_by_role("option", name="Library", exact=True).click()
                            wait_for_library_dataset(page, receipt["cases"]["error"]["run_id"])
                            receipt["library_transition_default_verified"] = True
                            submit("library-filter")
                            filtered = capture("library-filter", "Ada")
                            assert [
                                e["payload"]["rows"] for e in filtered if e["kind"] == "db_result"
                            ] == [[[1, "Ada", 1]]]
                            submit("library")
                            library = capture("library", "Ada")
                            raw = [
                                e["payload"]["rows"] for e in library if e["kind"] == "db_result"
                            ]
                            assert raw == [[[1, "Ada", 1], [2, "Bob", 1]]]
                        receipt["status"] = "passed"
                    except BaseException:
                        if "page" in locals():
                            capture_failure(page, out, receipt)
                        raise
                    finally:
                        browser.close()
                        receipt["browser_closed"] = True
                        browser = None
            except BaseException as exc:
                receipt["status"] = "failed"
                receipt["failure_type"] = type(exc).__name__
                raise
            finally:
                if browser is not None:
                    browser.close()
                    receipt["browser_closed"] = True
                if server.poll() is None:
                    os.killpg(server.pid, signal.SIGTERM)
                    try:
                        server.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(server.pid, signal.SIGKILL)
                        server.wait(timeout=5)
                receipt["server_stopped"] = server.poll() is not None
                log.flush()
                shutil.copyfile(temp / "server.log", out / "server.log")
                if receipt.get("status") == "failed" and (temp / "runtime/traces").is_dir():
                    shutil.copytree(temp / "runtime/traces", out / "failure-runtime-traces")
                receipt["temporary_ledger_absent"] = not (temp / "runtime/spending.json").exists()
                after = {
                    str(p.relative_to(ROOT)): digest(p)
                    for p in (ROOT / "runtime").rglob("*")
                    if p.is_file()
                }
                receipt["actual_runtime_unchanged"] = after == before
                (out / "browser-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "cases": list(receipt["cases"]),
                "server_stopped": receipt["server_stopped"],
                "browser_closed": receipt["browser_closed"],
            }
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    run(args.output, args.full)
