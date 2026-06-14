"""Business card section: Moat Analysis (C46 + C124)."""
import streamlit as st
from src.services.moat_analyzer import get_moat_summary
from src.pages._router_base import _info_card, _summary_card, _mini_score_card, _explain_button


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
        _info_card("護城河分析", f"目前無法評估 {stock_name} 的護城河，需要更多財務數據", "🏰")
        return

    # Moat type badge
    _info_card("護城河類型", f"**{summary['moat_type']}**\n\n{summary['moat_type_description']}", "🏰")

    # Moat score
    score = summary["moat_score"]
    emoji = _score_color(score)
    _summary_card("護城河強度", f"{emoji} {score:.0f}/100", "🏰")

    # 5 dimension mini-cards
    st.markdown("##### 五維度評分")
    dims = summary["dimensions"]
    dim_order = ["品牌力", "成本優勢", "網路效應", "轉換成本", "規模經濟"]

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
                source_label="📊 系統估算",
            )

    # Evidence list
    evidence = summary.get("evidence", [])
    if evidence:
        st.markdown("##### 📋 證據")
        evidence_text = "\n\n".join(f"• {ev}" for ev in evidence)
        _info_card("歷史證據", evidence_text, "📋")
