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

# ── Metric registry ────────────────────────────────────────
# Each entry: (display_name, unit, is_higher_better, explanation_template, analogy_fn, historical_context)
_METRIC_REGISTRY: dict[str, dict] = {
    "ROE": {
        "display_name": "ROE（股東權益報酬率）",
        "unit": "%",
        "is_higher_better": True,
        "explanation": (
            "ROE 衡量公司用股東的錢賺錢的效率。"
            "ROE 15% 表示每 100 元股東資本，公司一年賺 15 元。"
            "越高代表公司越會賺錢。"
        ),
        "analogy_fn": get_roe_analogy,
        "historical_context": (
            "台股平均 ROE 約 10-12%。ROE 長期維持 15% 以上的公司通常具備競爭優勢（護城河）。"
            "巴菲特偏好 ROE 長期高於 20% 的公司。"
        ),
    },
    "gross_margin": {
        "display_name": "毛利率",
        "unit": "%",
        "is_higher_better": True,
        "explanation": (
            "毛利率是賣出商品後，扣掉直接成本（原料、人工）剩下的利潤比例。"
            "毛利率 40% 表示每賣 100 元，扣掉成本還剩 40 元。"
            "越高代表產品越有定價能力。"
        ),
        "analogy_fn": get_gross_margin_analogy,
        "historical_context": (
            "不同產業毛利率差異很大：軟體業可達 80%以上，代工廠可能只有 5-10%。"
            "跟自己過去的毛利率比較，比跟不同產業比較更有意義。"
        ),
    },
    "net_margin": {
        "display_name": "淨利率",
        "unit": "%",
        "is_higher_better": True,
        "explanation": (
            "淨利率是扣掉所有成本（營業費用、利息、稅金）後，真正賺到的錢。"
            "淨利率 10% 表示每賣 100 元，公司最後口袋剩 10 元。"
            "越高代表公司控制成本的能力越好。"
        ),
        "analogy_fn": lambda val: (
            f"每賣 100 元東西，扣掉所有開銷後剩 {val:.1f} 元 — "
            + ("獲利能力不錯" if val >= 15 else "利潤空間有限" if val >= 5 else "賺錢很辛苦")
        ),
        "historical_context": (
            "淨利率會受一次性業外損益影響，建議看近 4-8 季的趨勢而非單季數字。"
            "科技業淨利率通常 10-30%，零售業可能只有 1-5%。"
        ),
    },
    "debt_ratio": {
        "display_name": "負債比",
        "unit": "%",
        "is_higher_better": False,
        "explanation": (
            "負債比是公司資產中有多少比例是借來的錢。"
            "負債比 60% 表示每 100 元資產中，有 60 元是借來的。"
            "越低代表財務越保守，但適度借錢可以加速成長。"
        ),
        "analogy_fn": get_debt_ratio_analogy,
        "historical_context": (
            "金融業負債比通常 80-90%（因為存款算負債），這是正常的。"
            "製造業建議負債比控制在 50% 以下。景氣差時高負債比風險較大。"
        ),
    },
    "revenue_yoy": {
        "display_name": "營收年增率",
        "unit": "%",
        "is_higher_better": True,
        "explanation": (
            "營收年增率是跟去年同月比較，營收成長或衰退的幅度。"
            "年增 20% 表示今年營收比去年同月多 20%。"
            "正數代表成長，負數代表衰退。"
        ),
        "analogy_fn": get_yoy_analogy,
        "historical_context": (
            "單月營收年增率波動較大，建議看 3-6 個月的趨勢更有參考價值。"
            "季節性產業（如冷飲、觀光）需考慮淡旺季因素。"
        ),
    },
    "PER": {
        "display_name": "本益比 (PER)",
        "unit": "倍",
        "is_higher_better": False,
        "explanation": (
            "本益比是股價除以每股盈餘，代表市場願意為公司每賺 1 元付多少錢。"
            "本益比 15 倍表示市場願意為每 1 元獲利付 15 元。"
            "越低代表回本越快，但也可能反映市場不看好。"
        ),
        "analogy_fn": get_per_analogy,
        "historical_context": (
            "台股歷史本益比區間約 10-25 倍。不同產業合理本益比不同："
            "成長股可能 20-30 倍，景氣循環股可能 8-12 倍。"
            "虧損公司沒有本益比。"
        ),
    },
    "PBR": {
        "display_name": "淨值比 (PBR)",
        "unit": "倍",
        "is_higher_better": False,
        "explanation": (
            "淨值比是股價除以每股淨值，代表股價相對於公司帳面價值的倍數。"
            "淨值比 1.5 表示股價是淨值的 1.5 倍。"
            "低於 1 表示股價比淨值還便宜（但可能有原因）。"
        ),
        "analogy_fn": get_pbr_analogy,
        "historical_context": (
            "淨值比適合評估資產密集型產業（如銀行、營建）。"
            "輕資產公司（如軟體、品牌）淨值比通常較高，因為價值在無形資產。"
            "巴菲特早期偏好淨值比低於 1 的股票。"
        ),
    },
    "dividend_yield": {
        "display_name": "殖利率",
        "unit": "%",
        "is_higher_better": True,
        "explanation": (
            "殖利率是每年配發的股利除以股價，代表投資一年能領回的現金比例。"
            "殖利率 4% 表示每投資 100 元，一年約領回 4 元股利。"
            "越高代表配息越多，但太高可能代表股價下跌或配息不可持續。"
        ),
        "analogy_fn": get_dividend_analogy,
        "historical_context": (
            "台股平均殖利率約 3-4%。殖利率 5% 以上算高息股，但要注意："
            "1) 是否為一次性業外收入造成的超高殖利率；2) 公司是否有賺錢。"
            "過去 5 年穩定配息的公司較可靠。"
        ),
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
            "explanation": f"{metric_name} 是衡量公司表現的指標之一。",
            "analogy": "這個指標需要更多背景資料才能提供比喻。",
            "is_higher_better": True,
            "historical_context": "建議查閱更多關於此指標的資料。",
            "display_name": metric_name,
            "unit": "",
            "value": value,
        }

    analogy_fn = entry["analogy_fn"]
    try:
        analogy = analogy_fn(value)
    except Exception:
        analogy = "暫時無法產生比喻。"

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
