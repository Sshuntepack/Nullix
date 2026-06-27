"""Small helpers for time-window math used by the CLI and web layer."""

from __future__ import annotations

from datetime import datetime, timedelta


def day_bounds(day: datetime | None = None) -> tuple[float, float]:
    """Return ``(start_ts, end_ts)`` epoch seconds for the given day."""
    day = day or datetime.now()
    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start.timestamp(), end.timestamp()


def range_bounds(days: int, now: datetime | None = None) -> tuple[float, float]:
    """Return ``(start_ts, end_ts)`` covering the last ``days`` days."""
    now = now or datetime.now()
    end = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start = end - timedelta(days=max(1, days))
    return start.timestamp(), end.timestamp()


def format_duration(seconds: float) -> str:
    """Human-friendly duration like ``2h 5m`` or ``45s``."""
    seconds = int(round(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {sec}s"
