"""
First Visit Guide — C103 Lite
2-card dismissible primer shown on first visit to Stock Explorer.
"""

from __future__ import annotations

import streamlit as st
from src.pages._router_base import _summary_card, _白话_card


def _render_first_visit_guide(client):
    """First Visit Guide — 2-card dismissible primer for new users."""
    # Already dismissed — show nothing
    if st.session_state.get("first_visit_dismissed", False):
        return

    st.markdown("## 👋 歡迎使用股識")
    st.markdown("花兩分鐘認識這個工具，讓你更快上手。")
    st.markdown("---\n")

    # ── Card 1: 你將學到什麼 ────────────────────────────────
    _summary_card(
        "你將學到什麼",
        "在這裡，你會認識公司，而不是追逐股價。從一個故事開始，了解這家公司是做什麼的、怎麼賺錢、最近有什麼變化。",
        icon="📖",
    )

    st.markdown("\n")

    # ── Card 2: 關於股識 ────────────────────────────────────
    _白话_card(
        "關於股識",
        "股識不是投資建議工具。我們不告訴你該買什麼或賣什麼。我們只告訴你這家公司發生了什麼事。",
        analogy="我們是「公司紀錄者」，不是「股票推薦者」。",
    )

    st.markdown("\n")

    # ── Dismiss button ──────────────────────────────────────
    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if st.button("我知道了 ✓", key="dismiss_first_visit", use_container_width=True):
            st.session_state["first_visit_dismissed"] = True
            st.rerun()

    st.markdown("---")
