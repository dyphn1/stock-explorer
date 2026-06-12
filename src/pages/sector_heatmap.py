"""
Sector Heatmap — C51 Visual Market Overview
Displays a color-coded grid of Taiwan stock sectors showing performance.
Uses market_data service for data access (D-044).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
    st.markdown("## 🗺️ 產業熱力圖")
    st.markdown("*即時掌握各產業板塊的漲跌分布*")
    st.markdown("---\n")

    # ── Load stock info via market_data service ────────────
    with st.spinner("載入股票資料中…"):
        try:
            all_stock_info = get_all_stock_info(client)
        except Exception as e:
            st.error(f"無法取得股票資訊：{e}")
            return

    if all_stock_info is None or len(all_stock_info) == 0:
        st.warning("目前無股票資料可顯示。")
        return

    # Ensure required columns exist
    for col in ("stock_id", "stock_name", "industry_category"):
        if col not in all_stock_info.columns:
            st.error(f"資料缺少必要欄位：{col}")
            return

    # ── Build industry → stock_ids mapping via service ────
    sector_stocks = get_sector_stocks(all_stock_info)

    if not sector_stocks:
        st.info("無產業分類資料。")
        return

    # ── Fetch prices via market_data service ───────────────
    progress = st.progress(0, text="正在取得即時報價…")
    all_stock_ids = sorted(all_stock_info["stock_id"].unique())
    total_stocks = len(all_stock_ids)
    batch_size = 50

    def _update_progress(fraction: float):
        progress.progress(
            fraction,
            text=f"已處理 {int(fraction * total_stocks)}/{total_stocks} 檔…",
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
        st.warning(f"無法取得報價資料：{e}")
        return

    progress.empty()

    if not summary_map:
        st.warning("無法取得報價資料，請稍後再試。")
        return

    # ── Compute sector-level metrics via service ───────────
    sector_metrics = compute_sector_metrics(summary_map, sector_stocks)

    if not sector_metrics:
        st.info("無報價資料可分析。")
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
            "產業平均漲幅",
            _format_pct(overall_avg),
            "所有產業平均值",
        )
    with col2:
        _白话_card(
            "最強板塊",
            leading_sector[0],
            f"平均 {_format_pct(leading_sector[1]['avg_change'])}",
        )
    with col3:
        _白话_card(
            "最弱板塊",
            lagging_sector[0],
            f"平均 {_format_pct(lagging_sector[1]['avg_change'])}",
        )
    with col4:
        _白话_card(
            "漲跌產業數",
            f"🔴 {up_sectors} / 🟢 {down_sectors}",
            "上漲 / 下跌",
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
    st.markdown("### 📊 板塊熱力圖（TreeMap）")

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
            f"平均漲跌: {_format_pct(avg_chg)}<br>"
            f"上漲: {up} / 下跌: {down} / 平盤: {flat}<br>"
            f"共 {count} 檔"
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
                f"漲跌: {_format_pct(chg)}"
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
            text="板塊熱力圖 — 紅色=上漲、綠色=下跌、面積=檔數",
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
    st.markdown("### 🏭 板塊表現排行")

    # Sort by avg change descending
    sorted_sectors = sorted(
        sector_metrics.items(),
        key=lambda x: x[1]["avg_change"],
        reverse=True,
    )

    df = pd.DataFrame([
        {
            "排名": idx + 1,
            "產業": sector,
            "平均漲跌": _format_pct(m["avg_change"]),
            "上漲": m["up"],
            "下跌": m["down"],
            "平盤": m["flat"],
            "有報價": m["count"],
            "_avg_change": m["avg_change"],
        }
        for idx, (sector, m) in enumerate(sorted_sectors)
    ])

    # Render as color-coded grid
    cols_per_row = 4
    for i in range(0, len(df), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(df):
                break
            row = df.iloc[idx]
            chg = row["_avg_change"]
            bg = _perf_bg_color(chg, 0.12)
            border_color = _perf_color(chg)
            text_color = _perf_color(chg)

            cols[j].markdown(
                f"""
                <div style="
                    background:{bg};
                    border-radius:12px;
                    padding:1rem;
                    margin-bottom:0.5rem;
                    border-left:4px solid {border_color};
                    min-height:140px;
                ">
                    <div style="font-size:0.75rem;color:#7F8C8D;">#{int(row['排名'])}  {row['產業']}</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{text_color};margin:0.3rem 0;">
                        {row['平均漲跌']}
                    </div>
                    <div style="font-size:0.75rem;color:#7F8C8D;">
                        🔴{int(row['上漲'])} 🟢{int(row['下跌'])} ⚪{int(row['平盤'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_top_movers(summary_map: dict, sector_stocks: dict):
    """Show top gainers and losers across all sectors."""
    st.markdown("### 🔥 漲跌幅排行")

    all_stocks = []
    for sector, stock_ids in sector_stocks.items():
        for sid in stock_ids:
            s = summary_map.get(sid)
            if s and s.get("change") is not None:
                all_stocks.append({**s, "sector": sector})

    if not all_stocks:
        st.info("無可比較的漲跌幅資料。")
        return

    all_stocks.sort(key=lambda x: x["change"], reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔴 漲幅排行")
        top_gainers = all_stocks[:10]
        for rank, s in enumerate(top_gainers, 1):
            change = s["change"]
            card_bg = "rgba(231,76,60,0.06)"
            border = "#E74C3C"
            st.markdown(
                f"""
                <div style="background:{card_bg};border-radius:10px;padding:0.7rem 1rem;
                            border-left:3px solid {border};margin-bottom:0.4rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:0.8rem;color:#7F8C8D;">#{rank}</span>
                            <span style="font-weight:600;color:#2C3E50;margin-left:0.3rem;">
                                {s.get('stock_name', s['stock_id'])}
                            </span>
                            <span style="font-size:0.75rem;color:#7F8C8D;margin-left:0.3rem;">
                                ({s['stock_id']})
                            </span>
                        </div>
                        <span style="font-weight:700;color:#E74C3C;">{_format_pct(change)}</span>
                    </div>
                    <div style="font-size:0.75rem;color:#7F8C8D;margin-top:0.2rem;">
                        {s.get('sector', '')} ｜ {"NT$" + str(s['latest_price']) if s.get('latest_price') else "—"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("#### 🟢 跌幅排行")
        top_losers = all_stocks[-10:][::-1]
        for rank, s in enumerate(top_losers, 1):
            change = s["change"]
            card_bg = "rgba(39,174,96,0.06)"
            border = "#27AE60"
            st.markdown(
                f"""
                <div style="background:{card_bg};border-radius:10px;padding:0.7rem 1rem;
                            border-left:3px solid {border};margin-bottom:0.4rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:0.8rem;color:#7F8C8D;">#{rank}</span>
                            <span style="font-weight:600;color:#2C3E50;margin-left:0.3rem;">
                                {s.get('stock_name', s['stock_id'])}
                            </span>
                            <span style="font-size:0.75rem;color:#7F8C8D;margin-left:0.3rem;">
                                ({s['stock_id']})
                            </span>
                        </div>
                        <span style="font-weight:700;color:#27AE60;">{_format_pct(change)}</span>
                    </div>
                    <div style="font-size:0.75rem;color:#7F8C8D;margin-top:0.2rem;">
                        {s.get('sector', '')} ｜ {"NT$" + str(s['latest_price']) if s.get('latest_price') else "—"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
