"""Business card shared helpers and constants."""
import streamlit as st


def _get_health_metric_values(extra_metrics: dict, latest_per_pbr: dict | None) -> dict:
    """Return dict mapping dimension names to list of metric value strings."""
    metrics = {}

    # 獲利能力: ROE, 毛利率, 淨利率
    profit = []
    if extra_metrics.get("roe") is not None:
        profit.append(f"ROE {extra_metrics['roe']:.1f}%")
    if extra_metrics.get("gross_margin") is not None:
        profit.append(f"毛利率 {extra_metrics['gross_margin']:.1f}%")
    if extra_metrics.get("net_margin") is not None:
        profit.append(f"淨利率 {extra_metrics['net_margin']:.1f}%")
    if profit:
        metrics["獲利能力"] = profit

    # 成長性: 營收年增率
    growth = []
    if extra_metrics.get("revenue_yoy") is not None:
        growth.append(f"營收年增率 {extra_metrics['revenue_yoy']:.1f}%")
    if growth:
        metrics["成長性"] = growth

    # 財務健康: 負債比, 流動比
    health = []
    if extra_metrics.get("debt_ratio") is not None:
        health.append(f"負債比 {extra_metrics['debt_ratio']:.1f}%")
    if extra_metrics.get("current_ratio") is not None:
        health.append(f"流動比 {extra_metrics['current_ratio']:.1f}")
    if health:
        metrics["財務健康"] = health

    # 股利品質: 殖利率, 連續配息
    div = []
    if latest_per_pbr and latest_per_pbr.get("dividend_yield") is not None:
        div.append(f"殖利率 {latest_per_pbr['dividend_yield']:.2f}%")
    if extra_metrics.get("dividend_years") is not None:
        div.append(f"連續配息 {extra_metrics['dividend_years']:.0f} 年")
    if div:
        metrics["股利品質"] = div

    # 估值合理性: PER, PBR
    val = []
    if latest_per_pbr and latest_per_pbr.get("PER") is not None:
        val.append(f"本益比 {latest_per_pbr['PER']:.1f}")
    if latest_per_pbr and latest_per_pbr.get("PBR") is not None:
        val.append(f"淨值比 {latest_per_pbr['PBR']:.2f}")
    if val:
        metrics["估值合理性"] = val

    return metrics


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


# ── D-039: Standardized Section Header Pattern ──────────────────

def _section_header(icon: str, title: str, collapsed: bool = False):
    """Render a standardized section header.

    If collapsed=False: renders a markdown header (### icon title).
    If collapsed=True: renders a st.expander with the header as label.
    Returns the expander context manager if collapsed, else None.
    """
    if collapsed:
        return st.expander(f"{icon} {title}", expanded=False)
    else:
        st.markdown(f"### {icon} {title}")


def _section_title(icon: str, title: str):
    """Shortcut for _section_header with collapsed=False."""
    st.markdown(f"### {icon} {title}")


# ── D-040: Standardized Disclaimer Component ────────────────────

_DISCLAIMER_TEXTS = {
    "expert": "⚠️ 專家分析由 AI 輔助整理，僅供參考，不構成投資建議。",
    "scenario": "⚠️ 歷史情境為假設性試算，僅供教育用途，不構成投資建議。過去績效不代表未來表現。",
    "general": "⚠️ 本工具僅供認識公司使用，所有數據來自公開資訊觀測站與 FinMind。不構成任何投資建議。投資有風險，請自行評估。",
}


def _historian_disclaimer(disclaimer_type: str = "general"):
    """Render a standardized disclaimer caption.

    Types:
        'expert'   — for expert analysis sections
        'scenario' — for historical scenario sections
        'general'  — default general disclaimer
    """
    text = _DISCLAIMER_TEXTS.get(disclaimer_type, _DISCLAIMER_TEXTS["general"])
    st.caption(text)


# ── D-041: Card Components for Sprint 5 ─────────────────────────

def _study_card(title: str, content: str, icon: str = "📚"):
    """Render a study log card with consistent styling."""
    st.markdown(
        f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
        border-left:4px solid #3498DB;margin:0.5rem 0 1rem 0;">
            <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
            <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;
            line-height:1.7;">{content}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def _expert_card(title: str, content: str, icon: str = "🎓"):
    """Render an expert analysis card with consistent styling."""
    st.markdown(
        f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
        border-left:4px solid #9B59B6;margin:0.5rem 0 1rem 0;">
            <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
            <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;
            line-height:1.7;">{content}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def _scenario_card(title: str, content: str, icon: str = "🔍"):
    """Render a historical scenario card with consistent styling."""
    st.markdown(
        f"""<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;
        border-left:4px solid #E67E22;margin:0.5rem 0 1rem 0;">
            <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
            <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;
            line-height:1.7;">{content}</div>
        </div>""",
        unsafe_allow_html=True,
    )
