from productivity.blocker import Blocker, NullController, is_blocked
from productivity.models import WindowSample


def sample(app, title=""):
    return WindowSample(app=app, title=title, timestamp=0.0)


def test_is_blocked_matches_app():
    assert is_blocked(sample("YouTube"), ["youtube"]) is True


def test_is_blocked_matches_title():
    assert is_blocked(sample("Chrome", "reddit - r/x"), ["reddit"]) is True


def test_is_blocked_no_match():
    assert is_blocked(sample("Code"), ["youtube", "reddit"]) is False


def test_is_blocked_empty_list():
    assert is_blocked(sample("YouTube"), []) is False


def test_blocker_enforces_and_counts():
    controller = NullController()
    blocker = Blocker(controller)
    acted = blocker.enforce(sample("YouTube"), ["youtube"])
    assert acted is True
    assert blocker.blocks_enforced == 1
    assert controller.minimize_calls == 1


def test_blocker_ignores_allowed():
    controller = NullController()
    blocker = Blocker(controller)
    assert blocker.enforce(sample("Code"), ["youtube"]) is False
    assert controller.minimize_calls == 0


def test_blocker_handles_failed_controller():
    class FailController:
        def minimize_active(self):
            return False

    blocker = Blocker(FailController())
    acted = blocker.enforce(sample("YouTube"), ["youtube"])
    assert acted is False
    assert blocker.blocks_enforced == 0
