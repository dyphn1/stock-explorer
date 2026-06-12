"""
Market Event Case Study — C84
Interactive historical market event explorer with historian positioning.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card, _白话_card, _subsidiary_card
from src.pages.business_card._helpers import _section_title, _historian_disclaimer
from src.services.market_event_service import (
    get_case_studies,
    get_case_study,
)


def _severity_badge(severity: str) -> str:
    badges = {
        "high": "🔴 重大事件",
        "medium": "🟡 重要事件",
        "low": "🟢 參考事件",
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
        relation=f"股票代碼 {stock_id}",
    )


def _render_market_event_case_study(client: FinMindClient):
    """Market Event Case Study main page — historian perspective."""
    st.markdown("## 📚 市場事件案例研究")
    st.markdown("以歷史學家的角度，回顧台灣與全球金融市場的重大事件")
    st.markdown("---\n")

    # ── Historian positioning disclaimer ─────────────────────
    _info_card(
        "我們的定位：歷史學家，不是投資顧問",
        "這些案例研究是在解釋「發生了什麼事」和「為什麼」，不是在告訴你「該買什麼」。"
        "投資決策每個人都不同，過去的經驗不代表未來的結果。",
        icon="📖",
    )

    # ── Case study selector ──────────────────────────────────
    case_studies = get_case_studies()

    if not case_studies:
        new_events = get_case_studies()
        if new_events:
            case_studies = new_events

    st.markdown("### 🔍 選擇一個事件深入研究\n")

    # Display as selection cards using a selectbox
    options = {f"{_severity_badge(cs['severity'])} {cs['title']}（{cs['date'][:4]}）": cs["id"] for cs in case_studies}
    selected_label = st.selectbox(
        "選擇事件",
        list(options.keys()),
        key="case_study_selector",
        label_visibility="collapsed",
    )
    selected_id = options[selected_label] if selected_label else None

    if not selected_id:
        return

    study = get_case_study(selected_id)
    if not study:
        st.error("找不到此案例研究的詳細資料。")
        return

    st.markdown("---\n")

    # ── Hero section ─────────────────────────────────────────
    severity_badge = _severity_badge(study["severity"])
    st.markdown(f"# {study['title']}")
    st.markdown(f"**{study['date']}** ｜ {severity_badge}")
    st.markdown(f"\n> {study['summary']}")

    st.markdown("---\n")

    # ── What Happened ────────────────────────────────────────
    _section_title("📖", "發生了什麼事")

    for i, paragraph in enumerate(study["what_happened"]):
        if i == 0:
            # First paragraph is the opening — make it prominent
            st.markdown(f"**{paragraph}**")
        else:
            st.markdown(paragraph)
        st.markdown("")

    # ── Key Metrics ──────────────────────────────────────────
    st.markdown("---\n")
    _section_title("📊", "關鍵數據")

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
    _section_title("🎓", "歷史教了我們什麼")

    lessons = study.get("lessons", [])
    for lesson in lessons:
        with st.expander(f"💡 {lesson['title']}", expanded=False):
            st.markdown(lesson["content"])

    # ── Related Stocks ───────────────────────────────────────
    st.markdown("---\n")
    _section_title("🏷️", "相關個股")

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
                        f"查看 {stock['stock_name']} 名片",
                        key=f"related_{study['id']}_{stock['stock_id']}",
                        use_container_width=True,
                    ):
                        navigate_to(page="名片", stock_id=stock["stock_id"])

    # ── All case studies overview ────────────────────────────
    st.markdown("---\n")
    _section_title("📋", "所有案例研究")

    for cs in case_studies:
        badge = _severity_badge(cs["severity"])
        with st.expander(f"{badge} {cs['title']} — {cs['date'][:4]}"):
            st.markdown(cs["summary"])
            if st.button(
                f"深入研究：{cs['title']}",
                key=f"goto_{cs['id']}",
                use_container_width=True,
            ):
                st.session_state["case_study_selector"] = f"{badge} {cs['title']}（{cs['date'][:4]}）"
                st.rerun()

    # ── Historian disclaimer ─────────────────────────────────
    st.markdown("---\n")
    _historian_disclaimer("general")
