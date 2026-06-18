"""src/plugins/case_study_library/plugin.py — Phase 2: LegacyPageAdapter for case_study_library."""
from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.case_study_library import _render_case_study_library

registered_plugin = LegacyPageAdapter(
    key="case_study_library",
    icon="📖",
    category=PluginCategory.LEARN,
    render_fn=_render_case_study_library,
    requires_stock_id=False,
    requires_data=False,
    order=40,
)
