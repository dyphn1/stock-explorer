"""
Investment Memo Service — C83
Business logic for investment memo template feature.
No streamlit imports.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def get_stock_suggestions(client: Any, query: str) -> pd.DataFrame:
    """Search stocks by name or ID for memo stock selector.

    Args:
        client: FinMindClient instance.
        query: Search string (stock_id or Chinese name).

    Returns:
        DataFrame of matching stocks, empty if no matches.
    """
    if not query or not query.strip():
        return pd.DataFrame()
    try:
        return client.search_stocks(query.strip())
    except Exception as exc:
        logger.warning("get_stock_suggestions failed for %r: %s", query, exc)
        return pd.DataFrame()


def validate_memo_input(data: dict) -> tuple[bool, str]:
    """Validate investment memo form input.

    Args:
        data: Dict with memo fields.

    Returns:
        (is_valid, error_message) — error_message empty if valid.
    """
    if not data.get("one_liner", "").strip():
        return False, "請填寫「一句話定位」"
    if not data.get("reasons", "").strip():
        return False, "請填寫「投資理由」"
    low = data.get("target_low")
    high = data.get("target_high")
    if low is not None and high is not None:
        if low < 0 or high < 0:
            return False, "目標價不能為負數"
        if low > high:
            return False, "目標價下限不能大於上限"
    confidence = data.get("confidence", 3)
    if not (1 <= confidence <= 5):
        return False, "信心水平必須在 1-5 之間"
    return True, ""


def format_memo_summary(memo_data: dict) -> dict:
    """Format saved memo data for display in _summary_card components.

    Args:
        memo_data: Raw memo dict from session_state.

    Returns:
        Formatted dict with display-ready strings.
    """
    confidence = memo_data.get("confidence", 3)
    confidence_labels = {
        1: "⭐ 很低",
        2: "⭐⭐ 低",
        3: "⭐⭐⭐ 中等",
        4: "⭐⭐⭐⭐ 高",
        5: "⭐⭐⭐⭐⭐ 很高",
    }
    low = memo_data.get("target_low")
    high = memo_data.get("target_high")
    if low is not None and high is not None:
        price_range = f"NT$ {low:,.0f} — {high:,.0f}"
    else:
        price_range = "未設定"

    return {
        "one_liner": memo_data.get("one_liner", ""),
        "reasons": memo_data.get("reasons", ""),
        "concerns": memo_data.get("concerns", "未填寫"),
        "key_metrics": memo_data.get("key_metrics", "未填寫"),
        "price_range": price_range,
        "confidence_label": confidence_labels.get(confidence, "⭐⭐⭐"),
        "notes": memo_data.get("notes", ""),
    }
