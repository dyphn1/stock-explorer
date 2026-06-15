"""
Stock Movement Explainer Service — C188
Explains "Why did this stock move?" with plain-language narratives.
Cross-references events from adaptive_engine to find correlated causes.

Historian positioning: Explains what happened, never says buy/sell.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

from src.services.event_interpretation_service import get_interpretation

logger = logging.getLogger(__name__)

# ── Load movement templates once at module level ──────────
_TEMPLATES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "movement_explanation_templates.yaml",
)

_TEMPLATES: dict[str, Any] = {}


def _load_templates() -> dict[str, Any]:
    """Load movement explanation templates from YAML, cached in memory."""
    global _TEMPLATES
    if _TEMPLATES:
        return _TEMPLATES
    try:
        with open(_TEMPLATES_PATH, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            _TEMPLATES = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load movement templates from %s: %s", _TEMPLATES_PATH, e)
        _TEMPLATES = {}
    return _TEMPLATES


def _classify_magnitude(change_pct: float) -> str:
    """Classify movement magnitude.

    Returns:
        'major' if |change_pct| >= 10%,
        'significant' if |change_pct| >= 3%,
        'minor' otherwise.
    """
    abs_pct = abs(change_pct)
    templates = _load_templates()
    major_t = templates.get("major_threshold", 10.0)
    sig_t = templates.get("significant_threshold", 3.0)
    if abs_pct >= major_t:
        return "major"
    elif abs_pct >= sig_t:
        return "significant"
    return "minor"


def _detect_direction(change_pct: float) -> str:
    """Detect movement direction from percentage change."""
    if change_pct > 0.5:
        return "up"
    elif change_pct < -0.5:
        return "down"
    return "sideways"


def _find_correlated_events(
    stock_id: str,
    date: str | None,
    direction: str,
) -> list[dict[str, Any]]:
    """Find events from adaptive_engine that correlate with the movement.

    Cross-references recent events for the stock to find potential causes.
    Returns a list of event dicts sorted by relevance.
    """
    try:
        from src.services.adaptive_engine import get_events_for_stock
        events = get_events_for_stock(stock_id, days=30)
    except Exception as e:
        logger.debug("Could not load events for %s: %s", stock_id, e)
        return []

    if not events:
        return []

    # Filter events near the movement date (within 5 days if date provided)
    correlated = []
    if date:
        from datetime import datetime, timedelta
        try:
            move_date = datetime.strptime(date, "%Y-%m-%d")
            for ev in events:
                ev_date_str = ev.get("date", "")
                try:
                    ev_date = datetime.strptime(ev_date_str, "%Y-%m-%d")
                    if abs((ev_date - move_date).days) <= 5:
                        correlated.append(ev)
                except (ValueError, TypeError):
                    continue
        except (ValueError, TypeError):
            # If date parsing fails, use all recent events
            correlated = events[:5]
    else:
        # No date specified — use most recent events
        correlated = events[:5]

    return correlated


def _categorize_event(event: dict[str, Any]) -> str:
    """Map an event to a movement explanation category.

    Returns one of: earnings, dividend, sector, institutional, news, technical.
    """
    event_type = event.get("type", "")
    title = event.get("title", "")
    summary = event.get("summary", "")

    # Map event types to categories
    type_map = {
        "revenue_surge": "earnings",
        "price_abnormal": "technical",
        "dividend_change": "dividend",
        "institutional_shift": "institutional",
        "news_major": "news",
        "news_medium": "news",
    }

    category = type_map.get(event_type)
    if category:
        return category

    # Fallback: keyword-based categorization from title/summary
    text = f"{title} {summary}"
    if any(kw in text for kw in ["營收", "獲利", "財報", "盈餘", "EPS"]):
        return "earnings"
    if any(kw in text for kw in ["股利", "配息", "除權", "除息"]):
        return "dividend"
    if any(kw in text for kw in ["外資", "投信", "法人", "買超", "賣超"]):
        return "institutional"
    if any(kw in text for kw in ["漲", "跌", "漲停", "跌停", "波動"]):
        return "technical"

    return "news"


def _build_narrative(
    direction: str,
    change_pct: float,
    category: str,
    events: list[dict[str, Any]],
) -> dict[str, str]:
    """Build plain-language narrative from templates.

    Returns dict with keys: short, detail, key_concept.
    """
    templates = _load_templates()
    abs_pct = abs(change_pct)

    direction_templates = templates.get(direction, {})
    if not direction_templates:
        # Ultimate fallback
        return {
            "short": f"股價{'上漲' if direction == 'up' else '下跌' if direction == 'down' else '震盪'} {abs_pct:.1f}%。",
            "detail": "股價變動可能受到多種因素影響，可搭配其他資訊一起觀察。",
            "key_concept": "股價變動通常是多重因素綜合結果",
        }

    category_template = direction_templates.get(category, direction_templates.get("fallback", {}))
    if not category_template:
        category_template = direction_templates.get("fallback", {})

    short = category_template.get("short", "").format(pct=f"{abs_pct:.1f}")
    detail = category_template.get("detail", "")
    key_concept = category_template.get("key_concept", "")

    # If we have events, enrich the detail with event interpretation
    if events:
        primary_event = events[0]
        interp = get_interpretation(
            event_type=primary_event.get("type", ""),
            severity=primary_event.get("severity", "low"),
            title=primary_event.get("title", ""),
            summary=primary_event.get("summary", ""),
        )
        if interp.get("detail"):
            detail = f"{detail}\n\n{interp['detail']}"
        if interp.get("key_concept") and not key_concept:
            key_concept = interp["key_concept"]

    return {
        "short": short,
        "detail": detail,
        "key_concept": key_concept,
    }


def explain_movement(
    stock_id: str,
    current_price: float,
    previous_price: float,
    date: str | None = None,
) -> dict[str, Any]:
    """Explain why a stock moved between two prices.

    Args:
        stock_id: Stock identifier.
        current_price: Current/latest price.
        previous_price: Previous comparison price.
        date: Optional date string (YYYY-MM-DD) of the movement.

    Returns:
        Structured dict with keys:
            direction: 'up' | 'down' | 'sideways'
            magnitude: 'major' | 'significant' | 'minor'
            change_pct: float percentage change
            reason: category string (earnings, dividend, etc.)
            detail: plain-language detail text
            key_concept: one-line key takeaway
            events_used: list of correlated event dicts
            narrative: short narrative summary
    """
    # Guard against invalid prices
    if previous_price == 0 or previous_price is None:
        return {
            "direction": "sideways",
            "magnitude": "minor",
            "change_pct": 0.0,
            "reason": "unknown",
            "detail": "無法計算漲跌幅（前一日價格為零或未提供）。",
            "key_concept": "需要完整的價格資料才能分析",
            "events_used": [],
            "narrative": "無法判斷股價變動原因。",
        }

    change_pct = ((current_price - previous_price) / previous_price) * 100
    direction = _detect_direction(change_pct)
    magnitude = _classify_magnitude(change_pct)

    # Find correlated events
    events = _find_correlated_events(stock_id, date, direction)

    # Determine primary reason category
    if events:
        category = _categorize_event(events[0])
    else:
        category = "fallback"

    # Build narrative
    narrative = _build_narrative(direction, change_pct, category, events)

    return {
        "direction": direction,
        "magnitude": magnitude,
        "change_pct": round(change_pct, 2),
        "reason": category,
        "detail": narrative["detail"],
        "key_concept": narrative["key_concept"],
        "events_used": events,
        "narrative": narrative["short"],
    }
