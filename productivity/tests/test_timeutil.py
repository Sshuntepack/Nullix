from datetime import datetime

from productivity.timeutil import day_bounds, format_duration, range_bounds


def test_day_bounds_span_24h():
    day = datetime(2024, 3, 15, 14, 30, 0)
    start, end = day_bounds(day)
    assert end - start == 86400
    assert datetime.fromtimestamp(start).hour == 0


def test_range_bounds_span_days():
    now = datetime(2024, 3, 15, 14, 30, 0)
    start, end = range_bounds(7, now=now)
    assert round((end - start) / 86400) == 7


def test_range_bounds_minimum_one_day():
    now = datetime(2024, 3, 15, 14, 30, 0)
    start, end = range_bounds(0, now=now)
    assert round((end - start) / 86400) == 1


def test_format_duration_seconds():
    assert format_duration(45) == "45s"


def test_format_duration_minutes():
    assert format_duration(125) == "2m 5s"


def test_format_duration_hours():
    assert format_duration(3 * 3600 + 25 * 60) == "3h 25m"
