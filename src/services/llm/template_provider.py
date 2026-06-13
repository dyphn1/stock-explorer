"""
Template-based Explanation Provider — D5

A fallback implementation of ExplanationProvider that uses
predefined templates for common financial metrics.
No LLM API calls — pure Python string formatting.
"""

from __future__ import annotations

from src.services.llm.base import ExplanationProvider, ExplanationRequest, ExplanationResponse

# ── Templates ──────────────────────────────────────────────────
# Template keys (after the metric name) are matched by direction:
#   "increase"  — delta is positive or metric context indicates growth
#   "decrease"  — delta is negative or metric context indicates decline
#   "neutral"   — no significant change

TEMPLATES: dict[str, dict[str, str]] = {
    "revenue": {
        "increase": "{name}較上期成長{value}，代表公司營收持續擴大",
        "decrease": "{name}較上期減少{value}，需要關注後續趨勢",
        "neutral": "{name}維持在{value}左右，表現穩定",
    },
    "eps": {
        "increase": "{name}成長至{value}，每股獲利能力提升",
        "decrease": "{name}下降至{value}，每股獲利能力減弱",
        "neutral": "{name}維持在{value}，獲利表現穩定",
    },
    "pe_ratio": {
        "increase": "{name}上升至{value}，市場願意用更高價格買入獲利",
        "decrease": "{name}下降至{value}，市場對評價趨於保守",
        "neutral": "{name}維持在{value}左右，評價穩定",
    },
    "roe": {
        "increase": "{name}提升至{value}，股東權益報酬率改善",
        "decrease": "{name}下降至{value}，股東權益報酬率減弱",
        "neutral": "{name}維持在{value}左右，表現平穩",
    },
    "debt_ratio": {
        "increase": "{name}上升至{value}，負債比重增加需留意財務風險",
        "decrease": "{name}下降至{value}，負債比重降低財務結構改善",
        "neutral": "{name}維持在{value}左右，財務結構穩定",
    },
    "dividend_yield": {
        "increase": "{name}上升至{value}，殖利率提高對收息族更有吸引力",
        "decrease": "{name}下降至{value}，殖利率降低",
        "neutral": "{name}維持在{value}左右，配息表現穩定",
    },
    "gross_margin": {
        "increase": "{name}提升至{value}，產品競爭力與成本控制改善",
        "decrease": "{name}下降至{value}，毛利空間受到壓縮",
        "neutral": "{name}維持在{value}左右，毛利表現穩定",
    },
    "operating_margin": {
        "increase": "{name}提升至{value}，本業經營效率改善",
        "decrease": "{name}下降至{value}，經營效率需要關注",
        "neutral": "{name}維持在{value}左右，經營效率穩定",
    },
    "net_margin": {
        "increase": "{name}提升至{value}，最終獲利能力改善",
        "decrease": "{name}下降至{value}，最終獲利能力減弱",
        "neutral": "{name}維持在{value}左右，獲利能力穩定",
    },
}

# Fallback template for unknown metrics
_FALLBACK_TEMPLATES = {
    "increase": "{name}為{value}，數值較上期上升",
    "decrease": "{name}為{value}，數值較上期下降",
    "neutral": "{name}為{value}，數值維持穩定",
}


def _resolve_direction(delta: str | None) -> str:
    """Resolve a delta string to a direction key.

    Args:
        delta: Human-readable delta string, e.g. "+5.2%", "-3.1%", "持平".

    Returns:
        One of "increase", "decrease", "neutral".
    """
    if delta is None:
        return "neutral"
    stripped = delta.strip()
    if stripped.startswith("+") or "成長" in stripped or "增加" in stripped or "上升" in stripped:
        return "increase"
    if stripped.startswith("-") or "減少" in stripped or "下降" in stripped or "降低" in stripped:
        return "decrease"
    return "neutral"


class TemplateExplanationProvider:
    """Template-based fallback that implements ExplanationProvider.

    No external API calls. Always available.
    Designed to be replaced later by an LLM-backed provider.
    """

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        """Generate an explanation using predefined templates.

        Args:
            request: The explanation request with metric details.

        Returns:
            A plain-language ExplanationResponse with source="template".
        """
        metric_key = request.metric_name.lower().replace(" ", "_")
        direction = _resolve_direction(request.delta)

        # Look up metric templates, fall back to generic
        metric_templates = TEMPLATES.get(metric_key, _FALLBACK_TEMPLATES)
        template_text = metric_templates.get(direction, _FALLBACK_TEMPLATES[direction])

        text = template_text.format(
            name=request.metric_name,
            value=request.metric_value,
        )

        return ExplanationResponse(
            text=text,
            source="template",
            confidence=1.0,
        )

    def is_available(self) -> bool:
        """Always available — no external dependencies."""
        return True

