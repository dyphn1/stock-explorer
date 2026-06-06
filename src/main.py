"""
股識 Stock Explorer
Streamlit 入口 — M1 完善版
"""

import pandas as pd
import streamlit as st
from src.data.finmind_client import FinMindClient
from src.services.chart import (
    create_revenue_trend_chart,
    create_revenue_pie_chart,
    create_price_chart,
    create_funnel_chart,
    create_institutional_chart,
)
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_debt_ratio_analogy,
    get_volume_analogy,
    get_institutional_analogy,
)
from src.services.news_summarizer import summarize_news, get_news_impact_level

# ── 頁面設定 ──────────────────────────────────────────
st.set_page_config(
    page_title="股識 Stock Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 自定義 CSS（PPT 風格）────────────────────────────
st.markdown("""
<style>
    /* 全局字型 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

    * {
        font-family: 'Noto Sans TC', sans-serif;
    }

    /* 隱藏 Streamlit 預設元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 主容器 */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* 公司名片標題 */
    .company-name {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 0.2rem;
    }

    .company-id {
        font-size: 1.2rem;
        color: #7F8C8D;
        font-weight: 300;
    }

    .one-liner {
        font-size: 1.4rem;
        font-weight: 500;
        color: #2C3E50;
        text-align: center;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #EBF5FB 0%, #D4E6F1 100%);
        border-radius: 12px;
        margin: 1rem 0;
        line-height: 1.8;
        border-left: 5px solid #3498DB;
    }

    /* 關鍵數字卡片 */
    .metric-card {
        background: #F8F9FA;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #3498DB;
        transition: transform 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2C3E50;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-top: 0.3rem;
    }

    .metric-analogy {
        font-size: 0.85rem;
        color: #27AE60;
        margin-top: 0.5rem;
        font-style: italic;
        line-height: 1.4;
    }

    /* 營收組成卡片 */
    .revenue-section {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }

    .revenue-item {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3498DB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .revenue-item-name {
        font-weight: 600;
        color: #2C3E50;
        font-size: 1rem;
    }

    .revenue-item-desc {
        font-size: 0.85rem;
        color: #5D6D7E;
        margin-top: 0.3rem;
    }

    .revenue-item-pct {
        font-size: 1.1rem;
        font-weight: 700;
        color: #3498DB;
    }

    /* 新聞卡片 */
    .news-card {
        background: #FFF8F0;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #F39C12;
        margin: 0.5rem 0;
    }

    .news-title {
        font-weight: 600;
        color: #2C3E50;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .news-summary {
        font-size: 0.9rem;
        color: #5D6D7E;
        line-height: 1.6;
        background: white;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-top: 0.5rem;
    }

    .news-meta {
        font-size: 0.8rem;
        color: #95A5A6;
        margin-top: 0.5rem;
    }

    .news-impact-high {
        display: inline-block;
        background: #FADBD8;
        color: #C0392B;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .news-impact-medium {
        display: inline-block;
        background: #FEF9E7;
        color: #D4AC0D;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .news-impact-low {
        display: inline-block;
        background: #E8F8F5;
        color: #1ABC9C;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    /* 區塊標題 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2C3E50;
        border-left: 4px solid #3498DB;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #7F8C8D;
        margin-bottom: 1rem;
    }

    /* 導航標籤 */
    .nav-tab {
        display: inline-block;
        padding: 0.6rem 1.5rem;
        margin: 0.3rem;
        border-radius: 20px;
        background: #ECF0F1;
        color: #2C3E50;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }

    .nav-tab:hover {
        background: #3498DB;
        color: white;
    }

    .nav-tab.active {
        background: #3498DB;
        color: white;
    }

    /* 警語 */
    .disclaimer {
        background: #FEF9E7;
        border: 1px solid #F9E79F;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #7D6608;
        margin-top: 2rem;
    }

    /* 數據來源標籤 */
    .data-source {
        font-size: 0.75rem;
        color: #BDC3C7;
        text-align: right;
        margin-top: 0.5rem;
    }

    /* 歡迎頁面 */
    .welcome-hero {
        text-align: center;
        padding: 4rem 2rem;
    }

    .welcome-hero h1 {
        font-size: 3rem;
        color: #2C3E50;
    }

    .welcome-hero p {
        font-size: 1.3rem;
        color: #7F8C8D;
        margin-top: 1rem;
    }

    /* 分隔線 */
    .custom-hr {
        border: none;
        border-top: 1px solid #ECF0F1;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ── 初始化 ────────────────────────────────────────────

@st.cache_resource
def get_client():
    return FinMindClient(cache_dir=".cache")


client = get_client()


# ── 側邊欄：搜尋 ──────────────────────────────────────

with st.sidebar:
    st.markdown("## 🔍 股識")
    st.markdown("*認識一家公司，從這裡開始*")
    st.markdown("---")

    # 搜尋框
    search_input = st.text_input(
        "輸入股票代號或名稱",
        placeholder="例如：2330 或 台積電",
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 快速瀏覽")

    # 熱門股票
    hot_stocks = [
        ("2330", "台積電"),
        ("2317", "鴻海"),
        ("2454", "聯發科"),
        ("2308", "台達電"),
        ("2881", "富邦金"),
        ("1101", "台泥"),
        ("2002", "中鋼"),
        ("1301", "台塑"),
    ]

    for sid, name in hot_stocks:
        if st.button(f"{sid} {name}", key=f"hot_{sid}", use_container_width=True):
            st.session_state["stock_id"] = sid
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
    ⚠️ 本工具僅供認識公司使用，<br>
    不構成任何投資建議。<br>
    投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)


# ── 主內容 ────────────────────────────────────────────

# 決定要顯示的股票
stock_id = search_input.strip() if search_input else st.session_state.get("stock_id", None)

if not stock_id:
    # 歡迎頁面
    st.markdown("""
    <div class="welcome-hero">
        <h1>📊 股識</h1>
        <p>認識一家公司，從這裡開始</p>
        <p style="font-size: 1rem; color: #95A5A6; margin-top: 2rem;">
            在左側輸入股票代號或名稱，開始認識一家公司
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # 取得股票資料
    with st.spinner(f"正在載入 {stock_id} 的資料..."):
        try:
            stock_info = client.get_stock_info(stock_id)
            if len(stock_info) == 0:
                st.error(f"找不到股票代號 {stock_id}，請確認是否正確。")
                st.stop()

            stock_name = stock_info.iloc[0]["stock_name"]
            industry = stock_info.iloc[0]["industry_category"]

            # 取得各項資料
            latest_price = client.get_latest_price(stock_id)
            latest_per_pbr = client.get_latest_per_pbr(stock_id)
            monthly_revenue = client.get_monthly_revenue(stock_id)
            daily_price = client.get_daily_price(stock_id)
            financial = client.get_financial_statement(stock_id)
            news = client.get_news(stock_id)
            institutional = client.get_institutional_investors(stock_id)
            balance_sheet = client.get_balance_sheet(stock_id)

            # 計算額外指標
            extra_metrics = _calc_extra_metrics(financial, balance_sheet, monthly_revenue)

        except Exception as e:
            st.error(f"資料載入失敗：{e}")
            st.stop()

    # ══════════════════════════════════════════════════
    # 第一頁：公司名片
    # ══════════════════════════════════════════════════

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="company-name">{stock_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="company-id">{stock_id} ｜ {industry}</div>', unsafe_allow_html=True)
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            color = "#E74C3C" if change >= 0 else "#2ECC71"
            sign = "+" if change >= 0 else ""
            st.markdown(f"""
            <div style="text-align: right;">
                <span style="font-size: 2rem; font-weight: 700; color: #2C3E50;">{price:,.0f}</span>
                <span style="font-size: 1.2rem; color: {color};">{sign}{change:,.0f}</span>
                <br><span style="font-size: 0.8rem; color: #7F8C8D;">{latest_price['date']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

    # 一句話定位
    one_liner = get_one_liner(stock_id, stock_name, industry)
    st.markdown(f'<div class="one-liner">💡 {one_liner}</div>', unsafe_allow_html=True)

    # 關鍵數字三連卡
    st.markdown('<div class="section-title">關鍵數字</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{per:.1f}</div>
                <div class="metric-label">本益比 (PER)</div>
                <div class="metric-analogy">{get_per_analogy(per)}</div>
            </div>
            """, unsafe_allow_html=True)
        elif extra_metrics.get("gross_margin"):
            gm = extra_metrics["gross_margin"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{gm:.1f}%</div>
                <div class="metric-label">毛利率</div>
                <div class="metric-analogy">{get_gross_margin_analogy(gm)}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            yoy = extra_metrics.get("revenue_yoy")
            yoy_str = f'<div class="metric-analogy">{get_yoy_analogy(yoy)}</div>' if yoy is not None else ""
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{rev:,.0f} 億</div>
                <div class="metric-label">最近月營收</div>
                <div class="metric-analogy">{get_revenue_analogy(rev, industry)}</div>
                {yoy_str}
            </div>
            """, unsafe_allow_html=True)
        elif extra_metrics.get("roe"):
            roe = extra_metrics["roe"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{roe:.1f}%</div>
                <div class="metric-label">ROE</div>
                <div class="metric-analogy">{get_roe_analogy(roe)}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dy:.2f}%</div>
                <div class="metric-label">殖利率</div>
                <div class="metric-analogy">{get_dividend_analogy(dy)}</div>
            </div>
            """, unsafe_allow_html=True)
        elif latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{pbr:.2f}</div>
                <div class="metric-label">淨值比 (PBR)</div>
                <div class="metric-analogy">{get_pbr_analogy(pbr)}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

    # 營收組成（圓餅圖 + 白話說明）
    st.markdown('<div class="section-title">營收組成</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">這家公司靠什麼賺錢？</div>', unsafe_allow_html=True)

    revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="data-source">📡 資料來源：FinMind 財報資料</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="revenue-section">', unsafe_allow_html=True)
        for item in revenue_items:
            st.markdown(f"""
            <div class="revenue-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="revenue-item-name">{item['name']}</span>
                    <span class="revenue-item-pct">{item['value']:.0f}%</span>
                </div>
                <div class="revenue-item-desc">{item['description']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

    # 營收趨勢圖
    st.markdown('<div class="section-title">營收趨勢</div>', unsafe_allow_html=True)
    if len(monthly_revenue) > 0:
        fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="data-source">📡 資料來源：FinMind 月營收資料</div>', unsafe_allow_html=True)
    else:
        st.info("暫無營收資料")

    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

    # 近期動態（白話摘要版）
    st.markdown('<div class="section-title">近期動態</div>', unsafe_allow_html=True)
    if len(news) > 0:
        for i in range(min(3, len(news))):
            news_item = news.iloc[i]
            title = news_item['title']
            source = news_item.get('source', '未知')
            date_str = str(news_item.get('date', ''))[:10]
            impact = get_news_impact_level(title)
            summary = summarize_news(title, stock_name)

            impact_class = f"news-impact-{impact}"
            impact_label = {"high": "🔴 重大", "medium": "🟡 注意", "low": "🟢 參考"}[impact]

            st.markdown(f"""
            <div class="news-card">
                <div class="news-title">
                    <span class="{impact_class}">{impact_label}</span>
                    📰 {title}
                </div>
                <div class="news-summary">{summary}</div>
                <div class="news-meta">📡 {source} ｜ {date_str}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("近期無重大新聞")

    # 免責聲明
    st.markdown("""
    <div class="disclaimer">
    ⚠️ 本工具僅供認識公司使用，所有數據來自公開資訊觀測站與 FinMind。
    不構成任何投資建議。投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)


# ── 輔助函數 ──────────────────────────────────────────

def _calc_extra_metrics(financial_df, balance_sheet_df, monthly_revenue_df) -> dict:
    """計算額外的財務指標"""
    metrics = {}

    # 毛利率（從損益表）
    if financial_df is not None and len(financial_df) > 0:
        try:
            latest_date = financial_df["date"].max()
            latest = financial_df[financial_df["date"] == latest_date]

            revenue = _find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
            gross_profit = _find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
            operating_income = _find_financial_value(latest, ["營業利益", "營業利潤", "Operating Income", "operating_income"])
            net_income = _find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])

            if revenue and revenue > 0:
                if gross_profit:
                    metrics["gross_margin"] = round(gross_profit / revenue * 100, 1)
                if operating_income:
                    metrics["operating_margin"] = round(operating_income / revenue * 100, 1)
                if net_income:
                    metrics["net_margin"] = round(net_income / revenue * 100, 1)
        except Exception:
            pass

    # 負債比（從資產負債表）
    if balance_sheet_df is not None and len(balance_sheet_df) > 0:
        try:
            latest_date = balance_sheet_df["date"].max()
            latest = balance_sheet_df[balance_sheet_df["date"] == latest_date]

            total_assets = _find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
            total_liabilities = _find_financial_value(latest, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])

            if total_assets and total_assets > 0 and total_liabilities:
                metrics["debt_ratio"] = round(total_liabilities / total_assets * 100, 1)
        except Exception:
            pass

    # 營收年增率
    if monthly_revenue_df is not None and len(monthly_revenue_df) > 12:
        try:
            latest_rev = monthly_revenue_df.iloc[-1]["revenue"]
            last_year_rev = monthly_revenue_df.iloc[-13]["revenue"]
            if last_year_rev > 0:
                metrics["revenue_yoy"] = round((latest_rev - last_year_rev) / last_year_rev * 100, 1)
        except Exception:
            pass

    return metrics


def _find_financial_value(df, keywords: list) -> float:
    """從財務資料中根據關鍵字找值"""
    for _, row in df.iterrows():
        type_val = str(row.get("type", ""))
        for kw in keywords:
            if kw.lower() in type_val.lower():
                val = row.get("value")
                if pd.notna(val) and val != 0:
                    return float(val)
    return 0.0



