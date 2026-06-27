import json

from productivity import config


def test_default_rules_nonempty():
    assert config.DEFAULT_RULES
    assert any(cat == "distracting" for _, cat, _ in config.DEFAULT_RULES)


def test_load_rules_missing_returns_default(tmp_path):
    rules = config.load_rules(tmp_path / "nope.json")
    assert rules == config.DEFAULT_RULES


def test_load_rules_malformed_returns_default(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text("{not valid json")
    assert config.load_rules(path) == config.DEFAULT_RULES


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "rules.json"
    rules = [("code", "productive", "Eng"), ("youtube", "distracting", "Media")]
    config.save_rules(rules, path)
    loaded = config.load_rules(path)
    assert loaded == rules


def test_load_rules_skips_entries_without_match(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text(
        json.dumps(
            [
                {"category": "productive"},  # no match -> skipped
                {"match": "code", "category": "productive", "project": "Eng"},
            ]
        )
    )
    loaded = config.load_rules(path)
    assert loaded == [("code", "productive", "Eng")]


def test_load_rules_empty_list_falls_back(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text("[]")
    assert config.load_rules(path) == config.DEFAULT_RULES


def test_path_helpers_under_home(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))
    assert str(config.config_dir()).startswith(str(tmp_path / "cfg"))
    assert str(config.data_dir()).startswith(str(tmp_path / "data"))
    assert config.default_db_path().name == "activity.db"
    assert config.rules_path().name == "rules.json"
