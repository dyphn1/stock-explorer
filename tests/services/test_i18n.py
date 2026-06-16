"""Tests for i18n formatting utilities (format_amount, format_percent)."""
from __future__ import annotations

import pytest
from unittest.mock import patch

from src.core.i18n import format_amount, format_percent


# ── format_amount tests ───────────────────────────────────────────────────


class TestFormatAmount:
    def test_billions_zh_tw(self):
        """Values >= 1e8 should display as 億."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(1_500_000_000)
            assert result == "15.0 億"

    def test_ten_thousands_zh_tw(self):
        """Values >= 1e4 and < 1e8 should display as 萬."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(5_000_000)
            assert result == "500 萬"

    def test_yuan_zh_tw(self):
        """Values < 1e4 should display as 元."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(1234)
            assert result == "1,234 元"

    def test_negative_value(self):
        """Negative values should preserve the sign."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(-1_500_000_000)
            assert result == "-15.0 億"

    def test_zero(self):
        """Zero should display as 0 元."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(0)
            assert result == "0 元"

    def test_exactly_1e8(self):
        """Boundary: exactly 1e8 should display as 1.0 億."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(100_000_000)
            assert result == "1.0 億"

    def test_just_below_1e8(self):
        """Boundary: 99,999,999 should display as 萬."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(99_999_999)
            assert result == "10,000 萬"

    def test_small_value(self):
        """Small values (< 1e4) should display as 元."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
        }.get(key, key)):
            result = format_amount(500)
            assert result == "500 元"

    def test_custom_unit_key(self):
        """Custom unit_key should be used for small values."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "億",
            "unit.ten_thousand": "萬",
            "unit.yuan": "元",
            "unit.percent": "%",
        }.get(key, key)):
            result = format_amount(12.5, "unit.percent")
            assert result == "12 %"

    def test_billions_english(self):
        """English locale should use B suffix."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "B",
            "unit.ten_thousand": "M",
            "unit.yuan": "TWD",
        }.get(key, key)):
            result = format_amount(2_000_000_000)
            assert result == "20.0 B"

    def test_millions_english(self):
        """English locale should use M suffix."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.hundred_million": "B",
            "unit.ten_thousand": "M",
            "unit.yuan": "TWD",
        }.get(key, key)):
            result = format_amount(5_000_000)
            assert result == "500 M"


# ── format_percent tests ──────────────────────────────────────────────────


class TestFormatPercent:
    def test_basic_percentage(self):
        """Basic percentage formatting."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.percent": "%",
        }.get(key, key)):
            result = format_percent(25.5)
            assert result == "25.50%"

    def test_zero_percentage(self):
        """Zero should format as 0.00%."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.percent": "%",
        }.get(key, key)):
            result = format_percent(0)
            assert result == "0.00%"

    def test_negative_percentage(self):
        """Negative values should preserve the sign."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.percent": "%",
        }.get(key, key)):
            result = format_percent(-3.14)
            assert result == "-3.14%"

    def test_custom_decimals(self):
        """Custom decimal places should be respected."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.percent": "%",
        }.get(key, key)):
            result = format_percent(25.5, decimals=1)
            assert result == "25.5%"

    def test_whole_number_with_decimals(self):
        """Whole numbers should still show decimal places."""
        with patch("src.core.i18n.t", side_effect=lambda key, **kw: {
            "unit.percent": "%",
        }.get(key, key)):
            result = format_percent(100, decimals=3)
            assert result == "100.000%"
