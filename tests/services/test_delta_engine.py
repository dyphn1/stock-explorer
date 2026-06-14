"""
Regression tests for delta_engine.py — explain_delta() and compute_recent_deltas().

Captures the CURRENT output of explain_delta() for all metric types, directions,
and magnitude tiers so that C134 refactoring (D-101) has a safe baseline.

All tests assert exact string output — any change in delta_engine.py will
cause these to fail, which is the intended behavior for regression tests.
"""
import pandas as pd
import pytest

from src.services.delta_engine import explain_delta, compute_recent_deltas


# ── explain_delta: 月營收 ──────────────────────────────────────

class TestExplainDeltaRevenue:
    """月營收 (monthly revenue) — thresholds: mild <30%, moderate ≥30%, extreme ≥50%."""

    def test_revenue_up_mild(self):
        """月營收成長 5% → mild tier (else branch, <30%)."""
        result = explain_delta("月營收", 5.0, "up")
        assert result == "月營收成長 5%，溫和成長中"

    def test_revenue_up_moderate(self):
        """月營收成長 35% → moderate tier (≥30%, <50%)."""
        result = explain_delta("月營收", 35.0, "up")
        assert result == "月營收成長 35%，表現相對正面，可能是需求回溫或新產品貢獻"

    def test_revenue_up_extreme(self):
        """月營收成長 60% → extreme tier (≥50%)."""
        result = explain_delta("月營收", 60.0, "up")
        assert result == "月營收暴增 60%，可能是大訂單入帳或旺季效應，可持續觀察其變化"

    def test_revenue_down_mild(self):
        """月營收衰退 5% → mild tier (else branch, <30%)."""
        result = explain_delta("月營收", -5.0, "down")
        assert result == "月營收小跌 5%，略有衰退但仍在合理範圍"

    def test_revenue_down_moderate(self):
        """月營收衰退 35% → moderate tier (≥30%, <50%)."""
        result = explain_delta("月營收", -35.0, "down")
        assert result == "月營收衰退 35%，表現不如預期，可能是需求下滑或訂單遞延"

    def test_revenue_down_extreme(self):
        """月營收衰退 60% → extreme tier (≥50%)."""
        result = explain_delta("月營收", -60.0, "down")
        assert result == "月營收驟降 60%，可能是淡季或失去大客戶，可留意其趨勢"


# ── explain_delta: 股價（近 30 日均價） ──────────────────────

class TestExplainDeltaPrice:
    """股價（近 30 日均價） — thresholds: mild <20%, moderate ≥20%, extreme ≥30%."""

    def test_price_up_mild(self):
        """股價上漲 5% → mild tier (else branch, <20%)."""
        result = explain_delta("股價（近 30 日均價）", 5.0, "up")
        assert result == "股價近 30 日上漲 5%，穩步走揚"

    def test_price_up_moderate(self):
        """股價上漲 25% → moderate tier (≥20%, <30%)."""
        result = explain_delta("股價（近 30 日均價）", 25.0, "up")
        assert result == "股價近 30 日上漲 25%，多頭趨勢明顯"

    def test_price_up_extreme(self):
        """股價上漲 40% → extreme tier (≥30%)."""
        result = explain_delta("股價（近 30 日均價）", 40.0, "up")
        assert result == "股價近 30 日大漲 40%，市場情緒樂觀，可能是基本面改善或利多消息推動"

    def test_price_down_mild(self):
        """股價下跌 5% → mild tier (else branch, <20%)."""
        result = explain_delta("股價（近 30 日均價）", -5.0, "down")
        assert result == "股價近 30 日小跌 5%，略有回檔"

    def test_price_down_moderate(self):
        """股價下跌 25% → moderate tier (≥20%, <30%)."""
        result = explain_delta("股價（近 30 日均價）", -25.0, "down")
        assert result == "股價近 30 日下跌 25%，空頭趨勢明顯"

    def test_price_down_extreme(self):
        """股價下跌 40% → extreme tier (≥30%)."""
        result = explain_delta("股價（近 30 日均價）", -40.0, "down")
        assert result == "股價近 30 日大跌 40%，市場信心不足，可能是利空消息或基本面惡化"


# ── explain_delta: 營收年增率 ─────────────────────────────────

class TestExplainDeltaYoy:
    """營收年增率 — thresholds: mild <20%, moderate ≥20%, extreme ≥50%."""

    def test_yoy_up_mild(self):
        """營收年增 5% → mild tier (else branch, <20%)."""
        result = explain_delta("營收年增率", 5.0, "up")
        assert result == "營收年增 5%，溫和成長"

    def test_yoy_up_moderate(self):
        """營收年增 25% → moderate tier (≥20%, <50%)."""
        result = explain_delta("營收年增率", 25.0, "up")
        assert result == "營收年增 25%，穩定成長，公司經營績效良好"

    def test_yoy_up_extreme(self):
        """營收年增 60% → extreme tier (≥50%)."""
        result = explain_delta("營收年增率", 60.0, "up")
        assert result == "營收年增 60%，成長非常強勁，可能是新產品大賣或市場需求爆發"

    def test_yoy_down_mild(self):
        """營收年減 5% → mild tier (else branch, <20%)."""
        result = explain_delta("營收年增率", -5.0, "down")
        assert result == "營收年減 5%，略有衰退"

    def test_yoy_down_moderate(self):
        """營收年減 25% → moderate tier (≥20%, <50%)."""
        result = explain_delta("營收年增率", -25.0, "down")
        assert result == "營收年減 25%，比去年差，需留意原因"

    def test_yoy_down_extreme(self):
        """營收年減 60% → extreme tier (≥50%)."""
        result = explain_delta("營收年增率", -60.0, "down")
        assert result == "營收年減 60%，大幅衰退，可能有結構性問題需要關注"


# ── explain_delta: boundary values ────────────────────────────

class TestExplainDeltaBoundaries:
    """Boundary values at exact threshold points."""

    # 月營收 boundaries (thresholds: 30, 50)
    def test_revenue_boundary_30_up(self):
        """月營收成長 exactly 30% → moderate tier (≥30%)."""
        result = explain_delta("月營收", 30.0, "up")
        assert result == "月營收成長 30%，表現相對正面，可能是需求回溫或新產品貢獻"

    def test_revenue_boundary_50_up(self):
        """月營收成長 exactly 50% → extreme tier (≥50%)."""
        result = explain_delta("月營收", 50.0, "up")
        assert result == "月營收暴增 50%，可能是大訂單入帳或旺季效應，可持續觀察其變化"

    def test_revenue_boundary_30_down(self):
        """月營收衰退 exactly 30% → moderate tier (≥30%)."""
        result = explain_delta("月營收", -30.0, "down")
        assert result == "月營收衰退 30%，表現不如預期，可能是需求下滑或訂單遞延"

    def test_revenue_boundary_50_down(self):
        """月營收衰退 exactly 50% → extreme tier (≥50%)."""
        result = explain_delta("月營收", -50.0, "down")
        assert result == "月營收驟降 50%，可能是淡季或失去大客戶，可留意其趨勢"

    # 股價 boundaries (thresholds: 20, 30)
    def test_price_boundary_20_up(self):
        """股價上漲 exactly 20% → moderate tier (≥20%)."""
        result = explain_delta("股價（近 30 日均價）", 20.0, "up")
        assert result == "股價近 30 日上漲 20%，多頭趨勢明顯"

    def test_price_boundary_30_up(self):
        """股價上漲 exactly 30% → extreme tier (≥30%)."""
        result = explain_delta("股價（近 30 日均價）", 30.0, "up")
        assert result == "股價近 30 日大漲 30%，市場情緒樂觀，可能是基本面改善或利多消息推動"

    def test_price_boundary_20_down(self):
        """股價下跌 exactly 20% → moderate tier (≥20%)."""
        result = explain_delta("股價（近 30 日均價）", -20.0, "down")
        assert result == "股價近 30 日下跌 20%，空頭趨勢明顯"

    def test_price_boundary_30_down(self):
        """股價下跌 exactly 30% → extreme tier (≥30%)."""
        result = explain_delta("股價（近 30 日均價）", -30.0, "down")
        assert result == "股價近 30 日大跌 30%，市場信心不足，可能是利空消息或基本面惡化"

    # 營收年增率 boundaries (thresholds: 20, 50)
    def test_yoy_boundary_20_up(self):
        """營收年增 exactly 20% → moderate tier (≥20%)."""
        result = explain_delta("營收年增率", 20.0, "up")
        assert result == "營收年增 20%，穩定成長，公司經營績效良好"

    def test_yoy_boundary_50_up(self):
        """營收年增 exactly 50% → extreme tier (≥50%)."""
        result = explain_delta("營收年增率", 50.0, "up")
        assert result == "營收年增 50%，成長非常強勁，可能是新產品大賣或市場需求爆發"

    def test_yoy_boundary_20_down(self):
        """營收年減 exactly 20% → moderate tier (≥20%)."""
        result = explain_delta("營收年增率", -20.0, "down")
        assert result == "營收年減 20%，比去年差，需留意原因"

    def test_yoy_boundary_50_down(self):
        """營收年減 exactly 50% → extreme tier (≥50%)."""
        result = explain_delta("營收年增率", -50.0, "down")
        assert result == "營收年減 50%，大幅衰退，可能有結構性問題需要關注"


# ── explain_delta: generic fallback ───────────────────────────

class TestExplainDeltaGeneric:
    """Generic fallback for unknown metric names."""

    def test_generic_up(self):
        result = explain_delta("自訂指標", 15.0, "up")
        assert result == "自訂指標 較前期成長 15.0%"

    def test_generic_down(self):
        result = explain_delta("自訂指標", -15.0, "down")
        assert result == "自訂指標 較前期衰退 15.0%"

    def test_generic_up_with_stock_name(self):
        result = explain_delta("自訂指標", 15.0, "up", stock_name="台積電")
        assert result == "台積電 自訂指標 較前期成長 15.0%"

    def test_generic_down_with_stock_name(self):
        result = explain_delta("自訂指標", -15.0, "down", stock_name="台積電")
        assert result == "台積電 自訂指標 較前期衰退 15.0%"


# ── explain_delta: stock_name prefix ──────────────────────────

class TestExplainDeltaStockName:
    """stock_name prefix behavior."""

    def test_revenue_up_with_stock_name(self):
        result = explain_delta("月營收", 35.0, "up", stock_name="台積電")
        assert result == "台積電 月營收成長 35%，表現相對正面，可能是需求回溫或新產品貢獻"

    def test_revenue_up_without_stock_name(self):
        result = explain_delta("月營收", 35.0, "up")
        assert result == "月營收成長 35%，表現相對正面，可能是需求回溫或新產品貢獻"

    def test_price_down_with_stock_name(self):
        result = explain_delta("股價（近 30 日均價）", -25.0, "down", stock_name="鴻海")
        assert result == "鴻海 股價近 30 日下跌 25%，空頭趨勢明顯"

    def test_yoy_up_with_stock_name(self):
        result = explain_delta("營收年增率", 60.0, "up", stock_name="聯發科")
        assert result == "聯發科 營收年增 60%，成長非常強勁，可能是新產品大賣或市場需求爆發"

    def test_empty_stock_name_no_prefix(self):
        """Empty string stock_name should not add a prefix."""
        result = explain_delta("月營收", 5.0, "up", stock_name="")
        assert result == "月營收成長 5%，溫和成長中"
        # Ensure no leading space (which would happen if "" was treated as truthy)
        assert not result.startswith(" ")


# ── compute_recent_deltas: threshold behavior ─────────────────

class TestComputeRecentDeltas:
    """compute_recent_deltas() threshold (>10% filter) and max-2-deltas behavior."""

    def _make_revenue_df(self, values):
        """Build monthly_revenue DataFrame with 'revenue' column."""
        n = len(values)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="ME")
        return pd.DataFrame({"date": dates, "revenue": values})

    def _make_price_df(self, n_days, base_price=100.0):
        """Build daily_price DataFrame with 'close' column."""
        dates = pd.date_range(end=pd.Timestamp.now(), periods=n_days, freq="D")
        return pd.DataFrame({"date": dates, "close": [base_price] * n_days})

    def test_revenue_change_below_threshold_excluded(self):
        """月營收變化 ≤10% 不應出現在結果中。"""
        rev_df = self._make_revenue_df([100, 105])  # 5% change
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_revenue_change_above_threshold_included(self):
        """月營收變化 >10% 應出現在結果中。"""
        rev_df = self._make_revenue_df([100, 120])  # 20% change
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert result[0]["metric_name"] == "月營收"
        assert result[0]["direction"] == "up"

    def test_revenue_change_exactly_10pct_excluded(self):
        """月營收變化 exactly 10% 不應出現（條件是 >10%，不是 ≥10%）。"""
        rev_df = self._make_revenue_df([100, 110])  # exactly 10%
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_revenue_change_just_above_10pct_included(self):
        """月營收變化 10.1% 應出現在結果中。"""
        rev_df = self._make_revenue_df([100, 110.1])  # 10.1% change
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert result[0]["metric_name"] == "月營收"

    def test_yoy_below_threshold_excluded(self):
        """營收年增率 ≤10% 不應出現在結果中。"""
        result = compute_recent_deltas(
            extra_metrics={"revenue_yoy": 5.0},
            monthly_revenue=None,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_yoy_above_threshold_included(self):
        """營收年增率 >10% 應出現在結果中。"""
        result = compute_recent_deltas(
            extra_metrics={"revenue_yoy": 25.0},
            monthly_revenue=None,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert result[0]["metric_name"] == "營收年增率"
        assert result[0]["direction"] == "up"

    def test_yoy_negative_above_threshold_included(self):
        """營收年增率 -25% (abs >10%) 應出現在結果中。"""
        result = compute_recent_deltas(
            extra_metrics={"revenue_yoy": -25.0},
            monthly_revenue=None,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert result[0]["metric_name"] == "營收年增率"
        assert result[0]["direction"] == "down"

    def test_yoy_exactly_10pct_excluded(self):
        """營收年增率 exactly 10% 不應出現。"""
        result = compute_recent_deltas(
            extra_metrics={"revenue_yoy": 10.0},
            monthly_revenue=None,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_max_two_deltas_returned(self):
        """即使有 3 個 delta 也最多回傳 2 個（[:2] slice）。"""
        rev_df = self._make_revenue_df([100, 150])  # 50% change → included
        result = compute_recent_deltas(
            extra_metrics={"revenue_yoy": 30.0},  # 30% → included
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        # Both revenue (50%) and yoy (30%) exceed 10%, but max 2 returned
        assert len(result) <= 2

    def test_no_data_returns_empty(self):
        """所有輸入為 None/空時，回傳空 list。"""
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=None,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert result == []

    def test_revenue_insufficient_data(self):
        """月營收只有 1 筆資料時無法計算變化。"""
        rev_df = self._make_revenue_df([100])
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_price_insufficient_data(self):
        """股價只有 30 天資料時無法計算 30 日 vs 前 30 日（需要 ≥60 天）。"""
        price_df = self._make_price_df(30)
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=None,
            daily_price=price_df,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_price_sufficient_data_with_change(self):
        """股價有 60 天資料且變化 >10% 時應被包含。"""
        dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq="D")
        # First 30 days: price 100, last 30 days: price 130 → 30% change
        closes = [100.0] * 30 + [130.0] * 30
        price_df = pd.DataFrame({"date": dates, "close": closes})
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=None,
            daily_price=price_df,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert result[0]["metric_name"] == "股價（近 30 日均價）"
        assert result[0]["direction"] == "up"

    def test_price_sufficient_data_no_significant_change(self):
        """股價有 60 天資料但變化 ≤10% 時不應被包含。"""
        dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq="D")
        closes = [100.0] * 30 + [105.0] * 30  # 5% change
        price_df = pd.DataFrame({"date": dates, "close": closes})
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=None,
            daily_price=price_df,
            latest_per_pbr=None,
        )
        assert len(result) == 0

    def test_delta_includes_explanation(self):
        """compute_recent_deltas 回傳的每個 delta 應包含 explanation 欄位。"""
        rev_df = self._make_revenue_df([100, 150])  # 50% change
        result = compute_recent_deltas(
            extra_metrics={},
            monthly_revenue=rev_df,
            daily_price=None,
            latest_per_pbr=None,
        )
        assert len(result) == 1
        assert "explanation" in result[0]
        assert result[0]["explanation"] != ""
        # Should match explain_delta output for 月營收 up extreme
        assert "暴增" in result[0]["explanation"]
