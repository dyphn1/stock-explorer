"""
Story Timeline page (C28) — Full Company Story Timeline MVP.

Composes a scrollable timeline from detected events, case studies,
and company milestones, enriched with historian-style interpretations.

This page is accessible from the Business Card page via the "更多分析" expander.
"""

from __future__ import annotations

import streamlit as st

from src.pages._router_base import _section_title, _summary_card, _info_card
from src.services.timeline_service import get_timeline, TimelineEntry


# ── Severity → border color ───────────────────────────────

_SEVERITY_COLORS = {
    "high": "#E74C3C",
    "medium": "#F39C12",
    "low": "#27AE68",
}


def _severity_color(severity: str) -> str:
    return _SEVERITY_COLORS.get(severity, "#3498DB")


# ── Timeline event card renderer ───────────────────────────

def _render_timeline_card(entry: TimelineEntry, index: int) -> None:
    """Render a single timeline entry as a styled card.

    Uses _summary_card with severity-based border color.
    Falls back to inline card rendering without unsafe_allow_html.
    """
    date = entry.get("date", "未知日期")
    icon = entry.get("icon", "📌")
    title = entry.get("title", "未命名事件")
    summary = entry.get("summary", "")
    interpretation = entry.get("interpretation", "")
    severity = entry.get("severity", "low")
    source = entry.get("source", "")
    count = entry.get("count", 0)

    # Build card content
    content_parts = [f"**{title}**", ""]
    if summary:
        content_parts.append(summary)
        content_parts.append("")
    if interpretation:
        content_parts.append(f"💡 {interpretation}")
        content_parts.append("")
    if count and count > 1:
        content_parts.append(f"📌 這一天共有 {count} 個相關事件")
        content_parts.append("")

    # Source badge
    source_labels = {
        "detected": "🔍 系統偵測",
        "case_study": "📚 案例研究",
        "milestone": "⭐ 公司里程碑",
    }
    source_label = source_labels.get(source, "")
    if source_label:
        content_parts.append(f"*{source_label} · {date}*")

    content = "\n\n".join(content_parts)

    # Use _summary_card with severity-based color
    _summary_card(
        title=f"{icon} {date}",
        content=content,
        icon="",
        border_color=_severity_color(severity),
    )


# ── Main page renderer ─────────────────────────────────────

def render_story_timeline_page(data: dict, client) -> None:
    """C28 Story Timeline — full company story timeline page.

    Shows a scrollable horizontal timeline with event cards,
    color-coded by severity, enriched with interpretations.

    Args:
        data: Standard page data dict with stock_id, stock_name, etc.
        client: FinMindClient instance.
    """
    stock_id = data["stock_id"]
    stock_name = data.get("stock_name", "")

    # Page header
    display_name = f"{stock_name} ({stock_id})" if stock_name else stock_id
    _section_title(f"📅 故事時間軸 — {display_name}")

    st.markdown("*公司完整的故事時間軸：營收異動、新聞事件、歷史轉折與案例研究*")
    st.markdown("")

    # ── Lookback selector ───────────────────────────────────
    col_sel, _ = st.columns([1, 3])
    with col_sel:
        lookback_options = {"1 年": 365, "3 年": 1095, "5 年": 1825, "全部": 3650}
        selected_label = st.selectbox(
            "時間範圍",
            list(lookback_options.keys()),
            index=0,
            key=f"timeline_lookback_{stock_id}",
        )
    lookback_days = lookback_options.get(selected_label, 365)

    st.markdown("")

    # ── Fetch timeline ──────────────────────────────────────
    try:
        entries = get_timeline(stock_id, lookback_days=lookback_days)
    except Exception as exc:
        st.error(f"載入時間軸時發生錯誤：{exc}")
        return

    # ── Empty state ─────────────────────────────────────────
    if not entries:
        _info_card(
            title="目前沒有足夠的時間軸內容",
            content=(
                f"系統尚未在「{selected_label}」範圍內找到 **{display_name}** 的相關事件。\n\n"
                "時間軸資料來源包含：\n\n"
                "• **系統自動偵測**：營收異動、新聞事件、股價異常\n\n"
                "• **歷史案例研究**：與該公司相關的市場事件分析\n\n"
                "• **公司里程碑**：成立、上市、重要產品發佈等歷史轉折\n\n"
                "💡 嘗試擴大時間範圍，或瀏覽其他頁面觸發自動事件偵測。"
            ),
            icon="📭",
        )
        return

    # ── Timeline stats ──────────────────────────────────────
    st.caption(f"共找到 **{len(entries)}** 個時間軸事件（{selected_label}）")
    st.markdown("---")

    # ── Timeline display ────────────────────────────────────
    # Use a horizontal scroll container via columns
    # For better UX, show entries in reverse chronological order (newest first)
    for idx, entry in enumerate(entries):
        _render_timeline_card(entry, idx)
        if idx < len(entries) - 1:
            st.markdown("")

    st.markdown("---")

    # ── Severity legend ─────────────────────────────────────
    _section_title("圖例說明")
    legend_cols = st.columns(3)
    with legend_cols[0]:
        _info_card("🔴 重大事件", "严重程度高，需要密切關注", "⚠️")
    with legend_cols[1]:
        _info_card("🟡 重要事件", "中等嚴重程度，值得留意", "📌")
    with legend_cols[2]:
        _info_card("🟢 參考事件", "嚴重程度低，作為背景參考", "💡")

    # ── Historian disclaimer ────────────────────────────────
    st.markdown("---")
    st.caption(
        "⚠️ 以上時間軸由系統自動整理，事件解讀僅供參考。"
        "不構成任何投資建議。投資有風險，入市需謹慎。"
    )
