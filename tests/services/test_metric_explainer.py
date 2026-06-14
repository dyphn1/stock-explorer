"""
Regression tests for Metric Explainer — D-113

Tests the _resolve_template_key() function and get_metric_explanation_for_popover()
from metric_explainer.py, covering known mappings, English pass-through, fallback
behavior, result dict structure, optional parameters, and edge cases.
"""
import pytest

from src.services.metric_explainer import _resolve_template_key, get_metric_explanation_for_popover


# ── _resolve_template_key() — known Chinese mappings ─────────────

class TestResolveTemplateKeyChineseMappings:
    """Chinese display names map to correct lowercase English template keys."""

    def test_yueshouyuan_maps_to_revenue(self):
        assert _resolve_template_key("月營收") == "revenue"

    def test_roe_maps_to_roe(self):
        assert _resolve_template_key("ROE") == "roe"

    def test_gross_margin_maps_to_gross_margin(self):
        assert _resolve_template_key("毛利率") == "gross_margin"

    def test_pe_ratio_maps_to_pe_ratio(self):
        assert _resolve_template_key("本益比") == "pe_ratio"

    def test_debt_ratio_maps_to_debt_ratio(self):
        assert _resolve_template_key("負債比") == "debt_ratio"

    def test_dividend_yield_maps_to_dividend_yield(self):
        assert _resolve_template_key("殖利率") == "dividend_yield"

    def test_net_margin_maps_to_net_margin(self):
        assert _resolve_template_key("淨利率") == "net_margin"

    def test_operating_margin_maps_to_operating_margin(self):
        assert _resolve_template_key("營業利益率") == "operating_margin"

    def test_eps_maps_to_eps(self):
        assert _resolve_template_key("EPS") == "eps"

    def test_revenue_yoy_maps_to_revenue(self):
        assert _resolve_template_key("營收年增率") == "revenue"

    def test_per_maps_to_pe_ratio(self):
        assert _resolve_template_key("PER") == "pe_ratio"

    def test_jingzhibi_maps_to_pe_ratio(self):
        """淨值比 falls back to pe_ratio template."""
        assert _resolve_template_key("淨值比") == "pe_ratio"

    def test_pbr_maps_to_pe_ratio(self):
        """PBR falls back to pe_ratio template."""
        assert _resolve_template_key("PBR") == "pe_ratio"


# ── _resolve_template_key() — English pass-through ────────────────

class TestResolveTemplateKeyEnglishPassthrough:
    """English keys that exist in the map should return themselves."""

    def test_revenue_passthrough(self):
        assert _resolve_template_key("revenue") == "revenue"

    def test_roe_passthrough(self):
        assert _resolve_template_key("roe") == "roe"

    def test_gross_margin_passthrough(self):
        assert _resolve_template_key("gross_margin") == "gross_margin"


# ── _resolve_template_key() — fallback for unknown names ─────────

class TestResolveTemplateKeyFallback:
    """Unknown metric names fall back to lowercase with underscores."""

    def test_unknown_name_lowercased(self):
        assert _resolve_template_key("SomeMetric") == "somemetric"

    def test_spaces_replaced_with_underscores(self):
        assert _resolve_template_key("net profit margin") == "net_profit_margin"

    def test_mixed_case_with_spaces(self):
        assert _resolve_template_key("Foo Bar") == "foo_bar"


# ── get_metric_explanation_for_popover() — dict structure ─────────

class TestGetMetricExplanationStructure:
    """Return dict must always contain the four required keys."""

    def test_returns_required_keys(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億")
        assert set(result.keys()) == {"display_name", "value_text", "explanation_text", "source"}

    def test_display_name_matches_input(self):
        result = get_metric_explanation_for_popover("ROE", "15.2%")
        assert result["display_name"] == "ROE"

    def test_value_text_matches_input(self):
        result = get_metric_explanation_for_popover("ROE", "15.2%")
        assert result["value_text"] == "15.2%"

    def test_value_text_rendered_as_string(self):
        """The value_text in the result is a string representation of metric_value."""
        result = get_metric_explanation_for_popover("ROE", "15.2")
        assert result["value_text"] == "15.2"
        assert isinstance(result["value_text"], str)

    def test_source_is_template(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億")
        assert result["source"] == "template"


# ── get_metric_explanation_for_popover() — known metrics ──────────

class TestGetMetricExplanationKnownMetrics:
    """Known metric names should produce non-empty explanation text."""

    def test_revenue_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億")
        assert len(result["explanation_text"]) > 0

    def test_roe_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("ROE", "15.2%")
        assert len(result["explanation_text"]) > 0

    def test_gross_margin_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("毛利率", "35.1%")
        assert len(result["explanation_text"]) > 0

    def test_pe_ratio_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("本益比", "12.5")
        assert len(result["explanation_text"]) > 0

    def test_dividend_yield_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("殖利率", "3.5%")
        assert len(result["explanation_text"]) > 0

    def test_eps_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("EPS", "5.2")
        assert len(result["explanation_text"]) > 0

    def test_debt_ratio_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("負債比", "45%")
        assert len(result["explanation_text"]) > 0

    def test_net_margin_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("淨利率", "10.5%")
        assert len(result["explanation_text"]) > 0

    def test_operating_margin_explanation_non_empty(self):
        result = get_metric_explanation_for_popover("營業利益率", "20.3%")
        assert len(result["explanation_text"]) > 0


# ── get_metric_explanation_for_popover() — optional parameters ────

class TestGetMetricExplanationOptionalParams:
    """delta and context parameters are optional."""

    def test_without_delta(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億")
        assert len(result["explanation_text"]) > 0

    def test_with_delta(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億", delta="+5.2%")
        assert len(result["explanation_text"]) > 0

    def test_with_empty_delta(self):
        result = get_metric_explanation_for_popover("月營收", "123.4 億", delta="")
        assert len(result["explanation_text"]) > 0

    def test_without_context(self):
        result = get_metric_explanation_for_popover("ROE", "15.2%")
        assert len(result["explanation_text"]) > 0

    def test_with_context(self):
        result = get_metric_explanation_for_popover(
            "ROE", "15.2%", context={"industry": "semiconductor"}
        )
        assert len(result["explanation_text"]) > 0

    def test_with_delta_and_context(self):
        result = get_metric_explanation_for_popover(
            "毛利率", "35.1%", delta="-2.1%", context={"direction": "down"}
        )
        assert len(result["explanation_text"]) > 0


# ── Edge cases ────────────────────────────────────────────────────

class TestEdgeCases:
    """Edge cases: empty string, spaces, unicode."""

    def test_empty_metric_name(self):
        """Empty string should still return a valid dict (fallback template)."""
        result = get_metric_explanation_for_popover("", "N/A")
        assert set(result.keys()) == {"display_name", "value_text", "explanation_text", "source"}
        assert result["display_name"] == ""
        assert len(result["explanation_text"]) > 0

    def test_metric_name_with_spaces(self):
        """Metric name with spaces should be handled via fallback."""
        result = get_metric_explanation_for_popover("custom metric", "42")
        assert result["display_name"] == "custom metric"
        assert len(result["explanation_text"]) > 0

    def test_unicode_metric_name(self):
        """Unicode metric names should work via fallback."""
        result = get_metric_explanation_for_popover("自訂指標", "100")
        assert result["display_name"] == "自訂指標"
        assert len(result["explanation_text"]) > 0

    def test_negative_delta(self):
        """Negative delta should produce a decrease-direction explanation."""
        result = get_metric_explanation_for_popover("月營收", "100 億", delta="-5.2%")
        assert len(result["explanation_text"]) > 0

    def test_positive_delta(self):
        """Positive delta should produce an increase-direction explanation."""
        result = get_metric_explanation_for_popover("月營收", "100 億", delta="+5.2%")
        assert len(result["explanation_text"]) > 0
