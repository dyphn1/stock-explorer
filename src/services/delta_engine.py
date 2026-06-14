"""
變化量（Delta）引擎
計算最近的重要變化並生成白話解釋
"""

from src.services.delta_explanation_provider import DeltaExplanationProvider
from src.services.llm.base import ExplanationRequest

# Singleton provider instance — reusable across calls
_delta_provider = DeltaExplanationProvider()


def compute_recent_deltas(
    extra_metrics: dict,
    monthly_revenue,
    daily_price,
    latest_per_pbr: dict | None,
) -> list[dict]:
    """計算最近的重要變化（C39）

    比較：營收（最近月 vs 前一月）、股價（近 30 日 vs 前 30 日）、
          毛利率（最近季 vs 前季）。
    只回傳變化幅度 > 10% 的項目。

    回傳 list of dict，每個 dict 包含：
        metric_name, current_value, previous_value, change_pct, direction, explanation
    """
    deltas: list[dict] = []

    # 1. 營收月對月變化（最近月 vs 前一月）
    if monthly_revenue is not None and len(monthly_revenue) >= 2:
        try:
            latest_rev = float(monthly_revenue.iloc[-1]["revenue"])
            prev_rev = float(monthly_revenue.iloc[-2]["revenue"])
            if prev_rev > 0:
                rev_change = (latest_rev - prev_rev) / prev_rev * 100
                if abs(rev_change) > 10:
                    deltas.append({
                        "metric_name": "月營收",
                        "current_value": f"{latest_rev / 1e8:.0f} 億",
                        "previous_value": f"{prev_rev / 1e8:.0f} 億",
                        "change_pct": round(rev_change, 1),
                        "direction": "up" if rev_change > 0 else "down",
                        "explanation": "",
                    })
        except (KeyError, IndexError, TypeError, ZeroDivisionError):
            pass

    # 2. 股價 30 日變化（最後 30 日 vs 前 30 日）
    if daily_price is not None and len(daily_price) >= 60:
        try:
            recent_30 = daily_price.iloc[-30:]
            prior_30 = daily_price.iloc[-60:-30]
            recent_avg = float(recent_30["close"].mean())
            prior_avg = float(prior_30["close"].mean())
            if prior_avg > 0:
                price_change = (recent_avg - prior_avg) / prior_avg * 100
                if abs(price_change) > 10:
                    deltas.append({
                        "metric_name": "股價（近 30 日均價）",
                        "current_value": f"{recent_avg:.0f} 元",
                        "previous_value": f"{prior_avg:.0f} 元",
                        "change_pct": round(price_change, 1),
                        "direction": "up" if price_change > 0 else "down",
                        "explanation": "",
                    })
        except (KeyError, IndexError, TypeError, ZeroDivisionError):
            pass

    # 3. 毛利率季度變化（需要 financial_df，這裡從 extra_metrics 取得最新值，
    #    但季度比較需要歷史數據，這裡用 revenue_yoy 作為替代指標）
    yoy = extra_metrics.get("revenue_yoy")
    if yoy is not None and abs(yoy) > 10:
        deltas.append({
            "metric_name": "營收年增率",
            "current_value": f"{yoy:+.1f}%",
            "previous_value": "去年同期",
            "change_pct": round(yoy, 1),
            "direction": "up" if yoy > 0 else "down",
            "explanation": "",
        })

    # 為每個 delta 產生白話解釋
    for delta in deltas:
        explanation, implication = explain_delta_full(
            delta["metric_name"],
            delta["change_pct"],
            delta["direction"],
            "",  # stock_name 可選，留空使用通用描述
            "",
        )
        delta["explanation"] = explanation
        delta["implication"] = implication

    return deltas[:2]


def explain_delta(
    metric_name: str,
    change_pct: float,
    direction: str,
    stock_name: str = "",
    industry: str = "",
) -> str:
    """為變化量生成白話解釋（C39）

    Delegates to DeltaExplanationProvider which implements the
    ExplanationProvider protocol (D5 LLM abstraction layer).

    Args:
        metric_name: 指標名稱
        change_pct: 變化百分比（含正負號）
        direction: "up" 或 "down"
        stock_name: 股票名稱（可選）
        industry: 產業名稱（可選）

    回傳中文（zh-TW）的解釋字串。
    """
    abs_pct = abs(change_pct)
    delta_str = f"{abs_pct:+.1f}%"

    request = ExplanationRequest(
        metric_name=metric_name,
        metric_value=f"{abs_pct:.1f}%",
        delta=delta_str,
        context={
            "stock_name": stock_name,
            "industry": industry,
            "direction": direction,
            "change_pct": change_pct,
        },
        language="zh-TW",
    )

    response = _delta_provider.explain(request)
    return response.text


def explain_delta_full(
    metric_name: str,
    change_pct: float,
    direction: str,
    stock_name: str = "",
    industry: str = "",
) -> tuple[str, str]:
    """為變化量生成白話解釋 + 暗示句（C143）

    Like explain_delta() but returns a tuple of (explanation_text, implication_sentence).
    The implication sentence is a short historian-tone "so what" observation
    that replaces the explanation on delta cards (C143), while the explanation
    moves to the 💡 popover.

    Delegates to DeltaExplanationProvider which implements the
    ExplanationProvider protocol.

    Args:
        metric_name: 指標名稱
        change_pct: 變化百分比（含正負號）
        direction: "up" 或 "down"
        stock_name: 股票名稱（可選）
        industry: 產業名稱（可選）

    Returns:
        Tuple of (explanation_text, implication_sentence), both zh-TW.
    """
    abs_pct = abs(change_pct)
    delta_str = f"{abs_pct:+.1f}%"

    request = ExplanationRequest(
        metric_name=metric_name,
        metric_value=f"{abs_pct:.1f}%",
        delta=delta_str,
        context={
            "stock_name": stock_name,
            "industry": industry,
            "direction": direction,
            "change_pct": change_pct,
        },
        language="zh-TW",
    )

    response = _delta_provider.explain(request)
    return response.text, response.implication
