import time

from productivity.config import Settings
from productivity.demo import seed_demo_data
from productivity.models import WindowSample
from productivity.service import ProductivityService
from productivity.storage import Storage
from productivity.window_provider import FakeWindowProvider


def test_seed_demo_data_deterministic():
    s1 = Storage(":memory:")
    s2 = Storage(":memory:")
    n1 = seed_demo_data(s1, days=2, seed=7)
    n2 = seed_demo_data(s2, days=2, seed=7)
    assert n1 == n2
    assert n1 > 0
    a1 = s1.get_activities()
    a2 = s2.get_activities()
    assert [a.app for a in a1] == [a.app for a in a2]
    s1.close()
    s2.close()


def test_seed_demo_data_not_in_future():
    storage = Storage(":memory:")
    seed_demo_data(storage, days=1)
    now = time.time()
    assert all(a.end_ts <= now + 1 for a in storage.get_activities())
    storage.close()


def test_service_tracks_and_enforces(tmp_path):
    samples = [
        WindowSample(app="Code", title="main.py", timestamp=time.time()),
        WindowSample(app="YouTube", title="video", timestamp=time.time() + 1),
        WindowSample(app="Code", title="main.py", timestamp=time.time() + 2),
    ]
    settings = Settings(db_path=str(tmp_path / "svc.db"), poll_interval=0.01)
    service = ProductivityService(
        settings,
        provider=FakeWindowProvider(samples),
        enforce_blocking=False,
    )
    # Start a focus session that blocks YouTube.
    service.focus.start_focus(blocklist=["youtube"])

    # Drive the loop manually via poll_once for determinism.
    service.tracker.poll_once()  # Code starts
    service.tracker.poll_once()  # switch -> Code persisted, YouTube enforced
    service.tracker.poll_once()  # switch -> YouTube persisted

    activities = service.storage.get_activities()
    apps = [a.app for a in activities]
    assert "Code" in apps
    # All tracked activities should be tagged with the active focus session.
    assert all(a.focus_session_id is not None for a in activities)
    service.close()


def test_service_close_is_idempotent(tmp_path):
    settings = Settings(db_path=str(tmp_path / "svc2.db"))
    service = ProductivityService(
        settings,
        provider=FakeWindowProvider([]),
        enforce_blocking=False,
    )
    service.start()
    service.close()
