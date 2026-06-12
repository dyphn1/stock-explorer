"""
Financial Wellness Service — C85
Behavioral finance self-assessment quiz logic.
No streamlit imports.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# ── Load quiz config once at module level ──────────────────
_QUIZ_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "quiz.yaml",
)

_QUIZ_CONFIG: dict[str, Any] = {}


def _load_quiz_config() -> dict[str, Any]:
    """Load quiz config from YAML, cached in memory."""
    global _QUIZ_CONFIG
    if _QUIZ_CONFIG:
        return _QUIZ_CONFIG
    try:
        with open(_QUIZ_CONFIG_PATH, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            _QUIZ_CONFIG = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load quiz config from %s: %s", _QUIZ_CONFIG_PATH, e)
        _QUIZ_CONFIG = {}
    return _QUIZ_CONFIG


def _get_questions_raw() -> list[dict[str, Any]]:
    """Return raw question bank from YAML config."""
    config = _load_quiz_config()
    return config.get("questions", [])


def _get_category_map() -> dict[str, str]:
    """Return question_id -> category_name mapping from YAML config."""
    config = _load_quiz_config()
    return config.get("category_map", {})


def _get_category_tips() -> dict[str, str]:
    """Return category tips from YAML config."""
    config = _load_quiz_config()
    return config.get("category_tips", {})


def get_questions() -> list[dict[str, Any]]:
    """Return the list of quiz questions.

    Each question dict has keys:
        id, text, options: list of (key, label, score)
    """
    questions = _get_questions_raw()
    # Convert options from YAML lists to tuples
    for q in questions:
        if "options" in q:
            q["options"] = [tuple(opt) if isinstance(opt, list) else opt for opt in q["options"]]
    return questions


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
    questions = _get_questions_raw()
    category_map = _get_category_map()
    question_map = {q["id"]: q for q in questions}
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

    max_score = len(questions) * 4
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
            "color": "#F39C12",
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
