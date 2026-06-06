"""
股識 Stock Explorer
Streamlit 入口
"""

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.services.chart import (
    create_revenue_trend_chart,
    create_price_chart,
    create_funnel_chart,
    create_institutional_chart,
)

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
        font-size: 1.5rem;
        font-weight: 500;
        color: #3498DB;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #EBF5FB 0%, #D4E6F1 100%);
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* 關鍵數字卡片 */
    .metric-card {
        background: #F8F9FA;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #3498DB;
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
    
    /* 區塊標題 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2C3E50;
        border-left: 4px solid #3498DB;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
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
    <div style="text-align: center; padding: 4rem 2rem;">
        <h1 style="font-size: 3rem; color: #2C3E50;">📊 股識</h1>
        <p style="font-size: 1.3rem; color: #7F8C8D; margin-top: 1rem;">
            認識一家公司，從這裡開始
        </p>
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

    st.markdown("---")

    # 一句話定位
    one_liner = _generate_one_liner(stock_id, stock_name, industry)
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
                <div class="metric-analogy">每賺 1 元，市場願意付 {per:.1f} 元</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{rev:,.0f} 億</div>
                <div class="metric-label">最近月營收</div>
                <div class="metric-analogy">大約是 {rev/1000:.1f} 個小目標</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dy:.2f}%</div>
                <div class="metric-label">殖利率</div>
                <div class="metric-analogy">每放 100 元，大約領回 {dy:.2f} 元</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 營收趨勢圖
    st.markdown('<div class="section-title">營收趨勢</div>', unsafe_allow_html=True)
    if len(monthly_revenue) > 0:
        fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暫無營收資料")

    st.markdown("---")

    # 近期動態
    st.markdown('<div class="section-title">近期動態</div>', unsafe_allow_html=True)
    if len(news) > 0:
        latest_news = news.iloc[0]
        st.markdown(f"""
        <div style="background: #F8F9FA; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #F39C12;">
            <div style="font-weight: 600; color: #2C3E50; margin-bottom: 0.5rem;">
                📰 {latest_news['title']}
            </div>
            <div style="font-size: 0.85rem; color: #7F8C8D;">
                {latest_news['source']} ｜ {str(latest_news['date'])[:10]}
            </div>
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

def _generate_one_liner(stock_id: str, stock_name: str, industry: str) -> str:
    """生成一句話定位（第一版用規則，未來可接 LLM）"""
    # 常見公司的一句話定位
    one_liners = {
        "2330": "全世界最大的晶圓代工廠，幫蘋果、輝達等科技巨頭製造晶片",
        "2317": "全球最大的電子代工帝國，iPhone 的主要組裝廠",
        "2454": "手機晶片設計龍頭，你的手機裡很可能有它的晶片",
        "2308": "電源供應器隱形冠軍，從手機充電器到電動車充電樁都有它的身影",
        "2881": "台灣最大的金融控股集團之一，旗下有銀行、證券、壽險",
        "1101": "台灣最老牌的水泥廠，從蓋房子到基礎建設都少不了它",
        "2002": "台灣鋼鐵業龍頭，從建築鋼材到汽車鋼板都有生產",
        "1301": "台灣最大的塑膠集團，從塑膠袋到醫療用品都有它的產品",
    }

    if stock_id in one_liners:
        return one_liners[stock_id]

    # 通用模板
    return f"{industry}產業的重要成員，股票代號 {stock_id}"
