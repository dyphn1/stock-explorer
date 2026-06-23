from collections.abc import Callable

import streamlit as st
from src.view.activity_bar import render_activity_bar
from src.view.search_bar import render_search_bar
from src.view.fab import render_fab


def _inject_global_styles():
    st.html("""
<style>
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8F9FA;
  --text-primary: #1C1C1E;
  --text-secondary: #7F8C8D;
  --border-color: #E5E5EA;
  --accent: #007AFF;
  --sidebar-width: 260px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1C1C1E;
    --bg-secondary: #2C2C2E;
    --text-primary: #F2F2F7;
    --text-secondary: #8E8E93;
    --border-color: #38383A;
    --accent: #0A84FF;
  }
}

* { transition: background-color 0.2s ease, color 0.2s ease; }

@media (max-width: 768px) {
  section[data-testid="stSidebar"] { min-width: 200px !important; width: 200px !important; }
}

@media (max-width: 480px) {
  section[data-testid="stSidebar"] { min-width: 100% !important; width: 100% !important; }
  .stRadio [role="radiogroup"] { flex-wrap: wrap; }
}
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


def render_layout(
    current_key: str,
    on_navigate: Callable[[str], None],
    activity_items: list[tuple[str, str, str]],
    hot_stocks: list[tuple[str, str]],
    hot_etfs: list[tuple[str, str]],
    on_hot_stock_click: Callable[[str, str], None] | None = None,
):
    _inject_global_styles()
    with st.sidebar:
        render_activity_bar(
            items=activity_items,
            current_key=current_key,
            hot_stocks=hot_stocks,
            hot_etfs=hot_etfs,
            on_navigate=on_navigate,
            on_hot_stock_click=on_hot_stock_click,
        )

    search_val = render_search_bar()
    return search_val


def render_fab_bottom(stock_id: str, fab_menu_items: list[dict]):
    if stock_id:
        render_fab(stock_id, fab_menu_items)
