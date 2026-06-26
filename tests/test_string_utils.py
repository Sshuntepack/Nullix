"""Tests for nullix.string_utils — comprehensive coverage."""

import pytest

from nullix.string_utils import (
    camel_to_snake,
    count_words,
    is_palindrome,
    mask_string,
    reverse_words,
    slugify,
    snake_to_camel,
    truncate,
)


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("Foo & Bar!") == "foo-bar"

    def test_custom_separator(self):
        assert slugify("Hello World", separator="_") == "hello_world"


class TestTruncate:
    def test_no_truncation(self):
        assert truncate("hi", 10) == "hi"

    def test_truncation(self):
        assert truncate("Hello, World!", 8) == "Hello..."

    def test_negative_length(self):
        with pytest.raises(ValueError):
            truncate("hi", -1)

    def test_length_shorter_than_suffix(self):
        assert truncate("Hello, World!", 2) == "He"


class TestCamelToSnake:
    def test_camel(self):
        assert camel_to_snake("camelCase") == "camel_case"

    def test_pascal(self):
        assert camel_to_snake("PascalCase") == "pascal_case"

    def test_multiple_caps(self):
        assert camel_to_snake("getHTTPResponse") == "get_http_response"

    def test_already_snake(self):
        assert camel_to_snake("already_snake") == "already_snake"


class TestSnakeToCamel:
    def test_basic(self):
        assert snake_to_camel("hello_world") == "helloWorld"

    def test_pascal(self):
        assert snake_to_camel("hello_world", pascal=True) == "HelloWorld"

    def test_single_word(self):
        assert snake_to_camel("hello") == "hello"


class TestIsPalindrome:
    def test_simple(self):
        assert is_palindrome("racecar") is True

    def test_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_case_sensitive(self):
        assert is_palindrome("Racecar", ignore_case=False) is False


class TestCountWords:
    def test_basic(self):
        assert count_words("hello world") == 2

    def test_empty(self):
        assert count_words("") == 0

    def test_extra_spaces(self):
        assert count_words("  one  two  three  ") == 3


class TestReverseWords:
    def test_basic(self):
        assert reverse_words("hello world") == "world hello"

    def test_single(self):
        assert reverse_words("hello") == "hello"


class TestMaskString:
    def test_basic(self):
        assert mask_string("1234567890") == "******7890"

    def test_short_string(self):
        assert mask_string("hi", visible=4) == "hi"

    def test_custom_char(self):
        assert mask_string("secret", visible=2, mask_char="#") == "####et"

    def test_negative_visible(self):
        with pytest.raises(ValueError):
            mask_string("test", visible=-1)
