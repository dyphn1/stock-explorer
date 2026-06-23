"""
ROE 計算服務
支援 TTM（近四季）計算，處理季節性產業

For seasonal industries (retail, semiconductors, etc.), ROE is computed
using trailing 12-month net income divided by average equity, NOT by
annualizing a single quarter's result.
"""
from __future__ import annotations

from src.services.financial_metrics import find_financial_value
from src.core.i18n import t

SEASONAL_INDUSTRIES = frozenset({
    "觀光餐旅",
    "農漁業",
    "零售",
    "半導體業",
    "貿易百貨",
    "建材營造",
})


def is_seasonal_industry(industry: str) -> bool:
    """判定是否為高季節性產業"""
    return industry in SEASONAL_INDUSTRIES


def calc_roe_ttm(financial_df, balance_sheet_df, industry: str = "") -> dict | None:
    """
    Calculate ROE using Trailing Twelve Months (TTM) approach.

    For all industries: sum last 4 quarters of net income, divide by
    average equity. This avoids the naive *4 multiplication that distorts
    seasonal businesses.

    For seasonal industries: adds a warning flag and uses the same TTM
    method (which is already correct), but notes the seasonal context.

    Returns dict with keys:
        roe (float): ROE percentage
        method (str): "TTM" | "3季累計" | "2季累計" | "單季"
        quarters_used (int): number of quarters actually summed
        ttm_net_income (float): total net income used
        avg_equity (float): average equity used
        is_seasonal (bool): True if industry is seasonal
        warning (str | None): warning message for seasonal businesses
    Returns None if data insufficient.
    """
    if financial_df is None or len(financial_df) == 0:
        return None
    if balance_sheet_df is None or len(balance_sheet_df) == 0:
        return None

    try:
        # ── Step 1: Collect quarterly net income (up to 4 quarters) ──
        net_income_kw = ["淨利", "本期淨利", "Net Income", "net_income"]
        dates_sorted = sorted(financial_df["date"].unique(), reverse=True)

        quarterly_ni = []
        for d in dates_sorted:
            subset = financial_df[financial_df["date"] == d]
            ni = find_financial_value(subset, net_income_kw)
            if ni != 0:
                quarterly_ni.append(ni)
            if len(quarterly_ni) >= 4:
                break

        if not quarterly_ni:
            return None

        quarters_used = len(quarterly_ni)
        ttm_net_income = sum(quarterly_ni)

        # ── Step 2: Average equity (beginning + ending) / 2 ──
        equity_kw = ["權益總計", "股東權益", "Total Equity", "total_equity"]
        bs_dates_sorted = sorted(balance_sheet_df["date"].unique(), reverse=True)

        # Ending equity (latest)
        latest_bs = balance_sheet_df[balance_sheet_df["date"] == bs_dates_sorted[0]]
        equity_end = find_financial_value(latest_bs, equity_kw)

        # Beginning equity (quarters_used quarters back, or earliest available)
        begin_idx = min(quarters_used, len(bs_dates_sorted)) - 1
        earliest_bs = balance_sheet_df[balance_sheet_df["date"] == bs_dates_sorted[begin_idx]]
        equity_begin = find_financial_value(earliest_bs, equity_kw)

        if equity_end <= 0 and equity_begin <= 0:
            return None

        # Use whichever is available for averaging
        if equity_begin > 0 and equity_end > 0:
            avg_equity = (equity_end + equity_begin) / 2
        else:
            avg_equity = max(equity_end, equity_begin)

        if avg_equity <= 0:
            return None

        # ── Step 3: Compute ROE ──
        roe = ttm_net_income / avg_equity * 100

        # ── Step 4: Method label ──
        if quarters_used >= 4:
            method = "TTM"
        elif quarters_used == 3:
            method = t("roe_calculator.method.3q")
        elif quarters_used == 2:
            method = t("roe_calculator.method.2q")
        else:
            method = t("roe_calculator.method.1q")

        # ── Step 5: Seasonal warning ──
        is_seasonal = is_seasonal_industry(industry)
        warning = None
        if is_seasonal and quarters_used < 4:
            warning = t("metric_education.roe_warning_seasonal_insufficient").format(
                industry=industry, quarters=quarters_used
            )
        elif is_seasonal:
            warning = t("metric_education.roe_warning_seasonal_sufficient").format(
                industry=industry
            )

        return {
            "roe": round(roe, 1),
            "method": method,
            "quarters_used": quarters_used,
            "ttm_net_income": ttm_net_income,
            "avg_equity": avg_equity,
            "is_seasonal": is_seasonal,
            "warning": warning,
        }
    except Exception:
        return None
