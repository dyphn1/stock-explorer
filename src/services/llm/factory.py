"""
LLM Provider Factory — D5

Returns the best available explanation provider.
Currently always returns TemplateExplanationProvider.
Future: check config for LLM provider, fall back to template.
"""

from __future__ import annotations

from src.services.llm.base import ExplanationProvider
from src.services.llm.template_provider import TemplateExplanationProvider


def get_explanation_provider() -> ExplanationProvider:
    """Get the best available explanation provider.

    Returns:
        An ExplanationProvider instance.
        Currently always returns TemplateExplanationProvider.
        Future: check config for LLM provider, fall back to template.
    """
    # Future: check config for LLM provider, fall back to template
    return TemplateExplanationProvider()
