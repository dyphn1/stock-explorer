"""驗證各頁面渲染邏輯（簡化版）"""
import sys
sys.path.insert(0, '.')

results = []

from src.data.finmind_client import FinMindClient
client = FinMindClient(cache_dir=".cache")
from src.pages._router_base import get_stock_data

# 載入 2330 台積電
data = get_stock_data(client, "2330")
if not data:
    print("❌ 無法載入 2330 資料")
    sys.exit(1)

print(f"✅ 資料載入: {data['stock_name']} ({data['stock_id']}) - {data['industry']}")
print(f"   monthly_revenue: {len(data.get('monthly_revenue', []))} rows")
print(f"   daily_price: {len(data.get('daily_price', []))} rows")
print(f"   institutional: {len(data.get('institutional', []))} rows")
print(f"   financial: {len(data.get('financial', []))} rows")
print(f"   balance_sheet: {len(data.get('balance_sheet', []))} rows")
print(f"   cash_flow: {len(data.get('cash_flow', []))} rows")
print(f"   news: {len(data.get('news', []))} items")
print()

# 測試 analogy_engine 各函數
print("── analogy_engine 測試 ──")
from src.services.analogy_engine import *
try:
    r = get_one_liner("2330", "台積電", "半導體業")
    print(f"✅ get_one_liner: {r}")
except Exception as e:
    print(f"❌ get_one_liner: {e}")

try:
    r = get_revenue_analogy(300000000000)
    print(f"✅ get_revenue_analogy: {r[:50]}...")
except Exception as e:
    print(f"❌ get_revenue_analogy: {e}")

try:
    r = get_yoy_analogy(15.5)
    print(f"✅ get_yoy_analogy(15.5%): {r}")
except Exception as e:
    print(f"❌ get_yoy_analogy: {e}")

try:
    r = get_gross_margin_analogy(55.0)
    print(f"✅ get_gross_margin_analogy(55%): {r}")
except Exception as e:
    print(f"❌ get_gross_margin_analogy: {e}")

try:
    r = get_roe_analogy(25.0)
    print(f"✅ get_roe_analogy(25%): {r}")
except Exception as e:
    print(f"❌ get_roe_analogy: {e}")

try:
    r = get_debt_ratio_analogy(35.0)
    print(f"✅ get_debt_ratio_analogy(35%): {r}")
except Exception as e:
    print(f"❌ get_debt_ratio_analogy: {e}")

try:
    r = get_per_analogy(20.0)
    print(f"✅ get_per_analogy(20x): {r}")
except Exception as e:
    print(f"❌ get_per_analogy: {e}")

try:
    r = get_pbr_analogy(3.0)
    print(f"✅ get_pbr_analogy(3x): {r}")
except Exception as e:
    print(f"❌ get_pbr_analogy: {e}")

try:
    r = get_dividend_analogy(3.5)
    print(f"✅ get_dividend_analogy(3.5%): {r}")
except Exception as e:
    print(f"❌ get_dividend_analogy: {e}")

print()

# 測試 revenue_analyzer
print("── revenue_analyzer 測試 ──")
try:
    from src.services.revenue_analyzer import analyze_revenue_breakdown
    rev = data.get("monthly_revenue", [])
    if rev:
        bd = analyze_revenue_breakdown(rev)
        print(f"✅ analyze_revenue_breakdown: {type(bd).__name__}")
    else:
        print(f"⚠️ no revenue data to analyze")
except Exception as e:
    print(f"❌ analyze_revenue_breakdown: {e}")

print()

# 測試 news_summarizer
print("── news_summarizer 測試 ──")
try:
    from src.services.news_summarizer import summarize_news, get_news_impact_level
    news = data.get("news", [])
    if news:
        s = summarize_news(news[:3])
        imp = get_news_impact_level(news[0])
        print(f"✅ summarize_news: {len(s)} chars, impact={imp}")
    else:
        print(f"⚠️ no news data")
except Exception as e:
    print(f"❌ news_summarizer: {e}")

print()

# 測試 chart 模組
print("── chart 模組測試 ──")
try:
    from src.services.chart import (
        create_revenue_trend_chart, create_revenue_pie_chart,
        create_price_chart, create_institutional_chart,
        create_funnel_chart, create_comparison_radar
    )
    print(f"✅ all chart functions imported")
    
    # 實際生成圖表
    rev = data.get("monthly_revenue", [])
    if rev:
        fig = create_revenue_trend_chart(rev)
        print(f"✅ create_revenue_trend_chart: {type(fig).__name__}")
    
    dp = data.get("daily_price", [])
    if dp:
        fig = create_price_chart(dp)
        print(f"✅ create_price_chart: {type(fig).__name__}")
    
    inst = data.get("institutional", [])
    if inst:
        fig = create_institutional_chart(inst)
        print(f"✅ create_institutional_chart: {type(fig).__name__}")
    
    fin = data.get("financial", [])
    if fin:
        fig = create_funnel_chart(fin)
        print(f"✅ create_funnel_chart: {type(fig).__name__}")

except Exception as e:
    print(f"❌ chart: {e}")

print()

# 測試多股票
print("── 多股票資料測試 ──")
for sid in ["2330", "2454", "1101"]:
    try:
        d = get_stock_data(client, sid)
        if d:
            print(f"✅ {sid}: {d['stock_name']} ({d['industry']})")
        else:
            print(f"⚠️ {sid}: no data")
    except Exception as e:
        print(f"❌ {sid}: {e}")

print()
print("=" * 60)
print("驗證完成")
