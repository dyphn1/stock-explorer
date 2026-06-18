"""Business card section: story/delta sections (deltas, compare stories, read next)."""
import streamlit as st
import pandas as pd
from src.services.delta_engine import compute_recent_deltas
from src.services.company_facts import get_company_facts
from src.pages._router_base import _info_card, _section_title, _explain_button, _so_what_box, _confidence_badge
from src.pages.url_sync import navigate_to
from src.services.compare_stories import generate_compare_stories
from src.core.i18n import t


def _render_deltas(data: dict, client) -> None:
    """C39 Recent Deltas section."""
    extra_metrics = data["extra_metrics"]
    monthly_revenue = data["monthly_revenue"]
    latest_per_pbr = data["latest_per_pbr"]
    stock_id = data["stock_id"]

    # 🔄 最近有什麼變化 (C39: Recent Deltas)
    deltas = compute_recent_deltas(
        extra_metrics=extra_metrics,
        monthly_revenue=monthly_revenue,
        daily_price=data.get("daily_price"),
        latest_per_pbr=latest_per_pbr,
    )
    if deltas:
        delta_lines = []
        for d in deltas:
            emoji = "📈" if d["direction"] == "up" else "📉"
            sign = "+" if d["change_pct"] >= 0 else ""
            color = "#27AE60" if d["direction"] == "up" else "#E74C3C"
            # C143: implication sentence replaces explanation on card
            implication_text = d.get("implication", "")
            delta_lines.append(
                f"{emoji} <span style=\\\"color:{color}\\\">**{d['metric_name']}**：{d['current_value']}（前期：{d['previous_value']}，{sign}{d['change_pct']:.1f}%）</span><br>\\n"
                f"　→ {implication_text}"
            )
        delta_text = "\\n\\n".join(delta_lines)
        _info_card(t("story.recent_changes"), delta_text, "🔄")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t("story.confidence_note")}")

        # C139: 💡 explain buttons for each delta metric (show original explanation in popover)
        for d in deltas:
            sign = "+" if d["change_pct"] >= 0 else ""
            _explain_button(
                metric_name=d["metric_name"],
                metric_value=d["current_value"],
                delta=f"{sign}{d['change_pct']:.1f}%",
                key_prefix=f"delta_{stock_id}",
                context={"direction": d["direction"]},
                source_label="📊 FinMind",
            )

        # C149: So What? implication box — synthesize all deltas
        _so_what_box(deltas)
    else:
        _info_card(t("story.recent_changes"), t("story.no_significant_changes"), "🔄")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t("story.confidence_note")}")


def _render_compare_stories(data: dict, client, all_info=None) -> None:
    """C38 Compare Stories: narrative comparison with peer companies.

    Shows a collapsible section with plain-language narrative comparing
    the current stock against 2-3 peer companies in the same industry.
    Uses the analogy engine for generating comparison text.
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]

    # ── Find peers ──
    if all_info is None or len(all_info) == 0:
        return
    if not industry or industry == t("story.unknown_industry"):
        return

    peer_mask = (
        (all_info["industry_category"] == industry)
        & (all_info["stock_id"] != stock_id)
    )
    try:
        peers_df = all_info[peer_mask]
        if not isinstance(peers_df, pd.DataFrame):
            return
        peers_df = peers_df.sort_values("stock_id").head(3)
    except Exception:
        return

    if len(peers_df) == 0:
        return

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

    if not stories:
        return

    # ── Render in collapsible section (D-032 progressive disclosure) ──
    with st.expander(t("story.peer_comparison"), expanded=False):
        st.markdown(t("story.peer_comparison_subtitle", name=stock_name))
        st.markdown("")

        for story in stories:
            peer_name = story["peer_name"]
            peer_id = story["peer_id"]
            lines = story["narrative_lines"]

            # Peer header with navigation button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**vs. {peer_name}** `{peer_id}`")
            with col2:
                if st.button(
                    t("story.view_peer", name=peer_name),
                    key=f"compare_story_{stock_id}_peer_{peer_id}",
                    use_container_width=True,
                ):
                    navigate_to(page="名片", stock_id=peer_id)

            # Narrative lines — use _info_card for each comparison point
            for line in lines:
                # Determine icon based on content
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

                # Strip leading emoji from line for cleaner display
                clean_line = line
                # Remove leading emoji + space if present
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[0] in ("📏", "💰", "📈", "🏷️", "💵", "📊"):
                    clean_line = parts[1]

                _info_card("", clean_line, icon)

            st.markdown("---")


def _render_read_next(data: dict, client, all_info=None) -> None:
    """C41 Read Next: peer stocks + curated fun facts."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    # 📖 推薦閱讀 (C41: Read Next Recommendations)
    _section_title(t("story.read_next"))

    # --- Peer stocks from same industry ---
    _peers = pd.DataFrame()
    if all_info is not None and len(all_info) > 0 and industry and industry != t("story.unknown_industry"):
        _peers = all_info[
            (all_info["industry_category"] == industry) &
            (all_info["stock_id"] != stock_id)
        ].head(5)

    if len(_peers) > 0:
        st.markdown(t("story.peer_recommendations"))
        for _, _peer in _peers.iterrows():
            _peer_id = str(_peer["stock_id"])
            _peer_name = _peer["stock_name"]
            _peer_industry = _peer.get("industry_category", industry)
            _key = f"read_next_{stock_id}_peer_{_peer_id}"

            _info_card(
                f"{_peer_name} ({_peer_id})",
                t("story.peer_info", industry=_peer_industry),
                "📖",
            )
            if st.button(
                t("story.view_peer_card", name=_peer_name),
                key=_key,
                use_container_width=True,
            ):
                navigate_to(page="名片", stock_id=_peer_id)
            st.markdown("")
    else:
        _info_card("推薦閱讀", t("story.no_recommendations"), "📖")

    # --- Curated fun facts from company_facts.yaml ---
    _curated_facts = get_company_facts(stock_id)
    if _curated_facts:
        st.markdown(t("story.you_might_wonder"))
        # Show up to 2 remaining facts (skip the one already shown in 你知道嗎？ section)
        _fact_idx_key = f"_fact_idx_{stock_id}"
        _shown_idx = st.session_state.get(_fact_idx_key, 0) % len(_curated_facts) if _curated_facts else 0
        _remaining_facts = [
            f for i, f in enumerate(_curated_facts)
            if i != _shown_idx
        ]
        for _fact in _remaining_facts[:2]:
            _info_card(t("story.did_you_know"), _fact, "🤔")

    # ── C28: Story Timeline nav button ──────────────────────
    st.markdown(t("story.more_analysis"))
    if st.button(
        t("story.full_timeline"),
        key=f"nav_story_timeline_{stock_id}",
        use_container_width=True,
    ):
        navigate_to(page="完整故事時間軸", stock_id=stock_id)
    st.caption(t("story.timeline_caption"))
