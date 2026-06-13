"""
No Inline HTML — unsafe_allow_html=True 洩漏檢查
目標：禁止使用 inline HTML（unsafe_allow_html=True），允許既有共用元件暫時列入豁免清單。
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

# ── 豁免清單 ────────────────────────────────────────────────
# key: 檔案（相對於 PROJECT_ROOT）
# value: 允許的出現次數上限（0 = 不允許），或 "all" = 全部允許
ALLOWLIST: dict[str, int | str] = {
    # 路由器共用工具與元件（內部有自行 construct safe HTML 的 justifications）
    "src/pages/_router_base.py": "all",
}

# 掃描
pattern = re.compile(r"unsafe_allow_html\s*=\s*True")

violations: list[tuple[str, int, str]] = []

py_files = sorted(SRC_DIR.rglob("*.py"))
for py_file in py_files:
    rel = str(py_file.relative_to(PROJECT_ROOT))
    try:
        lines = py_file.read_text(encoding="utf-8").splitlines()
    except Exception:
        continue

    allowed = ALLOWLIST.get(rel, 0)
    if allowed == "all":
        continue

    max_allowed = allowed if isinstance(allowed, int) else 0

    count_in_file = 0
    for lineno, line in enumerate(lines, 1):
        if pattern.search(line):
            count_in_file += 1
            occurrence_index = count_in_file
            if occurrence_index > max_allowed:
                violations.append((rel, lineno, line.strip()))

# ── 報告 ────────────────────────────────────────────────────
print("=" * 60)
print("No Inline HTML — unsafe_allow_html=True 洩漏檢查")
print("=" * 60)
print()

if ALLOWLIST:
    print("豁免清單：")
    for f, limit in ALLOWLIST.items():
        print(f"  ✅ {f}（{'全部允許' if limit == 'all' else f'允許 {limit} 次'}）")
    print()

print(f"掃描檔案數: {len(py_files)}")
print(f"違規數: {len(violations)}")
print()

if violations:
    print("違規項目：")
    for rel, lineno, code in violations:
        print(f"  ❌ {rel}:{lineno}  —  {code}")
    print()
    print("✗ 檢查未通過 — 請移除 unsafe_allow_html=True 或更新豁免清單。")
    sys.exit(1)
else:
    print("✅ 無違規 — 所有 unsafe_allow_html=True 皆在豁免清單中。")
    sys.exit(0)
