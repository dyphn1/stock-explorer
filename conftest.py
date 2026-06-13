"""
Global pytest fixtures for Stock Explorer test suite.

Provides:
- project_root          → Path to the project root
- sample_stock_data     → Mimics get_stock_data() return dict
- mock_finmind_client   → FinMindClient with real API calls replaced
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


# ── project root ──────────────────────────────────────────────

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory (stock-explorer/)."""
    return Path(__file__).resolve().parent


# ── sample data builders ──────────────────────────────────────

def _make_daily_price_df(n: int = 30) -> pd.DataFrame:
    """Build a daily_price DataFrame with realistic columns."""
    dates = pd.date_range(end=datetime.now(), periods=n, freq="D")
    base_price = 100.0
    closes = [base_price + i * 0.5 for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "close": closes,
        "open": [c - 0.5 for c in closes],
        "max": [c + 1.0 for c in closes],
        "min": [c - 1.0 for c in closes],
        "Trading_Volume": [1_000_000 + i * 10_000 for i in range(n)],
        "spread": [0.5] * n,
    })


def _make_monthly_revenue_df(n: int = 24) -> pd.DataFrame:
    """Build a monthly_revenue DataFrame."""
    dates = pd.date_range(end=datetime.now(), periods=n, freq="ME")
    base_rev = 50.0  # 億
    revenues = [base_rev + i * 2.0 for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "revenue": revenues,
    })


def _make_news_df(n: int = 3) -> pd.DataFrame:
    """Build a news DataFrame."""
    titles = [
        "營收創歷史新高",
        "獲得大廠訂單合作",
        "董事會決議股利分派",
    ][:n]
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n)]
    return pd.DataFrame({
        "title": titles,
        "date": dates,
    })


def _make_peers() -> list[str]:
    """Return a small list of peer stock IDs."""
    return ["2454", "2317", "1101"]


@pytest.fixture
def sample_stock_data() -> dict:
    """
    Return a dict mimicking the structure from get_stock_data() in _router_base.py.

    Keys:
        stock_id        (str)
        stock_name      (str)
        industry        (str)
        daily_price     (pd.DataFrame)
        monthly_revenue (pd.DataFrame)
        news            (pd.DataFrame)
        peers           (list)
    """
    return {
        "stock_id": "2330",
        "stock_name": "台積電",
        "industry": "半導體業",
        "daily_price": _make_daily_price_df(),
        "monthly_revenue": _make_monthly_revenue_df(),
        "news": _make_news_df(),
        "peers": _make_peers(),
    }


# ── mock FinMind client ───────────────────────────────────────

@pytest.fixture
def mock_finmind_client() -> MagicMock:
    """
    Return a mock FinMindClient that avoids real API calls.

    All get_* methods return empty DataFrames by default.
    Use monkeypatching or configure return_value per test.
    """
    client = MagicMock(name="FinMindClient")

    # Stock info with a valid row so gate-check passes
    client.get_stock_info.return_value = pd.DataFrame([{
        "stock_id": "2330",
        "stock_name": "台積電",
        "industry_category": "半導體業",
    }])

    # Most data methods return empty DataFrames (safe no-op)
    empty_df = pd.DataFrame()
    for method_name in [
        "get_latest_price",
        "get_latest_per_pbr",
        "get_monthly_revenue",
        "get_daily_price",
        "get_financial_statement",
        "get_news",
        "get_institutional_investors",
        "get_balance_sheet",
        "get_cash_flow",
        "get_dividend",
    ]:
        getattr(client, method_name).return_value = empty_df

    client.get_stock_name.return_value = "台積電"
    client.get_industry.return_value = "半導體業"

    return client


# ── SAMPLE CSV DATA for quiz tests ────────────────────────────

@pytest.fixture
def quiz_config_path(project_root: Path) -> Path:
    """Return the path to comprehension_quiz.yaml."""
    return project_root / "config" / "comprehension_quiz.yaml"


@pytest.fixture
def events_yaml_path(tmp_path: Path) -> Path:
    """Return a temporary path for events.yaml (isolated from real config)."""
    return tmp_path / "events.yaml"
