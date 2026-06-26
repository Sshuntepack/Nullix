"""Tests for nullix.validators — comprehensive coverage."""

import pytest

from nullix.validators import (
    is_numeric_string,
    is_strong_password,
    is_valid_email,
    is_valid_hex_color,
    is_valid_ipv4,
    is_valid_ipv6,
    is_valid_url,
)


class TestIsValidEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "first.last@domain.co",
            "name+tag@sub.domain.org",
        ],
    )
    def test_valid(self, email):
        assert is_valid_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "",
            "plainaddress",
            "@missing-user.com",
            "user@.com",
            "user@com",
        ],
    )
    def test_invalid(self, email):
        assert is_valid_email(email) is False


class TestIsValidUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "http://example.com",
            "https://sub.domain.co.uk/path?q=1",
            "https://example.com:8080/path",
        ],
    )
    def test_valid(self, url):
        assert is_valid_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "",
            "ftp://example.com",
            "example.com",
            "http://",
        ],
    )
    def test_invalid(self, url):
        assert is_valid_url(url) is False


class TestIsValidIpv4:
    @pytest.mark.parametrize("addr", ["192.168.1.1", "0.0.0.0", "255.255.255.255"])
    def test_valid(self, addr):
        assert is_valid_ipv4(addr) is True

    @pytest.mark.parametrize("addr", ["256.0.0.1", "abc", "192.168.1", ""])
    def test_invalid(self, addr):
        assert is_valid_ipv4(addr) is False


class TestIsValidIpv6:
    @pytest.mark.parametrize("addr", ["::1", "fe80::1", "2001:db8::1"])
    def test_valid(self, addr):
        assert is_valid_ipv6(addr) is True

    @pytest.mark.parametrize("addr", ["", "not-an-ip", "192.168.1.1", "gggg::1"])
    def test_invalid(self, addr):
        assert is_valid_ipv6(addr) is False


class TestIsStrongPassword:
    def test_strong(self):
        assert is_strong_password("Str0ng!Pass") is True

    def test_too_short(self):
        assert is_strong_password("Aa1!") is False

    def test_no_uppercase(self):
        assert is_strong_password("weak1pass!") is False

    def test_no_lowercase(self):
        assert is_strong_password("WEAK1PASS!") is False

    def test_no_digit(self):
        assert is_strong_password("WeakPass!") is False

    def test_no_special(self):
        assert is_strong_password("WeakPass1") is False

    def test_custom_min_length(self):
        assert is_strong_password("Ab1!", min_length=4) is True
        assert is_strong_password("Ab1!", min_length=5) is False


class TestIsValidHexColor:
    @pytest.mark.parametrize("color", ["#fff", "#FFF", "#aabbcc", "#123456"])
    def test_valid(self, color):
        assert is_valid_hex_color(color) is True

    @pytest.mark.parametrize("color", ["", "fff", "#gg0000", "#12345", "#1234567"])
    def test_invalid(self, color):
        assert is_valid_hex_color(color) is False


class TestIsNumericString:
    @pytest.mark.parametrize("value", ["42", "-3.14", "0", "1e10", ".5"])
    def test_numeric(self, value):
        assert is_numeric_string(value) is True

    @pytest.mark.parametrize("value", ["", "abc", "12.34.56"])
    def test_non_numeric(self, value):
        assert is_numeric_string(value) is False
