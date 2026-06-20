"""
Financial Wellness Service — C85
Behavioral finance self-assessment quiz logic.
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
_QUIZ_CONFIG_PATH = get_config_path("config", "quiz.yaml")

_QUIZ_CONFIG: dict[str, Any] = {}


def _load_quiz_config() -> dict[str, Any]:
    """Load quiz config from YAML, cached in memory."""
    global _QUIZ_CONFIG
    if _QUIZ_CONFIG:
        return _QUIZ_CONFIG
    _QUIZ_CONFIG = load_yaml_config(_QUIZ_CONFIG_PATH)
    return _QUIZ_CONFIG


def _get_questions_raw() -> list[dict[str, Any]]:
    """Return raw question bank from YAML config."""
    return get_questions_raw(_QUIZ_CONFIG_PATH)


def get_questions() -> list[dict[str, Any]]:
    """Return the list of quiz questions.

    Each question dict has keys:
        id, text, options: list of (key, label, score)
    """
    raw = _get_questions_raw()
    return normalize_questions(raw)


def _get_category_map() -> dict[str, str]:
    """Return question_id -> category_name mapping from YAML config."""
    config = _load_quiz_config()
    return config.get("category_map", {})


def _get_category_tips() -> dict[str, str]:
    """Return category tips from YAML config."""
    config = _load_quiz_config()
    return config.get("category_tips", {})


def calculate_score(answers: dict[str, str]) -> dict[str, Any]:
    """Calculate total and category scores from user answers.

    Args:
        answers: Dict mapping question_id -> option_key (a/b/c/d).

    Returns:
        Dict with keys:
            total_score (int), max_score (int),
            category_scores: dict[category_name -> score],
            weak_areas: list of category_names with score <= 2
    """
    raw = _get_questions_raw()
    category_map = _get_category_map()
    question_map = build_question_map(raw)
    total = 0
    category_scores: dict[str, int] = {}

    for qid, opt_key in answers.items():
        q = question_map.get(qid)
        if not q:
            continue
        for key, _label, score in q["options"]:
            if key == opt_key:
                total += score
                cat = category_map.get(qid, qid)
                category_scores[cat] = score
                break

    max_score = len(raw) * 4
    weak_areas = [cat for cat, s in category_scores.items() if s <= 2]
    # Sort weak areas by score ascending (weakest first)
    weak_areas.sort(key=lambda c: category_scores[c])

    return {
        "total_score": total,
        "max_score": max_score,
        "category_scores": category_scores,
        "weak_areas": weak_areas,
    }


def get_interpretation(score: int) -> dict[str, Any]:
    """Return plain-language interpretation for a total score.

    Args:
        score: Total score (10-40).

    Returns:
        Dict with keys: level, emoji, title, description, color
    """
    if score >= 30:
        return {
            "level": "healthy",
            "emoji": "🟢",
            "title": "理財健康",
            "description": "你的理財習慣整體來說很不錯！有基本的財務紀律和風險意識。繼續保持，並持續學習。",
            "color": "#27AE60",
        }
    elif score >= 20:
        return {
            "level": "average",
            "emoji": "🟡",
            "title": "理財一般",
            "description": "你的理財習慣有基本的概念，但還有一些地方可以加強。參考下方的建議，逐步改善。",
            "color": "#E67E22",
        }
    else:
        return {
            "level": "attention",
            "emoji": "🔴",
            "title": "需要留意",
            "description": "你的理財習慣還有不少改善空間。別擔心，每個人都是從零開始。先從最簡單的步驟做起。",
            "color": "#E74C3C",
        }


def get_tips(answers: dict[str, str]) -> list[dict[str, str]]:
    """Return 3 personalized tips based on lowest-scoring areas.

    Args:
        answers: Dict mapping question_id -> option_key.

    Returns:
        List of up to 3 dicts with keys: category, tip
    """
    category_map = _get_category_map()
    category_tips = _get_category_tips()
    result = calculate_score(answers)
    weak = result["weak_areas"][:3]
    tips = []
    for cat in weak:
        # Find question_id from category name
        qid = None
        for k, v in category_map.items():
            if v == cat:
                qid = k
                break
        tip_text = category_tips.get(qid, "") if qid else ""
        if not tip_text:
            tip_text = f'"{cat}" 是你最需要加強的部分，建議多了解相關知識。'
        tips.append({"category": cat, "tip": tip_text})
    return tips
