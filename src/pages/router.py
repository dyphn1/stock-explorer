"""
股識 Stock Explorer — M5 自適應更新
頁面路由器：根據 session_state['page'] 顯示不同頁面
"""

import logging
import streamlit as st

from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import (
    get_stock_data,
)
from src.pages.business_card import _render_business_card
from src.pages.revenue_tree import _render_revenue_tree
from src.pages.compare_stories import _render_compare_stories_page
from src.pages.moat_comparison import _render_moat_comparison_page
from src.pages.operation_checkup import _render_operation_checkup
from src.pages.financial_health import _render_financial_health
from src.pages.peer_comparison import _render_peer_comparison
from src.pages.group_structure import _render_group_structure
from src.pages.category_browser import _render_category_browser
from src.pages.etf_browser import _render_etf_browser
from src.pages.etf_detail import _render_etf_detail
from src.pages.watchlist_page import _render_watchlist_page
from src.pages.event_dashboard import (
    _render_event_dashboard,
    _render_freshness_indicator,
    _render_adaptive_banner,
    _render_event_alerts,
)
from src.pages.sector_heatmap import _render_sector_heatmap
from src.pages.settings import render_settings_page
from src.pages.investment_memo import _render_investment_memo
from src.pages.financial_wellness import _render_financial_wellness
from src.pages.comprehension_check import _render_comprehension_check
from src.pages.market_event_case_study import _render_market_event_case_study
from src.pages.stock_screener import _render_stock_screener
from src.pages.notification_center import _render_notification_center
from src.pages.first_visit_guide import _render_first_visit_guide
from src.pages.learn_first_gate import _render_learn_first_gate
from src.pages.company_timeline import render_company_timeline
from src.pages.story_timeline import render_story_timeline_page
from src.pages.debate_cards import render_debate_cards_page
from src.services.adaptive_engine import (
    run_auto_detection,
    check_data_freshness,
)
from src.core.i18n import t, set_lang, get_available_locales
from src.services.watchlist import _is_etf_check as _is_etf_check
from src.pages.investor_story_feed import render_investor_story_feed
from src.pages.academy import _render_academy
from src.pages.case_study_library import _render_case_study_library

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

    # 不需要特定股票的頁面，獨立渲染
    if page_key == "category_browser":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_category_browser(client)
        return
    if page_key == "etf_section":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_etf_browser(client)
        return
    if page_key == "watchlist":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_watchlist_page(client)
        return
    if page_key == "event_dashboard":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_event_dashboard(client)
        return
    if page_key == "notification_center":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_notification_center(client)
        return
    if page_key == "settings":
        _render_navbar_minimal(page_key)
        render_settings_page()
        return
    if page_key == "sector_heatmap":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_sector_heatmap(client)
        return
    if page_key == "investment_memo":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_investment_memo(client)
        return
    if page_key == "case_study":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_market_event_case_study(client)
        return
    if page_key == "financial_wellness":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_financial_wellness(client)
        return
    if page_key == "comprehension_check":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_comprehension_check(client)
        return
    if page_key == "academy":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_academy(client)
        return
    if page_key == "case_study_library":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_case_study_library(client)
        return
    if page_key == "stock_screener":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_stock_screener(client)
        return
    if page_key == "learn_first_gate":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_learn_first_gate(client)
        return
    if page_key == "first_visit_guide":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            _render_first_visit_guide(client)
        return
    if page_key == "daily_story":
        _render_navbar_minimal(page_key)
        with st.spinner(t("status.loading_page")):
            render_investor_story_feed({}, client)
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

        # M5: 資料新鮮度指標
        freshness = check_data_freshness(stock_id, data)
        _render_freshness_indicator(freshness)
    except Exception as exc:
        logger.warning("M5 event detection/rendering failed for %s: %s", stock_id, exc)

    # ETF 導向 ETF 詳細頁
    if _is_etf_check(stock_id, data["stock_name"], data["industry"]):
        _render_navbar(data, page_key)
        with st.spinner(t("status.loading_page")):
            _render_etf_detail(data, client)
        return

    # 渲染導航列
    _render_navbar(data, page_key)

    # 分頁渲染
    if page_key == "business_card":
        with st.spinner(t("status.loading_page")):
            _render_business_card(data, client)
    elif page_key == "operation_checkup":
        with st.spinner(t("status.loading_page")):
            _render_operation_checkup(data)
    elif page_key == "financial_health":
        with st.spinner(t("status.loading_page")):
            _render_financial_health(data)
    elif page_key == "peer_comparison":
        with st.spinner(t("status.loading_page")):
            _render_peer_comparison(data, client)
    elif page_key == "group_structure":
        with st.spinner(t("status.loading_page")):
            _render_group_structure(data)
    elif page_key == "story_timeline":
        with st.spinner(t("status.loading_page")):
            render_company_timeline(data, client)
    elif page_key == "full_story_timeline":
        with st.spinner(t("status.loading_page")):
            render_story_timeline_page(data, client)
    elif page_key == "revenue_tree":
        with st.spinner(t("status.loading_page")):
            _render_revenue_tree(data, client)
    elif page_key == "compare_stories":
        with st.spinner(t("status.loading_page")):
            _render_compare_stories_page(data, client)
    elif page_key == "moat_comparison":
        with st.spinner(t("status.loading_page")):
            _render_moat_comparison_page(data, client)
    elif page_key == "debate_cards":
        with st.spinner(t("status.loading_page")):
            render_debate_cards_page(data, client)


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
        "頁面導航",
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