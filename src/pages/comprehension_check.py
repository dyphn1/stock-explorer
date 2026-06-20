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
from src.core.i18n import t
from src.services.comprehension_quiz_service import (
    get_questions,
    check_answer,
    calculate_score,
)


def _render_comprehension_check(client: FinMindClient):
    """Comprehension Check Quiz main page — investing literacy questions."""
    st.markdown(f"## 📝 {t('comprehension_check.title')}")
    st.markdown(t("comprehension_check.subtitle"))
    st.markdown("---\n")

    # ── Introduction ───────────────────────────────────────
    _info_card(
        t("comprehension_check.what_is_this"),
        t("comprehension_check.what_is_this_desc"),
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
            if st.button(f"🚀 {t('comprehension_check.start_btn')}", key="comprehension_start", use_container_width=True):
                st.session_state["comprehension_show_form"] = True
                st.rerun()
    with col_reset:
        if st.session_state["comprehension_quiz_done"]:
            if st.button(f"🔄 {t('comprehension_check.reset_btn')}", key="comprehension_reset", use_container_width=True):
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
        _section_title(f"📝 {t('comprehension_check.start_answering')}")

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

            quiz_submitted = st.form_submit_button(f"✅ {t('comprehension_check.submit_btn')}", use_container_width=True)

        if quiz_submitted:
            st.session_state["comprehension_answers"] = answers
            st.session_state["comprehension_quiz_done"] = True
            st.session_state["comprehension_show_form"] = False
            st.rerun()

    # ── Results display ────────────────────────────────────
    if st.session_state["comprehension_quiz_done"]:
        answers = st.session_state.get("comprehension_answers", {})
        if not answers:
            st.warning(t("comprehension_check.no_answers"))
            return

        result = calculate_score(answers)
        correct_count = result["correct_count"]
        total = result["total"]
        percentage = result["percentage"]

        st.markdown("---\n")
        _section_title(f"📊 {t('comprehension_check.results')}")

        # ── Score summary cards ─────────────────────────────
        if percentage >= 80:
            score_color = "#27AE60"
            score_emoji = "🟢"
            score_title = t("comprehension_check.excellent")
            score_desc = t("comprehension_check.excellent_desc")
        elif percentage >= 60:
            score_color = "#E67E22"
            score_emoji = "🟡"
            score_title = t("comprehension_check.good")
            score_desc = t("comprehension_check.good_desc")
        else:
            score_color = "#E74C3C"
            score_emoji = "🔴"
            score_title = t("comprehension_check.needs_work")
            score_desc = t("comprehension_check.needs_work_desc")

        col1, col2 = st.columns(2)
        with col1:
            _白话_card(
                t("comprehension_check.correct_count"),
                f"{correct_count} / {total}",
                f"{score_emoji} {score_title}",
            )
        with col2:
            _白话_card(
                t("comprehension_check.accuracy"),
                f"{percentage:.0f}%",
                score_desc,
            )

        st.markdown("\n")

        # ── Detailed results per question ───────────────────
        _section_title(f"📋 {t('comprehension_check.question_details')}")

        for i, r in enumerate(result["results"], 1):
            qid = r["question_id"]
            is_correct = r["correct"]
            status = f"✅ {t('comprehension_check.correct')}" if is_correct else f"❌ {t('comprehension_check.wrong')}"

            with st.container():
                if is_correct:
                    st.success(f"{status} {t('comprehension_check.question_n', n=i)}")
                else:
                    st.error(f"{status} {t('comprehension_check.question_n', n=i)}")
                st.markdown(f"**{r['question_text']}**")
                st.info(r["explanation"])
                st.markdown("---")

        st.markdown("\n")

        # ── Encouragement message ───────────────────────────
        if correct_count == total:
            _info_card(
                t("comprehension_check.perfect_title"),
                t("comprehension_check.perfect_desc"),
                icon="🏆",
            )
        elif correct_count >= total // 2:
            _info_card(
                t("comprehension_check.good_job_title"),
                t("comprehension_check.good_job_desc"),
                icon="📚",
            )
        else:
            _info_card(
                t("comprehension_check.keep_learning_title"),
                t("comprehension_check.keep_learning_desc"),
                icon="📖",
            )

    st.markdown("---\n")
    _historian_disclaimer("general")
