"""
Stock Screener / Discovery Engine — C42
Beginner-friendly stock discovery tool.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card, _section_title
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.stock_screener_service import (
    get_all_stocks_with_metrics,
    apply_preset_filter,
    apply_custom_filter,
    format_screening_results,
)
from src.services.screener_explanation_provider import ScreenerExplanationProvider

# ── Singleton provider ──────────────────────────────────────────────
_screener_provider = ScreenerExplanationProvider()


def _render_stock_screener(client: FinMindClient):
    """Stock Screener main page — discover stocks by criteria."""
    st.markdown("## 🔎 股票探索引擎")
    st.markdown("不知道從哪開始？用篩選條件發現適合你的股票")
    st.markdown("---\n")

    # ── Mode selector ──────────────────────────────────────
    mode = st.radio(
        "選擇模式",
        ["新手模式", "進階模式"],
        horizontal=True,
        key="screener_mode",
        label_visibility="collapsed",
    )

    # ── Load data ──────────────────────────────────────────
    if "screener_data" not in st.session_state:
        st.session_state["screener_data"] = None

    load_col, _ = st.columns([1, 3])
    with load_col:
        if st.button("🔄 載入股票資料", key="screener_load", use_container_width=True):
            with st.spinner("載入股票資料中…"):
                df = get_all_stocks_with_metrics(client)
            st.session_state["screener_data"] = df
            if not df.empty:
                st.success(f"已載入 {len(df)} 檔股票資料")
            else:
                st.warning("無法載入股票資料")

    df = st.session_state.get("screener_data")

    if df is None:
        _info_card(
            "請先載入資料",
            "點擊上方「載入股票資料」按鈕，取得最新股票數據。",
            icon="📊",
        )
        st.markdown("---\n")
        _historian_disclaimer("general")
        return

    if df.empty:
        _info_card(
            "沒有股票資料",
            "資料載入為空，請檢查 API 連線或稍後再試。",
            icon="⚠️",
        )
        st.markdown("---\n")
        _historian_disclaimer("general")
        return

    st.markdown("\n")

    # ── Filtering ──────────────────────────────────────────
    filtered_df = df.copy()

    if mode == "新手模式":
        _render_beginner_mode(df)
    else:
        _render_advanced_mode(df)

    st.markdown("---\n")
    _historian_disclaimer("general")


def _render_beginner_mode(df: pd.DataFrame):
    """Render beginner mode with preset profiles."""
    _section_title(f"🎯 選擇你的投資風格")

    # Preset cards
    col1, col2, col3 = st.columns(3)

    preset = st.session_state.get("screener_preset", None)

    with col1:
        is_selected = preset == "dividend"
        border_color = "#27AE60" if is_selected else "#BDC3C7"
        bg_color = "#E8F8F5" if is_selected else "#F8F9FA"
        st.markdown(
            f"""<div style="background:{bg_color};border-radius:12px;padding:1.2rem;
            border:2px solid {border_color};text-align:center;cursor:pointer;">
                <div style="font-size:2rem;">💰</div>
                <div style="font-weight:600;color:#2C3E50;margin-top:0.5rem;">穩定收息</div>
                <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.3rem;">
                    殖利率 &gt; 3%<br>波動較小
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("選擇", key="screener_preset_dividend", use_container_width=True):
            st.session_state["screener_preset"] = "dividend"
            preset = "dividend"
            st.rerun()

    with col2:
        is_selected = preset == "growth"
        border_color = "#3498DB" if is_selected else "#BDC3C7"
        bg_color = "#EBF5FB" if is_selected else "#F8F9FA"
        st.markdown(
            f"""<div style="background:{bg_color};border-radius:12px;padding:1.2rem;
            border:2px solid {border_color};text-align:center;cursor:pointer;">
                <div style="font-size:2rem;">🚀</div>
                <div style="font-weight:600;color:#2C3E50;margin-top:0.5rem;">成長潛力</div>
                <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.3rem;">
                    營收成長 &gt; 10%<br>具成長動能
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("選擇", key="screener_preset_growth", use_container_width=True):
            st.session_state["screener_preset"] = "growth"
            preset = "growth"
            st.rerun()

    with col3:
        is_selected = preset == "value"
        border_color = "#9B59B6" if is_selected else "#BDC3C7"
        bg_color = "#F5EEF8" if is_selected else "#F8F9FA"
        st.markdown(
            f"""<div style="background:{bg_color};border-radius:12px;padding:1.2rem;
            border:2px solid {border_color};text-align:center;cursor:pointer;">
                <div style="font-size:2rem;">💎</div>
                <div style="font-weight:600;color:#2C3E50;margin-top:0.5rem;">便宜估值</div>
                <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.3rem;">
                    PER &lt; 15<br>PBR &lt; 2
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("選擇", key="screener_preset_value", use_container_width=True):
            st.session_state["screener_preset"] = "value"
            preset = "value"
            st.rerun()

    # Apply filter and show results
    if preset:
        filtered_df = apply_preset_filter(df, preset)
        _render_results(filtered_df, preset=preset)


def _render_advanced_mode(df: pd.DataFrame):
    """Render advanced mode with custom filters."""
    _section_title(f"⚙️ 自訂篩選條件")

    # Get unique industries
    industries = sorted(df["industry_category"].dropna().unique().tolist())
    industries = [i for i in industries if i.strip()]
    industry_options = ["全部"] + industries

    col1, col2 = st.columns(2)

    with col1:
        selected_industry = st.selectbox(
            "產業分類",
            industry_options,
            key="screener_industry",
        )

    with col2:
        revenue_growth = st.checkbox(
            "只顯示營收正成長",
            key="screener_revenue_growth",
        )

    col3, col4 = st.columns(2)

    with col3:
        per_range = st.slider(
            "本益比 (PER) 範圍",
            min_value=0,
            max_value=50,
            value=(0, 50),
            key="screener_per_range",
        )

    with col4:
        div_range = st.slider(
            "殖利率 (%) 範圍",
            min_value=0.0,
            max_value=15.0,
            value=(0.0, 15.0),
            step=0.5,
            key="screener_div_range",
        )

    # Apply filters
    filters = {
        "industry": selected_industry,
        "per_min": per_range[0] if per_range[0] > 0 else None,
        "per_max": per_range[1] if per_range[1] < 50 else None,
        "div_min": div_range[0] if div_range[0] > 0 else None,
        "div_max": div_range[1] if div_range[1] < 15 else None,
        "revenue_growth": revenue_growth,
    }
    filtered_df = apply_custom_filter(df, filters)
    _render_results(filtered_df, filters=filters)


def _render_results(filtered_df: pd.DataFrame, preset: str | None = None, filters: dict | None = None):
    """Render screening results as card grid with AI explanations."""
    st.markdown("---\n")
    _section_title(f"📋 篩選結果")

    count = len(filtered_df)
    st.markdown(f"**符合條件的股票：{count} 檔**\n")

    if count == 0:
        _info_card(
            "沒有符合條件的股票",
            "試著放寬篩選條件，或選擇不同的投資風格。",
            icon="🔍",
        )
        return

    results = format_screening_results(filtered_df)

    # Display as card grid (3 columns)
    cols_per_row = 3
    for i in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(results):
                break
            r = results[idx]
            with cols[j]:
                # Build explanation context from the row data
                row_data = filtered_df[filtered_df["stock_id"] == r["stock_id"]]
                explanation = ""
                if not row_data.empty:
                    row = row_data.iloc[0]
                    context = {
                        "stock_name": r["stock_name"],
                        "stock_id": r["stock_id"],
                        "preset": preset,
                        "filters": filters,
                        "per": row.get("per"),
                        "pbr": row.get("pbr"),
                        "dividend_yield": row.get("dividend_yield"),
                        "revenue_yoy": row.get("revenue_yoy"),
                        "industry": r.get("industry", ""),
                    }
                    from src.services.llm.base import ExplanationRequest
                    req = ExplanationRequest(
                        metric_name="screener",
                        metric_value=r["key_metric"],
                        context=context,
                    )
                    resp = _screener_provider.explain(req)
                    explanation = resp.text

                st.markdown(
                    f"""<div style="background:#F8F9FA;border-radius:12px;
                    padding:1rem;border-left:4px solid #3498DB;
                    margin-bottom:0.5rem;">
                        <div style="font-size:0.75rem;color:#7F8C8D;">
                            {r['stock_id']} ｜ {r['industry']}
                        </div>
                        <div style="font-weight:600;color:#2C3E50;font-size:1.1rem;">
                            {r['stock_name']}
                        </div>
                        <div style="font-size:0.85rem;color:#27AE60;font-weight:600;
                        margin-top:0.3rem;">
                            {r['key_metric']}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                # Show explanation if available
                if explanation:
                    _summary_card(
                        "篩選說明",
                        explanation,
                        icon="🔍",
                        border_color="#3498DB",
                    )
                if st.button(
                    "查看",
                    key=f"screener_goto_{r['stock_id']}_{idx}",
                    use_container_width=True,
                ):
                    navigate_to(page="名片", stock_id=r["stock_id"])
