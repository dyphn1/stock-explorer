"""Business card section: C147 歷史模式 — 當類似事件發生過，結果如何。"""
import streamlit as st
from src.services.pattern_detector import detect_patterns, get_available_types
from src.pages._router_base import _info_card, _section_title
from src.core.i18n import t


def _render_historical_pattern(data: dict, client) -> None:
    """C147 歷史模式：顯示過去類似事件的結果範圍。

    使用歷史模式偵測器搜尋過去相似事件，
    以卡片形式呈現日期、描述與結果。
    包含歷史免責聲明。
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    _section_title(t("historical_pattern:title"))

    available_types = get_available_types(stock_id)

    if not available_types:
        _info_card(
            f"{stock_name} ({stock_id})",
            t("historical_pattern:no_data"),
            "📊",
        )
        st.caption(t("historical_pattern:disclaimer"))
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
                f"{direction_emoji} **{t('historical_pattern:outcome_label')}** {match.outcome}"
            )
            _info_card("", card_content, direction_emoji)

    # 歷史免責聲明
    st.caption(t("historical_pattern:disclaimer"))
    st.markdown("---")
