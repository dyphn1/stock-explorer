"""
變化量（Delta）引擎
計算最近的重要變化並生成白話解釋
"""


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
        delta["explanation"] = explain_delta(
            delta["metric_name"],
            delta["change_pct"],
            delta["direction"],
            "",  # stock_name 可選，留空使用通用描述
            "",
        )

    return deltas[:2]


def explain_delta(
    metric_name: str,
    change_pct: float,
    direction: str,
    stock_name: str = "",
    industry: str = "",
) -> str:
    """為變化量生成白話解釋（C39）

    Args:
        metric_name: 指標名稱
        change_pct: 變化百分比（含正負號）
        direction: "up" 或 "down"
        stock_name: 股票名稱（可選）
        industry: 產業名稱（可選）

    回傳中文（zh-TW）的解釋字串。
    """
    abs_pct = abs(change_pct)
    name_prefix = f"{stock_name} " if stock_name else ""

    # 根據指標類型和方向產生解釋
    if metric_name == "月營收":
        if direction == "up":
            if abs_pct >= 50:
                return f"{name_prefix}月營收暴增 {abs_pct:.0f}%，可能是大訂單入帳或旺季效應，值得關注後續動能"
            elif abs_pct >= 30:
                return f"{name_prefix}月營收成長 {abs_pct:.0f}%，表現優於預期，可能是需求回溫或新產品貢獻"
            else:
                return f"{name_prefix}月營收成長 {abs_pct:.0f}%，溫和成長中"
        else:
            if abs_pct >= 50:
                return f"{name_prefix}月營收驟降 {abs_pct:.0f}%，可能是淡季或失去大客戶，需要密切關注"
            elif abs_pct >= 30:
                return f"{name_prefix}月營收衰退 {abs_pct:.0f}%，表現不如預期，可能是需求下滑或訂單遞延"
            else:
                return f"{name_prefix}月營收小跌 {abs_pct:.0f}%，略有衰退但仍在合理範圍"

    if metric_name == "股價（近 30 日均價）":
        if direction == "up":
            if abs_pct >= 30:
                return f"{name_prefix}股價近 30 日大漲 {abs_pct:.0f}%，市場情緒樂觀，可能是基本面改善或利多消息推動"
            elif abs_pct >= 20:
                return f"{name_prefix}股價近 30 日上漲 {abs_pct:.0f}%，多頭趨勢明顯"
            else:
                return f"{name_prefix}股價近 30 日上漲 {abs_pct:.0f}%，穩步走揚"
        else:
            if abs_pct >= 30:
                return f"{name_prefix}股價近 30 日大跌 {abs_pct:.0f}%，市場信心不足，可能是利空消息或基本面惡化"
            elif abs_pct >= 20:
                return f"{name_prefix}股價近 30 日下跌 {abs_pct:.0f}%，空頭趨勢明顯"
            else:
                return f"{name_prefix}股價近 30 日小跌 {abs_pct:.0f}%，略有回檔"

    if metric_name == "營收年增率":
        if direction == "up":
            if abs_pct >= 50:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，成長非常強勁，可能是新產品大賣或市場需求爆發"
            elif abs_pct >= 20:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，穩定成長，公司經營績效良好"
            else:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，溫和成長"
        else:
            if abs_pct >= 50:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，大幅衰退，可能有結構性問題需要關注"
            elif abs_pct >= 20:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，比去年差，需留意原因"
            else:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，略有衰退"

    # 通用解釋
    if direction == "up":
        return f"{name_prefix}{metric_name} 較前期成長 {abs_pct:.1f}%"
    else:
        return f"{name_prefix}{metric_name} 較前期衰退 {abs_pct:.1f}%"
