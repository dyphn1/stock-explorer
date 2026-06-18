"""
src/plugins/moat_comparison/plugin.py
Phase 2: LegacyPageAdapter for moat_comparison (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.moat_comparison import _render_moat_comparison_page

registered_plugin = LegacyPageAdapter(
    key="moat_comparison",
    icon="🏰",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_moat_comparison_page,
    requires_stock_id=True,
    requires_data=True,
    order=90,
)
