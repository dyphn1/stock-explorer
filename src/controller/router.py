import logging
from src.data.finmind_client import FinMindClient
from src.pages._router_base import get_stock_data
from src.services.adaptive_engine import run_auto_detection
from src.services.settings_service import get_threshold
from src.services.watchlist import _is_etf as _is_etf_check
from src.core.plugin_protocol import PluginRenderContext
from src.core.plugin_registry import PluginRegistry
from src.pages.event_dashboard import _render_adaptive_banner, _render_event_alerts
from src.pages.etf_detail import _render_etf_detail

logger = logging.getLogger(__name__)

_STANDALONE_PLUGIN_KEYS = {
    "category_browser", "settings", "event_dashboard", "notification_center",
    "daily_market", "watchlist", "investment_memo", "etf_section", "case_study",
    "financial_wellness", "comprehension_check", "case_study_library",
    "stock_screener", "sector_heatmap", "learn_first_gate", "first_visit_guide",
    "daily_story", "academy",
}

_STOCK_PLUGIN_KEYS = {
    "business_card", "operation_checkup", "financial_health", "peer_comparison",
    "group_structure", "story_timeline", "full_story_timeline", "revenue_tree",
    "compare_stories", "moat_comparison", "debate_cards",
}

_registry: PluginRegistry | None = None


def _get_registry() -> PluginRegistry:
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
        count = _registry.discover()
        logger.info("PluginRegistry initialized: %d plugins discovered.", count)
    return _registry


def resolve_plugin(page_key: str, client: FinMindClient, stock_id: str | None = None, data: dict | None = None) -> bool:
    registry = _get_registry()
    if not registry.has(page_key):
        return False
    import streamlit as st
    plugin = registry.get(page_key)
    ctx = PluginRenderContext(
        page_key=page_key, data=data, client=client,
        stock_id=stock_id, session_state=st.session_state,
    )
    plugin.render(ctx)
    return True


def is_standalone(page_key: str) -> bool:
    return page_key in _STANDALONE_PLUGIN_KEYS


def is_stock_plugin(page_key: str) -> bool:
    return page_key in _STOCK_PLUGIN_KEYS


def load_stock_data(client: FinMindClient, stock_id: str) -> dict | None:
    return get_stock_data(client, stock_id)


def run_event_detection(stock_id: str, data: dict):
    import streamlit as st
    try:
        price_threshold = get_threshold(st.session_state, "settings_price_threshold")
        revenue_threshold = get_threshold(st.session_state, "settings_revenue_threshold")
        new_events = run_auto_detection(stock_id, data, price_threshold=price_threshold, revenue_threshold=revenue_threshold)
        _render_adaptive_banner(data)
        _render_event_alerts(stock_id)
    except Exception as exc:
        logger.warning("M5 event detection/rendering failed for %s: %s", stock_id, exc)


def render_etf_detail_page(data: dict, client: FinMindClient):
    _render_etf_detail(data, client)


def get_page_key() -> str:
    import streamlit as st
    from src.pages.url_sync import _PAGE_NAME_TO_KEY
    name = st.session_state.get("page")
    if name and name in _PAGE_NAME_TO_KEY:
        return _PAGE_NAME_TO_KEY[name]
    return st.session_state.get("page_key", "business_card")
