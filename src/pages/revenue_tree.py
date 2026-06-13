"""Revenue Tree page (C36) — detailed revenue breakdown with tree visualization.

This page is accessible from the Business Card page via the "更多分析" expander.
It provides a deep dive into the company's revenue structure and product mix.
"""
import streamlit as st
import pandas as pd

from src.pages._router_base import _section_title, _info_card, _白话_card, _glossary_tooltip
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.chart import create_revenue_pie_chart, create_revenue_treemap, create_revenue_trend_chart
from src.services.analogy_engine import get_revenue_analogy, get_yoy_analogy
from src.services import glossary_service
from src.pages.business_card._helpers import _historian_disclaimer


def _render_revenue_tree(data: dict, client) -> None:
    """C36 Revenue Tree V2 — deep dive into revenue structure and product mix.

    Shows:
    - Revenue pie chart (default) with treemap toggle
    - Revenue concentration warning
    - Revenue trend mini-chart (12-month sparkline)
    - Product/category revenue tree
    - Plain-language analogy for each revenue source
    - Glossary tooltips on revenue breakdown items
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    financial = data["financial"]
    extra_metrics = data["extra_metrics"]
    monthly_revenue = data["monthly_revenue"]

    # Page header
    _section_title(f"🌳 營收結構樹 — {stock_name} ({stock_id})")
    st.markdown("*深入拆解這家公司靠什麼賺錢*")
    st.markdown("")

    # ── Revenue breakdown chart with treemap toggle ──
    revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)

    if revenue_items:
        st.markdown("### 📊 營收來源佔比")

        # Treemap toggle
        treemap_mode = st.toggle("🔬 切換樹狀圖", value=False, help="切換為樹狀圖視圖，面積大小代表營收佔比")
        if treemap_mode:
            fig = create_revenue_treemap(revenue_items, f"{stock_name} 營收來源")
        else:
            fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
        st.plotly_chart(fig, use_container_width=True)

        # Concentration warning
        max_item = max(revenue_items, key=lambda x: x["value"])
        if max_item["value"] > 60:
            _info_card("⚠️ 營收集中風險", 
                       f"{max_item['name']}佔營收 {max_item['value']:.0f}%，超過 60% 營收來自單一來源，需留意客戶集中度風險", 
                       "⚠️")

        # Revenue trend sparkline
        if len(monthly_revenue) >= 3:
            st.markdown("##### 📈 近 12 個月營收趨勢")
            trend_fig = create_revenue_trend_chart(monthly_revenue.tail(12), "")
            trend_fig.update_layout(height=200, margin=dict(t=10, b=10, l=10, r=10),
                                   showlegend=False)
            st.plotly_chart(trend_fig, use_container_width=True)

        st.markdown("---")

        # ── Revenue details ──
        st.markdown("### 📋 各營收來源說明")
        for item in revenue_items:
            analogy = get_revenue_analogy(item['value'], industry)
            _白话_card(item['name'], f"{item['value']:.0f}%", analogy)

        st.markdown("---")
    else:
        st.info("目前沒有詳細營收組成資料")

    # ── YoY growth context ──
    yoy = extra_metrics.get("revenue_yoy")
    if yoy is not None:
        yoy_analogy = get_yoy_analogy(yoy)
        direction = "成長" if yoy >= 0 else "衰退"
        _info_card(
            "營收年增率",
            f"較去年同期 **{direction} {abs(yoy):.1f}%**\n\n{yoy_analogy}",
            "📈" if yoy >= 0 else "📉",
        )

    _historian_disclaimer("revenue_tree")
