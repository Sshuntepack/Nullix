from productivity.models import WindowSample
from productivity.window_provider import (
    FakeWindowProvider,
    X11WindowProvider,
    default_provider,
)


def test_fake_provider_replays_then_repeats_last():
    provider = FakeWindowProvider(
        [
            WindowSample(app="Code", title="a", timestamp=0.0),
            WindowSample(app="Chrome", title="b", timestamp=1.0),
        ]
    )
    assert provider.sample().app == "Code"
    assert provider.sample().app == "Chrome"
    # Exhausted -> keeps returning the last sample.
    assert provider.sample().app == "Chrome"


def test_fake_provider_empty_returns_none():
    assert FakeWindowProvider([]).sample() is None


def test_default_provider_is_x11():
    assert isinstance(default_provider(), X11WindowProvider)


def test_x11_provider_no_xdotool(monkeypatch):
    provider = X11WindowProvider()
    provider._xdotool = None
    assert provider.sample() is None


def test_x11_provider_parses_sample(monkeypatch):
    provider = X11WindowProvider(idle_threshold=120.0)
    provider._xdotool = "xdotool"
    provider._xprop = "xprop"
    provider._xprintidle = "xprintidle"

    def fake_run(args):
        if args[:2] == ["xdotool", "getactivewindow"]:
            return "12345"
        if args[:2] == ["xdotool", "getwindowname"]:
            return "tracker.py - Visual Studio Code"
        if args[0] == "xprop":
            return 'WM_CLASS(STRING) = "code", "Code"'
        if args[0] == "xprintidle":
            return "1000"
        return None

    monkeypatch.setattr(provider, "_run", fake_run)
    sample = provider.sample()
    assert sample is not None
    assert sample.app == "Code"
    assert "Visual Studio Code" in sample.title
    assert sample.idle is False


def test_x11_provider_idle_detection(monkeypatch):
    provider = X11WindowProvider(idle_threshold=10.0)
    provider._xdotool = "xdotool"
    provider._xprop = "xprop"
    provider._xprintidle = "xprintidle"

    def fake_run(args):
        if args[:2] == ["xdotool", "getactivewindow"]:
            return "1"
        if args[:2] == ["xdotool", "getwindowname"]:
            return "idle window"
        if args[0] == "xprop":
            return 'WM_CLASS(STRING) = "x", "X"'
        if args[0] == "xprintidle":
            return "60000"  # 60s idle > 10s threshold
        return None

    monkeypatch.setattr(provider, "_run", fake_run)
    sample = provider.sample()
    assert sample is not None
    assert sample.idle is True


def test_x11_provider_no_active_window(monkeypatch):
    provider = X11WindowProvider()
    provider._xdotool = "xdotool"
    monkeypatch.setattr(provider, "_run", lambda args: None)
    assert provider.sample() is None
