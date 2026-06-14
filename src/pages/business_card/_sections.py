"""Business card section rendering functions — 15 sections (D24+C188).

This module is now a backward-compatible re-export shim.
All functions have been split into sub-modules under _sections/:
  _summary_hero — header, story_card
  _summary  — takeaways, one_liner, news
  _financial — key_metrics, dividend, revenue_breakdown, revenue_trend, valuation
  _health   — health, risk
  _story    — deltas, compare_stories, read_next
  _why_moved — why_moved (C188)
  _detail   — share_section, footer
"""
from src.pages.business_card._sections._summary_hero import (  # noqa: F401,F403
    _render_header,
    _render_story_card,
)
from src.pages.business_card._sections._summary import (  # noqa: F401,F403
    _render_takeaways,
    _render_one_liner,
    _render_news,
)
from src.pages.business_card._sections._financial import (
    _render_key_metrics,
    _render_dividend,
    _render_revenue_breakdown,
    _render_revenue_trend,
    _render_valuation,
)
from src.pages.business_card._sections._health import (
    _render_health,
    _render_risk,
)
from src.pages.business_card._sections._story import (
    _render_deltas,
    _render_compare_stories,
    _render_read_next,
)
from src.pages.business_card._sections._why_moved import (
    _render_why_moved,
)
from src.pages.business_card._sections._detail import (
    _render_share_section,
    _render_footer,
)

__all__ = [
    "_render_header",
    "_render_story_card",
    "_render_takeaways",
    "_render_deltas",
    "_render_health",
    "_render_risk",
    "_render_one_liner",
    "_render_key_metrics",
    "_render_dividend",
    "_render_revenue_breakdown",
    "_render_revenue_trend",
    "_render_valuation",
    "_render_compare_stories",
    "_render_news",
    "_render_read_next",
    "_render_why_moved",
    "_render_share_section",
    "_render_footer",
]
