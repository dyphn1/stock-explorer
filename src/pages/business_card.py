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
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.services.watchlist import (
    is_in_watchlist,
    is_in_any_list,
    get_lists_for_stock,
    add_to_watchlist,
    remove_from_all_lists,
    remove_from_watchlist,
    create_list,
    list_names,
)


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
        # Watchlist buttons
        watchlist_lists = get_lists_for_stock(stock_id)
        if watchlist_lists:
            # Stock is in at least one list
            st.markdown(f"**已加入清單：** {', '.join(watchlist_lists)}")
            if st.button("❌ 取消關注 (全部清單)", key=f"unwatch_{stock_id}", use_container_width=True):
                if remove_from_all_lists(stock_id):
                    st.toast("🗑️ 已從所有關注清單移除")
                else:
                    st.error("移除失敗")
                st.rerun()
        else:
            # Stock is not in any list
            if st.button("➕ 加入關注", key=f"watch_{stock_id}", use_container_width=True):
                # Show popup to select list
                st.session_state[f"show_watchlist_popup_{stock_id}"] = True
                st.rerun()

    # Popup for adding to watchlist
    if st.session_state.get(f"show_watchlist_popup_{stock_id}", False):
        with st.popover("選擇要加入的清單", use_container_width=True):
            # Get existing list names
            existing_lists = list_names()
            tab1, tab2 = st.tabs(["選擇現有清單", "建立新清單"])
            target_list = None

            with tab1:
                if existing_lists:
                    selected = st.selectbox(
                        "選擇清單",
                        options=existing_lists,
                        key=f"select_existing_{stock_id}",
                    )
                    if selected:
                        target_list = selected
                else:
                    st.info("目前沒有現有清單")

            with tab2:
                new_name = st.text_input(
                    "新清單名稱",
                    placeholder="請輸入新清單名稱",
                    key=f"new_name_{stock_id}",
                )
                if st.button("建立清單", key=f"create_btn_{stock_id}"):
                    if new_name:
                        if create_list(new_name):
                            st.success(f"已建立清單：{new_name}")
                            target_list = new_name
                        else:
                            st.error("建立失敗：名稱可能已存在")
                    else:
                        st.error("請輸入清單名稱")

            # Add stock button
            if st.button("加入關注", key=f"add_stock_btn_{stock_id}", type="primary"):
                if target_list:
                    success = add_to_watchlist(
                        stock_id=stock_id,
                        name=stock_name,
                        alert_above=None,
                        alert_below=None,
                        industry_category=industry,
                        list_name=target_list,
                    )
                    if success:
                        st.session_state[f"show_watchlist_popup_{stock_id}"] = False
                        st.toast(f"已加入關注清單：{target_list}")
                        st.rerun()
                    else:
                        st.error("加入失敗：股票可能已在該清單中")
                else:
                    st.error("請先選擇或建立清單")

    st.markdown("---")

    # 一句話定位
    one_liner = get_one_liner(stock_id, stock_name, industry)
    st.markdown(f"""
    <div style="font-size:1.3rem;font-weight:500;color:#2C3E50;text-align:center;padding:1.5rem 2rem;background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);border-radius:12px;margin:1rem 0;line-height:1.8;border-left:5px solid #3498DB;">
        💡 {one_liner}
    </div>
    """, unsafe_allow_html=True)

    # 💡 你知道嗎？ Company facts tip card
    facts = get_company_facts(stock_id)
    if facts:
        # Rotate facts on each rerun using session_state
        fact_key = f"_fact_idx_{stock_id}"
        if fact_key not in st.session_state:
            st.session_state[fact_key] = 0
        idx = st.session_state[fact_key] % len(facts)
        st.session_state[fact_key] = (idx + 1) % len(facts)
        current_fact = facts[idx]
        st.markdown(f"""
        <div style="background:#F0F7FF;border-left:4px solid #3498DB;border-radius:12px;padding:1.2rem 2rem;margin:1rem 0;text-align:center;">
            <div style="font-size:0.85rem;color:#3498DB;font-weight:600;margin-bottom:0.4rem;">💡 你知道嗎？</div>
            <div style="font-size:1.05rem;color:#2C3E50;line-height:1.7;">{current_fact}</div>
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

    # === 💵 配息故事 (Dividend Story) ===
    # Extract current price for yield calculation
    _current_price = None
    if latest_price and latest_price.get("close"):
        _current_price = float(latest_price["close"])

    dividend_data = data.get("dividend") if isinstance(data, dict) else None
    div_summary = extract_dividend_summary(
        dividend_data,
        current_price=_current_price,
    )

    if div_summary["has_data"]:
        # Plain-language headline (tip card style)
        st.markdown(
            f"""<div style="
                background: #FFF8F0;
                border-left: 4px solid #E74C3C;
                padding: 12px 16px;
                border-radius: 4px;
                margin: 12px 0;
                font-size: 1.05rem;
                color: #2C3E50;
            ">
                💵 {div_summary['plain_summary']}
            </div>""",
            unsafe_allow_html=True,
        )

        # Three mini-cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""<div style="text-align: center; padding: 8px;">
                    <div style="font-size: 0.85rem; color: #7F8C8D;">最近一季</div>
                    <div style="font-size: 1.4rem; font-weight: bold; color: #2C3E50;">
                        {div_summary['latest_cash_div']:.2f} 元
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            annual_str = f"{div_summary['estimated_annual']:.2f}" if div_summary['estimated_annual'] else "—"
            st.markdown(
                f"""<div style="text-align: center; padding: 8px;">
                    <div style="font-size: 0.85rem; color: #7F8C8D;">預估全年</div>
                    <div style="font-size: 1.4rem; font-weight: bold; color: #2C3E50;">
                        {annual_str} 元
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        with col3:
            yield_str = f"{div_summary['estimated_yield']:.2f}" if div_summary['estimated_yield'] else "—"
            st.markdown(
                f"""<div style="text-align: center; padding: 8px;">
                    <div style="font-size: 0.85rem; color: #7F8C8D;">殖利率</div>
                    <div style="font-size: 1.4rem; font-weight: bold; color: #2C3E50;">
                        {yield_str}%
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

        # Expandable history table
        with st.expander("📋 展開查看歷史除權息紀錄", expanded=False):
            if div_summary["yearly_dividends"]:
                hist_df = pd.DataFrame(div_summary["yearly_dividends"])
                # Rename columns for display
                display_df = hist_df[["year", "cash_div", "ex_date", "status"]].copy()
                display_df.columns = ["年度", "現金股利", "除息日", "狀態"]
                if "stock_div" in hist_df.columns:
                    display_df["股票股利"] = hist_df["stock_div"]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        # Show a subtle note for stocks without dividends
        st.markdown(
            f"""<div style="
                background: #F8F9FA;
                border-left: 4px solid #BDC3C7;
                padding: 10px 14px;
                border-radius: 4px;
                margin: 8px 0;
                font-size: 0.9rem;
                color: #7F8C8D;
            ">
                💡 {div_summary['plain_summary']}
            </div>""",
            unsafe_allow_html=True,
        )

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
            <div style="background:#FFF8F0;border-radius:12px;padding:1.5rem;border-left:4px solid #E74C3C;margin:0.5rem 0;">
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
