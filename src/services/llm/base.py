"""
LLM Abstraction Layer — Base Protocol & Data Classes

Defines the protocol that any explanation provider must implement,
plus the request/response data classes used across all providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable


@dataclass
class ExplanationRequest:
    """Request for generating an explanation."""

    metric_name: str
    metric_value: str
    delta: Optional[str] = None
    context: dict = field(default_factory=dict)
    language: str = "zh-TW"


@dataclass
class ExplanationResponse:
    """Response containing the generated explanation."""

    text: str
    source: str  # "template" | "llm" | "fallback"
    confidence: float = 1.0
    implication: str = ""  # C143: one-sentence "so what" implication (zh-TW, historian tone)


@runtime_checkable
class ExplanationProvider(Protocol):
    """Protocol for explanation generation providers."""

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        """Generate a plain-language explanation for a metric or change."""
        ...

    def is_available(self) -> bool:
        """Check if this provider is currently available."""
        ...
