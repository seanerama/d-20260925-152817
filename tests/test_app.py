from datetime import datetime, timezone

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
