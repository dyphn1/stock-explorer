"""
src/plugins/debate_cards/plugin.py
Phase 2: LegacyPageAdapter for debate_cards (data+client stock page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.debate_cards import render_debate_cards_page

registered_plugin = LegacyPageAdapter(
    key="debate_cards",
    icon="🃏",
    category=PluginCategory.ANALYSIS,
    render_fn=render_debate_cards_page,
    requires_stock_id=True,
    requires_data=True,
    order=100,
)
