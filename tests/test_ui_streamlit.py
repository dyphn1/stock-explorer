"""
tests/test_ui_streamlit.py
UI automation tests for Stock Explorer using Playwright.
Verifies that Streamlit page renders correctly with proper translations.
"""
import pytest
import subprocess
import time
import socket
import signal
import os
import sys
pytest.importorskip('playwright')
from playwright.sync_api import sync_playwright

# ── Streamlit server management ──────────────────────────────

def find_free_port():
    """Find a free port for Streamlit."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def streamlit_server():
    """Start Streamlit server for testing, stop after tests complete."""
    port = find_free_port()
    env = os.environ.copy()
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/main.py",
         "--server.port", str(port),
         "--server.headless", "true",
         "--browser.gatherUsageStats", "false",
         "--server.enableCORS", "false",
         "--server.enableXsrfProtection", "false"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    # Wait for server to start
    for _ in range(60):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))
                break
        except ConnectionRefusedError:
            time.sleep(0.5)
    else:
        proc.terminate()
        raise RuntimeError(f"Streamlit server failed to start on port {port}")

    yield f"http://localhost:{port}"

    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=30)


@pytest.fixture(scope="module")
def browser():
    """Launch headless browser."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each test."""
    page = browser.new_page()
    yield page
    page.close()


# ── Page rendering tests ──────────────────────────────────────

def test_page_title_and_welcome_message(streamlit_server, page):
    """Verify welcome page shows translated Chinese strings, not raw i18n keys."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)  # Wait for Streamlit to fully render

    # Check that translated title appears
    assert page.query_selector("text=股識") is not None, "Translated title not found"

    # Should NOT show raw i18n keys
    raw_keys = ["main.home.title", "main.home.lead1", "main.home.lead2",
                "main.disclaimer", "sidebar.search_header"]
    for key in raw_keys:
        el = page.query_selector(f"text={key}")
        assert el is None, f"Found raw i18n key on page: {key}"


def test_search_box_present(streamlit_server, page):
    """Verify search input box is rendered."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    search_input = page.query_selector("input[placeholder*='台積電']")
    assert search_input is not None, "Search input box not found"


def test_welcome_subtitle_below_search(streamlit_server, page):
    """Verify welcome subtitle appears below search box (not above)."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    search_box = page.query_selector("input[placeholder*='台積電']")
    subtitle = page.query_selector("text=認識一家公司，從這裡開始")

    assert search_box is not None, "Search box not found"
    assert subtitle is not None, "Welcome subtitle not found"

    search_y = search_box.bounding_box()["y"]
    subtitle_y = subtitle.bounding_box()["y"]

    assert subtitle_y > search_y, \
        f"Subtitle (y={subtitle_y}) should be below search box (y={search_y})"


def test_no_navigation_header(streamlit_server, page):
    """Verify navigation_header is removed (issue #3)."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    nav_header = page.query_selector("text=導覽")
    assert nav_header is None, "navigation_header still present on page"


def test_disclaimer_present(streamlit_server, page):
    """Verify disclaimer is displayed with correct Chinese text."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    disclaimer = page.query_selector("text=本工具僅供認識公司使用")
    assert disclaimer is not None, "Disclaimer not found or not in Chinese"


def test_no_raw_i18n_keys_on_page(streamlit_server, page):
    """General check: no raw i18n key patterns should be visible on page."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    page_content = page.content()

    # These patterns in visible text indicate unresolved t() keys
    # (locale file key names appearing as raw text)
    bad_patterns = ['main.', 'sidebar.', 'app.', 'daily_market.', 'screener.']
    found_bad = []
    for pattern in bad_patterns:
        elements = page.query_selector_all(f"text={pattern}")
        if elements:
            found_bad.append(pattern)

    assert not found_bad, f"Raw i18n key prefixes found on page: {found_bad}"


# ── Screenshot test ──────────────────────────────────────────

def test_screenshot_welcome_page(streamlit_server, page, tmp_path):
    """Take screenshot of welcome page for visual regression."""
    page.goto(streamlit_server)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    screenshot_path = tmp_path / "welcome_page.png"
    page.screenshot(path=str(screenshot_path))

    assert screenshot_path.exists(), "Screenshot not saved"
    assert screenshot_path.stat().st_size > 1000, "Screenshot too small (likely blank)"
