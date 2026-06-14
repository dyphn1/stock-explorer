"""股識 Stock Explorer — C140 歷史案例研究圖書館
可瀏覽的歷史案例研究圖書館，以史學家視角回顧台灣市場重大事件。
"""
from __future__ import annotations

import streamlit as st
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
            "閱讀完整案例",
            key=f"read_{cs['id']}",
            use_container_width=True,
        ):
            st.session_state["case_study_library_selected"] = cs["id"]
            st.rerun()

        st.markdown("---")


def _render_case_study_detail(cs: dict) -> None:
    """Render the full detail view of a case study."""
    # Back button
    if st.button("← 返回圖書館", key="back_to_library"):
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
    _section_title("📋 事件摘要")
    st.markdown(cs["summary"])

    # Key lesson
    st.markdown("---")
    _section_title("🎓 歷史啟示")
    st.markdown(cs["key_lesson"])

    # Related stocks
    related = cs.get("related_stocks", [])
    if related:
        st.markdown("---")
        _section_title("📈 相關個股")
        cols = st.columns(min(len(related), 3))
        for i, stock in enumerate(related):
            with cols[i % 3]:
                st.markdown(f"**{stock['stock_name']}** `{stock['stock_id']}`")

    st.markdown("---")
    _historian_disclaimer("general")


def _render_case_study_library(client: FinMindClient) -> None:
    """Historical Case Study Library main page."""
    st.markdown("## 📚 歷史案例研究圖書館")
    st.markdown("以史學家視角，回顧台灣金融市場的重大事件與產業變遷")
    st.markdown("---")

    # Historian positioning
    _info_card(
        "我們的定位：歷史學家，不是投資顧問",
        "這些案例研究是在解釋「發生了什麼事」和「為什麼」，不是在告訴你「該買什麼」。"
        "投資決策每個人都不同，過去的經驗不代表未來的結果。",
        icon="📖",
    )

    # Check if a specific case study is selected
    selected_id = st.session_state.get("case_study_library_selected")

    if selected_id:
        cs = get_case_study_by_id(selected_id)
        if cs:
            _render_case_study_detail(cs)
        else:
            st.error("找不到此案例研究。")
            st.session_state["case_study_library_selected"] = None
        return

    # ── Filters ───────────────────────────────────────────────
    st.markdown("### 🔍 篩選條件")

    industries = ["全部"] + get_all_industries()
    tags = ["全部"] + get_all_topic_tags()

    col1, col2 = st.columns(2)
    with col1:
        selected_industry = st.selectbox(
            "依產業篩選",
            industries,
            key="cslib_filter_industry",
        )
    with col2:
        selected_tag = st.selectbox(
            "依主題標籤篩選",
            tags,
            key="cslib_filter_tag",
        )

    # Apply filters
    filtered = filter_case_studies(
        industry=selected_industry if selected_industry != "全部" else None,
        topic_tag=selected_tag if selected_tag != "全部" else None,
    )

    st.markdown("---")

    # ── Results ───────────────────────────────────────────────
    _count_label(len(filtered), "篇案例研究")

    if not filtered:
        st.info("沒有符合篩選條件的案例研究。請調整篩選條件。")
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
