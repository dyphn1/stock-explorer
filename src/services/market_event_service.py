"""股識 Stock Explorer — C84 市場事件案例研究服務 + C147 歷史事件模式服務
讀取 case_studies.yaml（C84）與 events.yaml（C147），提供事件查詢 API。
"""
from __future__ import annotations

import os
import yaml

_data_dir = os.path.dirname(__file__)

# ── C84: Case Study Data ──────────────────────────────────

_case_studies_path = os.path.join(_data_dir, "..", "data", "case_studies.yaml")
with open(_case_studies_path, "r", encoding="utf-8") as f:
    _CASE_STUDIES: list[dict] = yaml.safe_load(f) or []

# ── C147: Historical Event Data ───────────────────────────

_events_path = os.path.join(_data_dir, "..", "data", "events.yaml")
with open(_events_path, "r", encoding="utf-8") as f:
    _EVENTS: list[dict] = yaml.safe_load(f).get("events", [])


# ── C84 Public API ────────────────────────────────────────

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


def get_events_for_stock_c84(stock_id: str) -> list[dict]:
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


# ── C147 Public API ───────────────────────────────────────

def get_events_for_stock(stock_id: str) -> list[dict]:
    """回傳指定股票的所有歷史事件。"""
    return [e for e in _EVENTS if e["stock_id"] == stock_id]


def get_events_by_type(stock_id: str, event_type: str) -> list[dict]:
    """回傳指定股票、指定類型的歷史事件。"""
    return [
        e for e in _EVENTS
        if e["stock_id"] == stock_id and e["type"] == event_type
    ]


def get_event_types_for_stock(stock_id: str) -> list[str]:
    """回傳指定股票有哪些事件類型（去重）。"""
    types = {e["type"] for e in _EVENTS if e["stock_id"] == stock_id}
    return sorted(types)


def get_all_events() -> list[dict]:
    """回傳所有歷史事件。"""
    return list(_EVENTS)
