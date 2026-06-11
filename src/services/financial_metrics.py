"""
Financial Metrics Calculator
Shared financial calculation functions extracted from _router_base.py, chart.py, and analogy_engine.py
"""
import pandas as pd
from typing import Optional


def find_financial_value(df: pd.DataFrame, keywords: list) -> float:
    """從財務資料中根據關鍵字找值"""
    for _, row in df.iterrows():
        type_val = str(row.get("type", ""))
        for kw in keywords:
            if kw.lower() in type_val.lower():
                val = row.get("value")
                if pd.notna(val) and val != 0:
                    return float(val)
    return 0.0


def extract_ttm_eps(financial_df: pd.DataFrame, as_of_date=None) -> Optional[float]:
    """
    Extract Trailing Twelve Months EPS from quarterly financial statements.

    Args:
        financial_df: DataFrame with financial statement data (columns: type, value, date)
        as_of_date: Optional cutoff date. If None, uses the latest date in the data.

    Returns:
        TTM EPS (sum of last 4 quarters), or None if insufficient data.
    """
    if financial_df is None or len(financial_df) == 0:
        return None

    eps_df = extract_quarterly_eps(financial_df, as_of_date)

    if eps_df is None or len(eps_df) < 1:
        return None

    # Sum last 4 quarters (or fewer if not enough history)
    ttm_eps = eps_df.tail(4)["value"].sum()

    if ttm_eps <= 0:
        return None

    return float(ttm_eps)


def extract_quarterly_eps(financial_df: pd.DataFrame, as_of_date=None) -> Optional[pd.DataFrame]:
    """
    Extract and clean quarterly EPS data from financial statements.

    Returns a DataFrame with columns (date, value) sorted by date,
    with one row per date (max value if duplicates exist).
    Returns None if no EPS data found.
    """
    if financial_df is None or len(financial_df) == 0:
        return None

    fin = financial_df.copy()
    fin["date"] = pd.to_datetime(fin["date"])

    # Find EPS rows (type contains eps or 每股盈餘)
    eps_keywords = ["eps", "每股盈餘", "earnings per share"]
    eps_mask = fin["type"].str.lower().str.contains(
        "|".join(eps_keywords), case=False, na=False
    )
    eps_df = fin[eps_mask].copy()

    if len(eps_df) == 0:
        return None

    # One row per date (if multiple, take the max value)
    eps_df = eps_df.groupby("date", as_index=False)["value"].max()
    eps_df = eps_df.sort_values("date").reset_index(drop=True)

    if as_of_date is not None:
        as_of_date = pd.to_datetime(as_of_date)
        eps_df = eps_df[eps_df["date"] <= as_of_date]

    if len(eps_df) < 1:
        return None

    return eps_df


def calculate_gross_margin(revenue: float, gross_profit: float) -> Optional[float]:
    """Calculate gross margin percentage."""
    if revenue and revenue > 0 and gross_profit:
        return round(gross_profit / revenue * 100, 1)
    return None


def calculate_net_margin(revenue: float, net_income: float) -> Optional[float]:
    """Calculate net margin percentage."""
    if revenue and revenue > 0 and net_income:
        return round(net_income / revenue * 100, 1)
    return None


def calculate_operating_margin(revenue: float, operating_income: float) -> Optional[float]:
    """Calculate operating margin percentage."""
    if revenue and revenue > 0 and operating_income:
        return round(operating_income / revenue * 100, 1)
    return None


def calculate_debt_ratio(total_liabilities: float, total_assets: float) -> Optional[float]:
    """Calculate debt ratio percentage."""
    if total_assets and total_assets > 0 and total_liabilities:
        return round(total_liabilities / total_assets * 100, 1)
    return None


def calculate_equity_ratio(total_equity: float, total_assets: float) -> Optional[float]:
    """Calculate equity ratio percentage."""
    if total_assets and total_assets > 0 and total_equity:
        return round(total_equity / total_assets * 100, 1)
    return None


def calculate_revenue_yoy(monthly_revenue_df: pd.DataFrame) -> Optional[float]:
    """Calculate year-over-year revenue growth from monthly revenue data."""
    if monthly_revenue_df is not None and len(monthly_revenue_df) > 12:
        try:
            latest_rev = monthly_revenue_df.iloc[-1]["revenue"]
            last_year_rev = monthly_revenue_df.iloc[-13]["revenue"]
            if last_year_rev > 0:
                return round((latest_rev - last_year_rev) / last_year_rev * 100, 1)
        except Exception:
            pass
    return None


def calc_extra_metrics(financial_df, balance_sheet_df, monthly_revenue_df) -> dict:
    """
    Calculate all extra metrics (consolidated version of _calc_extra_metrics from _router_base.py).
    Returns dict with: gross_margin, operating_margin, net_margin, debt_ratio, equity_ratio, revenue_yoy
    """
    metrics = {}

    if financial_df is not None and len(financial_df) > 0:
        try:
            latest_date = financial_df["date"].max()
            latest = financial_df[financial_df["date"] == latest_date]

            revenue = find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
            gross_profit = find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
            operating_income = find_financial_value(latest, ["營業利益", "營業利潤", "Operating Income", "operating_income"])
            net_income = find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])

            if revenue and revenue > 0:
                if gross_profit:
                    metrics["gross_margin"] = round(gross_profit / revenue * 100, 1)
                if operating_income:
                    metrics["operating_margin"] = round(operating_income / revenue * 100, 1)
                if net_income:
                    metrics["net_margin"] = round(net_income / revenue * 100, 1)
        except Exception:
            pass

    if balance_sheet_df is not None and len(balance_sheet_df) > 0:
        try:
            latest_date = balance_sheet_df["date"].max()
            latest = balance_sheet_df[balance_sheet_df["date"] == latest_date]

            total_assets = find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
            total_liabilities = find_financial_value(latest, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])
            total_equity = find_financial_value(latest, ["權益總計", "股東權益", "Total Equity", "total_equity"])

            if total_assets and total_assets > 0:
                if total_liabilities:
                    metrics["debt_ratio"] = round(total_liabilities / total_assets * 100, 1)
                if total_equity:
                    metrics["equity_ratio"] = round(total_equity / total_assets * 100, 1)
        except Exception:
            pass

    if monthly_revenue_df is not None and len(monthly_revenue_df) > 12:
        try:
            latest_rev = monthly_revenue_df.iloc[-1]["revenue"]
            last_year_rev = monthly_revenue_df.iloc[-13]["revenue"]
            if last_year_rev > 0:
                metrics["revenue_yoy"] = round((latest_rev - last_year_rev) / last_year_rev * 100, 1)
        except Exception:
            pass

    return metrics
