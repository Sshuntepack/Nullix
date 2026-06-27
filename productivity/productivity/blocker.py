"""App blocking enforced during focus sessions."""

from __future__ import annotations

import shutil
import subprocess
from typing import Protocol, runtime_checkable

from productivity.models import WindowSample


def is_blocked(sample: WindowSample, blocklist: list[str]) -> bool:
    """Return ``True`` if the sample matches any blocklist entry.

    Matching is a case-insensitive substring test against ``"<app> <title>"``.
    """
    if not blocklist:
        return False
    haystack = f"{sample.app} {sample.title}".lower()
    return any(entry.strip().lower() in haystack for entry in blocklist if entry)


@runtime_checkable
class WindowController(Protocol):
    """Performs the actual enforcement action on a window."""

    def minimize_active(self) -> bool:
        """Minimize/hide the foreground window. Returns success."""
        ...


class NullController:
    """A controller that records calls but takes no real action (tests/demo)."""

    def __init__(self) -> None:
        self.minimize_calls = 0

    def minimize_active(self) -> bool:
        self.minimize_calls += 1
        return True


class WmctrlController:
    """Minimizes the active window using ``xdotool``/``wmctrl``."""

    def __init__(self) -> None:
        self._xdotool = shutil.which("xdotool")

    def minimize_active(self) -> bool:
        if not self._xdotool:
            return False
        try:
            subprocess.run(
                ["xdotool", "getactivewindow", "windowminimize"],
                capture_output=True,
                timeout=2.0,
                check=False,
            )
        except (subprocess.SubprocessError, OSError):
            return False
        return True


class Blocker:
    """Enforces a blocklist by minimizing distracting windows on sight."""

    def __init__(self, controller: WindowController | None = None) -> None:
        self._controller = controller or NullController()
        self.blocks_enforced = 0

    def enforce(self, sample: WindowSample, blocklist: list[str]) -> bool:
        """If the sample is blocked, act on it. Returns whether it acted."""
        if not is_blocked(sample, blocklist):
            return False
        acted = self._controller.minimize_active()
        if acted:
            self.blocks_enforced += 1
        return acted
