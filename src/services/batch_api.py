"""
Batch API utility — concurrent multi-stock data fetching.

Provides thread-pool-based batch fetching functions for prices and
financial data, following the existing service pattern:
pure functions, no Streamlit imports, client passed in.

Usage:
    from src.services.batch_api import batch_fetch_prices, batch_fetch_financials

    results = batch_fetch_prices(client, ["2330", "2317", "2454"])
    # results = {"2330": {...}, "2317": {...}, "2454": {...}}
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

logger = logging.getLogger(__name__)


def _fetch_price_single(client, stock_id: str) -> tuple[str, dict[str, Any] | None]:
    """Fetch daily price for a single stock. Returns (stock_id, result_or_None)."""
    try:
        df = client.get_daily_price(stock_id)
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            return stock_id, {
                "date": str(latest.get("date", "")),
                "open": float(latest.get("open", 0)),
                "high": float(latest.get("high", 0)),
                "low": float(latest.get("low", 0)),
                "close": float(latest.get("close", 0)),
                "volume": int(latest.get("volume", 0)),
            }
        logger.debug("batch_fetch_prices: empty result for %s", stock_id)
    except Exception as exc:
        logger.debug("batch_fetch_prices: failed for %s: %s", stock_id, exc)
    return stock_id, None


def _fetch_financial_single(client, stock_id: str) -> tuple[str, dict[str, Any] | None]:
    """Fetch financial data for a single stock. Returns (stock_id, result_or_None)."""
    try:
        income_df = client.get_financial_statement(stock_id)
        balance_df = client.get_balance_sheet(stock_id)
        revenue_df = client.get_monthly_revenue(stock_id)

        result: dict[str, Any] = {}

        if income_df is not None and len(income_df) > 0:
            result["financial_statement"] = income_df.to_dict("records")
        if balance_df is not None and len(balance_df) > 0:
            result["balance_sheet"] = balance_df.to_dict("records")
        if revenue_df is not None and len(revenue_df) > 0:
            result["monthly_revenue"] = revenue_df.to_dict("records")

        if result:
            return stock_id, result
        logger.debug("batch_fetch_financials: empty result for %s", stock_id)
    except Exception as exc:
        logger.debug("batch_fetch_financials: failed for %s: %s", stock_id, exc)
    return stock_id, None


def batch_fetch_prices(
    client,
    stock_ids: list[str],
    max_workers: int = 10,
) -> dict[str, dict]:
    """Fetch daily prices for multiple stocks concurrently.

    Args:
        client: FinMindClient instance.
        stock_ids: List of stock ID strings.
        max_workers: Max concurrent threads.

    Returns:
        Dict mapping stock_id to price dict (or omitted on failure).
    """
    results: dict[str, dict] = {}
    if not stock_ids:
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_fetch_price_single, client, sid): sid
            for sid in stock_ids
        }
        for future in as_completed(futures):
            sid, data = future.result()
            if data is not None:
                results[sid] = data

    logger.info(
        "batch_fetch_prices: fetched %d/%d stocks", len(results), len(stock_ids)
    )
    return results


def batch_fetch_financials(
    client,
    stock_ids: list[str],
    max_workers: int = 10,
) -> dict[str, dict]:
    """Fetch financial data for multiple stocks concurrently.

    Retrieves financial statements, balance sheets, and monthly revenue
    for each stock and returns them as a combined dict.

    Args:
        client: FinMindClient instance.
        stock_ids: List of stock ID strings.
        max_workers: Max concurrent threads.

    Returns:
        Dict mapping stock_id to financial data dict with keys:
            financial_statement, balance_sheet, monthly_revenue
        Stocks that fail are omitted.
    """
    results: dict[str, dict] = {}
    if not stock_ids:
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_fetch_financial_single, client, sid): sid
            for sid in stock_ids
        }
        for future in as_completed(futures):
            sid, data = future.result()
            if data is not None:
                results[sid] = data

    logger.info(
        "batch_fetch_financials: fetched %d/%d stocks", len(results), len(stock_ids)
    )
    return results
