"""C73 Expert Analysis (專家分析) — curated expert analysis for major Taiwan stocks."""
import streamlit as st
import yaml
from src.core.i18n import t
from src.pages.business_card._helpers import (
    _expert_card,
    _historian_disclaimer,
)
from src.pages._router_base import _section_title

# Load expert analysis data from YAML
with open('../../data/yaml/expert_analysis.yaml', 'r', encoding='utf-8') as f:
    EXPERT_ANALYSIS_DATA = yaml.safe_load(f)


def _render_expert_analysis(data: dict, client) -> None:
    """C73 Expert Analysis: curated expert analysis for major Taiwan stocks.

    For 10 major Taiwan stocks, shows curated expert analysis.
    For other stocks, shows a "coming soon" placeholder.
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    _section_title(t("expert_analysis.title"))

    analysis = EXPERT_ANALYSIS_DATA.get(stock_id)
    if analysis:
        title = t(analysis["title"])
        content = t(analysis["content"])
        _expert_card(title, content, "🎓")
    else:
        _expert_card(
            f"{stock_name} ({stock_id})",
            t("expert_analysis.coming_soon"),
            "🎓",
        )

    _historian_disclaimer("expert")
    st.markdown("---")