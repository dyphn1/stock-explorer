"""Business card section: Moat Analysis (C46 + C124)."""
import streamlit as st
from src.services.moat_analyzer import get_moat_summary
from src.pages._router_base import _info_card, _summary_card, _mini_score_card, _explain_button
from src.core.i18n import t


def _score_color(score):
    if score >= 70:
        return "🟢"
    elif score >= 40:
        return "🟡"
    else:
        return "🔴"


def _render_moat(data: dict, client) -> None:
    """C46 Moat Analysis section — competitive advantage assessment."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    monthly_revenue = data["monthly_revenue"]

    summary = get_moat_summary(stock_id, extra_metrics, latest_per_pbr, financial, monthly_revenue)

    if not summary["has_data"]:
        _info_card(t("moat.no_data_title"), t("moat.no_data_content", stock_name=stock_name), "🏰")
        return

    # Moat type badge
    _info_card(t("moat.moat_type"), f"**{summary['moat_type']}**\n\n{summary['moat_type_description']}", "🏰")

    # Moat score
    score = summary["moat_score"]
    emoji = _score_color(score)
    _summary_card(t("moat.moat_strength"), f"{emoji} {score:.0f}/100", "🏰")

    # 5 dimension mini-cards
    st.markdown(f"##### {t('moat.five_dimensions')}")
    dims = summary["dimensions"]
    dim_order = [t("moat.brand_power"), t("moat.cost_advantage"), t("moat.network_effect"), t("moat.switching_cost"), t("moat.scale_economy")]

    cols = st.columns(5)
    for i, dim_name in enumerate(dim_order):
        score_val = dims.get(dim_name, 0)
        color_emoji = _score_color(score_val)
        with cols[i]:
            _mini_score_card(f"{color_emoji} {dim_name}", score_val)
            _explain_button(
                metric_name=dim_name,
                metric_value=f"{score_val:.0f} 分",
                key_prefix=f"moat_{stock_id}",
                source_label=t("moat.system_estimate"),
            )

    # Evidence list
    evidence = summary.get("evidence", [])
    if evidence:
        st.markdown(f"##### {t('moat.evidence_header')}")
        evidence_text = "\n\n".join(f"• {ev}" for ev in evidence)
        _info_card(t("moat.historical_evidence"), evidence_text, "📋")
