"""Configuration: file locations and default categorization rules."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

APP_NAME = "productivity"


def _xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def _xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def config_dir() -> Path:
    """Directory that holds user configuration (rules, settings)."""
    return _xdg_config_home() / APP_NAME


def data_dir() -> Path:
    """Directory that holds the activity database."""
    return _xdg_data_home() / APP_NAME


def default_db_path() -> Path:
    """Default path to the SQLite database."""
    return data_dir() / "activity.db"


def rules_path() -> Path:
    """Path to the user-editable categorization rules file."""
    return config_dir() / "rules.json"


# Default rules: (substring matched against "app title", category, project).
# Matching is case-insensitive and order-sensitive (first match wins).
DEFAULT_RULES: list[tuple[str, str, str | None]] = [
    ("code", "productive", "Engineering"),
    ("vim", "productive", "Engineering"),
    ("pycharm", "productive", "Engineering"),
    ("intellij", "productive", "Engineering"),
    ("terminal", "productive", "Engineering"),
    ("iterm", "productive", "Engineering"),
    ("kitty", "productive", "Engineering"),
    ("gnome-terminal", "productive", "Engineering"),
    ("github", "productive", "Engineering"),
    ("stack overflow", "productive", "Engineering"),
    ("localhost", "productive", "Engineering"),
    ("figma", "productive", "Design"),
    ("notion", "productive", "Planning"),
    ("linear", "productive", "Planning"),
    ("docs.google", "productive", "Writing"),
    ("obsidian", "productive", "Writing"),
    ("youtube", "distracting", "Media"),
    ("netflix", "distracting", "Media"),
    ("twitch", "distracting", "Media"),
    ("reddit", "distracting", "Social"),
    ("twitter", "distracting", "Social"),
    ("x.com", "distracting", "Social"),
    ("instagram", "distracting", "Social"),
    ("facebook", "distracting", "Social"),
    ("tiktok", "distracting", "Social"),
    ("discord", "distracting", "Social"),
    ("steam", "distracting", "Games"),
]


@dataclass
class Settings:
    """Runtime settings for the tracker and dashboard."""

    db_path: Path = field(default_factory=default_db_path)
    poll_interval: float = 2.0
    idle_threshold: float = 120.0
    rules: list[tuple[str, str, str | None]] = field(
        default_factory=lambda: list(DEFAULT_RULES)
    )


def load_rules(path: Path | None = None) -> list[tuple[str, str, str | None]]:
    """Load categorization rules from disk, falling back to the defaults.

    The rules file is a JSON list of ``{"match", "category", "project"}``
    objects. Missing or malformed files yield :data:`DEFAULT_RULES`.
    """
    path = path or rules_path()
    if not path.exists():
        return list(DEFAULT_RULES)
    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return list(DEFAULT_RULES)
    rules: list[tuple[str, str, str | None]] = []
    for item in raw:
        match = item.get("match")
        category = item.get("category", "neutral")
        if not match:
            continue
        rules.append((str(match), str(category), item.get("project")))
    return rules or list(DEFAULT_RULES)


def save_rules(
    rules: list[tuple[str, str, str | None]], path: Path | None = None
) -> Path:
    """Persist categorization rules to disk as JSON."""
    path = path or rules_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {"match": match, "category": category, "project": project}
        for match, category, project in rules
    ]
    path.write_text(json.dumps(payload, indent=2))
    return path
