import pytest

from productivity.models import Activity, Category, FocusSession
from productivity.storage import Storage


@pytest.fixture
def storage():
    s = Storage(":memory:")
    yield s
    s.close()


def _activity(start, end, app="Code", category=Category.PRODUCTIVE):
    return Activity(
        app=app,
        title="t",
        category=category,
        start_ts=start,
        end_ts=end,
        project="Engineering",
    )


def test_add_and_get_activity(storage):
    new_id = storage.add_activity(_activity(100, 160))
    assert new_id == 1
    rows = storage.get_activities()
    assert len(rows) == 1
    assert rows[0].id == 1
    assert rows[0].duration == 60
    assert rows[0].project == "Engineering"


def test_get_activities_time_window(storage):
    storage.add_activity(_activity(0, 50))
    storage.add_activity(_activity(100, 150))
    storage.add_activity(_activity(200, 260))
    # Window [120, 210) overlaps only the middle and last activity.
    rows = storage.get_activities(start=120, end=210)
    starts = sorted(r.start_ts for r in rows)
    assert starts == [100, 200]


def test_add_activities_bulk(storage):
    storage.add_activities([_activity(0, 10), _activity(10, 20)])
    assert len(storage.get_activities()) == 2


def test_focus_session_lifecycle(storage):
    session = FocusSession(
        label="Deep Work",
        start_ts=1000.0,
        planned_seconds=1500,
        blocklist=["youtube", "reddit"],
    )
    sid = storage.add_focus_session(session)
    assert sid == 1

    active = storage.active_focus_session()
    assert active is not None
    assert active.label == "Deep Work"
    assert active.blocklist == ["youtube", "reddit"]
    assert active.is_active is True

    session.end_ts = 2500.0
    session.completed = True
    storage.update_focus_session(session)
    assert storage.active_focus_session() is None

    finished = storage.get_focus_sessions()
    assert len(finished) == 1
    assert finished[0].completed is True


def test_update_focus_without_id_raises(storage):
    with pytest.raises(ValueError):
        storage.update_focus_session(
            FocusSession(label="x", start_ts=0.0, planned_seconds=60)
        )


def test_empty_blocklist_roundtrip(storage):
    storage.add_focus_session(
        FocusSession(label="Break", start_ts=0.0, planned_seconds=300, kind="break")
    )
    active = storage.active_focus_session()
    assert active is not None
    assert active.blocklist == []
    assert active.kind == "break"


def test_context_manager_closes():
    with Storage(":memory:") as s:
        s.add_activity(_activity(0, 5))
        assert len(s.get_activities()) == 1
