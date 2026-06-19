"""C73 Expert Analysis (專家分析) — curated expert analysis for major Taiwan stocks."""
import streamlit as st
from src.core.i18n import t
from src.pages.business_card._helpers import (
    _expert_card,
    _historian_disclaimer,
)
from src.pages._router_base import _section_title

# Curated expert analysis for 10 major Taiwan stocks
_EXPERT_ANALYSIS = {
    "2330": {
        "title": t("expert_analysis.title", name=t("expert_analysis.tsmc.stock_name"), id="2330"),
        "content": (
            f"🌍 {t('expert_analysis.tsmc.global_leader')}\n\n"
            f"📈 {t('expert_analysis.tsmc.growth')}\n\n"
            f"⚠️ {t('expert_analysis.tsmc.risk')}"
        ),
    },
    "2317": {
        "title": t("expert_analysis.title", name=t("expert_analysis.foxconn.stock_name"), id="2317"),
        "content": (
            f"🔧 {t('expert_analysis.foxconn.ems_leader')}\n\n"
            f"🤖 {t('expert_analysis.foxconn.transformation')}\n\n"
            f"⚠️ {t('expert_analysis.foxconn.risk')}"
        ),
    },
    "2454": {
        "title": t("expert_analysis.title", name=t("expert_analysis.mediatek.stock_name"), id="2454"),
        "content": (
            f"📱 {t('expert_analysis.mediatek.ic_leader')}\n\n"
            f"🚀 {t('expert_analysis.mediatek.ai_edge')}\n\n"
            f"⚠️ {t('expert_analysis.mediatek.risk')}"
        ),
    },
    "2308": {
        "title": t("expert_analysis.title", name=t("expert_analysis.delta.stock_name"), id="2308"),
        "content": (
            f"🔋 {t('expert_analysis.delta.power_expert')}\n\n"
            f"🌱 {t('expert_analysis.delta.esg')}\n\n"
            f"⚠️ {t('expert_analysis.delta.risk')}"
        ),
    },
    "2881": {
        "title": t("expert_analysis.title", name=t("expert_analysis.fubon_finance.stock_name"), id="2881"),
        "content": (
            f"🏦 {t('expert_analysis.fubon_finance.financial_giant')}\n\n"
            f"💰 {t('expert_analysis.fubon_finance.profit_stable')}\n\n"
            f"⚠️ {t('expert_analysis.fubon_finance.risk')}"
        ),
    },
    "2882": {
        "title": t("expert_analysis.title", name=t("expert_analysis.cathay_finance.stock_name"), id="2882"),
        "content": (
            f"🏦 {t('expert_analysis.cathay_finance.financial_duo')}\n\n"
            f"📊 {t('expert_analysis.cathay_finance.digital_transform')}\n\n"
            f"⚠️ {t('expert_analysis.cathay_finance.risk')}"
        ),
    },
    "1301": {
        "title": t("expert_analysis.title", name=t("expert_analysis.formosa_plastics.stock_name"), id="1301"),
        "content": (
            f"🧪 {t('expert_analysis.formosa_plastics.petro_leader')}\n\n"
            f"🔄 {t('expert_analysis.formosa_plastics.transformation')}\n\n"
            f"⚠️ {t('expert_analysis.formosa_plastics.risk')}"
        ),
    },
    "2002": {
        "title": t("expert_analysis.title", name=t("expert_analysis.china_steel.stock_name"), id="2002"),
        "content": (
            f"🏗️ {t('expert_analysis.china_steel.steel_leader')}\n\n"
            f"🌱 {t('expert_analysis.china_steel.green_transform')}\n\n"
            f"⚠️ {t('expert_analysis.china_steel.risk')}"
        ),
    },
    "2382": {
        "title": t("expert_analysis.title", name=t("expert_analysis.quanta.stock_name"), id="2382"),
        "content": (
            f"💻 {t('expert_analysis.quanta.server_leader')}\n\n"
            f"🤖 {t('expert_analysis.quanta.ai_server')}\n\n"
            f"⚠️ {t('expert_analysis.quanta.risk')}"
        ),
    },
    "3045": {
        "title": t("expert_analysis.title", name=t("expert_analysis.largan.stock_name"), id="3045"),
        "content": (
            f"📷 {t('expert_analysis.largan.optical_leader')}\n\n"
            f"🔬 {t('expert_analysis.largan.tech_lead')}\n\n"
            f"⚠️ {t('expert_analysis.largan.risk')}"
        ),
    },
}


def _render_expert_analysis(data: dict, client) -> None:
    """C73 Expert Analysis: curated expert analysis for major Taiwan stocks.

    For 10 major Taiwan stocks, shows curated expert analysis.
    For other stocks, shows a "coming soon" placeholder.
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    _section_title(t("expert_analysis.title"))

    analysis = _EXPERT_ANALYSIS.get(stock_id)
    if analysis:
        _expert_card(analysis["title"], analysis["content"], "🎓")
    else:
        _expert_card(
            f"{stock_name} ({stock_id})",
            t("expert_analysis.coming_soon"),
            "🎓",
        )

    _historian_disclaimer("expert")
    st.markdown("---")
