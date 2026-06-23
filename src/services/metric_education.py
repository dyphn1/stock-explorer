"""
Metric Education Service
將財務指標轉化為新手能秒懂的解釋 + 比喻
No Streamlit imports — pure data service.
"""

from src.services.analogy_engine import (
    get_roe_analogy,
    get_gross_margin_analogy,
    get_per_analogy,
    get_pbr_analogy,
    get_dividend_analogy,
    get_debt_ratio_analogy,
    get_yoy_analogy,
)

from src.core.i18n import t

# ── Metric registry ──────────────────────────────────────
# Each entry: (display_name, unit, is_higher_better, explanation_template, analogy_fn, historical_context)
_METRIC_REGISTRY: dict[str, dict] = {
    "ROE": {
        "display_name": t('metric_education.roe_display_name'),
        "unit": "%",
        "is_higher_better": True,
        "explanation": t('metric_education.roe_explanation'),
        "analogy_fn": get_roe_analogy,
        "historical_context": t('metric_education.roe_historical_context'),
    },
    "gross_margin": {
        "display_name": t('metric_education.gross_margin_display_name'),
        "unit": "%",
        "is_higher_better": True,
        "explanation": t('metric_education.gross_margin_explanation'),
        "analogy_fn": get_gross_margin_analogy,
        "historical_context": t('metric_education.gross_margin_historical_context'),
    },
    "net_margin": {
        "display_name": t('metric_education.net_margin_display_name'),
        "unit": "%",
        "is_higher_better": True,
        "explanation": t('metric_education.net_margin_explanation'),
        "analogy_fn": lambda val: (
            t("metric_education.net_margin_analogy_high", val=val) if val >= 15
            else t("metric_education.net_margin_analogy_mid", val=val) if val >= 5
            else t("metric_education.net_margin_analogy_low", val=val)
        ),
        "historical_context": t('metric_education.net_margin_historical_context'),
    },
    "debt_ratio": {
        "display_name": t('metric_education.debt_ratio_display_name'),
        "unit": "%",
        "is_higher_better": False,
        "explanation": t('metric_education.debt_ratio_explanation'),
        "analogy_fn": get_debt_ratio_analogy,
        "historical_context": t('metric_education.debt_ratio_historical_context'),
    },
    "revenue_yoy": {
        "display_name": t('metric_education.revenue_yoy_display_name'),
        "unit": "%",
        "is_higher_better": True,
        "explanation": t('metric_education.revenue_yoy_explanation'),
        "analogy_fn": get_yoy_analogy,
        "historical_context": t('metric_education.revenue_yoy_historical_context'),
    },
    "PER": {
        "display_name": t('metric_education.per_display_name'),
        "unit": "倍",
        "is_higher_better": False,
        "explanation": t('metric_education.per_explanation'),
        "analogy_fn": get_per_analogy,
        "historical_context": t('metric_education.per_historical_context'),
    },
    "PBR": {
        "display_name": t('metric_education.pbr_display_name'),
        "unit": "倍",
        "is_higher_better": False,
        "explanation": t('metric_education.pbr_explanation'),
        "analogy_fn": get_pbr_analogy,
        "historical_context": t('metric_education.pbr_historical_context'),
    },
    "dividend_yield": {
        "display_name": t('metric_education.dividend_yield_display_name'),
        "unit": "%",
        "is_higher_better": True,
        "explanation": t('metric_education.dividend_yield_explanation'),
        "analogy_fn": get_dividend_analogy,
        "historical_context": t('metric_education.dividend_yield_historical_context'),
    },
}
def get_metric_explanation(metric_name: str, value: float, stock_id: str) -> dict:
    """
    取得單一財務指標的完整解釋。

    Args:
        metric_name: 指標代碼（如 "ROE", "gross_margin", "PER" 等）
        value: 指標數值
        stock_id: 股票代號（用於未來擴展，如提供同業比較）

    Returns:
        dict with keys:
            - explanation: 白話解釋（10 秒內能理解）
            - analogy: 生活化比喻
            - is_higher_better: True 代表越高越好
            - historical_context: 歷史/產業背景
            - display_name: 指標中文名稱
            - unit: 單位
            - value: 原始數值
    """
    entry = _METRIC_REGISTRY.get(metric_name)
    if entry is None:
        return {
            "explanation": t("metric_education.fallback.explanation", metric_name=metric_name),
            "analogy": t("metric_education.fallback.analogy"),
            "is_higher_better": True,
            "historical_context": t("metric_education.fallback.historical_context"),
            "display_name": metric_name,
            "unit": "",
            "value": value,
        }

    analogy_fn = entry["analogy_fn"]
    try:
        analogy = analogy_fn(value)
    except Exception:
        analogy = t("metric_education.analogy_error")

    return {
        "explanation": entry["explanation"],
        "analogy": analogy,
        "is_higher_better": entry["is_higher_better"],
        "historical_context": entry["historical_context"],
        "display_name": entry["display_name"],
        "unit": entry["unit"],
        "value": value,
    }


def get_supported_metrics() -> list[str]:
    """回傳支援的指標代碼列表。"""
    return list(_METRIC_REGISTRY.keys())


def get_top_metrics_for_education(data: dict) -> list[dict]:
    """
    從股票資料中選出最重要的 3 個指標用於教育展示。

    優先順序：ROE > 毛利率 > 本益比 > 殖利率 > 負債比 > 營收年增率 > 淨值比 > 淨利率

    Args:
        data: 從 get_stock_data() 回傳的 dict

    Returns:
        list of dicts, each with keys: metric_name, value, explanation_dict
        最多 3 個
    """
    extra_metrics = data.get("extra_metrics", {})
    latest_per_pbr = data.get("latest_per_pbr")

    # 優先順序
    priority_order = [
        ("ROE", "roe"),
        ("gross_margin", "gross_margin"),
        ("PER", None),  # 從 latest_per_pbr 取值
        ("dividend_yield", None),  # 從 latest_per_pbr 取值
        ("debt_ratio", "debt_ratio"),
        ("revenue_yoy", "revenue_yoy"),
        ("PBR", None),  # 從 latest_per_pbr 取值
        ("net_margin", "net_margin"),
    ]

    stock_id = data.get("stock_id", "")
    results = []

    for metric_name, extra_key in priority_order:
        if len(results) >= 3:
            break

        value = None
        if extra_key and extra_metrics.get(extra_key) is not None:
            value = extra_metrics[extra_key]
        elif latest_per_pbr and metric_name in ("PER", "PBR", "dividend_yield"):
            value = latest_per_pbr.get(metric_name)

        if value is not None:
            explanation = get_metric_explanation(metric_name, float(value), stock_id)
            results.append({
                "metric_name": metric_name,
                "value": float(value),
                "explanation": explanation,
            })

    return results