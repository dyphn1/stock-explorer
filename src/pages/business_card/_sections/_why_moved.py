"""Business card section: Why Did This Move? (C188).

Renders an inline explanation of single-stock price movements
with plain-language narratives. Only shown when movement is significant (>3%).
"""
import streamlit as st
from src.core.i18n import t
from src.services.stock_movement_explainer import explain_movement
from src.pages._router_base import _info_card, _summary_card, _section_title, _confidence_badge, _section_title_with_read_time


def _render_why_moved(data: dict, client) -> None:
    """C188: Why Did This Move? — plain-language movement explanation.

    Shows direction emoji, magnitude percentage, narrative, and key concept.
    Only renders when movement is significant (>3%).
    Gracefully falls back for insufficient data.
    """
    stock_id = data["stock_id"]
    latest_price = data.get("latest_price")
    daily_price = data.get("daily_price")

    # ── Need at least current price and previous close ──
    if not latest_price:
        return

    try:
        current_price = float(latest_price.get("close", 0))
    except (TypeError, ValueError):
        return

    if current_price <= 0:
        return

    # Get previous close from daily_price DataFrame or latest_price dict
    previous_price = None
    if daily_price is not None and len(daily_price) >= 2:
        try:
            close_col = "close" if "close" in daily_price.columns else None
            if close_col is None:
                # Try common aliases
                for candidate in ["Close", "收盤價"]:
                    if candidate in daily_price.columns:
                        close_col = candidate
                        break
            if close_col:
                previous_price = float(daily_price.iloc[-2][close_col])
        except (IndexError, KeyError, TypeError, ValueError):
            previous_price = None

    if previous_price is None:
        # Fallback: try to compute from change field in latest_price
        try:
            change = float(latest_price.get("change", 0))
            previous_price = current_price - change
        except (TypeError, ValueError):
            return

    if previous_price <= 0:
        return

    # ── Get movement explanation ──
    movement_date = None
    if daily_price is not None and len(daily_price) >= 1:
        try:
            date_col = "date" if "date" in daily_price.columns else None
            if date_col is None:
                for candidate in ["Date", "日期", "trade_date"]:
                    if candidate in daily_price.columns:
                        date_col = candidate
                        break
            if date_col:
                movement_date = str(daily_price.iloc[-1][date_col])[:10]
        except (IndexError, KeyError):
            pass

    explanation = explain_movement(
        stock_id=stock_id,
        current_price=current_price,
        previous_price=previous_price,
        date=movement_date,
    )

    # ── Only show for significant movements (>3%) ──
    if explanation["magnitude"] == "minor":
        return

    # ── Render the section ──
    # C205: section title with read time badge
    movement_full_text = explanation.get("narrative", "") + " " + explanation.get("detail", "")
    _section_title_with_read_time(t("why_moved.section_title"), movement_full_text)

    # Direction emoji and magnitude
    direction_emoji = {
        "up": "📈",
        "down": "📉",
        "sideways": "↔️",
    }.get(explanation["direction"], "➡️")

    direction_label = {
        "up": t("why_moved.direction_up"),
        "down": t("why_moved.direction_down"),
        "sideways": t("why_moved.direction_sideways"),
    }.get(explanation["direction"], t("why_moved.direction_change"))

    magnitude_label = {
        "major": t("why_moved.magnitude_major"),
        "significant": t("why_moved.magnitude_significant"),
    }.get(explanation["magnitude"], "")

    change_pct = explanation["change_pct"]
    sign = "+" if change_pct >= 0 else ""

    # Main movement card
    movement_content = (
        f"{direction_emoji} **{magnitude_label}{direction_label} {sign}{change_pct:.1f}%**\n\n"
        f"{explanation['narrative']}"
    )

    border_color = "#27AE60" if explanation["direction"] == "up" else (
        "#E74C3C" if explanation["direction"] == "down" else "#F39C12"
    )
    _summary_card(t("why_moved.stock_price_change"), movement_content, direction_emoji, border_color=border_color)
    # C204: confidence badge
    st.caption(f"{_confidence_badge(0.9)} · {t('why_moved.confidence_note')}")

    # Detail explanation
    if explanation.get("detail"):
        _info_card(t("why_moved.detail_explanation"), explanation["detail"], "📖")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t('why_moved.confidence_note')}")

    # Key concept callout
    if explanation.get("key_concept"):
        _info_card(t("why_moved.key_concept"), explanation["key_concept"], "💡")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t('why_moved.confidence_note')}")
