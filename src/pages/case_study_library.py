"""股識 Stock Explorer — C140 歷史案例研究圖書館
可瀏覽的歷史案例研究圖書館，以史學家視角回顧台灣市場重大事件。
"""
from __future__ import annotations

import streamlit as st
from src.core.i18n import t
from src.data.finmind_client import FinMindClient
from src.pages._router_base import _info_card, _section_title, _count_label
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.case_study_library import (
    get_all_case_studies,
    get_case_study_by_id,
    get_all_industries,
    get_all_topic_tags,
    filter_case_studies,
)


def _render_case_study_card(cs: dict) -> None:
    """Render a single case study as a compact card in the grid."""
    with st.container():
        st.markdown(f"**{cs['title']}**")
        st.caption(f"📅 {cs['date']} ｜ 🏭 {cs['industry']}")
        st.markdown(f"_{cs['summary'][:100]}..._")

        # Topic tags as captions
        tags = cs.get("topic_tags", [])
        if tags:
            st.caption(" · ".join(f"`{t}`" for t in tags))

        if st.button(
            t("library.read_full_case"),
            key=f"read_{cs['id']}",
            use_container_width=True,
        ):
            st.session_state["case_study_library_selected"] = cs["id"]
            st.rerun()

        st.markdown("---")


def _render_case_study_detail(cs: dict) -> None:
    """Render the full detail view of a case study."""
    # Back button
    if st.button(t("library.back_to_library"), key="back_to_library"):
        st.session_state["case_study_library_selected"] = None
        st.rerun()

    st.markdown(f"# {cs['title']}")
    st.markdown(f"**📅 {cs['date']}** ｜ 🏭 **{cs['industry']}**")

    # Topic tags
    tags = cs.get("topic_tags", [])
    if tags:
        st.caption("　".join(f"`{t}`" for t in tags))

    st.markdown("---")

    # Summary
    _section_title(t("library.event_summary"))
    st.markdown(cs["summary"])

    # Key lesson
    st.markdown("---")
    _section_title(t("library.historical_lesson"))
    st.markdown(cs["key_lesson"])

    # Related stocks
    related = cs.get("related_stocks", [])
    if related:
        st.markdown("---")
        _section_title(t("library.related_stocks"))
        cols = st.columns(min(len(related), 3))
        for i, stock in enumerate(related):
            with cols[i % 3]:
                st.markdown(f"**{stock['stock_name']}** `{stock['stock_id']}`")

    st.markdown("---")
    _historian_disclaimer("general")


def _render_case_study_library(client: FinMindClient) -> None:
    """Historical Case Study Library main page."""
    st.markdown(f"## 📚 {t('library.title')}")
    st.markdown(t("library.subtitle"))
    st.markdown("---")

    # Historian positioning
    _info_card(
        t("library.disclaimer_title"),
        t("library.disclaimer_body")
        t("library.disclaimer_footer"),
        icon="📖",
    )

    # Check if a specific case study is selected
    selected_id = st.session_state.get("case_study_library_selected")

    if selected_id:
        cs = get_case_study_by_id(selected_id)
        if cs:
            _render_case_study_detail(cs)
        else:
            st.error(t("library.not_found"))
            st.session_state["case_study_library_selected"] = None
        return

    # ── Filters ───────────────────────────────────────────────
    st.markdown(f"### 🔍 {t('library.filter_title')}")

    industries = [t("library.all")] + get_all_industries()
    tags = [t("library.all")] + get_all_topic_tags()

    col1, col2 = st.columns(2)
    with col1:
        selected_industry = st.selectbox(
            t("library.filter_by_industry"),
            industries,
            key="cslib_filter_industry",
        )
    with col2:
        selected_tag = st.selectbox(
            t("library.filter_by_tag"),
            tags,
            key="cslib_filter_tag",
        )

    # Apply filters
    filtered = filter_case_studies(
        industry=selected_industry if selected_industry != t("library.all") else None,
        topic_tag=selected_tag if selected_tag != t("library.all") else None,
    )

    st.markdown("---")

    # ── Results ───────────────────────────────────────────────
    _count_label(len(filtered), t("library.case_count"))

    if not filtered:
        st.info(t("library.no_results"))
        return

    # Display as cards in a grid (2 columns)
    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= len(filtered):
                break
            with cols[j]:
                _render_case_study_card(filtered[idx])
