"""Flask application factory exposing the dashboard and JSON API."""

from __future__ import annotations

from datetime import datetime

from flask import Flask, jsonify, render_template, request

from productivity import analytics
from productivity.focus import FocusManager
from productivity.storage import Storage
from productivity.timeutil import day_bounds, range_bounds


def create_app(
    storage: Storage,
    focus_manager: FocusManager | None = None,
) -> Flask:
    """Create the Flask app bound to a storage instance and focus manager."""
    app = Flask(__name__)
    focus = focus_manager or FocusManager(storage)

    def _window_from_request() -> tuple[float, float, str]:
        rng = request.args.get("range", "today")
        if rng == "today":
            start, end = day_bounds()
        elif rng == "week":
            start, end = range_bounds(7)
        elif rng == "month":
            start, end = range_bounds(30)
        else:
            start, end = day_bounds()
            rng = "today"
        return start, end, rng

    @app.get("/")
    def index() -> str:
        return render_template("dashboard.html")

    @app.get("/api/dashboard")
    def dashboard():
        start, end, rng = _window_from_request()
        activities = storage.get_activities(start, end)
        payload = analytics.build_dashboard(activities)
        payload["range"] = rng
        payload["focus"] = focus.status()
        payload["generated_at"] = datetime.now().isoformat(timespec="seconds")
        return jsonify(payload)

    @app.get("/api/focus")
    def focus_status():
        return jsonify(focus.status())

    @app.post("/api/focus/start")
    def focus_start():
        data = request.get_json(silent=True) or {}
        kind = data.get("kind", "focus")
        minutes = data.get("minutes")
        minutes = int(minutes) if minutes is not None else None
        if kind == "break":
            session = focus.start_break(
                label=data.get("label", "Break"), minutes=minutes
            )
        else:
            session = focus.start_focus(
                label=data.get("label", "Focus"),
                minutes=minutes,
                blocklist=data.get("blocklist"),
            )
        return jsonify({"started": True, "id": session.id, "kind": session.kind})

    @app.post("/api/focus/stop")
    def focus_stop():
        session = focus.stop(completed=False)
        return jsonify({"stopped": session is not None})

    return app
