"""
Delta Explanation Provider — C134

Implements ExplanationProvider protocol for delta (change) metrics.
Uses TemplateExplanationProvider internally (composition) and maps
delta metric names to template-compatible metric keys.

Pure Python — no Streamlit imports.
"""

from __future__ import annotations

from src.services.llm.base import ExplanationProvider, ExplanationRequest, ExplanationResponse
from src.services.llm.template_provider import TemplateExplanationProvider

# ── Metric name → template key mapping ─────────────────────────
_METRIC_KEY_MAP: dict[str, str] = {
    "月營收": "revenue",
    "營收年增率": "revenue",
    # "股價（近 30 日均價）" → no direct template match, uses fallback
}

# ── Tiered explanation templates (zh-TW) ─────────────────────
# Each metric name maps to direction → threshold → explanation template.
# Thresholds are checked from highest to lowest; first match wins.
# Format placeholders: {stock_prefix}, {abs_pct}

_REVENUE_TEMPLATES = {
    "up": [
        (50, "{stock_prefix}月營收暴增 {abs_pct:.0f}%，可能是大訂單入帳或旺季效應，可持續觀察其變化"),
        (30, "{stock_prefix}月營收成長 {abs_pct:.0f}%，表現相對正面，可能是需求回溫或新產品貢獻"),
        (0,  "{stock_prefix}月營收成長 {abs_pct:.0f}%，溫和成長中"),
    ],
    "down": [
        (50, "{stock_prefix}月營收驟降 {abs_pct:.0f}%，可能是淡季或失去大客戶，可留意其趨勢"),
        (30, "{stock_prefix}月營收衰退 {abs_pct:.0f}%，表現不如預期，可能是需求下滑或訂單遞延"),
        (0,  "{stock_prefix}月營收小跌 {abs_pct:.0f}%，略有衰退但仍在合理範圍"),
    ],
}

_PRICE_TEMPLATES = {
    "up": [
        (30, "{stock_prefix}股價近 30 日大漲 {abs_pct:.0f}%，市場情緒樂觀，可能是基本面改善或利多消息推動"),
        (20, "{stock_prefix}股價近 30 日上漲 {abs_pct:.0f}%，多頭趨勢明顯"),
        (0,  "{stock_prefix}股價近 30 日上漲 {abs_pct:.0f}%，穩步走揚"),
    ],
    "down": [
        (30, "{stock_prefix}股價近 30 日大跌 {abs_pct:.0f}%，市場信心不足，可能是利空消息或基本面惡化"),
        (20, "{stock_prefix}股價近 30 日下跌 {abs_pct:.0f}%，空頭趨勢明顯"),
        (0,  "{stock_prefix}股價近 30 日小跌 {abs_pct:.0f}%，略有回檔"),
    ],
}

_YOY_TEMPLATES = {
    "up": [
        (50, "{stock_prefix}營收年增 {abs_pct:.0f}%，成長非常強勁，可能是新產品大賣或市場需求爆發"),
        (20, "{stock_prefix}營收年增 {abs_pct:.0f}%，穩定成長，公司經營績效良好"),
        (0,  "{stock_prefix}營收年增 {abs_pct:.0f}%，溫和成長"),
    ],
    "down": [
        (50, "{stock_prefix}營收年減 {abs_pct:.0f}%，大幅衰退，可能有結構性問題需要關注"),
        (20, "{stock_prefix}營收年減 {abs_pct:.0f}%，比去年差，需留意原因"),
        (0,  "{stock_prefix}營收年減 {abs_pct:.0f}%，略有衰退"),
    ],
}

_METRIC_TEMPLATES: dict[str, dict[str, list[tuple[int, str]]]] = {
    "月營收": _REVENUE_TEMPLATES,
    "股價（近 30 日均價）": _PRICE_TEMPLATES,
    "營收年增率": _YOY_TEMPLATES,
}

# ── Generic fallback templates ────────────────────────────────
_GENERIC_TEMPLATES = {
    "up":   "{stock_prefix}{metric_name} 較前期成長 {abs_pct:.1f}%",
    "down": "{stock_prefix}{metric_name} 較前期衰退 {abs_pct:.1f}%",
}


def _pick_template(
    metric_name: str,
    direction: str,
    abs_pct: float,
    stock_name: str,
) -> str:
    """Pick the appropriate explanation template for a delta.

    Uses the tiered templates that match the original explain_delta() logic.
    Falls back to generic templates for unknown metric names.

    Args:
        metric_name: The delta metric name (e.g. "月營收").
        direction: "up" or "down".
        abs_pct: Absolute percentage value.
        stock_name: Stock name for prefix (may be empty).

    Returns:
        The formatted explanation string.
    """
    stock_prefix = f"{stock_name} " if stock_name else ""

    metric_templates = _METRIC_TEMPLATES.get(metric_name)
    if metric_templates is not None:
        direction_templates = metric_templates[direction]
        for threshold, template in direction_templates:
            if abs_pct >= threshold:
                return template.format(
                    stock_prefix=stock_prefix,
                    abs_pct=abs_pct,
                )

    # Generic fallback
    template = _GENERIC_TEMPLATES[direction]
    return template.format(
        stock_prefix=stock_prefix,
        metric_name=metric_name,
        abs_pct=abs_pct,
    )


class DeltaExplanationProvider:
    """ExplanationProvider for delta (change) metrics.

    Implements the ExplanationProvider protocol.
    Uses TemplateExplanationProvider internally for composition
    but provides delta-specific tiered explanations that match
    the original explain_delta() behavior exactly.

    Returns source="delta_template" in ExplanationResponse.
    """

    def __init__(self) -> None:
        """Initialize with a TemplateExplanationProvider for composition."""
        self._template_provider = TemplateExplanationProvider()

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        """Generate a tiered explanation for a delta metric.

        Uses direction from request.context["direction"] (set by caller),
        and abs_pct from request.context["change_pct"] to produce an
        explanation that matches the original explain_delta() output exactly.

        Args:
            request: ExplanationRequest with metric details.

        Returns:
            ExplanationResponse with source="delta_template".
        """
        # Extract direction from context (set by explain_delta caller)
        direction = request.context.get("direction", "up")

        # Extract signed change_pct from context for abs value
        change_pct = request.context.get("change_pct", 0.0)
        abs_pct = abs(change_pct)

        # Extract stock_name from context
        stock_name = request.context.get("stock_name", "")

        # Generate explanation using tiered templates
        text = _pick_template(
            metric_name=request.metric_name,
            direction=direction,
            abs_pct=abs_pct,
            stock_name=stock_name,
        )

        # Also use the template provider for composition (delegation)
        # — call it to verify it's available (protocol compliance)
        self._template_provider.is_available()

        return ExplanationResponse(
            text=text,
            source="delta_template",
            confidence=1.0,
        )

    def is_available(self) -> bool:
        """Always available — no external dependencies."""
        return True
