"""
Education Academy — C47
Structured investing lessons with quizzes in Traditional Chinese.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages._router_base import _info_card, _section_title, _白话_card, get_stock_data
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.lesson_service import (
    load_academy_meta,
    get_lesson,
    get_all_lessons,
    check_answer,
    get_progress,
    mark_lesson_complete,
    get_completion_rate,
)


# ── Content block rendering helpers ──────────────────────────

def _render_content_block(block: dict, client: FinMindClient) -> None:
    """Render a single content block based on its type."""
    btype = block.get("type", "")

    if btype == "heading":
        st.markdown(f"#### {block.get('text', '')}")

    elif btype == "paragraph":
        st.markdown(block.get("text", ""))

    elif btype == "callout":
        text = block.get("text", "")
        _info_card("重點提示", text, icon="💡")

    elif btype == "stock_example":
        _render_stock_example(block, client)

    else:
        # Fallback: render as paragraph
        if "text" in block:
            st.markdown(block["text"])


def _render_stock_example(block: dict, client: FinMindClient) -> None:
    """Render a stock example block with live data."""
    stock_id = block.get("stock_id", "")
    stock_name = block.get("stock_name", "")
    text = block.get("text", "")
    data_points = block.get("data_points", [])

    st.markdown(text)
    st.markdown("")

    # Fetch live data
    if stock_id:
        try:
            data = get_stock_data(client, stock_id)
            if data:
                cols = st.columns(min(len(data_points) + 1, 4))

                # Show stock name and price
                latest_price = data.get("latest_price")
                if latest_price and len(cols) > 0:
                    price = latest_price.get("close", "N/A")
                    change = latest_price.get("change", 0)
                    sign = "+" if isinstance(change, (int, float)) and change >= 0 else ""
                    with cols[0]:
                        _白话_card(
                            f"{stock_name} ({stock_id})",
                            f"{price:,.0f}" if isinstance(price, (int, float)) else str(price),
                            f"{sign}{change:,.0f}" if isinstance(change, (int, float)) else "",
                        )

                # Show additional data points
                for i, dp in enumerate(data_points):
                    if i + 1 < len(cols):
                        label = dp.get("label", "")
                        source = dp.get("source", "")
                        # Parse source like "latest_price.close"
                        parts = source.split(".")
                        value = "N/A"
                        if len(parts) == 2 and latest_price:
                            value = latest_price.get(parts[1], "N/A")
                        with cols[i + 1]:
                            _白话_card(label, str(value), "")
        except Exception:
            st.caption("⚠️ 無法載入即時資料，請稍後再試。")

    st.markdown("---")


def _get_score_style(percentage: float) -> dict:
    """Get score styling based on percentage."""
    if percentage >= 80:
        return {
            "emoji": "🟢",
            "title": "優秀！",
            "desc": "你對這課的內容有很好的理解，繼續保持！"
        }
    elif percentage >= 60:
        return {
            "emoji": "🟡",
            "title": "不錯！",
            "desc": "你有基本的概念，但還有一些地方可以加強。"
        }
    else:
        return {
            "emoji": "🔴",
            "title": "加油！",
            "desc": "別擔心，回頭看看解說，你會進步的！"
        }


def _render_quiz(lesson: dict, lesson_id: str, progress: dict) -> None:
    """Render the quiz section for a lesson."""
    quiz_list = lesson.get("quiz", [])
    if not quiz_list:
        return

    st.markdown("---")
    _section_title("📝 課後測驗")

    st.markdown("完成以下問題來檢驗你的理解。")

    # Quiz state keys
    quiz_submitted_key = f"academy_quiz_submitted_{lesson_id}"
    quiz_answers_key = f"academy_quiz_answers_{lesson_id}"

    if quiz_submitted_key not in st.session_state:
        st.session_state[quiz_submitted_key] = False

    if not st.session_state[quiz_submitted_key]:
        with st.form(f"academy_quiz_form_{lesson_id}"):
            answers = {}
            for q in quiz_list:
                qid = q["id"]
                option_texts = [opt[1] for opt in q["options"]]
                option_keys = [opt[0] for opt in q["options"]]

                st.markdown(f"**{q['text']}**")
                selected_label = st.radio(
                    q["text"],
                    option_texts,
                    key=f"academy_q_{lesson_id}_{qid}",
                    label_visibility="collapsed",
                )
                idx = option_texts.index(selected_label)
                answers[qid] = option_keys[idx]
                st.markdown("")

            quiz_submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)

        if quiz_submitted:
            st.session_state[quiz_answers_key] = answers
            st.session_state[quiz_submitted_key] = True
            st.rerun()

    # Results display
    if st.session_state[quiz_submitted_key]:
        answers = st.session_state.get(quiz_answers_key, {})
        if not answers:
            st.warning("找不到測驗答案，請重新開始。")
            return

        results = []
        correct_count = 0
        for q in quiz_list:
            qid = q["id"]
            selected = answers.get(qid, "")
            result = check_answer(lesson_id, qid, selected)
            # Attach question text for display
            result["question_text"] = q.get("text", "")
            results.append(result)
            if result["correct"]:
                correct_count += 1

        total = len(quiz_list)
        percentage = (correct_count / total * 100) if total > 0 else 0

        # Mark lesson complete
        mark_lesson_complete(progress, lesson_id, percentage)

        st.markdown("---")
        _section_title("📊 測驗結果")

        # Score summary
        score_style = _get_score_style(percentage)

        col1, col2 = st.columns(2)
        with col1:
            _白话_card("答對題數", f"{correct_count} / {total}", f"{score_style['emoji']} {score_style['title']}")
        with col2:
            _白话_card("正確率", f"{percentage:.0f}%", score_style['desc'])

        st.markdown("")

        # Detailed results
        _section_title("📋 各題詳解")
        for i, r in enumerate(results, 1):
            is_correct = r["correct"]
            status = "✅ 答對" if is_correct else "❌ 答錯"

            if is_correct:
                st.success(f"{status} 第 {i} 題")
            else:
                st.error(f"{status} 第 {i} 題")
            st.markdown(f"**{r['question_text']}**")
            st.info(r["explanation"])
            st.markdown("---")

        # Completion message
        completion_message = lesson.get("completion_message", "🎉 恭喜完成這一課！")
        st.success(completion_message)

        # Next lesson button
        next_lesson_id = lesson.get("next_lesson_id")
        if next_lesson_id:
            if st.button("➡️ 前往下一課", key=f"academy_next_{lesson_id}", use_container_width=True):
                st.session_state["academy_current_lesson"] = next_lesson_id
                # Clear quiz state for current lesson
                st.session_state[quiz_submitted_key] = False
                if quiz_answers_key in st.session_state:
                    del st.session_state[quiz_answers_key]
                st.rerun()

        # Reset button
        if st.button("🔄 重新測驗", key=f"academy_reset_{lesson_id}", use_container_width=True):
            st.session_state[quiz_submitted_key] = False
            if quiz_answers_key in st.session_state:
                del st.session_state[quiz_answers_key]
            st.rerun()


# ── Main page renderer ────────────────────────────────────────

def _render_academy(client: FinMindClient):
    """Education Academy main page — structured investing lessons with quizzes."""
    meta = load_academy_meta()
    title = meta.get("title", "學習學院")
    description = meta.get("description", "")

    # ── Academy header ────────────────────────────────────────
    st.markdown(f"## 🎓 {title}")
    st.markdown(f"_{description}_")
    st.markdown("")

    # Progress bar
    if "academy_progress" not in st.session_state:
        st.session_state["academy_progress"] = {}
    progress = get_progress(st.session_state["academy_progress"])
    completion_rate = get_completion_rate(progress)
    all_lessons = get_all_lessons()
    total_lessons = len(all_lessons)
    completed_count = sum(1 for v in progress.values() if v.get("completed", False))

    col_prog, col_text = st.columns([4, 1])
    with col_prog:
        st.progress(completion_rate / 100.0)
    with col_text:
        st.markdown(f"**{completed_count}/{total_lessons}** 完成")

    st.markdown("---")

    # ── Lesson list ───────────────────────────────────────────

    if "academy_current_lesson" not in st.session_state:
        st.session_state["academy_current_lesson"] = None

    # Determine which lesson to show
    current_lesson_id = st.session_state["academy_current_lesson"]

    if current_lesson_id is None:
        # Show lesson list
        _section_title("📚 課程列表")

        for lesson in all_lessons:
            lid = lesson.get("id", "")
            l_title = lesson.get("title", "")
            l_icon = lesson.get("icon", "📖")
            l_time = lesson.get("estimated_time", "")
            l_diff = lesson.get("difficulty", "")
            l_objectives = lesson.get("learning_objectives", "")
            order = lesson.get("order", "")

            lesson_progress = progress.get(lid, {})
            is_completed = lesson_progress.get("completed", False)
            score = lesson_progress.get("score", 0)

            # Status icon
            status_icon = "✅" if is_completed else "📖"

            with st.container():
                col_main, col_btn = st.columns([4, 1])
                with col_main:
                    st.markdown(f"### {status_icon} {l_icon} 第 {order} 課：{l_title}")
                    st.markdown(f"⏱ {l_time} ｜ 📊 難度：{l_diff}")
                    if is_completed:
                        st.caption(f"已完成 ｜ 得分：{score:.0f}%")
                with col_btn:
                    if st.button(
                        "開始" if not is_completed else "複習",
                        key=f"academy_start_{lid}",
                        use_container_width=True,
                    ):
                        st.session_state["academy_current_lesson"] = lid
                        st.rerun()

                # Learning objectives
                if isinstance(l_objectives, list):
                    for obj in l_objectives:
                        st.markdown(f"- {obj}")
                elif isinstance(l_objectives, str) and l_objectives:
                    st.markdown(f"- {l_objectives}")

                st.markdown("---")

    else:
        # Show specific lesson
        lesson = get_lesson(current_lesson_id)
        if lesson is None:
            st.error("找不到課程內容。")
            if st.button("← 返回課程列表"):
                st.session_state["academy_current_lesson"] = None
                st.rerun()
            return

        # Back button
        if st.button("← 返回課程列表"):
            st.session_state["academy_current_lesson"] = None
            st.rerun()

        # Lesson header
        l_icon = lesson.get("icon", "📖")
        l_title = lesson.get("title", "")
        l_time = lesson.get("estimated_time", "")
        l_diff = lesson.get("difficulty", "")

        st.markdown(f"## {l_icon} 第 {lesson.get('order', '')} 課：{l_title}")
        st.markdown(f"⏱ {l_time} ｜ 📊 難度：{l_diff}")
        st.markdown("---")

        # Learning objectives
        objectives = lesson.get("learning_objectives", [])
        if objectives:
            _section_title("🎯 學習目標")
            if isinstance(objectives, list):
                for obj in objectives:
                    st.markdown(f"- {obj}")
            elif isinstance(objectives, str) and objectives:
                st.markdown(f"- {objectives}")
            st.markdown("")

        # Lesson content
        content_blocks = lesson.get("content", [])
        for block in content_blocks:
            _render_content_block(block, client)

        # Quiz
        _render_quiz(lesson, current_lesson_id, progress)

    st.markdown("---\n")
    _historian_disclaimer("general")
