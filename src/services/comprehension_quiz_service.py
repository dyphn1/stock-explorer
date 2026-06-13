"""
Comprehension Quiz Service — C101
Generic investing literacy comprehension check quiz logic.
No streamlit imports.
"""

from __future__ import annotations

import logging
from typing import Any

from src.services.quiz_engine import (
    build_question_map,
    get_config_path,
    get_questions_raw,
    load_yaml_config,
    normalize_questions,
)

logger = logging.getLogger(__name__)

# ── Load quiz config once at module level ──────────────────
_QUIZ_CONFIG_PATH = get_config_path("config", "comprehension_quiz.yaml")

_QUIZ_CONFIG: dict[str, Any] = {}


def _load_quiz_config() -> dict[str, Any]:
    """Load comprehension quiz config from YAML, cached in memory."""
    global _QUIZ_CONFIG
    if _QUIZ_CONFIG:
        return _QUIZ_CONFIG
    _QUIZ_CONFIG = load_yaml_config(_QUIZ_CONFIG_PATH)
    return _QUIZ_CONFIG


def _get_questions_raw() -> list[dict[str, Any]]:
    """Return raw question bank from YAML config."""
    return get_questions_raw(_QUIZ_CONFIG_PATH)


def get_questions() -> list[dict[str, Any]]:
    """Return the list of comprehension quiz questions.

    Each question dict has keys:
        id, text, correct_key, options: list of (key, label, explanation)
    """
    raw = _get_questions_raw()
    return normalize_questions(raw)


def check_answer(question_id: str, selected_key: str) -> dict[str, Any]:
    """Check if the selected answer is correct.

    Args:
        question_id: The question ID.
        selected_key: The option key the user selected (a/b/c/d).

    Returns:
        Dict with keys:
            correct (bool), explanation (str), correct_key (str)
    """
    raw = _get_questions_raw()
    question_map = build_question_map(raw)
    q = question_map.get(question_id)
    if not q:
        return {"correct": False, "explanation": "找不到題目", "correct_key": ""}

    correct_key = q.get("correct_key", "")
    is_correct = selected_key == correct_key

    # Find the explanation for the selected option
    explanation = ""
    for opt in q.get("options", []):
        if opt[0] == selected_key:
            explanation = opt[2]  # explanation is the third element
            break

    return {
        "correct": is_correct,
        "explanation": explanation,
        "correct_key": correct_key,
    }


def calculate_score(answers: dict[str, str]) -> dict[str, Any]:
    """Calculate score from user answers.

    Args:
        answers: Dict mapping question_id -> option_key (a/b/c/d).

    Returns:
        Dict with keys:
            correct_count (int), total (int), percentage (float),
            results: list of dicts with question_id, correct, explanation
    """
    raw = _get_questions_raw()
    question_map = build_question_map(raw)
    total = len(raw)
    correct_count = 0
    results = []

    for qid, selected_key in answers.items():
        q = question_map.get(qid)
        if not q:
            continue
        correct_key = q.get("correct_key", "")
        is_correct = selected_key == correct_key
        if is_correct:
            correct_count += 1

        # Find explanation for selected option
        explanation = ""
        for opt in q.get("options", []):
            if opt[0] == selected_key:
                explanation = opt[2]
                break

        results.append({
            "question_id": qid,
            "question_text": q.get("text", ""),
            "correct": is_correct,
            "explanation": explanation,
            "selected_key": selected_key,
            "correct_key": correct_key,
        })

    percentage = (correct_count / total * 100) if total > 0 else 0

    return {
        "correct_count": correct_count,
        "total": total,
        "percentage": percentage,
        "results": results,
    }
