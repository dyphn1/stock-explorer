"""
健康評分（Health Scoring）模組
五維度財務健康評分與摘要
"""

from src.services.financial_metrics import extract_quarterly_eps

import yaml
from pathlib import Path


def _score_roe(roe: float) -> float:
    """ROE 評分：≥20→100, ≥15→80, ≥10→60, ≥5→40, ≥0→20, <0→0"""
    if roe >= 20:
        return 100.0
    elif roe >= 15:
        return 80.0
    elif roe >= 10:
        return 60.0
    elif roe >= 5:
        return 40.0
    elif roe >= 0:
        return 20.0
    else:
        return 0.0


def _score_gross_margin(gross_margin: float, industry_avg: float = 30.0) -> float:
    """毛利率評分：產業相對（above avg→80-100, avg→50-70, below avg→0-40）"""
    if gross_margin >= industry_avg * 1.2:
        return min(100.0, 80.0 + (gross_margin - industry_avg * 1.2) / (industry_avg * 0.3) * 20.0)
    elif gross_margin >= industry_avg:
        ratio = (gross_margin - industry_avg) / (industry_avg * 0.2)
        return 50.0 + ratio * 20.0
    else:
        ratio = max(0.0, gross_margin / industry_avg)
        return ratio * 50.0


def _score_revenue_yoy(yoy: float) -> float:
    """營收年增率評分：≥30→100, ≥15→80, ≥5→60, ≥0→40, <0→0-30"""
    if yoy >= 30:
        return 100.0
    elif yoy >= 15:
        return 80.0 + (yoy - 15) / 15 * 20.0
    elif yoy >= 5:
        return 60.0 + (yoy - 5) / 10 * 20.0
    elif yoy >= 0:
        return 40.0 + yoy / 5 * 20.0
    else:
        return max(0.0, 40.0 + yoy / 30.0 * 40.0)


def _score_debt_ratio(debt_ratio: float) -> float:
    """負債比評分：≤30→100, ≤50→80, ≤70→50, >70→20"""
    if debt_ratio <= 30:
        return 100.0
    elif debt_ratio <= 50:
        return 80.0 + (50.0 - debt_ratio) / 20.0 * 20.0
    elif debt_ratio <= 70:
        return 50.0 + (70.0 - debt_ratio) / 20.0 * 30.0
    else:
        return max(0.0, 20.0 - (debt_ratio - 70.0) / 30.0 * 20.0)


def _score_dividend_yield(dy: float) -> float:
    """殖利率評分：≥5→100, ≥3→75, ≥1→50, >0→30, 0→10"""
    if dy >= 5:
        return 100.0
    elif dy >= 3:
        return 75.0 + (dy - 3) / 2.0 * 25.0
    elif dy >= 1:
        return 50.0 + (dy - 1) / 2.0 * 25.0
    elif dy > 0:
        return 30.0 + dy / 1.0 * 20.0
    else:
        return 10.0


def _score_valuation(per: float, pbr: float) -> float:
    """
    估值合理性評分：PER/PBR 越接近合理範圍越高分
    PER 合理範圍 10-20，PBR 合理範圍 1-2
    """
    if per is None or per <= 0:
        per_score = 15.0
    elif per <= 10:
        per_score = 80.0 + (10.0 - per) / 10.0 * 20.0
    elif per <= 20:
        per_score = 60.0 + (20.0 - per) / 10.0 * 20.0
    elif per <= 30:
        per_score = 40.0 + (30.0 - per) / 10.0 * 20.0
    elif per <= 40:
        per_score = 20.0 + (40.0 - per) / 10.0 * 20.0
    else:
        per_score = max(0.0, 20.0 - (per - 40.0) / 20.0 * 20.0)

    if pbr is None or pbr <= 0:
        pbr_score = 15.0
    elif pbr <= 1:
        pbr_score = 70.0 + pbr / 1.0 * 30.0
    elif pbr <= 2:
        pbr_score = 50.0 + (2.0 - pbr) / 1.0 * 20.0
    elif pbr <= 3:
        pbr_score = 30.0 + (3.0 - pbr) / 1.0 * 20.0
    elif pbr <= 5:
        pbr_score = 10.0 + (5.0 - pbr) / 2.0 * 20.0
    else:
        pbr_score = max(0.0, 10.0 - (pbr - 5.0) / 5.0 * 10.0)

    return (per_score + pbr_score) / 2.0


def compute_health_scores(
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    financial_df,
    monthly_revenue,
) -> dict:
    """
    計算公司健康狀況五維度評分（C43）

    Args:
        extra_metrics: dict，包含 gross_margin, net_margin, roe, debt_ratio, revenue_yoy 等
        latest_per_pbr: dict，包含 PER, PBR, dividend_yield
        financial_df: DataFrame，季度財務資料
        monthly_revenue: DataFrame，月營收資料

    回傳 dict：{
        "獲利能力": 0-100,
        "成長性": 0-100,
        "財務健康": 0-100,
        "股利品質": 0-100,
        "估值合理性": 0-100,
    }
    """
    # 1. 獲利能力（Profitability）：ROE + 毛利率 + 淨利率
    roe = extra_metrics.get("roe")
    gross_margin = extra_metrics.get("gross_margin")
    net_margin = extra_metrics.get("net_margin")

    roe_score = _score_roe(roe) if roe is not None else 50.0
    gm_score = _score_gross_margin(gross_margin) if gross_margin is not None else 50.0

    if net_margin is not None:
        if net_margin >= 20:
            nm_score = 100.0
        elif net_margin >= 10:
            nm_score = 75.0
        elif net_margin >= 5:
            nm_score = 55.0
        elif net_margin >= 0:
            nm_score = 35.0
        else:
            nm_score = 10.0
    else:
        nm_score = 50.0

    profitability = roe_score * 0.4 + gm_score * 0.35 + nm_score * 0.25

    # 2. 成長性（Growth）：營收年增率 + EPS 成長
    revenue_yoy = extra_metrics.get("revenue_yoy")
    growth_score = _score_revenue_yoy(revenue_yoy) if revenue_yoy is not None else 50.0

    eps_growth_score = 50.0
    if financial_df is not None and len(financial_df) >= 2:
        try:
            eps_df = extract_quarterly_eps(financial_df)
            if eps_df is not None and len(eps_df) >= 2:
                latest_eps = eps_df.iloc[-1]["value"]
                prev_eps = eps_df.iloc[-2]["value"]
                if prev_eps > 0:
                    eps_growth = (latest_eps - prev_eps) / prev_eps * 100
                    eps_growth_score = _score_revenue_yoy(eps_growth)
        except Exception:
            eps_growth_score = 50.0

    growth = growth_score * 0.6 + eps_growth_score * 0.4

    # 3. 財務健康（Financial Health）：負債比 + 流動比
    debt_ratio = extra_metrics.get("debt_ratio")
    debt_score = _score_debt_ratio(debt_ratio) if debt_ratio is not None else 50.0

    current_ratio = extra_metrics.get("current_ratio")
    if current_ratio is not None:
        if current_ratio >= 2:
            current_score = 90.0
        elif current_ratio >= 1.5:
            current_score = 75.0
        elif current_ratio >= 1:
            current_score = 55.0
        else:
            current_score = 30.0
    else:
        current_score = 60.0

    financial_health = debt_score * 0.6 + current_score * 0.4

    # 4. 股利品質（Dividend Quality）：殖利率 + 配息穩定性
    if latest_per_pbr and latest_per_pbr.get("dividend_yield") is not None:
        dy = latest_per_pbr["dividend_yield"]
        dy_score = _score_dividend_yield(dy)
    else:
        dy_score = 10.0

    dividend_stability = 60.0
    if monthly_revenue is not None and len(monthly_revenue) >= 12:
        try:
            recent_12 = monthly_revenue.tail(12)["revenue"]
            cv = recent_12.std() / recent_12.mean() if recent_12.mean() > 0 else 1.0
            if cv <= 0.1:
                dividend_stability = 95.0
            elif cv <= 0.2:
                dividend_stability = 80.0
            elif cv <= 0.3:
                dividend_stability = 65.0
            else:
                dividend_stability = 45.0
        except Exception:
            dividend_stability = 60.0

    dividend_quality = dy_score * 0.6 + dividend_stability * 0.4

    # 5. 估值合理性（Valuation）：PER + PBR
    per = latest_per_pbr.get("PER") if latest_per_pbr else None
    pbr = latest_per_pbr.get("PBR") if latest_per_pbr else None
    valuation = _score_valuation(per, pbr)

    return {
        "獲利能力": round(profitability, 1),
        "成長性": round(growth, 1),
        "財務健康": round(financial_health, 1),
        "股利品質": round(dividend_quality, 1),
        "估值合理性": round(valuation, 1),
    }


def get_health_summary(health_scores: dict) -> str:
    """
    根據五維度評分產生白話健康摘要（C43）

    回傳中文（zh-TW）的健康摘要字串。
    """
    if not health_scores:
        return "整體健康狀況：無法評估"

    values = list(health_scores.values())
    avg = sum(values) / len(values)

    sorted_dims = sorted(health_scores.items(), key=lambda x: x[1], reverse=True)

    if avg >= 70:
        status = "良好"
        emoji = "🟢"
    elif avg >= 40:
        status = "普通"
        emoji = "🟡"
    else:
        status = "需關注"
        emoji = "🔴"

    weak_dims = [name for name, score in health_scores.items() if score < 40]
    strong_dims = [name for name, score in health_scores.items() if score >= 70]

    parts = [f"{emoji} 整體健康狀況：{status}（平均 {avg:.0f} 分）"]

    if strong_dims:
        parts.append(f"💪 表現較佳：{'、'.join(strong_dims)}")
    if weak_dims:
        parts.append(f"⚠️ 需要留意：{'、'.join(weak_dims)}")

    return "\n".join(parts)
