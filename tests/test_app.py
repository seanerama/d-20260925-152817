from datetime import datetime, timezone
from types import SimpleNamespace

import app as app_module
from app import app


def test_index_returns_html_with_server_time():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.content_type.startswith("text/html")

    body = response.get_data(as_text=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    assert 'id="server-time"' in body
    assert today in body


def test_index_has_check_health_button_and_result_area():
    client = app.test_client()
    response = client.get("/")
    body = response.get_data(as_text=True)

    assert 'id="check-health"' in body
    assert "Check health" in body
    assert 'id="health-result"' in body
    assert "fetch('/health')" in body or 'fetch("/health")' in body


def test_index_script_never_uses_innerhtml_for_health_data():
    client = app.test_client()
    response = client.get("/")
    body = response.get_data(as_text=True)

    assert "innerHTML" not in body
    assert "textContent" in body


def test_health_healthy_path_real_psutil():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.content_type.startswith("application/json")

    data = response.get_json()

    assert data["status"] == "ok"

    cpu_percent = data["cpu_percent"]
    mem_percent = data["mem_percent"]
    assert isinstance(cpu_percent, (int, float))
    assert isinstance(mem_percent, (int, float))
    assert 0 <= cpu_percent <= 100
    assert 0 <= mem_percent <= 100

    parsed_time = datetime.fromisoformat(data["time"])
    assert parsed_time.tzinfo is not None


def test_health_healthy_path_deterministic(monkeypatch):
    monkeypatch.setattr(app_module.psutil, "cpu_percent", lambda: 12.5)
    monkeypatch.setattr(
        app_module.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=43.0),
    )

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "ok"
    assert data["cpu_percent"] == 12.5
    assert data["mem_percent"] == 43.0


def test_health_degraded_when_cpu_percent_raises(monkeypatch):
    def boom():
        raise RuntimeError("probe boom")

    monkeypatch.setattr(app_module.psutil, "cpu_percent", boom)

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "degraded"
    assert isinstance(data["error"], str)
    assert "probe boom" in data["error"]


def test_health_degraded_when_virtual_memory_raises(monkeypatch):
    def boom():
        raise RuntimeError("probe boom")

    monkeypatch.setattr(app_module.psutil, "virtual_memory", boom)

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "degraded"
    assert isinstance(data["error"], str)
    assert "probe boom" in data["error"]
