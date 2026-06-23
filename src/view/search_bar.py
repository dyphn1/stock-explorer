import streamlit as st
from src.core.i18n import t
from src.data.finmind_client import get_rate_limit_status


def render_search_bar() -> str:
    col1, col2 = st.columns([4, 1])
    with col1:
        search_val = st.text_input(
            t("main.sidebar.search_label"),
            placeholder=t("main.sidebar.search_placeholder"),
            label_visibility="collapsed",
            key="global_search",
        )
    with col2:
        render_rate_limit_indicator()
    return search_val


def render_rate_limit_indicator():
    status = get_rate_limit_status()
    if status["is_limited"]:
        st.warning(f"⚠️ {t('rate_limited')}")
