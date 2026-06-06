"""Screenshot script for Streamlit verification."""
import subprocess
import sys
import time
import os

def check_playwright():
    result = subprocess.run(
        [sys.executable, "-c", "from playwright.sync_api import sync_playwright; print('ok')"],
        capture_output=True, text=True, timeout=10
    )
    return result.returncode == 0

def screenshot_with_playwright():
    screenshots_dir = "/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    stocks = [
        ("2330", "tsmc"),
        ("2454", "mediatek"),
        ("1101", "taicheng"),
    ]
    
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for stock_id, name in stocks:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            url = f"http://localhost:8501?stock_id={stock_id}"
            page.goto(url, wait_until="networkidle", timeout=30000)
            time.sleep(5)
            
            screenshot_path = f"{screenshots_dir}/{name}_{stock_id}.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved: {screenshot_path}")
            page.close()
        
        browser.close()

def check_page_content():
    import urllib.request
    
    try:
        req = urllib.request.urlopen("http://localhost:8501", timeout=10)
        content = req.read().decode("utf-8", errors="replace")
        return {
            "status": req.status,
            "content_length": len(content),
            "has_streamlit": "streamlit" in content.lower(),
            "has_stock_explorer": "股識" in content or "stock" in content.lower(),
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if check_playwright():
        print("Playwright available, taking screenshots...")
        screenshot_with_playwright()
    else:
        print("Playwright not available, checking page content...")
        result = check_page_content()
        print(result)
