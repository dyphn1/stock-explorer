from collections.abc import Callable

import streamlit as st
from src.core.i18n import t
from src.data.finmind_client import get_rate_limit_status


def render_activity_bar(
    items: list[tuple[str, str, str]],
    current_key: str,
    hot_stocks: list[tuple[str, str]],
    hot_etfs: list[tuple[str, str]],
    on_navigate: Callable[[str], None],
    on_hot_stock_click: Callable[[str, str], None] | None = None,
):
    st.markdown(f"### 📊 {t('app.title')}")
    st.markdown("---")

    for key, icon, label in items:
        is_active = (key == current_key)
        btn_label = f"{icon} {t(f'page.{key}') if key != 'business_card' else label}"
        if is_active:
            btn_label = f"▸ {btn_label}"
        if st.button(btn_label, key=f"nav_{key}", use_container_width=True, type="secondary" if not is_active else "primary"):
            on_navigate(key)

    st.markdown("---")

    status = get_rate_limit_status()
    if status["is_limited"]:
        st.warning(t("main.sidebar.api_warning"))

    click_handler = on_hot_stock_click or on_navigate

    with st.expander(f"🔥 {t('main.sidebar.hot_stocks')}", expanded=False):
        for sid, name in hot_stocks:
            if st.button(f"{sid} {name}", key=f"hot_{sid}", use_container_width=True):
                click_handler("business_card", sid)

    with st.expander(f"🏷️ {t('main.sidebar.hot_etfs')}", expanded=False):
        for sid, name in hot_etfs:
            if st.button(f"{sid} {name}", key=f"hot_etf_{sid}", use_container_width=True):
                click_handler("business_card", sid)

    st.markdown("---")
    st.markdown(t("main.disclaimer"), unsafe_allow_html=True)
