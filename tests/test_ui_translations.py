"""tests/test_ui_translations.py
Translation verification tests for Stock Explorer using Playwright.
Verifies that t() translations display correctly (not raw keys).
"""
import pytest
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.ui


def test_sidebar_and_main_translations(streamlit_server, page):
    """Verify sidebar and main page show translated text, not raw i18n keys."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    # Wait for the app to render the translated title
    page.wait_for_selector("text=股識", timeout=10000)

    # Check that Activity Bar navigation items appear in Chinese (translated page keys)
    assert page.query_selector("text=📇 名片") is not None, "Activity Bar nav 名片 not found"
    assert page.query_selector("text=📂 分類瀏覽") is not None, "Activity Bar nav 分類瀏覽 not found"
    assert page.query_selector("text=🏷️ ETF 專區") is not None, "Activity Bar nav ETF 專區 not found"
    assert page.query_selector("text=⭐ 關注列表") is not None, "Activity Bar nav 關注列表 not found"
    assert page.query_selector("text=🔔 事件儀表板") is not None, "Activity Bar nav 事件儀表板 not found"
    assert page.query_selector("text=📈 今日市場動態") is not None, "Activity Bar nav 市場動態 not found"

    # Check that translated main page elements appear
    assert page.query_selector("text=股識") is not None, "Main page title not found in Chinese"
    assert page.query_selector("text=認識一家公司，從這裡開始") is not None, "Main page lead1 not found in Chinese"

    # Should NOT show raw i18n keys
    raw_keys = [
        "main.sidebar.search_header",
        "main.sidebar.nav_home",
        "main.sidebar.nav_sector",
        "main.sidebar.nav_category",
        "main.sidebar.nav_etf",
        "main.sidebar.nav_watchlist",
        "main.home.title",
        "main.home.lead1",
        "main.home.lead2",
        "app.title"
    ]
    for key in raw_keys:
        el = page.query_selector(f"text={key}")
        assert el is None, f"Found raw i18n key on page: {key}"


def test_no_raw_i18n_keys_in_sidebar_and_main(streamlit_server, page):
    """General check: no raw i18n key patterns should be visible in sidebar and main."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    page_content = page.content()

    # These patterns in visible text indicate unresolved t() keys
    bad_patterns = ['main.', 'sidebar.', 'app.']
    found_bad = []
    for pattern in bad_patterns:
        elements = page.query_selector_all(f"text={pattern}")
        if elements:
            found_bad.append(pattern)

    assert not found_bad, f"Raw i18n key prefixes found on page: {found_bad}"