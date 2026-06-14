"""
Experience Service — C163 + C40
Manages user experience level (beginner/expert) and gateway lesson content.

Pure Python — no Streamlit imports. Session state is passed in by the caller.
"""
from __future__ import annotations
import os
import yaml
from typing import Any

def _config_dir() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "lessons")

def get_experience_level(session_state: dict) -> str:
    return session_state.get("user_experience_level", "beginner")

def is_beginner_mode(session_state: dict) -> bool:
    return get_experience_level(session_state) == "beginner"

def set_experience_level(session_state: dict, level: str) -> None:
    if level in ("beginner", "expert"):
        session_state["user_experience_level"] = level

def get_gateway_lessons() -> list[dict]:
    path = os.path.join(_config_dir(), "gateway_lessons.yaml")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("lessons", []) if data else []
    except Exception:
        return []
