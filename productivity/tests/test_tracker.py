from productivity.categorizer import Categorizer
from productivity.models import WindowSample
from productivity.storage import Storage
from productivity.tracker import SessionAggregator, Tracker
from productivity.window_provider import FakeWindowProvider


def s(app, ts, title="t", idle=False):
    return WindowSample(app=app, title=title, timestamp=ts, idle=idle)


def test_aggregator_extends_same_app():
    agg = SessionAggregator()
    assert agg.feed(s("Code", 0)) is None
    assert agg.feed(s("Code", 10)) is None
    assert agg.current is not None
    assert agg.current.end_ts == 10


def test_aggregator_closes_on_app_change():
    agg = SessionAggregator()
    agg.feed(s("Code", 0))
    finished = agg.feed(s("Chrome", 30))
    assert finished is not None
    assert finished.app == "Code"
    assert finished.duration == 30
    # New segment started for Chrome.
    assert agg.current is not None
    assert agg.current.app == "Chrome"


def test_aggregator_idle_finalizes_and_skips():
    agg = SessionAggregator()
    agg.feed(s("Code", 0))
    finished = agg.feed(s("Code", 20, idle=True))
    assert finished is not None
    assert finished.duration == 20
    # Idle sample did not start a new segment.
    assert agg.current is None


def test_aggregator_min_duration_filter():
    agg = SessionAggregator(min_duration=5.0)
    agg.feed(s("Code", 0))
    # Switch after only 2s -> below threshold -> dropped.
    finished = agg.feed(s("Chrome", 2))
    assert finished is None


def test_aggregator_flush():
    agg = SessionAggregator()
    agg.feed(s("Code", 0))
    finished = agg.flush(now=99)
    assert finished is not None
    assert finished.end_ts == 99
    assert agg.flush() is None


def test_aggregator_classifies_category():
    agg = SessionAggregator(Categorizer())
    agg.feed(s("reddit", 0, title="r/python"))
    finished = agg.feed(s("Code", 60))
    assert finished is not None
    assert finished.category.value == "distracting"
    assert finished.project == "Social"


def test_tracker_poll_persists_on_switch():
    storage = Storage(":memory:")
    provider = FakeWindowProvider([s("Code", 0), s("Code", 10), s("Chrome", 20)])
    tracker = Tracker(storage, provider=provider, min_duration=0.0)
    assert tracker.poll_once() is None  # start Code
    assert tracker.poll_once() is None  # extend Code
    finished = tracker.poll_once()  # switch -> persist Code
    assert finished is not None
    assert len(storage.get_activities()) == 1
    storage.close()


def test_tracker_focus_lookup_tags_activity():
    from productivity.models import FocusSession

    storage = Storage(":memory:")
    session_id = storage.add_focus_session(
        FocusSession(label="Focus", start_ts=0.0, planned_seconds=1500)
    )
    provider = FakeWindowProvider([s("Code", 0), s("Chrome", 10)])
    tracker = Tracker(
        storage,
        provider=provider,
        min_duration=0.0,
        focus_lookup=lambda: session_id,
    )
    tracker.poll_once()
    tracker.poll_once()
    activities = storage.get_activities()
    assert activities[0].focus_session_id == session_id
    storage.close()


def test_tracker_sample_hook_called():
    storage = Storage(":memory:")
    seen = []
    provider = FakeWindowProvider([s("Code", 0)])
    tracker = Tracker(
        storage, provider=provider, sample_hook=lambda sm: seen.append(sm.app)
    )
    tracker.poll_once()
    assert seen == ["Code"]
    storage.close()


def test_tracker_handles_none_sample():
    storage = Storage(":memory:")

    class NoneProvider:
        def sample(self):
            return None

    tracker = Tracker(storage, provider=NoneProvider())
    assert tracker.poll_once() is None
    storage.close()
