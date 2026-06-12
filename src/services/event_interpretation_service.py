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
            "short": f'"{title}" 代表市場出現了值得關注的變化。',
            "detail": (
                f'這筆事件記錄顯示 "{title}"。'
                f"建議搭配其他資訊一起觀察，不要僅憑單一事件做判斷。"
            ),
            "key_concept": "單一事件不足以判斷，要搭配整體分析",
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
    severity_label = {"high": "重大", "medium": "注意", "low": "參考"}.get(severity, "未知")
    full_text = (
        f"【事件解讀】\n\n"
        f"這是一則「{severity_label}」等級的「{event_type}」事件。\n\n"
        f"📌 核心概念：{interp['key_concept']}\n\n"
        f"📖 詳細說明：{interp['detail']}\n\n"
        f"📋 原始摘要：{summary}\n\n"
        f"⚠️ 歷史學家觀點：以上解讀僅說明事件背景與可能意涵，"
        f"不構成任何投資建議。"
    )

    return {
        "short": interp["short"],
        "detail": interp["detail"],
        "key_concept": interp["key_concept"],
        "full_text": full_text,
    }
