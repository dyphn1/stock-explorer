"""Business card section: summary sections (story card, header, takeaways, one-liner, news)."""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.services.chart import create_revenue_trend_chart, create_health_snowflake
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
from src.services.key_takeaways import generate_key_takeaways
from src.services.health_scoring import compute_health_scores
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
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.business_card._helpers import (
    get_health_dimension_explanation,
    _get_health_metric_values,
    _section_title,
)


def _render_story_card(data: dict, client) -> None:
    """C48 Company Story Card — 30-second visual summary.

    A PPT-style hero card at the top of the business card page showing:
    - Company name + industry
    - One-liner description
    - 3 key metric highlights (bold numbers with plain-language)
    - Health score indicator
    - Rotating "Did You Know?" fact
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]

    # ── One-liner ──
    one_liner = get_one_liner(stock_id, stock_name, industry)

    # ── Pick top 3 most notable metrics ──
    metrics = []

    # Revenue (monthly)
    if len(monthly_revenue) > 0:
        rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
        yoy = extra_metrics.get("revenue_yoy")
        yoy_analogy = get_yoy_analogy(yoy) if yoy is not None else ""
        metrics.append(("最近月營收", f"{rev:,.0f} 億", get_revenue_analogy(rev, industry) + (f" ｜ {yoy_analogy}" if yoy_analogy else "")))

    # PER
    if latest_per_pbr and latest_per_pbr.get("PER") is not None:
        per = latest_per_pbr["PER"]
        metrics.append(("本益比 (PER)", f"{per:.1f}", get_per_analogy(per)))

    # Gross margin
    if extra_metrics.get("gross_margin") is not None:
        gm = extra_metrics["gross_margin"]
        metrics.append(("毛利率", f"{gm:.1f}%", get_gross_margin_analogy(gm)))

    # Dividend yield
    if latest_per_pbr and latest_per_pbr.get("dividend_yield") is not None:
        dy = latest_per_pbr["dividend_yield"]
        metrics.append(("殖利率", f"{dy:.2f}%", get_dividend_analogy(dy)))

    # ROE
    if extra_metrics.get("roe") is not None:
        roe = extra_metrics["roe"]
        metrics.append(("ROE", f"{roe:.1f}%", get_roe_analogy(roe)))

    # PBR
    if latest_per_pbr and latest_per_pbr.get("PBR") is not None:
        pbr = latest_per_pbr["PBR"]
        metrics.append(("淨值比 (PBR)", f"{pbr:.2f}", get_pbr_analogy(pbr)))

    # Take top 3
    top_metrics = metrics[:3]

    # ── Health score indicator ──
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=data["financial"],
        monthly_revenue=monthly_revenue,
    )
    overall_health = None
    health_label = "—"
    if health_scores:
        overall_health = sum(health_scores.values()) / len(health_scores)
        if overall_health >= 70:
            health_label = "🟢 健康"
        elif overall_health >= 40:
            health_label = "🟡 一般"
        else:
            health_label = "🔴 留意"

    # ── Did You Know? fact ──
    facts = get_company_facts(stock_id)
    fact_text = ""
    if facts:
        fact_key = f"_story_fact_idx_{stock_id}"
        if fact_key not in st.session_state:
            st.session_state[fact_key] = 0
        idx = st.session_state[fact_key] % len(facts)
        st.session_state[fact_key] = (idx + 1) % len(facts)
        fact_text = facts[idx]

    # ── Build the story card using shared components ──
    # We use st.expander to avoid overloading the page (D-032)
    with st.expander("📌 30 秒認識這家公司", expanded=True):
        # Company name + industry header
        st.markdown(f"### {stock_name} `{stock_id}`")
        st.markdown(f"*{industry}*")

        # One-liner
        _info_card("一句話定位", one_liner, "💡")

        # Key metrics row — use _白话_card for each
        if top_metrics:
            cols = st.columns(len(top_metrics))
            for col, (label, value, analogy) in zip(cols, top_metrics):
                with col:
                    _白话_card(label, value, analogy)

        # Health score
        if overall_health is not None:
            st.markdown(
                f"""<div style="text-align:center;padding:0.5rem;
                background:#F8F9FA;border-radius:10px;margin:0.5rem 0;">
                    <div style="font-size:0.85rem;color:#7F8C8D;">整體健康度</div>
                    <div style="font-size:1.5rem;font-weight:700;color:#2C3E50;">
                        {overall_health:.0f}/100</div>
                    <div style="font-size:0.85rem;">{health_label}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        # Did You Know?
        if fact_text:
            _info_card("你知道嗎？", fact_text, "🤔")


def _render_header(data: dict, client) -> None:
    """Watchlist header with stock name, price, watchlist buttons."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]

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


def _render_takeaways(data: dict, client) -> None:
    """C37 Key Takeaways section."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]

    # 📋 重點摘要 (C37: Key Takeaways)
    takeaways = generate_key_takeaways(
        stock_id=stock_id,
        stock_name=stock_name,
        industry=industry,
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        monthly_revenue=monthly_revenue,
        financial_df=financial,
    )
    if takeaways:
        takeaways_text = "\\n\\n".join(f"• {t}" for t in takeaways)
        _summary_card("重點摘要", takeaways_text, "📋")


def _render_one_liner(data: dict, client) -> None:
    """One-liner + rotating company facts tip card."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    # 一句話定位
    one_liner = get_one_liner(stock_id, stock_name, industry)
    _info_card("一句話定位", one_liner, "💡")

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
        _info_card("你知道嗎？", current_fact, "💡")


def _render_news(data: dict, client) -> None:
    """Recent news with impact level badges."""
    news = data["news"]
    stock_name = data["stock_name"]

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

            _info_card(f"{impact_class} {title}\n\n{summary}\n\n📡 {source} ｜ {date_str}", "", "📰")
    else:
        st.info("近期無重大新聞")
