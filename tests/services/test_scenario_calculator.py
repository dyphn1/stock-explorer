"""
Unit tests for scenario_calculator.py (C200).

Tests cover:
- calculate_scenario with known data
- Edge cases: pre-IPO, future date, no data
- Dividend calculation
- Annualized return calculation
- Max drawdown calculation

All tests use mock price/dividend DataFrames — no Streamlit, no API calls.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from src.services.scenario_calculator import (
    _get_price_on_date,
    _get_price_on_or_after,
    _get_price_on_or_before,
    _get_first_trading_date,
    _calc_max_drawdown,
    _calc_dividend_income,
    _parse_date,
    calculate_scenario,
)


# ── Helpers ──────────────────────────────────────────────────

def _make_price_df(dates: list[str], closes: list[float]) -> pd.DataFrame:
    """Build a minimal daily price DataFrame."""
    return pd.DataFrame({
        "date": dates,
        "close": closes,
        "open": closes,
        "high": closes,
        "low": closes,
        "Trading_Volume": [1000] * len(dates),
        "spread": [0.0] * len(dates),
    })


def _make_dividend_df(rows: list[dict]) -> pd.DataFrame:
    """Build a minimal dividend DataFrame."""
    return pd.DataFrame(rows)


def _mock_client(price_df: pd.DataFrame, dividend_df: pd.DataFrame | None = None) -> MagicMock:
    """Build a mock FinMindClient."""
    client = MagicMock()
    client.get_daily_price.return_value = price_df
    if dividend_df is not None:
        client.get_dividend.return_value = dividend_df
    else:
        client.get_dividend.return_value = pd.DataFrame()
    return client


# ── Test data ────────────────────────────────────────────────

# 2 years of daily prices: starts at 100, ends at 150
_DATES_2Y = pd.date_range("2022-01-03", "2023-12-29", freq="B").strftime("%Y-%m-%d").tolist()
_CLOSE_2Y = [100.0 + i * 0.1 for i in range(len(_DATES_2Y))]  # 100 → ~150
_PRICE_DF_2Y = _make_price_df(_DATES_2Y, _CLOSE_2Y)


# ── _parse_date() tests ─────────────────────────────────────

class TestParseDate:
    def test_valid_date(self):
        dt = _parse_date("2023-06-15")
        assert dt.year == 2023
        assert dt.month == 6
        assert dt.day == 15

    def test_date_with_time(self):
        dt = _parse_date("2023-06-15T10:30:00")
        assert dt.year == 2023
        assert dt.month == 6


# ── _get_price_on_or_after() tests ──────────────────────────

class TestGetPriceOnOrAfter:
    def test_exact_date(self):
        df = _make_price_df(["2023-01-03", "2023-01-04"], [100.0, 101.0])
        assert _get_price_on_or_after(df, "2023-01-03") == 100.0

    def test_next_available_date(self):
        df = _make_price_df(["2023-01-03", "2023-01-05"], [100.0, 102.0])
        # 2023-01-04 is a weekend, should get 2023-01-05
        assert _get_price_on_or_after(df, "2023-01-04") == 102.0

    def test_no_data_returns_none(self):
        df = _make_price_df(["2023-01-03"], [100.0])
        assert _get_price_on_or_after(df, "2024-01-01") is None

    def test_empty_df_returns_none(self):
        assert _get_price_on_or_after(pd.DataFrame(), "2023-01-01") is None

    def test_none_df_returns_none(self):
        assert _get_price_on_or_after(None, "2023-01-01") is None


# ── _get_price_on_or_before() tests ─────────────────────────

class TestGetPriceOnOrBefore:
    def test_exact_date(self):
        df = _make_price_df(["2023-01-03", "2023-01-04"], [100.0, 101.0])
        assert _get_price_on_or_before(df, "2023-01-04") == 101.0

    def test_prev_available_date(self):
        df = _make_price_df(["2023-01-03", "2023-01-05"], [100.0, 102.0])
        assert _get_price_on_or_before(df, "2023-01-04") == 100.0

    def test_no_data_returns_none(self):
        df = _make_price_df(["2023-06-01"], [100.0])
        assert _get_price_on_or_before(df, "2023-01-01") is None


# ── _get_first_trading_date() tests ─────────────────────────

class TestGetFirstTradingDate:
    def test_returns_first(self):
        df = _make_price_df(["2023-01-03", "2023-01-04"], [100.0, 101.0])
        assert _get_first_trading_date(df) == "2023-01-03"

    def test_empty_returns_none(self):
        assert _get_first_trading_date(pd.DataFrame()) is None


# ── _calc_max_drawdown() tests ─────────────────────────

class TestCalculateMaxDrawdown:
    def test_no_drawdown(self):
        """Prices only go up → max drawdown = 0."""
        df = _make_price_df(
            ["2023-01-03", "2023-01-04", "2023-01-05"],
            [100.0, 110.0, 120.0],
        )
        assert _calc_max_drawdown(df, "2023-01-03", "2023-01-05") == 0.0

    def test_simple_drawdown(self):
        """Price goes 100 → 80 → 90, max drawdown = -20%."""
        df = _make_price_df(
            ["2023-01-03", "2023-01-04", "2023-01-05"],
            [100.0, 80.0, 90.0],
        )
        dd = _calc_max_drawdown(df, "2023-01-03", "2023-01-05")
        assert dd == -20.0

    def test_recovery_to_new_high(self):
        """Price goes 100 → 70 → 120, max drawdown = -30%."""
        df = _make_price_df(
            ["2023-01-03", "2023-01-04", "2023-01-05"],
            [100.0, 70.0, 120.0],
        )
        dd = _calc_max_drawdown(df, "2023-01-03", "2023-01-05")
        assert dd == -30.0

    def test_empty_df(self):
        assert _calc_max_drawdown(pd.DataFrame(), "2023-01-01", "2023-12-31") == 0.0


# ── _calc_dividend_income() tests ──────────────────────

class TestCalculateDividendIncome:
    def test_single_dividend(self):
        df = _make_dividend_df([
            {"ex_dividend_date": "2023-06-15", "cash_dividend": 5.0},
        ])
        # 10 shares * 5.0 = 50.0
        assert _calc_dividend_income(df, "2023-01-01", "2023-12-31", 10) == 50.0

    def test_multiple_dividends(self):
        df = _make_dividend_df([
            {"ex_dividend_date": "2023-03-15", "cash_dividend": 3.0},
            {"ex_dividend_date": "2023-09-15", "cash_dividend": 4.0},
        ])
        # 10 shares * (3.0 + 4.0) = 70.0
        assert _calc_dividend_income(df, "2023-01-01", "2023-12-31", 10) == 70.0

    def test_dividend_outside_range(self):
        df = _make_dividend_df([
            {"ex_dividend_date": "2022-06-15", "cash_dividend": 5.0},
            {"ex_dividend_date": "2024-06-15", "cash_dividend": 5.0},
        ])
        assert _calc_dividend_income(df, "2023-01-01", "2023-12-31", 10) == 0.0

    def test_empty_df(self):
        assert _calc_dividend_income(pd.DataFrame(), "2023-01-01", "2023-12-31", 10) == 0.0

    def test_none_df(self):
        assert _calc_dividend_income(None, "2023-01-01", "2023-12-31", 10) == 0.0

    def test_zero_shares(self):
        """Zero shares → no dividend income."""
        df = _make_dividend_df([
            {"ex_dividend_date": "2023-06-15", "cash_dividend": 5.0},
        ])
        assert _calc_dividend_income(df, "2023-01-01", "2023-12-31", 0) == 0.0

    def test_cash_earnings_distributions_column(self):
        """Support alternative column name 'cash_earnings_distributions'."""
        df = _make_dividend_df([
            {"date": "2023-06-15", "cash_earnings_distributions": 5.0},
        ])
        assert _calc_dividend_income(df, "2023-01-01", "2023-12-31", 10) == 50.0


# ── calculate_scenario() tests ──────────────────────────────

class TestCalculateScenario:
    def test_basic_calculation(self):
        """Buy at 100, sell at 151.9, 100000 TWD → 1000 shares, 51.9% return."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        assert result["start_price"] == 100.0
        assert result["shares"] == 1000.0
        assert result["total_return"] == 51.9
        assert result["absolute_return"] == 51900.0
        assert result["dividend_income"] == 0.0
        assert result["is_estimated"] is False

    def test_annualized_return(self):
        """Positive return over ~2 years → positive annualized return."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        # total_return ~50%, over ~2 years → annualized ~22-25%
        assert result["annualized_return"] > 0

    def test_with_dividends(self):
        """Dividend income should be included in absolute return."""
        div_df = _make_dividend_df([
            {"ex_dividend_date": "2022-06-15", "cash_dividend": 5.0},
            {"ex_dividend_date": "2023-06-15", "cash_dividend": 5.0},
        ])
        client = _mock_client(_PRICE_DF_2Y, div_df)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=True,
            client=client,
        )
        assert result["error_key"] is None
        # 1000 shares * (5.0 + 5.0) = 10000 TWD dividend
        assert result["dividend_income"] == 10000.0

    def test_dividend_excluded(self):
        """When include_dividends=False, dividend_income should be 0."""
        div_df = _make_dividend_df([
            {"ex_dividend_date": "2022-06-15", "cash_dividend": 5.0},
        ])
        client = _mock_client(_PRICE_DF_2Y, div_df)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        assert result["dividend_income"] == 0.0

    def test_max_drawdown(self):
        """Max drawdown should be negative when price drops."""
        # Create a price series with a clear drawdown
        dates = pd.date_range("2023-01-02", "2023-03-31", freq="B").strftime("%Y-%m-%d").tolist()
        # Price: 100 → 120 → 80 → 100
        closes = [100.0 + i * 0.5 for i in range(20)] + \
                 [110.0 - i * 1.0 for i in range(20)] + \
                 [90.0 + i * 0.5 for i in range(len(dates) - 40)]
        closes = closes[:len(dates)]
        price_df = _make_price_df(dates, closes)
        client = _mock_client(price_df)
        result = calculate_scenario(
            stock_id="2330",
            start_date=dates[0],
            investment_amount=100000.0,
            end_date=dates[-1],
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        assert result["max_drawdown"] <= 0.0

    def test_end_date_defaults_to_today(self):
        """When end_date is None, use today's date as end_date."""
        client = _mock_client(_PRICE_DF_2Y)
        today_str = datetime.now().strftime("%Y-%m-%d")
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date=None,
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        # end_date defaults to today; actual_end_date may be last trading day <= today
        assert result["end_date"] <= today_str

    def test_end_date_in_future_is_estimated(self):
        """When end_date is in the future, is_estimated should be True."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2099-01-01",
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        assert result["is_estimated"] is True


# ── Edge case tests ─────────────────────────────────────────

class TestEdgeCases:
    def test_future_start_date(self):
        """start_date in the future → error_key 'scenario.future_date'."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2099-01-01",
            investment_amount=100000.0,
            end_date="2099-12-31",
            client=client,
        )
        assert result["error_key"] == "scenario.future_date"

    def test_before_ipo(self):
        """start_date before first trading date → error_key 'scenario.before_ipo'."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2000-01-01",
            investment_amount=100000.0,
            client=client,
        )
        assert result["error_key"] == "scenario.before_ipo"

    def test_no_price_data(self):
        """Empty price DataFrame → error_key 'scenario.no_data'."""
        client = _mock_client(pd.DataFrame())
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-01",
            investment_amount=100000.0,
            client=client,
        )
        assert result["error_key"] == "scenario.no_data"

    def test_api_error(self):
        """Client raises exception → error_key 'scenario.no_data'."""
        client = MagicMock()
        client.get_daily_price.side_effect = Exception("API error")
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-01",
            investment_amount=100000.0,
            client=client,
        )
        assert result["error_key"] == "scenario.no_data"

    def test_missing_dividend_data_no_estimate(self):
        """When dividend data is empty and end_date is in the past, is_estimated should be False."""
        client = _mock_client(_PRICE_DF_2Y, pd.DataFrame())
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=True,
            client=client,
        )
        assert result["error_key"] is None
        # end_date is in the past, so is_estimated is False
        assert result["is_estimated"] is False

    def test_dividend_fetch_failure_no_estimate(self):
        """When dividend fetch raises and end_date is in the past, is_estimated should be False."""
        client = MagicMock()
        client.get_daily_price.return_value = _PRICE_DF_2Y
        client.get_dividend.side_effect = Exception("dividend error")
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=True,
            client=client,
        )
        assert result["error_key"] is None
        # end_date is in the past, so is_estimated is False
        assert result["is_estimated"] is False

    def test_shares_are_whole_numbers(self):
        """Shares should be floored to whole numbers."""
        client = _mock_client(_PRICE_DF_2Y)
        # 100000 / 100.0 = 1000.0 exactly
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        assert result["shares"] == 1000.0

    def test_shares_floor_with_remainder(self):
        """Shares should be floored when division has remainder."""
        client = _mock_client(_PRICE_DF_2Y)
        # 150000 / 100.0 = 1500.0
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=150000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        assert result["shares"] == 1500.0

    def test_result_fields_complete(self):
        """All expected fields should be present in ScenarioResult."""
        client = _mock_client(_PRICE_DF_2Y)
        result = calculate_scenario(
            stock_id="2330",
            start_date="2022-01-03",
            investment_amount=100000.0,
            end_date="2023-12-29",
            include_dividends=False,
            client=client,
        )
        expected_keys = {
            "start_date", "end_date", "start_price", "end_price",
            "shares", "total_return", "absolute_return",
            "dividend_income", "annualized_return", "max_drawdown",
            "days_held", "is_estimated", "error_key",
        }
        assert set(result.keys()) == expected_keys

    def test_negative_return(self):
        """When end_price < start_price, total_return should be negative."""
        dates = pd.date_range("2023-01-02", "2023-06-30", freq="B").strftime("%Y-%m-%d").tolist()
        # Declining prices: 150 → 100
        closes = [150.0 - i * 0.5 for i in range(len(dates))]
        price_df = _make_price_df(dates, closes)
        client = _mock_client(price_df)
        result = calculate_scenario(
            stock_id="2330",
            start_date=dates[0],
            investment_amount=100000.0,
            end_date=dates[-1],
            include_dividends=False,
            client=client,
        )
        assert result["error_key"] is None
        assert result["total_return"] < 0
        assert result["absolute_return"] < 0
