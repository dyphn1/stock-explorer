"""Quiz Service — C101 Comprehension Check for Business Card
Loads quiz YAML files, selects appropriate quiz based on stock data,
tracks user's quiz attempts and score in session_state.
"""

from __future__ import annotations

import logging
import os
import random
from typing import Any, Dict, List, Optional, Tuple

import yaml

from src.services.quiz_engine import (
    load_yaml_config,
    normalize_questions,
    build_question_map,
    get_questions_raw,
)

logger = logging.getLogger(__name__)

# -- Module-level cache ------------------------------------------
_quiz_cache: Dict[str, Dict[str, Any]] = {}  # path -> loaded quiz config
_quiz_files: List[str] = []  # list of absolute paths to quiz YAML files

# -- Path helpers ------------------------------------------------
def _quiz_dir() -> str:
    """Return the absolute path to src/data/yaml/quiz/."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(project_root, "src", "data", "yaml", "quiz")


def _collect_quiz_files() -> List[str]:
    """Collect all YAML files in the quiz directory."""
    quiz_dir = _quiz_dir()
    if not os.path.isdir(quiz_dir):
        logger.warning(f"Quiz directory not found: {quiz_dir}")
        return []
    files = []
    for f in os.listdir(quiz_dir):
        if f.endswith(('.yaml', '.yml')):
            files.append(os.path.join(quiz_dir, f))
    return files


def _load_quiz_config(config_path: str) -> Dict[str, Any]:
    """Load a YAML quiz config file, cached in memory by absolute path."""
    if config_path in _quiz_cache:
        return _quiz_cache[config_path]
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            config = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning(f"Failed to load quiz config from {config_path}: {e}")
        config = {}
    _quiz_cache[config_path] = config
    return config


def _get_quiz_questions_raw(config_path: str) -> List[Dict[str, Any]]:
    """Return raw question bank from a YAML quiz config file."""
    config = _load_quiz_config(config_path)
    return config.get("questions", [])


def initialize_quiz_service() -> None:
    """Initialize the quiz service by collecting and caching quiz files."""
    global _quiz_files
    _quiz_files = _collect_quiz_files()
    logger.info(f"Loaded {len(_quiz_files)} quiz files from {_quiz_dir()}")
    # Optionally, we could pre-load all configs here, but we'll lazy-load.


def select_quiz_based_on_stock(data: Dict[str, Any]) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Select an appropriate quiz YAML file based on stock data.

    Args:
        data: The business card data dict containing stock information.

    Returns:
        Tuple of (selected_file_path, quiz_config) where quiz_config is the
        loaded YAML dict (with "questions" list). Returns (None, None) if no
        quiz files available.
    """
    if not _quiz_files:
        initialize_quiz_service()
    if not _quiz_files:
        return None, None

    # Extract relevant metrics
    extra_metrics = data.get("extra_metrics", {})
    latest_per_pbr = data.get("latest_per_pbr", {})

    has_roe = extra_metrics.get("roe") is not None
    has_per = latest_per_pbr.get("PER") is not None
    has_dividend_yield = latest_per_pbr.get("dividend_yield") is not None

    # Define priority order: ROE > PER > Dividend Yield > Random
    selected_path = None
    if has_roe:
        # Look for ROE quiz file
        for f in _quiz_files:
            if "roe" in f.lower():
                selected_path = f
                break
    if not selected_path and has_per:
        for f in _quiz_files:
            if "pe" in f.lower() or "per" in f.lower():
                selected_path = f
                break
    if not selected_path and has_dividend_yield:
        for f in _quiz_files:
            if "dividend" in f.lower() or "yield" in f.lower():
                selected_path = f
                break
    if not selected_path:
        # Fallback to random selection
        selected_path = random.choice(_quiz_files)

    # Load the selected quiz config
    quiz_config = _load_quiz_config(selected_path)
    return selected_path, quiz_config


def get_quiz_question(quiz_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract the first question from a quiz config.

    Args:
        quiz_config: The loaded YAML dict (expects a "questions" list).

    Returns:
        A question dict with keys: id, text, correct_key, options (list of tuples),
        or None if no questions found.
    """
    questions = quiz_config.get("questions", [])
    if not questions:
        return None
    # We assume each quiz file contains exactly one question for simplicity.
    # If there are multiple, we take the first one.
    raw_question = questions[0]
    # Normalize options to tuples (as expected by the quiz engine)
    if "options" in raw_question:
        raw_question["options"] = [
            tuple(opt) if isinstance(opt, list) else opt
            for opt in raw_question["options"]
        ]
    return raw_question


def check_quiz_answer(
    question: Dict[str, Any], selected_key: str
) -> Dict[str, Any]:
    """Check a quiz answer for a given question.

    Args:
        question: The question dict (as returned by get_quiz_question).
        selected_key: The option key the user selected (e.g., "a").

    Returns:
        Dict with keys: correct (bool), correct_key (str), explanation (str).
    """
    correct_key = question.get("correct_key", "")
    is_correct = selected_key == correct_key

    # Find explanation for the selected option
    explanation = ""
    for opt in question.get("options", []):
        if str(opt[0]) == str(selected_key):
            explanation = opt[2] if len(opt) > 2 else ""
            break

    return {
        "correct": is_correct,
        "correct_key": correct_key,
        "explanation": explanation,
    }


def track_quiz_attempt(
    stock_id: str, quiz_id: str, is_correct: bool
) -> None:
    """Track quiz attempt and score in session_state.

    Args:
        stock_id: The stock identifier.
        quiz_id: The quiz identifier (e.g., "roe_meaning").
        is_correct: Whether the user answered correctly.
    """
    import streamlit as st

    # Initialize quiz tracking in session state if not present
    if "quiz_attempts" not in st.session_state:
        st.session_state["quiz_attempts"] = {}
    if stock_id not in st.session_state["quiz_attempts"]:
        st.session_state["quiz_attempts"][stock_id] = {}

    # Record this attempt
    attempt_key = f"{quiz_id}"
    if attempt_key not in st.session_state["quiz_attempts"][stock_id]:
        st.session_state["quiz_attempts"][stock_id][attempt_key] = {
            "attempts": 0,
            "correct": 0,
            "last_result": None,
        }

    attempt_data = st.session_state["quiz_attempts"][stock_id][attempt_key]
    attempt_data["attempts"] += 1
    if is_correct:
        attempt_data["correct"] += 1
    attempt_data["last_result"] = {
        "correct": is_correct,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

    # Optionally, we can also track overall score for the stock
    # For simplicity, we'll just keep per-quiz stats.


def get_quiz_score(stock_id: str) -> Dict[str, Any]:
    """Get aggregated quiz score for a stock.

    Args:
        stock_id: The stock identifier.

    Returns:
        Dict with keys: total_attempts, total_correct, average_score (percentage).
    """
    import streamlit as st

    attempts = st.session_state.get("quiz_attempts", {}).get(stock_id, {})
    total_attempts = sum(v["attempts"] for v in attempts.values())
    total_correct = sum(v["correct"] for v in attempts.values())
    average_score = (
        (total_correct / total_attempts * 100) if total_attempts > 0 else 0.0
    )
    return {
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "average_score": average_score,
    }
