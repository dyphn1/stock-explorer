"""
src/plugins/settings/plugin.py
Phase 1: LegacyPageAdapter for settings (system page, no params needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.settings import render_settings_page

registered_plugin = LegacyPageAdapter(
    key="settings",
    icon="⚙️",
    category=PluginCategory.SYSTEM,
    render_fn=render_settings_page,
    requires_stock_id=False,
    requires_data=False,
    order=30,
)
