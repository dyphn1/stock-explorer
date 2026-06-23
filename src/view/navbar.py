import streamlit as st
from src.core.i18n import t
from src.pages.url_sync import navigate_to


PAGE_KEYS = [
    "business_card", "operation_checkup", "financial_health", "peer_comparison",
    "group_structure", "category_browser", "etf_section", "watchlist",
    "event_dashboard", "notification_center", "investment_memo",
    "financial_wellness", "stock_screener", "settings", "sector_heatmap",
    "daily_market", "case_study", "comprehension_check", "academy",
    "case_study_library", "first_visit_guide", "story_timeline",
    "full_story_timeline", "daily_story", "revenue_tree",
    "compare_stories", "moat_comparison", "debate_cards",
]


def _get_localized_page_labels():
    return [t(f"page.{key}") for key in PAGE_KEYS]


def _get_label_to_key_map():
    labels = _get_localized_page_labels()
    return {label: key for key, label in zip(PAGE_KEYS, labels)}


def render_navbar_minimal(current_page_key: str):
    page_labels = _get_localized_page_labels()
    current_label = t(f"page.{current_page_key}")
    try:
        current_idx = page_labels.index(current_label)
    except ValueError:
        current_idx = 0

    selected_label = st.radio(
        t("sidebar.nav_label"),
        page_labels,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio_minimal",
    )

    label_to_key = _get_label_to_key_map()
    selected_key = label_to_key.get(selected_label)
    if selected_key is None:
        selected_key = "business_card"

    if selected_key != current_page_key:
        navigate_to(page=selected_key)

    st.markdown("--")


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

    page_labels = _get_localized_page_labels()
    current_label = t(f"page.{current_page_key}")
    try:
        current_idx = page_labels.index(current_label)
    except ValueError:
        current_idx = 0

    selected_label = st.radio(
        t("router.page_navigation"),
        page_labels,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="navbar_radio",
    )

    label_to_key = _get_label_to_key_map()
    selected_key = label_to_key.get(selected_label)
    if selected_key is None:
        selected_key = "business_card"

    if selected_key != current_page_key:
        navigate_to(page=selected_key)

    st.markdown("--")
