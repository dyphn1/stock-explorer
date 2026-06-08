"""Screenshot all pages of the Stock Explorer app."""
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    
    # Go to main page
    page.goto("http://localhost:8501", wait_until="networkidle")
    time.sleep(3)
    page.screenshot(path="/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/screenshots/01_main.png", full_page=False)
    print("✅ Screenshot: main page")
    
    # Get page content to understand structure
    content = page.content()
    
    # Find all clickable elements in sidebar
    sidebar = page.locator("[data-testid='stSidebar']")
    sidebar_text = sidebar.inner_text() if sidebar.count() > 0 else "NO SIDEBAR FOUND"
    print(f"Sidebar content:\n{sidebar_text[:500]}")
    
    # Find all links
    links = page.locator("a")
    count = links.count()
    print(f"\nFound {count} links:")
    for i in range(count):
        text = links.nth(i).inner_text()
        href = links.nth(i).get_attribute("href") or ""
        print(f"  [{i}] '{text}' -> {href}")
    
    # Find all buttons
    buttons = page.locator("button")
    bcount = buttons.count()
    print(f"\nFound {bcount} buttons:")
    for i in range(min(bcount, 20)):
        text = buttons.nth(i).inner_text()
        print(f"  [{i}] '{text}'")
    
    # Find radio buttons (Streamlit sidebar nav is often radio)
    radios = page.locator("[data-baseweb='radio']")
    rcount = radios.count()
    print(f"\nFound {rcount} radio buttons:")
    for i in range(rcount):
        text = radios.nth(i).inner_text()
        print(f"  [{i}] '{text}'")
    
    browser.close()
    print("\nDone!")
