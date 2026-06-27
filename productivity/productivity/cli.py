"""Command-line interface for the productivity manager."""

from __future__ import annotations

import argparse
import time

from productivity import analytics
from productivity.config import Settings, default_db_path
from productivity.service import ProductivityService
from productivity.storage import Storage
from productivity.timeutil import day_bounds, format_duration, range_bounds


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="productivity",
        description="Automated Desktop Productivity Manager",
    )
    parser.add_argument(
        "--db",
        default=str(default_db_path()),
        help="Path to the SQLite database",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    track = sub.add_parser("track", help="Run the background tracker")
    track.add_argument("--interval", type=float, default=2.0)
    track.add_argument(
        "--no-block",
        action="store_true",
        help="Do not enforce app blocking during focus sessions",
    )

    serve = sub.add_parser("serve", help="Run the web dashboard (and tracker)")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument(
        "--no-track",
        action="store_true",
        help="Serve the dashboard without starting the tracker",
    )

    report = sub.add_parser("report", help="Print a text productivity report")
    report.add_argument(
        "--range",
        choices=["today", "week", "month"],
        default="today",
    )

    seed = sub.add_parser("seed", help="Insert demo activity data")
    seed.add_argument("--days", type=int, default=3)

    return parser


def _bounds(rng: str) -> tuple[float, float]:
    if rng == "today":
        return day_bounds()
    if rng == "week":
        return range_bounds(7)
    return range_bounds(30)


def cmd_track(args: argparse.Namespace) -> int:
    settings = Settings(db_path=args.db, poll_interval=args.interval)
    service = ProductivityService(settings, enforce_blocking=not args.no_block)
    service.start()
    print(f"Tracking active windows every {args.interval}s. Ctrl-C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping tracker\u2026")
    finally:
        service.close()
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from productivity.web import create_app

    settings = Settings(db_path=args.db)
    service = ProductivityService(settings)
    if not args.no_track:
        service.start()
    app = create_app(service.storage, service.focus)
    print(f"Dashboard: http://{args.host}:{args.port}")
    try:
        app.run(host=args.host, port=args.port, debug=False, use_reloader=False)
    finally:
        service.close()
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    storage = Storage(args.db)
    start, end = _bounds(args.range)
    activities = storage.get_activities(start, end)
    summary = analytics.summarize(activities)
    print(f"Productivity report \u2014 {args.range}")
    print("=" * 40)
    print(f"Total tracked : {format_duration(summary.total_seconds)}")
    print(f"Score         : {round(summary.productivity_score * 100)}%")
    for cat, seconds in sorted(
        summary.by_category.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {cat:<12}: {format_duration(seconds)}")
    print("\nTop applications")
    for row in analytics.by_app(activities, top_n=10):
        print(
            f"  {row['app'][:28]:<28} {format_duration(row['seconds']):>10}"
            f"  [{row['category']}]"
        )
    storage.close()
    return 0


def cmd_seed(args: argparse.Namespace) -> int:
    from productivity.demo import seed_demo_data

    storage = Storage(args.db)
    count = seed_demo_data(storage, days=args.days)
    storage.close()
    print(f"Seeded {count} demo activities across {args.days} day(s) into {args.db}")
    print(f"Run: productivity serve --db {args.db}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "track": cmd_track,
        "serve": cmd_serve,
        "report": cmd_report,
        "seed": cmd_seed,
    }
    handler = handlers[args.command]
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
