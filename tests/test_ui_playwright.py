"""tests/test_ui_playwright.py
Playwright UI tests for Stock Explorer.
Focuses on navigation and UI element verification.
"""
import pytest
import time
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.ui

# ── Test cases ────────────────────────────────────────────────

def test_main_page_loads(streamlit_server, page):
    """Verify the main page loads without errors."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Wait for Streamlit to render

    # Check that the page title is set (from t("app.title"))
    # We can check for the translated title "股識"
    assert page.query_selector("text=股識") is not None, "Translated title not found"


def test_no_raw_translation_keys(streamlit_server, page):
    """Check that the page doesn't contain raw t() keys (like 'main.welcome.title')."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # List of known raw i18n key prefixes that should not appear in visible text
    bad_patterns = ['main.', 'sidebar.', 'app.', 'daily_market.', 'screener.']
    found_bad = []
    for pattern in bad_patterns:
        elements = page.query_selector_all(f"text={pattern}")
        if elements:
            found_bad.append(pattern)

    assert not found_bad, f"Raw i18n key prefixes found on page: {found_bad}"


def test_search_box_exists(streamlit_server, page):
    """Verify the search input is present."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # The search input has a placeholder containing '台積電' (as seen in the app)
    search_input = page.query_selector("input[placeholder*='台積電']")
    assert search_input is not None, "Search input box not found"


def test_key_ui_elements(streamlit_server, page):
    """Verify key elements like the sidebar, main content area are rendered."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Sidebar should be present (since initial_sidebar_state="expanded")
    sidebar = page.query_selector("[data-testid='stSidebar']")
    assert sidebar is not None, "Sidebar not found"

    # Main content area
    main_content = page.query_selector("[data-testid='stMain']")
    assert main_content is not None, "Main content area not found"

    # Check for some known translated text in the main content
    welcome_subtitle = page.query_selector("text=認識一家公司，從這裡開始")
    assert welcome_subtitle is not None, "Welcome subtitle not found"


def test_search_navigation(streamlit_server, page):
    """Search for a stock and verify navigation to a stock page."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Fill in the search box with a stock ID (e.g., 台積電 -> 2330)
    search_input = page.query_selector("input[placeholder*='台積電']")
    assert search_input is not None, "Search input not found"

    # Type '2330' and press Enter
    search_input.fill("2330")
    search_input.press("Enter")

    # Wait for navigation to complete: wait for stock name to become visible
    # We'll poll for up to 15 seconds, checking every 0.5 seconds
    def is_stock_name_visible():
        element = page.query_selector("text=台積電")
        if element:
            box = element.bounding_box()
            return box is not None and box['width'] > 0 and box['height'] > 0
        return False

    timeout = 15
    interval = 0.5
    elapsed = 0
    while elapsed < timeout:
        if is_stock_name_visible():
            break
        time.sleep(interval)
        elapsed += interval
    else:
        raise AssertionError("Stock name did not become visible after search")

    # Verify stock ID is visible (should also be visible now)
    stock_id = page.query_selector("text=2330")
    assert stock_id is not None, "Stock ID not found on stock page"

    # Verify that main content is loaded and not empty
    main_content = page.query_selector("[data-testid='stMain']")
    assert main_content is not None, "Main content area not found"
    inner_text = main_content.inner_text()
    assert len(inner_text) > 10, "Main content appears empty"