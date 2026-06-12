"""
Batch API utility — fetch data for multiple stocks in one call.

Avoids N+1 query patterns by collecting all requested stock IDs
and fetching each dataset once (using the shared FinMindClient cache).

Usage:
    from src.data.batch_api import BatchAPI
    api = BatchAPI(client)
    results = api.get_latest_prices(["2330", "2317", "2454"])
    # results = {"2330": {...}, "2317": {...}, "2454": {...}}
"""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class BatchAPI:
    """Batch API utility that wraps FinMindClient for multi-stock fetching.

    Each method accepts a list of stock_ids and returns a dict keyed by
    stock_id.  Missing / error results are simply omitted from the dict
    (no exception raised for individual failures).
    """

    def __init__(self, client):
        """
        Args:
            client: A FinMindClient instance (shared, with cache).
        """
        self._client = client

    # ── latest price ──────────────────────────────────────

    def get_latest_prices(
        self, stock_ids: list[str]
    ) -> dict[str, dict]:
        """Fetch latest price dict for each stock_id.

        Returns:
            {stock_id: {date, close, open, high, low, volume, change}}
            Stocks that fail are omitted.
        """
        results: dict[str, dict] = {}
        for sid in stock_ids:
            try:
                price = self._client.get_latest_price(sid)
                if price:
                    results[sid] = price
            except Exception:
                logger.debug("BatchAPI: failed to get latest price for %s", sid)
        return results

    # ── daily price (full DataFrame) ──────────────────────

    def get_daily_prices(
        self,
        stock_ids: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Fetch daily price DataFrame for each stock_id.

        Returns:
            {stock_id: DataFrame} — empty dict entries omitted.
        """
        results: dict[str, pd.DataFrame] = {}
        for sid in stock_ids:
            try:
                df = self._client.get_daily_price(sid, start_date, end_date)
                if df is not None and len(df) > 0:
                    results[sid] = df
            except Exception:
                logger.debug("BatchAPI: failed to get daily price for %s", sid)
        return results

    # ── PER / PBR ─────────────────────────────────────────

    def get_latest_per_pbrs(
        self, stock_ids: list[str], start_date: str | None = None
    ) -> dict[str, dict]:
        """Fetch latest PER/PBR dict for each stock_id.

        Returns:
            {stock_id: {date, PER, PBR, dividend_yield}}
        """
        results: dict[str, dict] = {}
        for sid in stock_ids:
            try:
                data = self._client.get_latest_per_pbr(sid, start_date)
                if data:
                    results[sid] = data
            except Exception:
                logger.debug("BatchAPI: failed to get PER/PBR for %s", sid)
        return results

    # ── stock info (single cached call) ───────────────────

    def get_stock_infos(
        self, stock_ids: list[str]
    ) -> dict[str, dict]:
        """Fetch stock info for each stock_id.

        Uses the already-cached full-universe call internally, so
        multiple IDs incur only one API hit.

        Returns:
            {stock_id: {stock_name, industry_category, ...}}
        """
        results: dict[str, dict] = {}
        try:
            df = self._client.get_stock_info()
            if df is None or df.empty:
                return results
            for sid in stock_ids:
                match = df[df["stock_id"] == sid]
                if len(match) > 0:
                    row = match.iloc[0]
                    results[sid] = {
                        "stock_id": sid,
                        "stock_name": row.get("stock_name", sid),
                        "industry_category": row.get("industry_category", ""),
                    }
        except Exception:
            logger.debug("BatchAPI: failed to get stock infos")
        return results

    # ── monthly revenue ───────────────────────────────────

    def get_monthly_revenues(
        self,
        stock_ids: list[str],
        start_date: str | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Fetch monthly revenue DataFrame for each stock_id.

        Returns:
            {stock_id: DataFrame}
        """
        results: dict[str, pd.DataFrame] = {}
        for sid in stock_ids:
            try:
                df = self._client.get_monthly_revenue(sid, start_date)
                if df is not None and len(df) > 0:
                    results[sid] = df
            except Exception:
                logger.debug("BatchAPI: failed to get monthly revenue for %s", sid)
        return results

    # ── financial statement ───────────────────────────────

    def get_financial_statements(
        self,
        stock_ids: list[str],
        start_date: str | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Fetch financial statement DataFrame for each stock_id.

        Returns:
            {stock_id: DataFrame}
        """
        results: dict[str, pd.DataFrame] = {}
        for sid in stock_ids:
            try:
                df = self._client.get_financial_statement(sid, start_date)
                if df is not None and len(df) > 0:
                    results[sid] = df
            except Exception:
                logger.debug("BatchAPI: failed to get financial statement for %s", sid)
        return results

    # ── balance sheet ─────────────────────────────────────

    def get_balance_sheets(
        self,
        stock_ids: list[str],
        start_date: str | None = None,
    ) -> dict[str, pd.DataFrame]:
        """Fetch balance sheet DataFrame for each stock_id.

        Returns:
            {stock_id: DataFrame}
        """
        results: dict[str, pd.DataFrame] = {}
        for sid in stock_ids:
            try:
                df = self._client.get_balance_sheet(sid, start_date)
                if df is not None and len(df) > 0:
                    results[sid] = df
            except Exception:
                logger.debug("BatchAPI: failed to get balance sheet for %s", sid)
        return results

    # ── convenience: summary for watchlist ────────────────

    def get_watchlist_summaries(
        self,
        stock_ids: list[str],
    ) -> list[dict]:
        """Fetch a lightweight summary for each stock (price + info).

        This is the primary method for watchlist / heatmap pages that
        need one data point per stock without N+1 API calls.

        Returns:
            List of dicts with keys:
                stock_id, stock_name, industry_category,
                latest_price, change
        """
        infos = self.get_stock_infos(stock_ids)
        prices = self.get_latest_prices(stock_ids)

        summaries: list[dict] = []
        for sid in stock_ids:
            info = infos.get(sid, {})
            price = prices.get(sid, {})
            summaries.append({
                "stock_id": sid,
                "stock_name": info.get("stock_name", sid),
                "industry_category": info.get("industry_category", ""),
                "latest_price": price.get("close"),
                "change": price.get("change"),
            })
        return summaries
