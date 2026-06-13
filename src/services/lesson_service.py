"""
Lesson Service — C47
Lesson loading, progress tracking, and quiz checking for the Education Academy.

Provides:
  - load_academy_meta() -> dict
  - get_lesson(lesson_id: str) -> dict
  - get_all_lessons() -> list[dict]
  - get_progress() -> dict (from st.session_state["academy_progress"])
  - mark_lesson_complete(lesson_id, score) -> None
  - get_completion_rate() -> float
  - check_answer(lesson_id, question_id, selected_key) -> dict
"""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# -- Module-level cache ------------------------------------------
_lesson_cache: dict[str, dict[str, Any]] = {}
_meta_cache: dict[str, Any] | None = None

# -- Path helpers ------------------------------------------------

def _config_dir() -> str:
    """Return the absolute path to config/lessons/."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(project_root, "config", "lessons")


# -- Academy meta ------------------------------------------------

def load_academy_meta() -> dict[str, Any]:
    """Load academy metadata from academy_meta.yaml.

    Returns:
        Parsed academy config dict, or empty dict on failure.
    """
    global _meta_cache
    if _meta_cache is not None:
        return _meta_cache

    path = os.path.join(_config_dir(), "academy_meta.yaml")
    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            _meta_cache = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load academy meta from %s: %s", path, e)
        _meta_cache = {}
    return _meta_cache


# -- Lesson loading ----------------------------------------------

def _find_lesson_file(lesson_id: str) -> str | None:
    """Find the YAML file path for a given lesson ID by scanning academy_meta."""
    meta = load_academy_meta()
    lessons = meta.get("lessons", [])
    for lesson_entry in lessons:
        if lesson_entry.get("id") == lesson_id:
            file_name = lesson_entry.get("file", f"{lesson_id}.yaml")
            return os.path.join(_config_dir(), file_name)
    # Fallback: try the conventional name
    fallback = os.path.join(_config_dir(), f"{lesson_id}.yaml")
    if os.path.exists(fallback):
        return fallback
    return None


def get_lesson(lesson_id: str) -> dict[str, Any] | None:
    """Load a single lesson by ID.

    Args:
        lesson_id: Lesson identifier (e.g. "lesson_01").

    Returns:
        Lesson dict or None if not found.
    """
    if lesson_id in _lesson_cache:
        return _lesson_cache[lesson_id]

    path = _find_lesson_file(lesson_id)
    if path is None:
        logger.warning("Lesson file not found for lesson_id: %s", lesson_id)
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            lesson = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load lesson from %s: %s", path, e)
        return None

    _lesson_cache[lesson_id] = lesson
    return lesson


def get_all_lessons() -> list[dict[str, Any]]:
    """Load all lessons in the order defined by academy_meta.yaml.

    Returns:
        List of lesson dicts.
    """
    meta = load_academy_meta()
    lessons_order = meta.get("lessons", [])
    lessons = []
    for entry in lessons_order:
        lesson_id = entry.get("id")
        if lesson_id:
            lesson = get_lesson(lesson_id)
            if lesson is not None:
                lessons.append(lesson)
    return lessons


# -- Quiz checking -----------------------------------------------

def check_answer(lesson_id: str, question_id: str, selected_key: str) -> dict[str, Any]:
    """Check a quiz answer for a specific lesson and question.

    Args:
        lesson_id: Lesson identifier.
        question_id: Question identifier.
        selected_key: The option key the user selected (e.g. "a").

    Returns:
        Dict with keys: correct (bool), correct_key, explanation.
    """
    lesson = get_lesson(lesson_id)
    if lesson is None:
        return {"correct": False, "correct_key": "", "explanation": "找不到課程"}

    quiz_list = lesson.get("quiz", [])
    for q in quiz_list:
        if q.get("id") == question_id:
            correct_key = q.get("correct_key", "")
            is_correct = selected_key == correct_key
            # Find explanation from the matching option
            explanation = ""
            for opt in q.get("options", []):
                if str(opt[0]) == str(correct_key):
                    explanation = opt[2] if len(opt) > 2 else ""
                    break
            return {
                "correct": is_correct,
                "correct_key": correct_key,
                "explanation": explanation,
            }

    return {"correct": False, "correct_key": "", "explanation": "找不到題目"}


# -- Progress tracking -------------------------------------------

def get_progress(progress_dict: dict[str, Any] | None = None) -> dict[str, Any]:
    """Get the current academy progress.

    Args:
        progress_dict: The academy_progress dict (from st.session_state).
                       If None, returns an empty dict (safe for non-Streamlit contexts).

    Returns:
        Dict mapping lesson_id -> {"completed": bool, "score": float, "completed_at": str}.
    """
    if progress_dict is None:
        return {}
    return progress_dict


def mark_lesson_complete(progress_dict: dict[str, Any], lesson_id: str, score: float) -> None:
    """Mark a lesson as complete with a score.

    Args:
        progress_dict: The academy_progress dict (from st.session_state).
        lesson_id: Lesson identifier.
        score: Quiz score as a float (0-100).
    """
    from datetime import datetime
    progress_dict[lesson_id] = {
        "completed": True,
        "score": score,
        "completed_at": datetime.now().isoformat(),
    }


def get_completion_rate(progress_dict: dict[str, Any]) -> float:
    """Calculate the overall completion rate as a percentage.

    Args:
        progress_dict: The academy_progress dict (from st.session_state).

    Returns:
        Float from 0.0 to 100.0.
    """
    total = len(load_academy_meta().get("lessons", []))
    if total == 0:
        return 0.0
    completed = sum(1 for v in progress_dict.values() if v.get("completed", False))
    return (completed / total) * 100.0
