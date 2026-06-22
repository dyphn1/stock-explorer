"""
Business card section: Why Did This Move? (simple version).

Provides a plain-language explanation of recent price changes based on
institutional trading and price movement percentage.
"""
import streamlit as st
from src.core.i18n import t
from src.pages._router_base import _plain_card


def _render_why_did_this_move(data: dict, client) -> None:
    """Render a simple explanation for why the stock moved.
    
    Args:
        data: Dictionary containing stock data with latest_price and institutional keys
        client: FinMind client (not used in this simple version but kept for consistency)
    """
    # Get latest price data
    latest_price = data.get("latest_price", {})
    if not latest_price:
        # No price data available
        _plain_card(
            t("why_did_this_move.title"),
            t("why_did_this_move.no_data"),
            icon="💡"
        )
        return

    # Get price change
    price_change = latest_price.get("change", 0)

    # Get institutional data
    institutional = data.get("institutional")
    net_buying = 0

    if institutional is not None and hasattr(institutional, 'columns'):
        # If it's a DataFrame, calculate net buying from buy/sell columns
        try:
            # Assuming columns like 'buy', 'sell' or similar
            if 'buy' in institutional.columns and 'sell' in institutional.columns:
                # Sum across rows (if multiple institutional types) and calculate net
                total_buy = institutional['buy'].sum()
                total_sell = institutional['sell'].sum()
                net_buying = total_buy - total_sell
            elif 'net_buy' in institutional.columns:
                net_buying = institutional['net_buy'].sum()
        except Exception:
            # If calculation fails, default to 0
            net_buying = 0
    elif isinstance(institutional, dict):
        # If it's a dict, try to get net buying directly
        if 'net_buy' in institutional:
            net_buying = institutional['net_buy']
        elif 'buy' in institutional and 'sell' in institutional:
            # Assume values are lists or scalars
            buy = institutional['buy']
            sell = institutional['sell']
            # If they are lists, sum them; if scalars, use as is
            total_buy = sum(buy) if isinstance(buy, list) else buy
            total_sell = sum(sell) if isinstance(sell, list) else sell
            net_buying = total_buy - total_sell
        else:
            net_buying = 0
    else:
        net_buying = 0

    # Check if there is any significant movement to explain
    has_significant_movement = (
        net_buying != 0 or
        price_change > 5 or
        price_change < -5
    )

    if not has_significant_movement:
        # No significant movement, show no data message
        _plain_card(
            t("why_did_this_move.title"),
            t("why_did_this_move.no_data"),
            icon="💡"
        )
        return

    # Generate explanation based on conditions
    explanations = []

    # Check institutional trading
    if net_buying > 0:
        explanations.append(t("why_did_this_move.institutional_buying"))
    elif net_buying < 0:
        explanations.append(t("why_did_this_move.institutional_selling"))

    # Check price change percentage
    if price_change > 5:  # Greater than 5%
        explanations.append(t("why_did_this_move.price_surge"))
    elif price_change < -5:  # Less than -5%
        explanations.append(t("why_did_this_move.price_drop"))

    # Always add the general note about checking news
    explanations.append(t("why_did_this_move.check_news"))

    # Combine explanations
    if explanations:
        explanation_text = "\n\n".join(explanations)
    else:
        explanation_text = t("why_did_this_move.no_data")

    # Determine card color based on price change
    if price_change > 0:
        border_color = "#27AE60"  # Green for up
    elif price_change < 0:
        border_color = "#E74C3C"  # Red for down
    else:
        border_color = "#95A5A6"  # Gray for no change

    # Render the card
    _plain_card(
        t("why_did_this_move.title"),
        explanation_text,
        icon="💡",
        border_color=border_color
    )