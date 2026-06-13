"""Revenue Tree page (C36) — detailed revenue breakdown with tree visualization.

This page is accessible from the Business Card page via the "更多分析" expander.
It provides a deep dive into the company's revenue structure and product mix.
"""
import streamlit as st
import pandas as pd

from src.pages._router_base import _section_title, _info_card, _白话_card
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.chart import create_revenue_pie_chart
from src.services.analogy_engine import get_revenue_analogy, get_yoy_analogy
from src.pages.business_card._helpers import _historian_disclaimer


def _render_revenue_tree(data: dict, client) -> None:
    """C36 Revenue Tree — deep dive into revenue structure and product mix.

    Shows:
    - Revenue pie chart with detailed breakdown
    - Product/category revenue tree
    - Revenue trend comparison
    - Plain-language analogy for each revenue source
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    financial = data["financial"]
    extra_metrics = data["extra_metrics"]

    # Page header
    _section_title(f"🌳 營收結構樹 — {stock_name} ({stock_id})")
    st.markdown("*深入拆解這家公司靠什麼賺錢*")
    st.markdown("")

    # ── Revenue breakdown pie chart ──
    revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)

    if revenue_items:
        st.markdown("### 📊 營收來源佔比")
        col1, col2 = st.columns([3, 2])
        with col1:
            fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            for item in revenue_items:
                _info_card(f"{item['name']} — {item['value']:.0f}%", item['description'], "📊")

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
