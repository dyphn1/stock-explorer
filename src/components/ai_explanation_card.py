"""
AI explanation card component for displaying AI-generated explanations with confidence level.
"""

import streamlit as st
from src.core.i18n import t


def _ai_explanation_card(
    title: str,
    explanation_text: str,
    confidence_level: int | None = None,
) -> None:
    """Render an AI-style explanation card with optional confidence level.

    Args:
        title: Locale key for the title (e.g., "ai_explanation.title").
        explanation_text: Locale key for the explanation text (e.g., "ai_explanation.explanation").
        confidence_level: Optional confidence level (0-100). If provided, displays a confidence badge.
    """
    # Get translated strings
    title_text = t(title)
    explanation = t(explanation_text)

    # Build the content string
    content = f"**{title_text}**\n\n{explanation}"
    if confidence_level is not None:
        # Clamp confidence level between 0 and 100
        confidence_level = max(0, min(100, confidence_level))
        content += f"\n\n---\n**{t('ai_explanation.confidence')}:** {confidence_level}%"

    # Display using st.info for an info box
    st.info(content)
