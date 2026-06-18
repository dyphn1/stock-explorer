"""
src/plugins/event_dashboard/plugin.py
Phase 1: LegacyPageAdapter for event_dashboard (standalone page, no stock_id needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.event_dashboard import _render_event_dashboard

registered_plugin = LegacyPageAdapter(
    key="event_dashboard",
    icon="📊",
    category=PluginCategory.SYSTEM,
    render_fn=_render_event_dashboard,
    requires_stock_id=False,
    requires_data=False,
    order=10,
)
