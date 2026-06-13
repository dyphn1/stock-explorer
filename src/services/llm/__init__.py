"""
LLM Abstraction Layer — D5
Protocol-based explanation provider with template fallback.
"""

from src.services.llm.base import ExplanationProvider, ExplanationRequest, ExplanationResponse
from src.services.llm.template_provider import TemplateExplanationProvider
from src.services.llm.factory import get_explanation_provider

__all__ = [
    "ExplanationProvider",
    "ExplanationRequest",
    "ExplanationResponse",
    "TemplateExplanationProvider",
    "get_explanation_provider",
]
