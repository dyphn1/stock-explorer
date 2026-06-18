"""src/plugins/stock_screener/plugin.py — Phase 2: LegacyPageAdapter for stock_screener."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.stock_screener import _render_stock_screener

registered_plugin = LegacyPageAdapter(
    key="stock_screener",
    icon="🔎",
    category=PluginCategory.TOOL,
    render_fn=_render_stock_screener,
    requires_stock_id=False,
    requires_data=False,
    order=40,
)
