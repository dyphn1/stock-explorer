"""src/plugins/case_study/plugin.py — Phase 2: LegacyPageAdapter for case_study."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.market_event_case_study import _render_market_event_case_study

registered_plugin = LegacyPageAdapter(
    key="case_study",
    icon="📚",
    category=PluginCategory.LEARN,
    render_fn=_render_market_event_case_study,
    requires_stock_id=False,
    requires_data=False,
    order=10,
)
