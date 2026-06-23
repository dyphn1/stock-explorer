"""FinMind API Client 封裝
統一管理所有 FinMind 資料接口，提供快取和錯誤處理
"""

import os
import json
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import functools

import pandas as pd

logger = logging.getLogger(__name__)

try:
    from FinMind.data import DataLoader
except ImportError:
    DataLoader = None


# ── Rate Limit Detection ──────────────────────────────


class FinMindRateLimitError(Exception):
    """Raised when FinMind API rate limit is detected (e.g. HTTP 429)."""
    pass


# Module-level rate limit tracking (per-process, suitable for Streamlit)
_consecutive_failures: int = 0
_last_failure_time: Optional[datetime] = None
_RATE_LIMIT_THRESHOLD: int = 3  # Show warning after this many consecutive empty responses


def _record_api_failure():
    """Increment consecutive failure counter and record failure time."""
    global _consecutive_failures, _last_failure_time
    _consecutive_failures += 1
    _last_failure_time = datetime.now()


def _record_api_success():
    """Reset consecutive failure counter on a successful API call."""
    global _consecutive_failures
    _consecutive_failures = 0


def get_rate_limit_status() -> dict:
    """Return current rate limit detection status for UI integration.

    Returns:
        dict with keys:
            is_limited (bool): True if consecutive_failures >= threshold
            consecutive_failures (int): Number of consecutive empty/failed API responses
            last_failure (datetime|None): Timestamp of most recent failure
    """
    return {
        "is_limited": _consecutive_failures >= _RATE_LIMIT_THRESHOLD,
        "consecutive_failures": _consecutive_failures,
        "last_failure": _last_failure_time,
    }


class FinMindClient:
    """FinMind API 封裝，含本地快取"""

    def __init__(self, cache_dir: str = ".cache", cache_ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

        if DataLoader is None:
            raise ImportError("FinMind not installed. Run: uv add FinMind")

        self._loader = DataLoader()

        # P0 fix: clean up expired cache files on init
        self._cleanup_cache()

        # Memory cache for all stock info to avoid file cache lookups
        self._all_stock_info_memory = None
        self._all_stock_info_memory_time = None

    # ── 內部快取方法 ────────────────────────────────

    def _cache_key(self, prefix: str, **params) -> str:
        """生成快取 key，並標準化滑動窗口開始日期以防止每日快取失效"""
        filtered_params = {}
        today = datetime.now().date()
        for key, value in params.items():
            # Check if the value is a string in YYYY-MM-DD format
            if isinstance(value, str) and len(value) == 10 and value[4] == '-' and value[7] == '-':
                try:
                    param_date = datetime.strptime(value, "%Y-%m-%d").date()
                    delta = today - param_date
                    # If the date is between 30 and 2000 days ago (inclusive), treat as sliding window and exclude
                    if 30 <= delta.days <= 2000:
                        continue
                except ValueError:
                    # If parsing fails, fall through to include the value
                    pass
            # Include the parameter (either non-date, invalid date, or date outside sliding window)
            filtered_params[key] = value

        raw = json.dumps({"prefix": prefix, **filtered_params}, sort_keys=True)
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
        """先查快取，沒有才 fetch。追蹤連續失敗以偵測 rate limit。"""
        key = self._cache_key(prefix, **params)
        cached = self._read_cache(key)
        if cached is not None and len(cached) > 0:
            _record_api_success()
            return cached

        try:
            df = fetch_fn()
        except Exception as e:
            # Detect HTTP 429 rate limit from FinMind / requests
            error_msg = str(e)
            if "429" in error_msg or "rate" in error_msg.lower():
                _record_api_failure()
                raise FinMindRateLimitError(
                    f"FinMind API rate limit hit: {error_msg}"
                ) from e
            # Other exceptions — still count as failure for rate limit tracking
            _record_api_failure()
            raise

        if df is not None and len(df) > 0:
            _record_api_success()
            self._write_cache(key, df)
        else:
            # Empty DataFrame — potential rate limit symptom
            _record_api_failure()

        return df

    # LRU eviction thresholds
    _MAX_CACHE_FILES = 500
    _MAX_CACHE_BYTES = 100 * 1024 * 1024  # 100 MB

    def _cleanup_cache(self):
        """Remove expired cache files, then LRU-evict if over size/count thresholds.

        Two-phase cleanup:
        1. TTL expiry: remove files older than cache_ttl
        2. LRU eviction: if total files > _MAX_CACHE_FILES or total size > _MAX_CACHE_BYTES,
           delete oldest files (by mtime) until under threshold
        """
        try:
            now = datetime.now()
            expired_count = 0

            # Phase 1: TTL expiry
            for path in self.cache_dir.glob("*.json"):
                try:
                    mtime = datetime.fromtimestamp(path.stat().st_mtime)
                    if now - mtime > self.cache_ttl:
                        path.unlink(missing_ok=True)
                        expired_count += 1
                except OSError:
                    pass

            # Phase 2: LRU eviction — collect remaining files
            files = []
            total_size = 0
            for path in self.cache_dir.glob("*.json"):
                try:
                    stat = path.stat()
                    files.append((path, stat.st_mtime, stat.st_size))
                    total_size += stat.st_size
                except OSError:
                    pass

            total_files = len(files)
            evicted_count = 0

            # Evict oldest by mtime until under both thresholds
            if total_files > self._MAX_CACHE_FILES or total_size > self._MAX_CACHE_BYTES:
                files.sort(key=lambda f: f[1])  # sort by mtime ascending (oldest first)
                for path, mtime, size in files:
                    if total_files <= self._MAX_CACHE_FILES and total_size <= self._MAX_CACHE_BYTES:
                        break
                    try:
                        path.unlink(missing_ok=True)
                        total_files -= 1
                        total_size -= size
                        evicted_count += 1
                    except OSError:
                        pass

            # Log cleanup stats
            if expired_count > 0 or evicted_count > 0:
                logger.info(
                    "Cache cleanup: expired=%d, evicted=%d, remaining_files=%d, remaining_size=%.1fKB",
                    expired_count, evicted_count, total_files, total_size / 1024,
                )
        except Exception:
            pass  # Non-critical; don't crash on cache cleanup

    # ── 內部資料取得 ────────────────────────────────

    def _fetch_all_stock_info(self) -> pd.DataFrame:
        """取得全部股票基本資訊，使用單一快取 key（不含 stock_id）。

        解決 P0-3 問題：避免每次 get_stock_info(stock_id) 都產生不同
        cache key 導致重複呼叫 API 抓取同一份全量資料。
        """
        # Check memory cache first
        now = datetime.now()
        if (self._all_stock_info_memory is not None
                and self._all_stock_info_memory_time is not None
                and now - self._all_stock_info_memory_time < self.cache_ttl):
            logger.debug("Returning all stock info from memory cache")
            return self._all_stock_info_memory

        def fetch():
            return self._loader.taiwan_stock_info()

        df = self._fetch_or_cache("all_stock_info", fetch)
        if df is not None and len(df) > 0:
            self._all_stock_info_memory = df
            self._all_stock_info_memory_time = now
            logger.debug("Updated memory cache for all stock info")
        return df

    # ── 公開 API ────────────────────────────────────

    @functools.lru_cache(maxsize=128)
    def get_stock_info(self, stock_id: str = None) -> pd.DataFrame:
        """取得股票基本資訊（先取全量資料再記憶體內過濾）"""
        df = self._fetch_all_stock_info()
        if stock_id and len(df) > 0:
            df = df[df["stock_id"] == stock_id]
        return df

    def search_stocks(self, query: str, case_sensitive: bool = True) -> pd.DataFrame:
        """搜尋股票：完全比對 stock_id 或部分比對 stock_name（中文名稱）。

        Args:
            query: 搜尋關鍵字（股票代號或中文名稱）
            case_sensitive: 是否區分大小寫（預設 True，向後相容）

        Returns:
            符合條件的股票 DataFrame，無符合則回傳空 DataFrame
        """
        df = self._fetch_all_stock_info()
        if not query or len(df) == 0:
            return df.iloc[:0]  # empty DataFrame with same schema

        mask_id = df["stock_id"] == query.strip()
        mask_name = df["stock_name"].str.contains(query.strip(), case=case_sensitive, na=False)
        return df[mask_id | mask_name]

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

        # P0 fix: exclude 'end' from cache key to prevent daily cache invalidation
        return self._fetch_or_cache("daily_price", fetch,
                                     stock_id=stock_id, start=start_date)

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

    # ── 輔助方法 ────────────────────────────────────

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