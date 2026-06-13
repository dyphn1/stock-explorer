"""
URL ↔ session_state synchronization for browser back/forward support.
Uses st.query_params (Streamlit >=1.30) to keep URL in sync with page state.
"""

import streamlit as st

# Canonical list of valid page names
VALID_PAGES = frozenset({
    "名片", "營運健檢", "財務體質", "同業比較", "集團架構",
    "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板", "通知中心", "產業熱力圖",
    "投資備忘錄", "案例研究", "理財健康檢查", "股票探索", "每日故事",
    "營收結構樹", "同業比較故事", "護城河比較", "學習學院",
})

DEFAULT_PAGE = "名片"


def sync_url_to_session() -> None:
    """
    Phase 1: Read URL query params and sync to session_state.
    Called once at the top of main.py, BEFORE any rendering.

    Priority:
      1. URL params (source of truth) — handles back/forward, direct URL, bookmarks
      2. Existing session_state — handles in-app navigation that hasn't hit URL yet
      3. Defaults — first visit with no URL params and no session_state

    Also handles validation: invalid page/stock_id in URL falls back gracefully.
    """
    # --- Page sync ---
    url_page = st.query_params.get("page")
    if url_page is not None:
        if url_page in VALID_PAGES:
            st.session_state["page"] = url_page
        else:
            # Invalid page in URL → fall back to default, fix URL
            st.session_state["page"] = DEFAULT_PAGE
            st.query_params["page"] = DEFAULT_PAGE
    # If no URL param, session_state keeps its current value (if any)
    elif "page" not in st.session_state:
        st.session_state["page"] = DEFAULT_PAGE

    # --- Stock ID sync ---
    url_stock_id = st.query_params.get("stock_id")
    if url_stock_id is not None:
        # Basic validation: non-empty string
        if url_stock_id.strip():
            st.session_state["stock_id"] = url_stock_id.strip()
        else:
            # Empty stock_id in URL → remove it
            del st.query_params["stock_id"]
    # If no URL param and no session_state, that's fine (shows welcome page)

    # --- Reverse sync: make sure URL reflects current state ---
    # This handles the case where session_state was set by in-app navigation
    # but URL hasn't been updated yet (e.g., on the NEXT rerun after a button click)
    _sync_session_to_url()


def _sync_session_to_url() -> None:
    """
    Phase 2: Write current session_state to URL query params.
    Called internally by sync_url_to_session, and also by navigate_to().
    """
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
    Use this INSTEAD of manual session_state assignment + st.rerun().

    Examples:
        # Switch to 財務體質 tab (same stock)
        navigate_to(page="財務體質")

        # View a different stock's 名片 page
        navigate_to(page="名片", stock_id="2317")

        # View a stock, keeping current page
        navigate_to(stock_id="2454")
    """
    if page is not None:
        if page not in VALID_PAGES:
            raise ValueError(f"Invalid page: {page!r}. Must be one of {sorted(VALID_PAGES)}")
        st.session_state["page"] = page

    if stock_id is not None:
        st.session_state["stock_id"] = stock_id

    # Sync to URL before rerun
    _sync_session_to_url()
    st.rerun()
