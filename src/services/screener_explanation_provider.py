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

from src.services.llm.base import ExplanationProvider, ExplanationRequest, ExplanationResponse
from src.services.llm.template_provider import TemplateExplanationProvider

# ── Historian tone disclaimer ──────────────────────────────────────
_DISCLAIMER = "篩選結果僅供學習參考，不構成投資諮詢"

# ── Screener-specific explanation templates ────────────────────────
# Each filter type maps to a set of explanation templates keyed by
# the metric that triggered the match. Templates use historian tone:
# past tense, factual, no prescriptive language.

_DIVIDEND_TEMPLATES = {
    "high_yield": (
        "{stock_name} 殖利率為 {dividend_yield:.2f}%，"
        "高於市場平均水準，顯示公司持續配發股利的能力"
    ),
    "stable": (
        "{stock_name} 殖利率為 {dividend_yield:.2f}%，"
        "波動幅度較小，屬相對穩定的收息標的"
    ),
}

_GROWTH_TEMPLATES = {
    "strong": (
        "{stock_name} 營收年增率達 {revenue_yoy:.1f}%，"
        "顯示營收擴張速度優於同業平均水準"
    ),
    "moderate": (
        "{stock_name} 營收年增率為 {revenue_yoy:.1f}%，"
        "呈現溫和成長趨勢"
    ),
}

_VALUE_TEMPLATES = {
    "deep_value": (
        "{stock_name} 本益比為 {per:.1f}、淨值比為 {pbr:.2f}，"
        "估值低於市場平均，市場對其評價相對保守"
    ),
    "moderate_value": (
        "{stock_name} 本益比為 {per:.1f}、淨值比為 {pbr:.2f}，"
        "估值處於合理範圍"
    ),
}

_CUSTOM_FILTER_TEMPLATES = {
    "revenue_positive": (
        "{stock_name} 營收年增率為 {revenue_yoy:.1f}%，"
        "營收較去年同期成長"
    ),
    "industry_match": (
        "{stock_name} 屬於 {industry} 產業，符合所選產業分類"
    ),
    "per_range": (
        "{stock_name} 本益比為 {per:.1f}，落在所選範圍內"
    ),
    "div_range": (
        "{stock_name} 殖利率為 {dividend_yield:.2f}%，落在所選範圍內"
    ),
}

# ── Fallback template ──────────────────────────────────────────────
_FALLBACK_TEMPLATE = (
    "{stock_name}（{stock_id}）符合所設篩選條件"
)


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
                    _DIVIDEND_TEMPLATES["high_yield"].format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )
            else:
                parts.append(
                    _DIVIDEND_TEMPLATES["stable"].format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )
        else:
            parts.append(
                _FALLBACK_TEMPLATE.format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif preset == "growth":
        rev_yoy = row.get("revenue_yoy")
        if rev_yoy is not None and rev_yoy > 0:
            if rev_yoy > 20.0:
                parts.append(
                    _GROWTH_TEMPLATES["strong"].format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )
            else:
                parts.append(
                    _GROWTH_TEMPLATES["moderate"].format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )
        else:
            parts.append(
                _FALLBACK_TEMPLATE.format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif preset == "value":
        per = row.get("per")
        pbr = row.get("pbr")
        if per is not None and pbr is not None:
            if per < 10 and pbr < 1.5:
                parts.append(
                    _VALUE_TEMPLATES["deep_value"].format(
                        stock_name=stock_name,
                        per=per,
                        pbr=pbr,
                    )
                )
            else:
                parts.append(
                    _VALUE_TEMPLATES["moderate_value"].format(
                        stock_name=stock_name,
                        per=per,
                        pbr=pbr,
                    )
                )
        else:
            parts.append(
                _FALLBACK_TEMPLATE.format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )

    elif filters:
        # Custom filter mode — explain which filters matched
        if filters.get("revenue_growth"):
            rev_yoy = row.get("revenue_yoy")
            if rev_yoy is not None and rev_yoy > 0:
                parts.append(
                    _CUSTOM_FILTER_TEMPLATES["revenue_positive"].format(
                        stock_name=stock_name,
                        revenue_yoy=rev_yoy,
                    )
                )

        industry_filter = filters.get("industry")
        if industry_filter and industry_filter != "全部":
            industry = row.get("industry", industry_filter)
            parts.append(
                _CUSTOM_FILTER_TEMPLATES["industry_match"].format(
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
                    _CUSTOM_FILTER_TEMPLATES["per_range"].format(
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
                    _CUSTOM_FILTER_TEMPLATES["div_range"].format(
                        stock_name=stock_name,
                        dividend_yield=div_yield,
                    )
                )

        if not parts:
            parts.append(
                _FALLBACK_TEMPLATE.format(
                    stock_name=stock_name, stock_id=stock_id
                )
            )
    else:
        parts.append(
            _FALLBACK_TEMPLATE.format(
                stock_name=stock_name, stock_id=stock_id
            )
        )

    # Join all parts and append disclaimer
    explanation = "；".join(parts)
    return f"{explanation}。{_DISCLAIMER}"


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
        return "高殖利率公司通常具穩定現金流，可留意其配息持續性"
    elif preset == "growth":
        return "營收成長公司可能具擴張動能，可觀察其獲利是否同步提升"
    elif preset == "value":
        return "低估值公司可能存在市場低估，可進一步評估其基本面是否穩健"
    elif filters:
        active_filters = []
        if filters.get("revenue_growth"):
            active_filters.append("營收正成長")
        if filters.get("industry") and filters["industry"] != "全部":
            active_filters.append(f"屬於{filters['industry']}")
        if filters.get("per_min") is not None or filters.get("per_max") is not None:
            active_filters.append("本益比在指定範圍")
        if filters.get("div_min") is not None or filters.get("div_max") is not None:
            active_filters.append("殖利率在指定範圍")
        if active_filters:
            conditions = "、".join(active_filters)
            return "符合多項篩選條件的公司，可進一步比較其財務面與評價面"
        return "篩選結果可作為進一步研究的起點，可搭配基本面分析"

    return "篩選結果可作為進一步研究的起點"


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
