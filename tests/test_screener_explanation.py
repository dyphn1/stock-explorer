"""
Unit tests for ScreenerExplanationProvider — C167
Tests the historian-tone screener explanation generation.
"""
import pytest

from src.services.screener_explanation_provider import (
    ScreenerExplanationProvider,
    _build_screener_explanation,
    _build_screener_implication,
    _DISCLAIMER,
)
from src.services.llm.base import ExplanationRequest


class TestScreenerExplanationProvider:
    """Tests for the ScreenerExplanationProvider class."""

    def setup_method(self):
        self.provider = ScreenerExplanationProvider()

    def test_is_available_always_true(self):
        """Provider should always be available (no external deps)."""
        assert self.provider.is_available() is True

    def test_explain_returns_screener_template_source(self):
        """Response source should be 'screener_template'."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "dividend",
                "dividend_yield": 5.0,
            },
        )
        response = self.provider.explain(request)
        assert response.source == "screener_template"

    def test_explain_includes_disclaimer(self):
        """All explanations must include the mandatory disclaimer."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "dividend",
                "dividend_yield": 5.0,
            },
        )
        response = self.provider.explain(request)
        assert _DISCLAIMER in response.text

    def test_explain_dividend_preset(self):
        """Dividend preset should produce dividend-specific explanation."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "dividend",
                "dividend_yield": 5.0,
            },
        )
        response = self.provider.explain(request)
        assert "殖利率" in response.text
        assert "5.00%" in response.text

    def test_explain_growth_preset(self):
        """Growth preset should produce growth-specific explanation."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "growth",
                "revenue_yoy": 25.0,
            },
        )
        response = self.provider.explain(request)
        assert "營收年增率" in response.text
        assert "25.0%" in response.text

    def test_explain_value_preset(self):
        """Value preset should produce valuation-specific explanation."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "value",
                "per": 12.0,
                "pbr": 1.3,
            },
        )
        response = self.provider.explain(request)
        assert "本益比" in response.text
        assert "淨值比" in response.text

    def test_explain_custom_filters(self):
        """Custom filters should produce filter-specific explanation."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "filters": {
                    "revenue_growth": True,
                    "industry": "半導體業",
                },
                "revenue_yoy": 15.0,
                "industry": "半導體業",
            },
        )
        response = self.provider.explain(request)
        assert "營收" in response.text or "產業" in response.text

    def test_explain_has_implication(self):
        """Response should include an implication sentence."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "dividend",
                "dividend_yield": 5.0,
            },
        )
        response = self.provider.explain(request)
        assert response.implication != ""
        assert len(response.implication) > 5

    def test_explain_confidence_is_one(self):
        """Template-based provider should have confidence=1.0."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "preset": "dividend",
                "dividend_yield": 5.0,
            },
        )
        response = self.provider.explain(request)
        assert response.confidence == 1.0

    def test_explain_no_preset_no_filters_fallback(self):
        """Without preset or filters, should use fallback template."""
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
            },
        )
        response = self.provider.explain(request)
        assert "台積電" in response.text
        assert "2330" in response.text
        assert _DISCLAIMER in response.text


class TestBuildScreenerExplanation:
    """Tests for the _build_screener_explanation function."""

    def test_dividend_high_yield(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="dividend",
            row={"dividend_yield": 5.0},
        )
        assert "5.00%" in result
        assert _DISCLAIMER in result

    def test_dividend_stable(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="dividend",
            row={"dividend_yield": 3.5},
        )
        assert "3.50%" in result
        assert _DISCLAIMER in result

    def test_growth_strong(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="growth",
            row={"revenue_yoy": 30.0},
        )
        assert "30.0%" in result
        assert _DISCLAIMER in result

    def test_growth_moderate(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="growth",
            row={"revenue_yoy": 12.0},
        )
        assert "12.0%" in result
        assert _DISCLAIMER in result

    def test_value_deep(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="value",
            row={"per": 8.0, "pbr": 1.2},
        )
        assert "8.0" in result
        assert "1.20" in result
        assert _DISCLAIMER in result

    def test_value_moderate(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            preset="value",
            row={"per": 13.0, "pbr": 1.8},
        )
        assert "13.0" in result
        assert "1.80" in result
        assert _DISCLAIMER in result

    def test_custom_revenue_growth(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            filters={"revenue_growth": True},
            row={"revenue_yoy": 15.0},
        )
        assert "15.0%" in result
        assert _DISCLAIMER in result

    def test_custom_industry_match(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
            filters={"industry": "半導體業"},
            row={"industry": "半導體業"},
        )
        assert "半導體業" in result
        assert _DISCLAIMER in result

    def test_fallback_no_data(self):
        result = _build_screener_explanation(
            stock_name="台積電",
            stock_id="2330",
        )
        assert "台積電" in result
        assert "2330" in result
        assert _DISCLAIMER in result

    def test_empty_stock_name(self):
        result = _build_screener_explanation(
            stock_name="",
            stock_id="2330",
            preset="dividend",
            row={"dividend_yield": 4.0},
        )
        assert _DISCLAIMER in result


class TestBuildScreenerImplication:
    """Tests for the _build_screener_implication function."""

    def test_dividend_implication(self):
        result = _build_screener_implication(preset="dividend")
        assert "殖利率" in result or "現金流" in result

    def test_growth_implication(self):
        result = _build_screener_implication(preset="growth")
        assert "營收" in result or "動能" in result

    def test_value_implication(self):
        result = _build_screener_implication(preset="value")
        assert "估值" in result or "低估" in result

    def test_custom_filters_implication(self):
        result = _build_screener_implication(
            filters={"revenue_growth": True, "industry": "半導體業"}
        )
        assert len(result) > 5

    def test_no_preset_no_filters(self):
        result = _build_screener_implication()
        assert "進一步研究" in result


class TestHistorianToneCompliance:
    """Verify that explanations avoid prescriptive language."""

    # Blocked words from the tone blocklist
    BLOCKED_WORDS = [
        "建議", "應該", "買", "賣", "推薦",
        "進場", "出場", "值得關注", "需要密切關注",
    ]

    def _get_all_explanations(self):
        """Generate all possible explanation variants."""
        explanations = []
        provider = ScreenerExplanationProvider()

        # Preset variants
        for preset, ctx in [
            ("dividend", {"dividend_yield": 5.0}),
            ("dividend", {"dividend_yield": 3.5}),
            ("growth", {"revenue_yoy": 30.0}),
            ("growth", {"revenue_yoy": 12.0}),
            ("value", {"per": 8.0, "pbr": 1.2}),
            ("value", {"per": 13.0, "pbr": 1.8}),
        ]:
            request = ExplanationRequest(
                metric_name="screener",
                metric_value="test",
                context={
                    "stock_name": "台積電",
                    "stock_id": "2330",
                    "preset": preset,
                    **ctx,
                },
            )
            response = provider.explain(request)
            explanations.append(response.text)

        # Custom filter variants
        request = ExplanationRequest(
            metric_name="screener",
            metric_value="test",
            context={
                "stock_name": "台積電",
                "stock_id": "2330",
                "filters": {"revenue_growth": True, "industry": "半導體業"},
                "revenue_yoy": 15.0,
                "industry": "半導體業",
            },
        )
        response = provider.explain(request)
        explanations.append(response.text)

        return explanations

    def test_no_blocked_words_in_explanations(self):
        """No explanation template should contain prescriptive/blocked words.

        Note: The mandatory disclaimer "篩選結果僅供學習參考，不構成投資建議"
        contains "建議" — this is a legal requirement (Challenger Condition #6)
        and is excluded from the blocked-word check.
        """
        for text in self._get_all_explanations():
            # Remove the mandatory disclaimer before checking
            template_text = text.replace(f"。{_DISCLAIMER}", "")
            for word in self.BLOCKED_WORDS:
                assert word not in template_text, (
                    f"Blocked word '{word}' found in explanation template: {template_text[:100]}"
                )

    def test_all_explanations_end_with_disclaimer(self):
        """Every explanation must end with the disclaimer."""
        for text in self._get_all_explanations():
            assert _DISCLAIMER in text, (
                f"Missing disclaimer in: {text[:100]}"
            )
