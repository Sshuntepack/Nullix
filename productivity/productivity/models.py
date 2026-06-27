"""Core data models shared across the application."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Category(str, Enum):
    """The productivity classification of an activity."""

    PRODUCTIVE = "productive"
    DISTRACTING = "distracting"
    NEUTRAL = "neutral"

    @classmethod
    def from_value(cls, value: str) -> "Category":
        """Parse a category from a string, defaulting to ``NEUTRAL``."""
        try:
            return cls(value.strip().lower())
        except (ValueError, AttributeError):
            return cls.NEUTRAL


@dataclass(frozen=True)
class WindowSample:
    """A single observation of the foreground window at a point in time."""

    app: str
    title: str
    timestamp: float
    idle: bool = False

    def normalized_app(self) -> str:
        """Return a lowercased, stripped application name."""
        return self.app.strip().lower()


@dataclass
class Activity:
    """A contiguous block of time spent in one application."""

    app: str
    title: str
    category: Category
    start_ts: float
    end_ts: float
    project: str | None = None
    focus_session_id: int | None = None
    id: int | None = None

    @property
    def duration(self) -> float:
        """Duration of the activity in seconds (never negative)."""
        return max(0.0, self.end_ts - self.start_ts)


@dataclass
class FocusSession:
    """A focus (or break) session, optionally enforcing an app blocklist."""

    label: str
    start_ts: float
    planned_seconds: int
    kind: str = "focus"  # "focus" or "break"
    end_ts: float | None = None
    completed: bool = False
    blocklist: list[str] = field(default_factory=list)
    id: int | None = None

    @property
    def is_active(self) -> bool:
        """Whether the session is currently running."""
        return self.end_ts is None

    def elapsed(self, now: float) -> float:
        """Seconds elapsed since the session started."""
        end = self.end_ts if self.end_ts is not None else now
        return max(0.0, end - self.start_ts)

    def remaining(self, now: float) -> float:
        """Seconds remaining before the planned duration is reached."""
        return max(0.0, self.planned_seconds - self.elapsed(now))
