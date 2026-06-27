"""Automated Desktop Productivity Manager.

A self-contained toolkit that tracks how you spend time on your computer,
categorizes activity (productive / distracting / neutral), runs focus
sessions with optional app blocking, and serves an analytics dashboard.
"""

from productivity.models import Activity, Category, FocusSession, WindowSample

__version__ = "0.1.0"

__all__ = [
    "Activity",
    "Category",
    "FocusSession",
    "WindowSample",
    "__version__",
]
