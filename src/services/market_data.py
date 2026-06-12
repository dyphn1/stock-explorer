"""
Market Data Service — sector-level data aggregation.

Abstracts market-level data access so that pages like sector_heatmap
do not call FinMindClient or BatchAPI directly.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def get_all_stock_info(client) -> pd.DataFrame:
    """Fetch all stock info from FinMindClient.

    Returns:
        DataFrame with columns: stock_id, stock_name, industry_category
    """
    return client.get_stock_info()


def get_sector_list(client) -> list[str]:
    """Return a sorted list of all distinct industry categories (sectors).

    Args:
        client: FinMindClient instance.

    Returns:
        Sorted list of sector name strings.
    """
    try:
        info = get_all_stock_info(client)
    except Exception as exc:
        logger.warning("get_sector_list: failed to fetch stock info: %s", exc)
        return []

    industries = (
        info["industry_category"]
        .dropna()
        .unique()
    )
    return sorted([str(i).strip() for i in industries if str(i).strip()])


def get_sector_stocks(all_stock_info: pd.DataFrame) -> dict[str, list[str]]:
    """Build mapping of industry_category -> list of stock_ids.

    Args:
        all_stock_info: DataFrame with industry_category and stock_id columns.

    Returns:
        Dict mapping industry name to sorted list of stock IDs.
    """
    industries = (
        all_stock_info["industry_category"]
        .dropna()
        .unique()
    )
    industries = sorted([str(i).strip() for i in industries if str(i).strip()])

    sector_stocks: dict[str, list[str]] = {}
    for industry in industries:
        stocks_in_sector = all_stock_info[
            all_stock_info["industry_category"] == industry
        ]["stock_id"].tolist()
        if stocks_in_sector:
            sector_stocks[industry] = stocks_in_sector

    return sector_stocks


def get_sector_performance(
    client,
    sector: str,
    all_stock_info: pd.DataFrame | None = None,
) -> dict[str, Any] | None:
    """Return performance data for a single sector.

    Args:
        client: FinMindClient instance.
        sector: Sector name (industry_category value).
        all_stock_info: Optional pre-fetched stock info DataFrame.

    Returns:
        Dict with keys: avg_change, up, down, flat, count, stocks
        or None if no data available.
    """
    try:
        from src.data.batch_api import BatchAPI
    except ImportError:
        logger.error("get_sector_performance: BatchAPI not available")
        return None

    if all_stock_info is None:
        try:
            all_stock_info = get_all_stock_info(client)
        except Exception as exc:
            logger.warning("get_sector_performance: %s", exc)
            return None

    stock_ids = all_stock_info[
        all_stock_info["industry_category"] == sector
    ]["stock_id"].tolist()

    if not stock_ids:
        return None

    batch_api = BatchAPI(client)
    try:
        summaries = batch_api.get_watchlist_summaries(stock_ids)
    except Exception as exc:
        logger.warning("get_sector_performance: batch fetch failed: %s", exc)
        return None

    summary_map: dict[str, dict] = {s["stock_id"]: s for s in summaries}
    sector_stocks = {sector: stock_ids}
    metrics = compute_sector_metrics(summary_map, sector_stocks)
    return metrics.get(sector)


def get_top_movers(
    client,
    sector: str,
    n: int = 5,
    all_stock_info: pd.DataFrame | None = None,
) -> list[dict]:
    """Return the top n movers (by absolute change) in a sector.

    Args:
        client: FinMindClient instance.
        sector: Sector name.
        n: Number of top movers to return.
        all_stock_info: Optional pre-fetched stock info DataFrame.

    Returns:
        List of summary dicts sorted by abs(change) descending.
    """
    perf = get_sector_performance(client, sector, all_stock_info)
    if perf is None:
        return []

    stocks = perf.get("stocks", [])
    stocks.sort(key=lambda s: abs(s.get("change") or 0), reverse=True)
    return stocks[:n]


def get_all_summaries(
    client,
    all_stock_info: pd.DataFrame | None = None,
    batch_size: int = 50,
    progress_callback=None,
) -> tuple[list[dict], dict[str, dict]]:
    """Fetch watchlist summaries for all stocks with optional progress reporting.

    This is the batch-fetching helper that pages can use to get all stock
    summaries without directly instantiating BatchAPI.

    Args:
        client: FinMindClient instance.
        all_stock_info: Optional pre-fetched stock info DataFrame.
        batch_size: Number of stocks per batch.
        progress_callback: Optional callback(phase_str, fraction) for progress UI.

    Returns:
        Tuple of (summaries_list, summary_map) where summary_map is
        dict mapping stock_id -> summary dict.
    """
    try:
        from src.data.batch_api import BatchAPI
    except ImportError:
        logger.error("get_all_summaries: BatchAPI not available")
        return [], {}

    if all_stock_info is None:
        try:
            all_stock_info = get_all_stock_info(client)
        except Exception as exc:
            logger.warning("get_all_summaries: failed to get stock info: %s", exc)
            return [], {}

    batch_api = BatchAPI(client)
    all_stock_ids = sorted(all_stock_info["stock_id"].unique())
    total_stocks = len(all_stock_ids)

    summaries: list[dict] = []
    for i in range(0, len(all_stock_ids), batch_size):
        batch_ids = all_stock_ids[i: i + batch_size]
        try:
            batch_summaries = batch_api.get_watchlist_summaries(batch_ids)
            summaries.extend(batch_summaries)
        except Exception as exc:
            logger.debug("get_all_summaries: batch %d failed: %s", i, exc)

        if progress_callback:
            fraction = min((i + batch_size) / total_stocks, 1.0)
            progress_callback(fraction)

    summary_map: dict[str, dict] = {s["stock_id"]: s for s in summaries}
    return summaries, summary_map


def compute_sector_metrics(
    summary_map: dict[str, dict],
    sector_stocks: dict[str, list[str]],
) -> dict[str, dict[str, Any]]:
    """Compute per-sector performance metrics from stock summaries.

    Args:
        summary_map: Dict mapping stock_id -> summary dict (from BatchAPI)
        sector_stocks: Dict mapping industry -> list of stock_ids

    Returns:
        Dict mapping sector name to metrics dict with keys:
        avg_change, up, down, flat, count, stocks
    """
    sector_metrics: dict[str, dict[str, Any]] = {}
    for sector, stock_ids in sector_stocks.items():
        changes = []
        stock_data = []
        for sid in stock_ids:
            s = summary_map.get(sid)
            if s:
                chg = s.get("change")
                if chg is not None:
                    changes.append(chg)
                stock_data.append(s)

        if changes:
            avg_change = float(np.mean(changes))
            up = sum(1 for c in changes if c > 0)
            down = sum(1 for c in changes if c < 0)
            flat = len(changes) - up - down
            sector_metrics[sector] = {
                "avg_change": avg_change,
                "up": up,
                "down": down,
                "flat": flat,
                "count": len(changes),
                "stocks": stock_data,
            }

    return sector_metrics


def get_sector_grid_data(
    client,
    all_stock_info: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Return all data needed for the sector grid display.

    This is a convenience function that combines stock info fetching,
    batch summary retrieval, and sector metric computation into one call.

    Args:
        client: FinMindClient instance.
        all_stock_info: Optional pre-fetched stock info DataFrame.

    Returns:
        Dict with keys:
            all_stock_info: DataFrame of all stock info
            sector_stocks: Dict mapping sector -> list of stock_ids
            sector_metrics: Dict mapping sector -> metrics dict
            summary_map: Dict mapping stock_id -> summary dict
    """
    if all_stock_info is None:
        all_stock_info = get_all_stock_info(client)

    sector_stocks = get_sector_stocks(all_stock_info)
    _, summary_map = get_all_summaries(client, all_stock_info)
    sector_metrics = compute_sector_metrics(summary_map, sector_stocks)

    return {
        "all_stock_info": all_stock_info,
        "sector_stocks": sector_stocks,
        "sector_metrics": sector_metrics,
        "summary_map": summary_map,
    }
