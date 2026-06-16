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

i18n strategy: this service returns arc type keys (e.g. "growth")
and description keys (e.g. "story_arc.growth_description").
The page layer calls t() to resolve them.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TypedDict

from src.services.timeline_service import TimelineEntry

logger = logging.getLogger(__name__)

# ── Severity → numeric score ──────────────────────────────

_SEVERITY_SCORES = {"high": 3, "medium": 2, "low": 1}

# ── Arc type constants (i18n keys, NOT display text) ──────

ARC_GROWTH = "growth"
ARC_DECLINE = "decline"
ARC_VOLATILE = "volatile"
ARC_RECOVERY = "recovery"

_ARC_EMOJI = {
    ARC_GROWTH: "📈",
    ARC_DECLINE: "📉",
    ARC_VOLATILE: "🔄",
    ARC_RECOVERY: "🌱",
}

_ARC_DESCRIPTION_KEYS = {
    ARC_GROWTH: "story_arc.growth_description",
    ARC_DECLINE: "story_arc.decline_description",
    ARC_VOLATILE: "story_arc.volatile_description",
    ARC_RECOVERY: "story_arc.recovery_description",
}


class ArcLabel(TypedDict):
    """A detected story arc label for a time bucket."""
    arc_key: str              # i18n key: "growth", "decline", "volatile", "recovery"
    arc_emoji: str
    arc_description_key: str  # i18n key for description text
    bucket_start: str         # "YYYY-MM" start of bucket
    bucket_end: str           # "YYYY-MM" end of bucket
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
    """Classify a bucket into an arc type key.

    Thresholds designed to require meaningful signal:
    - score >= 4  → strong positive → growth
    - score <= -4 → strong negative → decline
    - score >= 1  → mild positive  → recovery
    - otherwise    → mixed          → volatile
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
    each into one of four arc types. Only returns labels for
    buckets with >= min_events entries, and only at transition
    points (where the label differs from the previous bucket).

    Returns arc type keys (e.g. "growth") — the page layer
    must call t("story_arc.{key}") for display text.

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
                arc_key=label,
                arc_emoji=_ARC_EMOJI.get(label, ""),
                arc_description_key=_ARC_DESCRIPTION_KEYS.get(label, ""),
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
    """Return arc legend data for UI rendering.

    Returns list of dicts with i18n keys — page layer calls t()
    to resolve display text.
    """
    return [
        {"key": ARC_GROWTH, "emoji": "📈", "label_key": "story_arc.growth", "desc_key": "story_arc.growth_description"},
        {"key": ARC_DECLINE, "emoji": "📉", "label_key": "story_arc.decline", "desc_key": "story_arc.decline_description"},
        {"key": ARC_VOLATILE, "emoji": "🔄", "label_key": "story_arc.volatile", "desc_key": "story_arc.volatile_description"},
        {"key": ARC_RECOVERY, "emoji": "🌱", "label_key": "story_arc.recovery", "desc_key": "story_arc.recovery_description"},
    ]
