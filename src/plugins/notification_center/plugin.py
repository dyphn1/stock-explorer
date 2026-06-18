"""
src/plugins/notification_center/plugin.py
Phase 1: LegacyPageAdapter for notification_center (standalone page, no stock_id needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.notification_center import _render_notification_center

registered_plugin = LegacyPageAdapter(
    key="notification_center",
    icon="🔔",
    category=PluginCategory.SYSTEM,
    render_fn=_render_notification_center,
    requires_stock_id=False,
    requires_data=False,
    order=20,
)
