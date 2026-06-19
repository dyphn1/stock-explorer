"""
Investor Story Feed Service
Generates personalized daily narrative stories from watchlist events and
market data.  No Streamlit imports — all UI rendering delegated to pages.

Functions:
    generate_daily_stories  – collect and compose story dicts
    generate_education_story – rotating metric-of-the-day card
"""

import logging
from datetime import datetime, timedelta

import pandas as pd

from src.core.i18n import t
from src.services.adaptive_engine import get_events_for_stock, get_all_recent_events
from src.services.market_data import get_sector_list, get_sector_performance
from src.services.analogy_engine import (
    get_revenue_analogy,
    get_per_analogy,
    get_dividend_analogy,
    get_roe_analogy,
    get_gross_margin_analogy,
    get_volume_analogy,
    get_institutional_analogy,
)
from src.services.metric_education import get_metric_explanation, get_supported_metrics

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────

TYPE_EVENT = "event"
TYPE_SECTOR = "sector"
TYPE_EDUCATION = "education"

SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}

# Rotating education metrics (cycled by day-of-year)
_EDUCATION_METRICS = ["ROE", "gross_margin", "PER", "dividend_yield", "debt_ratio", "revenue_yoy", "PBR", "net_margin"]

# Historian-style footnote templates
_HISTORIAN_TEMPLATES = [
    t("story.feed.historian.1"),
    t("story.feed.historian.2"),
    t("story.feed.historian.3"),
    t("story.feed.historian.4"),
]


def _severity_level(severity: str) -> int:
    """Map severity string to numeric rank (higher = more important)."""
    return SEVERITY_ORDER.get(severity, 0)


def _event_to_story(event: dict) -> dict:
    """Convert a raw event dict into a story dict."""
    stock_id = event.get("stock_id", "")
    title = event.get("title", t("story.feed.event.unknown"))
    summary = event.get("summary", "")
    date_str = event.get("date", datetime.now().strftime("%Y-%m-%d"))
    severity = event.get("severity", "low")
    event_type = event.get("type", "")

    # Build analogy based on event type
    analogy = ""
    try:
        if event_type == "revenue_surge":
            # Try to extract YoY percentage from title
            import re
            m = re.search(r'(-?\d+)%', title)
            if m:
                pct = float(m.group(1))
                analogy = get_revenue_analogy(abs(pct) / 10, "")  # rough scale-down
            else:
                analogy = t("story.feed.analogy.revenue_surge")
        elif event_type == "price_abnormal":
            analogy = t("story.feed.analogy.price_abnormal")
        elif event_type in ("news_major", "news_medium"):
            analogy = t("story.feed.analogy.news")
        elif event_type == "institutional_shift":
            analogy = t("story.feed.analogy.institutional_shift")
        else:
            analogy = t("story.feed.analogy.default")
    except Exception:
        analogy = t("story.feed.analogy.default")

    return {
        "title": title,
        "summary": summary,
        "stock_id": stock_id if stock_id else None,
        "date": date_str,
        "type": TYPE_EVENT,
        "severity": severity,
        "severity_level": _severity_level(severity),
        "analogy": analogy,
        "historian_note": _historian_note_for_event(title, summary),
    }


def _historian_note_for_event(title: str, summary: str) -> str:
    """Generate a short historian-style footnote for an event."""
    import hashlib
    # Deterministic but varied: hash the title
    h = int(hashlib.md5(title.encode()).hexdigest(), 16)
    template = _HISTORIAN_TEMPLATES[h % len(_HISTORIAN_TEMPLATES)]
    return f"📜 {template}"


def _sector_story(client, sector: str, perf: dict) -> dict:
    """Build a story dict from a sector performance summary."""
    if perf is None:
        return {}

    avg = perf.get("avg_change", 0)
    count = perf.get("count", 0)
    up = perf.get("up", 0)
    down = perf.get("down", 0)

    if avg > 1:
        emoji = "🔼"
        direction = t("story.feed.sector.direction.up")
    elif avg < -1:
        emoji = "🔽"
        direction = t("story.feed.sector.direction.down")
    else:
        emoji = "➡️"
        direction = t("story.feed.sector.direction.flat")

    title = t("story.feed.sector.title", sector=sector, direction=direction, avg=avg)
    summary = t("story.feed.sector.summary", sector=sector, count=count, up=up, down=down)

    # Pick top mover for analogy
    stocks = perf.get("stocks", [])
    top_stock = stocks[0] if stocks else {}
    stock_name = top_stock.get("stock_id", sector)
    try:
        top_chg = float(top_stock.get("change", 0))
        analogy = t("story.feed.sector.analogy.top_mover", stock_name=stock_name, top_chg=top_chg)
    except (TypeError, ValueError):
        analogy = t("story.feed.sector.analogy.general", sector=sector)

    return {
        "title": title,
        "summary": summary,
        "stock_id": None,  # sector-level
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": TYPE_SECTOR,
        "severity": "medium" if abs(avg) > 3 else "low",
        "severity_level": _severity_level("medium" if abs(avg) > 3 else "low"),
        "analogy": analogy,
        "historian_note": t("story.feed.sector.historian_note", sector=sector),
    }


# ── Public API ─────────────────────────────────────────────

def generate_daily_stories(client, watchlist_symbols: list[str], max_stories: int = 5) -> list[dict]:
    """
    Fetch recent events for compose a list of story dicts.

    Args:
        client: FinMindClient instance.
        watchlist_symbols: list of stock_id strings in the user's watchlist.
        max_stories: maximum number of stories to return.

    Returns:
        List of story dicts sorted newest-first, highest severity first.
        Each dict keys: title, summary, stock_id, date, type, analogy,
        historian_note, severity_level.
        Returns empty list if no data could be composed.
    """
    stories: list[dict] = []

    # ── 1. Watchlist events ─────────────────────────────────
    all_events: list = []
    if watchlist_symbols:
        for sid in watchlist_symbols:
            try:
                evts = get_events_for_stock(sid, days=30)
                all_events.extend(evts)
            except Exception as exc:
                logger.debug("story_feed: get_events_for_stock(%s) failed: %s", sid, exc)

    # Also grab any recent events globally (in case user hasn't viewed stocks yet)
    try:
        global_events = get_all_recent_events(days=14, limit=20)
        all_events.extend(global_events)
    except Exception as exc:
        logger.debug("story_feed: get_all_recent_events failed: %s", exc)

    # Deduplicate by (stock_id, title, date)
    seen = set()
    unique_events = []
    for e in all_events:
        key = (e.get("stock_id", ""), e.get("title", ""), e.get("date", ""))
        if key not in seen:
            seen.add(key)
            unique_events.append(e)

    # Sort: severity desc, then date desc
    unique_events.sort(
        key=lambda e: (_severity_level(e.get("severity", "low")), e.get("date", "")),
        reverse=True,
    )

    for event in unique_events[:max_stories]:
        story = _event_to_story(event)
        if story:
            stories.append(story)

    # ── 2. Sector-level stories ─────────────────────────────
    # Try to get sector data for the first watchlist stock's sector
    if watchlist_symbols:
        try:
            sectors = get_sector_list(client)
            if sectors:
                # Pick the most relevant sector (just take first available for now)
                sector = sectors[0]
                perf = get_sector_performance(client, sector)
                if perf:
                    sec_story = _sector_story(client, sector, perf)
                    if sec_story:
                        stories.append(sec_story)
        except Exception as exc:
            logger.debug("story_feed: sector data failed: %s", exc)

    # ── 3. Sort & limit ─────────────────────────────────────
    stories.sort(key=lambda s: (s.get("severity_level", 0), s.get("date", "")), reverse=True)
    stories = stories[:max_stories]

    # Log result
    logger.info("story_feed: generated %d stories for %d watchlist symbols",
                 len(stories), len(watchlist_symbols))

    return stories


def generate_education_story(client) -> dict:
    """
    Generate a rotating 'metric of the day' education story.

    Uses day-of-year to cycle through supported metrics deterministically.

    Args:
        client: FinMindClient instance (unused currently, kept for API compat).

    Returns:
        story dict with type=education, or empty dict if nothing usable.
    """
    day_of_year = datetime.now().timetuple().tm_yday  # 1..366
    metric_idx = day_of_year % len(_EDUCATION_METRICS)
    metric_name = _EDUCATION_METRICS[metric_idx]

    # Validate against registry (in case metric_education doesn't cover it)
    supported = get_supported_metrics()
    if metric_name not in supported:
        metric_name = supported[0] if supported else "ROE"

    try:
        edu = get_metric_explanation(metric_name, 0.0, "")
    except Exception:
        edu = get_metric_explanation("ROE", 0.0, "")

    display_name = edu.get("display_name", metric_name)
    explanation = edu.get("explanation", "")
    analogy = edu.get("analogy", "")
    historical = edu.get("historical_context", "")

    return {
        "title": t("story.feed.education.title", display_name=display_name),
        "summary": explanation,
        "stock_id": None,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": TYPE_EDUCATION,
        "severity": "low",
        "severity_level": 0,
        "analogy": analogy or t("story.feed.education.analogy_default"),
        "historian_note": f"📜 {historical}",
    }
