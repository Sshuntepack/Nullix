"""Tests for nullix.math_utils — good coverage."""

import pytest

from nullix.math_utils import (
    clamp,
    factorial,
    fibonacci,
    gcd,
    is_prime,
    lcm,
    mean,
    median,
)


class TestClamp:
    def test_within_bounds(self):
        assert clamp(5, 0, 10) == 5

    def test_below_lower(self):
        assert clamp(-3, 0, 10) == 0

    def test_above_upper(self):
        assert clamp(15, 0, 10) == 10

    def test_invalid_bounds(self):
        with pytest.raises(ValueError):
            clamp(5, 10, 0)


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3]) == 2.0

    def test_single(self):
        assert mean([7]) == 7.0

    def test_empty(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([3, 1, 2]) == 2

    def test_even_count(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_empty(self):
        with pytest.raises(ValueError):
            median([])


class TestGcd:
    def test_basic(self):
        assert gcd(12, 8) == 4

    def test_coprime(self):
        assert gcd(7, 13) == 1

    def test_zero(self):
        assert gcd(0, 5) == 5


class TestLcm:
    def test_basic(self):
        assert lcm(4, 6) == 12

    def test_zero(self):
        assert lcm(0, 5) == 0


class TestIsPrime:
    def test_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 29]:
            assert is_prime(p) is True

    def test_non_primes(self):
        for n in [0, 1, 4, 9, 15, 25]:
            assert is_prime(n) is False


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_basic(self):
        assert factorial(5) == 120

    def test_negative(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestFibonacci:
    def test_base_cases(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_larger(self):
        assert fibonacci(10) == 55

    def test_negative(self):
        with pytest.raises(ValueError):
            fibonacci(-1)
