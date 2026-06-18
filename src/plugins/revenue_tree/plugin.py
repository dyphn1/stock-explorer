"""
src/plugins/revenue_tree/plugin.py
Phase 2: LegacyPageAdapter for revenue_tree (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.revenue_tree import _render_revenue_tree

registered_plugin = LegacyPageAdapter(
    key="revenue_tree",
    icon="🌳",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_revenue_tree,
    requires_stock_id=True,
    requires_data=True,
    order=70,
)
