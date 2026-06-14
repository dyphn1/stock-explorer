"""
Regression tests for DeltaExplanationProvider — D-103

Tests the DeltaExplanationProvider class and _pick_template() function
from delta_explanation_provider.py, covering all metric types, directions,
magnitude tiers, boundary values, stock_name prefix behavior, generic fallback,
and protocol compliance.
"""
import pytest

from src.services.delta_explanation_provider import DeltaExplanationProvider, _pick_template
from src.services.llm.base import ExplanationRequest


# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture
def provider():
    """Create a fresh DeltaExplanationProvider instance."""
    return DeltaExplanationProvider()


def _make_request(metric_name, direction, change_pct, stock_name=""):
    """Helper to create an ExplanationRequest with delta context."""
    abs_pct = abs(change_pct)
    return ExplanationRequest(
        metric_name=metric_name,
        metric_value=f"{abs_pct:.1f}%",
        delta=f"{abs_pct:+.1f}%",
        context={
            "stock_name": stock_name,
            "direction": direction,
            "change_pct": change_pct,
        },
        language="zh-TW",
    )


# ── is_available ────────────────────────────────────────────────

class TestIsAvailable:
    """DeltaExplanationProvider.is_available() always returns True."""

    def test_is_available_returns_true(self, provider):
        assert provider.is_available() is True


# ── explain(): 月營收 ──────────────────────────────────────────

class TestExplainRevenue:
    """月營收 — thresholds: mild <30%, moderate ≥30%, extreme ≥50%."""

    def test_revenue_up_mild(self, provider):
        request = _make_request("月營收", "up", 5.0)
        resp = provider.explain(request)
        assert resp.text == "月營收成長 5%，溫和成長中"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_revenue_up_moderate(self, provider):
        request = _make_request("月營收", "up", 35.0)
        resp = provider.explain(request)
        assert resp.text == "月營收成長 35%，表現相對正面，可能是需求回溫或新產品貢獻"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_revenue_up_extreme(self, provider):
        request = _make_request("月營收", "up", 60.0)
        resp = provider.explain(request)
        assert resp.text == "月營收暴增 60%，可能是大訂單入帳或旺季效應，可持續觀察其變化"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_revenue_down_mild(self, provider):
        request = _make_request("月營收", "down", -5.0)
        resp = provider.explain(request)
        assert resp.text == "月營收小跌 5%，略有衰退但仍在合理範圍"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_revenue_down_moderate(self, provider):
        request = _make_request("月營收", "down", -35.0)
        resp = provider.explain(request)
        assert resp.text == "月營收衰退 35%，表現不如預期，可能是需求下滑或訂單遞延"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_revenue_down_extreme(self, provider):
        request = _make_request("月營收", "down", -60.0)
        resp = provider.explain(request)
        assert resp.text == "月營收驟降 60%，可能是淡季或失去大客戶，可留意其趨勢"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0


# ── explain(): 股價（近 30 日均價） ──────────────────────────

class TestExplainPrice:
    """股價（近 30 日均價） — thresholds: mild <20%, moderate ≥20%, extreme ≥30%."""

    def test_price_up_mild(self, provider):
        request = _make_request("股價（近 30 日均價）", "up", 5.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日上漲 5%，穩步走揚"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_price_up_moderate(self, provider):
        request = _make_request("股價（近 30 日均價）", "up", 25.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日上漲 25%，多頭趨勢明顯"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_price_up_extreme(self, provider):
        request = _make_request("股價（近 30 日均價）", "up", 40.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日大漲 40%，市場情緒樂觀，可能是基本面改善或利多消息推動"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_price_down_mild(self, provider):
        request = _make_request("股價（近 30 日均價）", "down", -5.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日小跌 5%，略有回檔"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_price_down_moderate(self, provider):
        request = _make_request("股價（近 30 日均價）", "down", -25.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日下跌 25%，空頭趨勢明顯"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_price_down_extreme(self, provider):
        request = _make_request("股價（近 30 日均價）", "down", -40.0)
        resp = provider.explain(request)
        assert resp.text == "股價近 30 日大跌 40%，市場信心不足，可能是利空消息或基本面惡化"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0


# ── explain(): 營收年增率 ─────────────────────────────────────

class TestExplainYoy:
    """營收年增率 — thresholds: mild <20%, moderate ≥20%, extreme ≥50%."""

    def test_yoy_up_mild(self, provider):
        request = _make_request("營收年增率", "up", 5.0)
        resp = provider.explain(request)
        assert resp.text == "營收年增 5%，溫和成長"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_yoy_up_moderate(self, provider):
        request = _make_request("營收年增率", "up", 25.0)
        resp = provider.explain(request)
        assert resp.text == "營收年增 25%，穩定成長，公司經營績效良好"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_yoy_up_extreme(self, provider):
        request = _make_request("營收年增率", "up", 60.0)
        resp = provider.explain(request)
        assert resp.text == "營收年增 60%，成長非常強勁，可能是新產品大賣或市場需求爆發"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_yoy_down_mild(self, provider):
        request = _make_request("營收年增率", "down", -5.0)
        resp = provider.explain(request)
        assert resp.text == "營收年減 5%，略有衰退"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_yoy_down_moderate(self, provider):
        request = _make_request("營收年增率", "down", -25.0)
        resp = provider.explain(request)
        assert resp.text == "營收年減 25%，比去年差，需留意原因"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_yoy_down_extreme(self, provider):
        request = _make_request("營收年增率", "down", -60.0)
        resp = provider.explain(request)
        assert resp.text == "營收年減 60%，大幅衰退，可能有結構性問題需要關注"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0


# ── explain(): generic fallback ────────────────────────────────

class TestExplainGeneric:
    """Generic fallback for unknown metric names."""

    def test_generic_up(self, provider):
        request = _make_request("unknown_metric", "up", 15.0)
        resp = provider.explain(request)
        assert resp.text == "unknown_metric 較前期成長 15.0%"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0

    def test_generic_down(self, provider):
        request = _make_request("unknown_metric", "down", -15.0)
        resp = provider.explain(request)
        assert resp.text == "unknown_metric 較前期衰退 15.0%"
        assert resp.source == "delta_template"
        assert resp.confidence == 1.0


# ── explain(): stock_name prefix ───────────────────────────────

class TestExplainStockName:
    """stock_name prefix behavior in explain()."""

    def test_stock_name_prefix_present(self, provider):
        """When stock_name='台積電', prefix should be '台積電 '."""
        request = _make_request("月營收", "up", 35.0, stock_name="台積電")
        resp = provider.explain(request)
        assert resp.text.startswith("台積電 ")
        assert "台積電 月營收成長 35%" in resp.text

    def test_stock_name_empty_no_prefix(self, provider):
        """When stock_name='', no prefix and no leading space."""
        request = _make_request("月營收", "up", 5.0, stock_name="")
        resp = provider.explain(request)
        assert not resp.text.startswith(" ")
        assert resp.text == "月營收成長 5%，溫和成長中"

    def test_stock_name_prefix_generic(self, provider):
        """Generic fallback also gets stock_name prefix."""
        request = _make_request("unknown_metric", "up", 15.0, stock_name="台積電")
        resp = provider.explain(request)
        assert resp.text == "台積電 unknown_metric 較前期成長 15.0%"


# ── _pick_template() boundary values ───────────────────────────

class TestPickTemplateBoundaries:
    """_pick_template() at exact threshold boundaries."""

    # 月營收 thresholds: 50, 30, 0
    def test_revenue_up_exactly_50(self):
        result = _pick_template("月營收", "up", 50.0, "")
        assert "暴增 50%" in result

    def test_revenue_up_exactly_30(self):
        result = _pick_template("月營收", "up", 30.0, "")
        assert "成長 30%" in result
        assert "表現相對正面" in result

    def test_revenue_up_exactly_0(self):
        result = _pick_template("月營收", "up", 0.0, "")
        assert "成長 0%" in result
        assert "溫和成長中" in result

    def test_revenue_down_exactly_50(self):
        result = _pick_template("月營收", "down", 50.0, "")
        assert "驟降 50%" in result
        assert "可留意其趨勢" in result

    def test_revenue_down_exactly_30(self):
        result = _pick_template("月營收", "down", 30.0, "")
        assert "衰退 30%" in result

    def test_revenue_down_exactly_0(self):
        result = _pick_template("月營收", "down", 0.0, "")
        assert "小跌 0%" in result

    # 股價 thresholds: 30, 20, 0
    def test_price_up_exactly_30(self):
        result = _pick_template("股價（近 30 日均價）", "up", 30.0, "")
        assert "大漲 30%" in result

    def test_price_up_exactly_20(self):
        result = _pick_template("股價（近 30 日均價）", "up", 20.0, "")
        assert "上漲 20%" in result
        assert "多頭趨勢明顯" in result

    def test_price_up_exactly_0(self):
        result = _pick_template("股價（近 30 日均價）", "up", 0.0, "")
        assert "上漲 0%" in result
        assert "穩步走揚" in result

    def test_price_down_exactly_30(self):
        result = _pick_template("股價（近 30 日均價）", "down", 30.0, "")
        assert "大跌 30%" in result

    def test_price_down_exactly_20(self):
        result = _pick_template("股價（近 30 日均價）", "down", 20.0, "")
        assert "下跌 20%" in result
        assert "空頭趨勢明顯" in result

    def test_price_down_exactly_0(self):
        result = _pick_template("股價（近 30 日均價）", "down", 0.0, "")
        assert "小跌 0%" in result

    # 營收年增率 thresholds: 50, 20, 0
    def test_yoy_up_exactly_50(self):
        result = _pick_template("營收年增率", "up", 50.0, "")
        assert "年增 50%" in result
        assert "成長非常強勁" in result

    def test_yoy_up_exactly_20(self):
        result = _pick_template("營收年增率", "up", 20.0, "")
        assert "年增 20%" in result
        assert "穩定成長" in result

    def test_yoy_up_exactly_0(self):
        result = _pick_template("營收年增率", "up", 0.0, "")
        assert "年增 0%" in result
        assert "溫和成長" in result

    def test_yoy_down_exactly_50(self):
        result = _pick_template("營收年增率", "down", 50.0, "")
        assert "年減 50%" in result
        assert "大幅衰退" in result

    def test_yoy_down_exactly_20(self):
        result = _pick_template("營收年增率", "down", 20.0, "")
        assert "年減 20%" in result
        assert "比去年差" in result

    def test_yoy_down_exactly_0(self):
        result = _pick_template("營收年增率", "down", 0.0, "")
        assert "年減 0%" in result
        assert "略有衰退" in result


# ── _pick_template() stock_name prefix ─────────────────────────

class TestPickTemplateStockName:
    """_pick_template() stock_name prefix behavior."""

    def test_pick_template_with_stock_name(self):
        result = _pick_template("月營收", "up", 5.0, "台積電")
        assert result.startswith("台積電 ")

    def test_pick_template_without_stock_name(self):
        result = _pick_template("月營收", "up", 5.0, "")
        assert not result.startswith(" ")

    def test_pick_template_generic_with_stock_name(self):
        result = _pick_template("unknown_metric", "up", 10.0, "鴻海")
        assert result.startswith("鴻海 ")
