"""
Metric card component for displaying key metrics with label, value, and optional trend indicator.
"""

import streamlit as st
from src.core.i18n import t


def _infocard(label: str, value: str, trend: str = None) -> None:
    """Render a metric card with label, value, and optional trend indicator.

    Args:
        label: The label/name of the metric (e.g., "Revenue", "Profit Margin")
        value: The value to display (e.g., "$1.2M", "15.3%", "42")
        trend: Optional trend indicator - "up" (📈), "down" (📉), or None for no trend
    """
    # Determine trend icon and color
    trend_icon = ""
    trend_color = "#7F8C8D"  # Default gray color
    
    if trend == "up":
        trend_icon = " 📈"
        trend_color = "#27AE60"  # Green
    elif trend == "down":
        trend_icon = " 📉"
        trend_color = "#E74C3C"  # Red
    
    # Style similar to _白话_card but simplified for metric display
    st.markdown("""
    <div style=\"background:white;border-radius:12px;padding:1.2rem;border:1px solid #E1E4E8;border-left:4px solid #3498DB;margin:0.5rem 0;\">
        <div style=\"font-size:0.85rem;color:#7F8C8D;\">""" + label + """</div>
        <div style=\"font-size:1.8rem;font-weight:700;color:#2C3E50;margin:0.2rem 0;\">""" + value + trend_icon + """</div>
    </div>
    """, unsafe_allow_html=True)