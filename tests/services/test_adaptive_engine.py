"""
Smoke tests for adaptive_engine.py services.

Tests: detect_revenue_event, detect_news_event, detect_price_abnormal,
       detect_company_type, check_data_freshness.

All tests use mock/sample data — no real API calls.
"""
import pandas as pd
import pytest
from datetime import datetime, timedelta

from src.services.adaptive_engine import (
    detect_revenue_event,
    detect_news_event,
    detect_price_abnormal,
    detect_company_type,
    check_data_freshness,
)


# ── Helpers ──────────────────────────────────────────────────

def _make_revenue_df(values):
    """Build monthly_revenue DataFrame with 'revenue' column."""
    n = len(values)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="ME")
    return pd.DataFrame({"date": dates, "revenue": values})


def _make_price_df(closes):
    """Build daily_price DataFrame with 'close' column."""
    n = len(closes)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="D")
    return pd.DataFrame({"date": dates, "close": closes})


def _make_news_df(titles):
    """Build a news DataFrame with 'title' column."""
    return pd.DataFrame({"title": titles})


# ── detect_revenue_event() ───────────────────────────────────

class TestDetectRevenueEvent:
    def test_revenue_yoy_plus50_triggers(self):
        values = [100.0] * 12 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["type"] == "revenue_surge"
        assert result["severity"] == "high"
        assert "成長" in result["title"]

    def test_revenue_yoy_minus50_triggers(self):
        values = [100.0] * 12 + [50.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["type"] == "revenue_surge"
        assert result["severity"] == "high"
        assert "衰退" in result["title"]

    def test_revenue_yoy_plus10_no_trigger(self):
        values = [100.0] * 12 + [110.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_revenue_yoy_minus10_no_trigger(self):
        values = [100.0] * 12 + [90.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_revenue_yoy_plus35_triggers_medium(self):
        values = [100.0] * 12 + [135.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None
        assert result["severity"] == "medium"

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["date", "revenue"])
        result = detect_revenue_event(df)
        assert result is None

    def test_insufficient_data(self):
        values = [100.0] * 5 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is None

    def test_exactly_13_rows(self):
        values = [100.0] * 12 + [150.0]
        df = _make_revenue_df(values)
        result = detect_revenue_event(df)
        assert result is not None


# ── detect_price_abnormal() ──────────────────────────────────

class TestDetectPriceAbnormal:
    def test_price_change_plus10_triggers(self):
        df = _make_price_df([100.0, 110.0])
        result = detect_price_abnormal(df)
        assert result is not None
        assert result["type"] == "price_abnormal"
        assert result["severity"] == "high"
        assert "漲" in result["title"]

    def test_price_change_minus10_triggers(self):
        df = _make_price_df([100.0, 90.0])
        result = detect_price_abnormal(df)
        assert result is not None
        assert result["type"] == "price_abnormal"
        assert result["severity"] == "high"
        assert "跌" in result["title"]

    def test_price_change_plus3_no_trigger(self):
        df = _make_price_df([100.0, 103.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_price_change_minus3_no_trigger(self):
        df = _make_price_df([100.0, 97.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_price_change_custom_threshold(self):
        df = _make_price_df([100.0, 103.0])
        result = detect_price_abnormal(df, threshold=2.0)
        assert result is not None

    def test_single_row_no_trigger(self):
        df = _make_price_df([100.0])
        result = detect_price_abnormal(df)
        assert result is None

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["date", "close"])
        result = detect_price_abnormal(df)
        assert result is None

    def test_exactly_at_threshold(self):
        df = _make_price_df([100.0, 107.0])
        result = detect_price_abnormal(df, threshold=7.0)
        assert result is not None
        assert result["type"] == "price_abnormal"


# ── detect_news_event() ──────────────────────────────────────

class TestDetectNewsEvent:
    def test_high_severity_keywords(self):
        df = _make_news_df(["公司宣布合併案", "營收創新高"])
        events = detect_news_event(df)
        assert len(events) >= 1
        assert events[0]["severity"] == "high"
        assert events[0]["type"] == "news_major"

    def test_medium_severity_keywords(self):
        df = _make_news_df(["董事會決議股利分派"])
        events = detect_news_event(df)
        assert len(events) >= 1
        assert events[0]["severity"] == "medium"
        assert events[0]["type"] == "news_medium"

    def test_no_matching_keywords(self):
        df = _make_news_df(["今日天氣晴朗", "股市小漲"])
        events = detect_news_event(df)
        assert len(events) == 0

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["title"])
        events = detect_news_event(df)
        assert events == []

    def test_mixed_severity(self):
        df = _make_news_df(["公司宣布合併案", "董事會決議股利分派"])
        events = detect_news_event(df)
        assert len(events) == 2
        severities = {e["severity"] for e in events}
        assert "high" in severities
        assert "medium" in severities

    def test_high_severity_keywords_bankruptcy(self):
        df = _make_news_df(["公司聲請破產"])
        events = detect_news_event(df)
        assert len(events) == 1
        assert events[0]["severity"] == "high"

    def test_high_severity_keywords_fraud(self):
        df = _make_news_df(["財報造假遭調查"])
        events = detect_news_event(df)
        assert len(events) == 1
        assert events[0]["severity"] == "high"

    def test_max_5_news_checked(self):
        titles = ["公司宣布合併案"] * 10
        df = _make_news_df(titles)
        events = detect_news_event(df)
        assert len(events) <= 5

    def test_false_positive_merged_revenue(self):
        df = _make_news_df(["水泥雙雄台泥、亞泥4月合併營收分別月減1.6%及月增6.5%"])
        events = detect_news_event(df)
        major = [e for e in events if e["severity"] == "high"]
        assert len(major) == 0, f"合併營收 should not trigger news_major, got {major}"


# ── check_data_freshness() ───────────────────────────────────

class TestCheckDataFreshness:
    def _make_price_df_date(self, date_str):
        return pd.DataFrame({"date": [date_str], "close": [100.0]})

    def _make_revenue_df_date(self, date_str):
        return pd.DataFrame({"date": [date_str], "revenue": [100.0]})

    def test_fresh_data_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(today),
            "monthly_revenue": self._make_revenue_df_date(today),
        }
        result = check_data_freshness("2330", data)
        assert result["overall"] == "fresh"
        assert result["needs_update"] is False

    def test_stale_data_over_7_days(self):
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
        old_date = (datetime.now() - timedelta(days=70)).strftime("%Y-%m-%d")
        data = {
            "monthly_revenue": self._make_revenue_df_date(old_date),
        }
        result = check_data_freshness("2330", data)
        rev_item = result["items"][0]
        assert rev_item["status"] == "very_stale"

    def test_stale_price_4_days(self):
        date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(date),
        }
        result = check_data_freshness("2330", data)
        price_item = result["items"][0]
        assert price_item["status"] == "stale"

    def test_empty_data(self):
        result = check_data_freshness("2330", {})
        assert result["overall"] == "fresh"
        assert len(result["items"]) == 0

    def test_none_data_values(self):
        data = {"daily_price": None, "monthly_revenue": None}
        result = check_data_freshness("2330", data)
        assert len(result["items"]) == 0

    def test_mixed_fresh_and_stale(self):
        today = datetime.now().strftime("%Y-%m-%d")
        rev_stale_date = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")
        data = {
            "daily_price": self._make_price_df_date(today),
            "monthly_revenue": self._make_revenue_df_date(rev_stale_date),
        }
        result = check_data_freshness("2330", data)
        assert result["overall"] == "partial"
        assert result["needs_update"] is True


# ── detect_company_type() ────────────────────────────────────

class TestDetectCompanyType:
    def test_etf_by_industry(self):
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": "ETF"}
        assert detect_company_type(data) == "etf"

    def test_etf_by_industry_case_insensitive(self):
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": "etf"}
        assert detect_company_type(data) == "etf"

    def test_etf_by_id_pattern(self):
        data = {"stock_id": "0050", "stock_name": "元大台灣50", "industry": ""}
        assert detect_company_type(data) == "etf"

    def test_group_by_keyword_jituan(self):
        data = {"stock_id": "1101", "stock_name": "台塑集團", "industry": "化學工業"}
        assert detect_company_type(data) == "group"

    def test_group_by_keyword_konggu(self):
        data = {"stock_id": "2330", "stock_name": "某控股", "industry": "其他"}
        assert detect_company_type(data) == "group"

    def test_group_by_keyword_gufen(self):
        data = {"stock_id": "2330", "stock_name": "某股份", "industry": "其他"}
        assert detect_company_type(data) == "group"

    def test_default_regular_company(self):
        data = {"stock_id": "2330", "stock_name": "台積電", "industry": "半導體業"}
        assert detect_company_type(data) == "default"

    def test_default_non_etf_non_group(self):
        data = {"stock_id": "1101", "stock_name": "台泥", "industry": "水泥工業"}
        assert detect_company_type(data) == "default"

    def test_etf_industry_takes_priority(self):
        data = {"stock_id": "0050", "stock_name": "某集團", "industry": "ETF"}
        assert detect_company_type(data) == "etf"

    def test_non_00_id_not_etf(self):
        data = {"stock_id": "1101", "stock_name": "台泥", "industry": ""}
        assert detect_company_type(data) == "default"
