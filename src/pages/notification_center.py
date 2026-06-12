"""
股識 Stock Explorer — C02 通知中心
獨立頁面：顯示所有訂閱股票的待處理通知
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card
from src.pages.business_card._helpers import (
    _historian_disclaimer,
    _study_card,
    _expert_card,
)
from src.pages._router_base import _section_title
from src.services.notification_service import (
    get_notification_settings,
    update_notification_settings,
    get_subscribed_stocks,
    get_pending_notifications,
    get_notification_summary,
    acknowledge_notification,
    acknowledge_all_notifications,
    _make_event_id,
)


def _severity_badge(severity: str) -> str:
    """產生嚴重程度標籤"""
    badges = {
        "high": "🔴 重大",
        "medium": "🟡 注意",
        "low": "🟢 參考",
    }
    return badges.get(severity, "⚪ 未知")


def _event_type_label(event_type: str) -> str:
    """事件類型中文標籤"""
    labels = {
        "revenue_surge": "💰 營收異動",
        "news_major": "📰 重大新聞",
        "news_medium": "📰 注意新聞",
        "price_abnormal": "📉 股價異常",
        "dividend_change": "💵 股利變更",
        "institutional_shift": "🏷️ 法人突變",
    }
    return labels.get(event_type, f"📌 {event_type}")


def _severity_color(severity: str) -> str:
    colors = {
        "high": "#E74C3C",
        "medium": "#F39C12",
        "low": "#27AE60",
    }
    return colors.get(severity, "#7F8C8D")


def _render_notification_center(client: FinMindClient):
    """通知中心主頁面"""
    st.markdown("## 🔔 通知中心")
    st.markdown("*追蹤你關注股票的重要事件與異動*")
    st.markdown("---\n")

    # ── 取得訂閱股票 ──────────────────────────────────────
    stock_ids = get_subscribed_stocks(client)

    if not stock_ids:
        _info_card(
            "尚未設定關注清單",
            "請先在「我的關注」頁面加入股票，通知中心才會顯示相關事件。",
            icon="📋",
        )
        st.markdown("---\n")
        _historian_disclaimer("general")
        return

    # ── 摘要橫幅 ──────────────────────────────────────────
    with st.spinner("檢查通知..."):
        summary = get_notification_summary(client, stock_ids)

    high_count = summary.get("high", 0)
    medium_count = summary.get("medium", 0)
    low_count = summary.get("low", 0)
    total_count = summary.get("total", 0)

    if total_count > 0:
        parts = []
        if high_count > 0:
            parts.append(f"🔴 {high_count} 項重大事件")
        if medium_count > 0:
            parts.append(f"🟡 {medium_count} 項注意事件")
        if low_count > 0:
            parts.append(f"🟢 {low_count} 項參考事件")
        summary_text = " ｜ ".join(parts)
        _summary_card("未讀通知", summary_text, icon="🔔")
    else:
        _info_card(
            "目前沒有待處理的通知",
            "當你有關注的股票出現重大事件時，會顯示在這裡。",
            icon="🔔",
        )

    # ── 全部標記已讀 ──────────────────────────────────────
    if total_count > 0:
        if st.button("✅ 全部標記已讀", key="ack_all_top", use_container_width=True):
            with st.spinner("標記中..."):
                pending = get_pending_notifications(client, stock_ids)
                event_ids = [e.get("_event_id", _make_event_id(e)) for e in pending]
                acknowledge_all_notifications(event_ids)
            st.success("已將所有通知標記為已讀")
            st.rerun()

    st.markdown("---\n")

    # ── 待處理通知列表 ────────────────────────────────────
    _section_title(f"📋 待處理通知")

    with st.spinner("載入通知..."):
        pending = get_pending_notifications(client, stock_ids)

    if not pending:
        _info_card(
            "目前沒有待處理的通知",
            "當你有關注的股票出現重大事件時，會顯示在這裡。",
            icon="🔔",
        )
    else:
        # 依股票分組顯示
        grouped: dict = {}
        for event in pending:
            sid = event.get("stock_id", "未知")
            if sid not in grouped:
                grouped[sid] = []
            grouped[sid].append(event)

        for sid, events in grouped.items():
            # 取得股票名稱（從第一筆事件推斷）
            stock_name = events[0].get("stock_name", sid)

            st.markdown(f"**{sid}** {stock_name}")

            for event in events:
                severity = event.get("severity", "low")
                badge = _severity_badge(severity)
                event_type = _event_type_label(event.get("type", ""))
                title = event.get("title", "")
                summary_text = event.get("summary", "")
                date = event.get("date", "")
                color = _severity_color(severity)

                # 使用 _study_card 或 _expert_card 依嚴重程度
                card_content = (
                    f"{badge} {event_type} ｜ {date}\n\n"
                    f"**{title}**\n\n"
                    f"{summary_text}"
                )

                if severity == "high":
                    _expert_card(title, f"{badge} {event_type} ｜ {date}\n\n{summary_text}", icon="🔴")
                elif severity == "medium":
                    _study_card(title, f"{badge} {event_type} ｜ {date}\n\n{summary_text}", icon="🟡")
                else:
                    _study_card(title, f"{badge} {event_type} ｜ {date}\n\n{summary_text}", icon="🟢")

                # 按鈕列
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button(
                        "查看名片",
                        key=f"notif_goto_{event.get('_event_id', '')}",
                        use_container_width=True,
                    ):
                        navigate_to(page="名片", stock_id=sid)
                with col_btn2:
                    if st.button(
                        "標記已讀",
                        key=f"notif_ack_{event.get('_event_id', '')}",
                        use_container_width=True,
                    ):
                        event_id = event.get("_event_id", _make_event_id(event))
                        acknowledge_notification(event_id)
                        st.rerun()

                st.markdown("")

            st.markdown("---")

    # ── 通知設定（收合） ──────────────────────────────────
    st.markdown("\n")
    _section_title(f"⚙️ 通知設定")

    settings = get_notification_settings()

    with st.expander("展開通知偏好設定", expanded=False):
        enable = st.toggle(
            "啟用通知",
            value=settings.get("enable_notifications", True),
            key="notif_enable",
        )
        notify_high = st.toggle(
            "重大事件通知（🔴）",
            value=settings.get("notify_high_severity", True),
            key="notif_high",
        )
        notify_medium = st.toggle(
            "注意事件通知（🟡）",
            value=settings.get("notify_medium_severity", True),
            key="notif_medium",
        )
        notify_low = st.toggle(
            "參考事件通知（🟢）",
            value=settings.get("notify_low_severity", False),
            key="notif_low",
        )

        digest_mode = st.selectbox(
            "通知頻率",
            options=["realtime", "daily", "weekly"],
            index=["realtime", "daily", "weekly"].index(
                settings.get("digest_mode", "realtime")
            ),
            format_func=lambda x: {"realtime": "即時", "daily": "每日彙整", "weekly": "每週彙整"}[x],
            key="notif_digest",
        )

        if st.button("💾 儲存設定", key="notif_save_settings", use_container_width=True):
            new_settings = {
                "enable_notifications": enable,
                "notify_high_severity": notify_high,
                "notify_medium_severity": notify_medium,
                "notify_low_severity": notify_low,
                "digest_mode": digest_mode,
                "subscribed_lists": settings.get("subscribed_lists", ["預設清單"]),
            }
            update_notification_settings(new_settings)
            st.success("✅ 設定已儲存")

    st.markdown("---\n")
    _historian_disclaimer("general")
