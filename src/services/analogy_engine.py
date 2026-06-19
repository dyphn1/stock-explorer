"""
生活化比喻引擎
將財務數字轉化為新手能秒懂的比喻
"""

import random
import pandas as pd
from typing import Optional

from src.core.i18n import t


def get_revenue_analogy(revenue_billion: float, industry: str) -> str:
    """營收的生活化比喻"""
    if revenue_billion >= 10000:
        return t("analogy.revenue.gov_budget_pct", pct=f"{revenue_billion/27000*100:.0f}")
    elif revenue_billion >= 1000:
        return t("analogy.revenue.trillion", value=f"{revenue_billion/1000:.1f}")
    elif revenue_billion >= 100:
        return t("analogy.revenue.monthly_100b", monthly=f"{revenue_billion/12:.0f}", buildings=f"{revenue_billion/12/10:.0f}")
    elif revenue_billion >= 10:
        return t("analogy.revenue.monthly_10b", monthly=f"{revenue_billion/12:.1f}", salaries=f"{revenue_billion/12/5:.0f}")
    else:
        return t("analogy.revenue.monthly_small", monthly=f"{revenue_billion/12:.1f}")


def get_gross_margin_analogy(margin: float) -> str:
    """毛利率的生活化比喻"""
    if margin >= 60:
        return t("analogy.gross_margin.high", margin=f"{margin:.0f}")
    elif margin >= 40:
        return t("analogy.gross_margin.good", margin=f"{margin:.0f}")
    elif margin >= 20:
        return t("analogy.gross_margin.thin", margin=f"{margin:.0f}")
    elif margin >= 10:
        return t("analogy.gross_margin.low", margin=f"{margin:.0f}")
    else:
        return t("analogy.gross_margin.very_low", margin=f"{margin:.0f}")


def get_per_analogy(per: float) -> str:
    """本益比的生活化比喻"""
    if per >= 30:
        return t("analogy.per.high", per=f"{per:.1f}")
    elif per >= 20:
        return t("analogy.per.moderate", per=f"{per:.1f}")
    elif per >= 10:
        return t("analogy.per.fair", per=f"{per:.1f}")
    elif per > 0:
        return t("analogy.per.low", per=f"{per:.1f}")
    else:
        return t("analogy.per.negative")


def get_pbr_analogy(pbr: float) -> str:
    """淨值比的生活化比喻"""
    if pbr >= 3:
        return t("analogy.pbr.premium", pbr=f"{pbr:.1f}")
    elif pbr >= 1.5:
        return t("analogy.pbr.reasonable", pbr=f"{pbr:.1f}")
    elif pbr >= 1:
        return t("analogy.pbr.neutral", pbr=f"{pbr:.1f}")
    else:
        return t("analogy.pbr.discount", pbr=f"{pbr:.1f}")


def get_dividend_analogy(dy: float, price: float = 0) -> str:
    """殖利率的生活化比喻"""
    if dy >= 6:
        return t("analogy.dividend.high", dy=f"{dy:.1f}")
    elif dy >= 4:
        return t("analogy.dividend.good", dy=f"{dy:.1f}")
    elif dy >= 2:
        return t("analogy.dividend.moderate", dy=f"{dy:.1f}")
    elif dy > 0:
        return t("analogy.dividend.low", dy=f"{dy:.1f}")
    else:
        return t("analogy.dividend.none")


def get_roe_analogy(roe: float) -> str:
    """ROE 的生活化比喻"""
    if roe >= 20:
        return t("analogy.roe.excellent", roe=f"{roe:.1f}")
    elif roe >= 15:
        return t("analogy.roe.good", roe=f"{roe:.1f}")
    elif roe >= 10:
        return t("analogy.roe.average", roe=f"{roe:.1f}")
    elif roe >= 5:
        return t("analogy.roe.poor", roe=f"{roe:.1f}")
    elif roe > 0:
        return t("analogy.roe.very_poor", roe=f"{roe:.1f}")
    else:
        return t("analogy.roe.negative")


def get_debt_ratio_analogy(ratio: float) -> str:
    """負債比的生活化比喻"""
    if ratio >= 70:
        return t("analogy.debt.high", ratio=f"{ratio:.0f}")
    elif ratio >= 50:
        return t("analogy.debt.moderate", ratio=f"{ratio:.0f}")
    elif ratio >= 30:
        return t("analogy.debt.healthy", ratio=f"{ratio:.0f}")
    else:
        return t("analogy.debt.low", ratio=f"{ratio:.0f}")


def get_volume_analogy(volume: int) -> str:
    """成交量的生活化比喻"""
    if volume >= 100000:
        return t("analogy.volume.very_high", volume=f"{volume/1000:.0f}")
    elif volume >= 50000:
        return t("analogy.volume.high", volume=f"{volume/1000:.0f}")
    elif volume >= 10000:
        return t("analogy.volume.normal", volume=f"{volume/1000:.0f}")
    elif volume >= 1000:
        return t("analogy.volume.low", volume=f"{volume/1000:.0f}")
    else:
        return t("analogy.volume.very_low", volume=f"{volume}")


def get_institutional_analogy(net_buy: float) -> str:
    """法人買賣超的生活化比喻"""
    if net_buy >= 50000:
        return t("analogy.institutional.strong_buy", volume=f"{net_buy/1000:.0f}")
    elif net_buy >= 10000:
        return t("analogy.institutional.buy", volume=f"{net_buy/1000:.0f}")
    elif net_buy >= 0:
        return t("analogy.institutional.slight_buy", volume=f"{net_buy/1000:.0f}")
    elif net_buy >= -10000:
        return t("analogy.institutional.sell", volume=f"{abs(net_buy)/1000:.0f}")
    else:
        return t("analogy.institutional.strong_sell", volume=f"{abs(net_buy)/1000:.0f}")


def get_yoy_analogy(yoy: float) -> str:
    """年增率的生活化比喻"""
    if yoy >= 50:
        return t("analogy.yoy.strong", yoy=f"{yoy:.0f}")
    elif yoy >= 20:
        return t("analogy.yoy.good", yoy=f"{yoy:.0f}")
    elif yoy >= 5:
        return t("analogy.yoy.moderate", yoy=f"{yoy:.0f}")
    elif yoy >= -5:
        return t("analogy.yoy.flat", yoy=f"{yoy:.0f}")
    elif yoy >= -20:
        return t("analogy.yoy.decline", yoy=f"{abs(yoy):.0f}")
    else:
        return t("analogy.yoy.sharp_decline", yoy=f"{abs(yoy):.0f}")


def get_one_liner(stock_id: str, stock_name: str, industry: str) -> str:
    """生成一句話定位（擴展版）"""
    one_liners = {
        "2330": t("analogy.oneliner.2330"),
        "2317": t("analogy.oneliner.2317"),
        "2454": t("analogy.oneliner.2454"),
        "2308": t("analogy.oneliner.2308"),
        "2881": t("analogy.oneliner.2881"),
        "1101": t("analogy.oneliner.1101"),
        "2002": t("analogy.oneliner.2002"),
        "1301": t("analogy.oneliner.1301"),
        "2357": t("analogy.oneliner.2357"),
        "2382": t("analogy.oneliner.2382"),
        "2886": t("analogy.oneliner.2886"),
        "2891": t("analogy.oneliner.2891"),
        "1216": t("analogy.oneliner.1216"),
        "2912": t("analogy.oneliner.2912"),
        "2303": t("analogy.oneliner.2303"),
        "2345": t("analogy.oneliner.2345"),
        "3008": t("analogy.oneliner.3008"),
        "2412": t("analogy.oneliner.2412"),
        "3711": t("analogy.oneliner.3711"),
        "2324": t("analogy.oneliner.2324"),
    }

    if stock_id in one_liners:
        return one_liners[stock_id]

    # 根據產業生成通用定位
    industry_templates = {
        "半導體業": t("analogy.oneliner.industry.semiconductor", name=stock_name),
        "電子工業": t("analogy.oneliner.industry.electronics", name=stock_name),
        "金融保險": t("analogy.oneliner.industry.finance", name=stock_name),
        "電腦及週邊設備業": t("analogy.oneliner.industry.computer", name=stock_name),
        "生技醫療業": t("analogy.oneliner.industry.biotech", name=stock_name),
        "觀光餐旅": t("analogy.oneliner.industry.tourism", name=stock_name),
        "電機機械": t("analogy.oneliner.industry.machinery", name=stock_name),
        "建材營造": t("analogy.oneliner.industry.construction", name=stock_name),
        "化學工業": t("analogy.oneliner.industry.chemical", name=stock_name),
        "通信網路業": t("analogy.oneliner.industry.telecom", name=stock_name),
    }

    return industry_templates.get(industry, t("analogy.oneliner.industry.default", name=stock_name, industry=industry, stock_id=stock_id))
