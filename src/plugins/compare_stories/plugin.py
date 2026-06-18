"""
src/plugins/compare_stories/plugin.py
Phase 2: LegacyPageAdapter for compare_stories (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.compare_stories import _render_compare_stories_page

registered_plugin = LegacyPageAdapter(
    key="compare_stories",
    icon="📖",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_compare_stories_page,
    requires_stock_id=True,
    requires_data=True,
    order=80,
)
