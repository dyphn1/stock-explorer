"""
股識 Stock Explorer
Streamlit 入口 — M2 完整版
"""

import streamlit as st
from src.pages.router import load_and_render_page

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
    from src.data.finmind_client import FinMindClient
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
    st.markdown("### 📈 熱門股票")

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
            st.session_state["page"] = "名片"  # 重置到名片頁
            st.rerun()

    st.markdown("---")
    st.markdown("### 🏷️ 熱門 ETF")

    hot_etfs = [
        ("0050", "元大台灣50"),
        ("0056", "元大高股息"),
        ("00878", "國泰永續高股息"),
        ("00919", "群益台灣精選高息"),
        ("006208", "富邦台50"),
    ]

    for sid, name in hot_etfs:
        if st.button(f"{sid} {name}", key=f"etf_{sid}", use_container_width=True):
            st.session_state["stock_id"] = sid
            st.session_state["page"] = "名片"
            st.rerun()

    # 我的關注快捷入口
    st.markdown("---")
    if st.button("📋 我的關注", key="sidebar_watchlist", use_container_width=True):
        st.session_state["page"] = "我的關注"
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
    <div style="text-align:center;padding:4rem 2rem;">
        <h1>📊 股識</h1>
        <p style="font-size:1.3rem;color:#7F8C8D;margin-top:1rem;">認識一家公司，從這裡開始</p>
        <p style="font-size:1rem;color:#95A5A6;margin-top:2rem;">
            在左側輸入股票代號或名稱，開始認識一家公司
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 使用路由器載入並渲染頁面
    load_and_render_page(client, stock_id)
