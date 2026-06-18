"""
Learn First Gate — C163
4-lesson interactive onboarding for first-time users.
Replaces the old first_visit_guide.py (C103).
"""
from __future__ import annotations
import streamlit as st
from src.core.i18n import t
from src.pages._router_base import (
    _lesson_card, _progress_dots, _section_title,
    _beginner_banner, _advanced_content_expander,
)
from src.services.experience_service import get_gateway_lessons, is_beginner_mode


def _render_learn_first_gate(client):
    """Learn First Gate — 4-lesson interactive onboarding."""
    # If already completed, redirect to business card
    if st.session_state.get("gateway_completed", False):
        return

    lessons = get_gateway_lessons()
    if not lessons:
        # No lessons loaded — show coming soon and allow skip
        _section_title(t("learn_first_gate.title"))
        _beginner_banner(t("learn_first_gate.coming_soon"))
        _render_skip_button()
        return

    # Initialize lesson index
    if "gateway_lesson_idx" not in st.session_state:
        st.session_state["gateway_lesson_idx"] = 0

    idx = st.session_state["gateway_lesson_idx"]
    total = len(lessons)

    _section_title(t("learn_first_gate.title"))
    _beginner_banner(t("learn_first_gate.intro"))
    _progress_dots(idx, total)

    # Current lesson
    lesson = lessons[idx]
    _lesson_card(
        title=lesson.get("title", ""),
        content=lesson.get("content", ""),
        icon=lesson.get("icon", "📖"),
        visual_area=lesson.get("visual_area"),
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if idx > 0:
            if st.button(t("learn_first_gate.btn_prev_lesson"), key="gateway_prev", use_container_width=True):
                st.session_state["gateway_lesson_idx"] = idx - 1
                st.rerun()
    with col2:
        if st.button(t("learn_first_gate.btn_skip"), key="gateway_skip", use_container_width=True):
            st.session_state["gateway_completed"] = True
            st.session_state["first_visit_dismissed"] = True
            st.rerun()
    with col3:
        if idx < total - 1:
            if st.button(t("learn_first_gate.btn_next_lesson"), key="gateway_next", use_container_width=True):
                st.session_state["gateway_lesson_idx"] = idx + 1
                st.rerun()
        else:
            if st.button(t("learn_first_gate.btn_start_using"), key="gateway_complete", use_container_width=True):
                st.session_state["gateway_completed"] = True
                st.session_state["first_visit_dismissed"] = True
                st.rerun()

    st.markdown("---")


def _render_skip_button():
    """Skip button for coming-soon state."""
    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button(t("learn_first_gate.btn_explore_instead"), key="gateway_skip_soon", use_container_width=True):
            st.session_state["gateway_completed"] = True
            st.session_state["first_visit_dismissed"] = True
            st.rerun()
