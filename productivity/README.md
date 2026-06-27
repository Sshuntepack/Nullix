# Automated Desktop Productivity Manager

A self-contained desktop productivity tool that **tracks how you spend time on
your computer**, **categorizes** it (productive / distracting / neutral), runs
**focus sessions** with optional **app blocking**, and serves a polished
**analytics dashboard**.

It is pure Python (standard library + Flask) with no external services. Window
tracking works on Linux/X11 via `xdotool`/`xprop`; the architecture abstracts
the window source behind a small protocol so other backends (or tests) can be
plugged in.

## Features

- **Activity tracking** — a background loop samples the foreground window and
  collapses contiguous samples into activities. Idle time (via `xprintidle`)
  is detected and never counted.
- **Rule-based categorization** — configurable, ordered substring rules map
  apps/titles to `productive` / `distracting` / `neutral` and a project tag.
  Rules live in `~/.config/productivity/rules.json` (defaults are built in).
- **Focus & Pomodoro** — start a focus session (default 25 min) that auto-rolls
  into a break (5 min). A productivity score is computed from engaged time.
- **App blocking** — during a focus session, windows matching the blocklist are
  minimized on sight.
- **Analytics dashboard** — a Flask + Chart.js dashboard with a productivity
  score ring, category breakdown, top apps, per-hour activity, projects, and a
  live focus timer with start/stop controls. Auto-refreshes every 5s.
- **CLI** — `track`, `serve`, `report`, and `seed`.

## Architecture

```
window_provider  ->  tracker  ->  storage (SQLite)
                        |             ^
   categorizer  --------+             |
                        v             |
   focus + blocker  <---+----  analytics  ->  web dashboard / CLI report
```

Each layer is independently testable: the tracker depends only on a
`WindowProvider` protocol, the focus manager takes an injectable clock, and the
blocker takes a `WindowController`. See `tests/` for examples.

## Install

```bash
cd productivity
pip install -e .
# system deps for live tracking on Linux/X11:
#   sudo apt-get install xdotool x11-utils xprintidle
```

## Usage

```bash
# Populate demo data and explore the dashboard immediately:
productivity --db /tmp/demo.db seed --days 3
productivity --db /tmp/demo.db serve        # http://127.0.0.1:8765

# Real tracking (records what you actually do):
productivity track                          # background sampler + blocking
productivity serve                          # dashboard + tracker together

# Text report:
productivity report --range week
```

### Configuration

| Setting          | Default                                | Notes                          |
| ---------------- | -------------------------------------- | ------------------------------ |
| Database         | `~/.local/share/productivity/activity.db` | `--db` to override          |
| Rules            | `~/.config/productivity/rules.json`    | falls back to built-in rules   |
| Poll interval    | 2.0s                                   | `track --interval`             |
| Idle threshold   | 120s                                   | requires `xprintidle`          |

## Development

```bash
pip install pytest pytest-cov ruff flask
pytest --cov=productivity        # 109 tests, ~99% line coverage
ruff check . && ruff format --check .
```
