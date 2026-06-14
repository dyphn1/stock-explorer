"""
路由器共享工具函式
"""

import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from src.data.finmind_client import FinMindClient, FinMindRateLimitError
from src.services.financial_metrics import calc_extra_metrics, find_financial_value


def get_stock_data(client: FinMindClient, stock_id: str) -> dict:
    """載入一支股票的所有資料，回傳 dict。gate check sequential，其餘資料平行載入。"""
    stock_info = client.get_stock_info(stock_id)
    if len(stock_info) == 0:
        return None

    stock_name = stock_info.iloc[0]["stock_name"]
    industry = stock_info.iloc[0]["industry_category"]

    data = {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "industry": industry,
    }

    # ── 定義每個 fetch task：(name, lambda) ──
    tasks = [
        ("latest_price",         lambda: client.get_latest_price(stock_id)),
        ("latest_per_pbr",       lambda: client.get_latest_per_pbr(stock_id)),
        ("monthly_revenue",      lambda: client.get_monthly_revenue(stock_id)),
        ("daily_price",          lambda: client.get_daily_price(stock_id)),
        ("financial",            lambda: client.get_financial_statement(stock_id)),
        ("news",                 lambda: client.get_news(stock_id)),
        ("institutional",        lambda: client.get_institutional_investors(stock_id)),
        ("balance_sheet",        lambda: client.get_balance_sheet(stock_id)),
        ("cash_flow",            lambda: client.get_cash_flow(stock_id)),
        ("dividend",             lambda: client.get_dividend(stock_id)),
    ]

    def _fetch(name, fn):
        try:
            return name, fn()
        except FinMindRateLimitError:
            # Set session state flag so UI can show a warning
            st.session_state["_rate_limited"] = True
            return name, None
        except Exception:
            return name, None

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_fetch, name, fn): name for name, fn in tasks}
        for future in as_completed(futures):
            name, result = future.result()
            data[name] = result

    data["extra_metrics"] = calc_extra_metrics(
        data["financial"], data["balance_sheet"], data["monthly_revenue"]
    )

    if st.session_state.get("_rate_limited"):
        st.warning("⚠️ API 速率限制已達上限，部分資料可能無法載入。請稍後再試。")
        st.session_state["_rate_limited"] = False  # reset after showing

    return data


def _section_title(title: str):
    if not title:
        return  # don't render anything for empty titles

    first_char = title[0]
    code = ord(first_char)
    if ( (0x1F300 <= code <= 0x1F5FF) or
         (0x1F600 <= code <= 0x1F64F) or
         (0x1F680 <= code <= 0x1F6FF) or
         (0x1F900 <= code <= 0x1F9FF) or
         (0x1FA70 <= code <= 0x1FAFF) or
         (0x2600 <= code <= 0x26FF) or
         (0x2700 <= code <= 0x27BF) or
         (0x1F1E6 <= code <= 0x1F1FF) ):
        st.markdown(f"### {title}")
    else:
        st.markdown(f"### 📊 {title}")


def _explain_button(
    metric_name: str,
    metric_value: str,
    delta: str = "",
    context: dict | None = None,
    key_prefix: str = "",
    source_label: str = "📊 系統估算",
) -> None:
    """Render a 💡 button that opens a popover with a plain-language metric explanation.

    Uses TemplateExplanationProvider from the D5 LLM abstraction layer.
    Shows source badge via st.caption() (C141).

    Args:
        metric_name: The metric name (e.g. "月營收", "ROE")
        metric_value: The metric value as display string
        delta: Optional delta string (e.g. "+5.2%", "-3.1%")
        context: Optional dict with additional context (industry, direction, etc.)
        key_prefix: Unique prefix for the popover button key
        source_label: Source badge text shown via st.caption() at bottom of popover
    """
    from src.services.metric_explainer import get_metric_explanation_for_popover

    popover_key = f"explain_{key_prefix}_{metric_name}"
    try:
        explanation = get_metric_explanation_for_popover(
            metric_name=metric_name,
            metric_value=metric_value,
            delta=delta,
            context=context or {},
        )
        with st.popover("💡", key=popover_key, help=f"解釋「{metric_name}」"):
            st.markdown(f"**{explanation['display_name']}**")
            st.markdown(f"_{explanation['value_text']}_")
            st.markdown("---")
            st.markdown(explanation["explanation_text"])
            st.caption(source_label)
    except Exception:
        with st.popover("💡", key=popover_key, help=f"解釋「{metric_name}」"):
            st.markdown(f"**{metric_name}**")
            st.markdown(f"_{metric_value}_")
            st.info("暫時無法產生解釋，請稍後再試。")
            st.caption(source_label)


def _白话_card(label: str, value: str, analogy: str = ""):
    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
        <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
        <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{analogy}</div>
    </div>
    """, unsafe_allow_html=True)

def _summary_card(title: str, content: str, icon: str = "📋", border_color: str = "#F39C12"):
    st.markdown(f"""
    <div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid {border_color};margin:0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
        <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def _mini_score_card(label: str, score: float) -> None:
    """Render a mini score card with score-based border color.

    Args:
        label: Display label (e.g. dimension name or company name).
        score: Numeric score (0-100). Determines border color:
            green (#27AE60) >= 70, amber (#F39C12) >= 40, red (#E74C3C) < 40.
    """
    if score >= 70:
        score_color = "#27AE60"
    elif score >= 40:
        score_color = "#F39C12"
    else:
        score_color = "#E74C3C"

    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:8px;padding:0.5rem;border-left:4px solid {score_color};text-align:center;">
        <div style="font-size:0.75rem;color:#7F8C8D;">{label}</div>
        <div style="font-size:1.2rem;font-weight:700;color:#2C3E50;">{score:.0f}</div>
    </div>
    """, unsafe_allow_html=True)



def _info_card(title: str, content: str, icon: str = "💡"):
    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
        <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def _so_what_box(deltas: list[dict]) -> None:
    """Render a 'So What?' implication box summarizing all deltas.

    C149: A dedicated visual callout that answers 'What does this mean?'
    Uses historian tone — factual past-tense observations only.
    Only shown when there are 2+ active deltas.

    Args:
        deltas: List of delta dicts, each containing at least:
            metric_name, direction, change_pct, implication
    """
    if len(deltas) < 2:
        return

    # Build a synthesized implication from all delta implications
    parts: list[str] = []
    for d in deltas:
        implication = d.get("implication", "")
        if implication:
            parts.append(implication)

    if not parts:
        return

    # Join with period + space for natural reading
    synthesized = "；".join(parts)

    st.markdown(f"""
    <div style="background:#F0F7FF;border-radius:12px;padding:1.2rem;border-left:4px solid #2980B9;margin:0.8rem 0 0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">🧭 所以呢？</div>
        <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;line-height:1.7;">{synthesized}</div>
    </div>
    """, unsafe_allow_html=True)


def _subsidiary_card(name: str, hold_label: str, hold_color: str,
                     holding: int, revenue: int, business: str, relation: str):
    """Render a subsidiary card with holding badge, business description, and relation.

    Args:
        name: Subsidiary company name.
        hold_label: Badge text (e.g. '🔴 控股子公司').
        hold_color: Hex color code for the badge (e.g. '#E74C3C').
        holding: Ownership percentage.
        revenue: Revenue contribution percentage.
        business: Plain-language description of what the subsidiary does.
        relation: Plain-language description of the parent-subsidiary relationship.
    """
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:1.5rem;border:1px solid #ECF0F1;margin:0.8rem 0;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.1rem;font-weight:700;color:#2C3E50;">{name}</span>
                <span style="background:{hold_color}15;color:{hold_color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;font-weight:600;margin-left:0.5rem;">
                    {hold_label}
                </span>
            </div>
            <div style="text-align:right;">
                <span style="font-size:0.85rem;color:#7F8C8D;">持股 {holding}%</span>
                <span style="font-size:0.85rem;color:#7F8C8D;margin-left:1rem;">營收貢獻 ~{revenue}%</span>
            </div>
        </div>
        <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.8rem;line-height:1.6;">
            <strong>在做什麼：</strong>{business}
        </div>
        <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;line-height:1.5;">
            <strong>跟母公司的關係：</strong>{relation}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _count_label(count: int, label: str):
    """Render a muted count label (e.g. '共找到 42 檔 ETF').

    Args:
        count: The number to display.
        label: Descriptive text after the count.
    """
    st.markdown(
        f"<div style='color:#7F8C8D;font-size:0.85rem;'>共找到 <b>{count}</b> {label}</div>",
        unsafe_allow_html=True,
    )


def _glossary_tooltip(term_key: str, glossary_service):
    """Render a clickable ℹ️ tooltip that shows glossary definition.

    Uses st.popover to show plain-language explanation.
    """
    term = glossary_service.get_glossary_term(term_key)
    if term is None:
        return

    name = term.get("name", term_key)
    plain = term.get("plain", "")
    example = term.get("example", "")
    analogy = term.get("analogy", "")

    popover_label = f"ℹ️ {name}"
    with st.popover(popover_label):
        st.markdown(f"**{name}**")
        st.markdown(f"_{plain}_")
        if example:
            st.markdown(f"**例子：** {example}")
        if analogy:
            st.markdown(f"**比喻：** {analogy}")


# ── M3: Timeline helpers ──────────────────────────────────

_TIMELINE_OPTIONS = {
    "1Y": 365,
    "3Y": 365 * 3,
    "5Y": 365 * 5,
    "ALL": None,
}

_TIMELINE_LABELS = {
    "1Y": "1 年",
    "3Y": "3 年",
    "5Y": "5 年",
    "ALL": "全部",
}


def filter_by_timeline(
    df: pd.DataFrame, date_col: str = "date", timeline_key: str = "timeline_range"
) -> pd.DataFrame:
    """
    根據 session_state[timeline_key] 過濾 dataframe。

    Args:
        df: 要過濾的 dataframe，必須包含 date_col 欄位。
        date_col: 日期欄位名稱，預設為 'date'。
        timeline_key: session_state 中的時間軸 key，預設為 'timeline_range'。

    Returns:
        過濾後的 dataframe。過濾失敗或結果為空時回傳原始 df 並顯示提示。
    """
    if df is None or len(df) == 0:
        return df

    selected = st.session_state.get(timeline_key, "3Y")

    if selected == "ALL":
        return df

    days = _TIMELINE_OPTIONS.get(selected)
    if days is None:
        return df

    try:
        dates = pd.to_datetime(df[date_col])
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        mask = dates >= cutoff
        filtered_df = df[mask].reset_index(drop=True)
    except (ValueError, TypeError, KeyError) as e:
        st.warning(f"⚠️ 時間軸過濾失敗（{e}），已顯示全部資料")
        return df
    except Exception as e:
        st.warning(f"⚠️ 時間軸過濾異常，已顯示全部資料")
        return df

    # Filtered result is empty — fall back to full data with info
    if len(filtered_df) == 0:
        st.info("📌 此時間範圍內無資料，已切換至全部資料")
        return df

    return filtered_df


# ── C163: Shared lesson mode components ─────────────────────────────

def _lesson_card(title: str, content: str, icon: str = "📖", visual_area: str | None = None) -> None:
    """Full-width lesson card with visual area and navigation."""
    visual_html = ""
    if visual_area:
        visual_html = f'<div style="background:#EBF5FB;border-radius:8px;padding:1rem;margin-bottom:0.8rem;font-size:0.9rem;">{visual_area}</div>'
    st.markdown(
        f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin-bottom:1rem;">
            <div style="font-size:1.1rem;font-weight:600;color:#2C3E50;margin-bottom:0.5rem;">{icon} {title}</div>
            {visual_html}
            <div style="font-size:0.9rem;color:#5D6D7E;line-height:1.6;">{content}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def _progress_dots(current: int, total: int, active_color: str = "#27AE60", inactive_color: str = "#BDC3C7") -> None:
    """Lesson progress dot indicators."""
    dots = []
    for i in range(total):
        color = active_color if i == current else inactive_color
        size = "12px" if i == current else "10px"
        dots.append(f'<span style="display:inline-block;width:{size};height:{size};border-radius:50%;background:{color};margin:0 4px;"></span>')
    st.markdown(
        f'<div style="text-align:center;padding:0.5rem 0;">{"".join(dots)}</div>',
        unsafe_allow_html=True,
    )


def _beginner_banner(message: str, icon: str = "🌱") -> None:
    """In-page banner for beginner mode."""
    st.markdown(
        f"""<div style="background:#E8F8F5;border-radius:12px;padding:1rem 1.2rem;border-left:4px solid #27AE60;margin-bottom:1rem;">
            <span style="font-size:1.1rem;">{icon}</span>
            <span style="font-size:0.9rem;color:#27AE60;margin-left:0.5rem;">{message}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def _advanced_content_expander(title: str, content: str, icon: str = "🔬") -> None:
    """Collapsible section for advanced content."""
    with st.expander(f"{icon} {title}", expanded=False):
        st.markdown(content)
