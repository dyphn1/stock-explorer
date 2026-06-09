"""
Unit tests for core business logic:
- calc_roe_ttm()
- _is_etf()
- filter_by_timeline()
- validate_stock_id()
- detect_revenue_event()
- detect_price_abnormal()
- detect_news_event()
- check_data_freshness()
- detect_company_type()
- extract_dividend_summary()
"""
import pandas as pd
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.services.roe_calculator import calc_roe_ttm
from src.services.watchlist import _is_etf
from src.pages._router_base import filter_by_timeline
from src.services.validation import validate_stock_id
from src.services.adaptive_engine import (
    detect_revenue_event,
    detect_price_abnormal,
    detect_news_event,
    check_data_freshness,
    detect_company_type,
)
from src.services.dividend_analyzer import extract_dividend_summary


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


# ── validate_stock_id() tests ─────────────────────────────

class TestValidateStockId:
    def test_valid_standard_ids(self):
        """Standard 4-digit stock IDs → valid."""
        for sid in ["2330", "0050", "1100"]:
            is_valid, cleaned = validate_stock_id(sid)
            assert is_valid is True
            assert cleaned == sid

    def test_valid_with_whitespace(self):
        """Stock ID with leading/trailing whitespace → valid after strip."""
        is_valid, cleaned = validate_stock_id("  2330  ")
        assert is_valid is True
        assert cleaned == "2330"

    def test_invalid_empty_string(self):
        """Empty string → invalid."""
        is_valid, msg = validate_stock_id("")
        assert is_valid is False
        assert "請輸入" in msg

    def test_invalid_non_numeric(self):
        """Non-numeric string → invalid."""
        is_valid, msg = validate_stock_id("abc")
        assert is_valid is False
        assert "數字" in msg

    def test_invalid_too_long(self):
        """More than 4 digits → invalid."""
        is_valid, msg = validate_stock_id("12345")
        assert is_valid is False
        assert "4 位" in msg

    def test_invalid_too_short(self):
        """Fewer than 4 digits → invalid."""
        is_valid, msg = validate_stock_id("12")
        assert is_valid is False
        assert "4 位" in msg

    def test_invalid_special_characters(self):
        """Special characters → invalid."""
        is_valid, msg = validate_stock_id("@#$%")
        assert is_valid is False
        assert "數字" in msg

    def test_invalid_mixed_alphanumeric(self):
        """Mixed letters and digits → invalid."""
        is_valid, msg = validate_stock_id("abcd")
        assert is_valid is False
        assert "數字" in msg

    def test_return_type(self):
        """Return type is tuple[bool, str]."""
        result = validate_stock_id("2330")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)


# ── detect_revenue_event() tests ──────────────────────────

def _make_revenue_df(values):
    """Helper: build a monthly_revenue DataFrame with 'revenue' column."""
    n = len(values)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="ME")
    return pd.DataFrame({"date": dates, "revenue": values})


class TestDetectRevenueEvent:
    def test_revenue_yoy_plus50_triggers(self):
        """Revenue YoY +50% → should trigger event (above +30% threshold)."""
        # 13 rows: 12 months ago = 100, latest = 150 → +50%
        values = [100.0] * 12 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["type"] == "revenue_surge"
        assert result["severity"] == "high"
        assert "成長" in result["title"]

    def test_revenue_yoy_minus50_triggers(self):
        """Revenue YoY -50% → should trigger event (below -30% threshold)."""
        values = [100.0] * 12 + [50.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["type"] == "revenue_surge"
        assert result["severity"] == "high"
        assert "衰退" in result["title"]

    def test_revenue_yoy_plus10_no_trigger(self):
        """Revenue YoY +10% → should NOT trigger (within ±30% range)."""
        values = [100.0] * 12 + [110.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_revenue_yoy_minus10_no_trigger(self):
        """Revenue YoY -10% → should NOT trigger (within ±30% range)."""
        values = [100.0] * 12 + [90.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_revenue_yoy_plus35_triggers_medium(self):
        """Revenue YoY +35% → triggers medium severity (between 30% and 50%)."""
        values = [100.0] * 12 + [135.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["severity"] == "medium"

    def test_empty_dataframe(self):
        """Empty DataFrame → should handle gracefully (returns None)."""
        df = pd.DataFrame(columns=["date", "revenue"])
        result = detect_revenue_event(df)
        assert result is None

    def test_insufficient_data(self):
        """Fewer than 13 rows → returns None."""
        values = [100.0] * 5 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_exactly_13_rows(self):
        """Exactly 13 rows → minimum data to compute YoY."""
        values = [100.0] * 12 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None


# ── detect_price_abnormal() tests ─────────────────────────

def _make_price_df(closes):
    """Helper: build a daily_prices DataFrame with 'close' column."""
    n = len(closes)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="D")
    return pd.DataFrame({"date": dates, "close": closes})


class TestDetectPriceAbnormal:
    def test_price_change_plus10_triggers(self):
        """Price change +10% → should trigger (above +7% threshold)."""
        df = _make_price_df([100.0, 110.0])
        result = detect_price_abnormal(df)
        assert result is not None
        assert result["type"] == "price_abnormal"
        assert result["severity"] == "high"
        assert "漲" in result["title"]

    def test_price_change_minus10_triggers(self):
        """Price change -10% → should trigger (below -7% threshold)."""
        df = _make_price_df([100.0, 90.0])
        result = detect_price_abnormal(df)
        assert result is not None
        assert result["type"] == "price_abnormal"
        assert result["severity"] == "high"
        assert "跌" in result["title"]

    def test_price_change_plus3_no_trigger(self):
        """Price change +3% → should NOT trigger (within ±7% range)."""
        df = _make_price_df([100.0, 103.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_price_change_minus3_no_trigger(self):
        """Price change -3% → should NOT trigger (within ±7% range)."""
        df = _make_price_df([100.0, 97.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_price_change_custom_threshold(self):
        """Custom threshold of 2% → +3% should trigger."""
        df = _make_price_df([100.0, 103.0])
        result = detect_price_abnormal(df, threshold=2.0)
        assert result is not None

    def test_single_row_no_trigger(self):
        """Only 1 row → returns None (need at least 2)."""
        df = _make_price_df([100.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_empty_dataframe(self):
        """Empty DataFrame → returns None."""
        df = pd.DataFrame(columns=["date", "close"])
        result = detect_price_abnormal(df)
        assert result is None

    def test_exactly_at_threshold(self):
        """Price change exactly at threshold (7%) → triggers (>= threshold)."""
        df = _make_price_df([100.0, 107.0])
        result = detect_price_abnormal(df, threshold=7.0)
        assert result is not None
        assert result["type"] == "price_abnormal"


# ── detect_news_event() tests ─────────────────────────────

def _make_news_df(titles):
    """Helper: build a news DataFrame with 'title' column."""
    return pd.DataFrame({"title": titles})


class TestDetectNewsEvent:
    def test_high_severity_keywords(self):
        """News with high-severity keywords → returns high severity events."""
        df = _make_news_df(["公司宣布合併案", "營收創新高"])
        events = detect_news_event(df)
        assert len(events) >= 1
        assert events[0]["severity"] == "high"
        assert events[0]["type"] == "news_major"

    def test_medium_severity_keywords(self):
        """News with medium-severity keywords → returns medium severity events."""
        df = _make_news_df(["董事會決議股利分派"])
        events = detect_news_event(df)
        assert len(events) >= 1
        assert events[0]["severity"] == "medium"
        assert events[0]["type"] == "news_medium"

    def test_no_matching_keywords(self):
        """News with no matching keywords → returns empty list."""
        df = _make_news_df(["今日天氣晴朗", "股市小漲"])
        events = detect_news_event(df)
        assert len(events) == 0

    def test_empty_dataframe(self):
        """Empty news DataFrame → returns empty list."""
        df = pd.DataFrame(columns=["title"])
        events = detect_news_event(df)
        assert events == []

    def test_mixed_severity(self):
        """Mix of high and medium severity news → both detected."""
        df = _make_news_df(["公司宣布合併案", "董事會決議股利分派"])
        events = detect_news_event(df)
        assert len(events) == 2
        severities = {e["severity"] for e in events}
        assert "high" in severities
        assert "medium" in severities

    def test_high_severity_keywords_bankruptcy(self):
        """Bankruptcy keyword → high severity."""
        df = _make_news_df(["公司聲請破產"])
        events = detect_news_event(df)
        assert len(events) == 1
        assert events[0]["severity"] == "high"

    def test_high_severity_keywords_fraud(self):
        """Fraud keyword → high severity."""
        df = _make_news_df(["財報造假遭調查"])
        events = detect_news_event(df)
        assert len(events) == 1
        assert events[0]["severity"] == "high"

    def test_max_5_news_checked(self):
        """Only first 5 news items are checked."""
        titles = ["公司宣布合併案"] * 10
        df = _make_news_df(titles)
        events = detect_news_event(df)
        assert len(events) <= 5


# ── check_data_freshness() tests ──────────────────────────

class TestCheckDataFreshness:
    def _make_price_df_date(self, date_str):
        """Helper: single-row price DataFrame with given date."""
        return pd.DataFrame({"date": [date_str], "close": [100.0]})

    def _make_revenue_df_date(self, date_str):
        """Helper: single-row revenue DataFrame with given date."""
        return pd.DataFrame({"date": [date_str], "revenue": [100.0]})

    def test_fresh_data_today(self):
        """Data from today → fresh."""
        today = datetime.now().strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(today),
            "monthly_revenue": self._make_revenue_df_date(today),
        }
        result = check_data_freshness("2330", data)
        assert result["overall"] == "fresh"
        assert result["needs_update"] is False

    def test_stale_data_over_7_days(self):
        """Price data >7 days old → stale status."""
        old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(old_date),
        }
        result = check_data_freshness("2330", data)
        assert result["overall"] in ("stale", "partial")
        assert result["needs_update"] is True
        price_item = result["items"][0]
        assert price_item["status"] == "very_stale"

    def test_very_stale_revenue(self):
        """Revenue data >60 days old → very_stale status."""
        old_date = (datetime.now() - timedelta(days=70)).strftime("%Y-%m-%d")
        data = {
            "monthly_revenue": self._make_revenue_df_date(old_date),
        }
        result = check_data_freshness("2330", data)
        rev_item = result["items"][0]
        assert rev_item["status"] == "very_stale"

    def test_stale_price_4_days(self):
        """Price data 4 days old → stale (not fresh, not very_stale)."""
        date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(date),
        }
        result = check_data_freshness("2330", data)
        price_item = result["items"][0]
        assert price_item["status"] == "stale"

    def test_empty_data(self):
        """No data at all → unknown overall, no items."""
        result = check_data_freshness("2330", {})
        assert result["overall"] == "fresh"  # no items → all() is True
        assert len(result["items"]) == 0

    def test_none_data_values(self):
        """None values for data keys → handled gracefully."""
        data = {"daily_price": None, "monthly_revenue": None}
        result = check_data_freshness("2330", data)
        assert len(result["items"]) == 0

    def test_mixed_fresh_and_stale(self):
        """One fresh, one stale → partial overall."""
        today = datetime.now().strftime("%Y-%m-%d")
        # Revenue stale if >35 days; price stale if >3 days
        rev_stale_date = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(today),
            "monthly_revenue": self._make_revenue_df_date(rev_stale_date),
        }
        result = check_data_freshness("2330", data)
        assert result["overall"] == "partial"
        assert result["needs_update"] is True


# ── detect_company_type() tests ───────────────────────────

class TestDetectCompanyType:
    def test_etf_by_industry(self):
        """Industry contains 'ETF' → 'etf'."""
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": "ETF"}
        assert detect_company_type(data) == "etf"

    def test_etf_by_industry_case_insensitive(self):
        """Industry 'etf' lowercase → 'etf'."""
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": "etf"}
        assert detect_company_type(data) == "etf"

    def test_etf_by_id_pattern(self):
        """Industry empty + 00xx ID → 'etf'."""
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": ""}
        assert detect_company_type(data) == "etf"

    def test_group_by_keyword_jituan(self):
        """Name contains '集團' → 'group'."""
        data = {"stock_id": "1101", "stock_name": "台塑集團", "industry": "化學工業"}
        assert detect_company_type(data) == "group"

    def test_group_by_keyword_konggu(self):
        """Name contains '控股' → 'group'."""
        data = {"stock_id": "2330", "stock_name": "某控股", "industry": "其他"}
        assert detect_company_type(data) == "group"

    def test_group_by_keyword_gufen(self):
        """Name contains '股份' → 'group'."""
        data = {"stock_id": "2330", "stock_name": "某股份", "industry": "其他"}
        assert detect_company_type(data) == "group"

    def test_default_regular_company(self):
        """Regular company → 'default'."""
        data = {"stock_id": "2330", "stock_name": "台積電", "industry": "半導體業"}
        assert detect_company_type(data) == "default"

    def test_default_non_etf_non_group(self):
        """Non-ETF, non-group → 'default'."""
        data = {"stock_id": "1101", "stock_name": "台泥", "industry": "水泥工業"}
        assert detect_company_type(data) == "default"

    def test_etf_industry_takes_priority(self):
        """ETF industry takes priority over group name."""
        data = {"stock_id": "0050", "stock_name": "某集團", "industry": "ETF"}
        assert detect_company_type(data) == "etf"

    def test_non_00_id_not_etf(self):
        """Non-00xx ID with empty industry → not ETF."""
        data = {"stock_id": "1101", "stock_name": "台泥", "industry": ""}
        assert detect_company_type(data) == "default"


# ── extract_dividend_summary() tests ──────────────────────

def _make_dividend_df(rows):
    """
    Helper: build a dividend DataFrame.
    rows: list of dicts with keys matching FinMind columns.
    """
    return pd.DataFrame(rows)


class TestExtractDividendSummary:
    def test_no_dividend_data_none(self):
        """None dividend_df → has_data=False, frequency=none."""
        result = extract_dividend_summary(None)
        assert result["has_data"] is False
        assert result["frequency"] == "none"
        assert result["latest_cash_div"] is None

    def test_no_dividend_data_empty(self):
        """Empty dividend_df → has_data=False."""
        df = pd.DataFrame(columns=["CashEarningsDistribution", "date"])
        result = extract_dividend_summary(df)
        assert result["has_data"] is False
        assert result["frequency"] == "none"

    def test_no_cash_dividend_column(self):
        """Missing CashEarningsDistribution column → has_data=False."""
        df = pd.DataFrame({"date": ["2024-01-01"], "CashExDividendTradingDate": ["2024-06-01"]})
        result = extract_dividend_summary(df)
        assert result["has_data"] is False

    def test_all_zero_cash_dividends(self):
        """All zero cash dividends → has_data=False."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 0, "date": "2024-01-01",
             "CashExDividendTradingDate": "2024-06-01", "CashDividendPaymentDate": "2024-07-01",
             "StockEarningsDistribution": 0, "year": "113年"},
        ])
        result = extract_dividend_summary(df)
        assert result["has_data"] is False

    def test_annual_dividends(self):
        """Annual dividends → frequency 'annual'."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 3.0, "date": "2024-06-01",
             "CashExDividendTradingDate": "2024-06-15", "CashDividendPaymentDate": "2024-07-15",
             "StockEarningsDistribution": 0, "year": "113年"},
            {"CashEarningsDistribution": 2.5, "date": "2023-06-01",
             "CashExDividendTradingDate": "2023-06-15", "CashDividendPaymentDate": "2023-07-15",
             "StockEarningsDistribution": 0, "year": "112年"},
        ])
        result = extract_dividend_summary(df)
        assert result["has_data"] is True
        assert result["frequency"] == "annual"
        assert result["latest_cash_div"] == 3.0

    def test_quarterly_dividends(self):
        """Quarterly dividends (3+ per year) → frequency 'quarterly'."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 1.0, "date": "2024-12-01",
             "CashExDividendTradingDate": "2024-12-15", "CashDividendPaymentDate": "2025-01-15",
             "StockEarningsDistribution": 0, "year": "113年"},
            {"CashEarningsDistribution": 1.0, "date": "2024-09-01",
             "CashExDividendTradingDate": "2024-09-15", "CashDividendPaymentDate": "2024-10-15",
             "StockEarningsDistribution": 0, "year": "113年"},
            {"CashEarningsDistribution": 1.0, "date": "2024-06-01",
             "CashExDividendTradingDate": "2024-06-15", "CashDividendPaymentDate": "2024-07-15",
             "StockEarningsDistribution": 0, "year": "113年"},
            {"CashEarningsDistribution": 1.0, "date": "2024-03-01",
             "CashExDividendTradingDate": "2024-03-15", "CashDividendPaymentDate": "2024-04-15",
             "StockEarningsDistribution": 0, "year": "113年"},
        ])
        result = extract_dividend_summary(df)
        assert result["has_data"] is True
        assert result["frequency"] == "quarterly"

    def test_estimated_yield(self):
        """With current_price → estimated_yield is calculated."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 3.0, "date": "2024-06-01",
             "CashExDividendTradingDate": "2024-06-15", "CashDividendPaymentDate": "2024-07-15",
             "StockEarningsDistribution": 0, "year": "113年"},
        ])
        result = extract_dividend_summary(df, current_price=100.0)
        assert result["has_data"] is True
        assert result["estimated_yield"] is not None
        assert result["estimated_yield"] == 3.0

    def test_yearly_dividends_list(self):
        """yearly_dividends list is populated."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 3.0, "date": "2024-06-01",
             "CashExDividendTradingDate": "2024-06-15", "CashDividendPaymentDate": "2024-07-15",
             "StockEarningsDistribution": 0, "year": "113年"},
        ])
        result = extract_dividend_summary(df)
        assert len(result["yearly_dividends"]) == 1
        assert result["yearly_dividends"][0]["cash_div"] == 3.0
        assert result["yearly_dividends"][0]["year"] == "113年"

    def test_plain_summary_generated(self):
        """plain_summary is a non-empty string."""
        df = _make_dividend_df([
            {"CashEarningsDistribution": 3.0, "date": "2024-06-01",
             "CashExDividendTradingDate": "2024-06-15", "CashDividendPaymentDate": "2024-07-15",
             "StockEarningsDistribution": 0, "year": "113年"},
        ])
        result = extract_dividend_summary(df)
        assert isinstance(result["plain_summary"], str)
        assert len(result["plain_summary"]) > 0
