"""
Sector Heatmap — C51 Visual Market Overview
Displays a color-coded grid of Taiwan stock sectors showing performance.
Uses market_data service for data access (D-044).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.core.i18n import t
from src.pages.url_sync import navigate_to
from src.pages._router_base import _白话_card, _info_card, _section_title
from src.services.market_data import (
    compute_sector_metrics,
    get_all_stock_info,
    get_all_summaries,
    get_sector_stocks,
)


# ── Sector color palette (PPT-style, distinct) ────────────
_SECTOR_COLORS = [
    "#3498DB", "#27AE60", "#E74C3C", "#9B59B6",
    "#F39C12", "#1ABC9C", "#E67E22", "#2980B9",
    "#2ECC71", "#8E44AD", "#F1C40F", "#D35400",
    "#16A085", "#C0392B", "#7F8C8D", "#2C3E50",
]


def _perf_color(change_pct: float | None) -> str:
    """Return PPT-style color for a performance value.
    台股慣例：紅漲綠跌
    """
    if change_pct is None:
        return "#7F8C8D"  # gray = no data
    if change_pct > 0:
        return "#E74C3C"  # red = up (Taiwan convention)
    if change_pct < 0:
        return "#27AE60"  # green = down (Taiwan convention)
    return "#7F8C8D"


def _perf_bg_color(change_pct: float | None, alpha: float = 0.15) -> str:
    """Return semi-transparent bg color for heatmap cells."""
    if change_pct is None:
        return f"rgba(127,140,141,{alpha})"
    if change_pct > 0:
        return f"rgba(231,76,60,{alpha})"
    if change_pct < 0:
        return f"rgba(39,174,96,{alpha})"
    return f"rgba(127,140,141,{alpha})"


def _format_pct(value: float | None) -> str:
    """Format percentage with sign."""
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def _render_sector_heatmap(client):
    """Sector Heatmap main page — visual market overview."""
    st.markdown(f"## 🗺️ {t('sector_heatmap.title')}")
    st.markdown(f"*{t('sector_heatmap.subtitle')}*")
    st.markdown("---\n")

    # ── Load stock info via market_data service ────────────
    with st.spinner(t('sector_heatmap.loading_data')):
        try:
            all_stock_info = get_all_stock_info(client)
        except Exception as e:
            st.error(t('sector_heatmap.fetch_error', error=e))
            return

    if all_stock_info is None or len(all_stock_info) == 0:
        st.warning(t('sector_heatmap.no_data'))
        return

    # Ensure required columns exist
    for col in ("stock_id", "stock_name", "industry_category"):
        if col not in all_stock_info.columns:
            st.error(t('sector_heatmap.missing_col', col=col))
            return

    # ── Build industry → stock_ids mapping via service ────
    sector_stocks = get_sector_stocks(all_stock_info)

    if not sector_stocks:
        st.info(t('sector_heatmap.no_industry_data'))
        return

    # ── Fetch prices via market_data service ───────────────
    progress = st.progress(0, text=t('sector_heatmap.fetching_prices'))
    all_stock_ids = sorted(all_stock_info["stock_id"].unique())
    total_stocks = len(all_stock_ids)
    batch_size = 50

    def _update_progress(fraction: float):
        progress.progress(
            fraction,
            text=t('sector_heatmap.processing_count', processed=int(fraction * total_stocks), total=total_stocks),
        )

    try:
        _, summary_map = get_all_summaries(
            client,
            all_stock_info=all_stock_info,
            batch_size=batch_size,
            progress_callback=_update_progress,
        )
    except Exception as e:
        progress.empty()
        st.warning(t('sector_heatmap.fetch_error', error=e))
        return

    progress.empty()

    if not summary_map:
        st.warning(t('sector_heatmap.no_price_data'))
        return

    # ── Compute sector-level metrics via service ───────────
    sector_metrics = compute_sector_metrics(summary_map, sector_stocks)

    if not sector_metrics:
        st.info(t('sector_heatmap.no_price_data_to_analyze'))
        return

    # ── Summary KPIs ───────────────────────────────────────
    all_avg_changes = [m["avg_change"] for m in sector_metrics.values()]
    overall_avg = float(np.mean(all_avg_changes)) if all_avg_changes else 0
    leading_sector = max(sector_metrics.items(), key=lambda x: x[1]["avg_change"])
    lagging_sector = min(sector_metrics.items(), key=lambda x: x[1]["avg_change"])

    up_sectors = sum(1 for m in sector_metrics.values() if m["avg_change"] > 0)
    down_sectors = sum(1 for m in sector_metrics.values() if m["avg_change"] < 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _白话_card(
            t('sector_heatmap.avg_change'),
            _format_pct(overall_avg),
            t('sector_heatmap.avg_change_help'),
        )
    with col2:
        _白话_card(
            t('sector_heatmap.strongest_sector'),
            leading_sector[0],
            t('sector_heatmap.avg_change_value', value=_format_pct(leading_sector[1]['avg_change'])),
        )
    with col3:
        _白话_card(
            t('sector_heatmap.weakest_sector'),
            lagging_sector[0],
            t('sector_heatmap.avg_change_value', value=_format_pct(lagging_sector[1]['avg_change'])),
        )
    with col4:
        _白话_card(
            t('sector_heatmap.up_down_count'),
            f"🔴 {up_sectors} / 🟢 {down_sectors}",
            t('sector_heatmap.up_down_help'),
        )

    st.markdown("---\n")

    # ── Treemap heatmap ─────────────────────────────────────
    _render_treemap(sector_metrics)

    st.markdown("---\n")

    # ── Sector Detail Grid ──────────────────────────────────
    _render_sector_grid(sector_metrics)

    st.markdown("---\n")

    # ── Top movers per sector ───────────────────────────────
    _render_top_movers(summary_map, sector_stocks)


def _render_treemap(sector_metrics: dict):
    """Render a treemap showing sector performance."""
    st.markdown(f"### 📊 {t('sector_heatmap.treemap_title')}")

    # Sort by average change for better color distribution
    sorted_sectors = sorted(
        sector_metrics.items(),
        key=lambda x: x[1]["avg_change"],
        reverse=True,
    )

    labels = []
    parents = []
    values = []
    colors = []
    hover_texts = []

    for sector, metrics in sorted_sectors:
        avg_chg = metrics["avg_change"]
        count = metrics["count"]
        up = metrics["up"]
        down = metrics["down"]
        flat = metrics["flat"]

        # Sector node
        labels.append(f"{sector}")
        parents.append("")
        values.append(count)
        colors.append(_perf_bg_color(avg_chg, 0.6))
        hover_texts.append(
            f"<b>{sector}</b><br>"
            f"{t('sector_heatmap.avg_change')}: {_format_pct(avg_chg)}<br>"
            f"{t('sector_heatmap.up')}: {up} / {t('sector_heatmap.down')}: {down} / {t('sector_heatmap.flat')}: {flat}<br>"
            f"{t('sector_heatmap.count')} {count} {t('sector_heatmap.stocks_unit')}"
        )

        # Stock nodes (top 5 by abs change for readability)
        stocks = sorted(
            metrics["stocks"],
            key=lambda s: abs(s.get("change") or 0),
            reverse=True,
        )[:5]

        for s in stocks:
            chg = s.get("change")
            stock_label = f"{s.get('stock_name', s['stock_id'])}"
            labels.append(stock_label)
            parents.append(sector)
            values.append(1)
            colors.append(_perf_bg_color(chg, 0.4 if chg is not None else 0.1))
            hover_texts.append(
                f"<b>{stock_label} ({s['stock_id']})</b><br>"
                f"{t('sector_heatmap.change')}: {_format_pct(chg)}"
            )

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(width=1, color="white"),
        ),
        textfont=dict(size=13, color="#2C3E50"),
        textinfo="label",
        hovertext=hover_texts,
        hovertemplate="%{hovertext}<extra></extra>",
        pathbar=dict(visible=False),
    ))

    fig.update_layout(
        title=dict(
            text=t('sector_heatmap.treemap_legend'),
            font=dict(size=16, color="#2C3E50"),
            x=0.5,
        ),
        margin=dict(t=50, b=20, l=20, r=20),
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_sector_grid(sector_metrics: dict):
    """Render a detailed grid table of sector performance."""
    st.markdown(f"### 🏭 {t('sector_heatmap.sector_ranking')}")

    # Sort by avg change descending
    sorted_sectors = sorted(
        sector_metrics.items(),
        key=lambda x: x[1]["avg_change"],
        reverse=True,
    )

    df = pd.DataFrame([
        {
            t("sector_heatmap.rank_col", rank=""): idx + 1,
            t("sector_heatmap.industry_col"): sector,
            t("sector_heatmap.avg_change_col"): _format_pct(m["avg_change"]),
            t("sector_heatmap.up_col"): m["up"],
            t("sector_heatmap.down_col"): m["down"],
            t("sector_heatmap.flat_col"): m["flat"],
            t("sector_heatmap.count_col"): m["count"],
            "_avg_change": m["avg_change"],
        }
        for idx, (sector, m) in enumerate(sorted_sectors)
    ])

    # Render as color-coded grid using _白话_card
    cols_per_row = 4
    for i in range(0, len(df), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(df):
                break
            row = df.iloc[idx]
            chg = row[_avg_change]

            with cols[j]:
                _白话_card(
                    label=t('sector_heatmap.rank_col', rank=int(row["排名"])),
                    value=row["平均漲跌"],
                    analogy=f"🔴{int(row["上漲"])} 🟢{int(row["下跌"])} ⚪{int(row["平盤"])}",
                )


def _render_mover_row(rank: int, stock_name: str, stock_id: str, change_pct: float,
                      sector: str, latest_price):
    """Render a single top mover row using pure streamlit-native components."""
    sign = "+" if change_pct > 0 else ""
    price_str = f"NT${latest_price}" if latest_price else "—"

    c1, c2 = st.columns([3, 1])
    with c1:
        st.text(f"#{rank} {stock_name} ({stock_id})")
    with c2:
        st.markdown(f"**{sign}{change_pct:.2f}%**")
    st.caption(f"{sector} ｜ {price_str}")
    st.write("")


def _render_top_movers(summary_map: dict, sector_stocks: dict):
    """Show top gainers and losers across all sectors."""
    st.markdown(f"### 🔥 {t('sector_heatmap.top_movers')}")

    all_stocks = []
    for sector, stock_ids in sector_stocks.items():
        for sid in stock_ids:
            s = summary_map.get(sid)
            if s and s.get("change") is not None:
                all_stocks.append({**s, "sector": sector})

    if not all_stocks:
        st.info(t('sector_heatmap.no_mover_data'))
        return

    all_stocks.sort(key=lambda x: x["change"], reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### 🔴 {t('sector_heatmap.gainers')}")
        top_gainers = all_stocks[:10]
        for rank, s in enumerate(top_gainers, 1):
            change = s["change"]
            _render_mover_row(
                rank=rank,
                stock_name=s.get("stock_name", s["stock_id"]),
                stock_id=s["stock_id"],
                change_pct=change,
                sector=s.get("sector", ""),
                latest_price=s.get("latest_price"),
            )

    with col2:
        st.markdown(f"#### 🟢 {t('sector_heatmap.losers')}")
        top_losers = all_stocks[-10:][::-1]
        for rank, s in enumerate(top_losers, 1):
            change = s["change"]
            _render_mover_row(
                rank=rank,
                stock_name=s.get("stock_name", s["stock_id"]),
                stock_id=s["stock_id"],
                change_pct=change,
                sector=s.get("sector", ""),
                latest_price=s.get("latest_price"),
            )
