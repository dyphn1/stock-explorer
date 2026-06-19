"""
Event Interpretation Service — C98
Hybrid template+LLM system for explaining "Why did this stock move?"
Sprint 9: Template-only approach. LLM integration deferred.

Historian positioning: Explains what happened, never says buy/sell.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

from src.core.i18n import t

logger = logging.getLogger(__name__)

# ── Load interpretation templates once at module level ──────────
_TEMPLATES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "event_interpretation_templates.yaml",
)

_TEMPLATES: dict[str, dict[str, str]] = {}


def _load_templates() -> dict[str, dict[str, str]]:
    """Load interpretation templates from YAML, cached in memory."""
    global _TEMPLATES
    if _TEMPLATES:
        return _TEMPLATES
    try:
        with open(_TEMPLATES_PATH, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            _TEMPLATES = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load interpretation templates from %s: %s", _TEMPLATES_PATH, e)
        _TEMPLATES = {}
    return _TEMPLATES


def get_interpretation(
    event_type: str,
    severity: str,
    title: str,
    summary: str = "",
) -> dict[str, str]:
    """Return interpretation dict for a given event type.

    Args:
        event_type: One of revenue_surge, news_major, news_medium,
                    price_abnormal, dividend_change, institutional_shift.
        severity: high / medium / low.
        title: Event title (for context).
        summary: Event summary (for context).

    Returns:
        Dict with keys: short, detail, key_concept, event_type, severity.
        Falls back to a generic interpretation for unknown event types.
    """
    templates = _load_templates()
    tmpl = templates.get(event_type)

    if tmpl is None:
        # Graceful fallback for unknown event types
        logger.info("No interpretation template for event_type='%s', using fallback.", event_type)
        return {
            "short": t("event.fallback_short", title=title),
            "detail": t("event.fallback_detail", title=title),
            "key_concept": t("event.fallback_key_concept"),
            "event_type": event_type,
            "severity": severity,
        }

    return {
        "short": tmpl["short"],
        "detail": tmpl["detail"],
        "key_concept": tmpl["key_concept"],
        "event_type": event_type,
        "severity": severity,
    }


def get_drilldown_interpretation(event: dict[str, Any]) -> dict[str, str]:
    """Return full drill-down interpretation for an event dict.

    Args:
        event: Event dict with keys: type, severity, title, summary.

    Returns:
        Dict with keys: short, detail, key_concept, full_text.
        full_text combines all parts into a plain-language explanation.
    """
    event_type = event.get("type", "")
    severity = event.get("severity", "low")
    title = event.get("title", "")
    summary = event.get("summary", "")

    interp = get_interpretation(event_type, severity, title, summary)

    # Build full plain-language explanation
    severity_label = {
        "high": t("event.severity_high"),
        "medium": t("event.severity_medium"),
        "low": t("event.severity_low"),
    }.get(severity, t("event.severity_unknown"))
    full_text = (
        t("event.interpretation_header")
        + t("event.interpretation_severity", severity_label=severity_label, event_type=event_type)
        + t("event.interpretation_key_concept", key_concept=interp["key_concept"])
        + t("event.interpretation_detail", detail=interp["detail"])
        + t("event.interpretation_summary", summary=summary)
        + t("event.interpretation_disclaimer")
    )

    return {
        "short": interp["short"],
        "detail": interp["detail"],
        "key_concept": interp["key_concept"],
        "full_text": full_text,
    }
