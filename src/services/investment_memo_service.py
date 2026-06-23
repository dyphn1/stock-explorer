"""
Investment Memo Service — C83
Business logic for investment memo template feature.
No streamlit imports.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from src.core.i18n import t

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
        return False, t("investment_memo.validation.one_liner_empty")
    if not data.get("reasons", "").strip():
        return False, t("investment_memo.validation.reasons_empty")
    low = data.get("target_low")
    high = data.get("target_high")
    if low is not None and high is not None:
        if low < 0 or high < 0:
            return False, t("investment_memo.validation.target_price_negative")
        if low > high:
            return False, t("investment_memo.validation.target_price_low_gt_high")
    confidence = data.get("confidence", 3)
    if not (1 <= confidence <= 5):
        return False, t("investment_memo.validation.confidence_out_of_range")
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
        1: t("investment_memo.confidence.very_low"),
        2: t("investment_memo.confidence.low"),
        3: t("investment_memo.confidence.medium"),
        4: t("investment_memo.confidence.high"),
        5: t("investment_memo.confidence.very_high"),
    }
    low = memo_data.get("target_low")
    high = memo_data.get("target_high")
    if low is not None and high is not None:
        price_range = f"NT$ {low:,.0f} — {high:,.0f}"
    else:
        price_range = t("investment_memo.default.price_range_unset")

    return {
        "one_liner": memo_data.get("one_liner", ""),
        "reasons": memo_data.get("reasons", ""),
        "concerns": memo_data.get("concerns", t("investment_memo.default.not_filled")),
        "key_metrics": memo_data.get("key_metrics", t("investment_memo.default.not_filled")),
        "price_range": price_range,
        "confidence_label": confidence_labels.get(confidence, "⭐⭐⭐"),
        "notes": memo_data.get("notes", ""),
    }
