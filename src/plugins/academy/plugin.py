"""
src/plugins/academy/plugin.py
Phase 2: LegacyPageAdapter for academy (standalone page, client-only).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.academy import _render_academy

registered_plugin = LegacyPageAdapter(
    key="academy",
    icon="🎓",
    category=PluginCategory.LEARN,
    render_fn=_render_academy,
    requires_stock_id=False,
    requires_data=False,
    order=30,
)
