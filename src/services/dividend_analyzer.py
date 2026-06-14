"""Dividend analysis service for Stock Explorer."""

from __future__ import annotations

import pandas as pd


def extract_dividend_summary(
    dividend_df: pd.DataFrame | None,
    current_price: float | None = None,
) -> dict:
    """Extract dividend summary from FinMind dividend DataFrame.

    FinMind TaiwanStockDividend columns:
    - CashEarningsDistribution: cash dividend per share
    - CashExDividendTradingDate: ex-dividend date (may be empty string)
    - CashDividendPaymentDate: payment date
    - StockEarningsDistribution: stock dividend per share
    - year: ROC calendar year (e.g., "113年")
    - date: announcement date (used for sorting)

    Returns dict with:
    - has_data (bool)
    - yearly_dividends (list of dicts)
    - latest_cash_div (float | None)
    - estimated_annual (float | None)
    - estimated_yield (float | None)
    - plain_summary (str)
    - frequency (str: "quarterly" | "annual" | "irregular" | "none")
    """
    if dividend_df is None or dividend_df.empty:
        return {
            "has_data": False,
            "yearly_dividends": [],
            "latest_cash_div": None,
            "estimated_annual": None,
            "estimated_yield": None,
            "plain_summary": "此公司暫無除權息紀錄",
            "frequency": "none",
        }

    # Work with a copy, sorted by date descending
    df = dividend_df.copy()
    # Ensure date column exists and is datetime-like for sorting
    if "date" in df.columns:
        df = df.sort_values("date", ascending=False)

    # Filter rows with actual cash dividends > 0
    cash_col = "CashEarningsDistribution"
    if cash_col not in df.columns:
        return {
            "has_data": False,
            "yearly_dividends": [],
            "latest_cash_div": None,
            "estimated_annual": None,
            "estimated_yield": None,
            "plain_summary": "此公司暫無除權息紀錄",
            "frequency": "none",
        }

    div_rows = df[df[cash_col].fillna(0) > 0].copy()
    if div_rows.empty:
        return {
            "has_data": False,
            "yearly_dividends": [],
            "latest_cash_div": None,
            "estimated_annual": None,
            "estimated_yield": None,
            "plain_summary": "此公司近五年無配息紀錄",
            "frequency": "none",
        }

    # Build yearly_dividends list (up to 8 most recent)
    yearly_dividends = []
    today = pd.Timestamp.now()
    for _, row in div_rows.head(8).iterrows():
        cash_div = float(row.get(cash_col, 0) or 0)
        stock_div = float(row.get("StockEarningsDistribution", 0) or 0)
        year_str = str(row.get("year", "")).strip() or "—"
        ex_date = str(row.get("CashExDividendTradingDate", "")).strip()
        pay_date = str(row.get("CashDividendPaymentDate", "")).strip()

        # Determine status
        if pay_date and pay_date != "":
            try:
                pay_dt = pd.Timestamp(pay_date)
                status = "✓ 已發放" if pay_dt <= today else "⏳ 待發放"
            except Exception:
                status = "⏳ 待發放"
        else:
            status = "⏳ 待發放"

        yearly_dividends.append({
            "year": year_str,
            "cash_div": cash_div,
            "stock_div": stock_div if stock_div > 0 else None,
            "ex_date": ex_date if ex_date else "—",
            "pay_date": pay_date if pay_date else "—",
            "status": status,
        })

    # Latest cash dividend
    latest_cash_div = yearly_dividends[0]["cash_div"] if yearly_dividends else None

    # Determine frequency
    frequency = _classify_frequency(div_rows)  # type: ignore[arg-type]

    # Estimate annual dividend
    estimated_annual = _estimate_annual(div_rows.copy(), frequency)  # type: ignore[arg-type]

    # Estimated yield
    estimated_yield = None
    if estimated_annual and current_price and current_price > 0:
        estimated_yield = round(estimated_annual / current_price * 100, 2)

    # Plain-language summary
    plain_summary = _generate_summary(yearly_dividends, frequency, latest_cash_div, estimated_yield)

    return {
        "has_data": True,
        "yearly_dividends": yearly_dividends,
        "latest_cash_div": latest_cash_div,
        "estimated_annual": estimated_annual,
        "estimated_yield": estimated_yield,
        "plain_summary": plain_summary,
        "frequency": frequency,
    }


def _classify_frequency(div_rows: pd.DataFrame) -> str:
    """Classify dividend payment frequency."""
    if div_rows.empty:
        return "none"

    # Count payments per ROC year
    year_col = "year"
    if year_col not in div_rows.columns:
        return "irregular"

    year_counts = div_rows.groupby(year_col).size()

    if len(year_counts) == 0:
        return "none"

    avg_per_year = year_counts.mean()

    if avg_per_year >= 3:
        return "quarterly"
    elif avg_per_year >= 1:
        # Check if it's consistently annual
        if len(year_counts) >= 2 and year_counts.min() >= 1:
            return "annual"
        return "irregular"
    return "irregular"


def _estimate_annual(div_rows: pd.DataFrame, frequency: str) -> float | None:
    """Estimate annual dividend based on frequency."""
    if div_rows.empty:
        return None

    cash_col = "CashEarningsDistribution"
    latest = div_rows.head(4)  # Last 4 payments

    if frequency == "quarterly":
        # Sum last 4 quarters (TTM)
        return round(latest[cash_col].sum(), 2)  # type: ignore[return-value]
    elif frequency == "annual":
        # Most recent annual payment
        return round(float(div_rows.iloc[0][cash_col]), 2)
    else:
        # Irregular: sum last 12 months of payments
        return round(latest[cash_col].sum(), 2)  # type: ignore[return-value]


def _generate_summary(
    yearly_dividends: list[dict],
    frequency: str,
    latest_cash_div: float | None,
    estimated_yield: float | None,
) -> str:
    """Generate plain-language dividend summary."""
    if not yearly_dividends:
        return "此公司近五年無配息紀錄"

    n_years = len(set(d["year"] for d in yearly_dividends if d["year"] != "—"))

    if frequency == "quarterly" and latest_cash_div:
        parts = [f"每季約配息 {latest_cash_div} 元"]
        if estimated_yield:
            parts.append(f"預估年化殖利率約 {estimated_yield}%")
        return f"過去 {n_years} 年，這家企業穩定" + "，".join(parts)
    elif frequency == "annual" and latest_cash_div:
        parts = [f"每年配息約 {latest_cash_div} 元"]
        if estimated_yield:
            parts.append(f"殖利率約 {estimated_yield}%")
        return f"過去 {n_years} 年，這家企業每年穩定" + "，".join(parts)
    elif frequency == "irregular":
        return f"配息不穩定，依當年度獲利情形決定。最近一次配息 {latest_cash_div or '—'} 元"
    else:
        return f"此公司近 {n_years} 年有配息紀錄"
