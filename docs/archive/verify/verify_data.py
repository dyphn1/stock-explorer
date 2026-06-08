"""
Visual verification script for Stock Explorer M1.
Tests data loading for 3 representative stocks: 2330, 2454, 1101.
"""
import sys
import os

# Ensure project root is in path
project_root = "/Users/daniel.chang/Desktop/GitHub/stock-explorer"
os.chdir(project_root)
sys.path.insert(0, project_root)

from src.data.finmind_client import FinMindClient
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import get_one_liner
from src.services.news_summarizer import summarize_news, get_news_impact_level

client = FinMindClient(cache_dir=".cache")

STOCKS = [
    ("2330", "台積電"),
    ("2454", "聯發科"),
    ("1101", "台泥"),
]

results = []

for stock_id, expected_name in STOCKS:
    print(f"\n{'='*60}")
    print(f"Testing {stock_id} ({expected_name})")
    print(f"{'='*60}")

    stock_result = {
        "stock_id": stock_id,
        "expected_name": expected_name,
        "tests": [],
        "errors": [],
    }

    # Test 1: Stock info
    try:
        info = client.get_stock_info(stock_id)
        if len(info) == 0:
            stock_result["errors"].append("Stock info: NOT FOUND")
            print(f"  FAIL Stock info: NOT FOUND")
        else:
            name = info.iloc[0]["stock_name"]
            industry = info.iloc[0]["industry_category"]
            stock_result["tests"].append(f"Stock info: OK - {name} ({industry})")
            print(f"  OK Stock info: {name} ({industry})")
    except Exception as e:
        stock_result["errors"].append(f"Stock info: {e}")
        print(f"  FAIL Stock info: {e}")

    # Test 2: Latest price
    try:
        price = client.get_latest_price(stock_id)
        if price:
            stock_result["tests"].append(f"Price: {price['close']} (change: {price['change']})")
            print(f"  OK Price: {price['close']} (change: {price['change']})")
        else:
            stock_result["tests"].append("Price: No data")
            print(f"  WARN Price: No data")
    except Exception as e:
        stock_result["errors"].append(f"Price: {e}")
        print(f"  FAIL Price: {e}")

    # Test 3: PER/PBR
    try:
        per_pbr = client.get_latest_per_pbr(stock_id)
        if per_pbr:
            per = per_pbr.get("PER")
            pbr = per_pbr.get("PBR")
            dy = per_pbr.get("dividend_yield")
            stock_result["tests"].append(f"PER: {per}, PBR: {pbr}, Dividend: {dy}")
            print(f"  OK PER: {per}, PBR: {pbr}, Dividend: {dy}")
        else:
            stock_result["tests"].append("PER/PBR: No data")
            print(f"  WARN PER/PBR: No data")
    except Exception as e:
        stock_result["errors"].append(f"PER/PBR: {e}")
        print(f"  FAIL PER/PBR: {e}")

    # Test 4: Monthly revenue
    try:
        rev = client.get_monthly_revenue(stock_id)
        if len(rev) > 0:
            latest_rev = rev.iloc[-1]["revenue"] / 1e8
            stock_result["tests"].append(f"Revenue: {latest_rev:.0f} 億 (latest month)")
            print(f"  OK Revenue: {latest_rev:.0f} 億")
        else:
            stock_result["tests"].append("Revenue: No data")
            print(f"  WARN Revenue: No data")
    except Exception as e:
        stock_result["errors"].append(f"Revenue: {e}")
        print(f"  FAIL Revenue: {e}")

    # Test 5: Financial statement
    try:
        fin = client.get_financial_statement(stock_id)
        if fin is not None and len(fin) > 0:
            stock_result["tests"].append(f"Financial: {len(fin)} rows")
            print(f"  OK Financial: {len(fin)} rows")
        else:
            stock_result["tests"].append("Financial: No data")
            print(f"  WARN Financial: No data")
    except Exception as e:
        stock_result["errors"].append(f"Financial: {e}")
        print(f"  FAIL Financial: {e}")

    # Test 6: News
    try:
        news = client.get_news(stock_id)
        if len(news) > 0:
            stock_result["tests"].append(f"News: {len(news)} items")
            print(f"  OK News: {len(news)} items")
            first_title = news.iloc[0]["title"]
            summary = summarize_news(first_title, expected_name)
            impact = get_news_impact_level(first_title)
            print(f"    First news: {first_title[:60]}...")
            print(f"    Summary: {summary[:100]}...")
            print(f"    Impact: {impact}")
        else:
            stock_result["tests"].append("News: No data")
            print(f"  WARN News: No data")
    except Exception as e:
        stock_result["errors"].append(f"News: {e}")
        print(f"  FAIL News: {e}")

    # Test 7: One-liner
    try:
        info = client.get_stock_info(stock_id)
        industry = info.iloc[0]["industry_category"] if len(info) > 0 else ""
        name = info.iloc[0]["stock_name"] if len(info) > 0 else expected_name
        one_liner = get_one_liner(stock_id, name, industry)
        stock_result["tests"].append(f"One-liner: OK")
        print(f"  OK One-liner: {one_liner}")
    except Exception as e:
        stock_result["errors"].append(f"One-liner: {e}")
        print(f"  FAIL One-liner: {e}")

    # Test 8: Revenue breakdown
    try:
        fin = client.get_financial_statement(stock_id)
        info = client.get_stock_info(stock_id)
        industry = info.iloc[0]["industry_category"] if len(info) > 0 else ""
        rev_items = analyze_revenue_breakdown(fin, stock_id, industry)
        if rev_items:
            stock_result["tests"].append(f"Revenue breakdown: {len(rev_items)} items")
            print(f"  OK Revenue breakdown: {len(rev_items)} items")
            for item in rev_items:
                print(f"    - {item['name']}: {item['value']:.0f}% - {item['description'][:50]}")
        else:
            stock_result["tests"].append("Revenue breakdown: No data")
            print(f"  WARN Revenue breakdown: No data")
    except Exception as e:
        stock_result["errors"].append(f"Revenue breakdown: {e}")
        print(f"  FAIL Revenue breakdown: {e}")

    # Test 9: Balance sheet
    try:
        bs = client.get_balance_sheet(stock_id)
        if bs is not None and len(bs) > 0:
            stock_result["tests"].append(f"Balance sheet: {len(bs)} rows")
            print(f"  OK Balance sheet: {len(bs)} rows")
        else:
            stock_result["tests"].append("Balance sheet: No data")
            print(f"  WARN Balance sheet: No data")
    except Exception as e:
        stock_result["errors"].append(f"Balance sheet: {e}")
        print(f"  FAIL Balance sheet: {e}")

    # Test 10: Institutional investors
    try:
        inst = client.get_institutional_investors(stock_id)
        if inst is not None and len(inst) > 0:
            stock_result["tests"].append(f"Institutional: {len(inst)} rows")
            print(f"  OK Institutional: {len(inst)} rows")
        else:
            stock_result["tests"].append("Institutional: No data")
            print(f"  WARN Institutional: No data")
    except Exception as e:
        stock_result["errors"].append(f"Institutional: {e}")
        print(f"  FAIL Institutional: {e}")

    # Test 11: Daily price
    try:
        dp = client.get_daily_price(stock_id)
        if dp is not None and len(dp) > 0:
            stock_result["tests"].append(f"Daily price: {len(dp)} rows")
            print(f"  OK Daily price: {len(dp)} rows")
        else:
            stock_result["tests"].append("Daily price: No data")
            print(f"  WARN Daily price: No data")
    except Exception as e:
        stock_result["errors"].append(f"Daily price: {e}")
        print(f"  FAIL Daily price: {e}")

    results.append(stock_result)

# Summary
print(f"\n{'='*60}")
print("VERIFICATION SUMMARY")
print(f"{'='*60}")

total_tests = 0
total_errors = 0
for r in results:
    stock_errors = len(r["errors"])
    stock_tests = len(r["tests"])
    total_tests += stock_tests
    total_errors += stock_errors
    status = "PASS" if stock_errors == 0 else f"{stock_errors} errors"
    print(f"  {r['stock_id']} ({r['expected_name']}): {stock_tests} tests, {status}")
    for e in r["errors"]:
        print(f"    ERROR: {e}")

print(f"\nTotal: {total_tests} tests, {total_errors} errors across {len(results)} stocks")

# Content safety check
print(f"\n{'='*60}")
print("CONTENT SAFETY CHECK")
print(f"{'='*60}")

investment_keywords = ["買進", "賣出", "建議", "推薦", "投資建議", "買入", "操作建議", "目標價", "停損", "加碼", "減碼"]
found_issues = []

test_companies = [
    ("2330", "台積電", "半導體業"),
    ("2454", "聯發科", "半導體業"),
    ("1101", "台泥", "水泥工業"),
    ("2317", "鴻海", "電子零組件業"),
    ("2308", "台達電", "電子零組件業"),
    ("2881", "富邦金", "金融業"),
    ("2002", "中鋼", "鋼鐵工業"),
    ("1301", "台塑", "塑膠工業"),
]

for sid, name, industry in test_companies:
    try:
        ol = get_one_liner(sid, name, industry)
        for kw in investment_keywords:
            if kw in ol:
                found_issues.append(f"One-liner for {sid} ({name}) contains '{kw}': {ol}")
    except Exception:
        pass

if found_issues:
    print("  WARN Found potential investment advice wording:")
    for issue in found_issues:
        print(f"    - {issue}")
else:
    print("  OK No investment advice wording found in one-liners")

print(f"\nDone.")
