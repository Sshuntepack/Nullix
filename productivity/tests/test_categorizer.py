from productivity.categorizer import Categorizer
from productivity.models import Category, WindowSample


def test_default_rules_productive():
    c = Categorizer()
    category, project = c.classify("Code", "tracker.py - Visual Studio Code")
    assert category is Category.PRODUCTIVE
    assert project == "Engineering"


def test_default_rules_distracting():
    c = Categorizer()
    category, project = c.classify("Chrome", "YouTube - Lo-fi")
    assert category is Category.DISTRACTING
    assert project == "Media"


def test_unmatched_is_neutral():
    c = Categorizer()
    category, project = c.classify("SomeRandomApp", "nothing here")
    assert category is Category.NEUTRAL
    assert project is None


def test_first_match_wins():
    rules = [
        ("chrome", "neutral", None),
        ("youtube", "distracting", "Media"),
    ]
    c = Categorizer(rules)
    # "chrome" appears first in the rule list, so it wins over youtube.
    category, _ = c.classify("Chrome", "YouTube")
    assert category is Category.NEUTRAL


def test_classify_sample():
    c = Categorizer()
    sample = WindowSample(app="reddit", title="r/python", timestamp=1.0)
    category, project = c.classify_sample(sample)
    assert category is Category.DISTRACTING
    assert project == "Social"


def test_rules_property_compiled():
    c = Categorizer([("Code", "productive", "Eng")])
    rules = c.rules
    assert rules[0][0] == "code"
    assert rules[0][1] is Category.PRODUCTIVE
