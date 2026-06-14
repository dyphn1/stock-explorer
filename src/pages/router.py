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
from src.services.adaptive_engine import (
    run_auto_detection,
    check_data_freshness,
)
from src.services.watchlist import _is_etf as _is_etf_check
from src.pages.investor_story_feed import render_investor_story_feed
from src.pages.academy import _render_academy
from src.pages.case_study_library import _render_case_study_library

logger = logging.getLogger(__name__)


# ── 初始化 ────────────────────────────────────────────

@st.cache_resource
def get_client():
    return FinMindClient(cache_dir=".cache")


def _render_navbar_minimal(current_page: str):
    """精簡導航列：僅分頁標籤（用於非股票頁面）"""
    pages = ["名片", "營運健檢", "財務體質", "同業比較", "集團架構", "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板", "通知中心", "設定", "產業熱力圖", "投資備忘錄", "案例研究", "理財健康檢查", "理解力測驗", "學習學院", "歷史案例庫", "股票探索", "新手導覽", "故事時間軸", "完整故事時間軸", "每日故事", "營收結構樹", "同業比較故事", "護城河比較", "學習入門"]
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
    if page == "通知中心":
        _render_navbar_minimal(page)
        with st.spinner("載入通知中心..."):
            _render_notification_center(client)
        return
    if page == "設定":
        _render_navbar_minimal(page)
        render_settings_page()
        return
    if page == "產業熱力圖":
        _render_navbar_minimal(page)
        with st.spinner("載入產業熱力圖..."):
            _render_sector_heatmap(client)
        return
    if page == "投資備忘錄":
        _render_navbar_minimal(page)
        with st.spinner("載入投資備忘錄..."):
            _render_investment_memo(client)
        return
    if page == "案例研究":
        _render_navbar_minimal(page)
        with st.spinner("載入案例研究..."):
            _render_market_event_case_study(client)
        return
    if page == "理財健康檢查":
        _render_navbar_minimal(page)
        with st.spinner("載入理財健康檢查..."):
            _render_financial_wellness(client)
        return
    if page == "理解力測驗":
        _render_navbar_minimal(page)
        with st.spinner("載入理解力測驗..."):
            _render_comprehension_check(client)
        return
    if page == "學習學院":
        _render_navbar_minimal(page)
        with st.spinner("載入學習學院..."):
            _render_academy(client)
        return
    if page == "歷史案例庫":
        _render_navbar_minimal(page)
        with st.spinner("載入歷史案例庫..."):
            _render_case_study_library(client)
        return
    if page == "股票探索":
        _render_navbar_minimal(page)
        with st.spinner("載入股票探索引擎..."):
            _render_stock_screener(client)
        return
    if page == "學習入門":
        _render_navbar_minimal(page)
        with st.spinner("載入學習入門..."):
            _render_learn_first_gate(client)
        return
    if page == "新手導覽":
        _render_navbar_minimal(page)
        with st.spinner("載入新手導覽..."):
            _render_first_visit_guide(client)
        return
    if page == "每日故事":
        _render_navbar_minimal(page)
        with st.spinner("載入每日故事..."):
            render_investor_story_feed({}, client)
        return

    with st.spinner("載入股票資料..."):
        data = get_stock_data(client, stock_id)
    if data is None:
        st.error(f"找不到股票代號 {stock_id}")
        return

    # M5: 自動事件偵測（背景執行，不阻塞頁面）
    try:
        from src.services.settings_service import get_threshold
        _ss = st.session_state
        _price_thresh = get_threshold(_ss, "settings_price_threshold")
        _revenue_thresh = get_threshold(_ss, "settings_revenue_threshold")
        with st.spinner("🔍 檢查近期事件..."):
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
    elif page == "故事時間軸":
        with st.spinner("載入故事時間軸..."):
            render_company_timeline(data, client)
    elif page == "完整故事時間軸":
        with st.spinner("載入完整故事時間軸..."):
            render_story_timeline_page(data, client)
    elif page == "營收結構樹":
        with st.spinner("載入營收結構..."):
            _render_revenue_tree(data, client)
    elif page == "同業比較故事":
        with st.spinner("載入同業比較..."):
            _render_compare_stories_page(data, client)
    elif page == "護城河比較":
        with st.spinner("載入護城河比較..."):
            _render_moat_comparison_page(data, client)


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
    pages = ["名片", "營運健檢", "財務體質", "同業比較", "集團架構", "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板", "通知中心", "設定", "產業熱力圖", "投資備忘錄", "案例研究", "理財健康檢查", "理解力測驗", "學習學院", "歷史案例庫", "股票探索", "新手導覽", "故事時間軸", "完整故事時間軸", "每日故事", "營收結構樹", "同業比較故事", "護城河比較", "學習入門"]
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
