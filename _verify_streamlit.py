"""Streamlit 頁面渲染驗證 - 完整測試"""
import sys
sys.path.insert(0, '.')

from streamlit.testing.v1 import AppTest

results = []

# 測試 1: 歡迎頁面（無股票代碼）
print("── 測試 1: 歡迎頁面 ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "welcome", f"error: {e.value}"))
    else:
        results.append(("✅", "welcome", "renders OK"))
        # 檢查關鍵元素
        has_title = any("股識" in m.value for m in at.markdown if m.value)
        has_disclaimer = any("投資有風險" in m.value for m in at.markdown if m.value)
        has_search = any("快速瀏覽" in m.value for m in at.markdown if m.value)
        results.append(("ℹ️", "welcome", f"has_title={has_title}, has_disclaimer={has_disclaimer}, has_search={has_search}"))
except Exception as e:
    results.append(("❌", "welcome", f"{type(e).__name__}: {e}"))

# 測試 2: 有股票代碼的頁面（模擬 session_state）
print("── 測試 2: 2330 台積電頁面 ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.session_state["stock_id"] = "2330"
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "2330", f"error: {e.value}"))
    else:
        results.append(("✅", "2330", "renders OK"))
        
        # 檢查關鍵元素
        all_text = " ".join([m.value for m in at.markdown if m.value])
        has_name = "台積電" in all_text
        has_nav = "營運健檢" in all_text or "財務體質" in all_text
        has_disclaimer = "投資有風險" in all_text or "僅供認識" in all_text
        results.append(("ℹ️", "2330", f"has_name={has_name}, has_nav={has_nav}, has_disclaimer={has_disclaimer}"))
        
        # 檢查是否有圖表
        has_charts = len(at.get("plotly_chart")) > 0 if hasattr(at, "get") else "N/A"
        results.append(("ℹ️", "2330", f"charts={has_charts}"))
        
except Exception as e:
    results.append(("❌", "2330", f"{type(e).__name__}: {e}"))

# 測試 3: 2454 聯發科
print("── 測試 3: 2454 聯發科頁面 ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.session_state["stock_id"] = "2454"
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "2454", f"error: {e.value}"))
    else:
        results.append(("✅", "2454", "renders OK"))
except Exception as e:
    results.append(("❌", "2454", f"{type(e).__name__}: {e}"))

# 測試 4: 1101 台泥
print("── 測試 4: 1101 台泥頁面 ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.session_state["stock_id"] = "1101"
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "1101", f"error: {e.value}"))
    else:
        results.append(("✅", "1101", "renders OK"))
except Exception as e:
    results.append(("❌", "1101", f"{type(e).__name__}: {e}"))

# 測試 5: 無效股票代碼
print("── 測試 5: 無效股票代碼 ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.session_state["stock_id"] = "9999"
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "invalid", f"error: {e.value}"))
    else:
        # 應該顯示錯誤訊息
        all_text = " ".join([m.value for m in at.markdown if m.value])
        has_error = "找不到" in all_text or "error" in all_text.lower()
        results.append(("✅", "invalid", f"handles invalid stock, has_error_msg={has_error}"))
except Exception as e:
    results.append(("❌", "invalid", f"{type(e).__name__}: {e}"))

# 輸出
print()
print("=" * 60)
print("Streamlit 頁面渲染驗證報告")
print("=" * 60)
for status, name, msg in results:
    print(f"  {status} {name}: {msg}")
print("=" * 60)
passed = sum(1 for s, _, _ in results if s == "✅")
failed = sum(1 for s, _, _ in results if s == "❌")
info = sum(1 for s, _, _ in results if s == "ℹ️")
print(f"結果: {passed} 通過, {failed} 失敗, {info} 資訊")
