"""
Scenario Calculator — C200
Calculate what-if investment scenarios.

Pure Python service — no Streamlit imports.
Uses FinMindClient for historical price and dividend data.

i18n strategy: this service returns error keys (e.g. "scenario.before_ipo").
The page layer calls t() to resolve them.
"""
from __future__ import annotations

import logging
import math
from datetime import datetime
from typing import TypedDict

import pandas as pd

logger = logging.getLogger(__name__)


class ScenarioResult(TypedDict):
    """Result of a what-if calculation."""
    start_date: str
    end_date: str
    start_price: float
    end_price: float
    shares: float           # shares bought with input amount
    total_return: float     # percentage
    absolute_return: float  # dollar amount (TWD)
    dividend_income: float  # accumulated dividends
    annualized_return: float
    max_drawdown: float     # maximum drawdown during the period (percentage, negative)
    days_held: int
    is_estimated: bool      # True if data incomplete
    error_key: str | None   # i18n key for error message, None if success


def _get_price_on_date(price_df: pd.DataFrame, target_date: str) -> float | None:
    """Get the closing price on or nearest before target_date.

    Args:
        price_df: DataFrame with 'date' and 'close' columns.
        target_date: "YYYY-MM-DD"

    Returns:
        Closing price, or None if no data available.
    """
    if price_df is None or price_df.empty:
        return None
    df = price_df.copy()
    df["date"] = pd.to_datetime(df["date"].astype(str).str[:10])
    target = pd.to_datetime(target_date)
    mask: pd.Series = df["date"] <= target
    if not mask.any():
        return None
    filtered = df.loc[mask].sort_values(by="date")
    return float(filtered.iloc[-1]["close"])


def _calc_max_drawdown(price_df: pd.DataFrame, start_date: str, end_date: str) -> float:
    """Calculate maximum drawdown between two dates.

    Returns negative percentage (e.g. -45.0 for 45% drawdown).
    Returns 0.0 if insufficient data.
    """
    if price_df is None or price_df.empty:
        return 0.0
    df = price_df.copy()
    df["date"] = pd.to_datetime(df["date"].astype(str).str[:10])
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    mask: pd.Series = (df["date"] >= start) & (df["date"] <= end)
    period = df.loc[mask].sort_values(by="date")
    if period.empty:
        return 0.0
    prices = period["close"].to_numpy()
    peak = float(prices[0])
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (p - peak) / peak * 100  # negative
        if dd < max_dd:
            max_dd = dd
    return round(max_dd, 2)


def _calc_dividend_income(
    dividend_df: pd.DataFrame,
    start_date: str,
    end_date: str,
    shares: float,
) -> float:
    """Calculate accumulated dividends between two dates.

    Args:
        dividend_df: DataFrame with dividend data.
        start_date: "YYYY-MM-DD"
        end_date: "YYYY-MM-DD"
        shares: Number of shares held.

    Returns:
        Total dividend income in TWD.
    """
    if dividend_df is None or dividend_df.empty or shares <= 0:
        return 0.0

    total = 0.0
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    for _, row in dividend_df.iterrows():
        try:
            pay_date = None
            for col in ("ex_dividend_date", "cash_dividend_date", "date", "pay_date"):
                if col in row.index and pd.notna(row[col]):
                    pay_date = pd.to_datetime(str(row[col])[:10])
                    break
            if pay_date is None:
                continue
            pay_dt = pd.Timestamp(pay_date)
            if start <= pay_dt <= end:
                div_per_share = 0.0
                for col in ("cash_dividend", "dividend", "cash_earnings_distributions"):
                    if col in row.index and pd.notna(row[col]):
                        div_per_share = float(row[col])
                        break
                total += div_per_share * shares
        except (ValueError, TypeError):
            continue

    return round(total, 2)



def _get_price_on_or_after(price_df: pd.DataFrame, target_date: str) -> float | None:
    """Get the closing price on or nearest after target_date.

    Args:
        price_df: DataFrame with 'date' and 'close' columns.
        target_date: "YYYY-MM-DD"

    Returns:
        Closing price, or None if no data available.
    """
    if price_df is None or price_df.empty:
        return None
    df = price_df.copy()
    df["date"] = pd.to_datetime(df["date"].astype(str).str[:10])
    target = pd.to_datetime(target_date)
    mask: pd.Series = df["date"] >= target
    if not mask.any():
        return None
    filtered = df.loc[mask].sort_values(by="date")
    return float(filtered.iloc[0]["close"])


def _get_price_on_or_before(price_df: pd.DataFrame, target_date: str) -> float | None:
    """Get the closing price on or nearest before target_date.

    Args:
        price_df: DataFrame with 'date' and 'close' columns.
        target_date: "YYYY-MM-DD"

    Returns:
        Closing price, or None if no data available.
    """
    return _get_price_on_date(price_df, target_date)


def _get_first_trading_date(price_df: pd.DataFrame) -> str | None:
    """Get the first trading date in the DataFrame.

    Args:
        price_df: DataFrame with 'date' column.

    Returns:
        First date as "YYYY-MM-DD" string, or None if no data.
    """
    if price_df is None or price_df.empty:
        return None
    df = price_df.copy()
    df["date"] = pd.to_datetime(df["date"].astype(str).str[:10])
    df = df.sort_values(by="date")
    return str(df.iloc[0]["date"])[:10]


def _parse_date(date_string: str) -> datetime:
    """Parse date string to datetime object.
    
    Handles formats like "YYYY-MM-DD" and "YYYY-MM-DDTHH:MM:SS".
    
    Args:
        date_string: Date string to parse.
        
    Returns:
        datetime object.
    """
    try:
        # Try parsing with time component first
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        # Fall back to date-only format
        return datetime.strptime(date_string, "%Y-%m-%d")

def calculate_scenario(
    stock_id: str,
    start_date: str,
    investment_amount: float,
    end_date: str | None = None,
    include_dividends: bool = True,
    client=None,
) -> ScenarioResult:
    """Calculate what-if investment scenario.

    Pure calculation — no LLM.
    Uses FinMindClient for historical price and dividend data.
    Handles edge cases: pre-IPO dates, missing data, future dates.

    Args:
        stock_id: Stock ID (e.g. "2330").
        start_date: Investment date "YYYY-MM-DD".
        investment_amount: Amount to invest in TWD.
        end_date: End date for calculation (default: latest available, or today).
        include_dividends: Whether to include dividend income.
        client: FinMindClient instance.

    Returns:
        ScenarioResult with all calculation fields.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = today

    # Validate dates
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.invalid_date",
        )

    if start_dt >= end_dt:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.invalid_range",
        )

    if start_dt > datetime.now():
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.future_date",
        )

    # Fetch price data
    try:
        price_df = client.get_daily_price(stock_id) if client else None
    except Exception as exc:
        logger.warning("scenario_calculator: failed to fetch price for %s: %s", stock_id, exc)
        price_df = None

    if price_df is None or price_df.empty:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.no_data",
        )

    # Get start price
    start_price = _get_price_on_date(price_df, start_date)
    if start_price is None:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.before_ipo",
        )

    # Get end price
    actual_end_date = end_date
    end_price = _get_price_on_date(price_df, end_date)
    is_estimated = end_date > today
    if end_price is None:
        # Fallback: use latest available price
        df_sorted = price_df.copy()
        df_sorted["date"] = pd.to_datetime(df_sorted["date"].astype(str).str[:10])
        df_sorted = df_sorted.sort_values(by="date")
        end_price = float(df_sorted.iloc[-1]["close"])
        actual_end_date = str(df_sorted.iloc[-1]["date"])[:10]
        is_estimated = True

    if start_price <= 0:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=0, end_price=0, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=False, error_key="scenario.no_data",
        )

    # Calculate shares (whole shares only)
    shares = math.floor(investment_amount / start_price)

    if shares <= 0:
        return ScenarioResult(
            start_date=start_date, end_date=end_date,
            start_price=start_price, end_price=end_price, shares=0,
            total_return=0, absolute_return=0, dividend_income=0,
            annualized_return=0, max_drawdown=0, days_held=0,
            is_estimated=is_estimated, error_key="scenario.amount_too_small",
        )

    # Calculate returns
    invested = start_price * shares
    current_value = end_price * shares

    # Dividend income
    dividend_income = 0.0
    if include_dividends and client is not None:
        try:
            dividend_df = client.get_dividend(stock_id)
            if dividend_df is not None and not dividend_df.empty:
                dividend_income = _calc_dividend_income(dividend_df, start_date, actual_end_date, shares)
        except Exception as exc:
            logger.warning("scenario_calculator: dividend fetch failed for %s: %s", stock_id, exc)

    absolute_return = current_value + dividend_income - invested
    total_return = (absolute_return / invested) * 100 if invested > 0 else 0

    # Days held
    actual_end_dt = datetime.strptime(actual_end_date[:10], "%Y-%m-%d")
    days_held = max((actual_end_dt - start_dt).days, 1)

    # Annualized return
    if days_held >= 365:
        annualized_return = ((1 + total_return / 100) ** (365.0 / days_held) - 1) * 100
    else:
        # For periods less than 1 year, still annualize
        annualized_return = ((1 + total_return / 100) ** (365.0 / days_held) - 1) * 100

    # Max drawdown
    max_drawdown = _calc_max_drawdown(price_df, start_date, actual_end_date)

    return ScenarioResult(
        start_date=start_date,
        end_date=actual_end_date,
        start_price=round(start_price, 2),
        end_price=round(end_price, 2),
        shares=float(shares),
        total_return=round(total_return, 2),
        absolute_return=round(absolute_return, 2),
        dividend_income=round(dividend_income, 2),
        annualized_return=round(annualized_return, 2),
        max_drawdown=max_drawdown,
        days_held=days_held,
        is_estimated=is_estimated,
        error_key=None,
    )
