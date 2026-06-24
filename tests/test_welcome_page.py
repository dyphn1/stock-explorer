"""Welcome page tests using chainable Page Object Model.

Usage:
    pytest tests/test_welcome_page.py -v
    pytest tests/test_welcome_page.py -v -k "test_welcome_flow"

Chainable pattern:
    WelcomePage(page, url).load()
        .assert_title_visible()
        .assert_search_bar_visible()
        .search("2330")
            .assert_stock_id_visible("2330")
"""

import pytest
from tests.pages.welcome_page import WelcomePage
from tests.pages.stock_page import StockPage

pytestmark = pytest.mark.ui


# ── Individual assertions ─────────────────────────────────────

def test_welcome_title(streamlit_server, page):
    WelcomePage(page, streamlit_server).load().assert_title_visible()


def test_welcome_lead(streamlit_server, page):
    WelcomePage(page, streamlit_server).load().assert_lead1_visible()


def test_welcome_search_bar(streamlit_server, page):
    (WelcomePage(page, streamlit_server).load()
     .assert_search_bar_visible()
     .assert_search_above_welcome())


def test_welcome_sidebar(streamlit_server, page):
    (WelcomePage(page, streamlit_server).load()
     .assert_sidebar_visible()
     .assert_sidebar_has_item("名片")
     .assert_sidebar_has_item("分類瀏覽")
     .assert_sidebar_has_item("ETF 專區")
     .assert_sidebar_has_item("設定")
     .assert_disclaimer_visible()
     .assert_hot_stocks_expander_visible()
     .assert_hot_etfs_expander_visible())


def test_welcome_no_raw_i18n_keys(streamlit_server, page):
    WelcomePage(page, streamlit_server).load().assert_no_raw_i18n_keys()


def test_welcome_page_title(streamlit_server, page):
    WelcomePage(page, streamlit_server).load().assert_page_title_correct()


# ── Chainable navigation flows ────────────────────────────────

@pytest.mark.xfail(reason="key_takeaways.2330.X raw i18n keys visible on stock page — needs locale fix")
def test_welcome_to_stock_flow(streamlit_server, page):
    """Chain: Welcome → search 2330 → Stock detail page."""
    stock_page = (WelcomePage(page, streamlit_server).load()
                  .assert_title_visible()
                  .search("2330"))

    stock_page.assert_stock_id_visible("2330")
    stock_page.assert_no_raw_i18n_keys()


def test_welcome_to_stock_metrics(streamlit_server, page):
    """Chain: Welcome → search 2330 → check metric icons."""
    (WelcomePage(page, streamlit_server).load()
     .search("2330")
     .assert_stock_id_visible("2330")
     .assert_metric_icons_visible())


def test_welcome_to_settings_flow(streamlit_server, page):
    """Chain: Welcome → sidebar click '設定' → Settings page."""
    (WelcomePage(page, streamlit_server).load()
     .navigate_to_settings()
     .assert_loaded())
