"""Streamlit 頁面渲染驗證 - 導航列深度測試"""
import sys
sys.path.insert(0, '.')

from streamlit.testing.v1 import AppTest

results = []

# 測試：完整 session_state 初始化
print("── 測試: 2330 完整 session_state ──")
try:
    at = AppTest.from_file("src/main.py", default_timeout=30)
    at.session_state["stock_id"] = "2330"
    at.session_state["page"] = "名片"
    at.run()
    
    if at.error:
        for e in at.error:
            results.append(("❌", "2330_full", f"error: {e.value}"))
    
    # 收集所有 markdown 文字
    all_markdown = []
    for m in at.markdown:
        if m.value:
            all_markdown.append(m.value)
    full_text = " ".join(all_markdown)
    
    # 檢查導航元素
    checks = {
        "台積電": "台積電" in full_text,
        "半導體業": "半導體業" in full_text,
        "營運健檢": "營運健檢" in full_text,
        "財務體質": "財務體質" in full_text,
        "同業比較": "同業比較" in full_text,
        "集團架構": "集團架構" in full_text,
        "名片": "名片" in full_text,
        "一句話定位": "一句話" in full_text or "全世界最大" in full_text,
        "營收組成": "營收組成" in full_text or "靠什麼賺錢" in full_text,
        "近期動態": "近期動態" in full_text,
        "免責聲明": "僅供認識" in full_text or "投資有風險" in full_text,
        "FinMind": "FinMind" in full_text or "公開資訊" in full_text,
    }
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        results.append((status, f"check_{check_name}", result))
    
    # 檢查圖表數量
    charts = at.get("plotly_chart") if hasattr(at, "get") else []
    results.append(("ℹ️", "charts_count", f"{len(charts)} charts"))
    
    # 檢查是否有 exception
    if at.exception:
        for exc in at.exception:
            results.append(("❌", "exception", f"{exc.type}: {exc.message}"))
    
    if not at.error and not at.exception:
        results.append(("✅", "2330_full", "no errors, no exceptions"))
    
except Exception as e:
    results.append(("❌", "2330_full", f"{type(e).__name__}: {e}"))

# 輸出
print()
print("=" * 60)
print("導航列深度測試報告")
print("=" * 60)
for status, name, msg in results:
    print(f"  {status} {name}: {msg}")
print("=" * 60)
passed = sum(1 for s, _, _ in results if s == "✅")
failed = sum(1 for s, _, _ in results if s == "❌")
info = sum(1 for s, _, _ in results if s == "ℹ️")
print(f"結果: {passed} 通過, {failed} 失敗, {info} 資訊")
