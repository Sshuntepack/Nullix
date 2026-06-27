"""Generate realistic demo data so the dashboard is populated for previews."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from productivity.categorizer import Categorizer
from productivity.models import Activity
from productivity.storage import Storage

# (app, title, weight) — weight biases how often the app is picked.
_APPS = [
    ("Code", "productivity/tracker.py - Visual Studio Code", 9),
    ("gnome-terminal", "pytest - terminal", 6),
    ("Chrome", "GitHub - Pull Request", 5),
    ("Chrome", "Stack Overflow - python threading", 3),
    ("Chrome", "localhost:8765 - Dashboard", 3),
    ("Notion", "Roadmap - Notion", 3),
    ("Figma", "Dashboard UI - Figma", 2),
    ("Chrome", "YouTube - Lo-fi beats", 4),
    ("Chrome", "reddit - r/programming", 3),
    ("Discord", "general - Discord", 2),
    ("Slack", "team - Slack", 2),
    ("Chrome", "Twitter / X", 2),
]


def seed_demo_data(storage: Storage, days: int = 3, seed: int = 7) -> int:
    """Populate ``storage`` with believable activity over the last ``days``.

    Returns the number of activities inserted. Deterministic for a given seed.
    """
    rng = random.Random(seed)
    categorizer = Categorizer()
    weighted: list[tuple[str, str]] = []
    for app, title, weight in _APPS:
        weighted.extend([(app, title)] * weight)

    count = 0
    today = datetime.now().replace(minute=0, second=0, microsecond=0)
    for day_offset in range(days):
        day_start = (today - timedelta(days=day_offset)).replace(hour=9)
        # Stop "now" on the current day so we never write the future.
        cap = datetime.now() if day_offset == 0 else day_start + timedelta(hours=9)
        cursor = day_start
        while cursor < cap:
            app, title = rng.choice(weighted)
            block = rng.randint(4, 28) * 60  # 4–28 minutes
            end = min(cursor + timedelta(seconds=block), cap)
            category, project = categorizer.classify(app, title)
            storage.add_activity(
                Activity(
                    app=app,
                    title=title,
                    category=category,
                    project=project,
                    start_ts=cursor.timestamp(),
                    end_ts=end.timestamp(),
                )
            )
            count += 1
            # occasional short break gap
            cursor = end + timedelta(seconds=rng.choice([0, 0, 0, 120, 300]))
    return count
