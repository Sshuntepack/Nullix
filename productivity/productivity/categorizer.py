"""Rule-based categorization of window activity."""

from __future__ import annotations

from productivity.config import DEFAULT_RULES
from productivity.models import Category, WindowSample


class Categorizer:
    """Classifies window samples into categories using ordered rules.

    Each rule is ``(match, category, project)``. The ``match`` substring is
    tested (case-insensitively) against the combined ``"<app> <title>"``
    string. The first matching rule wins. Samples that match no rule are
    classified as :attr:`Category.NEUTRAL`.
    """

    def __init__(self, rules: list[tuple[str, str, str | None]] | None = None) -> None:
        source = rules if rules is not None else DEFAULT_RULES
        self._rules: list[tuple[str, Category, str | None]] = [
            (match.lower(), Category.from_value(category), project)
            for match, category, project in source
        ]

    @property
    def rules(self) -> list[tuple[str, Category, str | None]]:
        """The compiled rules in evaluation order."""
        return list(self._rules)

    def classify(self, app: str, title: str = "") -> tuple[Category, str | None]:
        """Return the ``(category, project)`` for an app/title pair."""
        haystack = f"{app} {title}".lower()
        for match, category, project in self._rules:
            if match and match in haystack:
                return category, project
        return Category.NEUTRAL, None

    def classify_sample(self, sample: WindowSample) -> tuple[Category, str | None]:
        """Classify a :class:`WindowSample`."""
        return self.classify(sample.app, sample.title)
