"""Industry benchmark data and shared benchmark-fetching utilities.

Provides:
- get_industry_benchmarks() — loads INDUSTRY_BENCHMARKS from YAML
- fetch_benchmark_health_scores() — shared logic for fetching benchmark
  company health scores (extracted from duplicated inline logic in
  _summary.py and _health.py)
"""
from __future__ import annotations

import yaml
from pathlib import Path

from src.services.health_scoring import compute_health_scores


_yaml_path = Path(__file__).resolve().parent.parent / "data" / "industry_benchmarks.yaml"

_cache: dict[str, tuple[str, str]] | None = None


def get_industry_benchmarks() -> dict[str, tuple[str, str]]:
    """Load industry → (stock_id, stock_name) mapping from YAML.

    Returns a dict like:
        {"半導體業": ("2330", "台積電"), ...}
    Caches after first load.
    """
    global _cache
    if _cache is not None:
        return _cache

    with open(_yaml_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    _cache = {}
    for industry_name, entry in raw.items():
        if isinstance(entry, list) and len(entry) == 2:
            _cache[industry_name] = (str(entry[0]), str(entry[1]))

    return _cache


def fetch_benchmark_health_scores(client, industry: str, stock_id: str):
    """Fetch health scores for the industry benchmark company.

    This is the shared version of the logic that was duplicated between
    _health.py (_fetch_benchmark_health_scores) and _summary.py (inline
    inside _render_story_card).

    Returns a dict of dimension → score (0-100), or None if unavailable.
    """
    benchmarks = get_industry_benchmarks()

    if not industry or industry not in benchmarks:
        return None

    bench_id, bench_name = benchmarks[industry]

    # Don't benchmark against self
    if bench_id == stock_id:
        return None

    try:
        bench_per_pbr = client.get_latest_per_pbr(bench_id)
        bench_financial = client.get_financial_statement(bench_id)
        bench_balance = client.get_balance_sheet(bench_id)
        bench_revenue = client.get_monthly_revenue(bench_id)

        # Build extra_metrics dict from financial/balance data
        bench_extra = {}

        rev_col = None
        gp_col = None
        op_col = None
        ni_col = None
        latest = None
        if bench_financial is not None and len(bench_financial) > 0:
            def _find_col(df, keywords):
                for col in df.columns:
                    for kw in keywords:
                        if kw in str(col):
                            return col
                return None

            rev_col = _find_col(bench_financial, ["營業收入", "Revenue", "revenue"])
            gp_col = _find_col(bench_financial, ["營業毛利", "Gross_Profit", "gross_profit"])
            op_col = _find_col(bench_financial, ["營業利益", "Operating_Income", "operating_income"])
            ni_col = _find_col(bench_financial, ["淨利", "Net_Income", "net_income"])

            latest = bench_financial.iloc[-1]
            if rev_col and gp_col:
                rev = latest.get(rev_col)
                gp = latest.get(gp_col)
                if rev and gp and float(rev) > 0:
                    bench_extra["gross_margin"] = float(gp) / float(rev) * 100

            if rev_col and ni_col:
                rev = latest.get(rev_col)
                ni = latest.get(ni_col)
                if rev and ni and float(rev) > 0:
                    bench_extra["net_margin"] = float(ni) / float(rev) * 100

            # Revenue YoY
            try:
                if rev_col and len(bench_financial) >= 2:
                    curr_rev = float(latest[rev_col]) if latest.get(rev_col) else None
                    prev_rev = float(bench_financial.iloc[-2][rev_col]) if bench_financial.iloc[-2].get(rev_col) else None
                    if curr_rev and prev_rev and prev_rev > 0:
                        bench_extra["revenue_yoy"] = (curr_rev - prev_rev) / abs(prev_rev) * 100
            except Exception:
                pass
        else:
            latest = None

        # Debt ratio from balance sheet
        if bench_balance is not None and len(bench_balance) > 0:
            def _find_bal_col(df, keywords):
                for col in df.columns:
                    for kw in keywords:
                        if kw in str(col):
                            return col
                return None

            debt_col = _find_bal_col(bench_balance, ["負債總計", "Total_Liabilities", "total_liabilities"])
            asset_col = _find_bal_col(bench_balance, ["資產總計", "Total_Assets", "total_assets"])
            current_asset_col = _find_bal_col(bench_balance, ["流動資產", "Current_Assets", "current_assets"])
            current_liab_col = _find_bal_col(bench_balance, ["流動負債", "Current_Liabilities", "current_liabilities"])
            equity_col = _find_bal_col(bench_balance, ["權益總計", "Total_Equity", "total_equity"])

            bal_latest = bench_balance.iloc[-1]

            if debt_col and asset_col:
                debt = bal_latest.get(debt_col)
                asset = bal_latest.get(asset_col)
                if debt and asset and float(asset) > 0:
                    bench_extra["debt_ratio"] = float(debt) / float(asset) * 100

            if current_asset_col and current_liab_col:
                ca = bal_latest.get(current_asset_col)
                cl = bal_latest.get(current_liab_col)
                if ca and cl and float(cl) > 0:
                    bench_extra["current_ratio"] = float(ca) / float(cl)

            # ROE: Net Income / Equity
            if equity_col and ni_col:
                try:
                    ni_val = latest.get(ni_col) if bench_financial is not None and len(bench_financial) > 0 else None
                    eq_val = bal_latest.get(equity_col)
                    if ni_val and eq_val and float(eq_val) > 0:
                        bench_extra["roe"] = float(ni_val) / float(eq_val) * 100
                except Exception:
                    pass

        scores = compute_health_scores(
            extra_metrics=bench_extra,
            latest_per_pbr=bench_per_pbr,
            financial_df=bench_financial,
            monthly_revenue=bench_revenue,
        )
        return scores if scores else None

    except Exception:
        return None
