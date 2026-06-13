"""Business card main orchestrator."""
import streamlit as st
import pandas as pd
from datetime import datetime, date

from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_pbr_analogy,
)
from src.services.key_takeaways import generate_key_takeaways
from src.services.delta_engine import compute_recent_deltas
from src.services.health_scoring import compute_health_scores, get_health_summary
from src.services.risk_analyzer import assess_risk
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.services.watchlist import (
    is_in_watchlist,
    is_in_any_list,
    get_lists_for_stock,
    add_to_watchlist,
    remove_from_all_lists,
    remove_from_watchlist,
    create_list,
    list_names,
)
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.url_sync import navigate_to

from src.pages.business_card._sections import (
    _render_header,
    _render_story_card,
    _render_takeaways,
    _render_deltas,
    _render_health,
    _render_risk,
    _render_one_liner,
    _render_key_metrics,
    _render_dividend,
    _render_revenue_breakdown,
    _render_revenue_trend,
    _render_valuation,
    _render_compare_stories,
    _render_news,
    _render_read_next,
    _render_share_section,
    _render_footer,
)
from src.pages.business_card._study_log import _render_study_log
from src.pages.business_card._expert_analysis import _render_expert_analysis
from src.pages.business_card._historical_scenarios import _render_historical_scenarios


def _render_simple_overview(data: dict, client) -> None:
    """Render a simplified beginner-friendly summary of the key detail sections.

    This is shown in simple mode INSTEAD of the detail-heavy sections
    (health, risk, dividend details, revenue breakdown/trend, valuation,
    expert analysis, historical scenarios).
    """
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]
    dividend_data = data.get("dividend") if isinstance(data, dict) else None

    # ── Quick health summary (1-line) ──
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        overall = sum(health_scores.values()) / len(health_scores)
        if overall >= 70:
            health_text = "🟢 整體健康度良好，各項指標表現不錯"
        elif overall >= 40:
            health_text = "🟡 整體健康度中等，部分指標還有改善空間"
        else:
            health_text = "🔴 整體健康度偏弱，需要留意風險"
        _summary_card("公司健康狀況", f"{health_text}（{overall:.0f}/100）", "🏥")

    # ── Key financial snapshot ──
    snap_parts = []
    if latest_per_pbr and latest_per_pbr.get("PER") is not None:
        snap_parts.append(f"本益比 {latest_per_pbr['PER']:.1f}")
    if extra_metrics.get("gross_margin") is not None:
        snap_parts.append(f"毛利率 {extra_metrics['gross_margin']:.1f}%")
    if latest_per_pbr and latest_per_pbr.get("dividend_yield") is not None:
        snap_parts.append(f"殖利率 {latest_per_pbr['dividend_yield']:.2f}%")
    if extra_metrics.get("roe") is not None:
        snap_parts.append(f"ROE {extra_metrics['roe']:.1f}%")
    if snap_parts:
        _summary_card("關鍵財務數據", "｜".join(snap_parts), "💰")

    # ── Dividend snapshot ──
    _current_price = None
    _lp = data.get("latest_price")
    if _lp and _lp.get("close"):
        _current_price = float(_lp["close"])
    div_summary = extract_dividend_summary(dividend_data, current_price=_current_price)
    if div_summary["has_data"]:
        div_line = f"最近一季配 {div_summary['latest_cash_div']:.2f} 元"
        if div_summary["estimated_yield"]:
            div_line += f"｜年化殖利率約 {div_summary['estimated_yield']:.2f}%"
        _summary_card("配息概況", div_line, "💵")
    else:
        _summary_card("配息概況", "這家目前沒有配發股利", "💡")

    # ── Revenue at a glance ──
    if len(monthly_revenue) > 0:
        rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
        yoy = extra_metrics.get("revenue_yoy")
        rev_line = f"最近月營收約 {rev:,.0f} 億"
        if yoy is not None:
            direction = "成長" if yoy >= 0 else "衰退"
            rev_line += f"（較去年同期 {direction} {abs(yoy):.1f}%）"
        _summary_card("營收概況", rev_line, "📈")


def _render_business_card(data: dict, client):
    """公司名片主頁（M1）— orchestrator"""
    # ── Data extraction ──
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]
    news = data["news"]
    extra_metrics = data["extra_metrics"]

    # ── Section dispatch (always shown) ──
    _render_header(data, client)

    # ── C105: Simple/Detailed toggle ──
    # Default to simple mode (beginner-friendly)
    _toggle_col1, _toggle_col2 = st.columns([3, 1])
    with _toggle_col2:
        simple_mode = st.toggle("簡易模式", value=True, key="simple_mode_toggle")
    st.session_state["simple_mode"] = simple_mode
    if simple_mode:
        st.caption("🔰 簡易模式：只顯示重點摘要，适合新手快速瀏覽")
    else:
        st.caption("📖 詳細模式：顯示完整數據與深度分析")

    # ── Sections always shown in both modes ──
    _render_story_card(data, client)
    _render_takeaways(data, client)
    _render_deltas(data, client)
    _render_one_liner(data, client)
    _render_news(data, client)
    _render_study_log(data, client)

    # ── C105: Conditional detail sections ──
    if simple_mode:
        # Simple mode: show a compact overview instead of detail-heavy sections
        _render_simple_overview(data, client)
    else:
        # Detailed mode: show full data tables, charts, and analysis
        _render_health(data, client)
        _render_risk(data, client)
        _render_key_metrics(data, client)
        _render_dividend(data, client)
        _render_revenue_breakdown(data, client)
        _render_revenue_trend(data, client)
        _render_valuation(data, client)
        _render_expert_analysis(data, client)
        _render_historical_scenarios(data, client)

    # ── Footer sections (always shown) ──
    all_info = client.get_stock_info()
    _render_compare_stories(data, client, all_info=all_info)
    _render_read_next(data, client, all_info=all_info)
    _render_share_section(data, client)
    _render_footer(data, client)
