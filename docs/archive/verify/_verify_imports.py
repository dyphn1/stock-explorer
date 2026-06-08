"""Verify that main.py can be imported without errors (syntax check)."""
import ast
import sys

# Parse and verify syntax
with open("src/main.py", "r") as f:
    source = f.read()

try:
    ast.parse(source)
    print("✅ main.py syntax OK")
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")
    sys.exit(1)

# Check all imports resolve
import subprocess
result = subprocess.run(
    [sys.executable, "-c", """
import sys
sys.path.insert(0, '.')
from src.data.finmind_client import FinMindClient
from src.services.chart import (
    create_revenue_trend_chart,
    create_revenue_pie_chart,
    create_price_chart,
    create_funnel_chart,
    create_institutional_chart,
)
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_pbr_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_debt_ratio_analogy,
    get_volume_analogy,
    get_institutional_analogy,
)
from src.services.news_summarizer import summarize_news, get_news_impact_level
print("All imports OK")
"""],
    capture_output=True, text=True
)
if result.returncode == 0:
    print(result.stdout.strip())
else:
    print(f"❌ Import error: {result.stderr}")
    sys.exit(1)

print("✅ All checks passed!")
