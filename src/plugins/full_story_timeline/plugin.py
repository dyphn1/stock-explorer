"""
src/plugins/full_story_timeline/plugin.py
Phase 2: LegacyPageAdapter for full_story_timeline / render_story_timeline_page (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.story_timeline import render_story_timeline_page

registered_plugin = LegacyPageAdapter(
    key="full_story_timeline",
    icon="📆",
    category=PluginCategory.ANALYSIS,
    render_fn=render_story_timeline_page,
    requires_stock_id=True,
    requires_data=True,
    order=65,
)
