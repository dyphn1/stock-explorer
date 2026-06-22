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
from src.pages.router import load_and_render_page, get_stock_data
from src.pages._router_base import _infocard
from src.services.benchmarks import get_industry_benchmarks
from src.services.roe_calculator import calc_roe_ttm
import os

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
        var nav = document.querySelector("section[data-testid="stSidebarNav"]");
        if (nav) {
            nav.remove();
        }
    }\n    hideNav();\n    // Use MutationObserver to catch Streamlit re-renders\n
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

@st.cache_data(ttl=24*3600)
def get_chinese_name_mapping():
    mapping = {}
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'chinese_names.yaml')
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        mapping[key] = value
    return mapping

@st.cache_data(ttl=24*3600)
def get_all_stocks():
    client = get_client()
    df = client._fetch_all_stock_info()
    return df[['stock_id', 'stock_name']].copy()



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


def render_navbar(data: dict):
    """頂部導航列：公司名稱 + 價格 + 分頁標籤 (copied from _router_base.py)"""
    import streamlit as st
    from src.core.i18n import t
    from src.pages.router import _get_localized_page_labels, _get_label_to_key_map
    from src.pages.url_sync import navigate_to

    stock_name = data["stock_name"]
    stock_id = data["stock_id"]
    industry = data["industry"]
    latest_price = data["latest_price"]

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{stock_name}** `{stock_id}` ｜ {industry}")
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            sign = "+" if change >= 0 else ""
            st.markdown(f"**{price:,.0f}** `{sign}{change:,.0f}`")

    # 分頁標籤
    page_labels = _get_localized_page_labels()
    # Get current label from the page key
    current_page_key = st.session_state.get("page_key", "business_card")
    current_label = t(f"page.{current_page_key}")
    try:
        current_idx = page_labels.index(current_label)
    except ValueError:
        current_idx = 0

    selected_label = st.radio(
        t("router.page_navigation"),
        page_labels,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio",
    )

    # Map selected label back to page key
    label_to_key = _get_label_to_key_map()
    selected_key = label_to_key.get(selected_label)
    if selected_key is None:
        selected_key = "business_card"

    if selected_key != current_page_key:
        navigate_to(page=selected_key)

    st.markdown("--\"")


def render_metric_card(title: str, value_str: str, description: str, analogy: str = "", is_positive: bool | None = None):
    """Render a metric card similar to the prototype."""
    import streamlit as st
    from src.core.i18n import t

    # Determine value color
    value_color = ""
    if is_positive is not None:
        if is_positive:
            value_color = "price-up"
        else:
            value_color = "price-down"
    else:
        value_color = ""

    # Analogy background
    analogy_bg = ""
    if analogy:
        analogy_bg = 'style="background:#F8F9FA;padding:8px;border-radius:4px;font-size:12px;font-style:italic;color:#7F8C8D;"'

    st.markdown(
        f"""
    <div class="card" style="background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.05);border:1px solid #E1E4E8;">
        <div class="card-title">{title}</div>
        <div class="metric-value {value_color}">{value_str}</div>
        <div class="metric-desc">{description}</div>
        <div class="analogy" {analogy_bg}>{analogy}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


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
        chinese_name_map = get_chinese_name_mapping()
        if query in chinese_name_map:
            stock_id = chinese_name_map[query]
        else:
            all_stocks = get_all_stocks()
            # Filter where stock_name contains query (case-insensitive)
            matches = all_stocks[all_stocks['stock_name'].str.contains(query, case=False, na=False)]
            if len(matches) == 1:
                stock_id = matches.iloc[0]['stock_id']
            elif len(matches) > 1:
                options = [f"{row['stock_id']} {row['stock_name']}" for _, row in matches.iterrows()]
                selected = st.sidebar.selectbox(t("main.search.multiple_results"), options, key="search_select")
                if selected:
                    stock_id = selected.split()[0]
            else:
                st.sidebar.error(t("main.search.not_found"))
else:
    stock_id = st.session_state.get("stock_id", None)

if not stock_id:
    # 歡迎頁面
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 2rem;">
        <h1 style=\"font-size:2rem;\">📊 {t("main.home.title")}</h1>
        <p style="font-size:1.1rem;color:#7F8C8D;margin-top:0.5rem;">{t("main.home.lead1")}</p>
        <p style="font-size:0.9rem;color:#7F8C8D;margin-top:0.5rem;">
            {t("main.home.lead2")}
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    data = get_stock_data(client, stock_id)
    if data is None:
        st.error(t("error.not_found", sid=stock_id))
    else:
        render_navbar(data)
        # compute metrics
        from src.services.financial_metrics import calc_extra_metrics, find_financial_value
        extra_metrics = calc_extra_metrics(
            data.get("financial"),
            data.get("balance_sheet"),
            data.get("monthly_revenue"),
        )
        revenue_yoy = extra_metrics.get("revenue_yoy")
        net_margin = extra_metrics.get("net_margin")
        # compute ROE using TTM
        roe = None
        roe_warning = None
        if data.get("financial") is not None and len(data["financial"]) > 0 and data.get("balance_sheet") is not None and len(data["balance_sheet"]) > 0:
            roe_dict = calc_roe_ttm(
                data.get("financial"),
                data.get("balance_sheet"),
                industry=data.get("industry", ""),
            )
            if roe_dict is not None:
                roe = roe_dict.get("roe")
                roe_warning = roe_dict.get("warning")
        # compute debt-to-equity (still needs latest total_equity and total_liabilities)
        total_equity = None
        total_liabilities = None
        if data.get("balance_sheet") is not None and len(data["balance_sheet"]) > 0:
            latest_date = data["balance_sheet"]["date"].max()
            latest_bs = data["balance_sheet"][data["balance_sheet"]["date"] == latest_date]
            total_equity = find_financial_value(latest_bs, ["權益總計", "股東權益", "Total Equity", "total_equity"])
            total_liabilities = find_financial_value(latest_bs, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])
        debt_to_equity = None
        if total_liabilities is not None and total_equity is not None and total_equity != 0:
            debt_to_equity = round(total_liabilities / total_equity, 2)
        # format values
        def fmt_percent(val):
            if val is None:
                return "-"
            from src.core.i18n import format_percent
            return format_percent(val)
        # render cards using tabs
        tab1, tab2 = st.tabs([t("main.tab.key_metrics"), t("main.tab.financial_chart")])

        with tab1:
            # 2x2 grid for metric cards
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                render_metric_card(
                    title=f"📊 {t('metric_education.revenue_yoy_display_name')}",
                    value_str=fmt_percent(revenue_yoy),
                    description=t("metric_education.revenue_yoy_explanation") if revenue_yoy is not None else "",
                    analogy="",
                    is_positive=(revenue_yoy is not None and revenue_yoy >= 0),
                )
            with m_col2:
                render_metric_card(
                    title=f"💰 {t('metric_education.net_margin_display_name')}",
                    value_str=fmt_percent(net_margin),
                    description=t("metric_education.net_margin_explanation") if net_margin is not None else "",
                    analogy="",
                    is_positive=(net_margin is not None and net_margin >= 0),
                )
            m_col3, m_col4 = st.columns(2)
            with m_col3:
                render_metric_card(
                    title=f"📈 {t('metric_education.roe_display_name')}",
                    value_str=fmt_percent(roe),
                    description=t("metric_education.roe_explanation") if roe is not None else "",
                    analogy="",
                    is_positive=(roe is not None and roe >= 0),
                )
            with m_col4:
                render_metric_card(
                    title=f"⚖️ {t('metric_education.debt_ratio_display_name')}",
                    value_str=f"{debt_to_equity:.2f}" if debt_to_equity is not None else "-",
                    description=t("metric_education.debt_ratio_explanation") if debt_to_equity is not None else "",
                    analogy="",
                    is_positive=False,
                )

        with tab2:
            # Financial chart (full width)
            st.markdown(
                """
                <div class="card" style="background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.05);border:1px solid #E1E4E8;">
                    <div class="card-title">📉 Revenue Trend (Last 12 Months)</div>
                    <div class="chart-placeholder" style="width:100%;height:250px;background:#f9f9f9;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#aaa;border-radius:8px;margin-top:10px;">
                        [ Plotly Line Chart: Monthly Revenue Trend ]
                    </div>
                    <div style="font-size:12px;color:#7F8C8D;margin-top:10px;text-align:right;">Source: FinMind API</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
