#!/usr/bin/env bash
# =============================================================================
# Stock Explorer — End-to-End Verification Script
# =============================================================================
# Three gates:
#   Gate 1: Import check — all modules importable
#   Gate 2: Streamlit startup — server starts, all pages render without stException
#   Gate 3: Content smoke test — main page + search returns content
#
# Usage: bash scripts/verify.sh
# Exit code: 0 = all gates pass, 1+ = gate number that failed
# =============================================================================

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if command -v uv >/dev/null 2>&1; then
    USE_UV=true
else
    USE_UV=false
    if [ -f "$PROJECT_DIR/.venv/Scripts/python.exe" ]; then
        PYTHON_CMD="$PROJECT_DIR/.venv/Scripts/python.exe"
    elif [ -f "$PROJECT_DIR/.venv/bin/python" ]; then
        PYTHON_CMD="$PROJECT_DIR/.venv/bin/python"
    else
        PYTHON_CMD="python"
    fi
fi

run_python() {
    if [ "$USE_UV" = true ]; then
        uv run python "$@"
    else
        "$PYTHON_CMD" "$@"
    fi
}

PORT=8501
STREAMLIT_PID=""
REPORT_FILE="$PROJECT_DIR/docs/status/verify_report.md"

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "   $1"; }

# ── Cleanup ─────────────────────────────────────────────────────────────────
cleanup() {
    if [ -n "$STREAMLIT_PID" ] && kill -0 "$STREAMLIT_PID" 2>/dev/null; then
        kill "$STREAMLIT_PID" 2>/dev/null || true
        wait "$STREAMLIT_PID" 2>/dev/null || true
        info "Streamlit stopped (PID $STREAMLIT_PID)"
    fi
}
trap cleanup EXIT

cd "$PROJECT_DIR"

echo "============================================"
echo "  Stock Explorer — Verification"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo ""

# =============================================================================
# Gate 1: Import Check
# =============================================================================
echo "── Gate 1: Import Check ──"

IMPORT_MODULES=(
    "src.main"
    "src.data.finmind_client"
    "src.services.chart"
    "src.services.analogy_engine"
    "src.services.revenue_analyzer"
    "src.services.news_summarizer"
    "src.services.watchlist"
    "src.services.adaptive_engine"
    "src.pages.router"
    "src.pages._router_base"
    "src.pages.business_card"
    "src.pages.operation_checkup"
    "src.pages.financial_health"
    "src.pages.peer_comparison"
    "src.pages.group_structure"
    "src.pages.timeline_controls"
    "src.pages.category_browser"
    "src.pages.etf_browser"
    "src.pages.etf_detail"
    "src.pages.watchlist_page"
    "src.pages.event_dashboard"
)

IMPORT_FAIL=0
for mod in "${IMPORT_MODULES[@]}"; do
    if run_python -c "import $mod" 2>/dev/null; then
        pass "$mod"
    else
        fail "$mod"
        IMPORT_FAIL=$((IMPORT_FAIL + 1))
    fi
done

if [ "$IMPORT_FAIL" -gt 0 ]; then
    echo ""
    fail "Gate 1 FAILED — $IMPORT_FAIL module(s) failed to import"
    exit 1
fi
echo ""
pass "Gate 1 PASSED — all ${#IMPORT_MODULES[@]} modules importable"
echo ""

# =============================================================================
# Gate 2: Streamlit Startup + Page Rendering
# =============================================================================
echo "── Gate 2: Streamlit Startup + Page Rendering ──"

# Kill any existing Streamlit on port 8501
if lsof -i ":$PORT" -t 2>/dev/null | xargs kill -9 2>/dev/null; then
    info "Killed existing process on port $PORT"
    sleep 1
fi

# Check playwright is available
if ! run_python -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    warn "Playwright not installed, installing..."
    if [ "$USE_UV" = true ]; then
        uv add playwright 2>/dev/null || uv pip install playwright 2>/dev/null
    else
        "$PYTHON_CMD" -m pip install playwright 2>/dev/null
    fi
    run_python -m playwright install chromium 2>/dev/null
fi

# Start Streamlit in background
info "Starting Streamlit on port $PORT..."
run_python run.py --server.port "$PORT" --server.headless true 2>/dev/null &
STREAMLIT_PID=$!

# Wait for server to be ready
RETRIES=30
READY=false
for i in $(seq 1 $RETRIES); do
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT" | grep -q "200"; then
        READY=true
        break
    fi
    sleep 1
done

if [ "$READY" = false ]; then
    fail "Streamlit failed to start within ${RETRIES}s"
    exit 2
fi
pass "Streamlit started (PID $STREAMLIT_PID)"

# Use playwright to check each page
info "Checking page rendering with playwright..."

VERIFY_SCRIPT=$(cat <<'PYEOF'
import sys, time
from playwright.sync_api import sync_playwright

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8501
base = f"http://localhost:{port}"

# Pages to check: (url_path, description)
pages = [
    ("/", "Main page"),
    ("/business_card", "Business Card page"),
    ("/operation_checkup", "Operation Checkup page"),
    ("/financial_health", "Financial Health page"),
    ("/peer_comparison", "Peer Comparison page"),
    ("/group_structure", "Group Structure page"),
    ("/category_browser", "Category Browser page"),
    ("/etf_browser", "ETF Browser page"),
    ("/etf_detail", "ETF Detail page"),
    ("/watchlist_page", "Watchlist page"),
    ("/event_dashboard", "Event Dashboard page"),
]

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for path, desc in pages:
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        try:
            page.goto(f"{base}{path}", wait_until="networkidle", timeout=15000)
            time.sleep(2)

            # Check for Streamlit exceptions
            error_el = page.locator('[data-testid="stException"]')
            if error_el.count() > 0:
                error_text = error_el.inner_text()[:200]
                results.append((desc, "FAIL", error_text))
                continue

            # Check page has content (not just sidebar)
            body = page.locator('[data-testid="stAppViewContainer"]')
            text = body.inner_text() if body.count() > 0 else page.locator("body").inner_text()

            # Filter out just sidebar content
            if len(text.strip()) < 50:
                results.append((desc, "WARN", "Page has very little content"))
            else:
                results.append((desc, "PASS", f"{len(text.strip())} chars rendered"))
        except Exception as e:
            results.append((desc, "FAIL", str(e)[:200]))
        finally:
            page.close()
    browser.close()

# Print results
fail_count = 0
for desc, status, detail in results:
    icon = "✅" if status == "PASS" else ("⚠️" if status == "WARN" else "❌")
    print(f"  {icon} {desc}: {status} — {detail}")
    if status == "FAIL":
        fail_count += 1

if fail_count > 0:
    print(f"\n  {fail_count} page(s) failed")
    sys.exit(1)
else:
    print(f"\n  All {len(results)} pages rendered without errors")
    sys.exit(0)
PYEOF
)

if run_python -c "$VERIFY_SCRIPT" "$PORT"; then
    pass "Gate 2 PASSED — all pages render without stException"
else
    fail "Gate 2 FAILED — some pages have errors"
    exit 2
fi
echo ""

# =============================================================================
# Gate 3: Content Smoke Test
# =============================================================================
echo "── Gate 3: Content Smoke Test ──"

SMOKE_SCRIPT=$(cat <<'PYEOF'
import sys, time
from playwright.sync_api import sync_playwright

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8501
base = f"http://localhost:{port}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})

    # Test 1: Main page loads with welcome text
    page.goto(base, wait_until="networkidle", timeout=15000)
    time.sleep(2)
    text = page.locator("body").inner_text()
    if "股識" in text or "認識一家公司" in text:
        print("  ✅ Main page: welcome text found")
    else:
        print("  ❌ Main page: welcome text NOT found")
        sys.exit(1)

    # Test 2: Sidebar has navigation elements
    sidebar = page.locator('[data-testid="stSidebar"]')
    if sidebar.count() > 0:
        sidebar_text = sidebar.inner_text()
        if "熱門股票" in sidebar_text or "搜尋" in sidebar_text:
            print("  ✅ Sidebar: navigation elements found")
        else:
            print("  ⚠️  Sidebar: navigation elements may be missing")
    else:
        print("  ❌ Sidebar: not found")
        sys.exit(1)

    # Test 3: Search box exists
    inputs = page.locator('input[type="text"]')
    if inputs.count() > 0:
        print("  ✅ Search input: found")
    else:
        print("  ❌ Search input: NOT found")
        sys.exit(1)

    browser.close()
    print("\n  All smoke tests passed")
    sys.exit(0)
PYEOF
)

if run_python -c "$SMOKE_SCRIPT" "$PORT"; then
    pass "Gate 3 PASSED — content smoke test OK"
else
    fail "Gate 3 FAILED — content issues detected"
    exit 3
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "============================================"
echo -e "${GREEN}  ALL GATES PASSED ✅${NC}"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"

# Write report
cat > "$REPORT_FILE" <<EOF
# Verification Report

**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Result:** ✅ ALL GATES PASSED

| Gate | Result |
|------|--------|
| Gate 1: Import Check | ✅ ${#IMPORT_MODULES[@]} modules |
| Gate 2: Streamlit + Page Rendering | ✅ All pages render |
| Gate 3: Content Smoke Test | ✅ Main page + sidebar + search |

---
*Auto-generated by scripts/verify.sh*
EOF

exit 0
