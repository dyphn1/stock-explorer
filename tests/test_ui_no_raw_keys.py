# tests/test_ui_no_raw_keys.py
"""Playwright test to verify no raw t() keys are displayed in the UI.
Focuses on detecting unresolved i18n keys that appear as raw keys like 'main.sidebar.*'.
"""

from urllib.parse import quote
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
    page.goto(f"{streamlit_server}/?page={quote('產業熱力圖')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

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