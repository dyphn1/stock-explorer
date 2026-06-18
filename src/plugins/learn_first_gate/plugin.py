"""src/plugins/learn_first_gate/plugin.py — Phase 2: LegacyPageAdapter for learn_first_gate."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.learn_first_gate import _render_learn_first_gate

registered_plugin = LegacyPageAdapter(
    key="learn_first_gate",
    icon="🚪",
    category=PluginCategory.LEARN,
    render_fn=_render_learn_first_gate,
    requires_stock_id=False,
    requires_data=False,
    order=60,
)
