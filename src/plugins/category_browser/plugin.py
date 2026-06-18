"""
src/plugins/category_browser/plugin.py
Phase 1: LegacyPageAdapter for category_browser (standalone page, no stock_id needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.category_browser import _render_category_browser

registered_plugin = LegacyPageAdapter(
    key="category_browser",
    icon="🗺️",
    category=PluginCategory.BROWSE,
    render_fn=_render_category_browser,
    requires_stock_id=False,
    requires_data=False,
    order=10,
)
