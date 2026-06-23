"""src/plugins/etf_detail/plugin.py — LegacyPageAdapter for etf_detail."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.etf_detail import _render_etf_detail

registered_plugin = LegacyPageAdapter(
    key="etf_detail",
    icon="📊",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_etf_detail,
    requires_stock_id=True,
    requires_data=True,
    order=10,
)