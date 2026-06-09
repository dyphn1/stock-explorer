"""
Unit tests for core business logic:
- calc_roe_ttm()
- _is_etf()
- filter_by_timeline()
"""
import pandas as pd
import pytest
from datetime import datetime, timedelta

from src.services.roe_calculator import calc_roe_ttm
from src.services.watchlist import _is_etf
from src.pages._router_base import filter_by_timeline


# ── calc_roe_ttm() tests ──────────────────────────────────

def _make_financial_df(rows):
    """Helper: build a financial DataFrame from list of (date, type, value)."""
    return pd.DataFrame(rows, columns=["date", "type", "value"])


def _make_balance_df(rows):
    """Helper: build a balance-sheet DataFrame from list of (date, type, value)."""
    return pd.DataFrame(rows, columns=["date", "type", "value"])


class TestCalcRoeTtm:
    def test_full_ttm_4_quarters(self):
        """4 quarters of net income → TTM method."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
            ("2024-06-30", "淨利", 80.0),
            ("2024-03-31", "淨利", 60.0),
            ("2023-12-31", "淨利", 40.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
            ("2023-12-31", "權益總計", 800.0),
        ])
        result = calc_roe_ttm(fin, bal)
        assert result is not None
        assert result["method"] == "TTM"
        assert result["quarters_used"] == 4
        assert result["ttm_net_income"] == 280.0
        assert result["roe"] == pytest.approx(280.0 / 900.0 * 100, rel=1e-2)

    def test_single_quarter(self):
        """Only 1 quarter available → 單季 method."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
        ])
        result = calc_roe_ttm(fin, bal)
        assert result is not None
        assert result["method"] == "單季"
        assert result["quarters_used"] == 1
        assert result["roe"] == pytest.approx(10.0, rel=1e-2)

    def test_two_quarters(self):
        """2 quarters → N季累計 method."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
            ("2024-06-30", "淨利", 80.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
            ("2024-06-30", "權益總計", 900.0),
        ])
        result = calc_roe_ttm(fin, bal)
        assert result is not None
        assert result["method"] == "2季累計"
        assert result["quarters_used"] == 2

    def test_empty_financial(self):
        """Empty financial df → None."""
        fin = _make_financial_df([])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
        ])
        assert calc_roe_ttm(fin, bal) is None

    def test_empty_balance(self):
        """Empty balance sheet → None."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
        ])
        bal = _make_balance_df([])
        assert calc_roe_ttm(fin, bal) is None

    def test_none_financial(self):
        """None financial df → None."""
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
        ])
        assert calc_roe_ttm(None, bal) is None

    def test_none_balance(self):
        """None balance sheet → None."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
        ])
        assert calc_roe_ttm(fin, None) is None

    def test_zero_equity(self):
        """All equity values are zero → None."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", 100.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 0.0),
        ])
        assert calc_roe_ttm(fin, bal) is None

    def test_negative_roe(self):
        """Negative net income → negative ROE."""
        fin = _make_financial_df([
            ("2024-09-30", "淨利", -50.0),
            ("2024-06-30", "淨利", -30.0),
            ("2024-03-31", "淨利", -20.0),
            ("2023-12-31", "淨利", -10.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "權益總計", 1000.0),
            ("2023-12-31", "權益總計", 1000.0),
        ])
        result = calc_roe_ttm(fin, bal)
        assert result is not None
        assert result["roe"] < 0

    def test_english_column_names(self):
        """English keywords should also match."""
        fin = _make_financial_df([
            ("2024-09-30", "Net Income", 100.0),
            ("2024-06-30", "Net Income", 80.0),
            ("2024-03-31", "Net Income", 60.0),
            ("2023-12-31", "Net Income", 40.0),
        ])
        bal = _make_balance_df([
            ("2024-09-30", "Total Equity", 1000.0),
            ("2023-12-31", "Total Equity", 800.0),
        ])
        result = calc_roe_ttm(fin, bal)
        assert result is not None
        assert result["method"] == "TTM"


# ── _is_etf() tests ───────────────────────────────────────

class TestIsEtf:
    def test_regular_stock(self):
        """Normal stock → not ETF."""
        assert _is_etf("2330", "台積電", "半導體業") is False

    def test_etf_by_industry(self):
        """Industry category contains 'etf' → ETF."""
        assert _is_etf("0050", "元大台灣50", "ETF") is True

    def test_etf_by_industry_case_insensitive(self):
        """Industry category 'etf' case insensitive."""
        assert _is_etf("0050", "元大台灣50", "etf") is True
        assert _is_etf("0050", "元大台灣50", "Etf") is True

    def test_etf_by_name_contains_etf(self):
        """Name contains 'etf' → ETF."""
        assert _is_etf("0050", "某 ETF 基金", "其他") is True

    def test_etf_by_name_heuristic_dividend(self):
        """Name contains 高息 → ETF."""
        assert _is_etf("0056", "元大高股息", "其他") is True

    def test_etf_by_name_heuristic_bond(self):
        """Name contains 債券 → ETF."""
        assert _is_etf("00679B", "元大美債20年", "其他") is True

    def test_etf_by_name_heuristic_5g(self):
        """Name contains 5G → ETF."""
        assert _is_etf("00891", "中信 5G 概念", "其他") is True

    def test_non_etf_name_without_keywords(self):
        """Name without any ETF keywords and non-00 ID → not ETF."""
        assert _is_etf("2330", "中信金", "其他") is False

    def test_etf_by_id_pattern_00xx(self):
        """Stock ID starts with 00 and 4 digits → ETF (last resort)."""
        assert _is_etf("0050", "元大台灣50", "其他") is True
        assert _is_etf("006208", "富邦台50", "其他") is False  # 6 digits, not 4

    def test_etf_by_id_pattern_non_00(self):
        """Stock ID not starting with 00 → not ETF by ID pattern."""
        assert _is_etf("1101", "台泥", "其他") is False

    def test_etf_industry_takes_priority(self):
        """Industry check runs first (priority test)."""
        # Even if name doesn't suggest ETF, industry does
        assert _is_etf("2330", "某特別股", "ETF") is True

    def test_none_industry(self):
        """None industry_category → falls through to name/ID checks."""
        assert _is_etf("2330", "台積電", None) is False

    def test_empty_industry(self):
        """Empty string industry_category → falls through."""
        assert _is_etf("2330", "台積電", "") is False


# ── filter_by_timeline() tests ────────────────────────────

class TestFilterByTimeline:
    def _make_df(self, dates):
        """Helper: build a DataFrame with a 'date' column."""
        return pd.DataFrame({"date": pd.to_datetime(dates), "value": range(len(dates))})

    def test_empty_df(self):
        """Empty DataFrame → returns empty."""
        df = pd.DataFrame(columns=["date", "value"])
        result = filter_by_timeline(df, date_col="date", timeline_key="test_tl")
        assert len(result) == 0

    def test_none_df(self):
        """None DataFrame → returns None."""
        result = filter_by_timeline(None, date_col="date", timeline_key="test_tl")
        assert result is None

    def test_all_returns_everything(self):
        """ALL timeline → returns all rows."""
        dates = pd.date_range("2020-01-01", periods=200, freq="D")
        df = self._make_df(dates)
        result = filter_by_timeline(df, date_col="date", timeline_key="test_tl_all")
        assert len(result) == 200

    def test_1y_filter(self):
        """1Y timeline → only rows within last 365 days."""
        import streamlit as st
        now = pd.Timestamp.now()
        old_dates = pd.date_range(now - pd.Timedelta(days=500), periods=10, freq="D")
        new_dates = pd.date_range(now - pd.Timedelta(days=30), periods=5, freq="D")
        all_dates = old_dates.append(new_dates)
        df = pd.DataFrame({"date": all_dates, "value": range(len(all_dates))})
        # Explicitly set session_state to "1Y" for this test
        st.session_state["test_tl_1y"] = "1Y"
        result = filter_by_timeline(df, date_col="date", timeline_key="test_tl_1y")
        # Only the 5 recent dates should remain
        assert len(result) == 5

    def test_3y_filter(self):
        """3Y timeline → rows within last ~1095 days."""
        now = pd.Timestamp.now()
        old_dates = pd.date_range(now - pd.Timedelta(days=1500), periods=10, freq="D")
        new_dates = pd.date_range(now - pd.Timedelta(days=100), periods=5, freq="D")
        all_dates = old_dates.append(new_dates)
        df = pd.DataFrame({"date": all_dates, "value": range(len(all_dates))})
        result = filter_by_timeline(df, date_col="date", timeline_key="test_tl_3y")
        # Only the 5 recent dates should remain (old ones are > 3 years)
        assert len(result) == 5

    def test_missing_timeline_key_defaults_to_3y(self):
        """Missing timeline key in session_state → defaults to 3Y."""
        now = pd.Timestamp.now()
        old_dates = pd.date_range(now - pd.Timedelta(days=1500), periods=10, freq="D")
        new_dates = pd.date_range(now - pd.Timedelta(days=100), periods=5, freq="D")
        all_dates = old_dates.append(new_dates)
        df = pd.DataFrame({"date": all_dates, "value": range(len(all_dates))})
        # Use a key that won't be in session_state
        result = filter_by_timeline(df, date_col="date", timeline_key="test_tl_default")
        # Default is 3Y, so old dates (> 3Y) should be filtered out
        assert len(result) == 5
