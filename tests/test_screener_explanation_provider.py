"""
Unit tests for ScreenerExplanationProvider — D-124

Tests the ScreenerExplanationProvider class from
src/services/screener_explanation_provider.py, covering:
- Instantiation and protocol compliance
- Historian tone (no prescriptive language)
- Mandatory disclaimer presence
- All explanation paths (dividend, growth, value, custom, fallback)
- TemplateExplanationProvider integration
"""
import pytest
from unittest.mock import patch, MagicMock

from src.services.screener_explanation_provider import (
    ScreenerExplanationProvider,
    _build_screener_explanation,
    _build_screener_implication,
    _DISCLAIMER,
)
from src.services.llm.base import ExplanationRequest, ExplanationResponse
from src.core.i18n import t


# ── Fixtures ────────────────────────────────────────────────────


@pytest.fixture
def provider():
    """Create a fresh ScreenerExplanationProvider instance."""
    return ScreenerExplanationProvider()


def _ctx(preset=None, filters=None, stock_name="台積電", stock_id="2330", **extra):
    """Build a context dict for ExplanationRequest."""
    d = {"stock_name": stock_name, "stock_id": stock_id}
    if preset:
        d["preset"] = preset
    if filters:
        d["filters"] = filters
    d.update(extra)
    return d


def _req(preset=None, filters=None, *, stock_name="台積電", stock_id="2330", **extra):
    """Build an ExplanationRequest with screener context."""
    return ExplanationRequest(
        metric_name="screener",
        metric_value="test",
        context=_ctx(preset=preset, filters=filters, stock_name=stock_name, stock_id=stock_id, **extra),
    )


# ── Part 1: Instantiation ──────────────────────────────────────


class TestScreenerExplanationProviderInstantiation:
    """Test that ScreenerExplanationProvider exists and can be instantiated."""

    def test_class_exists(self):
        """ScreenerExplanationProvider should be importable and instantiable."""
        assert ScreenerExplanationProvider is not None
        provider = ScreenerExplanationProvider()
        assert isinstance(provider, ScreenerExplanationProvider)

    def test_has_explain_method(self):
        """Provider must have an explain() method."""
        provider = ScreenerExplanationProvider()
        assert hasattr(provider, "explain")
        assert callable(provider.explain)

    def test_has_is_available_method(self):
        """Provider must have an is_available() method."""
        provider = ScreenerExplanationProvider()
        assert hasattr(provider, "is_available")
        assert callable(provider.is_available)

    def test_is_available_returns_true(self):
        """Provider should always be available (no external deps)."""
        provider = ScreenerExplanationProvider()
        assert provider.is_available() is True

    def test_uses_template_provider_internally(self):
        """Provider should compose with TemplateExplanationProvider."""
        from src.services.llm.template_provider import TemplateExplanationProvider

        provider = ScreenerExplanationProvider()
        assert hasattr(provider, "_template_provider")
        assert isinstance(provider._template_provider, TemplateExplanationProvider)


# ── Part 2: Historian Tone ─────────────────────────────────────


class TestHistorianTone:
    """Verify explanations use historian tone (no prescriptive language)."""

    BLOCKED_WORDS = ["建議", "應該", "買", "賣", "推薦", "進場", "出場"]

    def _get_all_explanation_texts(self):
        """Generate all explanation variants from the provider."""
        provider = ScreenerExplanationProvider()
        texts = []

        for preset, extra in [
            ("dividend", {"dividend_yield": 5.0}),
            ("dividend", {"dividend_yield": 3.5}),
            ("growth", {"revenue_yoy": 30.0}),
            ("growth", {"revenue_yoy": 12.0}),
            ("value", {"per": 8.0, "pbr": 1.2}),
            ("value", {"per": 13.0, "pbr": 1.8}),
        ]:
            resp = provider.explain(_req(preset=preset, **extra))
            texts.append(resp.text)

        resp = provider.explain(_req(
            filters={"revenue_growth": True, "industry": "半導體業"},
            revenue_yoy=15.0,
            industry="半導體業",
        ))
        texts.append(resp.text)

        resp = provider.explain(_req())
        texts.append(resp.text)
        return texts

    def test_no_blocked_words_in_explanations(self):
        """No explanation template should contain prescriptive/blocked words.

        Note: The mandatory disclaimer contains "建議" as part of
        "不構成投資建議" — this is a legal requirement and is excluded.
        """
        for text in self._get_all_explanation_texts():
            template_text = text.replace(f"。{t(_DISCLAIMER)}", "")
            for word in self.BLOCKED_WORDS:
                assert word not in template_text, (
                    f"Blocked word '{word}' found in: {template_text[:100]}"
                )

    def test_explanations_are_strings(self):
        """All explanations should be non-empty strings."""
        provider = ScreenerExplanationProvider()
        for preset in ["dividend", "growth", "value"]:
            extra = {"dividend_yield": 5.0, "revenue_yoy": 20.0, "per": 12.0, "pbr": 1.5}
            resp = provider.explain(_req(preset=preset, **extra))
            assert isinstance(resp.text, str)
            assert len(resp.text) > 0


# ── Part 3: Disclaimer ─────────────────────────────────────────


class TestDisclaimer:
    """Verify that '僅供學習參考' appears in all explanations."""

    def test_disclaimer_in_dividend_explanation(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert "僅供學習參考" in resp.text

    def test_disclaimer_in_growth_explanation(self, provider):
        resp = provider.explain(_req(preset="growth", revenue_yoy=25.0))
        assert "僅供學習參考" in resp.text

    def test_disclaimer_in_value_explanation(self, provider):
        resp = provider.explain(_req(preset="value", per=12.0, pbr=1.5))
        assert "僅供學習參考" in resp.text

    def test_disclaimer_in_custom_filter_explanation(self, provider):
        resp = provider.explain(_req(filters={"revenue_growth": True}, revenue_yoy=15.0))
        assert "僅供學習參考" in resp.text

    def test_disclaimer_in_fallback_explanation(self, provider):
        resp = provider.explain(_req())
        assert "僅供學習參考" in resp.text

    def test_disclaimer_constant_value(self):
        """The disclaimer constant should contain the expected text."""
        assert "僅供學習參考" in t(_DISCLAIMER)


# ── Part 4: Explanation Paths ──────────────────────────────────


class TestDividendExplanationPath:
    """Test dividend preset explanation paths."""

    def test_dividend_high_yield(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert "殖利率" in resp.text
        assert "5.00%" in resp.text
        assert resp.source == "screener_template"

    def test_dividend_stable(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=3.5))
        assert "殖利率" in resp.text
        assert "3.50%" in resp.text

    def test_dividend_no_yield_data_fallback(self, provider):
        resp = provider.explain(_req(preset="dividend"))
        assert "台積電" in resp.text
        assert "2330" in resp.text


class TestGrowthExplanationPath:
    """Test growth preset explanation paths."""

    def test_growth_strong(self, provider):
        resp = provider.explain(_req(preset="growth", revenue_yoy=30.0))
        assert "營收年增率" in resp.text
        assert "30.0%" in resp.text
        assert resp.source == "screener_template"

    def test_growth_moderate(self, provider):
        resp = provider.explain(_req(preset="growth", revenue_yoy=12.0))
        assert "營收年增率" in resp.text
        assert "12.0%" in resp.text

    def test_growth_no_revenue_data_fallback(self, provider):
        resp = provider.explain(_req(preset="growth"))
        assert "台積電" in resp.text


class TestValueExplanationPath:
    """Test value preset explanation paths."""

    def test_value_deep(self, provider):
        resp = provider.explain(_req(preset="value", per=8.0, pbr=1.2))
        assert "本益比" in resp.text
        assert "淨值比" in resp.text
        assert "8.0" in resp.text
        assert "1.20" in resp.text
        assert resp.source == "screener_template"

    def test_value_moderate(self, provider):
        resp = provider.explain(_req(preset="value", per=13.0, pbr=1.8))
        assert "本益比" in resp.text
        assert "13.0" in resp.text
        assert "1.80" in resp.text

    def test_value_no_data_fallback(self, provider):
        resp = provider.explain(_req(preset="value"))
        assert "台積電" in resp.text


class TestCustomFilterExplanationPath:
    """Test custom filter explanation paths."""

    def test_custom_revenue_growth(self, provider):
        resp = provider.explain(_req(filters={"revenue_growth": True}, revenue_yoy=15.0))
        assert "營收" in resp.text
        assert "15.0%" in resp.text

    def test_custom_industry_match(self, provider):
        resp = provider.explain(_req(filters={"industry": "半導體業"}, industry="半導體業"))
        assert "半導體業" in resp.text

    def test_custom_per_range(self, provider):
        resp = provider.explain(_req(filters={"per_min": 5, "per_max": 20}, per=12.0))
        assert "本益比" in resp.text

    def test_custom_div_range(self, provider):
        resp = provider.explain(_req(filters={"div_min": 2.0, "div_max": 8.0}, dividend_yield=5.0))
        assert "殖利率" in resp.text

    def test_custom_no_matching_filters_fallback(self, provider):
        resp = provider.explain(_req(filters={"revenue_growth": True}))
        assert "台積電" in resp.text
        assert "2330" in resp.text


class TestFallbackExplanationPath:
    """Test fallback when no preset or filters are set."""

    def test_no_preset_no_filters(self, provider):
        resp = provider.explain(_req())
        assert "台積電" in resp.text
        assert "2330" in resp.text
        assert t(_DISCLAIMER) in resp.text


# ── Part 5: Response Structure ─────────────────────────────────


class TestResponseStructure:
    """Test that ExplanationResponse has correct structure."""

    def test_response_has_text(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert isinstance(resp.text, str)
        assert len(resp.text) > 0

    def test_response_source_is_screener_template(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert resp.source == "screener_template"

    def test_response_confidence_is_one(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert resp.confidence == 1.0

    def test_response_has_implication(self, provider):
        resp = provider.explain(_req(preset="dividend", dividend_yield=5.0))
        assert resp.implication is not None
        assert len(resp.implication) > 5

    def test_implication_varies_by_preset(self, provider):
        imp_d = provider.explain(_req(preset="dividend", dividend_yield=5.0)).implication
        imp_g = provider.explain(_req(preset="growth", revenue_yoy=25.0)).implication
        imp_v = provider.explain(_req(preset="value", per=12.0, pbr=1.5)).implication
        assert imp_d != imp_g or imp_g != imp_v


# ── Part 6: Mock TemplateExplanationProvider ───────────────────


class TestTemplateProviderIntegration:
    """Test that ScreenerExplanationProvider uses TemplateExplanationProvider."""

    def test_template_provider_is_available_called(self):
        """explain() should call is_available() on the template provider."""
        provider = ScreenerExplanationProvider()
        provider._template_provider = MagicMock()
        provider._template_provider.is_available.return_value = True

        req = _req(preset="dividend", dividend_yield=5.0)
        provider.explain(req)

        provider._template_provider.is_available.assert_called_once()

    def test_explain_works_with_mocked_template_provider(self):
        """ScreenerExplanationProvider should work even with a mocked template provider."""
        provider = ScreenerExplanationProvider()
        provider._template_provider = MagicMock()
        provider._template_provider.is_available.return_value = True

        resp = provider.explain(_req(preset="growth", revenue_yoy=25.0))
        assert resp.source == "screener_template"
        assert "營收年增率" in resp.text
        assert t(_DISCLAIMER) in resp.text


# ── Part 7: _build_screener_explanation function ───────────────


class TestBuildScreenerExplanation:
    """Direct tests for the _build_screener_explanation function."""

    def test_dividend_high_yield(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="dividend", row={"dividend_yield": 5.0},
        )
        assert "5.00%" in result
        assert t(_DISCLAIMER) in result

    def test_dividend_stable(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="dividend", row={"dividend_yield": 3.5},
        )
        assert "3.50%" in result
        assert t(_DISCLAIMER) in result

    def test_growth_strong(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="growth", row={"revenue_yoy": 30.0},
        )
        assert "30.0%" in result
        assert t(_DISCLAIMER) in result

    def test_growth_moderate(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="growth", row={"revenue_yoy": 12.0},
        )
        assert "12.0%" in result
        assert t(_DISCLAIMER) in result

    def test_value_deep(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="value", row={"per": 8.0, "pbr": 1.2},
        )
        assert "8.0" in result
        assert "1.20" in result
        assert t(_DISCLAIMER) in result

    def test_value_moderate(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            preset="value", row={"per": 13.0, "pbr": 1.8},
        )
        assert "13.0" in result
        assert "1.80" in result
        assert t(_DISCLAIMER) in result

    def test_custom_revenue_growth(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            filters={"revenue_growth": True}, row={"revenue_yoy": 15.0},
        )
        assert "15.0%" in result
        assert t(_DISCLAIMER) in result

    def test_custom_industry_match(self):
        result = _build_screener_explanation(
            stock_name="台積電", stock_id="2330",
            filters={"industry": "半導體業"}, row={"industry": "半導體業"},
        )
        assert "半導體業" in result
        assert t(_DISCLAIMER) in result

    def test_fallback_no_data(self):
        result = _build_screener_explanation(stock_name="台積電", stock_id="2330")
        assert "台積電" in result
        assert "2330" in result
        assert t(_DISCLAIMER) in result

    def test_empty_stock_name(self):
        result = _build_screener_explanation(
            stock_name="", stock_id="2330",
            preset="dividend", row={"dividend_yield": 4.0},
        )
        assert t(_DISCLAIMER) in result


# ── Part 8: _build_screener_implication function ───────────────


class TestBuildScreenerImplication:
    """Direct tests for the _build_screener_implication function."""

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
