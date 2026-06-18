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
from src.pages._router_base import _info_card, _白话_card, _summary_card, _section_title
from src.pages.business_card._helpers import _historian_disclaimer
from src.services.stock_screener_service import (
    get_all_stocks_with_metrics,
    apply_preset_filter,
    apply_custom_filter,
    format_screening_results,
)
from src.core.i18n import t
from src.services.screener_explanation_provider import ScreenerExplanationProvider

# ── Singleton provider ──────────────────────────────────────────────
_screener_provider = ScreenerExplanationProvider()


def _render_stock_screener(client: FinMindClient):
    """Stock Screener main page — discover stocks by criteria."""
    st.markdown(f"## 🔎 {t('stock_screener.title')}")
    st.markdown(t("stock_screener.subtitle"))
    st.markdown("---\n")

    # ── Mode selector ──────────────────────────────────────
    mode = st.radio(
        t("stock_screener.mode_selector"),
        [t("stock_screener.beginner_mode"), t("stock_screener.advanced_mode")],
        horizontal=True,
        key="screener_mode",
        label_visibility="collapsed",
    )

    # ── Load data ──────────────────────────────────────────
    if "screener_data" not in st.session_state:
        st.session_state["screener_data"] = None

    load_col, _ = st.columns([1, 3])
    with load_col:
        if st.button(f"🔄 {t('stock_screener.load_btn')}", key="screener_load", use_container_width=True):
            with st.spinner(t("stock_screener.loading_data")):
                df = get_all_stocks_with_metrics(client)
            st.session_state["screener_data"] = df
            if not df.empty:
                st.success(t("stock_screener.loaded_count", count=len(df)))
            else:
                st.warning(t("stock_screener.load_failed"))

    df = st.session_state.get("screener_data")

    if df is None:
        _info_card(
            t("stock_screener.please_load_first"),
            t("stock_screener.please_load_first_desc"),
            icon="📊",
        )
        st.markdown("---\n")
        _historian_disclaimer("general")
        return

    if df.empty:
        _info_card(
            t("stock_screener.no_stock_data"),
            t("stock_screener.no_stock_data_desc"),
            icon="⚠️",
        )
        st.markdown("---\n")
        _historian_disclaimer("general")
        return

    st.markdown("\n")

    # ── Filtering ──────────────────────────────────────────
    filtered_df = df.copy()

    if mode == t("stock_screener.beginner_mode"):
        _render_beginner_mode(df)
    else:
        _render_advanced_mode(df)

    st.markdown("---\n")
    _historian_disclaimer("general")


def _render_beginner_mode(df: pd.DataFrame):
    """Render beginner mode with preset profiles."""
    _section_title(f"🎯 {t('stock_screener.choose_style')}")

    # Preset cards
    col1, col2, col3 = st.columns(3)

    preset = st.session_state.get("screener_preset", None)

    with col1:
        selected_marker = " ✅" if preset == "dividend" else ""
        _info_card(f"💰 {t('stock_screener.dividend_title')}{selected_marker}", t("stock_screener.dividend_desc"))
        if st.button(t("stock_screener.btn_select"), key="screener_preset_dividend", use_container_width=True):
            st.session_state["screener_preset"] = "dividend"
            preset = "dividend"
            st.rerun()

    with col2:
        selected_marker = " ✅" if preset == "growth" else ""
        _info_card(f"🚀 {t('stock_screener.growth_title')}{selected_marker}", t("stock_screener.growth_desc"))
        if st.button(t("stock_screener.btn_select"), key="screener_preset_growth", use_container_width=True):
            st.session_state["screener_preset"] = "growth"
            preset = "growth"
            st.rerun()

    with col3:
        selected_marker = " ✅" if preset == "value" else ""
        _info_card(f"💎 {t('stock_screener.value_title')}{selected_marker}", t("stock_screener.value_desc"))
        if st.button(t("stock_screener.btn_select"), key="screener_preset_value", use_container_width=True):
            st.session_state["screener_preset"] = "value"
            preset = "value"
            st.rerun()

    # Apply filter and show results
    if preset:
        filtered_df = apply_preset_filter(df, preset)
        _render_results(filtered_df, preset=preset)


def _render_advanced_mode(df: pd.DataFrame):
    """Render advanced mode with custom filters."""
    _section_title(f"⚙️ {t('stock_screener.custom_filters')}")

    # Get unique industries
    industries = sorted(df["industry_category"].dropna().unique().tolist())
    industries = [i for i in industries if i.strip()]
    industry_options = [t("stock_screener.all_industries")] + industries

    col1, col2 = st.columns(2)

    with col1:
        selected_industry = st.selectbox(
            t("stock_screener.industry_label"),
            industry_options,
            key="screener_industry",
        )

    with col2:
        revenue_growth = st.checkbox(
            t("stock_screener.revenue_growth_only"),
            key="screener_revenue_growth",
        )

    col3, col4 = st.columns(2)

    with col3:
        per_range = st.slider(
            t("stock_screener.per_range"),
            min_value=0,
            max_value=50,
            value=(0, 50),
            key="screener_per_range",
        )

    with col4:
        div_range = st.slider(
            t("stock_screener.div_range"),
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
    _section_title(f"📋 {t('stock_screener.results')}")

    count = len(filtered_df)
    st.markdown(f"**{t('stock_screener.matching_stocks', count=count)}**\n")

    if count == 0:
        _info_card(
            t("stock_screener.no_matching_stocks"),
            t("stock_screener.no_matching_stocks_desc"),
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

                _summary_card(
                    f"{r['stock_name']}  {r['stock_id']} ｜ {r['industry']}",
                    r["key_metric"],
                    icon="📈",
                    border_color="#3498DB",
                )
                # Show explanation if available
                if explanation:
                    _summary_card(
                        t("stock_screener.explanation_title"),
                        explanation,
                        icon="🔍",
                        border_color="#3498DB",
                    )
                if st.button(
                    t("stock_screener.btn_view"),
                    key=f"screener_goto_{r['stock_id']}_{idx}",
                    use_container_width=True,
                ):
                    navigate_to(page="名片", stock_id=r["stock_id"])
