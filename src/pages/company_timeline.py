"""
股識 Stock Explorer — M5 公司故事時間軸
顯示特定股票近一年內的事件時間軸，以卡片形式呈現。
"""

import streamlit as st
from src.services.adaptive_engine import get_events_for_stock
from src.pages._router_base import _section_title, _summary_card, _info_card


# ── 事件類型中文標籤 ──────────────────────────────────────

_EVENT_TYPE_LABELS = {
    "revenue_surge": "💰 營收異動",
    "news_major": "📰 重大新聞",
    "news_medium": "📰 注意新聞",
    "price_abnormal": "📉 股價異常",
    "dividend_change": "💵 股利變更",
    "institutional_shift": "🏷️ 法人突變",
}


def _event_type_label(event_type: str) -> str:
    """事件類型中文標籤"""
    return _EVENT_TYPE_LABELS.get(event_type, f"📌 {event_type}")


# ── 嚴重程度標籤 ──────────────────────────────────────────

_SEVERITY_BADGES = {
    "high": "🔴 重大",
    "medium": "🟡 注意",
    "low": "🟢 參考",
}


def _severity_badge(severity: str) -> str:
    """產生嚴重程度標籤"""
    return _SEVERITY_BADGES.get(severity, "⚪ 未知")


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
    _section_title(f"📅 故事時間軸 — {display_name}")

    st.markdown("*過去一年內偵測到的公司事件，依時間順序排列*")
    st.markdown("---")

    # 取得事件
    events = get_events_for_stock(stock_id, days=365)

    if not events:
        _info_card(
            title="目前尚無事件記錄",
            content=(
                f"系統尚未在過去一年內偵測到 **{display_name}** 的重大事件。\n\n"
                "當公司發生營收異動、重大新聞或股價異常時，事件會自動記錄於此。\n\n"
                "💡 瀏覽其他頁面（如名片、營運健檢）可觸發自動事件偵測。"
            ),
            icon="📭",
        )
    else:
        # 時間軸由早到晚排列（最舊的在前，營造時間軸感）
        chronological = list(reversed(events))

        # 顯示事件計數
        st.markdown(
            f"<div style='color:#7F8C8D;font-size:0.85rem;'>"
            f"從過去一年中找到 <b>{len(events)}</b> 個事件"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        for event in chronological:
            date = event.get("date", "未知日期")
            event_type = event.get("type", "unknown")
            severity = event.get("severity", "low")
            title = event.get("title", "未命名事件")
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
    st.caption(
        "⚠️ 以上事件由系統自動偵測，僅供參考。事件解讀僅說明背景與可能意涵，"
        "不構成投資建議。"
    )
