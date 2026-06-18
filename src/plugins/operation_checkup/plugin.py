"""
src/plugins/operation_checkup/plugin.py
Phase 2: LegacyPageAdapter for operation_checkup (data-only stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.operation_checkup import _render_operation_checkup

registered_plugin = LegacyPageAdapter(
    key="operation_checkup",
    icon="🔧",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_operation_checkup,
    requires_stock_id=True,
    requires_data=True,
    order=20,
)
