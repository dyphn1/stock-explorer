"""
Timeline Service — C28 Story Timeline MVP
Compose-and-enrich pipeline merging events + case studies + milestones.

Pure Python service — no Streamlit imports.
Performance target: <200ms (all local YAML, no API calls at render time).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import TypedDict

import yaml

logger = logging.getLogger(__name__)

# ── Type definitions ──────────────────────────────────────


class TimelineEntry(TypedDict, total=False):
    """Single entry in the company story timeline."""

    date: str
    type: str
    severity: str
    title: str
    summary: str
    interpretation: str
    analogy: str
    source: str
    icon: str
    count: int


# ── Event type → icon mapping ─────────────────────────────

_EVENT_ICONS: dict[str, str] = {
    "revenue_surge": "💰",
    "news_major": "📰",
    "news_medium": "📰",
    "price_abnormal": "📉",
    "dividend_change": "💵",
    "institutional_shift": "🏷️",
    "founding": "🏛️",
    "ipo": "🔔",
    "product_launch": "🚀",
    "expansion": "🌍",
    "acquisition": "🤝",
    "merger": "🔗",
    "milestone": "⭐",
    "case_study": "📚",
}

# ── Severity → color mapping ──────────────────────────────

_SEVERITY_COLORS: dict[str, str] = {
    "high": "#E74C3C",
    "medium": "#F39C12",
    "low": "#279B68",
}

# ── Milestone data loading ────────────────────────────────

_MILESTONES_CACHE: dict[str, list[dict]] = {}


def _load_milestones() -> dict[str, list[dict]]:
    """Load company milestones from YAML, cached in memory."""
    global _MILESTONES_CACHE
    if _MILESTONES_CACHE:
        return _MILESTONES_CACHE

    yaml_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "src",
        "data",
        "company_milestones.yaml",
    )
    # Also try relative to config directory
    if not os.path.exists(yaml_path):
        yaml_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "company_milestones.yaml",
        )

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        # raw is keyed by stock_id string → {stock_id, milestones}
        for sid, entry in raw.items():
            if isinstance(entry, dict):
                _MILESTONES_CACHE[sid] = entry.get("milestones", [])
    except Exception as exc:
        logger.warning("Failed to load company milestones from %s: %s", yaml_path, exc)
        _MILESTONES_CACHE = {}

    return _MILESTONES_CACHE


# ── Interpretation helper ──────────────────────────────────


def _attach_interpretation(entry: TimelineEntry) -> TimelineEntry:
    """Attach interpretation text to a timeline entry.

    Delegates to event_interpretation_service when available;
    falls back to a generic interpretation for milestone/case types.
    """
    event_type = entry.get("type", "")
    severity = entry.get("severity", "low")
    title = entry.get("title", "")
    summary = entry.get("summary", "")

    # Try the interpretation service for known event types
    try:
        from src.services.event_interpretation_service import get_interpretation

        interp = get_interpretation(event_type, severity, title, summary)
        entry["interpretation"] = interp.get("short", "")
    except Exception:
        # Graceful fallback for any import or lookup failure
        entry["interpretation"] = (
            f'"{title}" 代表市場出現了值得關注的變化。'
            if title else ""
        )

    return entry


# ── Deduplication helper ──────────────────────────────────


def _deduplicate(entries: list[TimelineEntry]) -> list[TimelineEntry]:
    """Merge same-day, same-type events into a single entry with count badge.

    Groups entries by (date, type). When multiple entries share the
    same group, the first entry is kept and a `count` field is added.
    """
    from collections import OrderedDict

    groups: OrderedDict[tuple[str, str], list[TimelineEntry]] = OrderedDict()
    for e in entries:
        key = (e.get("date", ""), e.get("type", ""))
        if key not in groups:
            groups[key] = []
        groups[key].append(e)

    result: list[TimelineEntry] = []
    for _key, group_entries in groups.items():
        if len(group_entries) == 1:
            result.append(group_entries[0])
        else:
            # Keep the first entry, add count badge
            merged = dict(group_entries[0])
            merged["count"] = len(group_entries)
            # Combine summaries if they differ
            summaries = [e.get("summary", "") for e in group_entries if e.get("summary")]
            unique_summaries = list(dict.fromkeys(summaries))
            if len(unique_summaries) > 1:
                merged["summary"] = " | ".join(unique_summaries[:3])
            result.append(merged)  # type: ignore[arg-type]

    return result


# ── Public API ─────────────────────────────────────────────


def get_timeline(
    stock_id: str,
    lookback_days: int = 365,
) -> list[TimelineEntry]:
    """Build an enriched timeline for a given stock.

    Pipeline:
      1. Fetch detected events from adaptive_engine
      2. Fetch matching case studies from market_event_service
      3. Fetch company milestones from company_milestones.yaml
      4. Merge + sort by date
      5. Deduplicate overlapping same-day events
      6. Attach interpretation from event_interpretation_service

    Args:
        stock_id: Stock identifier (e.g. "2330").
        lookback_days: How many days back to include. Default 365.

    Returns:
        List of TimelineEntry dicts, sorted newest-first.
        Returns empty list if no entries found.
    """
    now = datetime.now()
    cutoff = now - timedelta(days=lookback_days)
    all_entries: list[TimelineEntry] = []

    # ── Step 1: Detected events from adaptive_engine ────────
    try:
        from src.services.adaptive_engine import get_events_for_stock

        detected = get_events_for_stock(stock_id, days=lookback_days)
        for evt in detected:
            event_date_str = evt.get("date", "")
            try:
                event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
            except (ValueError, TypeError):
                continue
            if event_date < cutoff:
                continue

            evt_type = evt.get("type", "unknown")
            entry: TimelineEntry = {
                "date": event_date_str,
                "type": evt_type,
                "severity": evt.get("severity", "low"),
                "title": evt.get("title", ""),
                "summary": evt.get("summary", ""),
                "source": "detected",
                "icon": _EVENT_ICONS.get(evt_type, "📌"),
                "analogy": evt.get("analogy", ""),
            }
            all_entries.append(entry)
    except Exception as exc:
        logger.debug("timeline_service: adaptive_engine events failed for %s: %s", stock_id, exc)

    # ── Step 2: Case studies from market_event_service ──────
    try:
        from src.services.market_event_service import get_events_for_stock as get_case_events

        case_events = get_case_events(stock_id)
        for cs in case_events:
            cs_date_str = cs.get("date", "")
            try:
                cs_date = datetime.strptime(cs_date_str[:10], "%Y-%m-%d")
            except (ValueError, TypeError):
                continue
            # For case studies, include regardless of lookback (they are historical)
            # but still respect the cutoff
            if cs_date < cutoff:
                continue

            entry: TimelineEntry = {
                "date": cs_date_str[:10],
                "type": "case_study",
                "severity": cs.get("severity", "low"),
                "title": cs.get("title", ""),
                "summary": cs.get("summary", ""),
                "source": "case_study",
                "icon": "📚",
                "analogy": "",
            }
            all_entries.append(entry)
    except Exception as exc:
        logger.debug("timeline_service: case studies failed for %s: %s", stock_id, exc)

    # ── Step 3: Company milestones from YAML ────────────────
    try:
        milestones = _load_milestones()
        stock_milestones = milestones.get(stock_id, [])
        for ms in stock_milestones:
            ms_date_str = ms.get("date", "")
            try:
                ms_date = datetime.strptime(ms_date_str, "%Y-%m-%d")
            except (ValueError, TypeError):
                continue
            if ms_date < cutoff:
                continue

            ms_type = ms.get("type", "milestone")
            entry: TimelineEntry = {
                "date": ms_date_str,
                "type": ms_type,
                "severity": "low",
                "title": ms.get("title", ""),
                "summary": ms.get("summary", ""),
                "source": "milestone",
                "icon": _EVENT_ICONS.get(ms_type, "⭐"),
                "analogy": "",
            }
            all_entries.append(entry)
    except Exception as exc:
        logger.debug("timeline_service: milestones failed for %s: %s", stock_id, exc)

    # ── Step 4: Sort by date (newest first) ─────────────────
    all_entries.sort(key=lambda e: e.get("date", ""), reverse=True)

    # ── Step 5: Deduplicate same-day, same-type entries ─────
    all_entries = _deduplicate(all_entries)

    # ── Step 6: Attach interpretation ───────────────────────
    all_entries = [_attach_interpretation(entry) for entry in all_entries]

    logger.info(
        "timeline_service: %d entries for stock_id=%s (lookback=%d days)",
        len(all_entries), stock_id, lookback_days,
    )
    return all_entries
