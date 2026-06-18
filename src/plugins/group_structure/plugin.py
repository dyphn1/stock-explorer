"""
src/plugins/group_structure/plugin.py
Phase 2: LegacyPageAdapter for group_structure (data-only stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.group_structure import _render_group_structure

registered_plugin = LegacyPageAdapter(
    key="group_structure",
    icon="🏗️",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_group_structure,
    requires_stock_id=True,
    requires_data=True,
    order=50,
)
