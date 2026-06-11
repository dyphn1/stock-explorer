"""
公司名片頁 — M1 MVP
目標：使用者在 10 秒內知道這家公司靠什麼賺錢
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake
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
    generate_key_takeaways,
    compute_recent_deltas,
    compute_health_scores,
    get_health_summary,
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
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.url_sync import navigate_to


def get_health_dimension_explanation(dim_name: str, score: float) -> str:
    """Return a plain-language explanation for a health dimension score."""
    if score >= 70:
        return "表現優異，在同產業中屬於前段班"
    elif score >= 40:
        return "表現穩定，有改善空間"
    else:
        return "需要留意，可能拖累整體表現"


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

    # 🔄 最近有什麼變化 (C39: Recent Deltas)
    deltas = compute_recent_deltas(
        extra_metrics=extra_metrics,
        monthly_revenue=monthly_revenue,
        daily_price=data.get("daily_price"),
        latest_per_pbr=latest_per_pbr,
    )
    if deltas:
        delta_lines = []
        for d in deltas:
            emoji = "📈" if d["direction"] == "up" else "📉"
            sign = "+" if d["change_pct"] >= 0 else ""
            color = "#27AE60" if d["direction"] == "up" else "#E74C3C"
            delta_lines.append(
                f"{emoji} <span style=\"color:{color}\">**{d['metric_name']}**：{d['current_value']}（前期：{d['previous_value']}，{sign}{d['change_pct']:.1f}%）</span><br>\\n"
                f"　→ {d['explanation']}"
            )
        delta_text = "\\n\\n".join(delta_lines)
        _info_card("最近有什麼變化", delta_text, "🔄")
    else:
        _info_card("最近有什麼變化", "近期無顯著變化，所有指標波動均在 10% 以內", "🔄")

    # 🏥 公司健康狀況 (C43: Health Snowflake)
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        st.markdown("### 🏥 公司健康狀況")
        health_fig = create_health_snowflake(stock_name, health_scores)
        st.plotly_chart(health_fig, use_container_width=True)

        # 五維度分數明細
        dim_cols = st.columns(5)
        for i, (dim_name, score) in enumerate(health_scores.items()):
            with dim_cols[i]:
                if score >= 70:
                    indicator = "🟢"
                elif score >= 40:
                    indicator = "🟡"
                else:
                    indicator = "🔴"
                st.markdown(
                    f"""
                    <div style="text-align:center;padding:0.5rem;background:#F8F9FA;border-radius:10px;margin:0.2rem 0;">
                        <div style="font-size:0.8rem;color:#7F8C8D;">{indicator} {dim_name}</div>
                        <div style="font-size:1.4rem;font-weight:700;color:#2C3E50;">{score:.0f}</div>
                        <div style="font-size:0.7rem;color:#7F8C8D;margin-top:0.2rem;">{get_health_dimension_explanation(dim_name, score)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # 白話健康摘要
        health_summary = get_health_summary(health_scores)
        _info_card("健康摘要", health_summary, "🏥")

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

    # 關鍵數字三連卡
    st.markdown("### 📊 關鍵數字")
    col1, col2, col3 = st.columns(3)

    with col1:
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            _白话_card("本益比 (PER)", f"{per:.1f}", get_per_analogy(per))
        elif extra_metrics.get("gross_margin"):
            gm = extra_metrics["gross_margin"]
            _白话_card("毛利率", f"{gm:.1f}%", get_gross_margin_analogy(gm))

    with col2:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            yoy = extra_metrics.get("revenue_yoy")
            yoy_analogy = get_yoy_analogy(yoy) if yoy is not None else ""
            _白话_card("最近月營收", f"{rev:,.0f} 億", get_revenue_analogy(rev, industry) + (f" ｜ {yoy_analogy}" if yoy_analogy else ""))
        elif extra_metrics.get("roe"):
            roe = extra_metrics["roe"]
            _白话_card("ROE", f"{roe:.1f}%", get_roe_analyzer(roe))

    with col3:
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            _白话_card("殖利率", f"{dy:.2f}%", get_dividend_analogy(dy))
        elif latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            _白话_card("淨值比 (PBR)", f"{pbr:.2f}", get_pbr_analyzer(pbr))

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
        # ── Countdown to next ex-dividend date ──
        _today = date.today()
        _next_ex_date = None
        _next_ex_year = None
        for _d in div_summary["yearly_dividends"]:
            _ex = _d.get("ex_date", "")
            if not _ex or _ex == "—":
                continue
            try:
                _ex_dt = pd.Timestamp(_ex).date()
                if _ex_dt >= _today:
                    if _next_ex_date is None or _ex_dt < _next_ex_date:
                        _next_ex_date = _ex_dt
                        _next_ex_year = _d.get("year", "")
            except Exception:
                continue

        if _next_ex_date:
            _days_left = (_next_ex_date - _today).days
            _info_card(
                "除息日倒數",
                f"距離除息日還剩 {_days_left} 天（預計 {_next_ex_date.strftime('%Y/%m/%d')}）",
                "⏳",
            )

        # Plain-language headline (tip card style)
        _info_card("配息摘要", div_summary["plain_summary"], "💵")

        # Three mini-cards
        col1, col2, col3 = st.columns(3)
        with col1:
            _白话_card("最近一季", f"{div_summary['latest_cash_div']:.2f} 元", "每股現金股利")
        with col2:
            annual_str = f"{div_summary['estimated_annual']:.2f} 元" if div_summary['estimated_annual'] else "—"
            _白话_card("預估全年", annual_str, "預估全年配息")
        with col3:
            yield_str = f"{div_summary['estimated_yield']:.2f}%" if div_summary['estimated_yield'] else "—"
            _白话_card("殖利率", yield_str, "年化股利／股價")

        # Expandable history table
        with st.expander("📋 展開查看歷史除權息紀錄", expanded=False):
            if div_summary["yearly_dividends"]:
                hist_df = pd.DataFrame(div_summary["yearly_dividends"])
                # Rename columns for display
                display_df = hist_df[["year", "cash_div", "ex_date", "status"]].copy()
                display_df.columns = ["年度", "現金股利", "除息日", "狀態"]
                if "stock_div" in hist_df.columns:
                    display_df["股票股利"] = hist_df["stock_div"]

                # Add ex-date badge column
                _today = date.today()
                _badges = []
                for _, _row in display_df.iterrows():
                    _ex = _row["除息日"]
                    if _ex and _ex != "—":
                        try:
                            _ex_dt = pd.Timestamp(_ex).date()
                            if _ex_dt >= _today:
                                _badges.append(
                                    f'<span style="background:#27AE60;color:#FFFFFF;padding:2px 8px;border-radius:10px;font-size:0.75rem;">即將除息</span>'
                                )
                            else:
                                _badges.append(
                                    f'<span style="background:#3498DB;color:#FFFFFF;padding:2px 8px;border-radius:10px;font-size:0.75rem;">已除息</span>'
                                )
                        except Exception:
                            _badges.append("")
                    else:
                        _badges.append("")
                display_df["除息標記"] = _badges

                # Render as HTML table to support badges
                html_rows = []
                _cols = list(display_df.columns)
                _header = "".join(f'<th style="text-align:left;padding:8px 12px;color:#7F8C8D;font-size:0.85rem;border-bottom:2px solid #BDC3C7;">{c}</th>' for c in _cols)
                html_rows.append(f"<tr>{_header}</tr>")
                for _, _r in display_df.iterrows():
                    _cells = ""
                    for _c in _cols:
                        _val = _r[_c]
                        if _c == "除息標記":
                            _cells += f'<td style="padding:8px 12px;border-bottom:1px solid #F8F9FA;">{_val}</td>'
                        else:
                            _cells += f'<td style="padding:8px 12px;color:#2C3E50;border-bottom:1px solid #F8F9FA;">{_val}</td>'
                    html_rows.append(f"<tr>{_cells}</tr>")
                _table_html = (
                    '<table style="width:100%;border-collapse:collapse;font-size:0.9rem;">'
                    + "".join(html_rows)
                    + "</table>"
                )
                st.markdown(_table_html, unsafe_allow_html=True)
    else:
        # Show a subtle note for stocks without dividends
        _info_card("配息摘要", div_summary["plain_summary"], "💡")

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
            _info_card(f"{item['name']} — {item['value']:.0f}%", item['description'], "📊")

    st.markdown("---")

    # 營收趨勢圖
    st.markdown("### 📊 營收趨勢")
    if len(monthly_revenue) > 0:
        fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暫無營收資料")

    st.markdown("---")

    # 估值區間圖（歷史 P/E 範圍）
    st.markdown("### 📊 估值區間")
    st.markdown("*目前本益比在歷史上的位置*")

    daily_price = data.get("daily_price")
    if daily_price is not None and len(daily_price) > 0 and len(financial) > 0 and latest_per_pbr and latest_per_pbr.get("PER"):
        fig, interp = create_valuation_band_chart(
            stock_id=stock_id,
            stock_name=stock_name,
            daily_price_df=daily_price,
            financial_df=financial,
            latest_per_pbr=latest_per_pbr,
        )
        st.plotly_chart(fig, use_container_width=True)

        # 白話解讀 — use interpretation returned by chart function
        if interp and interp.get("valuation_text"):
            _info_card("估值解讀", interp["valuation_text"], "💡")
    else:
        st.info("暫無足夠資料計算估值區間")

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

            _info_card(f"{impact_class} {title}\n\n{summary}\n\n📡 {source} ｜ {date_str}", "", "📰")
    else:
        st.info("近期無重大新聞")

    # 免責聲明
    _info_card("免責聲明", "本工具僅供認識公司使用，所有數據來自公開資訊觀測站與 FinMind。不構成任何投資建議。投資有風險，請自行評估。", "⚠️")
