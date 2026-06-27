from datetime import datetime

from productivity import analytics
from productivity.models import Activity, Category


def act(app, start, end, category=Category.PRODUCTIVE, project="Engineering"):
    return Activity(
        app=app,
        title="t",
        category=category,
        start_ts=start,
        end_ts=end,
        project=project,
    )


def test_summarize_totals():
    activities = [
        act("Code", 0, 100),
        act("Chrome", 100, 150, category=Category.DISTRACTING, project="Media"),
        act("Reader", 150, 200, category=Category.NEUTRAL, project=None),
    ]
    summary = analytics.summarize(activities)
    assert summary.total_seconds == 200
    assert summary.by_category["productive"] == 100
    assert summary.by_category["distracting"] == 50
    assert summary.by_category["neutral"] == 50


def test_productivity_score_excludes_neutral():
    by_cat = {"productive": 80, "distracting": 20, "neutral": 1000}
    assert analytics.productivity_score(by_cat) == 0.8


def test_productivity_score_zero_when_no_engaged():
    assert analytics.productivity_score({"neutral": 100}) == 0.0


def test_summary_as_dict_rounds():
    summary = analytics.summarize([act("Code", 0, 33.333)])
    d = summary.as_dict()
    assert d["total_seconds"] == 33.3
    assert "productive" in d["by_category"]


def test_by_app_sorted_desc_and_topn():
    activities = [
        act("Code", 0, 300),
        act("Chrome", 300, 360, category=Category.DISTRACTING),
        act("Code", 360, 420),
    ]
    rows = analytics.by_app(activities)
    assert rows[0]["app"] == "Code"
    assert rows[0]["seconds"] == 360
    top1 = analytics.by_app(activities, top_n=1)
    assert len(top1) == 1


def test_by_app_uses_dominant_category():
    # Chrome spends more time distracting than productive -> labeled distracting.
    activities = [
        act("Chrome", 0, 60, category=Category.PRODUCTIVE),
        act("Chrome", 60, 360, category=Category.DISTRACTING),
    ]
    rows = analytics.by_app(activities)
    assert rows[0]["app"] == "Chrome"
    assert rows[0]["category"] == "distracting"


def test_by_project_groups_uncategorized():
    activities = [
        act("Code", 0, 60, project="Engineering"),
        act("Reader", 60, 120, category=Category.NEUTRAL, project=None),
    ]
    rows = analytics.by_project(activities)
    projects = {r["project"]: r["seconds"] for r in rows}
    assert projects["Engineering"] == 60
    assert projects["Uncategorized"] == 60


def test_hourly_breakdown_24_buckets():
    base = datetime(2024, 1, 1, 10, 0, 0).timestamp()
    activities = [act("Code", base, base + 1800)]  # 30 min at 10:00
    hourly = analytics.hourly_breakdown(activities)
    assert len(hourly) == 24
    assert hourly[10]["productive"] == 1800
    assert hourly[11]["productive"] == 0


def test_hourly_breakdown_spans_hours():
    base = datetime(2024, 1, 1, 10, 30, 0).timestamp()
    activities = [act("Code", base, base + 3600)]  # 10:30 -> 11:30
    hourly = analytics.hourly_breakdown(activities)
    assert hourly[10]["productive"] == 1800
    assert hourly[11]["productive"] == 1800


def test_daily_totals_sorted():
    d1 = datetime(2024, 1, 1, 9, 0, 0).timestamp()
    d2 = datetime(2024, 1, 2, 9, 0, 0).timestamp()
    activities = [
        act("Code", d2, d2 + 60),
        act("Code", d1, d1 + 120),
    ]
    daily = analytics.daily_totals(activities)
    assert [d["date"] for d in daily] == ["2024-01-01", "2024-01-02"]
    assert daily[0]["productive"] == 120


def test_build_dashboard_keys():
    activities = [act("Code", 0, 60)]
    payload = analytics.build_dashboard(activities)
    assert set(payload) == {"summary", "by_app", "by_project", "hourly", "daily"}


def test_empty_inputs():
    assert analytics.summarize([]).total_seconds == 0
    assert analytics.by_app([]) == []
    assert analytics.by_project([]) == []
    assert analytics.daily_totals([]) == []
    assert len(analytics.hourly_breakdown([])) == 24
