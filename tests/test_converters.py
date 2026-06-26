"""Tests for nullix.converters — comprehensive coverage."""

import pytest

from nullix.converters import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    flatten_dict,
    int_to_roman,
    kg_to_lbs,
    km_to_miles,
    lbs_to_kg,
    miles_to_km,
    roman_to_int,
    safe_json_loads,
)


class TestTemperature:
    def test_c_to_f_freezing(self):
        assert celsius_to_fahrenheit(0) == 32.0

    def test_c_to_f_boiling(self):
        assert celsius_to_fahrenheit(100) == 212.0

    def test_f_to_c_freezing(self):
        assert fahrenheit_to_celsius(32) == 0.0

    def test_f_to_c_boiling(self):
        assert fahrenheit_to_celsius(212) == pytest.approx(100.0)

    def test_roundtrip(self):
        assert fahrenheit_to_celsius(celsius_to_fahrenheit(37)) == pytest.approx(37.0)


class TestWeight:
    def test_kg_to_lbs(self):
        assert kg_to_lbs(1) == pytest.approx(2.20462)

    def test_kg_to_lbs_zero(self):
        assert kg_to_lbs(0) == 0.0

    def test_kg_to_lbs_negative(self):
        with pytest.raises(ValueError, match="negative"):
            kg_to_lbs(-1)

    def test_lbs_to_kg(self):
        assert lbs_to_kg(2.20462) == pytest.approx(1.0)

    def test_lbs_to_kg_zero(self):
        assert lbs_to_kg(0) == 0.0

    def test_lbs_to_kg_negative(self):
        with pytest.raises(ValueError, match="negative"):
            lbs_to_kg(-1)


class TestDistance:
    def test_km_to_miles(self):
        assert km_to_miles(1) == pytest.approx(0.621371)

    def test_km_to_miles_zero(self):
        assert km_to_miles(0) == 0.0

    def test_km_to_miles_negative(self):
        with pytest.raises(ValueError, match="negative"):
            km_to_miles(-1)

    def test_miles_to_km(self):
        assert miles_to_km(1) == pytest.approx(1.60934, rel=1e-3)

    def test_miles_to_km_zero(self):
        assert miles_to_km(0) == 0.0

    def test_miles_to_km_negative(self):
        with pytest.raises(ValueError, match="negative"):
            miles_to_km(-1)


class TestRomanNumerals:
    @pytest.mark.parametrize(
        "num, expected",
        [
            (1, "I"),
            (4, "IV"),
            (9, "IX"),
            (14, "XIV"),
            (40, "XL"),
            (90, "XC"),
            (399, "CCCXCIX"),
            (400, "CD"),
            (900, "CM"),
            (1994, "MCMXCIV"),
            (3999, "MMMCMXCIX"),
        ],
    )
    def test_int_to_roman(self, num, expected):
        assert int_to_roman(num) == expected

    def test_int_to_roman_out_of_range_low(self):
        with pytest.raises(ValueError):
            int_to_roman(0)

    def test_int_to_roman_out_of_range_high(self):
        with pytest.raises(ValueError):
            int_to_roman(4000)

    @pytest.mark.parametrize(
        "s, expected",
        [
            ("I", 1),
            ("IV", 4),
            ("IX", 9),
            ("XIV", 14),
            ("XL", 40),
            ("MCMXCIV", 1994),
        ],
    )
    def test_roman_to_int(self, s, expected):
        assert roman_to_int(s) == expected

    def test_roman_to_int_empty(self):
        with pytest.raises(ValueError, match="empty"):
            roman_to_int("")

    def test_roman_to_int_invalid_char(self):
        with pytest.raises(ValueError, match="invalid"):
            roman_to_int("ABC")

    def test_roundtrip(self):
        for n in [1, 42, 100, 999, 3999]:
            assert roman_to_int(int_to_roman(n)) == n


class TestFlattenDict:
    def test_flat_dict(self):
        assert flatten_dict({"a": 1, "b": 2}) == {"a": 1, "b": 2}

    def test_nested(self):
        assert flatten_dict({"a": {"b": {"c": 1}}}) == {"a.b.c": 1}

    def test_mixed(self):
        result = flatten_dict({"x": 1, "y": {"z": 2}})
        assert result == {"x": 1, "y.z": 2}

    def test_custom_separator(self):
        assert flatten_dict({"a": {"b": 1}}, sep="/") == {"a/b": 1}

    def test_empty(self):
        assert flatten_dict({}) == {}


class TestSafeJsonLoads:
    def test_valid_json(self):
        assert safe_json_loads('{"a": 1}') == {"a": 1}

    def test_invalid_json(self):
        assert safe_json_loads("not json") is None

    def test_custom_default(self):
        assert safe_json_loads("bad", default={}) == {}

    def test_none_input(self):
        assert safe_json_loads(None) is None
