"""Wires storage, tracker, focus, and blocking into one running service."""

from __future__ import annotations

from productivity.blocker import Blocker, WmctrlController
from productivity.categorizer import Categorizer
from productivity.config import Settings, load_rules
from productivity.focus import FocusManager
from productivity.models import WindowSample
from productivity.storage import Storage
from productivity.tracker import Tracker
from productivity.window_provider import WindowProvider, default_provider


class ProductivityService:
    """Assembles and runs the tracker + focus manager together.

    The tracker's per-sample hook drives the Pomodoro state machine and
    enforces the active focus blocklist, so a single background loop powers
    both time tracking and app blocking.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        provider: WindowProvider | None = None,
        enforce_blocking: bool = True,
    ) -> None:
        self.settings = settings or Settings()
        self.storage = Storage(self.settings.db_path)
        self.categorizer = Categorizer(self.settings.rules or load_rules())
        controller = WmctrlController() if enforce_blocking else None
        self.focus = FocusManager(self.storage, blocker=Blocker(controller))
        self.provider = provider or default_provider(self.settings.idle_threshold)
        self.tracker = Tracker(
            self.storage,
            provider=self.provider,
            categorizer=self.categorizer,
            poll_interval=self.settings.poll_interval,
            focus_lookup=self.focus.active_session_id,
            sample_hook=self._on_sample,
        )

    def _on_sample(self, sample: WindowSample) -> None:
        self.focus.tick()
        self.focus.enforce(sample)

    def start(self) -> None:
        """Start the background tracking + focus loop."""
        self.tracker.start()

    def stop(self) -> None:
        """Stop the tracker and flush state."""
        self.tracker.stop()

    def close(self) -> None:
        """Stop and release resources."""
        self.stop()
        self.storage.close()
