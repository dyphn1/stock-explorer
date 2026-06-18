"""
股識 Stock Explorer — M5 公司故事時間軸
顯示特定股票近一年內的事件時間軸，以卡片形式呈現。
"""

import streamlit as st
from src.core.i18n import t
from src.services.adaptive_engine import get_events_for_stock
from src.pages._router_base import _section_title, _summary_card, _info_card


# ── 事件類型中文標籤 ──────────────────────────────────────

_EVENT_TYPE_LABELS = {
    "revenue_surge": t('timeline.event_revenue_surge'),
    "news_major": t('timeline.event_news_major'),
    "news_medium": t('timeline.event_news_medium'),
    "price_abnormal": t('timeline.event_price_abnormal'),
    "dividend_change": t('timeline.event_dividend_change'),
    "institutional_shift": t('timeline.event_institutional_shift'),
}


def _event_type_label(event_type: str) -> str:
    """事件類型中文標籤"""
    return _EVENT_TYPE_LABELS.get(event_type, f"📌 {t('timeline.event_unknown', type=event_type)}")


# ── 嚴重程度標籤 ──────────────────────────────────────────

_SEVERITY_BADGES = {
    "high": t('timeline.severity_high'),
    "medium": t('timeline.severity_medium'),
    "low": t('timeline.severity_low'),
}


def _severity_badge(severity: str) -> str:
    """產生嚴重程度標籤"""
    return _SEVERITY_BADGES.get(severity, f"⚪ {t('timeline.severity_unknown')}")


# ── 時間軸事件卡片 ────────────────────────────────────────

def _timeline_event_card(date: str, event_type: str, severity: str, title: str, summary: str):
    """Render a single timeline event as a card.

    Uses the existing _summary_card pattern from _router_base,
    prefixed with date and severity metadata.
    """
    badge = _severity_badge(severity)
    type_label = _event_type_label(event_type)
    header = f"{badge} {type_label} ｜ {date}"
    _summary_card(
        title=header,
        content=f"**{title}**\n\n{summary}",
        icon="📅",
    )


# ── 主渲染函式 ────────────────────────────────────────────

def render_company_timeline(data: dict, client):
    """公司故事時間軸頁面

    Args:
        data: dict 包含 stock_id, stock_name 等標準頁面資料
        client: FinMindClient 實例
    """
    stock_id = data["stock_id"]
    stock_name = data.get("stock_name", "")

    # 標題
    display_name = f"{stock_name} ({stock_id})" if stock_name else stock_id
    _section_title(t('timeline.page_title', name=display_name))

    st.markdown(t('timeline.page_subtitle'))
    st.markdown("---")

    # 取得事件
    events = get_events_for_stock(stock_id, days=365)

    if not events:
        _info_card(
            title=t('timeline.no_events_title'),
            content=(
                t('timeline.no_events_content', name=display_name)
            ),
            icon="📭",
        )
    else:
        # 時間軸由早到晚排列（最舊的在前，營造時間軸感）
        chronological = list(reversed(events))

        # 顯示事件計數
        st.caption(t('timeline.event_count', count=len(events)))
        st.markdown("")

        for event in chronological:
            date = event.get("date", t('timeline.unknown_date'))
            event_type = event.get("type", "unknown")
            severity = event.get("severity", "low")
            title = event.get("title", t('timeline.unnamed_event'))
            summary = event.get("summary", "")

            _timeline_event_card(
                date=date,
                event_type=event_type,
                severity=severity,
                title=title,
                summary=summary,
            )

    st.markdown("---")

    # 歷史學家免責聲明
    st.caption(t('timeline.disclaimer'))
