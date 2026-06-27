"""Aggregation of window samples into activities, and the tracking loop."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from productivity.categorizer import Categorizer
from productivity.models import Activity, WindowSample
from productivity.storage import Storage
from productivity.window_provider import WindowProvider, default_provider


class SessionAggregator:
    """Collapses a stream of window samples into contiguous activities.

    Feed samples in chronological order. Whenever the foreground application
    changes (or the user goes idle), the previous activity is finalized and
    returned. Idle samples never accrue time.
    """

    def __init__(
        self, categorizer: Categorizer | None = None, min_duration: float = 0.0
    ) -> None:
        self._categorizer = categorizer or Categorizer()
        self._min_duration = min_duration
        self._current: Activity | None = None

    @property
    def current(self) -> Activity | None:
        """The in-progress activity, if any."""
        return self._current

    def feed(self, sample: WindowSample) -> Activity | None:
        """Process one sample, returning a finalized activity if one closed."""
        if sample.idle:
            return self._finalize(sample.timestamp)

        category, project = self._categorizer.classify_sample(sample)
        if self._current is None:
            self._start(sample, category, project)
            return None

        if sample.normalized_app() == self._current.app.strip().lower():
            self._current.end_ts = sample.timestamp
            if sample.title:
                self._current.title = sample.title
            return None

        finished = self._finalize(sample.timestamp)
        self._start(sample, category, project)
        return finished

    def flush(self, now: float | None = None) -> Activity | None:
        """Finalize and return the in-progress activity, if any."""
        return self._finalize(now if now is not None else time.time())

    def _start(self, sample: WindowSample, category, project) -> None:
        self._current = Activity(
            app=sample.app,
            title=sample.title,
            category=category,
            project=project,
            start_ts=sample.timestamp,
            end_ts=sample.timestamp,
        )

    def _finalize(self, end_ts: float) -> Activity | None:
        current = self._current
        self._current = None
        if current is None:
            return None
        current.end_ts = max(current.end_ts, end_ts)
        if current.duration < self._min_duration:
            return None
        return current


class Tracker:
    """Runs the sampling loop and persists activities to storage."""

    def __init__(
        self,
        storage: Storage,
        provider: WindowProvider | None = None,
        categorizer: Categorizer | None = None,
        poll_interval: float = 2.0,
        min_duration: float = 1.0,
        focus_lookup: Callable[[], int | None] | None = None,
        on_activity: Callable[[Activity], None] | None = None,
        sample_hook: Callable[[WindowSample], None] | None = None,
    ) -> None:
        self._storage = storage
        self._provider = provider or default_provider()
        self._aggregator = SessionAggregator(categorizer, min_duration=min_duration)
        self._poll_interval = poll_interval
        self._focus_lookup = focus_lookup
        self._on_activity = on_activity
        self._sample_hook = sample_hook
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def poll_once(self) -> Activity | None:
        """Take a single sample and persist any finalized activity."""
        sample = self._provider.sample()
        if sample is None:
            return None
        if self._sample_hook is not None:
            self._sample_hook(sample)
        finished = self._aggregator.feed(sample)
        if finished is not None:
            self._persist(finished)
        return finished

    def _persist(self, activity: Activity) -> None:
        if self._focus_lookup is not None:
            activity.focus_session_id = self._focus_lookup()
        self._storage.add_activity(activity)
        if self._on_activity is not None:
            self._on_activity(activity)

    def _run(self) -> None:
        while not self._stop.is_set():
            self.poll_once()
            self._stop.wait(self._poll_interval)
        leftover = self._aggregator.flush()
        if leftover is not None:
            self._persist(leftover)

    def start(self) -> None:
        """Start the tracking loop on a background thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the tracking loop and flush any pending activity."""
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self._poll_interval + 2.0)
            self._thread = None
