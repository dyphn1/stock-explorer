"""
股識 Stock Explorer — C84 市場事件案例研究服務
Hardcoded educational case studies for historical market events.
"""

from __future__ import annotations

import os
import yaml

# ── Case Study Data ──────────────────────────────────────

_data_dir = os.path.dirname(__file__)
_yaml_path = os.path.join(_data_dir, "..", "data", "case_studies.yaml")

with open(_yaml_path, "r", encoding="utf-8") as f:
    _CASE_STUDIES: list[dict] = yaml.safe_load(f) or []


# ── Public API ──────────────────────────────────────────

def get_case_studies() -> list[dict]:
    """Returns list of all case studies (summary info only)."""
    return [
        {
            "id": cs["id"],
            "title": cs["title"],
            "date": cs["date"],
            "summary": cs["summary"],
            "severity": cs["severity"],
        }
        for cs in _CASE_STUDIES
    ]


def get_case_study(event_id: str) -> dict | None:
    """Returns a single case study with full details by event_id."""
    for cs in _CASE_STUDIES:
        if cs["id"] == event_id:
            return cs
    return None


def get_events_for_stock(stock_id: str) -> list[dict]:
    """Returns case studies that mention a specific stock."""
    results = []
    for cs in _CASE_STUDIES:
        related_ids = [s["stock_id"] for s in cs.get("related_stocks", [])]
        if stock_id in related_ids:
            results.append(
                {
                    "id": cs["id"],
                    "title": cs["title"],
                    "date": cs["date"],
                    "severity": cs["severity"],
                }
            )
    return results
