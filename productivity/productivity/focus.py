"""Focus / Pomodoro session management."""

from __future__ import annotations

import time
from collections.abc import Callable

from productivity.blocker import Blocker
from productivity.models import FocusSession, WindowSample
from productivity.storage import Storage

DEFAULT_BLOCKLIST = [
    "youtube",
    "netflix",
    "twitch",
    "reddit",
    "twitter",
    "x.com",
    "instagram",
    "facebook",
    "tiktok",
    "discord",
    "steam",
]


class FocusManager:
    """Coordinates focus/break sessions, persistence, and blocking.

    When ``auto_pomodoro`` is enabled, completing a focus session
    automatically starts a break, and completing a break returns to idle.
    All time math is driven by an injectable ``clock`` for testability.
    """

    def __init__(
        self,
        storage: Storage,
        blocker: Blocker | None = None,
        clock: Callable[[], float] = time.time,
        focus_minutes: int = 25,
        break_minutes: int = 5,
        auto_pomodoro: bool = True,
        blocklist: list[str] | None = None,
    ) -> None:
        self._storage = storage
        self._blocker = blocker or Blocker()
        self._clock = clock
        self.focus_minutes = focus_minutes
        self.break_minutes = break_minutes
        self.auto_pomodoro = auto_pomodoro
        self.blocklist = (
            list(blocklist) if blocklist is not None else list(DEFAULT_BLOCKLIST)
        )
        self._active: FocusSession | None = storage.active_focus_session()

    @property
    def active(self) -> FocusSession | None:
        """The currently running session, if any."""
        return self._active

    def active_session_id(self) -> int | None:
        """Return the id of the active session for activity tagging."""
        return self._active.id if self._active else None

    def start_focus(
        self,
        label: str = "Focus",
        minutes: int | None = None,
        blocklist: list[str] | None = None,
    ) -> FocusSession:
        """Start a focus session, ending any session already running."""
        return self._start("focus", label, minutes or self.focus_minutes, blocklist)

    def start_break(
        self, label: str = "Break", minutes: int | None = None
    ) -> FocusSession:
        """Start a break session (no blocking)."""
        return self._start("break", label, minutes or self.break_minutes, [])

    def _start(
        self,
        kind: str,
        label: str,
        minutes: int,
        blocklist: list[str] | None,
    ) -> FocusSession:
        if self._active is not None:
            self.stop(completed=False)
        if kind == "focus":
            block = blocklist if blocklist is not None else self.blocklist
        else:
            block = []
        session = FocusSession(
            label=label,
            kind=kind,
            start_ts=self._clock(),
            planned_seconds=int(minutes * 60),
            blocklist=list(block),
        )
        self._storage.add_focus_session(session)
        self._active = session
        return session

    def stop(self, completed: bool = False) -> FocusSession | None:
        """End the active session, marking it completed or aborted."""
        if self._active is None:
            return None
        session = self._active
        session.end_ts = self._clock()
        session.completed = completed
        self._storage.update_focus_session(session)
        self._active = None
        return session

    def tick(self) -> FocusSession | None:
        """Advance the state machine; return a newly started session if any.

        Call this periodically. When the active session's planned time is up
        it is completed, and (if ``auto_pomodoro``) the next phase starts.
        """
        if self._active is None:
            return None
        if self._active.remaining(self._clock()) > 0:
            return None

        finished_kind = self._active.kind
        self.stop(completed=True)
        if not self.auto_pomodoro:
            return None
        if finished_kind == "focus":
            return self.start_break()
        return None

    def enforce(self, sample: WindowSample) -> bool:
        """Enforce the active focus blocklist against a window sample."""
        if self._active is None or self._active.kind != "focus":
            return False
        return self._blocker.enforce(sample, self._active.blocklist)

    def status(self) -> dict:
        """Return a JSON-serializable snapshot of the focus state."""
        if self._active is None:
            return {"active": False}
        now = self._clock()
        return {
            "active": True,
            "id": self._active.id,
            "label": self._active.label,
            "kind": self._active.kind,
            "elapsed": round(self._active.elapsed(now), 1),
            "remaining": round(self._active.remaining(now), 1),
            "planned_seconds": self._active.planned_seconds,
            "blocklist": self._active.blocklist,
        }
