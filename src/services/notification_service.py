"""
股識 Stock Explorer — 通知中心服務
管理使用者通知偏好與待處理通知
"""

import logging
import os
import yaml
from datetime import datetime, timedelta
from filelock import FileLock

from src.utils import _atomic_write

logger = logging.getLogger(__name__)

# ── 配置 ───────────────────────────────────────────────
NOTIFICATIONS_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "notifications.yaml",
)
NOTIFICATIONS_LOCK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "notifications.lock",
)

# 預設通知偏好
DEFAULT_SETTINGS = {
    "enable_notifications": True,
    "notify_high_severity": True,
    "notify_medium_severity": True,
    "notify_low_severity": False,
    "digest_mode": "realtime",  # realtime | daily | weekly
    "subscribed_lists": ["預設清單"],
}


def _load_notifications() -> dict:
    """載入通知設定"""
    lock = FileLock(NOTIFICATIONS_LOCK_PATH, timeout=10)
    with lock:
        if not os.path.exists(NOTIFICATIONS_CONFIG_PATH):
            return {"settings": DEFAULT_SETTINGS, "acknowledged_events": []}
        with open(NOTIFICATIONS_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data


def _save_notifications(data: dict):
    """儲存通知設定（atomic write under file lock）"""
    lock = FileLock(NOTIFICATIONS_LOCK_PATH, timeout=10)
    with lock:
        content = yaml.dump(data, allow_unicode=True, default_flow_style=False)
        _atomic_write(NOTIFICATIONS_CONFIG_PATH, content.encode("utf-8"))


def get_notification_settings() -> dict:
    """取得使用者通知偏好設定"""
    data = _load_notifications()
    settings = data.get("settings", DEFAULT_SETTINGS)
    # 確保所有預設鍵都存在（向後相容）
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
    return settings


def update_notification_settings(settings: dict):
    """更新使用者通知偏好設定"""
    data = _load_notifications()
    data["settings"] = settings
    _save_notifications(data)


def get_subscribed_stocks(client) -> list:
    """
    從關注清單取得使用者訂閱的股票列表。
    回傳 stock_id 字串列表。
    """
    from src.services.watchlist import load_watchlist

    settings = get_notification_settings()
    lists = settings.get("subscribed_lists", ["預設清單"])

    stock_ids = []
    for list_name in lists:
        entries = load_watchlist(list_name)
        for entry in entries:
            sid = entry.get("stock_id", "") if isinstance(entry, dict) else str(entry)
            if sid and sid not in stock_ids:
                stock_ids.append(sid)

    return stock_ids


def _get_acknowledged_ids() -> set:
    """取得已確認的事件 ID 集合"""
    data = _load_notifications()
    return set(data.get("acknowledged_events", []))


def acknowledge_notification(event_id: str):
    """標記單一事件為已讀"""
    data = _load_notifications()
    acknowledged = set(data.get("acknowledged_events", []))
    acknowledged.add(event_id)
    data["acknowledged_events"] = list(acknowledged)
    _save_notifications(data)


def acknowledge_all_notifications(event_ids: list):
    """批次確認所有事件為已讀"""
    data = _load_notifications()
    acknowledged = set(data.get("acknowledged_events", []))
    acknowledged.update(event_ids)
    data["acknowledged_events"] = list(acknowledged)
    _save_notifications(data)


def get_pending_notifications(client, stock_ids: list) -> list:
    """
    對每個訂閱股票執行自動偵測，回傳尚未確認的新事件。
    回傳格式：list of dict，每個 dict 包含事件資訊 + stock_id
    """
    from src.services.adaptive_engine import run_auto_detection, _load_events

    acknowledged = _get_acknowledged_ids()
    pending = []

    for stock_id in stock_ids:
        try:
            from src.pages._router_base import get_stock_data
            data = get_stock_data(client, stock_id)
            if data is None:
                continue

            # 執行自動偵測（會寫入 events.yaml）
            run_auto_detection(stock_id, data)
        except Exception as exc:
            logger.warning("Notification detection failed for %s: %s", stock_id, exc)
            continue

    # 從 events.yaml 讀取所有事件，過濾掉已確認的
    all_events = _load_events()
    for event in all_events:
        event_id = _make_event_id(event)
        if event_id not in acknowledged:
            pending.append({**event, "_event_id": event_id})

    # 依嚴重程度排序（高到低），再依時間排序
    severity_order = {"high": 0, "medium": 1, "low": 2}
    pending.sort(key=lambda x: (severity_order.get(x.get("severity", "low"), 2), x.get("date", "")))

    return pending


def get_notification_summary(client, stock_ids: list) -> dict:
    """
    取得通知摘要計數。
    回傳：{"high": int, "medium": int, "low": int, "total": int}
    """
    from src.services.adaptive_engine import _load_events

    acknowledged = _get_acknowledged_ids()
    all_events = _load_events()

    # 只計算訂閱股票的事件
    subscribed_set = set(stock_ids)
    counts = {"high": 0, "medium": 0, "low": 0, "total": 0}

    for event in all_events:
        if event.get("stock_id") not in subscribed_set:
            continue
        event_id = _make_event_id(event)
        if event_id in acknowledged:
            continue
        severity = event.get("severity", "low")
        if severity in counts:
            counts[severity] += 1
        counts["total"] += 1

    return counts


def _make_event_id(event: dict) -> str:
    """為事件產生唯一 ID（用於已讀追蹤）"""
    return f"{event.get('stock_id', '')}_{event.get('date', '')}_{event.get('type', '')}_{event.get('title', '')}"
