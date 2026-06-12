"""
Financial Wellness Service — C85
Behavioral finance self-assessment quiz logic.
No streamlit imports.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Question bank ──────────────────────────────────────────

_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "emergency_fund",
        "text": "你有沒有準備緊急預備金（至少 3 個月的生活費）？",
        "options": [
            ("a", "有，超過 6 個月", 4),
            ("b", "有，大約 3-6 個月", 3),
            ("c", "有一點，但不到 3 個月", 2),
            ("d", "完全沒有", 1),
        ],
    },
    {
        "id": "investment_horizon",
        "text": "你預計這筆投資資金可以放多久？",
        "options": [
            ("a", "5 年以上", 4),
            ("b", "3-5 年", 3),
            ("c", "1-3 年", 2),
            ("d", "不到 1 年", 1),
        ],
    },
    {
        "id": "loss_reaction",
        "text": "如果你的投資在一個月內下跌 20%，你會怎麼做？",
        "options": [
            ("a", "冷靜持有，甚至考慮加碼", 4),
            ("b", "先觀察，等情況明朗", 3),
            ("c", "有點焦慮，考慮賣掉部分", 2),
            ("d", "立刻全部賣掉", 1),
        ],
    },
    {
        "id": "diversification",
        "text": "你的投資組合分散程度如何？",
        "options": [
            ("a", "分散在不同產業和資產類型", 4),
            ("b", "有分散在 2-3 個不同產業", 3),
            ("c", "集中在同一個產業", 2),
            ("d", "全部壓在單一股票", 1),
        ],
    },
    {
        "id": "debt_management",
        "text": "你目前的負債狀況（房貸、信用卡、學貸等）？",
        "options": [
            ("a", "沒有負債，或負債比率很低", 4),
            ("b", "有負債但每月還款很輕鬆", 3),
            ("c", "負債壓力有點大", 2),
            ("d", "每月還款很吃力", 1),
        ],
    },
    {
        "id": "financial_goals",
        "text": "你有沒有明確的理財目標？",
        "options": [
            ("a", "有，而且有具體計畫和時間表", 4),
            ("b", "有大致方向，但還沒細化", 3),
            ("c", "想過但沒有具體行動", 2),
            ("d", "沒有特別想過", 1),
        ],
    },
    {
        "id": "risk_tolerance",
        "text": "你對投資風險的態度是？",
        "options": [
            ("a", "願意承擔較高風險換取較高報酬", 4),
            ("b", "可接受中等風險", 3),
            ("c", "偏好低風險，報酬少一點沒關係", 2),
            ("d", "完全不能接受虧損", 1),
        ],
    },
    {
        "id": "investment_knowledge",
        "text": "你對投資理財的了解程度？",
        "options": [
            ("a", "有深入研究，能獨立分析", 4),
            ("b", "有基本概念，能理解財報", 3),
            ("c", "略懂一些術語", 2),
            ("d", "幾乎不了解", 1),
        ],
    },
    {
        "id": "review_frequency",
        "text": "你多久檢視一次自己的投資組合？",
        "options": [
            ("a", "定期檢視（每季或每月）", 4),
            ("b", "半年左右看一次", 3),
            ("c", "想到才看", 2),
            ("d", "幾乎不看", 1),
        ],
    },
    {
        "id": "emotional_control",
        "text": "看到市場大漲或大跌時，你的反應是？",
        "options": [
            ("a", "保持冷靜，按原定計畫執行", 4),
            ("b", "有點波動但能控制", 3),
            ("c", "情緒會受影響，可能衝動決策", 2),
            ("d", "非常焦慮，容易跟風操作", 1),
        ],
    },
]

# Category mapping for tips
_CATEGORY_MAP: dict[str, str] = {
    "emergency_fund": "財務安全網",
    "investment_horizon": "投資時間觀",
    "loss_reaction": "風險承受力",
    "diversification": "分散投資",
    "debt_management": "負債管理",
    "financial_goals": "理財目標",
    "risk_tolerance": "風險態度",
    "investment_knowledge": "投資知識",
    "review_frequency": "定期檢視",
    "emotional_control": "情緒管理",
}

# Tips per category (shown when score is low)
_CATEGORY_TIPS: dict[str, str] = {
    "emergency_fund": "建議先存夠 3-6 個月的生活費作為緊急預備金，再開始投資。這是理財的第一道防線。",
    "investment_horizon": "投資時間越長，越能承受短期波動。建議先確認資金用途，再決定投資期限。",
    "loss_reaction": "市場波動是正常的。建議在投資前先想好「如果下跌 20% 我會怎麼做」，避免衝動決策。",
    "diversification": "不要把雞蛋放在同一個籃子裡。可以考慮用 ETF 來達到產業分散。",
    "debt_management": "高利率負債（如信用卡循環利息）會侵蝕投資報酬。建議優先還清高利率債務。",
    "financial_goals": "明確的目標能幫助你堅持下去。試著寫下「我想在 X 年後達成 Y」。",
    "risk_tolerance": "了解自己的風險承受度，才能選擇適合的投資工具。沒有最好的投資，只有最適合的。",
    "investment_knowledge": "投資自己永遠最值得。建議從基礎理財書籍或課程開始，慢慢累積知識。",
    "review_frequency": "定期檢視能幫助你及時調整策略，但過度關注短期波動反而會增加焦慮。",
    "emotional_control": "制定投資計畫並嚴格執行，是克服情緒化決策的最佳方式。",
}


def get_questions() -> list[dict[str, Any]]:
    """Return the list of quiz questions.

    Each question dict has keys:
        id, text, options: list of (key, label, score)
    """
    return _QUESTIONS


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
    question_map = {q["id"]: q for q in _QUESTIONS}
    total = 0
    category_scores: dict[str, int] = {}

    for qid, opt_key in answers.items():
        q = question_map.get(qid)
        if not q:
            continue
        for key, _label, score in q["options"]:
            if key == opt_key:
                total += score
                cat = _CATEGORY_MAP.get(qid, qid)
                category_scores[cat] = score
                break

    max_score = len(_QUESTIONS) * 4
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
    result = calculate_score(answers)
    weak = result["weak_areas"][:3]
    tips = []
    for cat in weak:
        # Find question_id from category name
        qid = None
        for k, v in _CATEGORY_MAP.items():
            if v == cat:
                qid = k
                break
        tip_text = _CATEGORY_TIPS.get(qid, f'"{cat}" 是你最需要加強的部分，建議多了解相關知識。')
        tips.append({"category": cat, "tip": tip_text})
    return tips
