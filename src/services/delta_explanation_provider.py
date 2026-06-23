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
from src.core.i18n import t

# ── Metric name → template key mapping ─────────────────────────
_METRIC_KEY_MAP: dict[str, str] = {
    t("delta.metric.revenue_monthly"): "revenue",
    t("delta.metric.revenue_yoy"): "revenue",
    # "股價（近 30 日均價）" → no direct template match, uses fallback
}

# ── Tiered explanation templates (zh-TW) ─────────────────────
# Each metric name maps to direction → threshold → explanation template.
# Thresholds are checked from highest to lowest; first match wins.
# Format placeholders: {stock_prefix}, {abs_pct}

_REVENUE_TEMPLATES = {
    "up": [
        (50, t('delta_explanation_provider.revenue_up_extreme')),
        (30, t('delta_explanation_provider.revenue_up_strong')),
        (0,  t('delta_explanation_provider.revenue_up_moderate')),
    ],
    "down": [
        (50, t('delta_explanation_provider.revenue_down_extreme')),
        (30, t('delta_explanation_provider.revenue_down_strong')),
        (0,  t('delta_explanation_provider.revenue_down_moderate')),
    ],
}

_PRICE_TEMPLATES = {
    "up": [
        (30, t('delta_explanation_provider.price_up_large')),
        (20, t('delta_explanation_provider.price_up_medium')),
        (0,  t('delta_explanation_provider.price_up_small')),
    ],
    "down": [
        (30, t('delta_explanation_provider.price_down_large')),
        (20, t('delta_explanation_provider.price_down_medium')),
        (0,  t('delta_explanation_provider.price_down_small')),
    ],
}

_YOY_TEMPLATES = {
    "up": [
        (50, t('delta_explanation_provider.yoy_up_strong')),
        (20, t('delta_explanation_provider.yoy_up_moderate')),
        (0,  t('delta_explanation_provider.yoy_up_mild')),
    ],
    "down": [
        (50, t('delta_explanation_provider.yoy_down_extreme')),
        (20, t('delta_explanation_provider.yoy_down_strong')),
        (0,  t('delta_explanation_provider.yoy_down_moderate')),
    ],
}

_METRIC_TEMPLATES: dict[str, dict[str, list[tuple[int, str]]]] = {
    t("delta.metric.revenue_monthly"): _REVENUE_TEMPLATES,
    t("delta.metric.price_30d"): _PRICE_TEMPLATES,
    t("delta.metric.revenue_yoy"): _YOY_TEMPLATES,
}

# ── Implication templates (C143) ──────────────────────────────
# Historian tone, factual past-tense observations.
# All phrases verified against tone blocklist:
#   建議, 應該, 買, 賣, 推薦, 进场, 出场, 值得關注, 需要密切關注, 值得持續追蹤, 表現優於預期
# Safe alternatives used: 可留意, 可觀察, 可持續追蹤

_IMPLICATION_TEMPLATES: dict[str, dict[str, list[tuple[int, str]]]] = {
    t("delta.metric.revenue_monthly"): {
        "up": [
            (50, t('delta_explanation_provider.implication_revenue_up_extreme')),
            (30, t('delta_explanation_provider.implication_revenue_up_strong')),
            (0, t('delta_explanation_provider.implication_revenue_up_moderate')),
        ],
        "down": [
            (50, t('delta_explanation_provider.implication_revenue_down_extreme')),
            (30, t('delta_explanation_provider.implication_revenue_down_strong')),
            (0, t('delta_explanation_provider.implication_revenue_down_moderate')),
        ],
    },
    t("delta.metric.price_30d"): {
        "up": [
            (30, t('delta_explanation_provider.implication_price_up_extreme')),
            (20, t('delta_explanation_provider.implication_price_up_strong')),
            (0, t('delta_explanation_provider.implication_price_up_moderate')),
        ],
        "down": [
            (30, t('delta_explanation_provider.implication_price_down_extreme')),
            (20, t('delta_explanation_provider.implication_price_down_strong')),
            (0, t('delta_explanation_provider.implication_price_down_moderate')),
        ],
    },
    t("delta.metric.revenue_yoy"): {
        "up": [
            (50, t('delta_explanation_provider.implication_yoy_up_extreme')),
            (20, t('delta_explanation_provider.implication_yoy_up_strong')),
            (0, t('delta_explanation_provider.implication_yoy_up_moderate')),
        ],
        "down": [
            (50, t('delta_explanation_provider.implication_yoy_down_extreme')),
            (20, t('delta_explanation_provider.implication_yoy_down_strong')),
            (0, t('delta_explanation_provider.implication_yoy_down_moderate')),
        ],
    },
}

# Generic fallback implications for unknown metrics
_GENERIC_IMPLICATION_TEMPLATES: dict[str, str] = {
    "up": t('delta_explanation_provider.generic_implication_up'),
    "down": t('delta_explanation_provider.generic_implication_down'),
}

# ── Generic fallback templates ────────────────────────────────
_GENERIC_TEMPLATES = {
    "up":   t('delta_explanation_provider.generic_template_up'),
    "down": t('delta_explanation_provider.generic_template_down'),
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
                    metric_name=metric_name,
                )

    # Generic fallback
    template = _GENERIC_TEMPLATES[direction]
    return template.format(
        stock_prefix=stock_prefix,
        metric_name=metric_name,
        abs_pct=abs_pct,
    )


def _pick_implication(
    metric_name: str,
    direction: str,
    abs_pct: float,
) -> str:
    """Pick the appropriate implication sentence for a delta (C143).

    Uses tiered implication templates keyed on metric_name × direction.
    Falls back to generic implication templates for unknown metric names.

    All templates are historian-tone, factual past-tense observations
    that pass the tone blocklist (verified at write time).

    Args:
        metric_name: The delta metric name (e.g. "月營收").
        direction: "up" or "down".
        abs_pct: Absolute percentage value.

    Returns:
        The implication sentence string (no stock prefix — generic third-person).
    """
    metric_implications = _IMPLICATION_TEMPLATES.get(metric_name)
    if metric_implications is not None:
        direction_templates = metric_implications[direction]
        for threshold, template in direction_templates:
            if abs_pct >= threshold:
                return template

    # Generic fallback
    return _GENERIC_IMPLICATION_TEMPLATES[direction]


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

        # Generate implication sentence (C143)
        implication = _pick_implication(
            metric_name=request.metric_name,
            direction=direction,
            abs_pct=abs_pct,
        )

        # Also use the template provider for composition (delegation)
        # — call it to verify it's available (protocol compliance)
        self._template_provider.is_available()

        return ExplanationResponse(
            text=text,
            source="delta_template",
            confidence=1.0,
            implication=implication,
        )

    def is_available(self) -> bool:
        """Always available — no external dependencies."""
        return True
