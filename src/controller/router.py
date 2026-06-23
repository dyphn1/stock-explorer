import logging
from src.data.finmind_client import FinMindClient
from src.pages._router_base import get_stock_data
from src.services.adaptive_engine import run_auto_detection
from src.services.settings_service import get_threshold
from src.services.watchlist import _is_etf as _is_etf_check
from src.core.plugin_protocol import PluginRenderContext
from src.core.plugin_registry import PluginRegistry

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
    from src.pages.event_dashboard import _render_adaptive_banner, _render_event_alerts
    try:
        price_threshold = get_threshold(st.session_state, "settings_price_threshold")
        revenue_threshold = get_threshold(st.session_state, "settings_revenue_threshold")
        new_events = run_auto_detection(stock_id, data, price_threshold=price_threshold, revenue_threshold=revenue_threshold)
        _render_adaptive_banner(data)
        _render_event_alerts(stock_id)
    except Exception as exc:
        logger.warning("M5 event detection/rendering failed for %s: %s", stock_id, exc)


def render_etf_detail_page(data: dict, client: FinMindClient):
    from src.pages.etf_detail import _render_etf_detail
    _render_etf_detail(data, client)


def get_page_key() -> str:
    import streamlit as st
    from src.controller.url_sync import _PAGE_NAME_TO_KEY
    name = st.session_state.get("page")
    if name and name in _PAGE_NAME_TO_KEY:
        return _PAGE_NAME_TO_KEY[name]
    return st.session_state.get("page_key", "business_card")


# ── Page config data (owned by controller, consumed by view) ────

_ACTIVITY_ITEMS: list[tuple[str, str, str]] = [
    ("business_card", "📇", "基本資料"),
    ("category_browser", "📂", "分類瀏覽"),
    ("etf_section", "🏷️", "ETF 專區"),
    ("watchlist", "⭐", "關注清單"),
    ("event_dashboard", "🔔", "事件儀表板"),
    ("daily_market", "📈", "市場動態"),
    ("settings", "⚙️", "設定"),
]

_HOT_STOCKS: list[tuple[str, str]] = [
    ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
    ("2308", "台達電"), ("2881", "富邦金"),
]

_HOT_ETFS: list[tuple[str, str]] = [
    ("0050", "元大台灣50"), ("0056", "元大高股息"),
    ("00878", "國泰永續高股息"), ("00919", "群益台灣精選高息"),
]

_FAB_MENU_ITEMS: list[dict] = [
    {"icon": "📇", "label": "基本資料", "href": "?page=名片&stock_id={stock_id}"},
    {"icon": "🔧", "label": "營運健檢", "href": "?page=營運健檢&stock_id={stock_id}"},
    {"icon": "💊", "label": "財務體質", "href": "?page=財務體質&stock_id={stock_id}"},
    {"icon": "📊", "label": "同業比較", "href": "?page=同業比較&stock_id={stock_id}"},
    {"icon": "🏗️", "label": "集團架構", "href": "?page=集團架構&stock_id={stock_id}"},
    {"divider": True},
    {"icon": "🌳", "label": "營收結構樹", "href": "?page=營收結構樹&stock_id={stock_id}"},
    {"icon": "📚", "label": "同業比較故事", "href": "?page=同業比較故事&stock_id={stock_id}"},
    {"icon": "🏰", "label": "護城河比較", "href": "?page=護城河比較&stock_id={stock_id}"},
]


def get_activity_items() -> list[tuple[str, str, str]]:
    return list(_ACTIVITY_ITEMS)


def get_hot_stocks() -> list[tuple[str, str]]:
    return list(_HOT_STOCKS)


def get_hot_etfs() -> list[tuple[str, str]]:
    return list(_HOT_ETFS)


def get_fab_menu_items() -> list[dict]:
    return list(_FAB_MENU_ITEMS)
