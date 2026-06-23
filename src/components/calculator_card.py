"""
Calculator card component for interactive financial calculations.
"""

import streamlit as st
from src.core.i18n import t


def _calculator_card(
    title: str,
    formula: str,
    input1_label: str,
    input2_label: str,
    result_label: str,
    button_label: str = "Calculate",
    key: str | None = None,
) -> None:
    """Render a financial calculator card with two inputs and a result.

    Args:
        title: The title of the calculator (e.g., "ROE Calculator").
        formula: The formula to display (e.g., "ROE = (Net Income / Shareholder's Equity) × 100").
        input1_label: Label for the first input field.
        input2_label: Label for the second input field.
        result_label: Label for the result field.
        button_label: Label for the calculate button (defaults to "Calculate").
        key: Optional key for the Streamlit widgets to avoid conflicts.
            If not provided, a key is generated based on the input parameters.
    """
    # Generate a key if not provided
    if key is None:
        key = f"_calculator_{hash((title, formula, input1_label, input2_label, result_label, button_label))}"

    # Unique keys for widgets
    input1_key = f"{key}_input1"
    input2_key = f"{key}_input2"
    button_key = f"{key}_button"
    result_key = f"{key}_result"

    # Container for the card
    with st.container():
        # Card styling similar to _infocard
        st.markdown(
            """
            <div style="background:white;border-radius:12px;padding:1.2rem;border:1px solid #E1E4E8;border-left:4px solid #3498DB;margin:0.5rem 0;">
            """,
            unsafe_allow_html=True,
        )

        # Title
        st.markdown(f"**{title}**")

        # Formula display
        st.markdown(f"*{formula}*")

        # Input fields in two columns
        col1, col2 = st.columns(2)
        with col1:
            val1 = st.number_input(
                input1_label,
                min_value=0.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                key=input1_key,
            )
        with col2:
            val2 = st.number_input(
                input2_label,
                min_value=0.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                key=input2_key,
            )

        # Calculate button
        if st.button(button_label, key=button_key):
            # Avoid division by zero
            if val2 != 0:
                result = (val1 / val2) * 100
                st.session_state[result_key] = result
            else:
                st.session_state[result_key] = None
                st.error("Division by zero")

        # Result display
        result_value = st.session_state.get(result_key)
        if result_value is not None:
            st.markdown(
                f"<div style='font-size:1.6rem;font-weight:700;color:#2C3E50;margin:0.5rem 0;'>"
                f"{result_label}: {result_value:.2f}%</div>",
                unsafe_allow_html=True,
            )
        else:
            # Show placeholder if not calculated yet
            st.markdown(
                f"<div style='font-size:1.1rem;color:#7F8C8D;margin:0.5rem 0;'>"
                f"{result_label}: --</div>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)