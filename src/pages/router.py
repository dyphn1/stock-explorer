"""
股識 Stock Explorer — M2 四大深度區塊
頁面路由器：根據 session_state['page'] 顯示不同頁面
"""

import streamlit as st
import pandas as pd

from src.data.finmind_client import FinMindClient
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


# ── 初始化 ────────────────────────────────────────────

@st.cache_resource
def get_client():
    return FinMindClient(cache_dir=".cache")


def load_and_render_page(client: FinMindClient, stock_id: str):
    """根據 session_state['page'] 渲染對應頁面"""
    page = st.session_state.get("page", "名片")

    data = get_stock_data(client, stock_id)
    if data is None:
        st.error(f"找不到股票代號 {stock_id}")
        return

    # 渲染導航列
    _render_navbar(data, page)

    # 分頁渲染
    if page == "名片":
        _render_business_card(data, client)
    elif page == "營運健檢":
        _render_operation_checkup(data)
    elif page == "財務體質":
        _render_financial_health(data)
    elif page == "同業比較":
        _render_peer_comparison(data, client)
    elif page == "集團架構":
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
    pages = ["名片", "營運健檢", "財務體質", "同業比較", "集團架構"]
    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        with cols[i]:
            if p == current_page:
                st.markdown(f"**▎{p}**")
            else:
                if st.button(p, key=f"nav_{p}", use_container_width=True):
                    st.session_state["page"] = p
                    st.rerun()

    st.markdown("---")
