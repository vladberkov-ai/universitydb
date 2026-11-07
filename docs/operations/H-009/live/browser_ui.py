"""Capture normal live I1 UI once; no injection or provider calls in browser helper."""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "ui"


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/home/dev/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome",
            headless=True,
            args=["--no-sandbox"],
        )
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            page.set_default_timeout(200000)
            page.goto("http://127.0.0.1:8509")
            page.get_by_text("Execution profile: live.", exact=False).wait_for()
            assert "Execution profile: live" in page.inner_text("body")
            page.get_by_role("button", name="Выполнить", exact=True).click()
            page.get_by_text(
                "student_id=2; course_id=1; teacher_id=10; semester_id=S1: средняя 80.00 (2 оценок; 2 записей).",
                exact=True,
            ).wait_for()
            page.get_by_text("16000", exact=False).first.wait_for()
            page.get_by_text("run_end", exact=False).first.wait_for()
            page.screenshot(path=str(OUT / "live-ui-success.png"), full_page=True)
            for index, label in enumerate(["sql", "db", "trace"]):
                page.get_by_test_id("stExpander").nth(index).scroll_into_view_if_needed()
                if label == "db":
                    page.get_by_text("16000", exact=False).first.scroll_into_view_if_needed()
                if label == "trace":
                    page.get_by_text("run_end", exact=False).first.scroll_into_view_if_needed()
                page.screenshot(path=str(OUT / f"live-ui-{label}.png"))
            with page.expect_download() as download:
                page.get_by_role("button", name="JSONL trace").click()
            download.value.save_as(str(OUT / "live-ui-success.jsonl"))
            (OUT / "success-visible-body.txt").write_text(page.inner_text("body"))
            page.get_by_role("textbox", name="Вопрос").fill("unsupported")
            page.get_by_role("button", name="Выполнить", exact=True).click()
            page.get_by_text(
                "INVALID_INPUT: I1 supports only an explicit four-filter grade mean.", exact=True
            ).wait_for()
            assert "средняя 80.00" not in page.inner_text("body")
            page.screenshot(path=str(OUT / "live-ui-failure.png"), full_page=True)
            with page.expect_download() as download:
                page.get_by_role("button", name="JSONL trace").click()
            download.value.save_as(str(OUT / "live-ui-failure.jsonl"))
            result = {
                "profile": "live",
                "s6": "80.00",
                "raw": [16000, 2, 2],
                "sql_db_trace_panels": "expanded and visible",
                "failure": "INVALID_INPUT; prior 80.00 cleared",
                "browser": "cached Chromium1228 via cached isolated Playwright",
                "scope": "one normal live S6 UI form submission then unsupported input",
                "cleanup": "browser.close in finally",
            }
            (OUT / "browser-receipt.json").write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
