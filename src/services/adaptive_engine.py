"""
股識 Stock Explorer — M5 自適應更新引擎
事件偵測 + 公司類型判斷 + 分析框架推薦
"""

import yaml
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
from filelock import FileLock

# ── 配置 ───────────────────────────────────────────────
EVENTS_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "events.yaml",
)
EVENTS_LOCK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "events.lock",
)

# 嚴重程度分數映射
SEVERITY_SCORES = {"high": 3, "medium": 2, "low": 1}

# 重大新聞關鍵字（依嚴重程度分類）
NEWS_MAJOR_KEYWORDS = [
    "收購", "合併", "併購", "出售", "分割", "下市", "破產", "重整",
    "法說", "財報", "大虧", "巨虧", "訴訟", "調查", "裁罰", "造假",
]

NEWS_MEDIUM_KEYWORDS = [
    "股利", "增資", "減資", "庫藏股", "董監改選", "總經理", "董事長",
    "擴廠", "擴產", "訂單", "合約", "合作", "策略聯盟",
    "漲價", "降價", "漲息", "降息",
]


# ── Atomic write ──────────────────────────────────────────

def _atomic_write(path: str, content_bytes: bytes):
    """Write to temp file then atomically replace — prevents partial writes."""
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=parent)
    try:
        os.write(fd, content_bytes)
        os.close(fd)
        os.replace(tmp_path, path)
    except Exception:
        os.close(fd)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ── 事件記錄管理 ──────────────────────────────────────────

def _load_events() -> list:
    """載入事件記錄"""
    lock = FileLock(EVENTS_LOCK_PATH, timeout=10)
    with lock:
        if not os.path.exists(EVENTS_CONFIG_PATH):
            return []
        with open(EVENTS_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("events", [])


def _save_events(events: list):
    """儲存事件記錄（atomic write under file lock）"""
    lock = FileLock(EVENTS_LOCK_PATH, timeout=10)
    with lock:
        content = yaml.dump({"events": events}, allow_unicode=True, default_flow_style=False)
        _atomic_write(EVENTS_CONFIG_PATH, content.encode("utf-8"))


def record_event(
    stock_id: str,
    event_type: str,
    severity: str,
    title: str,
    summary: str,
    date: Optional[str] = None,
):
    """記錄一個新事件"""
    events = _load_events()
    events.append({
        "stock_id": stock_id,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "type": event_type,
        "severity": severity,
        "title": title,
        "summary": summary,
        "detected_at": datetime.now().isoformat(timespec="seconds"),
    })
    _save_events(events)


def get_events_for_stock(stock_id: str, days: int = 30) -> list:
    """取得特定股票近 N 天的事件"""
    events = _load_events()
    cutoff = datetime.now() - timedelta(days=days)
    result = []
    for e in events:
        if e["stock_id"] != stock_id:
            continue
        try:
            event_date = datetime.strptime(e["date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            continue
        if event_date >= cutoff:
            result.append(e)
    return sorted(result, key=lambda x: x.get("date", ""), reverse=True)


def get_all_recent_events(days: int = 30, limit: int = 50) -> list:
    """取得所有股票近 N 天的重大事件"""
    events = _load_events()
    cutoff = datetime.now() - timedelta(days=days)
    result = []
    for e in events:
        try:
            event_date = datetime.strptime(e["date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            continue
        if event_date >= cutoff:
            result.append(e)
    # 依嚴重程度排序（高到低），再依時間排序
    result.sort(key=lambda x: (-SEVERITY_SCORES.get(x.get("severity", "low"), 0), x.get("date", "")))
    return result[:limit]


# ── 事件偵測 ──────────────────────────────────────────────

def detect_revenue_event(monthly_revenue: pd.DataFrame) -> Optional[dict]:
    """
    偵測營收異動事件
    YoY 變化超過 ±30% 視為異常
    """
    if len(monthly_revenue) < 13:
        return None

    try:
        latest = monthly_revenue.iloc[-1]
        year_ago = monthly_revenue.iloc[-13]  # 前年第13個月前的資料

        latest_rev = latest["revenue"]
        year_ago_rev = year_ago["revenue"]
        yoy_pct = ((latest_rev - year_ago_rev) / year_ago_rev) * 100

        if abs(yoy_pct) < 30:
            return None

        severity = "high" if abs(yoy_pct) >= 50 else "medium"
        direction = "成長" if yoy_pct > 0 else "衰退"

        return {
            "type": "revenue_surge",
            "severity": severity,
            "title": f"營收 YoY {direction} {abs(yoy_pct):.0f}%",
            "summary": (
                f"最近月營收 {latest_rev/1e8:.0f} 億元，"
                f"較去年同期{'增加' if yoy_pct > 0 else '減少'} {abs(yoy_pct):.0f}%。"
                f"{'表現亮眼，關注後續動能。' if yoy_pct > 0 else '需留意是否為短期因素影響。'}"
            ),
        }
    except (KeyError, IndexError, ZeroDivisionError):
        return None


def detect_news_event(news: pd.DataFrame) -> list:
    """
    從新聞標題偵測重大事件
    """
    events = []
    if len(news) == 0:
        return events

    for i in range(min(5, len(news))):
        try:
            title = str(news.iloc[i].get("title", ""))
            date_str = str(news.iloc[i].get("date", ""))[:10]
        except (IndexError, KeyError):
            continue

        # 檢查重大關鍵字
        matched_major = [kw for kw in NEWS_MAJOR_KEYWORDS if kw in title]
        if matched_major:
            events.append({
                "type": "news_major",
                "severity": "high",
                "title": title[:60],
                "summary": f"重大事件：{'、'.join(matched_major[:3])}",
                "date": date_str,
            })
            continue

        # 檢查中型關鍵字
        matched_medium = [kw for kw in NEWS_MEDIUM_KEYWORDS if kw in title]
        if matched_medium:
            events.append({
                "type": "news_medium",
                "severity": "medium",
                "title": title[:60],
                "summary": f"注意事件：{'、'.join(matched_medium[:3])}",
                "date": date_str,
            })

    return events


def detect_price_abnormal(daily_prices: pd.DataFrame, threshold: float = 7.0) -> Optional[dict]:
    """
    偵測股價異常（單日漲跌幅超過 threshold%）
    """
    if len(daily_prices) < 2:
        return None

    try:
        latest = daily_prices.iloc[-1]
        prev = daily_prices.iloc[-2]
        change_pct = ((latest["close"] - prev["close"]) / prev["close"]) * 100

        if abs(change_pct) < threshold:
            return None

        direction = "漲" if change_pct > 0 else "跌"
        return {
            "type": "price_abnormal",
            "severity": "high",
            "title": f"股價單日{direction} {abs(change_pct):.1f}%",
            "summary": (
                f"收盤價 {latest['close']:.0f} 元，"
                f"較前一交易日{direction} {abs(change_pct):.1f}%。"
                f"單日波動劇烈，建議關注相關公告。"
            ),
        }
    except (KeyError, IndexError, ZeroDivisionError):
        return None


# ── 公司類型偵測 ──────────────────────────────────────────

def detect_company_type(data: dict) -> str:
    """
    判斷公司類型以自適應分析框架
    回傳: "group" | "etf" | "default"
    """
    stock_name = data.get("stock_name", "")
    stock_id = data.get("stock_id", "")
    industry = data.get("industry", "")

    # ETF 判斷
    if "etf" in industry.lower() or industry == "":
        try:
            # 嘗試判斷：00 開頭的 4 碼代號多為 ETF
            if stock_id.startswith("00") and len(stock_id) == 4:
                return "etf"
        except Exception:
            pass

    # 集團型判斷：名稱包含「集團」「控股」「股份」或特定關鍵字
    group_keywords = ["集團", "控股", "股份"]
    if any(kw in stock_name for kw in group_keywords):
        return "group"

    return "default"


def get_adaptive_framework(company_type: str) -> dict:
    """
    根據公司類型回傳推薦分析框架
    """
    frameworks = {
        "default": {
            "name": "標準分析",
            "description": "使用四大深度區塊完整分析",
            "priority_pages": ["名片", "營運健檢", "財務體質", "同業比較"],
            "focus": "全面理解公司營運與財務狀況",
        },
        "group": {
            "name": "集團分析",
            "description": "側重集團架構與子公司關聯",
            "priority_pages": ["名片", "集團架構", "營運健檢", "同業比較"],
            "focus": "理解集團內部結構與各子公司角色",
        },
        "etf": {
            "name": "ETF 分析",
            "description": "聚焦 ETF 特性與持倉",
            "priority_pages": ["名片", "績效", "配息", "費用"],
            "focus": "理解 ETF 追蹤標的、費用結構與配息特性",
        },
    }
    return frameworks.get(company_type, frameworks["default"])


# ── 資料新鮮度檢查 ──────────────────────────────────────────

def check_data_freshness(stock_id: str, data: dict) -> dict:
    """
    檢查各項資料的最後更新時間，回傳新鮮度狀態
    """
    freshness = {
        "overall": "fresh",  # fresh | stale | unknown
        "items": [],
        "needs_update": False,
    }

    # 檢查最新股價日期
    daily_price = data.get("daily_price")
    if daily_price is not None and len(daily_price) > 0:
        try:
            latest_date = str(daily_price.iloc[-1]["date"])[:10]
            date_obj = datetime.strptime(latest_date, "%Y-%m-%d")
            days_old = (datetime.now() - date_obj).days
            status = "fresh" if days_old <= 3 else ("stale" if days_old <= 7 else "very_stale")
            freshness["items"].append({
                "label": "股價資料",
                "date": latest_date,
                "days_old": days_old,
                "status": status,
            })
            if status != "fresh":
                freshness["needs_update"] = True
        except (KeyError, IndexError, ValueError):
            pass

    # 檢查月營收日期
    monthly_rev = data.get("monthly_revenue")
    if monthly_rev is not None and len(monthly_rev) > 0:
        try:
            latest_date = str(monthly_rev.iloc[-1]["date"])[:10]
            date_obj = datetime.strptime(latest_date, "%Y-%m-%d")
            days_old = (datetime.now() - date_obj).days
            status = "fresh" if days_old <= 35 else ("stale" if days_old <= 60 else "very_stale")
            freshness["items"].append({
                "label": "營收資料",
                "date": latest_date,
                "days_old": days_old,
                "status": status,
            })
            if status != "fresh":
                freshness["needs_update"] = True
        except (KeyError, IndexError, ValueError):
            pass

    # 整體判斷
    statuses = [item["status"] for item in freshness["items"]]
    if "very_stale" in statuses:
        freshness["overall"] = "stale"
    elif all(s == "fresh" for s in statuses):
        freshness["overall"] = "fresh"
    elif statuses:
        freshness["overall"] = "partial"

    return freshness


# ── 綜合事件偵測（自動執行並記錄）──────────────────────────

def run_auto_detection(stock_id: str, data: dict) -> list:
    """
    自動偵測該股票的所有事件，並記錄到 events.yaml
    回傳新偵測到的事件列表
    """
    new_events = []

    # 1. 營收異動偵測
    monthly_rev = data.get("monthly_revenue")
    if monthly_rev is not None:
        rev_event = detect_revenue_event(monthly_rev)
        if rev_event:
            new_events.append({**rev_event, "date": datetime.now().strftime("%Y-%m-%d")})

    # 2. 新聞事件偵測
    news = data.get("news")
    if news is not None:
        news_events = detect_news_event(news)
        new_events.extend(news_events)

    # 3. 股價異常偵測
    daily_price = data.get("daily_price")
    if daily_price is not None:
        price_event = detect_price_abnormal(daily_price)
        if price_event:
            new_events.append({**price_event, "date": datetime.now().strftime("%Y-%m-%d")})

    # 記錄新事件（避免重複記錄相同事件）
    existing_events = get_events_for_stock(stock_id, days=7)
    existing_titles = {e.get("title", "") for e in existing_events}

    for event in new_events:
        if event["title"] not in existing_titles:
            record_event(
                stock_id=stock_id,
                event_type=event["type"],
                severity=event["severity"],
                title=event["title"],
                summary=event["summary"],
            )

    return new_events
