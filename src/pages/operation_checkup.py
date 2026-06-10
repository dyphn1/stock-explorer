"""
營運健檢頁 — M2 第一頁
目標：理解這家公司的商業模式
"""

import streamlit as st
import pandas as pd
from src.services.chart import create_revenue_trend_chart, create_price_chart, create_institutional_chart
from src.services.analogy_engine import get_yoy_analogy, get_revenue_analogy, get_volume_analogy, get_institutional_analogy
from src.pages._router_base import filter_by_timeline, _section_title, _白话_card, _info_card
from src.pages.timeline_controls import render_timeline_selector


def _render_operation_checkup(data: dict):
    """營運健檢主頁"""
    stock_name = data["stock_name"]
    industry = data["industry"]
    monthly_revenue = data["monthly_revenue"]
    daily_price = data["daily_price"]
    institutional = data["institutional"]
    extra_metrics = data["extra_metrics"]
    latest_price = data["latest_price"]

    st.markdown(f"## 🏥 營運健檢 — {stock_name}")
    st.markdown(f"*靠什麼賺錢？穩不穩？隨時間怎麼變？*")
    st.markdown("---")

    # ── M3: 時間軸選擇器 ──────────────────────────────
    render_timeline_selector(key_prefix="oc_")
    st.markdown("---")

    # ── 1. 營收趨勢 ──────────────────────────────────
    _section_title("營收趨勢：公司生意做多大？")

    if len(monthly_revenue) > 0:
        filtered_revenue = filter_by_timeline(monthly_revenue, date_col="date")
        fig = create_revenue_trend_chart(filtered_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)

        # 營收白話解讀
        latest_rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
        yoy = extra_metrics.get("revenue_yoy")
        cols = st.columns(2)
        with cols[0]:
            _白话_card(
                "最近月營收",
                f"{latest_rev:,.0f} 億",
                get_revenue_analogy(latest_rev, industry),
            )
        with cols[1]:
            if yoy is not None:
                _白话_card(
                    "營收年增率",
                    f"{yoy:+.1f}%",
                    get_yoy_analogy(yoy),
                )
            else:
                _白话_card("營收年增率", "資料不足", "需要至少 13 個月資料才能計算")

        # 營收趨勢白話解讀
        if yoy is not None:
            if yoy >= 20:
                trend_msg = f"{stock_name} 的營收成長很強勁！這代表市場對它的產品或服務需求正在增加。"
            elif yoy >= 5:
                trend_msg = f"{stock_name} 的營收穩定成長，經營狀況不錯。"
            elif yoy >= -5:
                trend_msg = f"{stock_name} 的營收跟去年差不多，屬於持平狀態。"
            else:
                trend_msg = f"{stock_name} 的營收比去年下滑，需要關注是什麼原因導致的。"
            _info_card("營收趨勢解讀", trend_msg, "📈")
    else:
        st.info("暫無營收資料")

    st.markdown("---")

    # ── 2. 股價走勢 ──────────────────────────────────
    _section_title("股價走勢：市場怎麼看這家公司？")

    if daily_price is not None and len(daily_price) > 0:
        filtered_price = filter_by_timeline(daily_price, date_col="date")
        fig = create_price_chart(filtered_price, f"{stock_name} 股價走勢")
        st.plotly_chart(fig, use_container_width=True)

        if latest_price:
            vol = latest_price.get("volume", 0)
            cols = st.columns(2)
            with cols[0]:
                _白话_card(
                    "最新收盤價",
                    f"{latest_price['close']:,.0f} 元",
                    f"開盤 {latest_price['open']:,.0f}｜最高 {latest_price['high']:,.0f}｜最低 {latest_price['low']:,.0f}",
                )
            with cols[1]:
                _白话_card(
                    "成交量",
                    f"{vol/1000:.0f} 千張",
                    get_volume_analogy(vol),
                )
    else:
        st.info("暫無股價資料")

    st.markdown("---")

    # ── 3. 法人動向 ──────────────────────────────────
    _section_title("法人動向：大戶在想什麼？")

    if institutional is not None and len(institutional) > 0:
        filtered_institutional = filter_by_timeline(institutional, date_col="date")
        fig = create_institutional_chart(filtered_institutional, f"{stock_name} 三大法人買賣超")
        st.plotly_chart(fig, use_container_width=True)

        # 近期法人動向總結
        recent = filtered_institutional.tail(5)
        net_buy_total = (recent["buy"] - recent["sell"]).sum()
        _白话_card(
            "近 5 日法人買賣超",
            f"{net_buy_total/1000:+.0f} 千張",
            get_institutional_analogy(net_buy_total),
        )

        if net_buy_total > 10000:
            _info_card("法人動向解讀", "近期法人積極買進，代表專業投資人對這家公司看法偏多。", "🏦")
        elif net_buy_total > 0:
            _info_card("法人動向解讀", "法人小幅買進，態度中性偏多。", "🏦")
        elif net_buy_total > -10000:
            _info_card("法人動向解讀", "法人小幅賣出，態度中性偏空。", "🏦")
        else:
            _info_card("法人動向解讀", "法人積極賣出，需要關注原因。", "🏦")
    else:
        st.info("暫無法人資料")

    st.markdown("---")

    # ── 4. 營運摘要 ──────────────────────────────────
    summary_parts = []
    if yoy is not None:
        if yoy >= 20:
            summary_parts.append("📈 營收快速成長")
        elif yoy >= 5:
            summary_parts.append("📊 營收穩定成長")
        elif yoy >= -5:
            summary_parts.append("📊 營收持平")
        else:
            summary_parts.append("📉 營收下滑")

    if latest_price:
        vol = latest_price.get("volume", 0)
        if vol >= 50000:
            summary_parts.append("🔥 市場交易熱絡")
        elif vol <= 1000:
            summary_parts.append("💤 市場交易冷清")

    if institutional is not None and len(institutional) > 0:
        recent = institutional.tail(5)
        net = (recent["buy"] - recent["sell"]).sum()
        if net > 10000:
            summary_parts.append("🏦 法人積極買進")
        elif net < -10000:
            summary_parts.append("🏦 法人積極賣出")

    if not summary_parts:
        summary_parts.append("📊 持續觀察中")

    st.markdown(f"""
    <div style="background:#EBF5FB;border-radius:16px;padding:2rem;margin:1rem 0;">
        <div style="font-size:1.2rem;font-weight:700;color:#2C3E50;margin-bottom:1rem;">🩺 營運摘要</div>
        <div style="font-size:1rem;color:#2C3E50;line-height:2;">
            {"<br>".join(summary_parts)}
        </div>
    </div>
    """, unsafe_allow_html=True)
