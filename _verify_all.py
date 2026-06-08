"""
_verify_all.py — 依序執行所有驗證 Layer

用法：uv run python _verify_all.py [--skip-l2]

流程：
  Layer 0（靜態）：語法 + import + 分層檢查 + key 掃描
  Layer 1（渲染）：AppTest 所有頁面渲染
  Layer 2（互動）：Playwright 側邊欄 + 頁面切換 + console error

輸出：_summary_report.md
"""
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_PATH = PROJECT_ROOT / "_verify_summary.md"

SKIP_L2 = "--skip-l2" in sys.argv


def run_layer(script_name, timeout=300):
    """執行驗證 script，回傳 (exit_code, stdout, stderr, elapsed)"""
    start = time.time()
    try:
        result = subprocess.run(
            ["uv", "run", "python", script_name],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - start
        return result.returncode, result.stdout, result.stderr, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return -1, "", f"TIMEOUT after {timeout}s", elapsed


# ── 執行 ─────────────────────────────────────────────────
print("=" * 60)
print("股識 Stock Explorer — 完整驗證")
print(f"開始時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

LAYERS = [
    ("Layer 0: 靜態驗證", "_verify_layer0.py", 30),
    ("Layer 1: 渲染驗證", "_verify_layer1.py", 300),
]

if not SKIP_L2:
    # 檢查 Playwright 是否可用
    check = subprocess.run(
        ["uv", "run", "python", "-c", "import playwright; print('ok')"],
        capture_output=True, text=True, timeout=10, cwd=str(PROJECT_ROOT),
    )
    if check.returncode == 0:
        LAYERS.append(("Layer 2: 互動驗證", "_verify_layer2.py", 120))
    else:
        print("\n⚠️ Playwright 未安裝，跳過 Layer 2")
        print("   安裝方式：uv add playwright && uv run playwright install chromium\n")

results_summary = []

for layer_name, script, timeout in LAYERS:
    print(f"\n{'─' * 60}")
    print(f"▶ {layer_name} ({script})")
    print(f"{'─' * 60}")

    exit_code, stdout, stderr, elapsed = run_layer(script, timeout=timeout)
    print(stdout)
    if stderr:
        print(f"  [stderr] {stderr[:500]}")

    status = "✅ PASS" if exit_code == 0 else f"❌ FAIL (exit={exit_code})"
    if exit_code == -1:
        status = "⏰ TIMEOUT"

    results_summary.append({
        "layer": layer_name,
        "script": script,
        "status": status,
        "elapsed": f"{elapsed:.1f}s",
        "exit_code": exit_code,
    })

# ── 報告 ─────────────────────────────────────────────────
overall_pass = all(r["exit_code"] == 0 for r in results_summary)

report_lines = [
    "# 股識 Stock Explorer — 驗證報告",
    f"",
    f"**時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"**結果**：{'✅ 全部通過' if overall_pass else '❌ 有失敗項目'}",
    f"",
    "## 摘要",
    "",
    "| Layer | Script | 狀態 | 耗時 |",
    "|-------|--------|------|------|",
]

for r in results_summary:
    report_lines.append(
        f"| {r['layer']} | `{r['script']}` | {r['status']} | {r['elapsed']} |"
    )

report_lines.extend([
    "",
    "## 詳細結果",
    "",
])

for r in results_summary:
    report_lines.extend([
        f"### {r['layer']}",
        f"",
        f"- **狀態**：{r['status']}",
        f"- **耗時**：{r['elapsed']}",
        f"- **Exit Code**：{r['exit_code']}",
        f"",
    ])

report_lines.extend([
    "---",
    f"*由 _verify_all.py 自動生成*",
])

REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

print()
print("=" * 60)
print("完整驗證報告")
print("=" * 60)
for r in results_summary:
    print(f"  {r['status']}  {r['layer']} ({r['elapsed']})")
print()
print(f"報告已寫入：{REPORT_PATH}")
print()

if not overall_pass:
    sys.exit(1)
