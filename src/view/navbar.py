import streamlit as st
from src.core.i18n import t


def render_navbar_minimal(current_page_key: str):
    st.markdown(f"### {t(f'page.{current_page_key}')}")


def render_navbar(data: dict, current_page_key: str):
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
