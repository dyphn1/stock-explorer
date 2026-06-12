"""C71 Study Log (學習日誌) — track user's study streak and history."""
import streamlit as st
from datetime import datetime, date, timedelta
from src.pages.business_card._helpers import (
    _study_card,
    _historian_disclaimer,
)
from src.pages._router_base import _section_title

# Session state key for tracking study history
_STUDY_LOG_KEY = "_study_log"


def _get_study_log() -> dict:
    """Get the study log from session state, initializing if needed.

    Returns a dict with:
        - 'dates': list of date strings (YYYY-MM-DD) when user viewed stocks
        - 'stocks': dict mapping date_str -> list of stock_ids viewed that day
    """
    if _STUDY_LOG_KEY not in st.session_state:
        st.session_state[_STUDY_LOG_KEY] = {"dates": [], "stocks": {}}
    return st.session_state[_STUDY_LOG_KEY]


def _record_study(stock_id: str):
    """Record that the user studied a stock today."""
    log = _get_study_log()
    today_str = date.today().isoformat()

    if today_str not in log["dates"]:
        log["dates"].append(today_str)
        log["stocks"][today_str] = []

    if stock_id not in log["stocks"][today_str]:
        log["stocks"][today_str].append(stock_id)

    st.session_state[_STUDY_LOG_KEY] = log


def _compute_streak(log: dict) -> int:
    """Compute the current consecutive-day study streak."""
    dates = sorted(log.get("dates", []), reverse=True)
    if not dates:
        return 0

    streak = 0
    today = date.today()
    for i, date_str in enumerate(dates):
        expected = today - timedelta(days=i)
        if date_str == expected.isoformat():
            streak += 1
        else:
            break
    return streak


def _get_recent_history(log: dict, days: int = 7) -> list:
    """Return study history for the last N days.

    Returns list of (date_str, count) tuples, most recent first.
    """
    today = date.today()
    history = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        date_str = d.isoformat()
        count = len(log.get("stocks", {}).get(date_str, []))
        history.append((date_str, count))
    return history


def _get_total_stocks(log: dict) -> int:
    """Return total unique stocks studied across all dates."""
    all_stocks = set()
    for stocks in log.get("stocks", {}).values():
        all_stocks.update(stocks)
    return len(all_stocks)


def _render_study_log(data: dict, client) -> None:
    """C71 Study Log: track user's study streak and history.

    Shows:
    - Current study streak (consecutive days)
    - Recent study history (last 7 days)
    - Total unique stocks studied
    """
    stock_id = data["stock_id"]

    # Record this stock view
    _record_study(stock_id)

    log = _get_study_log()
    streak = _compute_streak(log)
    total = _get_total_stocks(log)
    recent = _get_recent_history(log, days=7)

    _section_title(f"📚 學習日誌")

    # Streak + total summary
    streak_text = f"目前連續學習 **{streak}** 天" if streak > 0 else "今天開始學習吧！"
    total_text = f"累計研究過 **{total}** 檔股票"

    _study_card(
        "學習進度",
        f"{streak_text}\n\n{total_text}",
        "📚",
    )

    # Recent 7-day history
    today = date.today()
    history_lines = []
    for date_str, count in recent:
        d = date.fromisoformat(date_str)
        day_label = d.strftime("%m/%d")
        # Mark today
        if d == today:
            day_label += " (今天)"
        bar = "█" * min(count, 10) + ("…" if count > 10 else "")
        if count == 0:
            bar = "—"
        history_lines.append(f"{day_label}　{bar} ({count})")

    _study_card(
        "最近 7 天學習紀錄",
        "\n".join(history_lines),
        "📅",
    )

    st.markdown("---")
