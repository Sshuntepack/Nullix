"""Foreground-window detection abstractions.

The tracker depends only on the :class:`WindowProvider` protocol, which makes
it trivial to unit-test with a fake provider and to add new backends.
"""

from __future__ import annotations

import shutil
import subprocess
import time
from typing import Protocol, runtime_checkable

from productivity.models import WindowSample


@runtime_checkable
class WindowProvider(Protocol):
    """Returns a sample describing the current foreground window."""

    def sample(self) -> WindowSample | None:
        """Return the active window, or ``None`` if it cannot be read."""
        ...


class FakeWindowProvider:
    """A scripted provider that replays a fixed list of samples.

    Useful for tests and demos. When the script is exhausted it keeps
    returning the final sample.
    """

    def __init__(self, samples: list[WindowSample]) -> None:
        self._samples = list(samples)
        self._index = 0

    def sample(self) -> WindowSample | None:
        if not self._samples:
            return None
        sample = self._samples[min(self._index, len(self._samples) - 1)]
        self._index += 1
        return sample


class X11WindowProvider:
    """Reads the active window on Linux/X11 via ``xdotool`` and ``xprop``.

    Falls back gracefully (returning ``None``) when the tools are missing or
    no window is focused. Idle time is detected with ``xprintidle`` when
    available.
    """

    def __init__(self, idle_threshold: float = 120.0) -> None:
        self.idle_threshold = idle_threshold
        self._xdotool = shutil.which("xdotool")
        self._xprop = shutil.which("xprop")
        self._xprintidle = shutil.which("xprintidle")

    def _run(self, args: list[str]) -> str | None:
        try:
            out = subprocess.run(args, capture_output=True, text=True, timeout=2.0)
        except (subprocess.SubprocessError, OSError):
            return None
        if out.returncode != 0:
            return None
        return out.stdout.strip()

    def _idle_seconds(self) -> float:
        if not self._xprintidle:
            return 0.0
        out = self._run([self._xprintidle])
        if out is None or not out.isdigit():
            return 0.0
        return int(out) / 1000.0

    def _app_name(self, window_id: str) -> str:
        if not self._xprop:
            return ""
        out = self._run(["xprop", "-id", window_id, "WM_CLASS"])
        if not out or "=" not in out:
            return ""
        # WM_CLASS(STRING) = "instance", "Class"
        values = out.split("=", 1)[1]
        parts = [p.strip().strip('"') for p in values.split(",")]
        return parts[-1] if parts else ""

    def sample(self) -> WindowSample | None:
        if not self._xdotool:
            return None
        window_id = self._run(["xdotool", "getactivewindow"])
        if not window_id:
            return None
        title = self._run(["xdotool", "getwindowname", window_id]) or ""
        app = self._app_name(window_id) or title.split(" - ")[-1]
        idle = self._idle_seconds() >= self.idle_threshold
        return WindowSample(
            app=app or "unknown",
            title=title,
            timestamp=time.time(),
            idle=idle,
        )


def default_provider(idle_threshold: float = 120.0) -> WindowProvider:
    """Return the best window provider available on this platform."""
    return X11WindowProvider(idle_threshold=idle_threshold)
