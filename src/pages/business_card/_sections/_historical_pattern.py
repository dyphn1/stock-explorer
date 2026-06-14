"""Business card section: C147 歷史模式 — 當類似事件發生過，結果如何。"""
import streamlit as st
from src.services.pattern_detector import detect_patterns, get_available_types
from src.pages._router_base import _info_card, _section_title


def _render_historical_pattern(data: dict, client) -> None:
    """C147 歷史模式：顯示過去類似事件的結果範圍。

    使用歷史模式偵測器搜尋過去相似事件，
    以卡片形式呈現日期、描述與結果。
    包含歷史免責聲明。
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    _section_title("📊 歷史模式")

    available_types = get_available_types(stock_id)

    if not available_types:
        _info_card(
            f"{stock_name} ({stock_id})",
            "目前無歷史模式資料。我們正在持續擴充歷史事件資料庫。",
            "📊",
        )
        st.caption("⚠️ 歷史表現不代表未來結果。本工具僅供認識公司使用。")
        return

    # 顯示每個事件類型的歷史模式
    for event_type in available_types:
        result = detect_patterns(stock_id, event_type)

        if not result.has_data:
            continue

        # 事件類型標題 + 結果摘要
        type_header = f"**{event_type}** — {result.outcome_summary}"
        st.markdown(type_header)

        # 每筆歷史事件以卡片呈現
        for match in result.matches:
            direction_emoji = {
                "positive": "📈",
                "negative": "📉",
                "mixed": "↔️",
            }.get(match.outcome_direction, "📋")

            card_content = (
                f"**{match.date}**\n\n"
                f"{match.description}\n\n"
                f"{direction_emoji} **後續結果：** {match.outcome}"
            )
            _info_card("", card_content, direction_emoji)

    # 歷史免責聲明
    st.caption("⚠️ 歷史表現不代表未來結果。本工具僅供認識公司使用，不構成投資決策的依據。")
    st.markdown("---")
