"""
Watchlist manager — config-based subscription system.
Stores watchlist in config/watchlist.yaml
Supports multiple named lists.
"""

from pathlib import Path
from datetime import datetime

import yaml
from filelock import FileLock

from src.utils import _atomic_write

# Relative to project root (where streamlit is launched from)
WATCHLIST_PATH = Path("config/watchlist.yaml")
WATCHLIST_LOCK = Path("config/watchlist.lock")


def _load_data() -> dict:
    """Load the entire watchlist data structure.
    Returns a dict with key 'lists' mapping list names to lists of entries.
    If file doesn't exist, returns {'lists': {}}.
    If old format (list) is detected, converts to {'lists': {'預設清單': <old list>}}.
    """
    lock = FileLock(str(WATCHLIST_LOCK), timeout=10)
    with lock:
        if not WATCHLIST_PATH.exists():
            return {"lists": {}}
        try:
            with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            # Backward compatibility: if data is a list, assume old format
            if isinstance(data, list):
                # Convert to new structure with a single list named "預設清單"
                return {"lists": {"預設清單": data}}
            # If data is a dict but doesn't have 'lists', assume it's the old dict format? 
            # We expect new format to have 'lists'. If not, we treat as empty.
            if isinstance(data, dict) and "lists" in data:
                return data
            # Fallback: treat as empty
            return {"lists": {}}
        except Exception:
            return {"lists": {}}


def _save_data(data: dict) -> None:
    """Save the entire watchlist data structure under file lock."""
    lock = FileLock(str(WATCHLIST_LOCK), timeout=10)
    with lock:
        content = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        _atomic_write(WATCHLIST_PATH, content.encode("utf-8"))


def load_watchlist(list_name: str = "預設清單") -> list:
    """Read YAML, return list of watchlist entries for the given list name.
    Return empty list if file doesn't exist or list doesn't exist.
    """
    data = _load_data()
    return data.get("lists", {}).get(list_name, [])


def save_watchlist(entries: list, list_name: str = "預設清單") -> None:
    """Write the given entries as the list for list_name under file lock."""
    data = _load_data()
    # Ensure the lists dict exists
    if "lists" not in data:
        data["lists"] = {}
    data["lists"][list_name] = entries
    _save_data(data)


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
    list_name: str = "預設清單",
) -> bool:
    """Add entry to the specified list if not already present in that list.
    Return True if added, False if already exists in that list.
    """
    entries = load_watchlist(list_name)

    # Check if already exists in this list
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
    save_watchlist(entries, list_name)
    return True


def remove_from_watchlist(stock_id: str, list_name: str = "預設清單") -> bool:
    """Remove entry by stock_id from the specified list.
    Return True if removed from that list.
    """
    entries = load_watchlist(list_name)
    original_len = len(entries)
    entries = [e for e in entries if e.get("stock_id") != stock_id]

    if len(entries) < original_len:
        save_watchlist(entries, list_name)
        return True
    return False


def remove_from_all_lists(stock_id: str) -> bool:
    """Remove entry by stock_id from all lists.
    Return True if removed from at least one list.
    """
    data = _load_data()
    lists = data.get("lists", {})
    removed = False
    for name, entries in lists.items():
        original_len = len(entries)
        new_entries = [e for e in entries if e.get("stock_id") != stock_id]
        if len(new_entries) < original_len:
            lists[name] = new_entries
            removed = True
    if removed:
        _save_data(data)
    return removed


def is_in_watchlist(stock_id: str, list_name: str = "預設清單") -> bool:
    """Check if stock is watched in the specified list."""
    entries = load_watchlist(list_name)
    return any(e.get("stock_id") == stock_id for e in entries)


def is_in_any_list(stock_id: str) -> bool:
    """Check if stock is watched in any list."""
    data = _load_data()
    lists = data.get("lists", {})
    for entries in lists.values():
        if any(e.get("stock_id") == stock_id for e in entries):
            return True
    return False


def get_lists_for_stock(stock_id: str) -> list:
    """Return a list of list names that contain the given stock."""
    data = _load_data()
    lists = data.get("lists", {})
    result = []
    for name, entries in lists.items():
        if any(e.get("stock_id") == stock_id for e in entries):
            result.append(name)
    return result


def update_alerts(
    stock_id: str,
    alert_above: float = None,
    alert_below: float = None,
    list_name: str = "預設清單",
) -> bool:
    """Update alert_above and alert_below for a watchlist entry in the specified list.

    Args:
        stock_id: The stock identifier to update.
        alert_above: Price threshold for upper alert (None to clear).
        alert_below: Price threshold for lower alert (None to clear).
        list_name: The name of the list to update.

    Returns:
        True if the entry was found and updated, False otherwise.
    """
    entries = load_watchlist(list_name)
    for entry in entries:
        if entry.get("stock_id") == stock_id:
            entry["alert_above"] = alert_above
            entry["alert_below"] = alert_below
            save_watchlist(entries, list_name)
            return True
    return False


def get_watchlist_summary(client, list_name: str = "預設清單") -> list:
    """For each watched stock in the specified list, get latest price and return list of dicts.

    Each dict contains:
        stock_id, name, type, latest_price, change,
        alert_above, alert_below, alert_triggered
    """
    entries = load_watchlist(list_name)
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


def create_list(list_name: str) -> bool:
    """Create a new watchlist with the given name.
    Returns True if created, False if list already exists.
    """
    data = _load_data()
    if "lists" not in data:
        data["lists"] = {}
    if list_name in data["lists"]:
        return False
    data["lists"][list_name] = []
    _save_data(data)
    return True


def delete_list(list_name: str) -> bool:
    """Delete the watchlist with the given name.
    Returns True if deleted, False if list doesn't exist or is the last list.
    We prevent deleting the last list to avoid empty watchlist structure.
    """
    data = _load_data()
    if "lists" not in data or list_name not in data["lists"]:
        return False
    # Prevent deleting the last list
    if len(data["lists"]) <= 1:
        return False
    del data["lists"][list_name]
    _save_data(data)
    return True


def rename_list(old_name: str, new_name: str) -> bool:
    """Rename a watchlist from old_name to new_name.
    Returns True if renamed, False if old_name doesn't exist or new_name already exists.
    """
    data = _load_data()
    if "lists" not in data:
        return False
    if old_name not in data["lists"]:
        return False
    if new_name in data["lists"]:
        return False
    data["lists"][new_name] = data["lists"].pop(old_name)
    _save_data(data)
    return True


def list_names() -> list:
    """Return a list of all watchlist names."""
    data = _load_data()
    return list(data.get("lists", {}).keys())


