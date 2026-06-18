"""
src/plugins/daily_market/plugin.py
Phase 1: LegacyPageAdapter for daily_market (standalone page, no stock_id needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.daily_market import _render_daily_market

registered_plugin = LegacyPageAdapter(
    key="daily_market",
    icon="📈",
    category=PluginCategory.BROWSE,
    render_fn=_render_daily_market,
    requires_stock_id=False,
    requires_data=False,
    order=40,
)
