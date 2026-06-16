"""
Debate Cards Page — C199
Bear vs Bull debate cards for a stock.

Two-column layout showing bull and bear arguments side by side,
with evidence balance indicator and four-safeguard pattern.
"""
from __future__ import annotations

import streamlit as st

from src.core.i18n import t
from src.pages._router_base import _section_title, _info_card
from src.services.debate_engine import (
    generate_debate,
    get_debate_summary,
    DebatePoint,
    DebateSummary,
)
from src.services.financial_metrics import calc_extra_metrics


def _render_verdict_banner(summary: dict | DebateSummary) -> None:
    """Render the evidence balance indicator at the top."""
    verdict_key = summary["verdict_key"]
    bull_count = summary["bull_count"]
    bear_count = summary["bear_count"]

    if verdict_key == "debate.bull_strong":
        emoji = "🟢"
        color = "#27AE60"
    elif verdict_key == "debate.bear_strong":
        emoji = "🔴"
        color = "#E74C3C"
    else:
        emoji = "🟡"
        color = "#F39C12"

    verdict_text = t(verdict_key)
    st.markdown(
        f"""
        <div style="
            background: {color}15;
            border-left: 4px solid {color};
            padding: 0.75em 1em;
            border-radius: 4px;
            margin: 0.5em 0 1em 0;
        ">
            <strong>{emoji} {verdict_text}</strong>
            <span style="color: #7F8C8D; font-size: 0.85em; margin-left: 1em;">
                {t('debate.bull_case')}: {bull_count} · {t('debate.bear_case')}: {bear_count}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_debate_card(point: DebatePoint, index: int, stock_id: str) -> None:
    """Render a single debate argument card."""
    side = point["side"]
    metric = point["metric"]
    value = point["value"]
    peer_avg = point["peer_avg"]
    argument_key = point["argument_key"]
    icon = point["icon"]
    strength = point["strength"]

    # Resolve display text via i18n
    argument_text = t(argument_key, value=f"{value:.1f}", peer_avg=f"{peer_avg:.1f}" if peer_avg is not None else "N/A")
    metric_label = t(f"metric.{metric}") if metric else metric

    # Color based on side
    if side == "bull":
        border_color = "#27AE60"
        bg_color = "#EAFAF1"
    else:
        border_color = "#E74C3C"
        bg_color = "#FDEDEC"

    # Strength bar
    strength_pct = int(strength * 100)

    st.markdown(
        f"""
        <div style="
            background: {bg_color};
            border-left: 4px solid {border_color};
            padding: 0.75em 1em;
            border-radius: 4px;
            margin: 0.5em 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{icon} {metric_label}</strong>
                <span style="font-size: 0.75em; color: #7F8C8D;">{t('debate.auto_generated')}</span>
            </div>
            <div style="margin: 0.5em 0;">
                {argument_text}
            </div>
            <div style="font-size: 0.8em; color: #7F8C8D;">
                {t('debate.confidence')}: <div style="
                    display: inline-block;
                    width: 60px;
                    height: 8px;
                    background: #ECF0F1;
                    border-radius: 4px;
                    vertical-align: middle;
                    margin-left: 4px;
                "><div style="
                    width: {strength_pct}%;
                    height: 100%;
                    background: {border_color};
                    border-radius: 4px;
                "></div></div> {strength_pct}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_debate_cards_page(data: dict, client) -> None:
    """C199 Bear vs Bull Debate Cards page.

    Shows bull and bear arguments side by side with evidence balance.

    Args:
        data: Standard page data dict with stock_id, stock_name, etc.
        client: FinMindClient instance.
    """
    stock_id = data["stock_id"]
    stock_name = data.get("stock_name", "")

    # Page header
    display_name = f"{stock_name} ({stock_id})" if stock_name else stock_id
    _section_title(f"⚖️ {t('debate.title')} — {display_name}")

    # Calculate metrics
    with st.spinner(t("status.loading")):
        try:
            financial_df = data.get("financial")
            balance_sheet_df = data.get("balance_sheet")
            monthly_revenue_df = data.get("monthly_revenue")
            extra_metrics = calc_extra_metrics(financial_df, balance_sheet_df, monthly_revenue_df)
        except Exception as exc:
            st.error(f"{t('error.no_data')}: {exc}")
            return

    # Generate debate points
    # Note: peer_metrics would come from peer_comparison service if available
    # For now, pass empty dict — the engine will skip metrics without peer data
    points = generate_debate(data, extra_metrics, peer_metrics={})

    if not points:
        _info_card(
            title=t("debate.no_data"),
            content=t("debate.no_data_detail"),
            icon="📭",
        )
        # Disclaimer even for empty state
        st.markdown("---")
        st.caption(t("debate.disclaimer"))
        return

    # Summary
    summary = get_debate_summary(points)
    _render_verdict_banner(summary)

    # Two-column layout
    bull_points = [p for p in points if p["side"] == "bull"]
    bear_points = [p for p in points if p["side"] == "bear"]

    col_bull, col_bear = st.columns(2)

    with col_bull:
        st.markdown(f"### 🟢 {t('debate.bull_case')}")
        st.caption(f"{summary['bull_count']} {t('debate.evidence')}")
        for i, point in enumerate(bull_points):
            _render_debate_card(point, i, stock_id)

    with col_bear:
        st.markdown(f"### 🔴 {t('debate.bear_case')}")
        st.caption(f"{summary['bear_count']} {t('debate.evidence')}")
        for i, point in enumerate(bear_points):
            _render_debate_card(point, i, stock_id)

    # Verdict section
    st.markdown("---")
    _section_title(t("debate.summary"))
    verdict_text = t(summary["verdict_key"])
    st.info(f"⚖️ **{verdict_text}**")

    # Four-safeguard: Disclaimer at bottom
    st.markdown("---")
    st.caption(t("debate.disclaimer"))
