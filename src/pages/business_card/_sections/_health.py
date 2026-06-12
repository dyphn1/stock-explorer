"""Business card section: health and risk sections."""
import streamlit as st
from src.services.chart import create_health_snowflake
from src.services.health_scoring import compute_health_scores, get_health_summary
from src.services.risk_analyzer import assess_risk
from src.pages._router_base import _info_card
from src.pages.business_card._helpers import (
    get_health_dimension_explanation,
    _render_risk_dimension,
    _get_health_metric_values,
)


def _render_health(data: dict, client) -> None:
    """C43 Health Snowflake chart + 5-dimension score cards + summary."""
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    monthly_revenue = data["monthly_revenue"]
    stock_name = data["stock_name"]

    # 🏥 公司健康狀況 (C43: Health Snowflake)
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        st.markdown("### 🏥 公司健康狀況")
        metric_values = _get_health_metric_values(extra_metrics, latest_per_pbr)
        health_fig = create_health_snowflake(stock_name, health_scores, metric_values=metric_values)
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
                metric_html = ""
                if dim_name in metric_values and metric_values[dim_name]:
                    metric_text = " · ".join(metric_values[dim_name])
                    metric_html = f'<div style="font-size:0.7rem;color:#3498DB;margin-top:0.2rem;">{metric_text}</div>'
                st.markdown(
                    f"""
                    <div style="text-align:center;padding:0.5rem;background:#F8F9FA;border-radius:10px;margin:0.2rem 0;">
                        <div style="font-size:0.8rem;color:#7F8C8D;">{indicator} {dim_name}</div>
                        <div style="font-size:1.4rem;font-weight:700;color:#2C3E50;">{score:.0f}</div>
                        <div style="font-size:0.7rem;color:#7F8C8D;margin-top:0.2rem;">{get_health_dimension_explanation(dim_name, score)}</div>
                        {metric_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

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
                st.markdown(
                    f"""<div style="color:#7F8C8D;font-size:0.9rem;margin-bottom:0.8rem;">
                    {risk["summary_text"]}</div>""",
                    unsafe_allow_html=True,
                )
            for dim_key in ("customer_concentration", "financial_health", "event_based"):
                dim = risk.get(dim_key)
                if dim is None:
                    continue
                _render_risk_dimension(dim, stock_name)
