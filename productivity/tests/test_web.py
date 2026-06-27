import pytest

from productivity.demo import seed_demo_data
from productivity.focus import FocusManager
from productivity.storage import Storage
from productivity.web import create_app


@pytest.fixture
def client():
    storage = Storage(":memory:")
    seed_demo_data(storage, days=1)
    focus = FocusManager(storage)
    app = create_app(storage, focus)
    app.config.update(TESTING=True)
    with app.test_client() as c:
        c.storage = storage
        yield c
    storage.close()


def test_index_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Productivity Manager" in resp.data


def test_dashboard_api_shape(client):
    resp = client.get("/api/dashboard?range=today")
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ("summary", "by_app", "hourly", "daily", "focus", "range"):
        assert key in data
    assert data["range"] == "today"


def test_dashboard_api_week_and_default(client):
    assert client.get("/api/dashboard?range=week").get_json()["range"] == "week"
    assert client.get("/api/dashboard?range=month").get_json()["range"] == "month"
    assert client.get("/api/dashboard?range=bogus").get_json()["range"] == "today"


def test_focus_start_stop_flow(client):
    status = client.get("/api/focus").get_json()
    assert status["active"] is False

    started = client.post(
        "/api/focus/start", json={"kind": "focus", "minutes": 25}
    ).get_json()
    assert started["started"] is True
    assert started["kind"] == "focus"

    status = client.get("/api/focus").get_json()
    assert status["active"] is True
    assert status["kind"] == "focus"

    stopped = client.post("/api/focus/stop", json={}).get_json()
    assert stopped["stopped"] is True
    assert client.get("/api/focus").get_json()["active"] is False


def test_focus_start_break(client):
    started = client.post(
        "/api/focus/start", json={"kind": "break", "minutes": 5}
    ).get_json()
    assert started["kind"] == "break"


def test_focus_stop_when_inactive(client):
    stopped = client.post("/api/focus/stop", json={}).get_json()
    assert stopped["stopped"] is False
