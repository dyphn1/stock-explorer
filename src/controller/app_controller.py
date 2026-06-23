import streamlit as st
from src.core.i18n import t
from src.pages.url_sync import sync_url_to_session, navigate_to
from src.controller.router import (
    get_page_key, is_standalone, is_stock_plugin,
    load_stock_data, resolve_plugin, run_event_detection,
    render_etf_detail_page,
)
from src.services.validation import validate_stock_id
from src.view.layout import render_layout, render_fab_bottom
from src.view.navbar import render_navbar, render_navbar_minimal
from src.view.welcome_page import render_welcome_page


class AppController:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from src.data.finmind_client import FinMindClient
            self._client = FinMindClient(cache_dir=".cache")
        return self._client

    def _get_page_key(self):
        return get_page_key()

    def _navigate(self, page_key: str):
        navigate_to(page=page_key)

    def _process_search(self, query: str) -> str | None:
        if not query or not query.strip():
            return st.session_state.get("stock_id")
        q = query.strip()
        c = self._get_client()
        if q.isdigit():
            is_valid, result = validate_stock_id(q)
            if is_valid:
                return result
            st.error(f"❌ {result}")
            return st.session_state.get("stock_id")
        with st.spinner(t("main.search.searching")):
            results = c.search_stocks(q, case_sensitive=False)
        if results is None or results.empty:
            st.error(t("main.search.not_found"))
            return st.session_state.get("stock_id")
        if len(results) == 1:
            return results.iloc[0]["stock_id"]
        options = [f"{r['stock_id']} {r['stock_name']}" for _, r in results.iterrows()]
        selected = st.selectbox(t("main.search.multiple_results"), options, key="search_select")
        if selected:
            return selected.split()[0]
        return st.session_state.get("stock_id")

    def _render_content(self, stock_id: str, page_key: str):
        client = self._get_client()
        if stock_id != st.session_state.get("stock_id"):
            st.session_state["stock_id"] = stock_id

        if is_standalone(page_key):
            render_navbar_minimal(page_key)
            with st.spinner(t("status.loading_page")):
                if not resolve_plugin(page_key, client):
                    pass
            return

        with st.spinner(t("status.loading_stock")):
            data = load_stock_data(client, stock_id)
        if data is None:
            st.error(t("error.not_found", sid=stock_id))
            return

        run_event_detection(stock_id, data)

        if is_stock_plugin(page_key):
            render_navbar(data, page_key)
            with st.spinner(t("status.loading_page")):
                if not resolve_plugin(page_key, client, stock_id, data):
                    pass
            return

        from src.services.watchlist import _is_etf as _is_etf_check
        if _is_etf_check(stock_id, data["stock_name"], data["industry"]):
            render_navbar(data, page_key)
            with st.spinner(t("status.loading_page")):
                render_etf_detail_page(data, client)
            return

        render_navbar(data, "business_card")
        with st.spinner(t("status.loading_page")):
            resolve_plugin("business_card", client, stock_id, data)

    def run(self):
        sync_url_to_session()
        current_key = self._get_page_key()
        stock_id = st.session_state.get("stock_id")

        search_val = render_layout(current_key, self._navigate)
        stock_id = self._process_search(search_val) or stock_id

        if stock_id:
            self._render_content(stock_id, current_key)
        else:
            render_welcome_page()

        render_fab_bottom(stock_id or "")
