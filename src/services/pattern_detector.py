"""股識 Stock Explorer — C147 歷史模式偵測器
純 Python 服務，無 Streamlit 依賴。
"""
from __future__ import annotations

from dataclasses import dataclass, field

from src.services.market_event_service import (
    get_events_by_type,
    get_event_types_for_stock,
)


@dataclass
class HistoricalPattern:
    """單一歷史模式匹配結果。"""
    event_type: str
    date: str
    description: str
    outcome: str
    outcome_direction: str  # "positive" | "negative" | "mixed"


@dataclass
class PatternResult:
    """模式偵測結果。"""
    stock_id: str
    event_type: str
    matches: list[HistoricalPattern] = field(default_factory=list)
    outcome_summary: str = ""
    has_data: bool = False


def detect_patterns(stock_id: str, event_type: str) -> PatternResult:
    """搜尋歷史中相似事件的模式。

    Args:
        stock_id: 股票代碼
        event_type: 事件類型（如 "財報亮眼"、"回檔後反彈"）

    Returns:
        PatternResult 包含所有匹配的歷史事件
    """
    result = PatternResult(stock_id=stock_id, event_type=event_type)

    raw_events = get_events_by_type(stock_id, event_type)

    if not raw_events:
        return result

    for evt in raw_events:
        result.matches.append(HistoricalPattern(
            event_type=evt["type"],
            date=evt["date"],
            description=evt["description"],
            outcome=evt["outcome"],
            outcome_direction=evt.get("outcome_direction", "mixed"),
        ))

    result.outcome_summary = _build_outcome_summary(result.matches)
    result.has_data = True
    return result


def get_available_types(stock_id: str) -> list[str]:
    """取得指定股票可用的歷史事件類型。"""
    return get_event_types_for_stock(stock_id)


def _build_outcome_summary(matches: list[HistoricalPattern]) -> str:
    """根據多筆歷史結果建立摘要描述。"""
    if not matches:
        return ""

    positive = sum(1 for m in matches if m.outcome_direction == "positive")
    negative = sum(1 for m in matches if m.outcome_direction == "negative")
    mixed = sum(1 for m in matches if m.outcome_direction == "mixed")
    total = len(matches)

    parts: list[str] = []
    if positive > 0:
        parts.append(f"{positive} 次偏向正面")
    if mixed > 0:
        parts.append(f"{mixed} 次結果不一")
    if negative > 0:
        parts.append(f"{negative} 次偏向負面")

    if not parts:
        return f"共 {total} 筆歷史記錄"

    return f"歷史共 {total} 次類似事件：{'、'.join(parts)}"
