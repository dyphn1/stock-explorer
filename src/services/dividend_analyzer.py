"""Dividend analysis service for Stock Explorer.

Implements proper annualized projection with historical comparison.
Never multiplies a single quarter's dividend by 4 blindly.
All estimated values are clearly labeled.
"""

from __future__ import annotations

import pandas as pd

from src.core.i18n import t


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
    - is_estimated (bool) — True when estimated_annual is projected, not actual
    - historical_yields (list of dicts) — recent years for comparison
    - plain_summary (str)
    - frequency (str: "quarterly" | "annual" | "irregular" | "none")
    """
    if dividend_df is None or dividend_df.empty:
        return _empty_result()

    # Work with a copy, sorted by date descending
    df = dividend_df.copy()
    if "date" in df.columns:
        df = df.sort_values("date", ascending=False)

    # Filter rows with actual cash dividends > 0
    cash_col = "CashEarningsDistribution"
    if cash_col not in df.columns:
        return _empty_result()

    div_rows = df[df[cash_col].fillna(0) > 0].copy()
    if div_rows.empty:
        return _empty_result(t("dividend.no_record_recent"))

    # Build yearly_dividends list (up to 8 most recent)
    yearly_dividends = _build_yearly_dividends(div_rows, cash_col)

    # Latest cash dividend (most recent single payment)
    latest_cash_div = yearly_dividends[0]["cash_div"] if yearly_dividends else None

    # Determine frequency
    frequency = _classify_frequency(div_rows)

    # Estimate annual dividend using proper annualization
    estimated_annual, is_estimated = _estimate_annual_proper(div_rows, frequency)

    # Estimated yield
    estimated_yield = None
    if estimated_annual and current_price and current_price > 0:
        estimated_yield = round(estimated_annual / current_price * 100, 2)

    # Historical yields for comparison
    historical_yields = _compute_historical_yields(div_rows, current_price)

    # Plain-language summary
    plain_summary = _generate_summary(
        yearly_dividends, frequency, latest_cash_div, estimated_yield, is_estimated
    )

    return {
        "has_data": True,
        "yearly_dividends": yearly_dividends,
        "latest_cash_div": latest_cash_div,
        "estimated_annual": estimated_annual,
        "estimated_yield": estimated_yield,
        "is_estimated": is_estimated,
        "historical_yields": historical_yields,
        "plain_summary": plain_summary,
        "frequency": frequency,
    }


def _empty_result(msg: str | None = None) -> dict:
    """Return an empty dividend result."""
    if msg is None:
        msg = t("dividend.no_record")
    return {
        "has_data": False,
        "yearly_dividends": [],
        "latest_cash_div": None,
        "estimated_annual": None,
        "estimated_yield": None,
        "is_estimated": False,
        "historical_yields": [],
        "plain_summary": msg,
        "frequency": "none",
    }


def _build_yearly_dividends(div_rows: pd.DataFrame, cash_col: str) -> list[dict]:
    """Build list of yearly dividend dicts from raw rows."""
    yearly_dividends = []
    today = pd.Timestamp.now()
    for _, row in div_rows.head(8).iterrows():
        cash_div = float(row.get(cash_col, 0) or 0)
        stock_div = float(row.get("StockEarningsDistribution", 0) or 0)
        year_str = str(row.get("year", "")).strip() or "—"
        ex_date = str(row.get("CashExDividendTradingDate", "")).strip()
        pay_date = str(row.get("CashDividendPaymentDate", "")).strip()

        if pay_date and pay_date != "":
            try:
                pay_dt = pd.Timestamp(pay_date)
                status = t("dividend.status_paid") if pay_dt <= today else t("dividend.status_pending")
            except Exception:
                status = t("dividend.status_pending")
        else:
            status = t("dividend.status_pending")

        yearly_dividends.append({
            "year": year_str,
            "cash_div": cash_div,
            "stock_div": stock_div if stock_div > 0 else None,
            "ex_date": ex_date if ex_date else "—",
            "pay_date": pay_date if pay_date else "—",
            "status": status,
        })
    return yearly_dividends


def _classify_frequency(div_rows: pd.DataFrame) -> str:
    """Classify dividend payment frequency."""
    if div_rows.empty:
        return "none"

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
        # Check if years are consecutive (when sorted descending)
        years_str = year_counts.index.tolist()
        # Convert to integers: remove trailing '年' and convert to int
        try:
            years_int = [int(y.rstrip('年')) for y in years_str]
        except Exception:
            # If conversion fails, treat as irregular
            return "irregular"
        years_int_sorted = sorted(years_int, reverse=True)  # descending
        # Check if consecutive: each year should be previous_year - 1
        is_consecutive = all(
            years_int_sorted[i] - years_int_sorted[i+1] == 1
            for i in range(len(years_int_sorted)-1)
        )
        if is_consecutive and year_counts.min() >= 1:
            return "annual"
        return "irregular"
    return "irregular"
def _sum_cash_div(rows: pd.DataFrame, cash_col: str) -> float:
    """Safely sum cash dividend column, returning a scalar float."""
    return float(rows[cash_col].sum())


def _estimate_annual_proper(
    div_rows: pd.DataFrame, frequency: str
) -> tuple[float | None, bool]:
    """Estimate annual dividend using proper annualization logic.

    Returns (estimated_annual, is_estimated).
    is_estimated=True when the value is a projection, not an actual paid amount.

    Rules:
    - annual: use the most recent year's actual total (not estimated)
    - quarterly: use the most recent complete year's total (not *4).
      Only if we have partial-year data with known quarters, we use
      the latest complete year as the base and note it as estimated.
    - irregular: use the most recent complete year's total.
    """
    if div_rows.empty:
        return None, False

    cash_col = "CashEarningsDistribution"
    year_col = "year"

    if frequency == "annual":
        # Most recent year's actual payment — this is a real number
        latest_val = float(div_rows.iloc[0][cash_col])
        return round(latest_val, 2), False

    if frequency == "quarterly":
        # For quarterly payers, sum all payments within the most recent year
        # to get the actual annual total. Do NOT multiply a single quarter by 4.
        if year_col in div_rows.columns:
            years = div_rows[year_col].unique()
            if len(years) > 0:
                latest_year = years[0]
                year_rows = div_rows[div_rows[year_col] == latest_year]
                n_payments = len(year_rows)
                if n_payments >= 3:
                    # Likely complete or nearly complete year
                    total = _sum_cash_div(year_rows, cash_col)
                    is_est = n_payments < 4  # Still estimated if < 4 payments
                    return round(total, 2), is_est
                else:
                    # Incomplete year — use the previous complete year if available
                    if len(years) >= 2:
                        prev_year = years[1]
                        prev_rows = div_rows[div_rows[year_col] == prev_year]
                        total = _sum_cash_div(prev_rows, cash_col)
                        return round(total, 2), True  # Using prior year = estimated
                    # Only one year of data, partial — use what we have but mark estimated
                    total = _sum_cash_div(year_rows, cash_col)
                    return round(total, 2), True

        # Fallback: sum last 4 payments (assumes they span ~1 year)
        latest = div_rows.head(4)
        return round(_sum_cash_div(latest, cash_col), 2), True

    # Irregular: use the most recent year's total
    if year_col in div_rows.columns:
        years = div_rows[year_col].unique()
        if len(years) > 0:
            latest_year = years[0]
            year_rows = div_rows[div_rows[year_col] == latest_year]
            total = _sum_cash_div(year_rows, cash_col)
            return round(total, 2), False

    # Last resort: sum whatever we have
    latest = div_rows.head(4)
    return round(_sum_cash_div(latest, cash_col), 2), True


def _compute_historical_yields(
    div_rows: pd.DataFrame,
    current_price: float | None,
) -> list[dict]:
    """Compute historical annual dividends for the last 5 years.

    Returns list of {year, total_dividend, yield} dicts.
    """
    if div_rows.empty or current_price is None or current_price <= 0:
        return []

    cash_col = "CashEarningsDistribution"
    year_col = "year"

    if year_col not in div_rows.columns:
        return []

    # Group by year and sum dividends within each year
    yearly_totals: dict[str, float] = {}
    for _, row in div_rows.iterrows():
        y = str(row[year_col]).strip()
        if y not in yearly_totals:
            yearly_totals[y] = 0.0
        yearly_totals[y] += float(row[cash_col])

    # Sort by year descending, take top 5
    sorted_years = sorted(yearly_totals.keys(), reverse=True)[:5]

    result = []
    for y in sorted_years:
        total = round(yearly_totals[y], 2)
        if total > 0:
            yield_pct = round(total / current_price * 100, 2)
            result.append({
                "year": y,
                "total_dividend": total,
                "yield": yield_pct,
            })

    return result


def _generate_summary(
    yearly_dividends: list[dict],
    frequency: str,
    latest_cash_div: float | None,
    estimated_yield: float | None,
    is_estimated: bool = False,
) -> str:
    """Generate plain-language dividend summary."""
    if not yearly_dividends:
        return t("dividend.no_record_recent")

    n_years = len(set(d["year"] for d in yearly_dividends if d["year"] != "—"))
    est_label = t("dividend.estimated_label") if is_estimated else ""

    if frequency == "quarterly" and latest_cash_div:
        parts = [t("dividend.quarterly_dividend", amount=latest_cash_div)]
        if estimated_yield:
            parts.append(t("dividend.quarterly_yield", label=est_label, yield_pct=estimated_yield))
        return t("dividend.stable_years", n_years=n_years) + "，".join(parts)
    elif frequency == "annual" and latest_cash_div:
        parts = [t("dividend.annual_dividend", amount=latest_cash_div)]
        if estimated_yield:
            parts.append(t("dividend.annual_yield", label=est_label, yield_pct=estimated_yield))
        return t("dividend.stable_years", n_years=n_years) + "，".join(parts)
    elif frequency == "irregular":
        return t("dividend.irregular", amount=latest_cash_div or "—")
    else:
        return t("dividend.record_years", n_years=n_years)
