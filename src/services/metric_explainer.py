"""
Metric Explainer — convenience function for C139 "Explain This Number".

Composes TemplateExplanationProvider with metric education data
to produce a dict suitable for rendering in a Streamlit popover.

No Streamlit imports — pure data service.
"""

from __future__ import annotations

from src.services.llm import TemplateExplanationProvider, ExplanationRequest


# ── Metric name → template key mapping ──────────────────────
# TemplateExplanationProvider uses lowercase English keys.
_METRIC_KEY_MAP: dict[str, str] = {
    "月營收": "revenue",
    "revenue": "revenue",
    "revenue_yoy": "revenue",
    "營收年增率": "revenue",
    "ROE": "roe",
    "roe": "roe",
    "毛利率": "gross_margin",
    "gross_margin": "gross_margin",
    "本益比": "pe_ratio",
    "PER": "pe_ratio",
    "pe_ratio": "pe_ratio",
    "負債比": "debt_ratio",
    "debt_ratio": "debt_ratio",
    "殖利率": "dividend_yield",
    "dividend_yield": "dividend_yield",
    "淨值比": "pe_ratio",  # fallback to pe_ratio template
    "PBR": "pe_ratio",     # fallback to pe_ratio template
    "pbr": "pe_ratio",
    "淨利率": "net_margin",
    "net_margin": "net_margin",
    "營業利益率": "operating_margin",
    "operating_margin": "operating_margin",
    "eps": "eps",
    "EPS": "eps",
}


def _resolve_template_key(metric_name: str) -> str:
    """Map a display metric name to a template key."""
    return _METRIC_KEY_MAP.get(metric_name, metric_name.lower().replace(" ", "_"))


def get_metric_explanation_for_popover(
    metric_name: str,
    metric_value: str,
    delta: str = "",
    context: dict | None = None,
) -> dict:
    """Get a dict with explanation data for the C139 popover.

    Composes TemplateExplanationProvider with the metric education layer.

    Args:
        metric_name: The metric name (e.g. "月營收", "ROE", "毛利率")
        metric_value: The metric value as display string (e.g. "123.4 億")
        delta: Optional delta string (e.g. "+5.2%", "-3.1%")
        context: Optional dict with additional context (industry, direction, etc.)

    Returns:
        dict with keys: display_name, value_text, explanation_text, source
    """
    provider = TemplateExplanationProvider()

    template_key = _resolve_template_key(metric_name)

    request = ExplanationRequest(
        metric_name=template_key,
        metric_value=str(metric_value),
        delta=delta or None,
        context=context or {},
    )
    response = provider.explain(request)

    return {
        "display_name": metric_name,
        "value_text": str(metric_value),
        "explanation_text": response.text,
        "source": response.source,
    }
