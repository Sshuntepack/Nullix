"""Data conversion utilities."""

from __future__ import annotations

import json
from typing import Any


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return c * 9.0 / 5.0 + 32.0


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32.0) * 5.0 / 9.0


def kg_to_lbs(kg: float) -> float:
    """Convert kilograms to pounds."""
    if kg < 0:
        raise ValueError("weight cannot be negative")
    return kg * 2.20462


def lbs_to_kg(lbs: float) -> float:
    """Convert pounds to kilograms."""
    if lbs < 0:
        raise ValueError("weight cannot be negative")
    return lbs / 2.20462


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    if km < 0:
        raise ValueError("distance cannot be negative")
    return km * 0.621371


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers."""
    if miles < 0:
        raise ValueError("distance cannot be negative")
    return miles / 0.621371


def int_to_roman(num: int) -> str:
    """Convert a positive integer (1-3999) to a Roman numeral string."""
    if not 1 <= num <= 3999:
        raise ValueError("number must be between 1 and 3999")
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = ""
    for v, s in zip(val, syms):
        while num >= v:
            result += s
            num -= v
    return result


def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    if not s:
        raise ValueError("empty string is not a valid Roman numeral")
    roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    for i, ch in enumerate(s.upper()):
        if ch not in roman_map:
            raise ValueError(f"invalid Roman numeral character: {ch}")
        value = roman_map[ch]
        if i + 1 < len(s) and roman_map.get(s[i + 1].upper(), 0) > value:
            result -= value
        else:
            result += value
    return result


def flatten_dict(
    d: dict[str, Any], parent_key: str = "", sep: str = "."
) -> dict[str, Any]:
    """Flatten a nested dictionary into a single-level dict with dotted keys."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def safe_json_loads(text: str, default: Any = None) -> Any:
    """Parse a JSON string, returning *default* on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default
