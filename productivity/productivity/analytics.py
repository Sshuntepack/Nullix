"""Aggregate activities into dashboard-ready statistics."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from productivity.models import Activity, Category


@dataclass
class Summary:
    """High-level totals for a collection of activities."""

    total_seconds: float = 0.0
    by_category: dict[str, float] = field(default_factory=dict)
    productivity_score: float = 0.0

    def as_dict(self) -> dict:
        return {
            "total_seconds": round(self.total_seconds, 1),
            "by_category": {k: round(v, 1) for k, v in self.by_category.items()},
            "productivity_score": round(self.productivity_score, 3),
        }


def productivity_score(by_category: dict[str, float]) -> float:
    """Productive share of *engaged* (productive + distracting) time.

    Neutral time is excluded from the denominator so that, e.g., idle reading
    does not dilute the score. Returns 0.0 when there is no engaged time.
    """
    productive = by_category.get(Category.PRODUCTIVE.value, 0.0)
    distracting = by_category.get(Category.DISTRACTING.value, 0.0)
    engaged = productive + distracting
    if engaged <= 0:
        return 0.0
    return productive / engaged


def summarize(activities: Sequence[Activity]) -> Summary:
    """Compute total time and per-category breakdown."""
    by_category: dict[str, float] = defaultdict(float)
    total = 0.0
    for activity in activities:
        by_category[activity.category.value] += activity.duration
        total += activity.duration
    summary = Summary(
        total_seconds=total,
        by_category=dict(by_category),
        productivity_score=productivity_score(by_category),
    )
    return summary


def by_app(activities: Sequence[Activity], top_n: int | None = None) -> list[dict]:
    """Time spent per application, descending by duration.

    Each app is labeled with its *dominant* category (the one it spent the
    most time in), since a single app (e.g. a browser) can span categories.
    """
    totals: dict[str, float] = defaultdict(float)
    per_category: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for activity in activities:
        totals[activity.app] += activity.duration
        per_category[activity.app][activity.category.value] += activity.duration
    rows = [
        {
            "app": app,
            "seconds": round(seconds, 1),
            "category": max(per_category[app].items(), key=lambda kv: kv[1])[0],
        }
        for app, seconds in totals.items()
    ]
    rows.sort(key=lambda r: r["seconds"], reverse=True)
    return rows[:top_n] if top_n else rows


def by_project(activities: Sequence[Activity]) -> list[dict]:
    """Time spent per project label, descending by duration."""
    totals: dict[str, float] = defaultdict(float)
    for activity in activities:
        key = activity.project or "Uncategorized"
        totals[key] += activity.duration
    rows = [
        {"project": project, "seconds": round(seconds, 1)}
        for project, seconds in totals.items()
    ]
    rows.sort(key=lambda r: r["seconds"], reverse=True)
    return rows


def hourly_breakdown(activities: Sequence[Activity]) -> list[dict]:
    """Per-hour-of-day productive/distracting/neutral seconds (0..23)."""
    buckets: list[dict[str, float]] = [
        {
            Category.PRODUCTIVE.value: 0.0,
            Category.DISTRACTING.value: 0.0,
            Category.NEUTRAL.value: 0.0,
        }
        for _ in range(24)
    ]
    for activity in activities:
        _spread_over_hours(activity, buckets)
    return [
        {"hour": hour, **{k: round(v, 1) for k, v in bucket.items()}}
        for hour, bucket in enumerate(buckets)
    ]


def _spread_over_hours(activity: Activity, buckets: list[dict[str, float]]) -> None:
    """Distribute an activity's duration across the hour buckets it spans."""
    start = datetime.fromtimestamp(activity.start_ts)
    end = datetime.fromtimestamp(activity.end_ts)
    cat = activity.category.value
    cursor = start
    while cursor < end:
        next_hour = (cursor + timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )
        slice_end = min(next_hour, end)
        buckets[cursor.hour][cat] += (slice_end - cursor).total_seconds()
        cursor = slice_end


def daily_totals(activities: Sequence[Activity]) -> list[dict]:
    """Per-day productive/distracting/neutral seconds, sorted by date."""
    days: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            Category.PRODUCTIVE.value: 0.0,
            Category.DISTRACTING.value: 0.0,
            Category.NEUTRAL.value: 0.0,
        }
    )
    for activity in activities:
        day = datetime.fromtimestamp(activity.start_ts).strftime("%Y-%m-%d")
        days[day][activity.category.value] += activity.duration
    return [
        {"date": day, **{k: round(v, 1) for k, v in totals.items()}}
        for day, totals in sorted(days.items())
    ]


def build_dashboard(activities: Sequence[Activity], top_apps: int = 8) -> dict:
    """Assemble the full payload consumed by the web dashboard."""
    return {
        "summary": summarize(activities).as_dict(),
        "by_app": by_app(activities, top_n=top_apps),
        "by_project": by_project(activities),
        "hourly": hourly_breakdown(activities),
        "daily": daily_totals(activities),
    }
