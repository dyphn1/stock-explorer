"""
src/plugins/story_timeline/plugin.py
Phase 2: LegacyPageAdapter for story_timeline / render_company_timeline (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.company_timeline import render_company_timeline

registered_plugin = LegacyPageAdapter(
    key="story_timeline",
    icon="📅",
    category=PluginCategory.ANALYSIS,
    render_fn=render_company_timeline,
    requires_stock_id=True,
    requires_data=True,
    order=60,
)
