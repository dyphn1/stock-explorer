"""
Debate Engine — C199
Generate bull/bear debate arguments from stock data.

Pure Python service — no Streamlit imports, no API calls.
Uses only data already loaded in memory.

i18n strategy: this service returns i18n keys (e.g. "debate.roe_bull").
The page layer calls t() to resolve them.
"""
from __future__ import annotations

import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class DebatePoint(TypedDict):
    """A single bull or bear argument."""
    side: str          # "bull" or "bear"
    metric: str        # e.g. "roe", "revenue_yoy"
    value: float       # actual value
    peer_avg: float | None  # industry average (None if unavailable)
    argument_key: str  # i18n key for the argument text
    icon: str          # emoji
    strength: float    # 0.0-1.0 evidence strength


class DebateSummary(TypedDict):
    """Summary of a debate."""
    verdict_key: str   # "debate.bull_strong" | "debate.bear_strong" | "debate.neutral"
    bull_count: int
    bear_count: int
    bull_strength: float
    bear_strength: float


# ── Metric configuration ─────────────────────────────────────
# For "direction": "higher_is_bullish" means higher value → bull argument.
# For "direction": "lower_is_bullish" means lower value → bull argument (e.g. debt_ratio).

_METRICS = [
    {"key": "roe", "direction": "higher_is_bullish", "bull_key": "debate.roe_bull", "bear_key": "debate.roe_bear", "icon_bull": "📈", "bear_icon": "📉"},
    {"key": "revenue_yoy", "direction": "higher_is_bullish", "bull_key": "debate.revenue_yoy_bull", "bear_key": "debate.revenue_yoy_bear", "icon_bull": "📈", "bear_icon": "📉"},
    {"key": "gross_margin", "direction": "higher_is_bullish", "bull_key": "debate.gross_margin_bull", "bear_key": "debate.gross_margin_bear", "icon_bull": "📈", "bear_icon": "📉"},
    {"key": "operating_margin", "direction": "higher_is_bullish", "bull_key": "debate.operating_margin_bull", "bear_key": "debate.operating_margin_bear", "icon_bull": "📈", "bear_icon": "📉"},
    {"key": "net_margin", "direction": "higher_is_bullish", "bull_key": "debate.net_margin_bull", "bear_key": "debate.net_margin_bear", "icon_bull": "📈", "bear_icon": "📉"},
    {"key": "debt_ratio", "direction": "lower_is_bullish", "bull_key": "debate.debt_ratio_bull", "bear_key": "debate.debt_ratio_bear", "icon_bull": "🛡️", "bear_icon": "⚠️"},
    {"key": "current_ratio", "direction": "higher_is_bullish", "bull_key": "debate.current_ratio_bull", "bear_key": "debate.current_ratio_bear", "icon_bull": "🛡️", "bear_icon": "⚠️"},
    {"key": "dividend_yield", "direction": "higher_is_bullish", "bull_key": "debate.dividend_yield_bull", "bear_key": "debate.dividend_yield_bear", "icon_bull": "💰", "bear_icon": "📉"},
]

# Banned words that must not appear in any argument (investment advice language)
_BANNED_WORDS = [
    "買進", "賣出", "買入", "拋出", "加碼", "減碼", "做多", "做空",
    "建議", "推薦", "強力買進", "目標價", "漲到", "跌到",
    "buy", "sell", "strong buy", "target price",
]


def _calc_strength(value: float, peer_avg: float) -> float:
    """Calculate evidence strength based on magnitude of difference.

    Returns 0.0-1.0, capped at 1.0.
    Uses relative difference: |value - peer_avg| / max(|peer_avg|, 1) * 0.5
    """
    if peer_avg == 0:
        return 0.3  # modest strength if no peer baseline
    rel_diff = abs(value - peer_avg) / max(abs(peer_avg), 1)
    return min(rel_diff * 0.5, 1.0)


def _check_banned(text: str) -> bool:
    """Return True if text contains banned words."""
    return any(word in text for word in _BANNED_WORDS)

def validate_debate_text(text: str) -> bool:
    """Validate debate text for banned words."""
    return _check_banned(text)



def generate_debate(
    data: dict,
    extra_metrics: dict,
    peer_metrics: dict | None = None,
) -> list[DebatePoint]:
    """Generate bull/bear arguments from stock data.

    Rules-based approach (no LLM):
    - Compare each metric vs industry average
    - Generate bull argument if metric > peer_avg (or metric < peer_avg for inverse metrics)
    - Strength based on magnitude of difference
    - Max 6 points per side, min 1 per side (if any data available)

    Args:
        data: Standard page data dict (stock_id, stock_name, etc.)
        extra_metrics: Dict from calc_extra_metrics() with roe, revenue_yoy, etc.
        peer_metrics: Optional dict of industry average metrics (same keys as extra_metrics).

    Returns:
        List of DebatePoint dicts. Empty list if no arguments generated.
    """
    if peer_metrics is None:
        peer_metrics = {}

    points: list[DebatePoint] = []
    bull_count = 0
    bear_count = 0

    for metric_cfg in _METRICS:
        metric_key = metric_cfg["key"]
        value = extra_metrics.get(metric_key)
        if value is None:
            continue

        peer_avg = peer_metrics.get(metric_key)
        if peer_avg is None:
            # No peer data — skip this metric
            continue

        direction = metric_cfg["direction"]
        is_bullish = (value >= peer_avg) if direction == "higher_is_bullish" else (value <= peer_avg)

        strength = _calc_strength(value, peer_avg)
        if strength < 0.05:
            # Too close to call — skip
            continue

        if is_bullish:
            if bull_count >= 6:
                continue
            point = DebatePoint(
                side="bull",
                metric=metric_key,
                value=value,
                peer_avg=peer_avg,
                argument_key=metric_cfg["bull_key"],
                icon=metric_cfg["icon_bull"],
                strength=strength,
            )
            bull_count += 1
        else:
            if bear_count >= 6:
                continue
            point = DebatePoint(
                side="bear",
                metric=metric_key,
                value=value,
                peer_avg=peer_avg,
                argument_key=metric_cfg["bear_key"],
                icon=metric_cfg["bear_icon"],
                strength=strength,
            )
            bear_count += 1

        points.append(point)

    logger.info(
        "debate_engine: %d points generated (%d bull, %d bear)",
        len(points), bull_count, bear_count,
    )
    return points


def get_debate_summary(points: list[DebatePoint]) -> DebateSummary:
    """Summarize a debate from generated points.

    Args:
        points: List of DebatePoint from generate_debate().

    Returns:
        DebateSummary with verdict key and counts.
    """
    bull_points = [p for p in points if p["side"] == "bull"]
    bear_points = [p for p in points if p["side"] == "bear"]

    bull_strength = sum(p["strength"] for p in bull_points)
    bear_strength = sum(p["strength"] for p in bear_points)

    diff = bull_strength - bear_strength
    if diff > 0.5:
        verdict_key = "debate.bull_strong"
    elif diff < -0.5:
        verdict_key = "debate.bear_strong"
    else:
        verdict_key = "debate.neutral"

    return DebateSummary(
        verdict_key=verdict_key,
        bull_count=len(bull_points),
        bear_count=len(bear_points),
        bull_strength=round(bull_strength, 2),
        bear_strength=round(bear_strength, 2),
    )
