import json

from conftest import ROOT, outputs
from streamlit.testing.v1 import AppTest


def test_actual_streamlit_app_offline_and_stale_clear(tmp_path, monkeypatch):
    # AppTest is an offline UI assertion, explicitly not browser or live E2E.
    fixture = tmp_path / "scripted.json"
    fixture.write_text(json.dumps(outputs()))
    monkeypatch.setenv("UNIVERSITYDB_TEST_MODE", "1")
    monkeypatch.setenv("UNIVERSITYDB_TEST_FIXTURE", str(fixture))
    monkeypatch.setenv("UNIVERSITYDB_ROOT", str(ROOT))
    app = AppTest.from_file(str(ROOT / "src/universitydb/ui.py")).run()
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert app.success and "80.00" in app.success[0].value
    assert [e.label for e in app.expander] == [
        "SQL and safe parameters",
        "DB typed rows",
        "Full same-run trace",
    ]
    assert app.code and any("16000" in e.value for e in app.json)
    app.text_area[0].set_value("unsupported")
    app.button[0].click().run()
    assert not app.success
    assert any("INVALID_INPUT" in e.value for e in app.error)


def test_normal_ui_missing_key_no_hidden_mock(monkeypatch):
    monkeypatch.delenv("UNIVERSITYDB_TEST_MODE", raising=False)
    monkeypatch.delenv("UNIVERSITYDB_TEST_FIXTURE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app = AppTest.from_file(str(ROOT / "src/universitydb/ui.py")).run()
    app.button[0].click().run()
    assert not app.exception and not app.success
    assert any("PROVIDER_UNAVAILABLE" in e.value for e in app.error)
