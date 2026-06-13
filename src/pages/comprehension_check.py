"""
Comprehension Check Quiz — C101
Generic investing literacy comprehension check quiz.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages._router_base import _info_card, _section_title, _白话_card
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.comprehension_quiz_service import (
    get_questions,
    check_answer,
    calculate_score,
)


def _render_comprehension_check(client: FinMindClient):
    """Comprehension Check Quiz main page — investing literacy questions."""
    st.markdown("## 📝 理解力測驗")
    st.markdown("測試你對投資基礎觀念的理解程度，共 5 題選擇題")
    st.markdown("---\n")

    # ── Introduction ───────────────────────────────────────
    _info_card(
        "這是什麼？",
        "這份測驗的目的不是考滿分，而是幫你確認自己對投資基礎觀念的理解是否正確。"
        "沒答對也沒關係——重要的是看解說，學到東西才是重點！",
        icon="💡",
    )

    # ── Quiz state management ──────────────────────────────
    if "comprehension_quiz_done" not in st.session_state:
        st.session_state["comprehension_quiz_done"] = False
    if "comprehension_show_form" not in st.session_state:
        st.session_state["comprehension_show_form"] = False

    questions = get_questions()

    # ── Start / Reset buttons ──────────────────────────────
    col_start, col_reset = st.columns(2)
    with col_start:
        if not st.session_state["comprehension_show_form"] and not st.session_state["comprehension_quiz_done"]:
            if st.button("🚀 開始測驗", key="comprehension_start", use_container_width=True):
                st.session_state["comprehension_show_form"] = True
                st.rerun()
    with col_reset:
        if st.session_state["comprehension_quiz_done"]:
            if st.button("🔄 重新測驗", key="comprehension_reset", use_container_width=True):
                st.session_state["comprehension_quiz_done"] = False
                st.session_state["comprehension_show_form"] = False
                # Clear answers
                for q in questions:
                    key = f"comprehension_q_{q['id']}"
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    st.markdown("\n")

    # ── Quiz form ──────────────────────────────────────────
    if st.session_state["comprehension_show_form"] and not st.session_state["comprehension_quiz_done"]:
        _section_title("📝 開始作答")

        with st.form("comprehension_quiz_form"):
            answers = {}
            for q in questions:
                qid = q["id"]
                option_texts = [opt[1] for opt in q["options"]]
                option_keys = [opt[0] for opt in q["options"]]

                st.markdown(f"**{q['text']}**")
                selected_label = st.radio(
                    q["text"],
                    option_texts,
                    key=f"comprehension_q_{qid}",
                    label_visibility="collapsed",
                )
                # Map back to key
                idx = option_texts.index(selected_label)
                answers[qid] = option_keys[idx]
                st.markdown("")

            quiz_submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)

        if quiz_submitted:
            st.session_state["comprehension_answers"] = answers
            st.session_state["comprehension_quiz_done"] = True
            st.session_state["comprehension_show_form"] = False
            st.rerun()

    # ── Results display ────────────────────────────────────
    if st.session_state["comprehension_quiz_done"]:
        answers = st.session_state.get("comprehension_answers", {})
        if not answers:
            st.warning("找不到測驗答案，請重新開始。")
            return

        result = calculate_score(answers)
        correct_count = result["correct_count"]
        total = result["total"]
        percentage = result["percentage"]

        st.markdown("---\n")
        _section_title("📊 測驗結果")

        # ── Score summary cards ─────────────────────────────
        if percentage >= 80:
            score_color = "#27AE60"
            score_emoji = "🟢"
            score_title = "優秀！"
            score_desc = "你對投資基礎觀念有很好的理解，繼續保持！"
        elif percentage >= 60:
            score_color = "#F39C12"
            score_emoji = "🟡"
            score_title = "不錯！"
            score_desc = "你有基本的概念，但還有一些地方可以加強。"
        else:
            score_color = "#E74C3C"
            score_emoji = "🔴"
            score_title = "加油！"
            score_desc = "別擔心，投資知識需要慢慢累積。看看下方的解說，下次會更好！"

        col1, col2 = st.columns(2)
        with col1:
            _白话_card(
                "答對題數",
                f"{correct_count} / {total}",
                f"{score_emoji} {score_title}",
            )
        with col2:
            _白话_card(
                "正確率",
                f"{percentage:.0f}%",
                score_desc,
            )

        st.markdown("\n")

        # ── Detailed results per question ───────────────────
        _section_title("📋 各題詳解")

        for i, r in enumerate(result["results"], 1):
            qid = r["question_id"]
            is_correct = r["correct"]
            status = "✅ 答對" if is_correct else "❌ 答錯"

            with st.container():
                if is_correct:
                    st.success(f"{status} 第 {i} 題")
                else:
                    st.error(f"{status} 第 {i} 題")
                st.markdown(f"**{r['question_text']}**")
                st.info(r["explanation"])
                st.markdown("---")

        st.markdown("\n")

        # ── Encouragement message ───────────────────────────
        if correct_count == total:
            _info_card(
                "🎉 太厲害了！全部答對！",
                "你已經具備了良好的投資基礎知識。記住，知識是投資最好的武器。繼續學習，保持謙虛！",
                icon="🏆",
            )
        elif correct_count >= total // 2:
            _info_card(
                "💪 表現不錯！",
                "你已經掌握了大部分概念。錯的題目是很好的學習機會，回頭看看解說，你會進步得更快。",
                icon="📚",
            )
        else:
            _info_card(
                "🌱 學習是投資最好的朋友",
                "投資知識需要慢慢累積，每位投資大師都是從零開始。建議重新閱讀名片頁的內容，再試一次！",
                icon="📖",
            )

    st.markdown("---\n")
    _historian_disclaimer("general")
