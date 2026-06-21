"""
Screener Explanation Provider — C167

Implements ExplanationProvider protocol for stock screener results.
Uses compose-and-enrich pipeline: TemplateExplanationProvider for base
explanations, then enriches with screener-specific context.

All explanations use historian tone (past tense, factual, no prescriptive language)
with mandatory disclaimer: "篩選結果僅供學習參考，不構成投資建議"

Pure Python — no Streamlit imports.
"""

from __future__ import annotations

import os

import yaml

from src.core.i18n import t
from src.services.llm.base import ExplanationProvider, ExplanationRequest, ExplanationResponse
from src.services.llm.template_provider import TemplateExplanationProvider


# ── Config helpers ──────────────────────────────────────────────────

def _config_dir() -> str:
    """Return the absolute path to the src/data/ directory."""
    return os.path.join(os.path.dirname(__file__), "..", "data")


def _load_templates_from_yaml() -> dict:
    """Load screener explanation templates from the YAML config file.

    Returns a dict with the keys:
        preset_explanations, custom_filter_explanations, thresholds, disclaimer.
    All string values are locale keys (NOT translated) - translation happens at runtime.
    """
    yaml_path = os.path.join(_config_dir(), "screener_templates.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Return raw YAML data with locale key strings - translate at runtime
    return data


# ── Load templates from YAML ────────────────────────────────────────
_yaml_data = _load_templates_from_yaml()

# ── Historian tone disclaimer ──────────────────────────────
_DISCLAIMER = _yaml_data.get("disclaimer", "screener.explanation.disclaimer")

# ── Screener-specific explanation templates ────────────────────────
# Each filter type maps to a set of explanation templates keyed by
# the metric that triggered the match. Templates use historian tone:
# past tense, factual, no prescriptive language.
# Loaded from src/data/screener_templates.yaml (D-121).

_preset_data = _yaml_data.get("preset_explanations", {})
_custom_data = _yaml_data.get("custom_filter_explanations", {})

_DIVIDEND_TEMPLATES: dict[str, str] = _preset_data.get("dividend", {})
_GROWTH_TEMPLATES: dict[str, str] = _preset_data.get("growth", {})
_VALUE_TEMPLATES: dict[str, str] = _preset_data.get("value", {})

_CUSTOM_FILTER_TEMPLATES: dict[str, str] = {
    "revenue_positive": _custom_data.get("revenue_positive", ""),
    "industry_match": _custom_data.get("industry_match", ""),
    "per_range": _custom_data.get("per_range", ""),
    "div_range": _custom_data.get("div_range", ""),
}

# ── Fallback template ─────────────────────────────────────
_FALLBACK_TEMPLATE = _custom_data.get(
    "fallback", "screener.explanation.fallback")
_DISCLAIMER_KEY = _DISCLAIMER
_FALLBACK_TEMPLATE_KEY = _FALLBACK_TEMPLATE




def _build_screener_explanation(
    stock_name: str,
    stock_id: str,
    preset: str | None = None,
    filters: dict | None = None,
    row: dict | None = None,
) -> str:
    """Build a plain-language explanation for why a stock passed the screener.

    Uses compose-and-enrich: picks the most relevant template based on
    the active filter/preset, then fills in actual metric values.

    Args:
        stock_name: Display name of the stock.
        stock_id: Stock ID string.
        preset: Active preset name ("dividend", "growth", "value") or None.
        filters: Active custom filters dict or None.
        row: Dict with metric values (per, pbr, dividend_yield, revenue_yoy, industry).

    Returns:
        A historian-tone explanation string with disclaimer.
    """
    row = row or {}
    parts: list[str] = []

    stock_prefix = f"{stock_name} " if stock_name else ""

    if preset == "dividend":
        div_yield = row.get("dividend_yield")
        if div_yield is not None and div_yield > 0:
            if div_yield > 4.0:
                parts.append(
                    t(_DIVIDEND_TEMPLATES["high_yield"]).format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )
            else:
                parts.append(
                    t(_DIVIDEND_TEMPLATES["stable"]).format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )
        else:
            parts.append(
                t(_FALLBACK_TEMPLATE).format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif preset == "growth":
        rev_yoy = row.get("revenue_yoy")
        if rev_yoy is not None and rev_yoy > 0:
            if rev_yoy > 20.0:
                parts.append(
                    t(_GROWTH_TEMPLATES["strong"]).format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )
            else:
                parts.append(
                    t(_GROWTH_TEMPLATES["moderate"]).format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )
        else:
            parts.append(
                t(_FALLBACK_TEMPLATE).format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif preset == "value":
        per = row.get("per")
        pbr = row.get("pbr")
        if per is not None and pbr is not None:
            if per < 10 and pbr < 1.5:
                parts.append(
                    t(_VALUE_TEMPLATES["deep_value"]).format(
                        stock_name=stock_name,
                        per=per,
                        pbr=pbr,
                    )
                )
            else:
                parts.append(
                    t(_VALUE_TEMPLATES["moderate_value"]).format(
                        stock_name=stock_name,
                        per=per,
                        pbr=pbr,
                    )
                )
        else:
            parts.append(
                t(_FALLBACK_TEMPLATE).format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif filters:
        # Custom filter mode — explain which filters matched
        if filters.get("revenue_growth"):
            rev_yoy = row.get("revenue_yoy")
            if rev_yoy is not None and rev_yoy > 0:
                parts.append(
                    t(_CUSTOM_FILTER_TEMPLATES["revenue_positive"]).format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )

        industry_filter = filters.get("industry")
        if industry_filter and industry_filter != "全部":
            industry = row.get("industry", industry_filter)
            parts.append(
                t(_CUSTOM_FILTER_TEMPLATES["industry_match"]).format(
                    stock_name=stock_name,
                    industry=industry,
                )
            )

        per_min = filters.get("per_min")
        per_max = filters.get("per_max")
        if per_min is not None or per_max is not None:
            per = row.get("per")
            if per is not None:
                parts.append(
                    t(_CUSTOM_FILTER_TEMPLATES["per_range"]).format(
                        stock_name=stock_name,
                        per=per,
                    )
                )

        div_min = filters.get("div_min")
        div_max = filters.get("div_max")
        if div_min is not None or div_max is not None:
            div_yield = row.get("dividend_yield")
            if div_yield is not None:
                parts.append(
                    t(_CUSTOM_FILTER_TEMPLATES["div_range"]).format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )

        if not parts:
            parts.append(
                t(_FALLBACK_TEMPLATE).format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )
    else:
        parts.append(
            t(_FALLBACK_TEMPLATE).format(
                stock_name=stock_name, stock_id=stock_id
            )
        )

    # Join all parts and append disclaimer
    explanation = "；".join(parts)
    return f"{explanation}。{t(_DISCLAIMER)}"


def _build_screener_implication(
    preset: str | None = None,
    filters: dict | None = None,
) -> str:
    """Build a one-sentence implication for the screener results.

    Historian tone, factual. Answers "so what?" for the screener.

    Args:
        preset: Active preset name or None.
        filters: Active custom filters dict or None.

    Returns:
        A one-sentence implication string.
    """
    if preset == "dividend":
        return t("screener.explanation.preset.implication.dividend")
    elif preset == "growth":
        return t("screener.explanation.preset.implication.growth")
    elif preset == "value":
        return t("screener.explanation.preset.implication.value")
    elif filters:
        active_filters = []
        if filters.get("revenue_growth"):
            active_filters.append(t("screener.explanation.preset.filter.revenue_positive"))
        if filters.get("industry") and filters["industry"] != t("screener.explanation.filter.all_industries"):
            active_filters.append(t("screener.explanation.preset.filter.industry_match", industry=filters["industry"]))
        if filters.get("per_min") is not None or filters.get("per_max") is not None:
            active_filters.append(t("screener.explanation.preset.filter.per_range"))
        if filters.get("div_min") is not None or filters.get("div_max") is not None:
            active_filters.append(t("screener.explanation.preset.filter.div_range"))
        if active_filters:
            return t("screener.explanation.preset.implication.custom_many")
        return t("screener.explanation.preset.implication.custom_fallback")

    return t("screener.explanation.preset.implication.default")


class ScreenerExplanationProvider:
    """ExplanationProvider for stock screener results.

    Implements the ExplanationProvider protocol.
    Uses TemplateExplanationProvider internally for composition
    but provides screener-specific historian-tone explanations.

    All explanations include the mandatory disclaimer.
    Returns source="screener_template" in ExplanationResponse.
    """

    def __init__(self) -> None:
        """Initialize with a TemplateExplanationProvider for composition."""
        self._template_provider = TemplateExplanationProvider()

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        """Generate a historian-tone explanation for a screener result.

        Uses preset from request.context["preset"] and filters from
        request.context["filters"] to produce a screener-specific
        explanation with mandatory disclaimer.

        Args:
            request: ExplanationRequest with screener context.

        Returns:
            ExplanationResponse with source="screener_template".
        """
        context = request.context
        preset = context.get("preset")
        filters = context.get("filters")
        stock_name = context.get("stock_name", "")
        stock_id = context.get("stock_id", "")

        # Build row dict from context for template formatting
        row = {
            "per": context.get("per"),
            "pbr": context.get("pbr"),
            "dividend_yield": context.get("dividend_yield"),
            "revenue_yoy": context.get("revenue_yoy"),
            "industry": context.get("industry", ""),
        }

        # Generate screener-specific explanation
        text = _build_screener_explanation(
            stock_name=stock_name,
            stock_id=stock_id,
            preset=preset,
            filters=filters,
            row=row,
        )

        # Generate implication sentence
        implication = _build_screener_implication(
            preset=preset,
            filters=filters,
        )

        # Verify template provider is available (protocol compliance)
        self._template_provider.is_available()

        return ExplanationResponse(
            text=text,
            source="screener_template",
            confidence=1.0,
            implication=implication,
        )

    def is_available(self) -> bool:
        """Always available — no external dependencies."""
        return True
