from collections.abc import Callable

import streamlit as st
from src.view.activity_bar import render_activity_bar
from src.view.search_bar import render_search_bar


def _inject_global_styles():
    collapsed = st.session_state.get("sidebar_collapsed", False)
    sidebar_w = "48px" if collapsed else "240px"

    st.html(f"""
<style>
:root {{
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8F9FA;
  --text-primary: #1C1C1E;
  --text-secondary: #7F8C8D;
  --border-color: #E5E5EA;
  --accent: #007AFF;
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --bg-primary: #1C1C1E;
    --bg-secondary: #2C2C2E;
    --text-primary: #F2F2F7;
    --text-secondary: #8E8E93;
    --border-color: #38383A;
    --accent: #0A84FF;
  }}
}}

* {{ transition: background-color 0.2s ease, color 0.2s ease; }}

/* ── Remove Streamlit default sidebar page nav ── */
div[data-testid="stSidebarNav"] {{ display: none !important; }}

/* ── Sidebar width control ── */
section[data-testid="stSidebar"] {{
  width: {sidebar_w} !important;
  min-width: {sidebar_w} !important;
  max-width: {sidebar_w} !important;
  transition: width 0.25s ease, min-width 0.25s ease !important;
}}

/* ── Home button (app logo) — left-aligned, no frame ── */
section[data-testid="stSidebar"] button[key="sd_home"] {{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  font-size: 20px !important;
  font-weight: 600 !important;
  text-align: left !important;
  padding: 12px 8px !important;
  color: var(--text-primary) !important;
  min-height: 48px !important;
  width: 100% !important;
  cursor: pointer !important;
}}
section[data-testid="stSidebar"] button[key="sd_home"]:hover {{
  background: var(--bg-secondary) !important;
}}

/* ── Collapse toggle at bottom — matches nav item style ── */
section[data-testid="stSidebar"] button[key="sd_toggle"] {{
  font-size: 14px !important;
}}

/* ── Sidebar nav buttons: no borders/frames ── */
section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] button {{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  font-size: 18px !important;
  padding: 6px 4px !important;
  text-align: center !important;
  color: var(--text-primary) !important;
  min-height: 36px !important;
}}
section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] button:hover {{
  background: var(--bg-secondary) !important;
  border-radius: 6px !important;
}}
section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] button:focus-visible {{
  outline: none !important;
  box-shadow: none !important;
}}
/* Active nav item: subtle highlight */
section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] button[type="primary"] {{
  background: var(--accent) !important;
  color: white !important;
  border-radius: 6px !important;
}}

/* ── Responsive ── */
@media (max-width: 768px) {{
  section[data-testid="stSidebar"] {{ min-width: 200px !important; width: 200px !important; }}
}}

@media (max-width: 480px) {{
  section[data-testid="stSidebar"] {{ min-width: 100% !important; width: 100% !important; }}
  .stRadio [role="radiogroup"] {{ flex-wrap: wrap; }}
}}
</style>
<script>
(function(){{
    function h(){{var n=document.querySelector('div[data-testid="stSidebarNav"]');if(n)n.remove();}}
    h();var t=document.querySelector('section[data-testid="stSidebar"]')||document.body;
    new MutationObserver(h).observe(t,{{childList:true,subtree:true,attributes:true}});
}})();
</script>
""")


def render_layout(
    current_key: str,
    on_navigate: Callable[[str], None],
    activity_items: list[tuple[str, str, str]],
    hot_stocks: list[tuple[str, str]],
    hot_etfs: list[tuple[str, str]],
    on_hot_stock_click: Callable[[str, str], None] | None = None,
    on_go_home: Callable[[], None] | None = None,
    stock_id: str | None = None,
    fab_menu_items: list[dict] | None = None,
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
            on_go_home=on_go_home,
        )

    search_val = render_search_bar()

    _render_fab(stock_id, fab_menu_items)

    return search_val


def _render_fab(stock_id: str | None, menu_items: list[dict] | None):
    if stock_id and menu_items:
        from src.view.fab import render_fab
        render_fab(stock_id, menu_items)
