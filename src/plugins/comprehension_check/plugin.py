"""src/plugins/comprehension_check/plugin.py — Phase 2: LegacyPageAdapter for comprehension_check."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.comprehension_check import _render_comprehension_check

registered_plugin = LegacyPageAdapter(
    key="comprehension_check",
    icon="✅",
    category=PluginCategory.LEARN,
    render_fn=_render_comprehension_check,
    requires_stock_id=False,
    requires_data=False,
    order=20,
)
