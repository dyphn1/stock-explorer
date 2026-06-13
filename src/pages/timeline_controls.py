"""
時間軸控制元件 — M3
提供時間範圍選擇器與資料過濾功能
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from src.pages._router_base import _TIMELINE_OPTIONS, _TIMELINE_LABELS


def render_timeline_selector(key_prefix: str = "") -> str:
    """
    渲染時間軸選擇器（按鈕風格）。

    Args:
        key_prefix: session_state key 的前綴，避免多頁面衝突。

    Returns:
        選擇的時間範圍字串（"1Y" / "3Y" / "5Y" / "ALL"）
    """
    state_key = f"{key_prefix}timeline_range" if key_prefix else "timeline_range"

    # 初始化預設值
    if state_key not in st.session_state:
        st.session_state[state_key] = "3Y"

    current = st.session_state[state_key]

    st.markdown("📅 **時間範圍：**")

    cols = st.columns(4)
    options = ["1Y", "3Y", "5Y", "ALL"]

    for i, opt in enumerate(options):
        with cols[i]:
            label = _TIMELINE_LABELS[opt]
            is_active = current == opt

            # 使用 CSS 樣式讓選中的按鈕看起來不同
            if is_active:
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
                    > div:nth-child({i+1}) button {{
                        background: #3498DB !important;
                        color: white !important;
                        border-color: #3498DB !important;
                        font-weight: 700 !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button(
                label,
                key=f"{key_prefix}timeline_btn_{opt}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state[state_key] = opt
                st.rerun()

    return st.session_state[state_key]
