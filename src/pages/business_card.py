"""
公司名片頁 — M1 MVP
目標：使用者在 10 秒內知道這家公司靠什麼賺錢
"""

import streamlit as st
import pandas as pd
from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_pbr_analogy,
)
from src.services.news_summarizer import summarize_news, get_news_impact_level


def _render_business_card(data: dict, client):
    """公司名片主頁（M1）"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]
    news = data["news"]
    extra_metrics = data["extra_metrics"]

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"**{stock_name}** `{stock_id}` ｜ {industry}")
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            sign = "+" if change >= 0 else ""
            st.markdown(f"**{price:,.0f}** `{sign}{change:,.0f}`")
    with col3:
        from src.services.watchlist import is_in_watchlist, add_to_watchlist, remove_from_watchlist
        if is_in_watchlist(stock_id):
            if st.button("❌ 取消關注", key=f"unwatch_{stock_id}", use_container_width=True):
                remove_from_watchlist(stock_id)
                st.rerun()
        else:
            if st.button("➕ 加入關注", key=f"watch_{stock_id}", use_container_width=True):
                add_to_watchlist(stock_id, stock_name)
                st.rerun()

    st.markdown("---")

    # 一句話定位
    one_liner = get_one_liner(stock_id, stock_name, industry)
    st.markdown(f"""
    <div style="font-size:1.3rem;font-weight:500;color:#2C3E50;text-align:center;padding:1.5rem 2rem;background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);border-radius:12px;margin:1rem 0;line-height:1.8;border-left:5px solid #3498DB;">
        💡 {one_liner}
    </div>
    """, unsafe_allow_html=True)

    # 關鍵數字三連卡
    st.markdown("### 📊 關鍵數字")
    col1, col2, col3 = st.columns(3)

    with col1:
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{per:.1f}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">本益比 (PER)</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_per_analogy(per)}</div>
            </div>
            """, unsafe_allow_html=True)
        elif extra_metrics.get("gross_margin"):
            gm = extra_metrics["gross_margin"]
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{gm:.1f}%</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">毛利率</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_gross_margin_analogy(gm)}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            yoy = extra_metrics.get("revenue_yoy")
            yoy_html = f'<div style="font-size:0.85rem;color:#27AE60;margin-top:0.3rem;font-style:italic;">{get_yoy_analogy(yoy)}</div>' if yoy is not None else ""
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{rev:,.0f} 億</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">最近月營收</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_revenue_analogy(rev, industry)}</div>
                {yoy_html}
            </div>
            """, unsafe_allow_html=True)
        elif extra_metrics.get("roe"):
            roe = extra_metrics["roe"]
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{roe:.1f}%</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">ROE</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_roe_analogy(roe)}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{dy:.2f}%</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">殖利率</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_dividend_analogy(dy)}</div>
            </div>
            """, unsafe_allow_html=True)
        elif latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;">{pbr:.2f}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">淨值比 (PBR)</div>
                <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;font-style:italic;">{get_pbr_analogy(pbr)}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 營收組成（圓餅圖 + 白話說明）
    st.markdown("### 📊 營收組成")
    st.markdown("*這家公司靠什麼賺錢？*")

    revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        for item in revenue_items:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:1rem 1.2rem;margin:0.5rem 0;border-left:4px solid #3498DB;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:600;color:#2C3E50;">{item['name']}</span>
                    <span style="font-size:1.1rem;font-weight:700;color:#3498DB;">{item['value']:.0f}%</span>
                </div>
                <div style="font-size:0.85rem;color:#5D6D7E;margin-top:0.3rem;">{item['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 營收趨勢圖
    st.markdown("### 📊 營收趨勢")
    if len(monthly_revenue) > 0:
        fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暫無營收資料")

    st.markdown("---")

    # 近期動態（白話摘要版）
    st.markdown("### 📊 近期動態")
    if len(news) > 0:
        for i in range(min(3, len(news))):
            news_item = news.iloc[i]
            title = news_item['title']
            source = news_item.get('source', '未知')
            date_str = str(news_item.get('date', ''))[:10]
            impact = get_news_impact_level(title)
            summary = summarize_news(title, stock_name)

            impact_class = {"high": "🔴 重大", "medium": "🟡 注意", "low": "🟢 參考"}[impact]

            st.markdown(f"""
            <div style="background:#FFF8F0;border-radius:12px;padding:1.5rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
                <div style="font-weight:600;color:#2C3E50;">
                    <span style="margin-right:0.5rem;">{impact_class}</span>
                    📰 {title}
                </div>
                <div style="font-size:0.9rem;color:#5D6D7E;line-height:1.6;background:white;border-radius:8px;padding:0.8rem 1rem;margin-top:0.5rem;">{summary}</div>
                <div style="font-size:0.8rem;color:#95A5A6;margin-top:0.5rem;">📡 {source} ｜ {date_str}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("近期無重大新聞")

    # 免責聲明
    st.markdown("""
    <div style="background:#FEF9E7;border:1px solid #F9E79F;border-radius:8px;padding:1rem;font-size:0.85rem;color:#7D6608;margin-top:2rem;">
        ⚠️ 本工具僅供認識公司使用，所有數據來自公開資訊觀測站與 FinMind。
        不構成任何投資建議。投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)
