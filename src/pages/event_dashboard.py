"""
股識 Stock Explorer — M5 事件儀表板
顯示近期重大事件、資料新鮮度、自適應框架推薦
"""

import streamlit as st
import pandas as pd
from src.services.adaptive_engine import (
    get_all_recent_events,
    get_events_for_stock,
    detect_company_type,
    get_adaptive_framework,
    check_data_freshness,
    SEVERITY_SCORES,
)


def _severity_badge(severity: str) -> str:
    """產生嚴重程度標籤"""
    badges = {
        "high": "🔴 重大",
        "medium": "🟡 注意",
        "low": "🟢 參考",
    }
    return badges.get(severity, "⚪ 未知")


def _freshness_badge(status: str) -> str:
    """產生新鮮度標籤"""
    badges = {
        "fresh": "🟢 最新",
        "stale": "🟡 較舊",
        "very_stale": "🔴 過時",
        "partial": "🟡 部分更新",
        "unknown": "⚪ 未知",
    }
    return badges.get(status, "⚪ 未知")


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


def _render_event_dashboard(client):
    """事件儀表板主頁面"""
    st.markdown("## 🔔 事件儀表板")
    st.markdown("*近期市場重大事件與異動*")
    st.markdown("---")

    # ── 近期重大事件 ──────────────────────────────────────
    st.markdown("### 📋 近期重大事件")

    recent_events = get_all_recent_events(days=30, limit=50)

    if not recent_events:
        st.info("近期無重大事件記錄。事件會在瀏覽股票頁面時自動偵測。")
    else:
        # 依日期分組顯示
        dates = {}
        for event in recent_events:
            date = event.get("date", "未知")
            if date not in dates:
                dates[date] = []
            dates[date].append(event)

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
                    st.markdown(f"**股票代號：** `{stock_id}`")
                    st.markdown(f"**摘要：** {summary}")
                    if st.button("查看名片", key=f"evt_{stock_id}_{title[:20]}"):
                        st.session_state["stock_id"] = stock_id
                        st.session_state["page"] = "名片"
                        st.rerun()

            st.markdown("")

    st.markdown("---")

    # ── 使用說明 ──────────────────────────────────────────
    st.markdown("### 💡 關於事件儀表板")
    st.markdown("""
    事件儀表板會自動偵測以下類型的重大變化：

    | 事件類型 | 觸發條件 | 嚴重程度 |
    |----------|----------|----------|
    | 💰 營收異動 | 月營收 YoY 變化 ±30% 以上 | 🟡~🔴 |
    | 📰 重大新聞 | 新聞標題包含收購、合併、虧損等關鍵字 | 🔴 |
    | 📰 注意新聞 | 新聞標題包含股利、訂單、合作等關鍵字 | 🟡 |
    | 📉 股價異常 | 單日漲跌幅超過 ±7% | 🔴 |

    事件會在瀏覽股票頁面時自動偵測並記錄。
    """)


def _render_freshness_indicator(freshness: dict):
    """在頁面頂部顯示資料新鮮度指標"""
    overall = freshness.get("overall", "unknown")
    needs_update = freshness.get("needs_update", False)

    if needs_update:
        st.warning("⚠️ 部分資料可能較舊，建議重新載入以取得最新資訊。")

    # 可展開的詳情
    items = freshness.get("items", [])
    if items:
        with st.expander("📡 資料新鮮度詳情", expanded=False):
            for item in items:
                badge = _freshness_badge(item["status"])
                st.markdown(
                    f"- **{item['label']}**：{item['date']} "
                    f"（{item['days_old']} 天前）{badge}"
                )


def _render_adaptive_banner(data: dict):
    """在頁面頂部顯示自適應分析框架推薦"""
    company_type = detect_company_type(data)
    framework = get_adaptive_framework(company_type)

    if company_type != "default":
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);
                    border-radius:10px;padding:1rem 1.5rem;margin:0.5rem 0;
                    border-left:4px solid #3498DB;">
            <div style="font-weight:600;color:#2C3E50;">
                🎯 分析框架：{framework['name']}
            </div>
            <div style="font-size:0.85rem;color:#5D6D7E;margin-top:0.3rem;">
                {framework['description']} — {framework['focus']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_event_alerts(stock_id: str):
    """在股票頁面顯示近期事件提醒"""
    events = get_events_for_stock(stock_id, days=30)
    if not events:
        return

    high_events = [e for e in events if e.get("severity") == "high"]
    medium_events = [e for e in events if e.get("severity") == "medium"]

    if high_events:
        st.error(f"🔴 近期有 {len(high_events)} 項重大事件需要注意！")
        for event in high_events[:3]:
            st.markdown(f"- **{event['title']}**：{event['summary']}")

    if medium_events:
        st.warning(f"🟡 近期有 {len(medium_events)} 項注意事件")
        for event in medium_events[:2]:
            st.markdown(f"- **{event['title']}**：{event['summary']}")
