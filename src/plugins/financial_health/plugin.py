"""
src/plugins/financial_health/plugin.py
Phase 2: LegacyPageAdapter for financial_health (data-only stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.financial_health import _render_financial_health

registered_plugin = LegacyPageAdapter(
    key="financial_health",
    icon="💪",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_financial_health,
    requires_stock_id=True,
    requires_data=True,
    order=30,
)
