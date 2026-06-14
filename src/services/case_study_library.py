"""股識 Stock Explorer — C140 歷史案例研究圖書館服務
讀取 case_studies_library.yaml，提供搜尋與篩選 API。
"""
from __future__ import annotations

import os
import yaml

_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
_library_path = os.path.join(_data_dir, "case_studies_library.yaml")

with open(_library_path, "r", encoding="utf-8") as f:
    _LIBRARY: dict = yaml.safe_load(f) or {}

_CASE_STUDIES: list[dict] = _LIBRARY.get("case_studies", [])


def get_all_case_studies() -> list[dict]:
    """回傳所有案例研究（完整資料）。"""
    return list(_CASE_STUDIES)


def get_case_study_by_id(study_id: str) -> dict | None:
    """依 id 回傳單一案例研究。"""
    for cs in _CASE_STUDIES:
        if cs["id"] == study_id:
            return cs
    return None


def get_all_industries() -> list[str]:
    """回傳所有不重複的產業列表（排序後）。"""
    industries = {cs["industry"] for cs in _CASE_STUDIES}
    return sorted(industries)


def get_all_topic_tags() -> list[str]:
    """回傳所有不重複的主題標籤（排序後）。"""
    tags: set[str] = set()
    for cs in _CASE_STUDIES:
        for tag in cs.get("topic_tags", []):
            tags.add(tag)
    return sorted(tags)


def filter_case_studies(
    industry: str | None = None,
    topic_tag: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    """依條件篩選案例研究。

    Args:
        industry: 產業名稱（完全比對）。
        topic_tag: 主題標籤（部分比對，存在任一標籤即符合）。
        date_from: 起始日期（含），格式 YYYY 或 YYYY-MM。
        date_to: 結束日期（含），格式 YYYY 或 YYYY-MM。

    Returns:
        符合條件的案例研究列表。
    """
    results = list(_CASE_STUDIES)

    if industry and industry != "全部":
        results = [cs for cs in results if cs["industry"] == industry]

    if topic_tag and topic_tag != "全部":
        results = [
            cs for cs in results
            if topic_tag in cs.get("topic_tags", [])
        ]

    if date_from:
        results = [
            cs for cs in results
            if _date_overlap(cs["date"], date_from, date_to)
        ]

    return results


def _date_overlap(
    cs_date: str,
    date_from: str | None,
    date_to: str | None,
) -> bool:
    """檢查案例日期範圍是否與篩選範圍有重疊。"""
    # 解析案例日期（可能為 "2020-2021" 或 "2022" 格式）
    cs_parts = cs_date.split("-")
    cs_start = int(cs_parts[0])
    cs_end = int(cs_parts[1]) if len(cs_parts) > 1 else cs_start

    if date_from:
        from_year = int(date_from[:4])
    else:
        from_year = 0

    if date_to:
        to_year = int(date_to[:4])
    else:
        to_year = 9999

    # 檢查是否有重疊
    return cs_start <= to_year and cs_end >= from_year
