"""
股識 Stock Explorer
Streamlit 入口 — M2 完整版
"""

import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
from src.core.i18n import t
from src.pages.url_sync import sync_url_to_session, navigate_to
from src.pages.router import load_and_render_page


# ── PAGE KEY LOOKUP ─────────────────────────────
# Uses url_sync's built-in mapping (PAGE_KEY_TO_NAME / PAGE_NAME_TO_KEY)

_PAGE_KEY_TO_NAME = {
    "business_card": "名片", "operation_checkup": "營運健檢",
    "financial_health": "財務體質", "peer_comparison": "同業比較",
    "group_structure": "集團架構", "category_browser": "分類瀏覽",
    "etf_section": "ETF 專區", "watchlist": "我的關注",
    "event_dashboard": "事件儀表板", "settings": "設定",
    "daily_market": "今日市場動態",
}
_PAGE_NAME_TO_KEY = {v: k for k, v in _PAGE_KEY_TO_NAME.items()}


def _get_page_key() -> str:
    name = st.session_state.get("page")
    if name in _PAGE_NAME_TO_KEY:
        return _PAGE_NAME_TO_KEY[name]
    return st.session_state.get("page_key", "business_card")


def _navigate(page_key: str):
    navigate_to(page=page_key)


# ── PAGE SETUP ──────────────────────────────────────
st.set_page_config(
    page_title=t("app.title"),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ─────────────────────────────────────
st.html("""
<style>
/* FAB */
.fab-container {
  position: fixed; bottom: 24px; right: 24px; z-index: 999;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.fab-button {
  width: 56px; height: 56px; border-radius: 50%; background: #007AFF;
  color: white; border: none; box-shadow: 0 4px 16px rgba(0,122,255,0.3);
  font-size: 28px; cursor: pointer; display: flex; align-items: center;
  justify-content: center; transition: transform 0.2s, box-shadow 0.2s; line-height: 1;
}
.fab-button:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(0,122,255,0.4); }
.fab-button:active { transform: scale(0.95); }
.fab-menu {
  display: none; position: absolute; bottom: 70px; right: 0;
  background: white; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  padding: 6px; min-width: 210px; max-height: 60vh; overflow-y: auto;
}
.fab-menu.show { display: block; }
.fab-menu-item {
  padding: 10px 16px; cursor: pointer; border-radius: 10px; font-size: 14px;
  color: #1C1C1E; display: flex; align-items: center; gap: 10px;
  text-decoration: none; transition: background 0.15s;
}
.fab-menu-item:hover { background: #F2F2F7; text-decoration: none; color: #1C1C1E; }
.fab-divider { height: 1px; background: #E5E5EA; margin: 4px 12px; }
.fab-overlay {
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 998;
}
.fab-overlay.show { display: block; }
</style>
""")

# Hide Streamlit sidebar nav
st.html("""
<script>
(function(){
    function h(){var n=document.querySelector('section[data-testid="stSidebarNav"]');if(n)n.remove();}
    h();var t=document.querySelector('section[data-testid="stSidebar"]')||document.body;
    new MutationObserver(h).observe(t,{childList:true,subtree:true,attributes:true});
})();
</script>
""")

sync_url_to_session()


# ── INIT ────────────────────────────────────────────
from src.data.finmind_client import get_rate_limit_status

client = None

def _get_client():
    global client
    if client is None:
        from src.data.finmind_client import FinMindClient
        client = FinMindClient(cache_dir=".cache")
    return client


# ── SEARCH ──────────────────────────────────────────────

def _process_search(query: str) -> str | None:
    """Process search input, return stock_id or None."""
    if not query or not query.strip():
        return st.session_state.get("stock_id")

    q = query.strip()
    from src.services.validation import validate_stock_id
    c = _get_client()

    if q.isdigit():
        is_valid, result = validate_stock_id(q)
        if is_valid:
            return result
        st.error(f"❌ {result}")
        return st.session_state.get("stock_id")

    with st.spinner(t("main.search.searching")):
        results = c.search_stocks(q, case_sensitive=False)
    if results is None or results.empty:
        st.error(t("main.search.not_found"))
        return st.session_state.get("stock_id")
    if len(results) == 1:
        return results.iloc[0]["stock_id"]
    options = [f"{r['stock_id']} {r['stock_name']}" for _, r in results.iterrows()]
    selected = st.selectbox(t("main.search.multiple_results"), options, key="search_select")
    if selected:
        return selected.split()[0]
    return st.session_state.get("stock_id")


# ── SIDEBAR: ACTIVITY BAR ──────────────────────────────

_ACTIVITY_ITEMS = [
    ("business_card", "📇", "基本資料"),
    ("category_browser", "📂", "分類瀏覽"),
    ("etf_section", "🏷️", "ETF 專區"),
    ("watchlist", "⭐", "關注清單"),
    ("event_dashboard", "🔔", "事件儀表板"),
    ("daily_market", "📈", "市場動態"),
    ("settings", "⚙️", "設定"),
]

def _render_activity_bar():
    """Render the left Activity Bar with icon navigation."""
    current_key = _get_page_key()

    st.markdown(f"### 📊 {t('app.title')}")
    st.markdown("---")

    for key, icon, label in _ACTIVITY_ITEMS:
        is_active = (key == current_key)
        btn_label = f"{icon} {t(f'page.{key}') if key != 'business_card' else label}"
        if is_active:
            btn_label = f"▸ {btn_label}"
        if st.button(btn_label, key=f"nav_{key}", use_container_width=True, type="secondary" if not is_active else "primary"):
            _navigate(key)

    st.markdown("---")

    # Rate limit
    _rate_status = get_rate_limit_status()
    if _rate_status["is_limited"]:
        st.warning(t("main.sidebar.api_warning"))

    # Hot stocks
    hot_stocks = [
        ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
        ("2308", "台達電"), ("2881", "富邦金"),
    ]
    with st.expander(f"🔥 {t('main.sidebar.hot_stocks')}", expanded=False):
        for sid, name in hot_stocks:
            if st.button(f"{sid} {name}", key=f"hot_{sid}", use_container_width=True):
                st.session_state["stock_id"] = sid
                _navigate("business_card")

    hot_etfs = [
        ("0050", "元大台灣50"), ("0056", "元大高股息"),
        ("00878", "國泰永續高股息"), ("00919", "群益台灣精選高息"),
    ]
    with st.expander(f"🏷️ {t('main.sidebar.hot_etfs')}", expanded=False):
        for sid, name in hot_etfs:
            if st.button(f"{sid} {name}", key=f"hot_etf_{sid}", use_container_width=True):
                st.session_state["stock_id"] = sid
                _navigate("business_card")

    st.markdown("---")
    st.markdown(t("main.disclaimer"), unsafe_allow_html=True)


# ── TOP SEARCH BAR ──────────────────────────────────────

_search_col, _status_col = st.columns([4, 1])
with _search_col:
    search_input = st.text_input(
        t("main.sidebar.search_label"),
        placeholder=t("main.sidebar.search_placeholder"),
        label_visibility="collapsed",
        key="global_search",
    )
with _status_col:
    _rate_status = get_rate_limit_status()
    if _rate_status["is_limited"]:
        st.warning(f"⚠️ {t('rate_limited')}")


# ── SIDEBAR ──────────────────────────────────────────────

with st.sidebar:
    _render_activity_bar()


# ── MAIN CONTENT ─────────────────────────────────────────

stock_id = _process_search(search_input)

if not stock_id:
    st.markdown(f"""
    <div style="text-align:center;padding:2rem;">
        <h1 style="font-size:1.5rem;">📊 {t("main.home.title")}</h1>
        <p style="color:#7F8C8D;margin-top:0.5rem;">{t("main.home.lead1")}</p>
        <p style="color:#5A6B7D;margin-top:0.5rem;font-style:italic;">{t("main.home.quick_hint")}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    if stock_id != st.session_state.get("stock_id"):
        st.session_state["stock_id"] = stock_id
    c = _get_client()
    load_and_render_page(c, stock_id)


# ── FAB HTML ─────────────────────────────────────────────

_fab_stock_id = st.session_state.get("stock_id", "")
st.html(f"""
<div class="fab-overlay" id="fabOverlay" onclick="closeFabMenu()"></div>
<div class="fab-container">
  <div class="fab-menu" id="fabMenu">
    <a class="fab-menu-item" href="?page=名片&stock_id={_fab_stock_id}">📇 基本資料</a>
    <a class="fab-menu-item" href="?page=營運健檢&stock_id={_fab_stock_id}">🔧 營運健檢</a>
    <a class="fab-menu-item" href="?page=財務體質&stock_id={_fab_stock_id}">💊 財務體質</a>
    <a class="fab-menu-item" href="?page=同業比較&stock_id={_fab_stock_id}">📊 同業比較</a>
    <a class="fab-menu-item" href="?page=集團架構&stock_id={_fab_stock_id}">🏗️ 集團架構</a>
    <div class="fab-divider"></div>
    <a class="fab-menu-item" href="?page=營收結構樹&stock_id={_fab_stock_id}">🌳 營收結構樹</a>
    <a class="fab-menu-item" href="?page=同業比較故事&stock_id={_fab_stock_id}">📚 同業比較故事</a>
    <a class="fab-menu-item" href="?page=護城河比較&stock_id={_fab_stock_id}">🏰 護城河比較</a>
  </div>
  <button class="fab-button" id="fabBtn" onclick="toggleFabMenu()">+</button>
</div>
<script>
function toggleFabMenu(){{
  var m=document.getElementById('fabMenu'),o=document.getElementById('fabOverlay'),b=document.getElementById('fabBtn');
  var isOpen=m.classList.contains('show');
  m.classList.toggle('show');o.classList.toggle('show');
  b.textContent=isOpen?'+':'×';
}}
function closeFabMenu(){{
  document.getElementById('fabMenu').classList.remove('show');
  document.getElementById('fabOverlay').classList.remove('show');
  document.getElementById('fabBtn').textContent='+';
}}
</script>
""")
