import pytest

from productivity import cli


def test_seed_and_report(tmp_path, capsys):
    db = str(tmp_path / "cli.db")
    assert cli.main(["--db", db, "seed", "--days", "2"]) == 0
    out = capsys.readouterr().out
    assert "Seeded" in out

    assert cli.main(["--db", db, "report", "--range", "week"]) == 0
    out = capsys.readouterr().out
    assert "Productivity report" in out
    assert "Top applications" in out


def test_report_empty_db(tmp_path, capsys):
    db = str(tmp_path / "empty.db")
    assert cli.main(["--db", db, "report"]) == 0
    out = capsys.readouterr().out
    assert "Total tracked" in out


def test_requires_subcommand():
    with pytest.raises(SystemExit):
        cli.main([])


def test_serve_no_track(tmp_path, monkeypatch):
    db = str(tmp_path / "serve.db")
    calls = {}

    def fake_run(self, host, port, **kwargs):
        calls["host"] = host
        calls["port"] = port

    monkeypatch.setattr("flask.Flask.run", fake_run)
    rc = cli.main(["--db", db, "serve", "--no-track", "--port", "9999"])
    assert rc == 0
    assert calls["port"] == 9999


def test_serve_with_tracking(tmp_path, monkeypatch):
    db = str(tmp_path / "serve2.db")
    started = {"v": False}
    monkeypatch.setattr("flask.Flask.run", lambda self, **kw: None)
    monkeypatch.setattr(
        "productivity.service.ProductivityService.start",
        lambda self: started.__setitem__("v", True),
    )
    rc = cli.main(["--db", db, "serve", "--port", "9998"])
    assert rc == 0
    assert started["v"] is True


def test_track_keyboard_interrupt(tmp_path, monkeypatch):
    db = str(tmp_path / "track.db")

    def fake_sleep(_seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(cli.time, "sleep", fake_sleep)
    # Avoid spawning real X11 polling threads.
    monkeypatch.setattr(
        "productivity.service.ProductivityService.start", lambda self: None
    )
    rc = cli.main(["--db", db, "track", "--interval", "0.01", "--no-block"])
    assert rc == 0


def test_bounds_helper():
    today = cli._bounds("today")
    week = cli._bounds("week")
    month = cli._bounds("month")
    assert today[1] - today[0] == pytest.approx(86400)
    assert week[1] - week[0] == pytest.approx(7 * 86400)
    assert month[1] - month[0] == pytest.approx(30 * 86400)
