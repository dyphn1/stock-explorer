"""Business card sections — split into sub-modules by concern."""

from src.pages.business_card._sections._summary_hero import (
    _render_header,
    _render_story_card,
)
from src.pages.business_card._sections._summary import (
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
from src.pages.business_card._sections._detail import (
    _render_share_section,
    _render_footer,
)
from src.pages.business_card._sections._historical_pattern import (
    _render_historical_pattern,
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
    "_render_share_section",
    "_render_footer",
    "_render_historical_pattern",
]
