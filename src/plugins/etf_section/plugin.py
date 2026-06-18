"""src/plugins/etf_section/plugin.py — Phase 2: LegacyPageAdapter for etf_section."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.etf_browser import _render_etf_browser

registered_plugin = LegacyPageAdapter(
    key="etf_section",
    icon="🏷️",
    category=PluginCategory.BROWSE,
    render_fn=_render_etf_browser,
    requires_stock_id=False,
    requires_data=False,
    order=20,
)
