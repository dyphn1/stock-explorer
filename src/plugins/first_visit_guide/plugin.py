"""src/plugins/first_visit_guide/plugin.py — Phase 2: LegacyPageAdapter for first_visit_guide."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.first_visit_guide import _render_first_visit_guide

registered_plugin = LegacyPageAdapter(
    key="first_visit_guide",
    icon="👋",
    category=PluginCategory.LEARN,
    render_fn=_render_first_visit_guide,
    requires_stock_id=False,
    requires_data=False,
    order=50,
)
