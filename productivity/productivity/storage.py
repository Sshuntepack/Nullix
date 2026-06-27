"""SQLite persistence for activities and focus sessions."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from pathlib import Path

from productivity.models import Activity, Category, FocusSession

_SCHEMA = """
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    project TEXT,
    start_ts REAL NOT NULL,
    end_ts REAL NOT NULL,
    focus_session_id INTEGER,
    FOREIGN KEY (focus_session_id) REFERENCES focus_sessions(id)
);
CREATE INDEX IF NOT EXISTS idx_activities_start ON activities(start_ts);

CREATE TABLE IF NOT EXISTS focus_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'focus',
    start_ts REAL NOT NULL,
    end_ts REAL,
    planned_seconds INTEGER NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    blocklist TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_focus_start ON focus_sessions(start_ts);
"""


class Storage:
    """A thin repository around a SQLite database.

    Pass ``":memory:"`` as the path for an ephemeral in-memory database
    (useful for tests). The connection is created with
    ``check_same_thread=False`` so the tracker thread and the web server can
    share one instance.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        """Close the underlying connection."""
        self._conn.close()

    def __enter__(self) -> "Storage":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ----- activities -------------------------------------------------
    def add_activity(self, activity: Activity) -> int:
        """Insert an activity and return its new id."""
        cur = self._conn.execute(
            """
            INSERT INTO activities
                (app, title, category, project, start_ts, end_ts, focus_session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                activity.app,
                activity.title,
                activity.category.value,
                activity.project,
                activity.start_ts,
                activity.end_ts,
                activity.focus_session_id,
            ),
        )
        self._conn.commit()
        activity.id = int(cur.lastrowid)
        return activity.id

    def get_activities(
        self, start: float | None = None, end: float | None = None
    ) -> list[Activity]:
        """Return activities overlapping the ``[start, end)`` window."""
        query = "SELECT * FROM activities"
        clauses: list[str] = []
        params: list[float] = []
        if start is not None:
            clauses.append("end_ts > ?")
            params.append(start)
        if end is not None:
            clauses.append("start_ts < ?")
            params.append(end)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY start_ts ASC"
        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_activity(row) for row in rows]

    # ----- focus sessions ---------------------------------------------
    def add_focus_session(self, session: FocusSession) -> int:
        """Insert a focus session and return its new id."""
        cur = self._conn.execute(
            """
            INSERT INTO focus_sessions
                (label, kind, start_ts, end_ts, planned_seconds, completed, blocklist)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.label,
                session.kind,
                session.start_ts,
                session.end_ts,
                session.planned_seconds,
                int(session.completed),
                ",".join(session.blocklist),
            ),
        )
        self._conn.commit()
        session.id = int(cur.lastrowid)
        return session.id

    def update_focus_session(self, session: FocusSession) -> None:
        """Persist changes to an existing focus session."""
        if session.id is None:
            raise ValueError("cannot update a focus session without an id")
        self._conn.execute(
            """
            UPDATE focus_sessions
               SET label = ?, kind = ?, start_ts = ?, end_ts = ?,
                   planned_seconds = ?, completed = ?, blocklist = ?
             WHERE id = ?
            """,
            (
                session.label,
                session.kind,
                session.start_ts,
                session.end_ts,
                session.planned_seconds,
                int(session.completed),
                ",".join(session.blocklist),
                session.id,
            ),
        )
        self._conn.commit()

    def get_focus_sessions(
        self, start: float | None = None, end: float | None = None
    ) -> list[FocusSession]:
        """Return focus sessions, optionally filtered by time window."""
        query = "SELECT * FROM focus_sessions"
        clauses: list[str] = []
        params: list[float] = []
        if start is not None:
            clauses.append("(end_ts IS NULL OR end_ts > ?)")
            params.append(start)
        if end is not None:
            clauses.append("start_ts < ?")
            params.append(end)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY start_ts ASC"
        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_focus(row) for row in rows]

    def active_focus_session(self) -> FocusSession | None:
        """Return the currently running focus session, if any."""
        row = self._conn.execute(
            "SELECT * FROM focus_sessions WHERE end_ts IS NULL "
            "ORDER BY start_ts DESC LIMIT 1"
        ).fetchone()
        return self._row_to_focus(row) if row else None

    # ----- helpers ----------------------------------------------------
    @staticmethod
    def _row_to_activity(row: sqlite3.Row) -> Activity:
        return Activity(
            id=row["id"],
            app=row["app"],
            title=row["title"],
            category=Category.from_value(row["category"]),
            project=row["project"],
            start_ts=row["start_ts"],
            end_ts=row["end_ts"],
            focus_session_id=row["focus_session_id"],
        )

    @staticmethod
    def _row_to_focus(row: sqlite3.Row) -> FocusSession:
        blocklist_raw: str = row["blocklist"] or ""
        blocklist = [item for item in blocklist_raw.split(",") if item]
        return FocusSession(
            id=row["id"],
            label=row["label"],
            kind=row["kind"],
            start_ts=row["start_ts"],
            end_ts=row["end_ts"],
            planned_seconds=row["planned_seconds"],
            completed=bool(row["completed"]),
            blocklist=blocklist,
        )

    def add_activities(self, activities: Iterable[Activity]) -> None:
        """Bulk-insert activities (used by importers and tests)."""
        for activity in activities:
            self.add_activity(activity)
