from collections.abc import Callable

import streamlit as st
from src.view.activity_bar import render_activity_bar
from src.view.search_bar import render_search_bar
from src.view.fab import render_fab


def _inject_global_styles():
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
