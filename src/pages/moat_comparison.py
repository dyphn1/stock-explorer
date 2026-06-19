"""Moat Comparison page (C126) — side-by-side moat comparison with peer companies.

This page is accessible from the Business Card page via the "更多分析" expander.
It provides a detailed moat comparison of the stock against its peers.
"""
import streamlit as st
import pandas as pd

from src.pages._router_base import _section_title, _info_card, _summary_card, _mini_score_card
from src.pages.url_sync import navigate_to
from src.services.moat_analyzer import get_moat_summary
from src.pages._router_base import get_stock_data
from src.core.i18n import t


def _render_moat_comparison_page(data: dict, client) -> None:
    """C126 Moat Comparison — side-by-side moat comparison with peer companies.

    Shows a full-page moat comparison of the current stock against 2-3 peer companies
    in the same industry, with navigation links to each peer's business card.
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]

    # Page header
    _section_title(f"🏰 {t('moat_comparison:title')} — {stock_name} ({stock_id})")
    st.markdown(f"*{t('moat_comparison:subtitle')}*")
    st.markdown("")

    # ── Find peers ──
    all_info = client.get_stock_info()

    if all_info is None or len(all_info) == 0:
        st.info(t("moat_comparison:no_peer_data"))
        return

    if not industry or industry == "未知":
        st.info(t("moat_comparison:unknown_industry"))
        return

    peer_mask = (
        (all_info["industry_category"] == industry)
        & (all_info["stock_id"] != stock_id)
    )

    try:
        peers_df = all_info[peer_mask]
        if not isinstance(peers_df, pd.DataFrame):
            st.info(t("moat_comparison:no_peer_data"))
            return
        peers_df = peers_df.sort_values("stock_id").head(3)
    except Exception:
        st.info(t("moat_comparison:no_peer_data"))
        return

    if len(peers_df) == 0:
        st.info(t("moat_comparison:no_peers_found"))
        return

    # ── Peer overview ──
    _section_title(t("moat_comparison:peer_overview"))
    peer_cols = st.columns(len(peers_df))
    for col, (_, peer) in zip(peer_cols, peers_df.iterrows()):
        with col:
            _info_card(
                f"{peer['stock_name']} ({peer['stock_id']})",
                f"📍 {peer.get('industry_category', industry)}",
                "🏢",
            )
            if st.button(
                t("moat_comparison:view_business_card", name=peer['stock_name']),
                key=f"moat_compare_nav_{stock_id}_to_{peer['stock_id']}",
                use_container_width=True,
            ):
                navigate_to(page="名片", stock_id=str(peer['stock_id']))

    st.markdown("---")

    # ── Get moat summary for primary stock ──
    primary_moat = get_moat_summary(
        stock_id=stock_id,
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )

    # ── Get moat summaries for peers ──
    peer_moats = []
    for _, peer in peers_df.iterrows():
        peer_id = str(peer["stock_id"])
        peer_data = get_stock_data(client, peer_id)
        if peer_data is None:
            continue
        peer_moat = get_moat_summary(
            stock_id=peer_id,
            extra_metrics=peer_data["extra_metrics"],
            latest_per_pbr=peer_data["latest_per_pbr"],
            financial_df=peer_data["financial"],
            monthly_revenue=peer_data["monthly_revenue"],
        )
        peer_moats.append({
            "stock_id": peer_id,
            "stock_name": peer["stock_name"],
            "moat": peer_moat,
        })

    # ── Moat score comparison ──
    _section_title(t("moat_comparison:moat_score_comparison"))

    all_names = [stock_name] + [p["stock_name"] for p in peer_moats]
    all_scores = [primary_moat.get("moat_score", 0)] + [p["moat"].get("moat_score", 0) for p in peer_moats]

    score_cols = st.columns(len(all_names))
    for col, name, score in zip(score_cols, all_names, all_scores):
        with col:
            emoji = "🟢" if score >= 70 else ("🟡" if score >= 40 else "🔴")
            _summary_card(name, f"{emoji} {score:.0f}/100", "🏰")

    st.markdown("---")

    # ── 5-dimension comparison ──
    _section_title(t("moat_comparison:five_dimensions"))
    dim_order = [
        t("moat_comparison:dim_brand"),
        t("moat_comparison:dim_cost_advantage"),
        t("moat_comparison:dim_network_effect"),
        t("moat_comparison:dim_switching_cost"),
        t("moat_comparison:dim_economies_of_scale"),
    ]

    # Collect all dimension scores
    all_dims = [primary_moat.get("dimensions", {})] + [p["moat"].get("dimensions", {}) for p in peer_moats]

    for dim_name in dim_order:
        st.markdown(f"**{dim_name}**")
        dim_cols = st.columns(len(all_names))
        for col, name, dims in zip(dim_cols, all_names, all_dims):
            with col:
                score_val = dims.get(dim_name, 0)
                _mini_score_card(f"{name}", score_val)
        st.markdown("")

    st.markdown("---")

    # ── Moat type comparison ──
    _section_title(t("moat_comparison:moat_type"))
    type_cols = st.columns(len(all_names))
    for col, name, moat in zip(type_cols, all_names, [primary_moat] + [p["moat"] for p in peer_moats]):
        with col:
            moat_type = moat.get("moat_type", t("moat_comparison:unknown_type"))
            moat_desc = moat.get("moat_type_description", "")
            _info_card(name, f"**{moat_type}**\n\n{moat_desc}", "🏷️")

    st.markdown("---")

    # ── Evidence comparison ──
    _section_title(t("moat_comparison:evidence"))
    evidence_cols = st.columns(len(all_names))
    for col, name, moat in zip(evidence_cols, all_names, [primary_moat] + [p["moat"] for p in peer_moats]):
        with col:
            evidence = moat.get("evidence", [])
            if evidence:
                evidence_text = "\n\n".join(f"• {ev}" for ev in evidence)
                _info_card(name, evidence_text, "📋")
            else:
                _info_card(name, t("moat_comparison:no_evidence"), "📋")
