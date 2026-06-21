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
from src.core.i18n import t
from src.pages.router import load_and_render_page
from src.services.benchmarks import get_industry_benchmarks

# ── 頁面設定 ──────────────────────────────────────────
# ── 頁面設定 ──────────────────────────────────────────
st.set_page_config(
    page_title=t("app.title"),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 自定義 CSS（PPT 風格）────────────────────────────
st.markdown(t("main.disclaimer"), unsafe_allow_html=True)

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
# Chinese name to stock ID mapping for common stocks
CHINESE_NAME_TO_STOCK_ID = {
    "台積電": "2330",
    "鴻海": "2317",
    "聯發科": "2454",
    "台達電": "2308",
    "富邦金": "2881",
    "台泥": "1101",
    "中鋼": "2002",
    "台塑": "1301",
    "元大台灣50": "0050",
    "元大高股息": "0056",
    "國泰永續高股息": "00878",
    "群益台灣精選高息": "00919",
    "富邦台50": "006208",
}
 
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

    # Search box
    search_input = st.text_input(
        t("main.sidebar.search_label"),
        placeholder=t("main.sidebar.search_placeholder"),
        label_visibility="collapsed",
        key="sidebar_search",
    )

    st.markdown(t("main.welcome.subtitle"))
    st.markdown("---")

    # Rate limit banner
    _rate_status = get_rate_limit_status()
    if _rate_status["is_limited"]:
        st.warning(t("main.sidebar.api_warning"))

    # Hot stocks (collapsible)
    with st.expander(f"🔥 {t('main.sidebar.hot_stocks')}", expanded=False):
        _render_sidebar_hot_stocks(client)

    # Hot ETFs (collapsible)
    with st.expander(f"🏷️ {t('main.sidebar.hot_etfs')}", expanded=False):
        _render_sidebar_hot_etfs(client)

    st.markdown("---")

    # Disclaimer
    st.markdown(t("main.disclaimer"), unsafe_allow_html=True)

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
        # First check hardcoded mapping for exact match
        if query in CHINESE_NAME_TO_STOCK_ID:
            stock_id = CHINESE_NAME_TO_STOCK_ID[query]
        else:
            matches = client.search_stocks(query)
        if len(matches) == 1:
            # 只有 1 筆符合，自動導航
            stock_id = matches.iloc[0]["stock_id"]
        elif len(matches) > 1:
            # 多筆符合，讓使用者選擇
            options = [f"{row['stock_id']} {row['stock_name']}" for _, row in matches.iterrows()]
            selected = st.sidebar.selectbox(t("main.search.multiple_results"), options, key="search_select")
            if selected:
                stock_id = selected.split()[0]
        else:
            # 沒有符合
            st.sidebar.error(t("main.search.not_found"))
else:
    stock_id = st.session_state.get("stock_id", None)

if not stock_id:
    # 歡迎頁面
    st.markdown(f"""
    <div style="text-align:center;padding:4rem 2rem;">
        <h1>📊 {t("main.home.title")}</h1>
        <p style="font-size:1.3rem;color:#7F8C8D;margin-top:1rem;">{t("main.home.lead1")}</p>
        <p style="font-size:1rem;color:#7F8C8D;margin-top:2rem;">
            {t("main.home.lead2")}
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 使用路由器載入並渲染頁面
    loading_text = t("main.loading.text")
    loading_subtext = t("main.loading.subtext")
    with st.spinner(f"{loading_text}\n{loading_subtext}"):
        load_and_render_page(client, stock_id)
