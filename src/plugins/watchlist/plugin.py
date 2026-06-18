"""src/plugins/watchlist/plugin.py — Phase 2: LegacyPageAdapter for watchlist."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.watchlist_page import _render_watchlist_page

registered_plugin = LegacyPageAdapter(
    key="watchlist",
    icon="📋",
    category=PluginCategory.TOOL,
    render_fn=_render_watchlist_page,
    requires_stock_id=False,
    requires_data=False,
    order=10,
)
