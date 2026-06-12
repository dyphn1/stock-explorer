"""Business card section: story/delta sections (deltas, compare stories, read next)."""
import streamlit as st
import pandas as pd
from src.services.delta_engine import compute_recent_deltas
from src.services.company_facts import get_company_facts
from src.pages._router_base import _info_card, _section_title
from src.pages.url_sync import navigate_to
from src.services.compare_stories import generate_compare_stories


def _render_deltas(data: dict, client) -> None:
    """C39 Recent Deltas section."""
    extra_metrics = data["extra_metrics"]
    monthly_revenue = data["monthly_revenue"]
    latest_per_pbr = data["latest_per_pbr"]

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
            delta_lines.append(
                f"{emoji} <span style=\\\"color:{color}\\\">**{d['metric_name']}**：{d['current_value']}（前期：{d['previous_value']}，{sign}{d['change_pct']:.1f}%）</span><br>\\n"
                f"　→ {d['explanation']}"
            )
        delta_text = "\\n\\n".join(delta_lines)
        _info_card("最近有什麼變化", delta_text, "🔄")
    else:
        _info_card("最近有什麼變化", "近期無顯著變化，所有指標波動均在 10% 以內", "🔄")


def _render_compare_stories(data: dict, client) -> None:
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
    all_info = client.get_stock_info()
    if all_info is None or len(all_info) == 0:
        return
    if not industry or industry == "未知":
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
    with st.expander("📖 同業比較故事 — 跟同業比起來怎麼樣？", expanded=False):
        st.markdown(f"*{stock_name} 與同產業同業的敘事比較*")
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
                    f"查看 {peer_name}",
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


def _render_read_next(data: dict, client) -> None:
    """C41 Read Next: peer stocks + curated fun facts."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    # 📖 推薦閱讀 (C41: Read Next Recommendations)
    _section_title(f"📖 推薦閱讀")

    # --- Peer stocks from same industry ---
    _all_info = client.get_stock_info()
    _current_industry = industry
    _peers = pd.DataFrame()
    if len(_all_info) > 0 and _current_industry and _current_industry != "未知":
        _peers = _all_info[
            (_all_info["industry_category"] == _current_industry) &
            (_all_info["stock_id"] != stock_id)
        ].head(5)

    if len(_peers) > 0:
        st.markdown("**同產業個股推薦**")
        for _, _peer in _peers.iterrows():
            _peer_id = str(_peer["stock_id"])
            _peer_name = _peer["stock_name"]
            _peer_industry = _peer.get("industry_category", _current_industry)
            _key = f"read_next_{stock_id}_peer_{_peer_id}"

            _info_card(
                f"{_peer_name} ({_peer_id})",
                f"📍 {_peer_industry}\\n🔗 同產業同業，一起認識這家公司",
                "📖",
            )
            if st.button(
                f"查看 {_peer_name} 名片",
                key=_key,
                use_container_width=True,
            ):
                navigate_to(page="名片", stock_id=_peer_id)
            st.markdown("")
    else:
        _info_card("推薦閱讀", "目前沒有找到相關的同產業個股推薦", "📖")

    # --- Curated fun facts from company_facts.yaml ---
    _curated_facts = get_company_facts(stock_id)
    if _curated_facts:
        st.markdown("**你可能會好奇**")
        # Show up to 2 remaining facts (skip the one already shown in 你知道嗎？ section)
        _fact_idx_key = f"_fact_idx_{stock_id}"
        _shown_idx = st.session_state.get(_fact_idx_key, 0) % len(_curated_facts) if _curated_facts else 0
        _remaining_facts = [
            f for i, f in enumerate(_curated_facts)
            if i != _shown_idx
        ]
        for _fact in _remaining_facts[:2]:
            _info_card("💡 你知道嗎？", _fact, "🤔")
