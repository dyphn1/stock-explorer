"""M1 驗證腳本 — 確認所有模組可正確載入"""
import ast
import sys

files = [
    'src/main.py',
    'src/data/finmind_client.py',
    'src/services/chart.py',
    'src/services/revenue_analyzer.py',
    'src/services/analogy_engine.py',
    'src/services/news_summarizer.py',
]

print('=== Syntax Check ===')
all_ok = True
for f in files:
    try:
        with open(f) as fh:
            ast.parse(fh.read())
        print(f'  OK: {f}')
    except SyntaxError as e:
        print(f'  FAIL: {f}: {e}')
        all_ok = False

if not all_ok:
    sys.exit(1)

print()
print('=== Import Check ===')
from src.data.finmind_client import FinMindClient
print('  OK: FinMindClient')

from src.services.chart import create_revenue_pie_chart, create_revenue_trend_chart, create_funnel_chart, create_price_chart, create_institutional_chart, create_comparison_radar
print('  OK: chart functions')

from src.services.revenue_analyzer import analyze_revenue_breakdown, KNOWN_COMPANY_REVENUE
print(f'  OK: revenue_analyzer ({len(KNOWN_COMPANY_REVENUE)} companies)')

from src.services.analogy_engine import get_one_liner, get_per_analogy, get_dividend_analogy, get_gross_margin_analogy, get_revenue_analogy, get_yoy_analogy, get_roe_analogy, get_debt_ratio_analogy, get_volume_analogy, get_institutional_analogy, get_pbr_analogy
print('  OK: analogy_engine (11 analogy functions)')

from src.services.news_summarizer import summarize_news, get_news_impact_level
print('  OK: news_summarizer')

print()
print('=== Functional Spot Checks ===')
# Test analogy engine
print(f'  one_liner(2330): {get_one_liner("2330", "台積電", "半導體業")[:40]}...')
print(f'  per_analogy(25): {get_per_analogy(25)}')
print(f'  dividend_analogy(3.5): {get_dividend_analogy(3.5)}')
print(f'  gross_margin_analogy(66): {get_gross_margin_analogy(66)}')
print(f'  roe_analogy(22): {get_roe_analogy(22)}')
print(f'  yoy_analogy(15): {get_yoy_analogy(15)}')

# Test news summarizer
print(f'  summarize_news: {summarize_news("台積電Q3財報亮眼 營收創高", "台積電")[:50]}...')
print(f'  impact(high): {get_news_impact_level("台積電Q3財報亮眼")}')
print(f'  impact(medium): {get_news_impact_level("台積電接獲大單")}')
print(f'  impact(low): {get_news_impact_level("台積電參加展會")}')

# Test revenue analyzer
items = analyze_revenue_breakdown(None, "2330", "半導體業")
print(f'  revenue_breakdown(2330): {len(items)} segments')

print()
print('=== ALL CHECKS PASSED ===')
