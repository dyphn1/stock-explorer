"""
Watchlist manager — config-based subscription system.
Stores watchlist in config/watchlist.yaml
"""

import json
from pathlib import Path
from datetime import datetime

import yaml

# Relative to project root (where streamlit is launched from)
WATCHLIST_PATH = Path("config/watchlist.yaml")


def load_watchlist() -> list:
    """Read YAML, return list of watchlist entries. Return empty list if file doesn't exist."""
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
    """Write list to YAML."""
    WATCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(WATCHLIST_PATH, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _is_etf(stock_id: str, name: str) -> bool:
    """Determine if a stock is an ETF based on name or id patterns."""
    name_lower = name.lower()
    # Common ETF indicators in Taiwanese market
    etf_keywords = ["etf", "00", "50", "56", "6208", "高息", "股息", "債券"]
    # Check if name contains ETF keyword
    if "etf" in name_lower:
        return True
    # Check stock_id patterns common for ETFs (many ETFs start with 00)
    if stock_id.startswith("00") and len(stock_id) == 4:
        return True
    return False


def add_to_watchlist(
    stock_id: str,
    name: str,
    alert_above: float = None,
    alert_below: float = None,
) -> bool:
    """Add entry if not already present. Return True if added, False if already exists."""
    entries = load_watchlist()

    # Check if already exists
    for entry in entries:
        if entry.get("stock_id") == stock_id:
            return False

    # Determine type
    etf_type = "etf" if _is_etf(stock_id, name) else "stock"

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
