"""
股識 Stock Explorer — M5 自適應更新
頁面路由器：根據 session_state['page'] 顯示不同頁面
"""

import streamlit as st
import pandas as pd

from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import (
    get_stock_data,
    _calc_extra_metrics,
    _find_financial_value,
    _section_title,
    _白话_card,
    _info_card,
)
from src.pages.business_card import _render_business_card
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
from src.services.adaptive_engine import (
    detect_company_type,
    run_auto_detection,
    check_data_freshness,
)


# ── 初始化 ────────────────────────────────────────────

@st.cache_resource
def get_client():
    return FinMindClient(cache_dir=".cache")


def _is_etf(client: FinMindClient, stock_id: str) -> bool:
    """判斷一檔股票是否為 ETF"""
    try:
        info = client.get_stock_info(stock_id)
        if len(info) > 0:
            industry = str(info.iloc[0].get("industry_category", ""))
            return "etf" in industry.lower()
    except Exception:
        pass
    return False


def _render_navbar_minimal(current_page: str):
    """精簡導航列：僅分頁標籤（用於非股票頁面）"""
    pages = ["名片", "營運健檢", "財務體質", "同業比較", "集團架構", "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板"]
    current_idx = pages.index(current_page) if current_page in pages else 0

    selected = st.radio(
        "頁面導航",
        pages,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio_minimal",
    )

    if selected != current_page:
        navigate_to(page=selected)

    st.markdown("---")


def load_and_render_page(client: FinMindClient, stock_id: str):
    """根據 session_state['page'] 渲染對應頁面"""
    page = st.session_state.get("page", "名片")

    # 不需要特定股票的頁面，獨立渲染
    if page == "分類瀏覽":
        _render_navbar_minimal(page)
        with st.spinner("載入分類瀏覽..."):
            _render_category_browser(client)
        return
    if page == "ETF 專區":
        _render_navbar_minimal(page)
        with st.spinner("載入 ETF 專區..."):
            _render_etf_browser(client)
        return
    if page == "我的關注":
        _render_navbar_minimal(page)
        with st.spinner("載入我的關注..."):
            _render_watchlist_page(client)
        return
    if page == "事件儀表板":
        _render_navbar_minimal(page)
        with st.spinner("載入事件儀表板..."):
            _render_event_dashboard(client)
        return

    with st.spinner("載入股票資料..."):
        data = get_stock_data(client, stock_id)
    if data is None:
        st.error(f"找不到股票代號 {stock_id}")
        return

    # M5: 自動事件偵測（背景執行，不阻塞頁面）
    with st.spinner("🔍 檢查近期事件..."):
        new_events = run_auto_detection(stock_id, data)

    # M5: 自適應框架橫幅
    _render_adaptive_banner(data)

    # M5: 事件提醒
    _render_event_alerts(stock_id)

    # M5: 資料新鮮度指標
    freshness = check_data_freshness(stock_id, data)
    _render_freshness_indicator(freshness)

    # ETF 導向 ETF 詳細頁
    if _is_etf(client, stock_id):
        _render_navbar(data, page)
        with st.spinner("載入 ETF 詳細頁..."):
            _render_etf_detail(data, client)
        return

    # 渲染導航列
    _render_navbar(data, page)

    # 分頁渲染
    if page == "名片":
        with st.spinner("載入名片頁..."):
            _render_business_card(data, client)
    elif page == "營運健檢":
        with st.spinner("載入營運健檢..."):
            _render_operation_checkup(data)
    elif page == "財務體質":
        with st.spinner("載入財務體質..."):
            _render_financial_health(data)
    elif page == "同業比較":
        with st.spinner("載入同業比較..."):
            _render_peer_comparison(data, client)
    elif page == "集團架構":
        with st.spinner("載入集團架構..."):
            _render_group_structure(data)


def _render_navbar(data: dict, current_page: str):
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
    pages = ["名片", "營運健檢", "財務體質", "同業比較", "集團架構", "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板"]
    current_idx = pages.index(current_page) if current_page in pages else 0

    selected = st.radio(
        "頁面導航",
        pages,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio",
    )

    if selected != current_page:
        navigate_to(page=selected)

    st.markdown("---")
