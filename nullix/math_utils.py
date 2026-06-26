"""Mathematical utility functions."""

from __future__ import annotations

import math
from typing import Sequence


def clamp(value: float, lower: float, upper: float) -> float:
    """Clamp a value between lower and upper bounds."""
    if lower > upper:
        raise ValueError("lower bound must be <= upper bound")
    return max(lower, min(value, upper))


def mean(values: Sequence[float]) -> float:
    """Return the arithmetic mean of a sequence of numbers."""
    if not values:
        raise ValueError("cannot compute mean of empty sequence")
    return sum(values) / len(values)


def median(values: Sequence[float]) -> float:
    """Return the median of a sequence of numbers."""
    if not values:
        raise ValueError("cannot compute median of empty sequence")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of two integers."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of two integers."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def is_prime(n: int) -> bool:
    """Check whether a positive integer is prime."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def factorial(n: int) -> int:
    """Return n! for a non-negative integer n."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    return math.factorial(n)


def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
