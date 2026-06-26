"""Input validation helpers."""

from __future__ import annotations

import re
from ipaddress import AddressValueError, IPv4Address, IPv6Address


def is_valid_email(email: str) -> bool:
    """Check whether a string looks like a valid email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Check whether a string looks like a valid HTTP(S) URL."""
    pattern = (
        r"^https?://"
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"[a-zA-Z]{2,}"
        r"(?::\d{1,5})?"
        r"(?:/[^\s]*)?$"
    )
    return bool(re.match(pattern, url))


def is_valid_ipv4(address: str) -> bool:
    """Check whether a string is a valid IPv4 address."""
    try:
        IPv4Address(address)
        return True
    except (AddressValueError, ValueError):
        return False


def is_valid_ipv6(address: str) -> bool:
    """Check whether a string is a valid IPv6 address."""
    try:
        IPv6Address(address)
        return True
    except (AddressValueError, ValueError):
        return False


def is_strong_password(password: str, min_length: int = 8) -> bool:
    """Check whether a password meets strength requirements.

    Requirements: at least *min_length* characters, one uppercase letter,
    one lowercase letter, one digit, and one special character.
    """
    if len(password) < min_length:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def is_valid_hex_color(color: str) -> bool:
    """Check whether a string is a valid hex color code (#RGB or #RRGGBB)."""
    return bool(re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color))


def is_numeric_string(value: str) -> bool:
    """Check whether a string represents a numeric value (int or float)."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
