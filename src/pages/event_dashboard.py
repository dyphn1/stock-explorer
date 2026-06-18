"""
股識 Stock Explorer — M5 事件儀表板
顯示近期重大事件、資料新鮮度、自適應框架推薦
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.pages.url_sync import navigate_to
from src.services.adaptive_engine import (
    get_all_recent_events,
    get_events_for_stock,
    detect_company_type,
    get_adaptive_framework,
    check_data_freshness,
    SEVERITY_SCORES,
)
from src.services.event_interpretation_service import (
    get_interpretation,
    get_drilldown_interpretation,
)
from src.pages._router_base import _summary_card, _info_card, _source_section
from src.core.i18n import t


def _severity_badge(severity: str) -> str:
    """產生嚴重程度標籤"""
    badges = {
        "high": t('event_dashboard.severity.high'),
        "medium": t('event_dashboard.severity.medium'),
        "low": t('event_dashboard.severity.low'),
    }
    return badges.get(severity, t('event_dashboard.severity.unknown'))


def _event_type_label(event_type: str) -> str:
    """事件類型中文標籤"""
    labels = {
        "revenue_surge": t('event_dashboard.event_type.revenue_surge'),
        "news_major": t('event_dashboard.event_type.news_major'),
        "news_medium": t('event_dashboard.event_type.news_medium'),
        "price_abnormal": t('event_dashboard.event_type.price_abnormal'),
        "dividend_change": t('event_dashboard.event_type.dividend_change'),
        "institutional_shift": t('event_dashboard.event_type.institutional_shift'),
    }
    return labels.get(event_type, f"📌 {event_type}")


def _render_event_dashboard(client):
    """事件儀表板主頁面"""
    st.markdown(f"## 🔔 {t('event_dashboard.title')}")
    st.markdown(f"*{t('event_dashboard.subtitle')}*")
    st.markdown("---")

    # ── 近期重大事件 ──────────────────────────────────────
    st.markdown(f"### 📋 {t('event_dashboard.recent_events')}")

    recent_events = get_all_recent_events(days=30, limit=50)

    if not recent_events:
        st.info(t('event_dashboard.no_events'))
    else:
        # 依日期分組顯示
        dates = {}
        for event in recent_events:
            date = event.get("date", t('event_dashboard.unknown_date'))
            if date not in dates:
                dates[date] = []
            dates[date].append(event)

        # P0 fix: use enumerate index for unique button keys (prevents DuplicateWidgetID)
        evt_idx = 0
        for date, events in sorted(dates.items(), reverse=True):
            st.markdown(f"**{date}**")
            for event in events:
                severity = event.get("severity", "low")
                badge = _severity_badge(severity)
                event_type = _event_type_label(event.get("type", ""))
                title = event.get("title", "")
                summary = event.get("summary", "")
                stock_id = event.get("stock_id", "")

                with st.expander(f"{badge} {event_type} — {title}"):
                    st.markdown(f"**{t('event_dashboard.stock_code')}: **`{stock_id}`")

                    # ── Interpretation card (replaces plain summary) ──────
                    interp = get_interpretation(
                        event.get("type", ""),
                        severity,
                        title,
                        summary,
                    )
                    _summary_card(
                        title=t("event_dashboard.historian_interpretation"),
                        content=interp["short"],
                        icon="🧭",
                    )

                    # ── Key concept (ten-second test) ────────────────────
                    st.caption(f"{t('event_dashboard.key_concept')}: {interp['key_concept']}")

                    # ── Drill-down button ────────────────────────────────
                    if st.button(t("event_dashboard.why_button"), key=f"why_{evt_idx}"):
                        drilldown = get_drilldown_interpretation(
                            {
                                "type": event.get("type", ""),
                                "severity": severity,
                                "title": title,
                                "summary": summary,
                            }
                        )
                        _info_card(
                            title=t("event_dashboard.detailed_interpretation"),
                            content=drilldown["detail"],
                            icon="📖",
                        )
                        st.caption(t("event_dashboard.disclaimer"))

                    # ── Raw summary in collapsed section ────────────────
                    with st.expander(t("event_dashboard.raw_summary"), expanded=False):
                        st.markdown(summary)

                    if st.button(t("event_dashboard.view_card"), key=f"evt_{evt_idx}"):
                        navigate_to(page="名片", stock_id=stock_id)
                evt_idx += 1

            st.markdown("")

    st.markdown("---")

    # ── 使用說明 ──────────────────────────────────────────
    st.markdown(f"### 💡 {t('event_dashboard.about_title')}")
    st.markdown(t("event_dashboard.about_content"))

    # ── Data Sources ──
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        {"label": t("event_dashboard.sources.events"), "api": t("event_dashboard.sources.local_db"), "time": now_str},
        {"label": t("event_dashboard.sources.interpretation"), "api": t("event_dashboard.sources.templates"), "time": now_str},
    ]
    _source_section(sources, now_str)


def _render_adaptive_banner(data: dict):
    """在頁面頂部顯示自適應分析框架推薦"""
    company_type = detect_company_type(data)
    framework = get_adaptive_framework(company_type)

    if company_type != "default":
        _info_card(
            title=t('event_dashboard.analysis_framework', name=framework['name']),
            content=f"{framework['description']} — {framework['focus']}",
        )


def _render_event_alerts(stock_id: str):
    """在股票頁面顯示近期事件提醒"""
    events = get_events_for_stock(stock_id, days=30)
    if not events:
        return

    high_events = [e for e in events if e.get("severity") == "high"]
    medium_events = [e for e in events if e.get("severity") == "medium"]

    if high_events:
        high_details = "\n".join(
            f"- **{e['title']}**：{e['summary']}" for e in high_events[:3]
        )
        _summary_card(
            title=t('event_dashboard.high_events_alert', count=len(high_events)),
            content=high_details,
            icon="⚠️",
        )

    if medium_events:
        medium_details = "\n".join(
            f"- **{e['title']}**：{e['summary']}" for e in medium_events[:2]
        )
        _info_card(
            title=t('event_dashboard.medium_events_alert', count=len(medium_events)),
            content=medium_details,
            icon="📌",
        )
