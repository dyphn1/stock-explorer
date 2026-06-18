"""src/plugins/financial_wellness/plugin.py — Phase 2: LegacyPageAdapter for financial_wellness."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.financial_wellness import _render_financial_wellness

registered_plugin = LegacyPageAdapter(
    key="financial_wellness",
    icon="💰",
    category=PluginCategory.TOOL,
    render_fn=_render_financial_wellness,
    requires_stock_id=False,
    requires_data=False,
    order=30,
)
