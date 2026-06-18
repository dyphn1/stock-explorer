"""
src/plugins/business_card/plugin.py
Phase 2: LegacyPageAdapter for business_card (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.business_card import _render_business_card

registered_plugin = LegacyPageAdapter(
    key="business_card",
    icon="🏢",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_business_card,
    requires_stock_id=True,
    requires_data=True,
    order=10,
)
