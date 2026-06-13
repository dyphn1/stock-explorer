"""
Layer 1 — AppTest 渲染驗證
目標：確認所有頁面在所有情境下都能渲染，無 exception、無 error
使用 streamlit.testing.v1.AppTest（不需要 Playwright）

注意：此驗證依賴 FinMind API cache。如果 cache 過期且 API rate limit，
      會標記為 ⚠️（警告）而非 ❌（失敗）。
"""
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from streamlit.testing.v1 import AppTest

RESULTS = []
API_RATE_LIMITED = False


def record(status, name, msg):
    RESULTS.append((status, name, msg))


def run_test(test_name, stock_id=None, page=None, expect_error=False, timeout=60):
    """執行單次 AppTest，檢查 error 和 exception"""
    global API_RATE_LIMITED
    print(f"  ── {test_name} ──")
    try:
        at = AppTest.from_file("src/main.py", default_timeout=timeout)
        if stock_id is not None:
            at.session_state["stock_id"] = stock_id
        if page is not None:
            at.session_state["page"] = page
        at.run()

        # 檢查 exception
        if at.exception:
            for exc in at.exception:
                exc_msg = exc.message[:300]
                # 偵測 API rate limit
                if "Requests reach the upper limit" in exc_msg:
                    API_RATE_LIMITED = True
                    record("⚠️", test_name, f"API rate limit（非程式碼問題）")
                    return None  # None = skip/uncertain
                record("❌", test_name, f"EXCEPTION: {exc.type}: {exc_msg}")
            return False

        # 檢查 error
        if at.error:
            for e in at.error:
                if expect_error:
                    record("✅", test_name, f"預期錯誤: {e.value[:100]}")
                else:
                    record("❌", test_name, f"ERROR: {e.value[:200]}")
            return expect_error

        record("✅", test_name, "renders OK")
        return True

    except Exception as e:
        error_msg = str(e)[:300]
        if "Requests reach the upper limit" in error_msg:
            API_RATE_LIMITED = True
            record("⚠️", test_name, f"API rate limit（非程式碼問題）")
            return None
        record("❌", test_name, f"CRASH: {type(e).__name__}: {error_msg}")
        return False


def run_test_safe(test_name, stock_id=None, page=None, expect_error=False, timeout=60):
    """如果已偵測到 API rate limit，自動 skip"""
    if API_RATE_LIMITED:
        record("⚠️", test_name, "SKIP（API rate limit）")
        print(f"  ⏭️ {test_name}: SKIP（API rate limit）")
        return None
    return run_test(test_name, stock_id=stock_id, page=page,
                    expect_error=expect_error, timeout=timeout)


print("=" * 60)
print("Layer 1 — AppTest 渲染驗證")
print("=" * 60)

# ── 1. 歡迎頁面（無 stock_id）────────────────────────────
print("\n── 群組 1: 歡迎頁面 ──")
run_test("welcome", stock_id=None)

# ── 2. 各股票的名片頁 ────────────────────────────────────
print("\n── 群組 2: 各股票名片頁 ──")
for sid in ["2330", "2454", "1101", "2317"]:
    run_test_safe(f"business_card_{sid}", stock_id=sid, page="名片")

# ── 3. 各頁面的渲染（用 2330）────────────────────────────
print("\n── 群組 3: 各頁面渲染（2330 台積電）──")
PAGES = [
    "名片", "營運健檢", "財務體質", "同業比較", "集團架構",
    "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板",
    "營收結構樹", "同業比較故事",
]
for page_name in PAGES:
    if page_name in ("分類瀏覽", "ETF 專區", "我的關注", "事件儀表板"):
        run_test_safe(f"page_{page_name}", stock_id=None, page=page_name, timeout=30)
    else:
        run_test_safe(f"page_{page_name}", stock_id="2330", page=page_name, timeout=60)

# ── 4. ETF 頁面 ──────────────────────────────────────────
print("\n── 群組 4: ETF 頁面 ──")
run_test_safe("etf_0050", stock_id="0050", page="名片", timeout=60)

# ── 5. 無效股票代碼 ──────────────────────────────────────
print("\n── 群組 5: 錯誤處理 ──")
run_test_safe("invalid_stock", stock_id="9999", page="名片", expect_error=True)

# ── 6. 多股票切換 ────────────────────────────────────────
print("\n── 群組 6: 多股票切換 ──")
if API_RATE_LIMITED:
    record("⚠️", "switch_2330_to_2454", "SKIP（API rate limit）")
    print("  ⏭️ switch_2330_to_2454: SKIP（API rate limit）")
else:
    print("  ── switch_2330_to_2454 ──")
    try:
        at = AppTest.from_file("src/main.py", default_timeout=60)
        at.session_state["stock_id"] = "2330"
        at.session_state["page"] = "名片"
        at.run()
        at.session_state["stock_id"] = "2454"
        at.run()
        if at.exception:
            for exc in at.exception:
                record("❌", "switch_2330_to_2454",
                       f"EXCEPTION: {exc.type}: {exc.message[:200]}")
        elif at.error:
            for e in at.error:
                record("❌", "switch_2330_to_2454", f"ERROR: {e.value[:200]}")
        else:
            record("✅", "switch_2330_to_2454", "switch OK")
    except Exception as e:
        record("❌", "switch_2330_to_2454",
               f"CRASH: {type(e).__name__}: {str(e)[:200]}")

# ── 7. category_browser 特別測試 ──────────────────────────
print("\n── 群組 7: category_browser 特別測試 ──")
# DuplicateElementKey 已由 Layer 0 的 key 掃描覆蓋
# 這裡只確認頁面不會因為 API 問題而 crash
if API_RATE_LIMITED:
    record("⚠️", "category_browser_render", "SKIP（API rate limit）")
    print("  ⏭️ category_browser_render: SKIP（API rate limit）")
else:
    print("  ── category_browser_render ──")
    try:
        at = AppTest.from_file("src/main.py", default_timeout=120)
        at.session_state["page"] = "分類瀏覽"
        at.run()
        if at.exception:
            for exc in at.exception:
                exc_msg = exc.message[:300]
                if "DuplicateElementKey" in exc_msg:
                    record("❌", "category_browser_dup_key",
                           f"DuplicateElementKey: {exc_msg}")
                else:
                    record("❌", "category_browser_render",
                           f"EXCEPTION: {exc.type}: {exc_msg}")
        elif at.error:
            for e in at.error:
                record("❌", "category_browser_render", f"ERROR: {e.value[:200]}")
        else:
            record("✅", "category_browser_render", "renders OK")
    except Exception as e:
        error_msg = str(e)[:300]
        if "DuplicateElementKey" in error_msg:
            record("❌", "category_browser_dup_key",
                   f"DuplicateElementKey: {error_msg}")
        else:
            record("❌", "category_browser_render",
                   f"CRASH: {type(e).__name__}: {error_msg}")

# ── 報告 ─────────────────────────────────────────────────
print()
print("=" * 60)
print("Layer 1 — AppTest 渲染驗證報告")
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
    print("警告項目（通常為 API rate limit，非程式碼問題）：")
    for item in RESULTS:
        if item[0] == "⚠️":
            print(f"  ⚠️ [{item[1]}] {item[2]}")
    print()

if failed > 0:
    sys.exit(1)
