"""
Layer 2 — Playwright 互動驗證
目標：模擬真實使用者操作，確認互動功能正常

需要：playwright（uv add playwright && uv run playwright install chromium）
"""
import sys
import time
import subprocess
import signal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS = []


def record(status, name, msg):
    RESULTS.append((status, name, msg))


# ── 檢查 Playwright 是否可用 ─────────────────────────────
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def start_streamlit():
    """啟動 Streamlit server，回傳 (process, url)"""
    proc = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "src/main.py",
         "--server.port", "8502",
         "--server.headless", "true",
         "--global.showWarningOnDirectQuery", "false"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(PROJECT_ROOT),
        preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL),
    )
    # 等待 server 啟動
    time.sleep(5)
    return proc, "http://localhost:8502"


def stop_streamlit(proc):
    """停止 Streamlit server"""
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


if not PLAYWRIGHT_AVAILABLE:
    record("⚠️", "playwright_check",
           "Playwright 未安裝。安裝方式：uv add playwright && uv run playwright install chromium")
    print("⚠️ Playwright 未安裝，Layer 2 無法執行")
    print("   安裝方式：uv add playwright && uv run playwright install chromium")
    # 不 exit(1)，因為這是可選的 layer
    sys.exit(0)

# ── 互動測試 ─────────────────────────────────────────────
print("=" * 60)
print("Layer 2 — Playwright 互動驗證")
print("=" * 60)

proc = None
try:
    print("\n▶ 啟動 Streamlit server...")
    proc, url = start_streamlit()
    print(f"  Server URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # 收集 console errors
        console_errors = []
        page.on("console", lambda msg: (
            console_errors.append(f"[{msg.type}] {msg.text}")
            if msg.type == "error" else None
        ))

        # ── Test 1: 頁面載入 ──────────────────────────────
        print("\n  ── test_page_load ──")
        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=30000)
            title = page.title()
            if "股識" in title or "Stock" in title:
                record("✅", "page_load", f"頁面載入成功，title={title}")
            else:
                record("✅", "page_load", f"頁面載入成功（title={title}）")
        except PlaywrightTimeout:
            record("❌", "page_load", "頁面載入超時（30s）— 可能卡死")
        except Exception as e:
            record("❌", "page_load", f"頁面載入失敗: {e}")

        # ── Test 2: 側邊欄功能 ─────────────────────────────
        print("  ── test_sidebar ──")
        try:
            # 等待側邊欄載入
            page.wait_for_selector("text=股識", timeout=15000)

            # 測試搜尋框
            search_input = page.query_selector("input[placeholder*='股票']")
            if search_input:
                search_input.fill("2330")
                search_input.press("Enter")
                page.wait_for_load_state("networkidle", timeout=15000)
                # 確認有載入股票
                page.wait_for_selector("text=台積電", timeout=15000)
                record("✅", "sidebar_search", "搜尋功能正常")
            else:
                record("⚠️", "sidebar_search", "找不到搜尋框（可能頁面結構已變）")

            # 測試側邊欄收起/展開
            # Streamlit 預設會顯示 sidebar toggle button
            sidebar_toggle = page.query_selector("button[title='展開側邊欄'], button[aria-label*='sidebar'], [data-testid='collapsedControl']")
            if sidebar_toggle:
                sidebar_toggle.click()
                time.sleep(1)
                # 展開
                expand_btn = page.query_selector("button[title='展開側邊欄'], [data-testid='collapsedControl']")
                if expand_btn:
                    expand_btn.click()
                    time.sleep(1)
                    record("✅", "sidebar_toggle", "側邊欄收起/展開正常")
                else:
                    record("⚠️", "sidebar_toggle", "找不到展開按鈕")
            else:
                record("⚠️", "sidebar_toggle", "找不到側邊欄 toggle 按鈕")

        except PlaywrightTimeout:
            record("❌", "sidebar", "側邊欄操作超時")
        except Exception as e:
            record("❌", "sidebar", f"側邊欄操作失敗: {e}")

        # ── Test 3: 頁面切換 ──────────────────────────────
        print("  ── test_page_navigation ──")
        try:
            # 等待頁面載入
            page.wait_for_selector("text=營運健檢", timeout=15000)

            # 點擊「營運健檢」
            start_time = time.time()
            page.click("text=營運健檢", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=15000)
            elapsed = time.time() - start_time

            if elapsed > 10:
                record("⚠️", "page_nav_latency",
                       f"頁面切換耗時 {elapsed:.1f}s（> 5s 可能感覺卡）")
            else:
                record("✅", "page_nav_latency",
                       f"頁面切換耗時 {elapsed:.1f}s（正常）")

            # 檢查內容有變
            page.wait_for_selector("text=營收", timeout=10000)
            record("✅", "page_nav_content", "頁面切換後內容正確更新")

            # 切換回名片
            page.click("text=名片", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=15000)

        except PlaywrightTimeout:
            record("❌", "page_navigation", "頁面切換超時（可能卡死）")
        except Exception as e:
            record("❌", "page_navigation", f"頁面切換失敗: {e}")

        # ── Test 4: Console Error 檢查 ─────────────────────
        print("  ── test_console_errors ──")
        # 等待一下讓 console 訊息有時間被記錄
        time.sleep(3)

        js_errors = [e for e in console_errors if "error" in e.lower()]
        if js_errors:
            for err in js_errors[:5]:  # 最多顯示 5 個
                record("⚠️", "console_error", err[:200])
        else:
            record("✅", "console_errors", "無 JS console error")

        # ── Test 5: 側邊欄熱門股票點擊 ─────────────────────
        print("  ── test_hot_stock_click ──")
        try:
            # 回到歡迎頁面
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=15000)

            # 等待熱門股票按鈕
            page.wait_for_selector("text=2330 台積電", timeout=15000)
            page.click("text=2330 台積電", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=15000)

            # 確認已跳轉到股票頁面
            page.wait_for_selector("text=台積電", timeout=15000)
            record("✅", "hot_stock_click", "熱門股票點擊跳轉正常")

        except PlaywrightTimeout:
            record("❌", "hot_stock_click", "熱門股票點擊後頁面未載入")
        except Exception as e:
            record("❌", "hot_stock_click", f"熱門股票點擊失敗: {e}")

        browser.close()

except Exception as e:
    record("❌", "playwright_setup", f"Playwright 設定失敗: {e}")
    print(f"❌ Playwright 錯誤: {e}")

finally:
    if proc:
        print("\n▶ 停止 Streamlit server...")
        stop_streamlit(proc)

# ── 報告 ─────────────────────────────────────────────────
print()
print("=" * 60)
print("Layer 2 — Playwright 互動驗證報告")
print("=" * 60)

passed = sum(1 for item in RESULTS if item[0] == "✅")
failed = sum(1 for item in RESULTS if item[0] == "❌")
warned = sum(1 for item in RESULTS if item[0] == "⚠️")
print(f"結果: {passed} 通過, {failed} 失敗, {warned} 警告")
print()

if failed > 0:
    print("失敗項目：")
    for item in RESULTS:
        if item[0] == "❌":
            print(f"  ❌ [{item[1]}] {item[2]}")
    print()

if warned > 0:
    print("警告項目：")
    for item in RESULTS:
        if item[0] == "⚠️":
            print(f"  ⚠️ [{item[1]}] {item[2]}")
    print()

if failed > 0:
    sys.exit(1)
