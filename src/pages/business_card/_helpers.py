"""Business card shared helpers and constants."""
import streamlit as st


def get_health_dimension_explanation(dim_name: str, score: float) -> str:
    """Return a plain-language explanation for a health dimension score."""
    if score >= 70:
        return "表現優異，在同產業中屬於前段班"
    elif score >= 40:
        return "表現穩定，有改善空間"
    else:
        return "需要留意，可能拖累整體表現"


_RISK_BADGES = {
    "high":   "🔴 高風險",
    "medium": "🟡 中風險",
    "low":    "🟢 低風險",
}

_RISK_COLORS = {
    "high":   "#E74C3C",
    "medium": "#F39C12",
    "low":    "#27AE60",
}


def _render_risk_dimension(dim: dict, stock_name: str):
    """Render a single risk dimension as an expandable info card."""
    badge = _RISK_BADGES.get(dim["risk_level"], "⚪ 未知")
    color = _RISK_COLORS.get(dim["risk_level"], "#7F8C8D")

    st.markdown(
        f"""<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;
        border-left:4px solid {color};margin:0.5rem 0 1rem 0;">
            <div style="font-weight:600;color:#2C3E50;">
                {badge} {dim["title"]}
            </div>
            <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;
            line-height:1.7;">{dim["plain_language_description"]}</div>
        </div>""",
        unsafe_allow_html=True,
    )
