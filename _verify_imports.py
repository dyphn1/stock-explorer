"""驗證所有模組能否正確載入"""
import sys
sys.path.insert(0, '.')

results = []

# 1. 測試所有頁面模組 import
modules = [
    ("router", "src.pages.router", "load_and_render_page"),
    ("business_card", "src.pages.business_card", "_render_business_card"),
    ("operation_checkup", "src.pages.operation_checkup", "_render_operation_checkup"),
    ("financial_health", "src.pages.financial_health", "_render_financial_health"),
    ("peer_comparison", "src.pages.peer_comparison", "_render_peer_comparison"),
    ("group_structure", "src.pages.group_structure", "_render_group_structure"),
    ("_router_base", "src.pages._router_base", "get_stock_data"),
]

for name, module_path, func_name in modules:
    try:
        mod = __import__(module_path, fromlist=[func_name])
        getattr(mod, func_name)
        results.append(("✅", name, "import OK"))
    except Exception as e:
        results.append(("❌", name, str(e)))

# 2. 測試服務模組
services = [
    ("chart", "src.services.chart", None),
    ("revenue_analyzer", "src.services.revenue_analyzer", None),
    ("analogy_engine", "src.services.analogy_engine", None),
    ("news_summarizer", "src.services.news_summarizer", None),
    ("finmind_client", "src.data.finmind_client", None),
]

for name, module_path, _ in services:
    try:
        __import__(module_path)
        results.append(("✅", name, "import OK"))
    except Exception as e:
        results.append(("❌", name, str(e)))

# 3. 測試 FinMind client 初始化
try:
    from src.data.finmind_client import FinMindClient
    client = FinMindClient(cache_dir=".cache")
    results.append(("✅", "FinMindClient", "init OK"))
except Exception as e:
    results.append(("❌", "FinMindClient", str(e)))

# 4. 測試資料載入（用 2330 台積電）
try:
    from src.pages._router_base import get_stock_data
    data = get_stock_data(client, "2330")
    if data:
        results.append(("✅", "get_stock_data(2330)", f"name={data.get('stock_name','?')} industry={data.get('industry','?')}"))
    else:
        results.append(("⚠️", "get_stock_data(2330)", "returned None"))
except Exception as e:
    results.append(("❌", "get_stock_data(2330)", str(e)))

# 輸出結果
print("=" * 60)
print("股識 Stock Explorer — 模組驗證報告")
print("=" * 60)
for status, name, msg in results:
    print(f"  {status} {name}: {msg}")
print("=" * 60)
passed = sum(1 for s, _, _ in results if s == "✅")
failed = sum(1 for s, _, _ in results if s == "❌")
warned = sum(1 for s, _, _ in results if s == "⚠️")
print(f"結果: {passed} 通過, {failed} 失敗, {warned} 警告")
