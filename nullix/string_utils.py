"""String manipulation utilities."""

from __future__ import annotations

import re
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """Convert a string to a URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", separator, text)


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to a given length, appending a suffix if truncated."""
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(text) <= length:
        return text
    if length <= len(suffix):
        return text[:length]
    return text[: length - len(suffix)] + suffix


def camel_to_snake(name: str) -> str:
    """Convert a camelCase or PascalCase string to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str, pascal: bool = False) -> str:
    """Convert a snake_case string to camelCase (or PascalCase)."""
    components = name.split("_")
    if pascal:
        return "".join(x.title() for x in components)
    return components[0] + "".join(x.title() for x in components[1:])


def is_palindrome(text: str, ignore_case: bool = True) -> bool:
    """Check whether a string is a palindrome."""
    cleaned = re.sub(r"\W", "", text)
    if ignore_case:
        cleaned = cleaned.lower()
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    """Count the number of words in a string."""
    return len(text.split())


def reverse_words(text: str) -> str:
    """Reverse the order of words in a string."""
    return " ".join(text.split()[::-1])


def mask_string(text: str, visible: int = 4, mask_char: str = "*") -> str:
    """Mask a string, leaving only the last `visible` characters exposed."""
    if visible < 0:
        raise ValueError("visible must be non-negative")
    if len(text) <= visible:
        return text
    return mask_char * (len(text) - visible) + text[-visible:]
