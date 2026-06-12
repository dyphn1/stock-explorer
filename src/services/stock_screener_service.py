"""
Stock Screener Service — C42
Beginner-friendly stock discovery / screening logic.
No streamlit imports.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def get_all_stocks_with_metrics(client: Any) -> pd.DataFrame:
    """Fetch all stocks with key metrics for screening.

    Uses BatchAPI for efficient multi-stock fetching.

    Args:
        client: FinMindClient instance.

    Returns:
        DataFrame with columns: stock_id, stock_name, industry_category,
        per, pbr, dividend_yield, revenue_yoy, change
    """
    try:
        from src.data.batch_api import BatchAPI
        batch_api = BatchAPI(client)
    except ImportError:
        batch_api = None

    # Get all stock info (single cached call)
    try:
        all_info = client.get_stock_info()
    except Exception as exc:
        logger.warning("Failed to get stock info: %s", exc)
        return pd.DataFrame()

    if all_info is None or all_info.empty:
        return pd.DataFrame()

    # Limit to first 300 stocks to avoid excessive API calls
    all_info = all_info.sort_values("stock_id").head(300).copy()
    stock_ids = all_info["stock_id"].tolist()

    # Fetch PER/PBR and prices
    per_pbr_map = {}
    price_map = {}

    if batch_api is not None:
        try:
            per_pbr_map = batch_api.get_latest_per_pbrs(stock_ids)
        except Exception as exc:
            logger.warning("BatchAPI get_latest_per_pbrs failed: %s", exc)
        try:
            price_map = batch_api.get_latest_prices(stock_ids)
        except Exception as exc:
            logger.warning("BatchAPI get_latest_prices failed: %s", exc)
    else:
        for sid in stock_ids:
            try:
                pp = client.get_latest_per_pbr(sid)
                if pp:
                    per_pbr_map[sid] = pp
            except Exception:
                pass
            try:
                pr = client.get_latest_price(sid)
                if pr:
                    price_map[sid] = pr
            except Exception:
                pass

    # Build result DataFrame
    records = []
    for _, row in all_info.iterrows():
        sid = row["stock_id"]
        pp = per_pbr_map.get(sid, {})
        pr = price_map.get(sid, {})

        # Calculate revenue YoY from monthly revenue if available
        revenue_yoy = None
        try:
            rev_df = client.get_monthly_revenue(sid)
            if rev_df is not None and len(rev_df) >= 13:
                latest = rev_df.iloc[-1].get("revenue", 0) or 0
                prev_year = rev_df.iloc[-13].get("revenue", 0) or 0
                if prev_year > 0:
                    revenue_yoy = ((latest - prev_year) / prev_year) * 100
        except Exception:
            pass

        records.append({
            "stock_id": sid,
            "stock_name": row.get("stock_name", sid),
            "industry_category": row.get("industry_category", ""),
            "per": pp.get("PER"),
            "pbr": pp.get("PBR"),
            "dividend_yield": pp.get("dividend_yield"),
            "revenue_yoy": revenue_yoy,
            "change": pr.get("change"),
            "close": pr.get("close"),
        })

    return pd.DataFrame(records)


def apply_preset_filter(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    """Apply a preset filter to the stocks DataFrame.

    Args:
        df: Stocks DataFrame from get_all_stocks_with_metrics.
        preset: One of "dividend", "growth", "value".

    Returns:
        Filtered DataFrame.
    """
    if df.empty:
        return df

    if preset == "dividend":
        # 穩定收息: dividend yield > 3%, low volatility (abs change < 3%)
        mask = (
            (df["dividend_yield"] > 3.0) &
            (df["dividend_yield"].notna())
        )
        if "change" in df.columns:
            mask = mask & (df["change"].abs() < 3.0)
        return df[mask].copy()

    elif preset == "growth":
        # 成長潛力: revenue growth > 10%
        mask = (
            (df["revenue_yoy"] > 10.0) &
            (df["revenue_yoy"].notna())
        )
        return df[mask].copy()

    elif preset == "value":
        # 便宜估值: PER < 15, PBR < 2
        mask = (
            (df["per"] < 15) &
            (df["per"].notna()) &
            (df["pbr"] < 2) &
            (df["pbr"].notna())
        )
        return df[mask].copy()

    return df.copy()


def apply_custom_filter(
    df: pd.DataFrame,
    filters: dict[str, Any],
) -> pd.DataFrame:
    """Apply custom filters to the stocks DataFrame.

    Args:
        df: Stocks DataFrame.
        filters: Dict with optional keys:
            industry (str or None),
            per_min (float or None), per_max (float or None),
            div_min (float or None), div_max (float or None),
            revenue_growth (bool),
    """
    if df.empty:
        return df

    result = df.copy()

    industry = filters.get("industry")
    if industry and industry != "全部":
        result = result[result["industry_category"] == industry]

    per_min = filters.get("per_min")
    per_max = filters.get("per_max")
    if per_min is not None:
        result = result[(result["per"] >= per_min) | (result["per"].isna())]
    if per_max is not None:
        result = result[(result["per"] <= per_max) | (result["per"].isna())]

    div_min = filters.get("div_min")
    div_max = filters.get("div_max")
    if div_min is not None:
        result = result[(result["dividend_yield"] >= div_min) | (result["dividend_yield"].isna())]
    if div_max is not None:
        result = result[(result["dividend_yield"] <= div_max) | (result["dividend_yield"].isna())]

    if filters.get("revenue_growth"):
        result = result[result["revenue_yoy"] > 0]

    return result


def format_screening_results(filtered_df: pd.DataFrame) -> list[dict]:
    """Format filtered results for display.

    Args:
        filtered_df: Filtered DataFrame.

    Returns:
        List of dicts with display-ready fields.
    """
    results = []
    for _, row in filtered_df.head(20).iterrows():
        per_str = f"PER {row['per']:.1f}" if pd.notna(row.get("per")) else "PER —"
        pbr_str = f"PBR {row['pbr']:.2f}" if pd.notna(row.get("pbr")) else "PBR —"
        div_str = f"殖利率 {row['dividend_yield']:.2f}%" if pd.notna(row.get("dividend_yield")) else "殖利率 —"

        # Pick the most relevant metric as "key metric"
        if pd.notna(row.get("dividend_yield")) and row["dividend_yield"] > 3:
            key_metric = f"殖利率 {row['dividend_yield']:.2f}%"
        elif pd.notna(row.get("revenue_yoy")) and row["revenue_yoy"] > 10:
            key_metric = f"營收成長 {row['revenue_yoy']:.1f}%"
        elif pd.notna(row.get("per")) and row["per"] < 15:
            key_metric = f"PER {row['per']:.1f}"
        else:
            key_metric = div_str

        results.append({
            "stock_id": row["stock_id"],
            "stock_name": row.get("stock_name", row["stock_id"]),
            "industry": row.get("industry_category", "—"),
            "key_metric": key_metric,
            "per_str": per_str,
            "pbr_str": pbr_str,
            "div_str": div_str,
        })
    return results
