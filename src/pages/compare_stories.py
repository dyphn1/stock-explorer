"""Compare Stories page (C38) — narrative comparison with peer companies.

This page is accessible from the Business Card page via the "更多分析" expander.
It provides a detailed narrative comparison of the stock against its peers.
"""
import streamlit as st
import pandas as pd

from src.pages._router_base import _section_title, _info_card
from src.services.compare_stories import generate_compare_stories
from src.pages.url_sync import navigate_to
from src.core.i18n import t


def _render_compare_stories_page(data: dict, client) -> None:
    """C38 Compare Stories — detailed narrative comparison with peer companies.

    Shows a full-page comparison of the current stock against 2-3 peer companies
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
    _section_title(f"📖 {t('compare_stories:title')} — {stock_name} ({stock_id})")
    st.markdown(f"*{t('compare_stories:subtitle')}*")
    st.markdown("")

    # ── Find peers ──
    all_info = client.get_stock_info()

    if all_info is None or len(all_info) == 0:
        st.info(t("compare_stories:no_peer_data"))
        return

    if not industry or industry == t("compare_stories:unknown_industry"):
        st.info(t("compare_stories:unknown_industry"))
        return

    peer_mask = (
        (all_info["industry_category"] == industry)
        & (all_info["stock_id"] != stock_id)
    )

    try:
        peers_df = all_info[peer_mask]
        if not isinstance(peers_df, pd.DataFrame):
            st.info(t("compare_stories:no_peer_data"))
            return
        peers_df = peers_df.sort_values("stock_id").head(3)
    except Exception:
        st.info(t("compare_stories:no_peer_data"))
        return

    if len(peers_df) == 0:
        st.info(t("compare_stories:no_peers_found"))
        return

    # ── Peer overview ──
    st.markdown(f"### 🏢 {t('compare_stories:peer_overview')}")
    peer_cols = st.columns(len(peers_df))
    for col, (_, peer) in zip(peer_cols, peers_df.iterrows()):
        with col:
            _info_card(
                f"{peer['stock_name']} ({peer['stock_id']})",
                f"📍 {peer.get('industry_category', industry)}",
                "🏢",
            )
            if st.button(
                t("compare_stories:view_business_card", name=peer['stock_name']),
                key=f"compare_nav_{stock_id}_to_{peer['stock_id']}",
                use_container_width=True,
            ):
                navigate_to(page="名片", stock_id=str(peer['stock_id']))

    st.markdown("---")

    # ── Generate comparison narratives ──
    stories = generate_compare_stories(
        stock_id=stock_id,
        stock_name=stock_name,
        industry=industry,
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        monthly_revenue=monthly_revenue,
        financial_df=financial,
        all_stock_info=all_info,
    )

    if stories:
        st.markdown(f"### 📊 {t('compare_stories:analysis')}")
        for story in stories:
            peer_name = story["peer_name"]
            peer_id = story["peer_id"]
            lines = story["narrative_lines"]

            # Peer header with navigation
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**vs. {peer_name}** `{peer_id}`")
            with col2:
                if st.button(
                    t("compare_stories:view_peer", name=peer_name),
                    key=f"story_{stock_id}_peer_{peer_id}",
                    use_container_width=True,
                ):
                    navigate_to(page="名片", stock_id=peer_id)

            # Narrative lines with icons
            for line in lines:
                icon = "📊"
                if line.startswith("📏"):
                    icon = "📏"
                elif line.startswith("💰"):
                    icon = "💰"
                elif line.startswith("📈"):
                    icon = "📈"
                elif line.startswith("🏷️"):
                    icon = "🏷️"
                elif line.startswith("💵"):
                    icon = "💵"

                # Strip leading emoji for cleaner display
                clean_line = line
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[0] in ("📏", "💰", "📈", "🏷️", "💵", "📊"):
                    clean_line = parts[1]

                _info_card("", clean_line, icon)

            st.markdown("---")
    else:
        st.info(t("compare_stories:no_comparison_data"))
