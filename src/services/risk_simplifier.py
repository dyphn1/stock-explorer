"""
風險簡化器 — 1-5 風險等級
將複雜的風險分析結果轉換為新手友善的 1-5 級風險指標
"""

from src.services.risk_analyzer import assess_risk
from src.services.health_scoring import compute_health_scores


def get_risk_level(data: dict) -> dict:
    """
    根據風險分析與健康評分，產生 1-5 級簡化風險指標。

    Args:
        data: 公司名片資料 dict（與 business card 使用相同格式）

    Returns:
        {
            "level": 1-5,
            "label": "非常低風險"/"低風險"/"中等風險"/"高風險"/"非常高風險",
            "emoji": "🟢"/"🟢"/"🟡"/"🟠"/"🔴",
            "description": "白話說明"
        }
    """
    extra_metrics = data.get("extra_metrics") or {}
    latest_per_pbr = data.get("latest_per_pbr")
    financial = data.get("financial")
    monthly_revenue = data.get("monthly_revenue")

    # ── Get health scores ──
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    health_avg = sum(health_scores.values()) / len(health_scores) if health_scores else 50.0

    # ── Get risk assessment ──
    risk = assess_risk(data)

    # Collect risk dimension levels
    dim_levels = []
    for dim_key in ("customer_concentration", "financial_health", "event_based"):
        dim = risk.get(dim_key)
        if dim is not None:
            dim_levels.append(dim.get("risk_level", "low"))

    high_count = dim_levels.count("high")
    medium_count = dim_levels.count("medium")
    all_low = all(d == "low" for d in dim_levels) if dim_levels else True
    any_high = high_count >= 1

    # ── Determine 1-5 level ──
    # Level 5 (very high): multiple high risk dims
    if high_count >= 2:
        level = 5
    # Level 4 (high): any high risk dim OR health avg < 30
    elif any_high or health_avg < 30:
        level = 4
    # Level 1 (very low): all risk dims low AND health avg >= 70
    elif all_low and health_avg >= 70:
        level = 1
    # Level 2 (low): all risk dims low-medium AND health avg >= 50
    elif all_low and health_avg >= 50:
        level = 2
    # Level 3 (medium): mixed risk OR health avg 30-50
    else:
        level = 3

    # ── Labels ──
    _LABELS = {
        1: {"label": "非常低風險", "emoji": "🟢"},
        2: {"label": "低風險", "emoji": "🟢"},
        3: {"label": "中等風險", "emoji": "🟡"},
        4: {"label": "高風險", "emoji": "🟠"},
        5: {"label": "非常高風險", "emoji": "🔴"},
    }

    # ── Generate plain-language description ──
    if level == 1:
        description = (
            f"這家公司目前風險很低，財務健康狀況良好（平均 {health_avg:.0f} 分）。"
            f"各項風險指標都在安全範圍內，適合保守型投資人關注。"
        )
    elif level == 2:
        description = (
            f"這家公司風險偏低，財務健康狀況尚可（平均 {health_avg:.0f} 分）。"
            f"雖然有些小地方可以留意，但整體來說問題不大。"
        )
    elif level == 3:
        weak_dims = [name for name, score in health_scores.items() if score < 40]
        if weak_dims:
            description = (
                f"這家公司有中等程度的風險，財務健康狀況普通（平均 {health_avg:.0f} 分）。"
                f"其中 {'、'.join(weak_dims)} 面向需要特別留意。"
            )
        else:
            description = (
                f"這家公司有中等程度的風險，財務健康狀況普通（平均 {health_avg:.0f} 分）。"
                f"部分指標表現不均，建議持續觀察。"
            )
    elif level == 4:
        description = (
            f"這家公司風險較高，財務健康狀況偏弱（平均 {health_avg:.0f} 分）。"
            f"有明顯的高風險面向，投資前請做好功課並評估自身風險承受能力。"
        )
    else:  # level 5
        description = (
            f"這家公司風險非常高，財務健康狀況較差（平均 {health_avg:.0f} 分）。"
            f"多個風險指標亮紅燈，建議謹慎評估，不適合風險承受度較低的投資人。"
        )

    return {
        "level": level,
        "label": _LABELS[level]["label"],
        "emoji": _LABELS[level]["emoji"],
        "description": description,
    }
