"""
ROE 計算服務
支援 TTM（近四季）計算，處理季節性產業
"""

import pandas as pd

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


def _find_value(df, keywords: list) -> float:
    """從財務資料中根據關鍵字找值"""
    for _, row in df.iterrows():
        type_val = str(row.get("type", ""))
        for kw in keywords:
            if kw.lower() in type_val.lower():
                val = row.get("value")
                if pd.notna(val) and val != 0:
                    return float(val)
    return 0.0


def calc_roe_ttm(financial_df, balance_sheet_df) -> dict | None:
    """
    計算 TTM ROE = 最近4季淨利合計 / 平均股東權益

    Returns dict with keys: roe, method, quarters_used, ttm_net_income, avg_equity
    Returns None if data insufficient.
    """
    if financial_df is None or len(financial_df) == 0:
        return None
    if balance_sheet_df is None or len(balance_sheet_df) == 0:
        return None

    try:
        # ── Step 1: Collect quarterly net income ──
        net_income_kw = ["淨利", "本期淨利", "Net Income", "net_income"]
        dates_sorted = sorted(financial_df["date"].unique(), reverse=True)

        quarterly_ni = []
        for d in dates_sorted:
            subset = financial_df[financial_df["date"] == d]
            ni = _find_value(subset, net_income_kw)
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
        equity_end = _find_value(latest_bs, equity_kw)

        # Beginning equity (quarters_used quarters back, or earliest available)
        begin_idx = min(quarters_used, len(bs_dates_sorted)) - 1
        earliest_bs = balance_sheet_df[balance_sheet_df["date"] == bs_dates_sorted[begin_idx]]
        equity_begin = _find_value(earliest_bs, equity_kw)

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
        elif quarters_used == 1:
            method = "單季"
        else:
            method = f"{quarters_used}季累計"

        return {
            "roe": round(roe, 1),
            "method": method,
            "quarters_used": quarters_used,
            "ttm_net_income": ttm_net_income,
            "avg_equity": avg_equity,
        }
    except Exception:
        return None
