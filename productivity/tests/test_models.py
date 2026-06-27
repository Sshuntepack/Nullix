from productivity.models import Activity, Category, FocusSession, WindowSample


def test_category_from_value_known():
    assert Category.from_value("Productive") is Category.PRODUCTIVE
    assert Category.from_value("  DISTRACTING ") is Category.DISTRACTING


def test_category_from_value_unknown_defaults_neutral():
    assert Category.from_value("nonsense") is Category.NEUTRAL
    assert Category.from_value(None) is Category.NEUTRAL  # type: ignore[arg-type]


def test_window_sample_normalized_app():
    sample = WindowSample(app="  Visual Studio CODE ", title="x", timestamp=1.0)
    assert sample.normalized_app() == "visual studio code"


def test_activity_duration_never_negative():
    a = Activity(
        app="Code",
        title="t",
        category=Category.PRODUCTIVE,
        start_ts=100.0,
        end_ts=90.0,
    )
    assert a.duration == 0.0
    b = Activity(
        app="Code",
        title="t",
        category=Category.PRODUCTIVE,
        start_ts=100.0,
        end_ts=160.0,
    )
    assert b.duration == 60.0


def test_focus_session_timing():
    s = FocusSession(label="Focus", start_ts=0.0, planned_seconds=1500)
    assert s.is_active is True
    assert s.elapsed(600.0) == 600.0
    assert s.remaining(600.0) == 900.0
    assert s.remaining(2000.0) == 0.0


def test_focus_session_elapsed_after_end():
    s = FocusSession(label="Focus", start_ts=0.0, planned_seconds=1500, end_ts=300.0)
    assert s.is_active is False
    assert s.elapsed(900.0) == 300.0
