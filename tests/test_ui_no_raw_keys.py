# tests/test_ui_no_raw_keys.py
"""Playwright test to verify no raw t() keys are displayed in the UI.
Focuses on detecting unresolved i18n keys that appear as raw keys like 'main.sidebar.*'.
"""

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_no_raw_i18n_keys_on_main_page(streamlit_server, page):
    """Check that the main page doesn't contain raw i18n keys."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Wait for Streamlit to render

    # List of known raw i18n key prefixes that should not appear in visible text
    bad_patterns = [
        'main.sidebar.',
        'page.',
        'business_card.',
        'app.',
        'daily_market.',
        'screener.'
    ]
    found_bad = []
    for pattern in bad_patterns:
        elements = page.query_selector_all(f"text={pattern}")
        if elements:
            found_bad.append(pattern)

    assert not found_bad, f"Raw i18n key prefixes found on main page: {found_bad}"


def test_no_raw_i18n_keys_on_sector_page(streamlit_server, page):
    """Check that the sector heatmap page doesn't contain raw i18n keys."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)  # Wait for initial render

    # Wait for sidebar to be present
    sidebar = page.wait_for_selector("[data-testid='stSidebar']", timeout=5000)
    assert sidebar is not None, "Sidebar not found"

    # Try to find the sector heatmap link in the sidebar
    sector_link = None
    # Try Chinese text first, then English
    sector_link = sidebar.query_selector("text=產業熱力圖")
    if not sector_link:
        sector_link = sidebar.query_selector("text=Sector Heatmap")

    if sector_link:
        sector_link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
    else:
        # If we can't find the sector link, we'll just stay on the main page and check again
        # but we already checked the main page, so we'll skip to avoid duplication.
        # Instead, we'll try to find any other sidebar link and click it.
        # Let's click the first link we find in the sidebar.
        links = sidebar.query_selector_all("a")
        if links:
            links[0].click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
        else:
            # No links found, we'll just check the main page again (though redundant)
            pass

    # Now check for raw i18n keys on the current page
    bad_patterns = [
        'main.sidebar.',
        'page.',
        'business_card.',
        'app.',
        'daily_market.',
        'screener.'
    ]
    found_bad = []
    for pattern in bad_patterns:
        elements = page.query_selector_all(f"text={pattern}")
        if elements:
            found_bad.append(pattern)

    assert not found_bad, f"Raw i18n key prefixes found on page: {found_bad}"