"""
C201 今日市場動態 — Daily Market Dashboard
Narrative-driven market overview: what happened in the Taiwan market today.
"""

import streamlit as st
import numpy as np
from datetime import datetime
from src.pages._router_base import _白话_card, _info_card, _summary_card, _section_title, _source_section
from src.core.i18n import t
from src.services.market_data import get_sector_grid_data
from src.services.adaptive_engine import get_all_recent_events


def _render_daily_market(client):
    """Daily Market Dashboard — main entry point."""
    st.markdown(f"## 📰 {t('daily_market.title')}")
    st.markdown(f"*{t('daily_market.subtitle')}*")
    st.markdown("---\n")

    # ── Load all market data via existing service ──
    with st.spinner(t("status.loading_page")):
        try:
            grid_data = get_sector_grid_data(client)
        except Exception as e:
            st.error(t("daily_market.error_load_failed", e=e))
            return

    all_stock_info = grid_data["all_stock_info"]
    sector_metrics = grid_data["sector_metrics"]
    summary_map = grid_data["summary_map"]
    sector_stocks = grid_data["sector_stocks"]

    if not summary_map:
        st.warning(t("daily_market.no_data"))
        return

    # ── Data freshness ──
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Section 1: Market Overview ──
    _render_overview(summary_map, sector_metrics)

    st.markdown("---\n")

    # ── Section 2: Market Sentiment ──
    _render_sentiment(summary_map)

    st.markdown("---\n")

    # ── Section 3: Sector Performance Strip ──
    _render_sector_strip(sector_metrics)

    st.markdown("---\n")

    # ── Section 4: Top Movers ──
    _render_top_movers(summary_map, sector_stocks)

    st.markdown("---\n")

    # ── Section 5: Key Events ──
    _render_key_events()

    # ── Data Sources ──
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        {"label": t("daily_market.sources.stock_info"), "api": "FinMind", "time": now_str},
        {"label": t("daily_market.sources.price_summary"), "api": "FinMind", "time": now_str},
        {"label": t("daily_market.sources.sector_data"), "api": "FinMind", "time": now_str},
        {"label": t("daily_market.sources.events"), "api": t("daily_market.sources.local_db"), "time": now_str},
    ]
    _source_section(sources, last_updated)

    # ── Disclaimer ──
    st.caption(t("daily_market.disclaimer"))


def _render_overview(summary_map: dict, sector_metrics: dict):
    """Section 1: One-paragraph market overview."""
    _section_title(t("daily_market.overview.title"))

    all_changes = [s["change"] for s in summary_map.values() if s.get("change") is not None]
    if not all_changes:
        _summary_card(t("daily_market.overview.title"), t("daily_market.no_data"))
        return

    # Compute market-level stats
    avg_change = float(np.mean(all_changes))
    up_count = sum(1 for c in all_changes if c > 0)
    down_count = sum(1 for c in all_changes if c < 0)
    total_stocks = len(all_changes)

    # Find leading/lagging sectors
    if sector_metrics:
        sorted_sectors = sorted(sector_metrics.items(), key=lambda x: x[1]["avg_change"], reverse=True)
        lead_sector = sorted_sectors[0]
        lag_sector = sorted_sectors[-1]
        sector_summary = t(
            "daily_market.overview.sector_lead_up",
            sector=lead_sector[0],
            pct=lead_sector[1]["avg_change"],
        )
    else:
        sector_summary = ""

    # Pick template based on direction
    if avg_change > 0.5:
        template_key = "daily_market.overview.template_bull"
    elif avg_change < -0.5:
        template_key = "daily_market.overview.template_bear"
    else:
        template_key = "daily_market.overview.template_flat"

    # Volume comment
    volume_comment = t("daily_market.overview.volume_normal")  # Simplified; could compare to MA

    overview_text = t(
        template_key,
        close=total_stocks * 100,  # Placeholder — real TAIEX value from index data
        abs_change=abs(avg_change),
        pct_change=avg_change,
        volume=total_stocks,  # Placeholder — no volume field in summary
        volume_comment=volume_comment,
        sector_summary=sector_summary,
    )

    _summary_card(t("daily_market.overview.title"), overview_text)


def _render_sentiment(summary_map: dict):
    """Section 2: Market sentiment indicators."""
    _section_title(t("daily_market.sentiment.title"))

    all_changes = [s["change"] for s in summary_map.values() if s.get("change") is not None]
    if not all_changes:
        st.info(t("daily_market.no_sentiment_data"))
        return

    up_count = sum(1 for c in all_changes if c > 0)
    down_count = sum(1 for c in all_changes if c < 0)
    flat_count = len(all_changes) - up_count - down_count

    # Market mood
    ad_ratio = up_count / max(down_count, 1)
    if ad_ratio >= 2.0:
        mood = t("daily_market.sentiment.mood_bullish")
    elif ad_ratio >= 0.8:
        mood = t("daily_market.sentiment.mood_neutral")
    else:
        mood = t("daily_market.sentiment.mood_bearish")

    # Total volume (placeholder — no volume field in summary)
    total_stocks = len(all_changes)
    volume_display = f"{total_stocks} {t('daily_market.sentiment.volume_unit')}"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _白话_card(
            t("daily_market.sentiment.ad_ratio"),
            f"{t('daily_market.sentiment.ad_ratio')}\n{t('daily_market.sentiment.ad_ratio_value', up=up_count, down=down_count)}",
            t("daily_market.flat_count", flat_count=flat_count),
        )
    with col2:
        _白话_card(
            t("daily_market.sentiment.volume"),
            volume_display,
            "",
        )
    with col3:
        _白话_card(
            t("daily_market.sentiment.mood"),
            mood,
            t("daily_market.ad_ratio_label", ratio=f"{ad_ratio:.1f}"),
        )
    with col4:
        _白话_card(
            t("daily_market.sentiment.up_count"),
            str(up_count),
            t("daily_market.sentiment.down_count") + f" {down_count}",
        )


def _render_sector_strip(sector_metrics: dict):
    """Section 3: Horizontal sector performance strip."""
    _section_title(t("daily_market.sectors.title"))

    if not sector_metrics:
        st.info(t("daily_market.no_sector_data"))
        return

    # Sort by avg change, take top 6
    sorted_sectors = sorted(
        sector_metrics.items(),
        key=lambda x: x[1]["avg_change"],
        reverse=True,
    )[:6]

    cols = st.columns(len(sorted_sectors))
    for i, (sector, metrics) in enumerate(sorted_sectors):
        chg = metrics["avg_change"]
        sign = "+" if chg > 0 else ""
        # FIX: Green (#27AE60) = positive/up, Red (#E74C3C) = negative/down
        color = "#27AE60" if chg > 0 else ("#E74C3C" if chg < 0 else "#7F8C8D")
        with cols[i]:
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:10px;padding:0.8rem;text-align:center;border-top:3px solid {color};">
                <div style="font-size:0.8rem;color:#7F8C8D;">{sector}</div>
                <div style="font-size:1.3rem;font-weight:700;color:{color};">{sign}{chg:.2f}%</div>
                <div style="font-size:0.7rem;color:#7F8C8D;">🟢{metrics['up']} 🔴{metrics['down']}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_top_movers(summary_map: dict, sector_stocks: dict):
    """Section 4: Top 5 gainers and losers."""
    _section_title(t("daily_market.movers.title"))

    # Build reverse mapping: stock_id -> sector
    stock_sector = {}
    for sector, sids in sector_stocks.items():
        for sid in sids:
            stock_sector[sid] = sector

    # Sort all stocks by change percentage
    all_stocks = []
    for s in summary_map.values():
        if s.get("change") is not None:
            # Compute percentage change: change / (latest_price - change) * 100
            latest_price = s.get("latest_price", 0) or 0
            prev_price = latest_price - s["change"]
            if prev_price > 0:
                pct_change = s["change"] / prev_price * 100
            else:
                pct_change = 0.0
            all_stocks.append({**s, "sector": stock_sector.get(s["stock_id"], ""), "pct_change": pct_change})

    if not all_stocks:
        st.info(t("daily_market.no_mover_data"))
        return

    all_stocks.sort(key=lambda x: x["pct_change"], reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {t('daily_market.movers.gainers')}")
        for rank, s in enumerate(all_stocks[:5], 1):
            _render_mover_row(rank, s, True)

    with col2:
        st.markdown(f"#### {t('daily_market.movers.losers')}")
        for rank, s in enumerate(reversed(all_stocks[-5:]), 1):
            _render_mover_row(rank, s, False)


def _render_mover_row(rank: int, s: dict, is_gainer: bool):
    """Render a single mover row."""
    pct_change = s.get("pct_change", s.get("change", 0))
    sign = "+" if pct_change > 0 else ""
    # FIX: Green (#27AE60) = gainers/positive, Red (#E74C3C) = losers/negative
    color = "#27AE60" if is_gainer else "#E74C3C"
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text(f"{t('daily_market.movers.rank', rank=rank)} {s.get('stock_name', s['stock_id'])} ({s['stock_id']})")
    with c2:
        st.markdown(f"<span style='color:{color};font-weight:700;'>{sign}{pct_change:.2f}%</span>", unsafe_allow_html=True)
    st.caption(f"{s.get('sector', '')} ｜ {t('daily_market.movers.price', price=s.get('latest_price', '—'))}")
    st.write("")


def _render_key_events():
    """Section 5: Key market events from adaptive engine."""
    _section_title(t("daily_market.events.title"))

    try:
        events = get_all_recent_events(days=1, limit=5)
    except Exception:
        events = []

    if not events:
        st.info(t("daily_market.events.empty"))
        return

    for event in events[:5]:
        event_title = event.get("title", event.get("event_type", ""))
        event_desc = event.get("description", event.get("implication", event.get("summary", "")))
        _info_card(event_title, event_desc)
