"""
URL ↔ session_state synchronization for browser back/forward support.
Uses st.query_params (Streamlit >=1.30) to keep URL in sync with page state.
"""

import streamlit as st

# Canonical list of valid page names (Chinese, for URL display)
VALID_PAGES = frozenset({
    "名片", "營運健檢", "財務體質", "同業比較", "集團架構",
    "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板", "通知中心", "設定", "產業熱力圖",
    "投資備忘錄", "案例研究", "理財健康檢查", "股票探索", "每日故事",
    "營收結構樹", "同業比較故事", "護城河比較", "學習學院", "今日市場動態",
})

# English page key ↔ Chinese name mapping
_PAGE_KEY_TO_NAME = {
    "business_card": "名片",
    "operation_checkup": "營運健檢",
    "financial_health": "財務體質",
    "peer_comparison": "同業比較",
    "group_structure": "集團架構",
    "category_browser": "分類瀏覽",
    "etf_section": "ETF 專區",
    "watchlist": "我的關注",
    "event_dashboard": "事件儀表板",
    "notification_center": "通知中心",
    "settings": "設定",
    "sector_heatmap": "產業熱力圖",
    "investment_memo": "投資備忘錄",
    "case_study": "案例研究",
    "financial_wellness": "理財健康檢查",
    "stock_screener": "股票探索",
    "daily_story": "每日故事",
    "daily_market": "今日市場動態",
    "revenue_tree": "營收結構樹",
    "compare_stories": "同業比較故事",
    "moat_comparison": "護城河比較",
    "academy": "學習學院",
    "story_timeline": "故事時間線",
    "full_story_timeline": "完整故事時間線",
    "debate_cards": "辯論卡",
    "comprehension_check": "理解測驗",
    "case_study_library": "案例庫",
    "first_visit_guide": "首次使用指南",
}
_PAGE_NAME_TO_KEY = {v: k for k, v in _PAGE_KEY_TO_NAME.items()}

DEFAULT_PAGE = "名片"


def _resolve_page(page: str) -> str:
    """Accept either Chinese page name or English page key; return Chinese name."""
    if page in VALID_PAGES:
        return page
    chinese = _PAGE_KEY_TO_NAME.get(page)
    if chinese:
        return chinese
    return DEFAULT_PAGE


def sync_url_to_session() -> None:
    url_page = st.query_params.get("page")
    if url_page is not None:
        resolved = _resolve_page(url_page)
        st.session_state["page"] = resolved
        if resolved != url_page:
            st.query_params["page"] = resolved
    elif "page" not in st.session_state:
        st.session_state["page"] = DEFAULT_PAGE

    # Also sync page_key
    page_name = st.session_state.get("page", DEFAULT_PAGE)
    st.session_state["page_key"] = _PAGE_NAME_TO_KEY.get(page_name, "business_card")

    url_stock_id = st.query_params.get("stock_id")
    if url_stock_id is not None:
        if url_stock_id.strip():
            st.session_state["stock_id"] = url_stock_id.strip()
        else:
            del st.query_params["stock_id"]

    _sync_session_to_url()


def _sync_session_to_url() -> None:
    page = st.session_state.get("page", DEFAULT_PAGE)
    st.query_params["page"] = page

    stock_id = st.session_state.get("stock_id")
    if stock_id:
        st.query_params["stock_id"] = stock_id
    elif "stock_id" in st.query_params:
        del st.query_params["stock_id"]


def navigate_to(page: str = None, stock_id: str = None) -> None:
    """
    Navigation helper: update session_state + URL + trigger rerun.

    Accepts both Chinese page names (e.g. "名片") and English page keys
    (e.g. "business_card").
    """
    if page is not None:
        resolved = _resolve_page(page)
        st.session_state["page"] = resolved
        st.session_state["page_key"] = _PAGE_NAME_TO_KEY.get(resolved, "business_card")

    if stock_id is not None:
        st.session_state["stock_id"] = stock_id

    _sync_session_to_url()
    st.rerun()
