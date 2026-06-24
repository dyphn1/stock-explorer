"""Take screenshot of welcome/main page for visual audit."""
import subprocess, time, socket, sys, os, signal, json
from playwright.sync_api import sync_playwright

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Find free port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', 0))
    port = s.getsockname()[1]

env = os.environ.copy()
env["STREAMLIT_SERVER_HEADLESS"] = "true"
env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

script_path = os.path.join(project_root, "src", "main.py")
proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", script_path,
     "--server.port", str(port),
     "--server.headless", "true",
     "--browser.gatherUsageStats", "false",
     "--server.enableCORS", "false",
     "--server.enableXsrfProtection", "false"],
    env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    cwd=project_root,
)

for _ in range(40):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', port))
            break
    except ConnectionRefusedError:
        time.sleep(0.5)
else:
    proc.terminate()
    raise RuntimeError("Streamlit server failed to start")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"http://localhost:{port}")
        page.wait_for_load_state("networkidle")
        time.sleep(4)

        out_dir = os.path.dirname(os.path.abspath(__file__))

        # Full page screenshot
        page.screenshot(path=os.path.join(out_dir, "welcome_full.png"), full_page=True)
        print(f"✅ Saved: welcome_full.png")

        # Viewport screenshot
        page.screenshot(path=os.path.join(out_dir, "welcome_viewport.png"))
        print(f"✅ Saved: welcome_viewport.png")

        # Extract visible text for i18n audit
        body_text = page.locator("body").inner_text()
        text_path = os.path.join(out_dir, "welcome_text.txt")
        with open(text_path, "w") as f:
            f.write(body_text)
        print(f"✅ Saved: welcome_text.txt")

        # Extract page HTML structure
        html = page.content()
        html_path = os.path.join(out_dir, "welcome_html.txt")
        with open(html_path, "w") as f:
            f.write(html[:50000])
        print(f"✅ Saved: welcome_html.txt")

        # Check for raw i18n keys in visible text
        bad_patterns = ['main.', 'sidebar.', 'app.', 'page.', 'daily_market.', 'screener.',
                        'health.', 'moat.', 'risk.', 'event_dashboard.', 'investment_memo.',
                        'metric_education.', 'business_card.', 'notification_center.',
                        'financial_wellness.', 'stock_screener.', 'case_study.']
        found_bad = []
        for pattern in bad_patterns:
            elements = page.query_selector_all(f"text={pattern}")
            if elements:
                for el in elements:
                    text = el.text_content()
                    if text and pattern in text:
                        found_bad.append(text.strip()[:80])

        if found_bad:
            print(f"\n❌ Raw i18n keys FOUND ({len(found_bad)}):")
            for b in found_bad[:15]:
                print(f"   - {b}")
        else:
            print("\n✅ No raw i18n keys found on welcome page")

        browser.close()
finally:
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
