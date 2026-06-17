"""
股識 Stock Explorer
Streamlit 入口 — M2 完整版
"""

import sys
from pathlib import Path

# 確保 src/ 的父目錄在 Python path 中，使 from src.xxx 絕對 import 能正確運作
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
from src.services.validation import validate_stock_id
from src.core.i18n import t\nfrom src.pages.router import load_and_render_page

# ── 頁面設定 ──────────────────────────────────────────
st.set_page_config(
    page_title=t("app.title"),
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
    
    /* 確保側邊欄收合時，展開按鈕不會被 header 的隱藏給蓋住 */
    header [data-testid="stExpandSidebarButton"] {
        visibility: visible;
    }

    /* 主容器 */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* 警語 */
    .disclaimer {
        background: #FEF9E7;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #2C3E50;
        margin-top: 2rem;
    }

    /* Responsive adjustments for small screens */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 1rem !important;
        }
    }
    @media (max-width: 600px) {
        .main .block-container {
            padding: 0.5rem 0.5rem !important;
        }
    }

    /* Responsive: make multi-column rows wrap gracefully on narrow screens */
    @media (max-width: 900px) {
        div[data-testid="column"] {
            min-width: 0 !important;
        }
        /* Shrink font inside column containers on narrow screens */
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] p,
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] span {
            font-size: 0.75rem !important;
            word-break: break-all !important;
        }
        /* Make buttons inside multi-col rows smaller */
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] button {
            font-size: 0.7rem !important;
            padding: 0.2rem 0.4rem !important;
            min-height: 0 !important;
        }
        /* Shrink markdown text in column rows */
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stMarkdown {
            font-size: 0.75rem !important;
        }
    }

    /* Style the collapse toggle button */
    button[kind="header"] {
        z-index: 999 !important;
        position: relative !important;
    }
    /* Hide Streamlit's auto-generated page nav in sidebar */
    section[data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    /* Ensure search input text is visible */
    section[data-testid="stSidebar"] input[type="text"] {
        color: #2C3E50 !important;
    }
    section[data-testid="stSidebar"] input[type="text"]::placeholder {
        color: #7F8C8D !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hide Streamlit's auto-generated sidebar nav via JS injection
_hide_nav_js = """
<script>
(function() {
    // 清除 Streamlit 記住的側邊欄狀態，強制每次載入都展開
    try {
        var keysToRemove = [];
        for (var i = 0; i < window.parent.localStorage.length; i++) {
            var key = window.parent.localStorage.key(i);
            if (key && key.toLowerCase().includes('sidebar')) {
                keysToRemove.push(key);
            }
        }
        keysToRemove.forEach(k => window.parent.localStorage.removeItem(k));
    } catch (e) {}

    function hideNav() {
        var nav = document.querySelector('section[data-testid="stSidebarNav"]');
        if (nav) {
            nav.style.cssText = 'display:none!important;height:0!important;overflow:hidden!important;visibility:hidden!important;';
        }
    }
    hideNav();
    // Use MutationObserver to catch Streamlit re-renders
    var target = document.querySelector('section[data-testid="stSidebar"]') || document.body;
    var observer = new MutationObserver(hideNav);
    observer.observe(target, { childList: true, subtree: true, attributes: true });
})();
</script>
"""
st.html(_hide_nav_js)


# ── 初始化 ────────────────────────────────────────────
from src.pages.url_sync import sync_url_to_session, navigate_to
from src.data.finmind_client import get_rate_limit_status

# Sync URL ↔ session_state (browser back/forward support)
sync_url_to_session()

@st.cache_resource
def get_client():
    from src.data.finmind_client import FinMindClient
    return FinMindClient(cache_dir=".cache")


client = get_client()

# ── 側邊欄 ──────────────────────────────────────────────

def _render_sidebar_hot_stocks(client):
    """Render hot stocks section with collapsible behavior."""
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
        if st.button(f"{sid} {name}", key=f"sidebar_hot_{sid}", use_container_width=True):
            navigate_to(page="名片", stock_id=sid)

def _render_sidebar_hot_etfs(client):
    """Render hot ETFs section."""
    hot_etfs = [
        ("0050", "元大台灣50"),
        ("0056", "元大高股息"),
        ("00878", "國泰永續高股息"),
        ("00919", "群益台灣精選高息"),
        ("006208", "富邦台50"),
    ]
    for sid, name in hot_etfs:
        if st.button(f"{sid} {name}", key=f"sidebar_etf_{sid}", use_container_width=True):
            navigate_to(page="名片", stock_id=sid)

def _render_sidebar(client):
    """Main sidebar rendering function."""
    st.markdown(t("sidebar.search_header"))
    st.markdown("*認識一家公司，從這裡開始*")
    st.markdown("---")

    # Search box
    search_input = st.text_input(
        "搜尋股票",
        placeholder="例如：2330 或 台積電",
        label_visibility="collapsed",
        key="sidebar_search",
    )

    # Rate limit banner
    _rate_status = get_rate_limit_status()
    if _rate_status["is_limited"]:
        st.warning("⚠️ FinMind API 暫時受限，資料可能不完整。請稍後再試。")

    st.markdown("---")

    # Primary navigation
    st.markdown("### 頁面導航")
    nav_items = [
        ("📊", "名片", "sidebar_nav_home"),
        ("🗺️", "產業熱力圖", "sidebar_nav_sector"),
        ("📈", "分類瀏覽", "sidebar_nav_category"),
        ("🏷️", "ETF 專區", "sidebar_nav_etf"),
        ("📋", "我的關注", "sidebar_nav_watchlist"),
        ("🔔", "事件儀表板", "sidebar_nav_events"),
        ("🔔", "通知中心", "sidebar_nav_notifications"),
        ("📝", "投資備忘錄", "sidebar_nav_memo"),
        ("💰", "理財健康檢查", "sidebar_nav_wellness"),
        ("🔎", "股票探索", "sidebar_nav_screener"),
    ]
    for icon, label, key in nav_items:
        if st.button(f"{icon} {label}", key=key, use_container_width=True):
            navigate_to(page=label)

    st.markdown("---")

    # Hot stocks (collapsible)
    with st.expander("🔥 熱門股票", expanded=False):
        _render_sidebar_hot_stocks(client)

    # Hot ETFs (collapsible)
    with st.expander("🏷️ 熱門 ETF", expanded=False):
        _render_sidebar_hot_etfs(client)

    st.markdown("---")

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
    ⚠️ 本工具僅供認識公司使用，<br>
    不構成任何投資建議。<br>
    投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)

    return search_input


search_input = _render_sidebar(client)


# ── 主內容 ────────────────────────────────────────────

# 決定要顯示的股票（支援中文名稱搜尋）
stock_id = None

if search_input and search_input.strip():
    query = search_input.strip()
    if query.isdigit():
        # 看起來像是股票代號，先驗證格式
        is_valid, result = validate_stock_id(query)
        if is_valid:
            stock_id = result
        else:
            st.sidebar.error(f"❌ {result}")
    else:
        # 可能是中文名稱，使用搜尋
        matches = client.search_stocks(query)
        if len(matches) == 1:
            # 只有 1 筆符合，自動導航
            stock_id = matches.iloc[0]["stock_id"]
        elif len(matches) > 1:
            # 多筆符合，讓使用者選擇
            options = [f"{row['stock_id']} {row['stock_name']}" for _, row in matches.iterrows()]
            selected = st.sidebar.selectbox("找到多筆符合的股票：", options, key="search_select")
            if selected:
                stock_id = selected.split()[0]
        else:
            # 沒有符合
            st.sidebar.error("找不到符合的股票")
else:
    stock_id = st.session_state.get("stock_id", None)

if not stock_id:
    # 歡迎頁面
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
        <h1>📊 股識</h1>
        <p style="font-size:1.3rem;color:#7F8C8D;margin-top:1rem;">認識一家公司，從這裡開始</p>
        <p style="font-size:1rem;color:#7F8C8D;margin-top:2rem;">
            在左側輸入股票代號或名稱，開始認識一家公司
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 使用路由器載入並渲染頁面
    load_and_render_page(client, stock_id)
