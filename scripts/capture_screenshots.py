"""
Capture screenshots of all key pages for visual QA.
Run Streamlit first: uv run streamlit run src/main.py --server.port 8501 --server.headless true
"""
import time
import subprocess
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Run: uv add playwright && uv run playwright install chromium")
    exit(1)

SCREENSHOTS_DIR = Path("docs/screenshots/verify")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Pages to capture: (url_suffix, filename, description)
PAGES = [
    ("", "01_welcome.png", "Welcome page (no stock selected)"),
    ("?stock_id=2330", "02_business_card_2330.png", "TSMC business card"),
    ("?stock_id=2330&page=營運健檢", "03_operation_checkup.png", "Operational checkup page"),
    ("?stock_id=2330&page=財務體質", "04_financial_health.png", "Financial health page"),
    ("?stock_id=2330&page=同業比較", "05_peer_comparison.png", "Peer comparison page"),
    ("?stock_id=2317", "06_business_card_2317.png", "Foxconn business card"),
    ("?stock_id=0050", "07_etf_0050.png", "ETF 0050 detail page"),
    ("?page=分類瀏覽", "08_category_browser.png", "Category browser page"),
    ("?page=我的關注", "09_watchlist.png", "Watchlist page"),
    ("?page=	event_dashboard", "10_event_dashboard.png", "Event dashboard page"),
]

# Sidebar states to capture
SIDEBAR_STATES = [
    ("", "11_sidebar_expanded.png", "Sidebar expanded"),
    ("", "12_sidebar_collapsed.png", "Sidebar collapsed"),
]

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        for suffix, filename, description in PAGES:
            url = f"http://localhost:8501/{suffix}"
            print(f"Capturing: {description} → {filename}")
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(3)  # Wait for data to load
                page.screenshot(path=str(SCREENSHOTS_DIR / filename), full_page=True)
                print(f"  ✅ Saved: {SCREENSHOTS_DIR / filename}")
            except Exception as e:
                print(f"  ❌ Failed: {e}")

        # Capture mobile viewport
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto("http://localhost:8501/?stock_id=2330", timeout=30000, wait_until="domcontentloaded")
        time.sleep(3)
        page.screenshot(path=str(SCREENSHOTS_DIR / "13_mobile_375px.png"), full_page=True)
        print(f"  ✅ Saved: {SCREENSHOTS_DIR / '13_mobile_375px.png'}")

        # Capture dark mode
        page.set_viewport_size({"width": 1280, "height": 900})
        # Note: Streamlit dark mode is triggered by system preference or st config
        # For now, capture light mode only

        browser.close()

    print(f"\n✅ All screenshots saved to {SCREENSHOTS_DIR}/")
    print("Next step: Delegate to QA Engineer (vision model) for analysis")

if __name__ == "__main__":
    capture_screenshots()
