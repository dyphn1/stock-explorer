"""
Market Event Case Study — C84
Interactive historical market event explorer with historian positioning.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.core.i18n import t
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card, _白话_card, _subsidiary_card, _section_title
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.market_event_service import (
    get_case_studies,
    get_case_study,
)


def _severity_badge(severity: str) -> str:
    badges = {
        "high": t("case_study.severity_high"),
        "medium": t("case_study.severity_medium"),
        "low": t("case_study.severity_low"),
    }
    return badges.get(severity, "⚪ 未知")


def _render_related_stock_card(stock_id: str, stock_name: str, impact: str):
    """Render a related stock card using shared _subsidiary_card component."""
    _subsidiary_card(
        name=stock_name,
        hold_label=f"📈 {stock_id}",
        hold_color="#3498DB",
        holding=0,
        revenue=0,
        business=impact,
        relation=t("case_study.stock_code", sid=stock_id),
    )


def _render_market_event_case_study(client: FinMindClient):
    """Market Event Case Study main page — historian perspective."""
    st.markdown(f"## 📚 {t('case_study.title')}")
    st.markdown(t("case_study.subtitle"))
    st.markdown("---\n")

    # ── Historian positioning disclaimer ─────────────────────
    _info_card(
        t("case_study.disclaimer_title"),
        t("case_study.disclaimer_body")
        t("case_study.disclaimer_footer"),
        icon="📖",
    )

    # ── Case study selector ──────────────────────────────────
    case_studies = get_case_studies()

    if not case_studies:
        new_events = get_case_studies()
        if new_events:
            case_studies = new_events

    st.markdown(f"### 🔍 {t('case_study.select_event')}")

    # Display as selection cards using a selectbox
    options = {f"{_severity_badge(cs['severity'])} {cs['title']}（{cs['date'][:4]}）": cs["id"] for cs in case_studies}
    selected_label = st.selectbox(
        t("case_study.choose_event"),
        list(options.keys()),
        key="case_study_selector",
        label_visibility="collapsed",
    )
    selected_id = options[selected_label] if selected_label else None

    if not selected_id:
        return

    study = get_case_study(selected_id)
    if not study:
        st.error(t("case_study.not_found"))
        return

    st.markdown("---\n")

    # ── Hero section ─────────────────────────────────────────
    severity_badge = _severity_badge(study["severity"])
    st.markdown(f"# {study['title']}")
    st.markdown(f"**{study['date']}** ｜ {severity_badge}")
    st.markdown(f"\n> {study['summary']}")

    st.markdown("---\n")

    # ── What Happened ────────────────────────────────────────
    _section_title(t("case_study.what_happened"))

    for i, paragraph in enumerate(study["what_happened"]):
        if i == 0:
            # First paragraph is the opening — make it prominent
            st.markdown(f"**{paragraph}**")
        else:
            st.markdown(paragraph)
        st.markdown("")

    # ── Key Metrics ──────────────────────────────────────────
    st.markdown("---\n")
    _section_title(t("case_study.key_data"))

    key_metrics = study.get("key_metrics", {})
    if key_metrics:
        cols_per_row = 2
        items = list(key_metrics.items())
        for i in range(0, len(items), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx >= len(items):
                    break
                label, data = items[idx]
                value = data.get("value", "N/A")
                analogy = data.get("analogy", "")
                with cols[j]:
                    _白话_card(label, value, analogy)

    # ── Lessons Learned ──────────────────────────────────────
    st.markdown("---\n")
    _section_title(t("case_study.lessons"))

    lessons = study.get("lessons", [])
    for lesson in lessons:
        with st.expander(f"💡 {lesson['title']}", expanded=False):
            st.markdown(lesson["content"])

    # ── Related Stocks ───────────────────────────────────────
    st.markdown("---\n")
    _section_title(t("case_study.related_stocks"))

    related_stocks = study.get("related_stocks", [])
    if related_stocks:
        cols_per_row = 3
        for i in range(0, len(related_stocks), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx >= len(related_stocks):
                    break
                stock = related_stocks[idx]
                with cols[j]:
                    _render_related_stock_card(
                        stock_id=stock["stock_id"],
                        stock_name=stock["stock_name"],
                        impact=stock["impact"],
                    )
                    if st.button(
                        t("case_study.view_card", name=stock["stock_name"]),
                        key=f"related_{study['id']}_{stock['stock_id']}",
                        use_container_width=True,
                    ):
                        navigate_to(page="名片", stock_id=stock["stock_id"])

    # ── All case studies overview ────────────────────────────
    st.markdown("---\n")
    _section_title(t("case_study.all_studies"))

    for cs in case_studies:
        badge = _severity_badge(cs["severity"])
        with st.expander(f"{badge} {cs['title']} — {cs['date'][:4]}"):
            st.markdown(cs["summary"])
            if st.button(
                t("case_study.deep_dive", title=cs["title"]),
                key=f"goto_{cs['id']}",
                use_container_width=True,
            ):
                st.session_state["case_study_selector"] = f"{badge} {cs['title']}（{cs['date'][:4]}）"
                st.rerun()

    # ── Historian disclaimer ─────────────────────────────────
    st.markdown("---\n")
    _historian_disclaimer("general")
