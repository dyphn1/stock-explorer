import streamlit as st
from src.core.i18n import t
from src.view.activity_bar import render_activity_bar
from src.view.search_bar import render_search_bar
from src.view.fab import render_fab


_ACTIVITY_ITEMS = [
    ("business_card", "📇", "基本資料"),
    ("category_browser", "📂", "分類瀏覽"),
    ("etf_section", "🏷️", "ETF 專區"),
    ("watchlist", "⭐", "關注清單"),
    ("event_dashboard", "🔔", "事件儀表板"),
    ("daily_market", "📈", "市場動態"),
    ("settings", "⚙️", "設定"),
]

_HOT_STOCKS = [
    ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
    ("2308", "台達電"), ("2881", "富邦金"),
]

_HOT_ETFS = [
    ("0050", "元大台灣50"), ("0056", "元大高股息"),
    ("00878", "國泰永續高股息"), ("00919", "群益台灣精選高息"),
]

_FAB_MENU_ITEMS = [
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


def _inject_global_styles():
    st.html("""
<style>
.fab-container {
  position: fixed; bottom: 24px; right: 24px; z-index: 999;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.fab-button {
  width: 56px; height: 56px; border-radius: 50%; background: #007AFF;
  color: white; border: none; box-shadow: 0 4px 16px rgba(0,122,255,0.3);
  font-size: 28px; cursor: pointer; display: flex; align-items: center;
  justify-content: center; transition: transform 0.2s, box-shadow 0.2s; line-height: 1;
}
.fab-button:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(0,122,255,0.4); }
.fab-button:active { transform: scale(0.95); }
.fab-menu {
  display: none; position: absolute; bottom: 70px; right: 0;
  background: white; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  padding: 6px; min-width: 210px; max-height: 60vh; overflow-y: auto;
}
.fab-menu.show { display: block; }
.fab-menu-item {
  padding: 10px 16px; cursor: pointer; border-radius: 10px; font-size: 14px;
  color: #1C1C1E; display: flex; align-items: center; gap: 10px;
  text-decoration: none; transition: background 0.15s;
}
.fab-menu-item:hover { background: #F2F2F7; text-decoration: none; color: #1C1C1E; }
.fab-divider { height: 1px; background: #E5E5EA; margin: 4px 12px; }
.fab-overlay {
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 998;
}
.fab-overlay.show { display: block; }
</style>
""")

    st.html("""
<script>
(function(){
    function h(){var n=document.querySelector('section[data-testid="stSidebarNav"]');if(n)n.remove();}
    h();var t=document.querySelector('section[data-testid="stSidebar"]')||document.body;
    new MutationObserver(h).observe(t,{childList:true,subtree:true,attributes:true});
})();
</script>
""")


def render_layout(current_key: str, on_navigate: callable):
    _inject_global_styles()
    with st.sidebar:
        render_activity_bar(
            items=_ACTIVITY_ITEMS,
            current_key=current_key,
            hot_stocks=_HOT_STOCKS,
            hot_etfs=_HOT_ETFS,
            on_navigate=on_navigate,
        )

    search_val = render_search_bar()
    return search_val


def render_fab_bottom(stock_id: str):
    if stock_id:
        render_fab(stock_id, _FAB_MENU_ITEMS)
