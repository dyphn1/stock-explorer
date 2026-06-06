"""
FinMind API Client 封裝
統一管理所有 FinMind 資料接口，提供快取和錯誤處理
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

try:
    from FinMind.data import DataLoader
except ImportError:
    DataLoader = None


class FinMindClient:
    """FinMind API 封裝，含本地快取"""

    def __init__(self, cache_dir: str = ".cache", cache_ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

        if DataLoader is None:
            raise ImportError("FinMind not installed. Run: uv add FinMind")

        self._loader = DataLoader()

    # ── 內部快取方法 ──────────────────────────────────

    def _cache_key(self, prefix: str, **params) -> str:
        """生成快取 key"""
        raw = json.dumps({"prefix": prefix, **params}, sort_keys=True)
        return hashlib.md5(raw.encode()).hexdigest()

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def _is_cache_valid(self, path: Path) -> bool:
        if not path.exists():
            return False
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return datetime.now() - mtime < self.cache_ttl

    def _read_cache(self, key: str) -> Optional[pd.DataFrame]:
        path = self._cache_path(key)
        if self._is_cache_valid(path):
            try:
                return pd.read_json(path, orient="records")
            except Exception:
                return None
        return None

    def _write_cache(self, key: str, df: pd.DataFrame):
        path = self._cache_path(key)
        df.to_json(path, orient="records", date_format="iso")

    def _fetch_or_cache(self, prefix: str, fetch_fn, **params) -> pd.DataFrame:
        """先查快取，沒有才 fetch"""
        key = self._cache_key(prefix, **params)
        cached = self._read_cache(key)
        if cached is not None and len(cached) > 0:
            return cached

        df = fetch_fn()
        if df is not None and len(df) > 0:
            self._write_cache(key, df)
        return df

    # ── 公開 API ──────────────────────────────────────

    def get_stock_info(self, stock_id: str = None) -> pd.DataFrame:
        """取得股票基本資訊"""

        def fetch():
            df = self._loader.taiwan_stock_info()
            if stock_id:
                df = df[df["stock_id"] == stock_id]
            return df

        return self._fetch_or_cache("stock_info", fetch, stock_id=stock_id)

    def get_daily_price(self, stock_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """取得日收盤價"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_daily(
                stock_id=stock_id, start_date=start_date, end_date=end_date
            )

        return self._fetch_or_cache("daily_price", fetch,
                                     stock_id=stock_id, start=start_date, end=end_date)

    def get_monthly_revenue(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得月營收"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_month_revenue(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("month_revenue", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_per_pbr(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得 PER / PBR / 殖利率"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_per_pbr(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("per_pbr", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_financial_statement(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得損益表"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1460)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_financial_statement(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("financial_statement", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_balance_sheet(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得資產負債表"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1460)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_balance_sheet(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("balance_sheet", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_cash_flow(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得現金流量表"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1460)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_cash_flows_statement(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("cash_flow", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_institutional_investors(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得三大法人買賣超"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_institutional_investors(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("institutional", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_margin_trading(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得融資融券"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_margin_purchase_short_sale(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("margin", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_dividend(self, stock_id: str, start_date: str = "2015-01-01") -> pd.DataFrame:
        """取得股利政策"""

        def fetch():
            return self._loader.taiwan_stock_dividend(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("dividend", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_news(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得新聞"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_news(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("news", fetch,
                                     stock_id=stock_id, start=start_date)

    def get_foreign_holding(self, stock_id: str, start_date: str = None) -> pd.DataFrame:
        """取得外資持股"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        def fetch():
            return self._loader.taiwan_stock_shareholding(
                stock_id=stock_id, start_date=start_date
            )

        return self._fetch_or_cache("foreign_holding", fetch,
                                     stock_id=stock_id, start=start_date)

    # ── 輔助方法 ──────────────────────────────────────

    def get_stock_name(self, stock_id: str) -> str:
        """取得股票名稱"""
        df = self.get_stock_info(stock_id)
        if len(df) > 0:
            return df.iloc[0]["stock_name"]
        return stock_id

    def get_industry(self, stock_id: str) -> str:
        """取得產業分類"""
        df = self.get_stock_info(stock_id)
        if len(df) > 0:
            return df.iloc[0]["industry_category"]
        return "未知"

    def get_latest_price(self, stock_id: str) -> dict:
        """取得最新價格資訊"""
        df = self.get_daily_price(stock_id)
        if len(df) == 0:
            return {}
        latest = df.iloc[-1]
        return {
            "date": str(latest["date"]),
            "close": float(latest["close"]),
            "open": float(latest["open"]),
            "high": float(latest["max"]),
            "low": float(latest["min"]),
            "volume": int(latest["Trading_Volume"]),
            "change": float(latest["spread"]),
        }

    def get_latest_per_pbr(self, stock_id: str) -> dict:
        """取得最新 PER/PBR"""
        df = self.get_per_pbr(stock_id)
        if len(df) == 0:
            return {}
        latest = df.iloc[-1]
        return {
            "date": str(latest["date"]),
            "PER": float(latest["PER"]) if pd.notna(latest["PER"]) else None,
            "PBR": float(latest["PBR"]) if pd.notna(latest["PBR"]) else None,
            "dividend_yield": float(latest["dividend_yield"]) if pd.notna(latest["dividend_yield"]) else None,
        }
