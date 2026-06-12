"""
Investment Memo Template — C83
A structured reflection tool where users write their own investment thesis.
Standalone page (no stock_id required).
"""

from __future__ import annotations

import streamlit as st
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card
from src.pages.business_card._helpers import _section_title, _historian_disclaimer
from src.services.investment_memo_service import (
    get_stock_suggestions,
    validate_memo_input,
    format_memo_summary,
)


def _render_investment_memo(client: FinMindClient):
    """Investment Memo main page — write your own investment thesis."""
    st.markdown("## 📝 投資備忘錄")
    st.markdown("寫下你對這家公司的看法，建立自己的分析框架")
    st.markdown("---\n")

    # ── Tip card ──────────────────────────────────────────
    _info_card(
        "怎麼寫？",
        "投資備忘錄是寫給自己看的筆記。不需要專業術語，用你自己的話記錄想法就好。",
        icon="💡",
    )

    # ── Stock selector ────────────────────────────────────
    _section_title("🔍", "選擇股票")

    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        stock_query = st.text_input(
            "輸入股票代號或名稱",
            placeholder="例如：2330 或 台積電",
            key="memo_stock_query",
            label_visibility="collapsed",
        )

    selected_stock_id = None
    selected_stock_name = None

    if stock_query and stock_query.strip():
        with st.spinner("搜尋中…"):
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
                        "選擇",
                        list(options.keys()),
                        key="memo_stock_select",
                        label_visibility="collapsed",
                    )
                if display:
                    selected_stock_id = options[display]
                    selected_stock_name = display.split(" ", 1)[1] if " " in display else display
        else:
            st.warning("找不到符合的股票，請確認代號或名稱是否正確。")

    if selected_stock_id:
        st.success(f"已選擇：**{selected_stock_name}** `{selected_stock_id}`")
        st.markdown("---\n")

        # ── Memo form ──────────────────────────────────────
        _section_title("✏️", "寫下你的分析")

        # Initialize session state for saved memos
        if "investment_memos" not in st.session_state:
            st.session_state["investment_memos"] = {}

        saved_memos = st.session_state["investment_memos"]
        existing_memo = saved_memos.get(selected_stock_id, {})

        with st.form("investment_memo_form", clear_on_submit=False):
            one_liner = st.text_input(
                "一句話定位",
                value=existing_memo.get("one_liner", ""),
                placeholder="用一句話描述這家公司是做什麼的",
                key="memo_oneliner",
            )

            reasons = st.text_area(
                "投資理由",
                value=existing_memo.get("reasons", ""),
                placeholder="為什麼想投資這家公司？列出 2-3 個理由",
                key="memo_reasons",
                height=100,
            )

            concerns = st.text_area(
                "擔心的事",
                value=existing_memo.get("concerns", ""),
                placeholder="有什麼讓你猶豫的地方？",
                key="memo_concerns",
                height=80,
            )

            key_metrics = st.text_input(
                "關鍵指標",
                value=existing_memo.get("key_metrics", ""),
                placeholder="你會追蹤哪些指標來驗證你的判斷？",
                key="memo_metrics",
            )

            st.markdown("**目標價區間**")
            col_low, col_high = st.columns(2)
            with col_low:
                target_low = st.number_input(
                    "下限",
                    value=float(existing_memo.get("target_low", 0)) if existing_memo.get("target_low") else None,
                    step=1.0,
                    format="%.0f",
                    key="memo_target_low",
                    label_visibility="collapsed",
                )
            with col_high:
                target_high = st.number_input(
                    "上限",
                    value=float(existing_memo.get("target_high", 0)) if existing_memo.get("target_high") else None,
                    step=1.0,
                    format="%.0f",
                    key="memo_target_high",
                    label_visibility="collapsed",
                )

            confidence = st.select_slider(
                "信心水平",
                options=[1, 2, 3, 4, 5],
                value=existing_memo.get("confidence", 3),
                key="memo_confidence",
            )

            notes = st.text_area(
                "備註",
                value=existing_memo.get("notes", ""),
                placeholder="其他想法或備注",
                key="memo_notes",
                height=60,
            )

            submitted = st.form_submit_button("💾 儲存備忘錄", use_container_width=True)

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
                st.success("✅ 備忘錄已儲存！")
            else:
                st.error(f"❌ {error_msg}")

        # ── Display saved memos ────────────────────────────
        st.markdown("---\n")
        _section_title("📋", "已儲存的備忘錄")

        if saved_memos:
            for sid, memo in saved_memos.items():
                formatted = format_memo_summary(memo)
                content = (
                    f"**{memo.get('stock_name', sid)}** `{sid}`\n\n"
                    f"📌 {formatted['one_liner']}\n\n"
                    f"💭 理由：{formatted['reasons']}\n\n"
                    f"⚠️ 擔心：{formatted['concerns']}\n\n"
                    f"📊 關鍵指標：{formatted['key_metrics']}\n\n"
                    f"🎯 目標價：{formatted['price_range']} ｜ "
                    f"信心：{formatted['confidence_label']}"
                )
                if formatted["notes"]:
                    content += f"\n\n📝 備註：{formatted['notes']}"

                _summary_card(
                    f"{memo.get('stock_name', sid)} 的投資備忘錄",
                    content,
                    icon="📝",
                )

                # Button to navigate to this stock's business card
                if st.button(
                    f"查看 {memo.get('stock_name', sid)} 名片",
                    key=f"memo_goto_{sid}",
                    use_container_width=True,
                ):
                    navigate_to(page="名片", stock_id=sid)
        else:
            _info_card(
                "還沒有儲存的備忘錄",
                "填寫上方表單並點擊「儲存備忘錄」，你的分析記錄就會顯示在這裡。",
                icon="📝",
            )

    st.markdown("---\n")
    _historian_disclaimer("general")
