"""
Story Arc Detector — C202
Auto-detect narrative arcs on company event timeline.

Pure Python service — no Streamlit imports, no API calls.
Uses only local TimelineEntry data already loaded in memory.

Algorithm: non-overlapping 6-month buckets (Jan-Jun, Jul-Dec).
Each bucket is classified into one of four arc labels based on
severity-weighted event scores. Arc labels are only emitted at
transition points (where classification changes between consecutive
buckets), not on every entry.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TypedDict

from src.services.timeline_service import TimelineEntry

logger = logging.getLogger(__name__)

# ── Severity → numeric score ──────────────────────────────

_SEVERITY_SCORES = {"high": 3, "medium": 2, "low": 1}

# ── Arc label constants ────────────────────────────────────

ARC_GROWTH = "成長期"
ARC_DECLINE = "調整期"
ARC_VOLATILE = "震盪期"
ARC_RECOVERY = "復甦期"

_ARC_EMOJI = {
    ARC_GROWTH: "📈",
    ARC_DECLINE: "📉",
    ARC_VOLATILE: "🔄",
    ARC_RECOVERY: "🌱",
}

_ARC_DESCRIPTIONS = {
    ARC_GROWTH: "過去6個月營收與市場評價偏向正面，整體趨勢向上",
    ARC_DECLINE: "過去6個月面臨較多負面事件，市場信心有所回落",
    ARC_VOLATILE: "過去6個月正負事件交織，市場看法分歧",
    ARC_RECOVERY: "調整後出現正面訊號，市場情緒逐步回暖",
}


class ArcLabel(TypedDict):
    """A detected story arc label for a time bucket."""
    arc_label: str
    arc_emoji: str
    arc_description: str
    bucket_start: str       # "YYYY-MM" start of bucket
    bucket_end: str         # "YYYY-MM" end of bucket
    event_count: int
    score: float


# ── Internal helpers ───────────────────────────────────────

def _bucket_key(date_str: str) -> str:
    """Convert a date string to a 6-month bucket key.

    Buckets: H1 (Jan-Jun) → "YYYY-01", H2 (Jul-Dec) → "YYYY-07".
    """
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
    except (ValueError, TypeError):
        return ""
    if dt.month <= 6:
        return f"{dt.year}-01"
    else:
        return f"{dt.year}-07"


def _bucket_label(bucket_key: str) -> str:
    """Human-readable bucket label like '2024 上半年' / '2024 下半年'."""
    if not bucket_key:
        return ""
    year, half = bucket_key.split("-")
    return f"{year} 上半年" if half == "01" else f"{year} 下半年"


def _score_bucket(entries: list[TimelineEntry]) -> float:
    """Compute a severity-weighted score for a bucket of entries.

    Positive score → leaning positive/growth.
    Negative score → leaning negative/decline.
    Near zero → mixed/volatile.
    """
    score = 0.0
    for e in entries:
        sev = e.get("severity", "low")
        pts = _SEVERITY_SCORES.get(sev, 1)
        etype = e.get("type", "")
        # Negative event types flip sign
        if etype in ("price_abnormal",):
            score -= pts
        else:
            score += pts
    return score


def _classify_bucket(score: float, event_count: int, min_events: int = 3) -> str:
    """Classify a bucket into an arc label.

    Thresholds designed to require meaningful signal:
    - score >= 4  → strong positive → 成長期
    - score <= -4 → strong negative → 調整期
    - score >= 1  → mild positive  → 復甦期 (recovery)
    - otherwise    → mixed          → 震盪期
    """
    if event_count < min_events:
        return ""  # insufficient data → no label
    if score >= 4:
        return ARC_GROWTH
    elif score <= -4:
        return ARC_DECLINE
    elif score >= 1:
        return ARC_RECOVERY
    else:
        return ARC_VOLATILE


# ── Public API ─────────────────────────────────────────────

def detect_arcs(
    entries: list[TimelineEntry],
    min_events: int = 3,
) -> list[ArcLabel]:
    """Detect story arc labels from a list of timeline entries.

    Groups entries into non-overlapping 6-month buckets, computes
    a severity-weighted score for each bucket, and classifies
    each into one of four arc labels. Only returns labels for
    buckets with >= min_events entries, and only at transition
    points (where the label differs from the previous bucket).

    Args:
        entries: TimelineEntry list (e.g. from get_timeline()).
        min_events: Minimum events in a bucket to assign a label.

    Returns:
        List of ArcLabel dicts, one per transition point.
        Empty list if no arcs detected.
    """
    if not entries:
        return []

    # Group entries by bucket
    buckets: dict[str, list[TimelineEntry]] = {}
    for e in entries:
        dk = _bucket_key(e.get("date", ""))
        if not dk:
            continue
        if dk not in buckets:
            buckets[dk] = []
        buckets[dk].append(e)

    # Classify each bucket in chronological order
    classified: list[tuple[str, str, int, float]] = []  # (bucket_key, label, count, score)
    for bk in sorted(buckets.keys()):
        bk_entries = buckets[bk]
        n = len(bk_entries)
        score = _score_bucket(bk_entries)
        label = _classify_bucket(score, n, min_events)
        classified.append((bk, label, n, score))

    # Find transition points: where label changes from previous bucket
    arcs: list[ArcLabel] = []
    prev_label = ""
    for bk, label, n, score in classified:
        if not label:
            # No label for this bucket (insufficient events)
            # Still update prev_label to break the chain
            prev_label = ""
            continue
        if label != prev_label:
            # Transition detected
            year_half = bk.split("-")
            bucket_start = f"{year_half[0]}-{'01' if year_half[1] == '01' else '07'}-01"
            bucket_end = f"{year_half[0]}-{'06-30' if year_half[1] == '01' else '12-31'}"
            arcs.append(ArcLabel(
                arc_label=label,
                arc_emoji=_ARC_EMOJI.get(label, ""),
                arc_description=_ARC_DESCRIPTIONS.get(label, ""),
                bucket_start=bucket_start,
                bucket_end=bucket_end,
                event_count=n,
                score=round(score, 1),
            ))
            prev_label = label
        # If same label as previous, skip (not a transition)

    logger.info(
        "story_arc_detector: %d arcs detected from %d entries across %d buckets",
        len(arcs), len(entries), len(buckets),
    )
    return arcs


def get_arc_legend() -> list[dict]:
    """Return arc legend data for UI rendering."""
    return [
        {"label": ARC_GROWTH, "emoji": "📈", "description": _ARC_DESCRIPTIONS[ARC_GROWTH]},
        {"label": ARC_DECLINE, "emoji": "📉", "description": _ARC_DESCRIPTIONS[ARC_DECLINE]},
        {"label": ARC_VOLATILE, "emoji": "🔄", "description": _ARC_DESCRIPTIONS[ARC_VOLATILE]},
        {"label": ARC_RECOVERY, "emoji": "🌱", "description": _ARC_DESCRIPTIONS[ARC_RECOVERY]},
    ]
