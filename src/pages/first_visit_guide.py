"""
First Visit Guide — C103 Lite
2-card dismissible primer shown on first visit to Stock Explorer.
"""

from __future__ import annotations

import streamlit as st
from src.pages._router_base import _summary_card, _白话_card
from src.core.i18n import t


def _render_first_visit_guide(client):
    """First Visit Guide — 2-card dismissible primer for new users."""
    # Already dismissed — show nothing
    if st.session_state.get("first_visit_dismissed", False):
        return

    st.markdown(f"## 👋 {t('first_visit:welcome')}")
    st.markdown(t("first_visit:intro"))
    st.markdown("---\n")

    # ── Card 1: 你將學到什麼 ────────────────────────────────
    _summary_card(
        t("first_visit:what_you_learn"),
        t("first_visit:what_you_learn_content"),
        icon="📖",
    )

    st.markdown("\n")

    # ── Card 2: 關於股識 ────────────────────────────────────
    _白话_card(
        t("first_visit:about_title"),
        t("first_visit:about_content"),
        analogy=t("first_visit:about_analogy"),
    )

    st.markdown("\n")

    # ── Dismiss button ──────────────────────────────────────
    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if st.button(t("first_visit:dismiss_btn"), key="dismiss_first_visit", use_container_width=True):
            st.session_state["first_visit_dismissed"] = True
            st.rerun()

    st.markdown("---")
