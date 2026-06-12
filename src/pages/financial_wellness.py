"""
Financial Wellness Check — C85
Behavioral finance self-assessment quiz.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages._router_base import _info_card, _summary_card, _section_title
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.financial_wellness_service import (
    get_questions,
    calculate_score,
    get_interpretation,
    get_tips,
)


def _render_financial_wellness(client: FinMindClient):
    """Financial Wellness Check main page — behavioral finance quiz."""
    st.markdown("## 💰 理財健康檢查")
    st.markdown("透過 10 個問題，了解你的理財習慣與風險承受度")
    st.markdown("---\n")

    # ── Introduction ───────────────────────────────────────
    _summary_card(
        "這不是投資建議",
        "這個測驗的目的是幫助你反思自己的理財行為與態度，不能替代專業理財規劃。"
        "請根據你「真實的情況」回答，而不是「理想的狀態」。",
        icon="📋",
    )

    # ── Quiz state management ──────────────────────────────
    if "wellness_quiz_done" not in st.session_state:
        st.session_state["wellness_quiz_done"] = False
    if "wellness_show_form" not in st.session_state:
        st.session_state["wellness_show_form"] = False

    questions = get_questions()

    # ── Start / Reset buttons ──────────────────────────────
    col_start, col_reset = st.columns(2)
    with col_start:
        if not st.session_state["wellness_show_form"] and not st.session_state["wellness_quiz_done"]:
            if st.button("📝 開始測驗", key="wellness_start", use_container_width=True):
                st.session_state["wellness_show_form"] = True
                st.rerun()
    with col_reset:
        if st.session_state["wellness_quiz_done"]:
            if st.button("🔄 重新測驗", key="wellness_reset", use_container_width=True):
                st.session_state["wellness_quiz_done"] = False
                st.session_state["wellness_show_form"] = False
                # Clear answers
                for q in questions:
                    key = f"wellness_q_{q['id']}"
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    st.markdown("\n")

    # ── Quiz form ──────────────────────────────────────────
    if st.session_state["wellness_show_form"] and not st.session_state["wellness_quiz_done"]:
        _section_title(f"📝 開始作答")

        with st.form("wellness_quiz_form"):
            answers = {}
            for q in questions:
                qid = q["id"]
                options_labels = {key: label for key, _score, label in [(o[0], o[2], o[1]) for o in q["options"]]}
                # Reorder: we need (key, label, score) -> display label, return key
                option_texts = [opt[1] for opt in q["options"]]
                option_keys = [opt[0] for opt in q["options"]]

                st.markdown(f"**{q['text']}**")
                selected_label = st.radio(
                    q["text"],
                    option_texts,
                    key=f"wellness_q_{qid}",
                    label_visibility="collapsed",
                )
                # Map back to key
                idx = option_texts.index(selected_label)
                answers[qid] = option_keys[idx]
                st.markdown("")

            quiz_submitted = st.form_submit_button("📊 查看結果", use_container_width=True)

        if quiz_submitted:
            st.session_state["wellness_answers"] = answers
            st.session_state["wellness_quiz_done"] = True
            st.session_state["wellness_show_form"] = False
            st.rerun()

    # ── Results display ────────────────────────────────────
    if st.session_state["wellness_quiz_done"]:
        answers = st.session_state.get("wellness_answers", {})
        if not answers:
            st.warning("找不到測驗答案，請重新開始。")
            return

        result = calculate_score(answers)
        interpretation = get_interpretation(result["total_score"])
        tips = get_tips(answers)

        st.markdown("---\n")
        _section_title(f"📊 測驗結果")

        # Score display
        score = result["total_score"]
        max_score = result["max_score"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
                border-left:4px solid {interpretation['color']};text-align:center;">
                    <div style="font-size:0.85rem;color:#7F8C8D;">總分</div>
                    <div style="font-size:2.5rem;font-weight:700;color:{interpretation['color']};">
                        {score}
                    </div>
                    <div style="font-size:0.8rem;color:#7F8C8D;">/ {max_score}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
                border-left:4px solid {interpretation['color']};text-align:center;">
                    <div style="font-size:0.85rem;color:#7F8C8D;">評級</div>
                    <div style="font-size:1.8rem;font-weight:700;color:{interpretation['color']};">
                        {interpretation['emoji']} {interpretation['title']}
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        with col3:
            # Category breakdown
            cat_scores = result.get("category_scores", {})
            low_count = sum(1 for s in cat_scores.values() if s <= 2)
            high_count = sum(1 for s in cat_scores.values() if s >= 3)
            st.markdown(
                f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
                border-left:4px solid #3498DB;text-align:center;">
                    <div style="font-size:0.85rem;color:#7F8C8D;">各面向</div>
                    <div style="font-size:1.2rem;font-weight:700;color:#27AE60;">
                        🟢 {high_count} 個達標
                    </div>
                    <div style="font-size:1.2rem;font-weight:700;color:#E74C3C;">
                        🔴 {low_count} 個需加強
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("\n")

        # Interpretation
        _summary_card(
            f"{interpretation['emoji']} {interpretation['title']}",
            interpretation["description"],
            icon="📊",
        )

        # ── Personalized tips ───────────────────────────────
        if tips:
            st.markdown("---\n")
            _section_title(f"💡 個人化建議")
            for tip in tips:
                _info_card(
                    f"加強「{tip['category']}」",
                    tip["tip"],
                    icon="📌",
                )

        # ── Category breakdown ─────────────────────────────
        st.markdown("---\n")
        _section_title(f"📋 各面向得分")

        cat_scores = result.get("category_scores", {})
        if cat_scores:
            cols_per_row = 3
            cat_items = list(cat_scores.items())
            for i in range(0, len(cat_items), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx >= len(cat_items):
                        break
                    cat_name, cat_score = cat_items[idx]
                    if cat_score >= 3:
                        color = "#27AE60"
                        emoji = "🟢"
                    elif cat_score == 2:
                        color = "#F39C12"
                        emoji = "🟡"
                    else:
                        color = "#E74C3C"
                        emoji = "🔴"
                    cols[j].markdown(
                        f"""<div style="background:#F8F9FA;border-radius:12px;
                        padding:0.8rem;border-left:4px solid {color};
                        margin-bottom:0.5rem;">
                            <div style="font-size:0.8rem;color:#7F8C8D;">{emoji} {cat_name}</div>
                            <div style="font-size:1.3rem;font-weight:700;color:{color};">
                                {cat_score}/4
                            </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

    st.markdown("---\n")
    _historian_disclaimer("general")
