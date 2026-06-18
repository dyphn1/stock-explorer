"""src/plugins/investment_memo/plugin.py — Phase 2: LegacyPageAdapter for investment_memo."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.investment_memo import _render_investment_memo

registered_plugin = LegacyPageAdapter(
    key="investment_memo",
    icon="📝",
    category=PluginCategory.TOOL,
    render_fn=_render_investment_memo,
    requires_stock_id=False,
    requires_data=False,
    order=20,
)
