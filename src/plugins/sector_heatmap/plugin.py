"""src/plugins/sector_heatmap/plugin.py — Phase 2: LegacyPageAdapter for sector_heatmap."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.sector_heatmap import _render_sector_heatmap

registered_plugin = LegacyPageAdapter(
    key="sector_heatmap",
    icon="🔥",
    category=PluginCategory.BROWSE,
    render_fn=_render_sector_heatmap,
    requires_stock_id=False,
    requires_data=False,
    order=30,
)
