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
    on_go_home: Callable[[], None] | None = None,
):
    collapsed = st.session_state.get("sidebar_collapsed", False)

    # ── Home button (app logo) ──
    home_label = "📊" if collapsed else "📊 " + t('app.title')
    if st.button(home_label, key="sd_home", use_container_width=True):
        if on_go_home:
            on_go_home()

    st.markdown("---")

    # ── Nav items ──
    for key, icon, label in items:
        is_active = (key == current_key)
        prefix = ""
        if is_active and not collapsed:
            prefix = "▸ "
        nav_label = icon if collapsed else f"{prefix}{icon} {t(f'page.{key}')}"
        if st.button(
            nav_label,
            key=f"nav_{key}",
            use_container_width=True,
            help=t(f'page.{key}') if collapsed else None,
        ):
            on_navigate(key)

    st.markdown("---")

    status = get_rate_limit_status()
    if status["is_limited"]:
        st.warning(t("main.sidebar.api_warning"))

    click_handler = on_hot_stock_click or on_navigate

    if not collapsed:
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

    st.markdown("---")
    # ── Collapse toggle as standalone bottom button ──
    chevron = "◀" if collapsed else "▶"
    label = t('sidebar.collapse') if not collapsed else t('sidebar.expand')
    toggle_text = chevron if collapsed else f"{label} {chevron}"
    if st.button(toggle_text, key="sd_toggle", use_container_width=True):
        st.session_state["sidebar_collapsed"] = not collapsed
        st.rerun()
