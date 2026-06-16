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
from src.pages.router import load_and_render_page
from src.core.i18n import t, set_lang, get_available_locales

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
        border: 1px solid #F9E79F;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #7D6608;
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
        color: #95A5A6 !important;
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

# Initialize language
if "lang" not in st.session_state:
    st.session_state["lang"] = "zh-TW"

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
    st.markdown(f"## {t("sidebar.title")}")
    st.markdown(f"*{t("app.subtitle")}*")
    st.markdown("---")

    # Search box
    search_input = st.text_input(
        t("app.search_label"),
        placeholder=t("app.search_placeholder"),
        label_visibility="collapsed",
        key="sidebar_search",
    )

    # Rate limit banner
    _rate_status = get_rate_limit_status()
    if _rate_status["is_limited"]:
        st.warning(t("status.rate_limited_short"))

    st.markdown("---")

    # Primary navigation
    st.markdown(f"### {t("sidebar.navigation_header")}")
    nav_items = [
        ("📊", t("page.business_card"), "sidebar_nav_home"),
        ("🗺️", t("page.sector_heatmap"), "sidebar_nav_sector"),
        ("📈", t("page.category_browser"), "sidebar_nav_category"),
        ("🏷️", t("page.etf_section"), "sidebar_nav_etf"),
        ("📋", t("page.watchlist"), "sidebar_nav_watchlist"),
        ("🔔", t("page.event_dashboard"), "sidebar_nav_events"),
        ("🔔", t("page.notification_center"), "sidebar_nav_notifications"),
        ("📝", t("page.investment_memo"), "sidebar_nav_memo"),
        ("💰", t("page.financial_wellness"), "sidebar_nav_wellness"),
        ("🔎", t("page.stock_screener"), "sidebar_nav_screener"),
    ]
        if st.button(f"{icon} {label}", key=key, use_container_width=True):
            navigate_to(page=label)

    st.markdown("---")

    # Hot stocks (collapsible)
    with st.expander(t("sidebar.hot_stocks"), expanded=False):
        _render_sidebar_hot_stocks(client)

    # Hot ETFs (collapsible)
    with st.expander(t("sidebar.hot_etfs"), expanded=False):
        _render_sidebar_hot_etfs(client)

    st.markdown("---")
    st.markdown("---")
    st.markdown(f"### {t("sidebar.language_header")}")
    lang_options = get_available_locales()
    lang_labels = [opt["label"] for opt in lang_options]
    lang_codes = [opt["code"] for opt in lang_options]
    current_lang = st.session_state.get("lang", "zh-TW")
    try:
        current_index = lang_codes.index(current_lang)
    except ValueError:
        current_index = 0
    selected_label = st.radio("", lang_labels, index=current_index, label_visibility="collapsed")
    selected_lang = lang_codes[lang_labels.index(selected_label)]
    if selected_lang != st.session_state.get("lang"):
        set_lang(selected_lang)
        st.rerun()

    # Disclaimer
    st.markdown(f'''
    <div class="disclaimer">
    ⚠️ {t('disclaimer.general')}
    </div>
    ''', unsafe_allow_html=True)

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
            selected = st.sidebar.selectbox(t("stock.search_multiple"), options, key="search_select")
            if selected:
                stock_id = selected.split()[0]
        else:
            # 沒有符合
            st.sidebar.error(t("error.search_no_results"))
else:
    stock_id = st.session_state.get("stock_id", None)

if not stock_id:
    # 歡迎頁面
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
        <h1>{t("welcome.title")}</h1>
        <p style="font-size:1.3rem;color:#7F8C8D;margin-top:1rem;">{t("app.subtitle")}</p>
        <p style="font-size:1rem;color:#95A5A6;margin-top:2rem;">{t("welcome.description")}</p>
    </div>
