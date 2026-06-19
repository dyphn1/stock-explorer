"""
重點摘要（Key Takeaways）模組
精選 + 自動生成重點摘要
"""

from src.core.i18n import t
from src.services.analogy_engine import get_one_liner

# Curated key takeaways for top 20 stocks (by stock_ID)
_KEY_TAKEAWAYS: dict[str, list[str]] = {
    "2330": [
        t("key_takeaways.2330.0"),
        t("key_takeaways.2330.1"),
        t("key_takeaways.2330.2"),
        t("key_takeaways.2330.3"),
    ],
    "2317": [
        t("key_takeaways.2317.0"),
        t("key_takeaways.2317.1"),
        t("key_takeaways.2317.2"),
        t("key_takeaways.2317.3"),
    ],
    "2454": [
        t("key_takeaways.2454.0"),
        t("key_takeaways.2454.1"),
        t("key_takeaways.2454.2"),
        t("key_takeaways.2454.3"),
    ],
    "2308": [
        t("key_takeaways.2308.0"),
        t("key_takeaways.2308.1"),
        t("key_takeaways.2308.2"),
        t("key_takeaways.2308.3"),
    ],
    "2881": [
        t("key_takeaways.2881.0"),
        t("key_takeaways.2881.1"),
        t("key_takeaways.2881.2"),
        t("key_takeaways.2881.3"),
    ],
    "1101": [
        t("key_takeaways.1101.0"),
        t("key_takeaways.1101.1"),
        t("key_takeaways.1101.2"),
        t("key_takeaways.1101.3"),
    ],
    "2002": [
        t("key_takeaways.2002.0"),
        t("key_takeaways.2002.1"),
        t("key_takeaways.2002.2"),
        t("key_takeaways.2002.3"),
    ],
    "1301": [
        t("key_takeaways.1301.0"),
        t("key_takeaways.1301.1"),
        t("key_takeaways.1301.2"),
        t("key_takeaways.1301.3"),
    ],
    "2357": [
        t("key_takeaways.2357.0"),
        t("key_takeaways.2357.1"),
        t("key_takeaways.2357.2"),
        t("key_takeaways.2357.3"),
    ],
    "2382": [
        t("key_takeaways.2382.0"),
        t("key_takeaways.2382.1"),
        t("key_takeaways.2382.2"),
        t("key_takeaways.2382.3"),
    ],
    "2886": [
        t("key_takeaways.2886.0"),
        t("key_takeaways.2886.1"),
        t("key_takeaways.2886.2"),
        t("key_takeaways.2886.3"),
    ],
    "2891": [
        t("key_takeaways.2891.0"),
        t("key_takeaways.2891.1"),
        t("key_takeaways.2891.2"),
        t("key_takeaways.2891.3"),
    ],
    "1216": [
        t("key_takeaways.1216.0"),
        t("key_takeaways.1216.1"),
        t("key_takeaways.1216.2"),
        t("key_takeaways.1216.3"),
    ],
    "2912": [
        t("key_takeaways.2912.0"),
        t("key_takeaways.2912.1"),
        t("key_takeaways.2912.2"),
        t("key_takeaways.2912.3"),
    ],
    "2303": [
        t("key_takeaways.2303.0"),
        t("key_takeaways.2303.1"),
        t("key_takeaways.2303.2"),
        t("key_takeaways.2303.3"),
    ],
    "2345": [
        t("key_takeaways.2345.0"),
        t("key_takeaways.2345.1"),
        t("key_takeaways.2345.2"),
        t("key_takeaways.2345.3"),
    ],
    "3008": [
        t("key_takeaways.3008.0"),
        t("key_takeaways.3008.1"),
        t("key_takeaways.3008.2"),
        t("key_takeaways.3008.3"),
    ],
    "2412": [
        t("key_takeaways.2412.0"),
        t("key_takeaways.2412.1"),
        t("key_takeaways.2412.2"),
        t("key_takeaways.2412.3"),
    ],
    "3711": [
        t("key_takeaways.3711.0"),
        t("key_takeaways.3711.1"),
        t("key_takeaways.3711.2"),
        t("key_takeaways.3711.3"),
    ],
    "2324": [
        t("key_takeaways.2324.0"),
        t("key_takeaways.2324.1"),
        t("key_takeaways.2324.2"),
        t("key_takeaways.2324.3"),
    ],
}


def generate_key_takeaways(
    stock_id: str,
    stock_name: str,
    industry: str,
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    monthly_revenue,
    financial_df,
) -> list[str]:
    """生成 3-5 條重點摘要（C37）

    優先使用精選內容（curated），若無則根據財務數據自動生成。
    回傳中文（zh-TW）的重點摘要列表。
    """
    # 1. 精選內容優先
    if stock_id in _KEY_TAKEAWAYS:
        return _KEY_TAKEAWAYS[stock_id]

    # 2. 自動生成
    takeaways: list[str] = []

    # 一句話定位作為第一條
    one_liner = get_one_liner(stock_id, stock_name, industry)
    # 取第一句（以 — 或逗號前的部分）
    first_sentence = one_liner.split("—")[0].strip()
    if first_sentence:
        takeaways.append(t("key_takeaways.one_liner", first_sentence=first_sentence, industry=industry))

    # 毛利率
    gm = extra_metrics.get("gross_margin")
    if gm is not None:
        if gm >= 40:
            takeaways.append(t("key_takeaways.gm_high", gm=gm))
        elif gm >= 20:
            takeaways.append(t("key_takeaways.gm_medium", gm=gm))
        elif gm >= 10:
            takeaways.append(t("key_takeaways.gm_low", gm=gm))
        else:
            takeaways.append(t("key_takeaways.gm_very_low", gm=gm))

    # 營收年增率
    yoy = extra_metrics.get("revenue_yoy")
    if yoy is not None:
        if yoy >= 20:
            takeaways.append(t("key_takeaways.yoy_high", yoy=yoy))
        elif yoy >= 5:
            takeaways.append(t("key_takeaways.yoy_medium", yoy=yoy))
        elif yoy >= -5:
            takeaways.append(t("key_takeaways.yoy_flat", yoy=yoy))
        else:
            takeaways.append(t("key_takeaways.yoy_negative", yoy=yoy))

    # 本益比
    if latest_per_pbr and latest_per_pbr.get("PER"):
        per = latest_per_pbr["PER"]
        if per >= 25:
            takeaways.append(t("key_takeaways.per_high", per=per))
        elif per >= 15:
            takeaways.append(t("key_takeaways.per_medium", per=per))
        elif per > 0:
            takeaways.append(t("key_takeaways.per_low", per=per))
        else:
            takeaways.append(t("key_takeaways.per_negative"))

    # 殖利率
    if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
        dy = latest_per_pbr["dividend_yield"]
        if dy >= 5:
            takeaways.append(t("key_takeaways.dy_high", dy=dy))
        elif dy >= 3:
            takeaways.append(t("key_takeaways.dy_medium", dy=dy))
        elif dy > 0:
            takeaways.append(t("key_takeaways.dy_low", dy=dy))
        else:
            takeaways.append(t("key_takeaways.dy_none"))

    # ROE
    roe = extra_metrics.get("roe")
    if roe is not None:
        if roe >= 20:
            takeaways.append(t("key_takeaways.roe_high", roe=roe))
        elif roe >= 10:
            takeaways.append(t("key_takeaways.roe_medium", roe=roe))
        elif roe > 0:
            takeaways.append(t("key_takeaways.roe_low", roe=roe))
        else:
            takeaways.append(t("key_takeaways.roe_negative"))

    # 負債比
    debt = extra_metrics.get("debt_ratio")
    if debt is not None:
        if debt >= 70:
            takeaways.append(t("key_takeaways.debt_high", debt=debt))
        elif debt >= 50:
            takeaways.append(t("key_takeaways.debt_medium", debt=debt))
        else:
            takeaways.append(t("key_takeaways.debt_low", debt=debt))

    # 最多回傳 5 條
    return takeaways[:3]
