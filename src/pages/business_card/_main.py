"""Business card main orchestrator — Sprint 12 Info Hierarchy."""
import streamlit as st
import pandas as pd
from datetime import datetime, date

from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake, create_revenue_treemap
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
from src.services.risk_simplifier import get_risk_level
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
from src.pages._router_base import _白话_card, _info_card, _summary_card, _beginner_banner
from src.pages.url_sync import navigate_to
from src.pages.revenue_tree import _render_revenue_tree
from src.services.experience_service import is_beginner_mode, set_experience_level

from src.pages.business_card._sections import (
    _render_header,
    _render_story_card,
    _render_takeaways,
    _render_deltas,
    _render_read_next,
    _render_health,
    _render_risk,
    _render_one_liner,
    _render_key_metrics,
    _render_dividend,
    _render_revenue_breakdown,
    _render_revenue_trend,
    _render_valuation,
    _render_news,
    _render_share_section,
    _render_footer,
    _render_historical_pattern,
    _render_why_moved,
)
from src.pages.business_card._study_log import _render_study_log
from src.pages.business_card._expert_analysis import _render_expert_analysis
from src.pages.business_card._historical_scenarios import _render_historical_scenarios
from src.pages.business_card._sections._moat import _render_moat
from src.services.feedback_service import record_feedback, get_feedback_count


_FEEDBACK_SESSION_KEY_PREFIX = "_feedback_given_"


def _feedback_session_key(stock_id: str) -> str:
    return f"{_FEEDBACK_SESSION_KEY_PREFIX}{stock_id}"


def _has_feedbacked(stock_id: str) -> bool:
    return st.session_state.get(_feedback_session_key(stock_id), False)


def _mark_feedbacked(stock_id: str) -> None:
    st.session_state[_feedback_session_key(stock_id)] = True


def _render_feedback_section(data: dict) -> None:
    """Binary 👍/👎 feedback UI at the bottom of the business card.

    Uses st.session_state to prevent duplicate feedback per stock per session.
    Records feedback to data/feedback.jsonl via feedback_service.
    """
    stock_id = data["stock_id"]

    st.markdown("---")
    st.markdown("#### 💬 這張名片對你有幫助嗎？")

    if _has_feedbacked(stock_id):
        st.caption("✅ 感謝你的回饋！")
        return

    col_up, col_down, _ = st.columns([1, 1, 6])

    with col_up:
        if st.button("👍", key=f"feedback_up_{stock_id}", use_container_width=True):
            record_feedback(stock_id=stock_id, feedback_type="up")
            _mark_feedbacked(stock_id)
            st.toast("感謝你的正面回饋！👍", icon="🎉")
            st.rerun()

    with col_down:
        if st.button("👎", key=f"feedback_down_{stock_id}", use_container_width=True):
            record_feedback(stock_id=stock_id, feedback_type="down")
            _mark_feedbacked(stock_id)
            st.toast("感謝你的回饋，我們會持續改進！👎", icon="💪")
            st.rerun()


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

    # ── Health narrative (C14 + C135 merged) ──
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        health_summary = get_health_summary(health_scores)
        _info_card("公司健康狀況", health_summary, "🏥")

    # ── Risk level (C132: simplified 1-5 scale) ──
    risk_level = get_risk_level(data)
    risk_content = (
        f"{risk_level['emoji']} **{risk_level['label']}**（等級 {risk_level['level']}/5）\n\n"
        f"{risk_level['description']}"
    )
    _summary_card("投資風險", risk_content, "⚠️")

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
    """公司名片主頁（M1）— Sprint 12 Info Hierarchy

    Above-fold (first 720px): C37 Key Takeaways, C39 What Changed, C43 Health Snowflake.
    All other sections via progressive disclosure (st.expander) or below the fold.
    C36 (Revenue Tree) and C38 (Compare Stories) relocated to separate pages.
    """
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

    # ── C40: Beginner/Expert mode toggle (replaces C105 simple toggle) ──
    _toggle_col1, _toggle_col2 = st.columns([3, 1])
    with _toggle_col2:
        _current_is_beginner = is_beginner_mode(st.session_state)
        beginner_mode = st.toggle("新手模式", value=_current_is_beginner, key="user_experience_level_toggle")
    # Persist the toggle into the experience level session state
    _new_level = "beginner" if beginner_mode else "expert"
    set_experience_level(st.session_state, _new_level)
    st.session_state["simple_mode"] = beginner_mode
    if beginner_mode:
        _beginner_banner("新手模式：只顯示重點摘要，適合快速瀏覽。隨時可切換回進階模式。")
        st.caption("🌱 新手模式")
    else:
        st.caption("🔬 進階模式：顯示完整數據與深度分析")

    # ══════════════════════════════════════════════════════════
    # ABOVE-FOLD: The 3 most important sections (C37, C39, C43)
    # ══════════════════════════════════════════════════════════

    # C48/C37: Company Story Card + Key Takeaways
    _render_story_card(data, client)
    _render_takeaways(data, client)

    # C39: What Changed — Recent Deltas
    _render_deltas(data, client)

    # C41: Read Next — peer recommendations (above-fold discovery)
    _render_read_next(data, client)

    # C188: Why Did This Move? — plain-language movement explanation
    _render_why_moved(data, client)

    # C43: Health Snowflake
    if beginner_mode:
        # Simple mode: show compact health summary
        _render_simple_overview(data, client)
    else:
        # Detailed mode: show full health snowflake
        _render_health(data, client)

    # ══════════════════════════════════════════════════════════
    # PROGRESSIVE DISCLOSURE: Secondary sections in expanders
    # ══════════════════════════════════════════════════════════

    # ── 一句話定位 + 近期動態 ──
    with st.expander("💡 一句話定位與近期動態", expanded=False):
        _render_one_liner(data, client)
        _render_news(data, client)

    # ── 學習日誌 ──
    with st.expander("📚 學習日誌", expanded=False):
        _render_study_log(data, client)

    # ── Detailed mode: full data sections in expanders ──
    if not beginner_mode:
        # 關鍵數字 + 配息 + 營收組成 + 營收趨勢 + 估值
        with st.expander("📊 關鍵數字與配息", expanded=False):
            _render_key_metrics(data, client)
            _render_dividend(data, client)

        with st.expander("📈 營收組成與趨勢", expanded=False):
            _render_revenue_breakdown(data, client)
            _render_revenue_trend(data, client)

        with st.expander("🌳 營收結構樹", expanded=False):
            st.markdown("*深入拆解這家公司靠什麼賺錢*")
            _render_revenue_tree(data, client)

        with st.expander("💎 估值區間", expanded=False):
            _render_valuation(data, client)

        with st.expander("⚠️ 風險分析", expanded=False):
            _render_risk(data, client)

        with st.expander("🎓 專家分析", expanded=False):
            _render_expert_analysis(data, client)

        with st.expander("🔍 歷史情境", expanded=False):
            _render_historical_scenarios(data, client)

        with st.expander("📊 歷史模式", expanded=False):
            _render_historical_pattern(data, client)



        # ── C46: Moat Analysis ──
        with st.expander("🏰 護城河分析", expanded=False):
            _render_moat(data, client)

    # ══════════════════════════════════════════════════════════
    # 更多分析: Navigation to C36 (Revenue Tree) & C38 (Compare Stories)
    # ══════════════════════════════════════════════════════════
    with st.expander("🔬 更多分析", expanded=False):
        st.markdown("*想更深入了解這家公司？看看以下深度分析：*")
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🌳 營收結構樹", key="nav_revenue_tree", use_container_width=True):
                navigate_to(page="營收結構樹", stock_id=stock_id)
            st.caption("深入拆解營收來源與產品組合")

        with col_b:
            if st.button("📖 同業比較故事", key="nav_compare_stories", use_container_width=True):
                navigate_to(page="同業比較故事", stock_id=stock_id)
            st.caption("與同業的敘事比較分析")

        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("🏰 護城河比較", key="nav_moat_comparison", use_container_width=True):
                navigate_to(page="護城河比較", stock_id=stock_id)
            st.caption("與同業的護城河深度比較")

    # ── Footer sections (always shown) ──
    _render_feedback_section(data)
    _render_share_section(data, client)
    _render_footer(data, client)
