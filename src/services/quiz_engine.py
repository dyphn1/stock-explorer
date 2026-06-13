"""
Quiz Engine — D-062
Shared quiz loading utilities for YAML-based quiz services.

Provides:
  - load_yaml_config(path): cached YAML loader
  - normalize_questions(raw): converts option lists to tuples
  - build_question_map(raw): id -> question dict lookup
"""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# -- Module-level cache ------------------------------------------
_config_cache: dict[str, dict[str, Any]] = {}


def load_yaml_config(config_path: str) -> dict[str, Any]:
    """Load a YAML quiz config file, cached in memory by absolute path.

    Args:
        config_path: Absolute or relative path to the YAML config file.

    Returns:
        Parsed config dict, or empty dict on failure.
    """
    abs_path = os.path.abspath(config_path)
    if abs_path in _config_cache:
        return _config_cache[abs_path]

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            config = loaded if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning("Failed to load quiz config from %s: %s", abs_path, e)
        config = {}

    _config_cache[abs_path] = config
    return config


def get_questions_raw(config_path: str) -> list[dict[str, Any]]:
    """Return raw question bank from a YAML config file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        List of raw question dicts.
    """
    config = load_yaml_config(config_path)
    return config.get("questions", [])


def normalize_questions(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert options from YAML lists to tuples (mutates in place and returns).

    Args:
        raw: List of raw question dicts.

    Returns:
        The same list with options converted to tuples.
    """
    for q in raw:
        if "options" in q:
            q["options"] = [tuple(opt) if isinstance(opt, list) else opt for opt in q["options"]]
    return raw


def build_question_map(raw: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build a question_id -> question dict lookup map.

    Args:
        raw: List of raw question dicts.

    Returns:
        Dict mapping question id to question dict.
    """
    return {q["id"]: q for q in raw}


def get_config_path(*parts: str) -> str:
    """Build an absolute config path relative to the project root.

    Convenience: get_config_path("subdir", "file.yaml") resolves to
    <project_root>/subdir/file.yaml where project root is 3 levels
    up from this file (src/services/).

    Args:
        *parts: Path parts joined after the project root.

    Returns:
        Absolute path string.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(project_root, *parts)
