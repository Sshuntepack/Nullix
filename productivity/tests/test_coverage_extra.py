"""Targeted tests covering threading, subprocess, and edge branches."""

from __future__ import annotations

import time

from productivity.blocker import WmctrlController
from productivity.focus import FocusManager
from productivity.models import FocusSession, WindowSample
from productivity.storage import Storage
from productivity.tracker import Tracker
from productivity.window_provider import FakeWindowProvider, X11WindowProvider


def test_focus_tick_without_active():
    storage = Storage(":memory:")
    manager = FocusManager(storage)
    assert manager.tick() is None
    storage.close()


def test_storage_get_focus_sessions_bounds():
    storage = Storage(":memory:")
    storage.add_focus_session(
        FocusSession(label="a", start_ts=0.0, end_ts=100.0, planned_seconds=60)
    )
    storage.add_focus_session(
        FocusSession(label="b", start_ts=500.0, end_ts=600.0, planned_seconds=60)
    )
    windowed = storage.get_focus_sessions(start=400.0, end=700.0)
    assert [s.label for s in windowed] == ["b"]
    assert len(storage.get_focus_sessions()) == 2
    storage.close()


def test_tracker_thread_start_stop_flushes():
    storage = Storage(":memory:")
    now = time.time()
    samples = [
        WindowSample(app="Code", title="x", timestamp=now),
        WindowSample(app="Code", title="x", timestamp=now + 100),
    ]
    tracker = Tracker(
        storage,
        provider=FakeWindowProvider(samples),
        poll_interval=0.01,
        min_duration=0.0,
    )
    tracker.start()
    tracker.start()  # idempotent
    time.sleep(0.1)
    tracker.stop()
    # On stop the in-progress activity is flushed.
    assert len(storage.get_activities()) >= 1
    storage.close()


def test_wmctrl_controller_without_xdotool():
    controller = WmctrlController()
    controller._xdotool = None
    assert controller.minimize_active() is False


def test_wmctrl_controller_with_fake_binary():
    controller = WmctrlController()
    # Point at a harmless real binary so the subprocess path executes.
    controller._xdotool = "true"
    assert controller.minimize_active() is True


def test_x11_run_executes_real_subprocess():
    provider = X11WindowProvider()
    assert provider._run(["echo", "hello"]) == "hello"
    # Non-existent binary -> None (OSError path).
    assert provider._run(["definitely-not-a-real-binary-xyz"]) is None
    # Non-zero exit -> None.
    assert provider._run(["false"]) is None


def test_x11_idle_seconds_no_xprintidle():
    provider = X11WindowProvider()
    provider._xprintidle = None
    assert provider._idle_seconds() == 0.0


def test_x11_app_name_no_xprop():
    provider = X11WindowProvider()
    provider._xprop = None
    assert provider._app_name("123") == ""


def test_x11_idle_seconds_non_digit(monkeypatch):
    provider = X11WindowProvider()
    provider._xprintidle = "xprintidle"
    monkeypatch.setattr(provider, "_run", lambda args: "not-a-number")
    assert provider._idle_seconds() == 0.0


def test_x11_app_name_malformed_output(monkeypatch):
    provider = X11WindowProvider()
    provider._xprop = "xprop"
    monkeypatch.setattr(provider, "_run", lambda args: "no equals sign here")
    assert provider._app_name("123") == ""


def test_blocker_controller_subprocess_error():
    controller = WmctrlController()
    controller._xdotool = "xdotool"

    import productivity.blocker as blocker_mod

    def boom(*args, **kwargs):
        raise OSError("nope")

    original = blocker_mod.subprocess.run
    blocker_mod.subprocess.run = boom
    try:
        assert controller.minimize_active() is False
    finally:
        blocker_mod.subprocess.run = original


def test_tracker_on_activity_callback():
    seen = []
    storage = Storage(":memory:")
    samples = [
        WindowSample(app="Code", title="x", timestamp=0.0),
        WindowSample(app="Chrome", title="y", timestamp=10.0),
    ]
    tracker = Tracker(
        storage,
        provider=FakeWindowProvider(samples),
        min_duration=0.0,
        on_activity=seen.append,
    )
    tracker.poll_once()
    tracker.poll_once()
    assert len(seen) == 1
    storage.close()
