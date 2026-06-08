"""
Watchlist manager — config-based subscription system.
Stores watchlist in config/watchlist.yaml
"""

import json
import os
import tempfile
from pathlib import Path
from datetime import datetime

import yaml
from filelock import FileLock

# Relative to project root (where streamlit is launched from)
WATCHLIST_PATH = Path("config/watchlist.yaml")
WATCHLIST_LOCK = Path("config/watchlist.lock")


def _atomic_write(path: Path, content_bytes: bytes):
    """Write to temp file then atomically replace — prevents partial writes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(path.parent))
    try:
        os.write(fd, content_bytes)
        os.close(fd)
        os.replace(tmp_path, str(path))
    except Exception:
        os.close(fd)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def load_watchlist() -> list:
    """Read YAML, return list of watchlist entries. Return empty list if file doesn't exist."""
    lock = FileLock(str(WATCHLIST_LOCK), timeout=10)
    with lock:
        if not WATCHLIST_PATH.exists():
            return []
        try:
            with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []


def save_watchlist(entries: list) -> None:
    """Write list to YAML using atomic write under file lock."""
    lock = FileLock(str(WATCHLIST_LOCK), timeout=10)
    with lock:
        content = yaml.dump(entries, allow_unicode=True, default_flow_style=False, sort_keys=False)
        _atomic_write(WATCHLIST_PATH, content.encode("utf-8"))


def _is_etf(stock_id: str, name: str, industry_category: str = None) -> bool:
    """Determine if a stock is an ETF.

    Priority:
    1. Use FinMind industry_category if available (most reliable)
    2. Fall back to name heuristic
    3. Fall back to stock_id pattern (least reliable)
    """
    # 1. Use FinMind industry_category if provided
    if industry_category and "etf" in industry_category.lower():
        return True
    # 2. Name heuristic
    name_lower = name.lower()
    if "etf" in name_lower:
        return True
    # Common ETF name patterns in Taiwanese market
    etf_name_keywords = ["高息", "高殖", "股息", "債券", "美債", "公司債",
                         "電信", "半導體", "AI", "ESG", "5G", "電動車",
                         "主題型", "杠杆", "反向", "2倍", "-1X", "正2", "反1"]
    for kw in etf_name_keywords:
        if kw in name:
            return True
    # 3. stock_id pattern (least reliable, last resort)
    if stock_id.startswith("00") and len(stock_id) == 4:
        return True
    return False


def add_to_watchlist(
    stock_id: str,
    name: str,
    alert_above: float = None,
    alert_below: float = None,
    industry_category: str = None,
) -> bool:
    """Add entry if not already present. Return True if added, False if already exists."""
    entries = load_watchlist()

    # Check if already exists
    for entry in entries:
        if entry.get("stock_id") == stock_id:
            return False

    # Determine type
    etf_type = "etf" if _is_etf(stock_id, name, industry_category) else "stock"

    new_entry = {
        "stock_id": stock_id,
        "name": name,
        "type": etf_type,
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "alert_above": alert_above,
        "alert_below": alert_below,
    }

    entries.append(new_entry)
    save_watchlist(entries)
    return True


def remove_from_watchlist(stock_id: str) -> bool:
    """Remove entry by stock_id. Return True if removed."""
    entries = load_watchlist()
    original_len = len(entries)
    entries = [e for e in entries if e.get("stock_id") != stock_id]

    if len(entries) < original_len:
        save_watchlist(entries)
        return True
    return False


def is_in_watchlist(stock_id: str) -> bool:
    """Check if stock is watched."""
    entries = load_watchlist()
    return any(e.get("stock_id") == stock_id for e in entries)


def update_alerts(stock_id: str, alert_above: float = None, alert_below: float = None) -> bool:
    """Update alert_above and alert_below for a watchlist entry.
    
    Args:
        stock_id: The stock identifier to update.
        alert_above: Price threshold for upper alert (None to clear).
        alert_below: Price threshold for lower alert (None to clear).
    
    Returns:
        True if the entry was found and updated, False otherwise.
    """
    entries = load_watchlist()
    for entry in entries:
        if entry.get("stock_id") == stock_id:
            entry["alert_above"] = alert_above
            entry["alert_below"] = alert_below
            save_watchlist(entries)
            return True
    return False


def get_watchlist_summary(client) -> list:
    """For each watched stock, get latest price and return list of dicts.

    Each dict contains:
        stock_id, name, type, latest_price, change,
        alert_above, alert_below, alert_triggered
    """
    entries = load_watchlist()
    summary = []

    for entry in entries:
        stock_id = entry.get("stock_id", "")
        name = entry.get("name", stock_id)
        etf_type = entry.get("type", "stock")
        alert_above = entry.get("alert_above")
        alert_below = entry.get("alert_below")

        latest_price = None
        change = None
        alert_triggered = False

        try:
            price_data = client.get_latest_price(stock_id)
            if price_data:
                latest_price = price_data.get("close")
                change = price_data.get("change")

                # Check alert conditions
                if latest_price is not None:
                    if alert_above is not None and latest_price >= alert_above:
                        alert_triggered = True
                    if alert_below is not None and latest_price <= alert_below:
                        alert_triggered = True
        except Exception:
            pass

        summary.append({
            "stock_id": stock_id,
            "name": name,
            "type": etf_type,
            "latest_price": latest_price,
            "change": change,
            "alert_above": alert_above,
            "alert_below": alert_below,
            "alert_triggered": alert_triggered,
        })

    return summary
