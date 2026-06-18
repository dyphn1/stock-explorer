"""
股識 Stock Explorer — M5 自適應更新
頁面路由器：根據 session_state['page'] 顯示不同頁面

TD-01 Phase 1+2: 使用 PluginRegistry 管理所有頁面。
所有頁面（獨立頁 + 股票分析頁）均通過 PluginRegistry 路由，
router.py 中不再有 if-elif 分頁鏈。
"""

import logging
import streamlit as st

from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import (
    get_stock_data,
)
from src.pages.event_dashboard import (
    _render_adaptive_banner,
    _render_event_alerts,
)
from src.services.adaptive_engine import (
    run_auto_detection,
)
from src.core.i18n import t, set_lang, get_available_locales
from src.services.watchlist import _is_etf as _is_etf_check
from src.pages.etf_detail import _render_etf_detail

# TD-01 Phase 1+2: Plugin Registry
from src.core.plugin_protocol import PluginRenderContext, PluginCategory
from src.core.plugin_registry import PluginRegistry

# Page keys for i18n (must match keys in locale files under 'page:' section)
PAGE_KEYS = [
    "business_card",
    "operation_checkup",
    "financial_health",
    "peer_comparison",
    "group_structure",
    "category_browser",
    "etf_section",
    "watchlist",
    "event_dashboard",
    "notification_center",
    "investment_memo",
    "financial_wellness",
    "stock_screener",
    "settings",
    "sector_heatmap",
    "daily_market",
    "case_study",
    "comprehension_check",
    "academy",
    "case_study_library",
    "first_visit_guide",
    "story_timeline",
    "full_story_timeline",
    "daily_story",
    "revenue_tree",
    "compare_stories",
    "moat_comparison",
    "debate_cards",
]

logger = logging.getLogger(__name__)


def _get_localized_page_labels():
    """Return list of localized page labels in the same order as PAGE_KEYS."""
    return [t(f"page.{key}") for key in PAGE_KEYS]


def _get_label_to_key_map():
    """Return mapping from localized label to page key."""
    labels = _get_localized_page_labels()
    return {label: key for key, label in zip(PAGE_KEYS, labels)}


# ── TD-01 Phase 1+2: Plugin Registry ────────────────────

# Standalone pages (no stock_id, no data required)
_STANDALONE_PLUGIN_KEYS = {
    # Phase 1 (existing)
    "category_browser",
    "settings",
    "event_dashboard",
    "notification_center",
    "daily_market",
    # Phase 2 Wave 1 (new)
    "watchlist",
    "investment_memo",
    "etf_section",
    "case_study",
    "financial_wellness",
    "comprehension_check",
    "case_study_library",
    "stock_screener",
    "sector_heatmap",
    "learn_first_gate",
    "first_visit_guide",
    "daily_story",
    # Phase 2 Waves 2+3 (new)
    "academy",
}

# Stock-dependent pages (require stock_id + data, rendered after data loading)
_STOCK_PLUGIN_KEYS = {
    "business_card",
    "operation_checkup",
    "financial_health",
    "peer_comparison",
    "group_structure",
    "story_timeline",
    "full_story_timeline",
    "revenue_tree",
    "compare_stories",
    "moat_comparison",
    "debate_cards",
}

_registry: PluginRegistry | None = None


def _get_registry() -> PluginRegistry:
    """Get or create the singleton PluginRegistry, discovering plugins once."""
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
        count = _registry.discover()
        logger.info("PluginRegistry initialized: %d plugins discovered.", count)
    return _registry


def _render_via_plugin(
    page_key: str,
    client: FinMindClient,
    stock_id: str | None = None,
    data: dict | None = None,
) -> bool:
    """Try to render a page via the PluginRegistry.

    Returns True if the page was handled by a plugin, False if not found
    (caller should fall back to legacy rendering).
    """
    registry = _get_registry()
    if not registry.has(page_key):
        return False

    plugin = registry.get(page_key)
    ctx = PluginRenderContext(
        page_key=page_key,
        data=data,
        client=client,
        stock_id=stock_id,
        session_state=st.session_state,
    )
    plugin.render(ctx)
    return True


# ── 初始化 ────────────────────────────────────────────


@st.cache_resource
def get_client():
    return FinMindClient(cache_dir=".cache")


def _render_navbar_minimal(current_page_key: str):
    """精簡導航列：僅分頁標籤（用於非股票頁面）"""
    # Get localized labels for this language
    page_labels = _get_localized_page_labels()
    # Get current label from the page key
    current_label = t(f"page.{current_page_key}")
    # Find index of current label in the list (should always be found)
    try:
        current_idx = page_labels.index(current_label)
    except ValueError:
        # Fallback to first page if label not found (should not happen)
        current_idx = 0

    selected_label = st.radio(
        t("sidebar.nav_label"),
        page_labels,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio_minimal",
    )

    # Map selected label back to page key
    label_to_key = _get_label_to_key_map()
    selected_key = label_to_key.get(selected_label)
    if selected_key is None:
        # Should not happen
        selected_key = "business_card"

    if selected_key != current_page_key:
        navigate_to(page=selected_key)

    st.markdown("--")


def load_and_render_page(client: FinMindClient, stock_id: str):
    """根據 session_state['page'] 渲染對應頁面"""
    page_key = st.session_state.get("page_key", "business_card")

    # TD-01 Phase 1+2: Try plugin registry first for standalone pages
    if page_key in _STANDALONE_PLUGIN_KEYS:
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            rendered = _render_via_plugin(page_key, client)
        if not rendered:
            # Fallback: plugin not found in registry
            logger.warning(
                "Plugin '%s' not found in registry.",
                page_key,
            )
        return

    # 頁面需要特定股票資料
    with st.spinner(t("status.loading_stock")):
        data = get_stock_data(client, stock_id)
    if data is None:
        st.error(t("error.not_found", sid=stock_id))
        return

    # M5: 自動事件偵測（背景執行，不阻塞頁面）
    try:
        from src.services.settings_service import get_threshold
        _ss = st.session_state
        _price_thresh = get_threshold(_ss, "settings_price_threshold")
        _revenue_thresh = get_threshold(_ss, "settings_revenue_threshold")
        with st.spinner(t("status.checking_events")):
            new_events = run_auto_detection(
                stock_id, data,
                price_threshold=_price_thresh,
                revenue_threshold=_revenue_thresh,
            )

        # M5: 自適應框架橫幅
        _render_adaptive_banner(data)

        # M5: 事件提醒
        _render_event_alerts(stock_id)
    except Exception as exc:
        logger.warning("M5 event detection/rendering failed for %s: %s", stock_id, exc)

    # TD-01 Phase 2: Try plugin registry for stock-dependent pages
    if page_key in _STOCK_PLUGIN_KEYS:
        _render_navbar(data, page_key)
        with st.spinner(t("status.loading_page")):
            rendered = _render_via_plugin(page_key, client, stock_id, data)
        if not rendered:
            logger.warning(
                "Stock plugin '%s' not found in registry.", page_key,
            )
        return

    # ETF 導向 ETF 詳細頁
    if _is_etf_check(stock_id, data["stock_name"], data["industry"]):
        _render_navbar(data, page_key)
        with st.spinner(t("status.loading_page")):
            _render_etf_detail(data, client)
        return

    # Fallback: unknown page key — render business_card via plugin
    logger.warning("Unknown page_key '%s', falling back to business_card.", page_key)
    _render_navbar(data, "business_card")
    with st.spinner(t("status.loading_page")):
        _render_via_plugin("business_card", client, stock_id, data)


def _render_navbar(data: dict, current_page_key: str):
    """頂部導航列：公司名稱 + 價格 + 分頁標籤"""
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

    st.markdown("--")
