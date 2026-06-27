import pytest

from productivity.blocker import Blocker, NullController
from productivity.focus import FocusManager
from productivity.models import WindowSample
from productivity.storage import Storage


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


@pytest.fixture
def env():
    storage = Storage(":memory:")
    clock = Clock()
    controller = NullController()
    manager = FocusManager(
        storage,
        blocker=Blocker(controller),
        clock=clock,
        focus_minutes=25,
        break_minutes=5,
    )
    yield manager, clock, controller, storage
    storage.close()


def test_start_focus_persists_and_active(env):
    manager, _clock, _ctrl, storage = env
    session = manager.start_focus("Deep Work")
    assert session.id is not None
    assert manager.active is not None
    assert manager.active_session_id() == session.id
    assert storage.active_focus_session() is not None
    assert session.blocklist  # default blocklist applied


def test_start_focus_replaces_existing(env):
    manager, clock, _ctrl, storage = env
    first = manager.start_focus("First")
    clock.advance(60)
    second = manager.start_focus("Second")
    assert manager.active.id == second.id
    sessions = storage.get_focus_sessions()
    assert len(sessions) == 2
    ended = next(s for s in sessions if s.id == first.id)
    assert ended.is_active is False


def test_stop_marks_completed(env):
    manager, clock, _ctrl, _storage = env
    manager.start_focus()
    clock.advance(120)
    stopped = manager.stop(completed=True)
    assert stopped is not None
    assert stopped.completed is True
    assert manager.active is None


def test_stop_without_active_returns_none(env):
    manager, _clock, _ctrl, _storage = env
    assert manager.stop() is None


def test_tick_autostarts_break(env):
    manager, clock, _ctrl, _storage = env
    manager.start_focus(minutes=25)
    clock.advance(25 * 60)
    new_session = manager.tick()
    assert new_session is not None
    assert new_session.kind == "break"
    assert manager.active.kind == "break"
    assert manager.active.blocklist == []


def test_tick_break_returns_to_idle(env):
    manager, clock, _ctrl, _storage = env
    manager.start_break(minutes=5)
    clock.advance(5 * 60)
    assert manager.tick() is None
    assert manager.active is None


def test_tick_no_autopomodoro(env):
    manager, clock, _ctrl, storage = env
    manager.auto_pomodoro = False
    manager.start_focus(minutes=1)
    clock.advance(61)
    assert manager.tick() is None
    assert manager.active is None


def test_tick_not_elapsed_noop(env):
    manager, clock, _ctrl, _storage = env
    manager.start_focus(minutes=25)
    clock.advance(60)
    assert manager.tick() is None
    assert manager.active is not None


def test_enforce_blocks_during_focus(env):
    manager, _clock, controller, _storage = env
    manager.start_focus(blocklist=["youtube"])
    acted = manager.enforce(WindowSample(app="YouTube", title="x", timestamp=0.0))
    assert acted is True
    assert controller.minimize_calls == 1


def test_enforce_ignores_during_break(env):
    manager, _clock, controller, _storage = env
    manager.start_break()
    acted = manager.enforce(WindowSample(app="YouTube", title="x", timestamp=0.0))
    assert acted is False
    assert controller.minimize_calls == 0


def test_enforce_no_active_session(env):
    manager, _clock, _ctrl, _storage = env
    assert (
        manager.enforce(WindowSample(app="YouTube", title="x", timestamp=0.0)) is False
    )


def test_status_inactive_and_active(env):
    manager, clock, _ctrl, _storage = env
    assert manager.status() == {"active": False}
    manager.start_focus("Deep", minutes=25)
    clock.advance(300)
    status = manager.status()
    assert status["active"] is True
    assert status["label"] == "Deep"
    assert status["remaining"] == pytest.approx(1200.0)
    assert status["elapsed"] == pytest.approx(300.0)


def test_manager_recovers_active_session_from_storage():
    storage = Storage(":memory:")
    clock = Clock()
    m1 = FocusManager(storage, clock=clock)
    m1.start_focus("Persisted")
    # A fresh manager should pick up the running session from the DB.
    m2 = FocusManager(storage, clock=clock)
    assert m2.active is not None
    assert m2.active.label == "Persisted"
    storage.close()
