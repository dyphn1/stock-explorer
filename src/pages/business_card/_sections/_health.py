"""Business card section: health and risk sections."""
import streamlit as st
from src.services.chart import create_health_snowflake
from src.services.health_scoring import compute_health_scores, get_health_summary
from src.services.risk_analyzer import assess_risk
from src.pages._router_base import _info_card, _explain_button, _mini_score_card, _glossary_tooltip
from src.pages.business_card._helpers import (
    get_health_dimension_explanation,
    _render_risk_dimension,
    _get_health_metric_values,
)
from src.services import glossary_service
from src.services.benchmarks import (
    get_industry_benchmarks,
    fetch_benchmark_health_scores,
)

# Re-export INDUSTRY_BENCHMARKS for backward compatibility
INDUSTRY_BENCHMARKS = get_industry_benchmarks()

# Backward-compatible alias
_fetch_benchmark_health_scores = fetch_benchmark_health_scores


def _render_health(data: dict, client) -> None:
    """C43 Health Snowflake chart + 5-dimension score cards + summary."""
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    monthly_revenue = data["monthly_revenue"]
    stock_name = data["stock_name"]
    stock_id = data["stock_id"]
    industry = data["industry"]

    # C170: beginner mode → more prominent glossary indicators
    _is_beginner = st.session_state.get("simple_mode", False) or st.session_state.get("user_experience_level", "beginner") == "beginner"

    # 🏥 公司健康狀況 (C43: Health Snowflake)
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        st.markdown("### 🏥 公司健康狀況")

        # ── Fetch benchmark overlay data ──
        benchmark_scores = None
        benchmark_label = "同業平均"
        if industry:
            benchmark_scores = _fetch_benchmark_health_scores(client, industry, stock_id)
            if benchmark_scores:
                # Determine label: use the benchmark company name
                bench_info = INDUSTRY_BENCHMARKS.get(industry)
                if bench_info:
                    _, bench_name = bench_info
                    benchmark_label = f"{bench_name}"

        metric_values = _get_health_metric_values(extra_metrics, latest_per_pbr)
        health_fig = create_health_snowflake(
            stock_name,
            health_scores,
            metric_values=metric_values,
            benchmark_scores=benchmark_scores,
            benchmark_label=benchmark_label,
        )
        st.plotly_chart(health_fig, use_container_width=True)

        # 五維度分數明細
        dim_cols = st.columns(5)
        for i, (dim_name, score) in enumerate(health_scores.items()):
            with dim_cols[i]:
                if score >= 70:
                    indicator = "🟢"
                elif score >= 40:
                    indicator = "🟡"
                else:
                    indicator = "🔴"
                _mini_score_card(f"{indicator} {dim_name}", score)
                explanation = get_health_dimension_explanation(dim_name, score)
                if explanation:
                    st.caption(explanation)
                if dim_name in metric_values and metric_values[dim_name]:
                    metric_text = " · ".join(metric_values[dim_name])
                    st.caption(metric_text)
                _explain_button(
                    metric_name=dim_name,
                    metric_value=f"{score:.0f} 分",
                    key_prefix=f"health_{stock_id}",
                    source_label="📊 系統估算",
                )
                # C170: Glossary tooltip for each health dimension
                _gkey = glossary_service.resolve_term_key(dim_name)
                if _gkey:
                    _glossary_tooltip(_gkey, glossary_service, beginner=_is_beginner)

        # 白話健康摘要
        health_summary = get_health_summary(health_scores)
        _info_card("健康摘要", health_summary, "🏥")


def _render_risk(data: dict, client) -> None:
    """C44 Risk Analysis with expandable dimensions."""
    stock_name = data["stock_name"]

    # ⚠️ 風險分析 (C44: Risk Analysis)
    risk = assess_risk(data)
    has_risk_dims = any(
        risk.get(dim) is not None
        for dim in ("customer_concentration", "financial_health", "event_based")
    )
    if has_risk_dims:
        with st.expander("⚠️ 風險分析 — 什麼可能出問題？", expanded=False):
            if risk.get("summary_text"):
                st.caption(risk["summary_text"])
            for dim_key in ("customer_concentration", "financial_health", "event_based"):
                dim = risk.get(dim_key)
                if dim is None:
                    continue
                _render_risk_dimension(dim, stock_name)
