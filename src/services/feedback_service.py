"""Feedback service — binary thumbs up/down feedback with JSONL storage.

Stores feedback entries as JSONL lines in a local file.
Each entry includes: timestamp, stock_id, section, feedback_type, context.

Note: This module is part of the service layer and has no UI framework dependency.
      Session-state deduplication is handled by the caller.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

# Default feedback file path (relative to project root)
DEFAULT_FEEDBACK_PATH = Path("data/feedback.jsonl")


def _feedback_path() -> Path:
    """Return the feedback file path, creating parent dirs if needed."""
    path = DEFAULT_FEEDBACK_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def record_feedback(
    stock_id: str,
    feedback_type: str,
    section: str | None = None,
    context: str | None = None,
) -> dict:
    """Record a single feedback entry as a JSONL line.

    Args:
        stock_id: The stock identifier (e.g. "2330").
        feedback_type: "up" for 👍 or "down" for 👎.
        section: Optional section name the feedback applies to.
        context: Optional free-form context string.

    Returns:
        The feedback entry dict that was written.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stock_id": stock_id,
        "feedback_type": feedback_type,
    }
    if section is not None:
        entry["section"] = section
    if context is not None:
        entry["context"] = context

    path = _feedback_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry


def get_feedback_count(stock_id: str) -> dict:
    """Return 👍/👎 counts for a given stock_id from the JSONL file.

    Args:
        stock_id: The stock identifier to query.

    Returns:
        Dict with keys "up" and "down" mapping to int counts.
    """
    counts = {"up": 0, "down": 0}
    path = _feedback_path()
    if not path.exists():
        return counts

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if entry.get("stock_id") == stock_id:
                ft = entry.get("feedback_type")
                if ft in counts:
                    counts[ft] += 1

    return counts
