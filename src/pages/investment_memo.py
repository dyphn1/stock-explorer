"""
Investment Memo Template — C83
A structured reflection tool where users write their own investment thesis.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card, _section_title
from src.pages.business_card._helpers import _historian_disclaimer
from src.core.i18n import t
from src.services.investment_memo_service import (
    get_stock_suggestions,
    validate_memo_input,
    format_memo_summary,
)


def _render_investment_memo(client: FinMindClient):
    """Investment Memo main page — write your own investment thesis."""
    st.markdown(f"## 📝 {t('investment_memo.title')}")
    st.markdown(t('investment_memo.subtitle'))
    st.markdown("---\n")

    # ── Tip card ──────────────────────────────────────────
    _info_card(
        t('investment_memo.tip_title'),
        t('investment_memo.tip_content'),
        icon="💡",
    )

    # ── Stock selector ────────────────────────────────────
    _section_title(f"🔍 {t('investment_memo.select_stock')}")

    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        stock_query = st.text_input(
            t('investment_memo.input_label'),
            placeholder=t('investment_memo.input_placeholder'),
            key="memo_stock_query",
            label_visibility="collapsed",
        )

    selected_stock_id = None
    selected_stock_name = None

    if stock_query and stock_query.strip():
        with st.spinner(t('investment_memo.searching')):
            matches = get_stock_suggestions(client, stock_query)

        if matches is not None and len(matches) > 0:
            if len(matches) == 1:
                selected_stock_id = matches.iloc[0]["stock_id"]
                selected_stock_name = matches.iloc[0]["stock_name"]
            else:
                options = {
                    f"{row['stock_id']} {row['stock_name']}": row["stock_id"]
                    for _, row in matches.iterrows()
                }
                with col_btn:
                    display = st.selectbox(
                        t('investment_memo.select'),
                        list(options.keys()),
                        key="memo_stock_select",
                        label_visibility="collapsed",
                    )
                if display:
                    selected_stock_id = options[display]
                    selected_stock_name = display.split(" ", 1)[1] if " " in display else display
        else:
            st.warning(t('investment_memo.no_match'))

    if selected_stock_id:
        st.success(t('investment_memo.selected', name=selected_stock_name, id=selected_stock_id))
        st.markdown("---\n")

        # ── Memo form ──────────────────────────────────────
        _section_title(f"✏️ {t('investment_memo.write_analysis')}")

        # Initialize session state for saved memos
        if "investment_memos" not in st.session_state:
            st.session_state["investment_memos"] = {}

        saved_memos = st.session_state["investment_memos"]
        existing_memo = saved_memos.get(selected_stock_id, {})

        with st.form("investment_memo_form", clear_on_submit=False):
            one_liner = st.text_input(
                t('investment_memo.one_liner'),
                value=existing_memo.get("one_liner", ""),
                placeholder=t('investment_memo.one_liner_placeholder'),
                key="memo_oneliner",
            )

            reasons = st.text_area(
                t('investment_memo.reasons'),
                value=existing_memo.get("reasons", ""),
                placeholder=t('investment_memo.reasons_placeholder'),
                key="memo_reasons",
                height=100,
            )

            concerns = st.text_area(
                t('investment_memo.concerns'),
                value=existing_memo.get("concerns", ""),
                placeholder=t('investment_memo.concerns_placeholder'),
                key="memo_concerns",
                height=80,
            )

            key_metrics = st.text_input(
                t('investment_memo.key_metrics'),
                value=existing_memo.get("key_metrics", ""),
                placeholder=t('investment_memo.key_metrics_placeholder'),
                key="memo_metrics",
            )

            st.markdown(f"**{t('investment_memo.target_price')}**")
            col_low, col_high = st.columns(2)
            with col_low:
                target_low = st.number_input(
                    t('investment_memo.target_low'),
                    value=float(existing_memo.get("target_low", 0)) if existing_memo.get("target_low") else None,
                    step=1.0,
                    format="%.0f",
                    key="memo_target_low",
                    label_visibility="collapsed",
                )
            with col_high:
                target_high = st.number_input(
                    t('investment_memo.target_high'),
                    value=float(existing_memo.get("target_high", 0)) if existing_memo.get("target_high") else None,
                    step=1.0,
                    format="%.0f",
                    key="memo_target_high",
                    label_visibility="collapsed",
                )

            confidence = st.select_slider(
                t('investment_memo.confidence'),
                options=[1, 2, 3, 4, 5],
                value=existing_memo.get("confidence", 3),
                key="memo_confidence",
            )

            notes = st.text_area(
                t('investment_memo.notes'),
                value=existing_memo.get("notes", ""),
                placeholder=t('investment_memo.notes_placeholder'),
                key="memo_notes",
                height=60,
            )

            submitted = st.form_submit_button(t('investment_memo.save_button'), use_container_width=True)

        if submitted:
            memo_data = {
                "stock_id": selected_stock_id,
                "stock_name": selected_stock_name,
                "one_liner": one_liner,
                "reasons": reasons,
                "concerns": concerns,
                "key_metrics": key_metrics,
                "target_low": target_low,
                "target_high": target_high,
                "confidence": confidence,
                "notes": notes,
            }
            is_valid, error_msg = validate_memo_input(memo_data)
            if is_valid:
                saved_memos[selected_stock_id] = memo_data
                st.session_state["investment_memos"] = saved_memos
                st.success(t('investment_memo.save_success'))
            else:
                st.error(f"❌ {error_msg}")

        # ── Display saved memos ────────────────────────────
        st.markdown("---\n")
        _section_title(f"📋 {t('investment_memo.saved_memos')}")

        if saved_memos:
            for sid, memo in saved_memos.items():
                formatted = format_memo_summary(memo)
                content = (
                    f"**{memo.get('stock_name', sid)}** `{sid}`\n\n"
                    f"{t('investment_memo.one_liner')}: {formatted['one_liner']}\n\n"
                    f"{t('investment_memo.reasons')}: {formatted['reasons']}\n\n"
                    f"{t('investment_memo.concerns')}: {formatted['concerns']}\n\n"
                    f"{t('investment_memo.key_metrics')}: {formatted['key_metrics']}\n\n"
                    f"{t('investment_memo.target_price')}: {formatted['price_range']} ｜ "
                    f"{t('investment_memo.confidence')}: {formatted['confidence_label']}"
                )
                if formatted["notes"]:
                    content += f"\n\n{t('investment_memo.notes')}: {formatted['notes']}"

                _summary_card(
                    t('investment_memo.memo_for_stock', name=memo.get('stock_name', sid)),
                    content,
                    icon="📝",
                )

                # Button to navigate to this stock's business card
                if st.button(
                    t('investment_memo.view_business_card', name=memo.get('stock_name', sid)),
                    key=f"memo_goto_{sid}",
                    use_container_width=True,
                ):
                    navigate_to(page=t('investment_memo.business_card_page'), stock_id=sid)
        else:
            _info_card(
                t('investment_memo.no_memos_title'),
                t('investment_memo.no_memos_content'),
                icon="📝",
            )

    st.markdown("---\n")
    _historian_disclaimer("general")
