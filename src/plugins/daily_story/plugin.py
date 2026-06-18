"""src/plugins/daily_story/plugin.py — Phase 2: LegacyPageAdapter for daily_story (wrapper)."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.investor_story_feed import render_investor_story_feed

def _render_daily_story_adapter(client):
    """Adapter: render_investor_story_feed expects (data, client) but data is unused."""
    render_investor_story_feed({}, client)

registered_plugin = LegacyPageAdapter(
    key="daily_story",
    icon="📰",
    category=PluginCategory.LEARN,
    render_fn=_render_daily_story_adapter,
    requires_stock_id=False,
    requires_data=False,
    order=70,
)
