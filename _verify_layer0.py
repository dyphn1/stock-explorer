"""
Layer 0 — 語法 + Import + Key 唯一性驗證
目標：< 5 秒，無 API 呼叫，純粹靜態檢查
"""
import ast
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
RESULTS = []


def record(status, name, msg):
    RESULTS.append((status, name, msg))


# ── 1. 語法檢查 ──────────────────────────────────────────
print("── 1. 語法檢查 ──")
py_files = sorted(SRC_DIR.rglob("*.py"))
syntax_ok = True
for py_file in py_files:
    try:
        ast.parse(py_file.read_text(encoding="utf-8"))
        record("✅", "syntax", py_file.relative_to(PROJECT_ROOT))
    except SyntaxError as e:
        record("❌", "syntax", f"{py_file.relative_to(PROJECT_ROOT)}: {e}")
        syntax_ok = False

if syntax_ok:
    print(f"  ✅ {len(py_files)} 個檔案語法正確")
else:
    print("  ❌ 有語法錯誤")


# ── 2. Import 檢查 ───────────────────────────────────────
print("── 2. Import 檢查 ──")
sys.path.insert(0, str(PROJECT_ROOT))

MODULES = [
    # 頁面
    ("router", "src.pages.router"),
    ("business_card", "src.pages.business_card"),
    ("operation_checkup", "src.pages.operation_checkup"),
    ("financial_health", "src.pages.financial_health"),
    ("peer_comparison", "src.pages.peer_comparison"),
    ("group_structure", "src.pages.group_structure"),
    ("category_browser", "src.pages.category_browser"),
    ("etf_browser", "src.pages.etf_browser"),
    ("etf_detail", "src.pages.etf_detail"),
    ("watchlist_page", "src.pages.watchlist_page"),
    ("event_dashboard", "src.pages.event_dashboard"),
    ("_router_base", "src.pages._router_base"),
    ("revenue_tree", "src.pages.revenue_tree"),
    ("compare_stories", "src.pages.compare_stories"),
    # 服務
    ("chart", "src.services.chart"),
    ("analogy_engine", "src.services.analogy_engine"),
    ("revenue_analyzer", "src.services.revenue_analyzer"),
    ("news_summarizer", "src.services.news_summarizer"),
    ("adaptive_engine", "src.services.adaptive_engine"),
    # 資料
    ("finmind_client", "src.data.finmind_client"),
    # 依賴
    ("streamlit", "streamlit"),
    ("plotly", "plotly"),
    ("pandas", "pandas"),
]

for name, module_path in MODULES:
    try:
        __import__(module_path)
        record("✅", "import", name)
    except ImportError as e:
        record("❌", "import", f"{name}: {e}")

imported = sum(1 for item in RESULTS if item[0] == "✅" and item[1] == "import")
print(f"  ✅ {imported}/{len(MODULES)} 個模組 import 成功")


# ── 3. 按鈕 Key 唯一性掃描 ───────────────────────────────
print("── 3. 按鈕 Key 唯一性掃描 ──")

# 掃描所有 key= 模式
key_pattern = re.compile(r'key\s*=\s*f["\']([^"\']+)["\']')
key_literal_pattern = re.compile(r'key\s*=\s*["\']([^"\']+)["\']')

all_keys = {}  # key_str -> [file:line]

for py_file in py_files:
    try:
        lines = py_file.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue
    rel = str(py_file.relative_to(PROJECT_ROOT))
    for lineno, line in enumerate(lines, 1):
        for m in key_pattern.finditer(line):
            key_str = m.group(1)
            # 跳過含變數的 f-string（如 f"val_{sid}"）— 這些是動態 key
            if "{" in key_str:
                continue
            all_keys.setdefault(key_str, []).append(f"{rel}:{lineno}")
        for m in key_literal_pattern.finditer(line):
            key_str = m.group(1)
            all_keys.setdefault(key_str, []).append(f"{rel}:{lineno}")

# 找出重複的靜態 key
dup_keys = {k: v for k, v in all_keys.items() if len(v) > 1}
if dup_keys:
    for key, locations in sorted(dup_keys.items()):
        record("❌", "dup_key", f'"{key}" 出現在 {len(locations)} 處: {", ".join(locations[:3])}')
    print(f"  ❌ 發現 {len(dup_keys)} 個重複的靜態 key")
else:
    record("✅", "dup_key", "無重複靜態 key")
    print("  ✅ 無重複靜態 key")

# 掃描動態 key 前綴（找出可能衝突的前綴）
dynamic_prefixes = {}  # prefix -> [file:line:raw_key]
for py_file in py_files:
    try:
        lines = py_file.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue
    rel = str(py_file.relative_to(PROJECT_ROOT))
    for lineno, line in enumerate(lines, 1):
        for m in key_pattern.finditer(line):
            key_str = m.group(1)
            if "{" not in key_str:
                continue
            # 提取前綴（{ 之前的部分）
            prefix = key_str.split("{")[0]
            if prefix:
                dynamic_prefixes.setdefault(prefix, []).append(
                    f"{rel}:{lineno}: {key_str}"
                )

# 檢查是否有「同一前綴在不同檔案中可能產生相同 key」的情況
# 例如 f"val_{row['stock_id']}" 在 category_browser 中，如果 stock_id 重複就會衝突
# 這需要執行時才能完全檢測，但我們可以標記「在同一檔案中多次出現相同前綴」的情況
for prefix, locations in sorted(dynamic_prefixes.items()):
    if len(locations) > 5:  # 同一前綴出現超過 5 次，可能是迴圈中產生
        record("⚠️", "key_prefix",
               f'前綴 "{prefix}" 出現 {len(locations)} 次（可能在迴圈中），請確認 key 在執行時唯一')
        print(f"  ⚠️ 前綴 \"{prefix}\" 出現 {len(locations)} 次")

if not any(s == "⚠️" and _ == "key_prefix" for s, _, _ in RESULTS):
    print("  ✅ 動態 key 前綴看起來正常")


# ── 4. 分層架構檢查 ──────────────────────────────────────
print("── 4. 分層架構檢查 ──")

# 檢查 service 層沒有 import streamlit
SERVICE_DIR = SRC_DIR / "services"
layer_violations = False
for py_file in SERVICE_DIR.glob("*.py"):
    try:
        content = py_file.read_text(encoding="utf-8")
    except Exception:
        continue
    # 允許 type checking 時的 import
    lines = content.splitlines()
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "import streamlit" in stripped or "from streamlit" in stripped:
            if "TYPE_CHECKING" not in content[:200]:  # 粗略檢查
                record("❌", "layer",
                       f"{py_file.name}:{lineno} — service 層不應 import streamlit")
                layer_violations = True

# 檢查 data 層沒有 import streamlit
DATA_DIR = SRC_DIR / "data"
for py_file in DATA_DIR.glob("*.py"):
    try:
        content = py_file.read_text(encoding="utf-8")
    except Exception:
        continue
    lines = content.splitlines()
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "import streamlit" in stripped or "from streamlit" in stripped:
            record("❌", "layer",
                   f"{py_file.name}:{lineno} — data 層不應 import streamlit")
            layer_violations = True

if not layer_violations:
    record("✅", "layer", "分層架構正確（data/service 層無 streamlit 依賴）")
    print("  ✅ 分層架構正確")


# ── 報告 ─────────────────────────────────────────────────
print()
print("=" * 60)
print("Layer 0 — 靜態驗證報告")
print("=" * 60)
passed = sum(1 for s, _, _ in RESULTS if s == "✅")
failed = sum(1 for s, _, _ in RESULTS if s == "❌")
warned = sum(1 for s, _, _ in RESULTS if s == "⚠️")
print(f"結果: {passed} 通過, {failed} 失敗, {warned} 警告")
print()

if failed > 0:
    print("失敗項目：")
    for s, n, m in RESULTS:
        if s == "❌":
            print(f"  ❌ [{n}] {m}")
    print()

if warned > 0:
    print("警告項目：")
    for s, n, m in RESULTS:
        if s == "⚠️":
            print(f"  ⚠️ [{n}] {m}")
    print()

if failed > 0:
    sys.exit(1)
