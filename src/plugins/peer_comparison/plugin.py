"""
src/plugins/peer_comparison/plugin.py
Phase 2: LegacyPageAdapter for peer_comparison (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.peer_comparison import _render_peer_comparison

registered_plugin = LegacyPageAdapter(
    key="peer_comparison",
    icon="👥",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_peer_comparison,
    requires_stock_id=True,
    requires_data=True,
    order=40,
)
