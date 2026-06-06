import sys

# Step 1: Page imports
try:
    from src.pages import router, business_card, operation_checkup, financial_health, peer_comparison, group_structure
    print("Step 1 - All page imports OK")
except Exception as e:
    print(f"Step 1 - FAIL: {e}")
    sys.exit(1)

# Step 2: Service imports
try:
    from src.data.finmind_client import FinMindClient
    from src.services.chart import ChartGenerator
    from src.services.analogy_engine import AnalogyEngine
    from src.services.revenue_analyzer import RevenueAnalyzer
    from src.services.news_summarizer import NewsSummarizer
    print("Step 2 - All services OK")
except Exception as e:
    print(f"Step 2 - FAIL: {e}")
    sys.exit(1)

# Step 3: Dependency imports
try:
    import streamlit
    import plotly
    import pandas
    import requests
    print("Step 3 - All deps OK")
except Exception as e:
    print(f"Step 3 - FAIL: {e}")
    sys.exit(1)

# Step 4: FinMind API call
try:
    c = FinMindClient()
    df = c.get_stock_info('2330')
    print(f"Step 4 - FinMind OK: {df.shape if df is not None else 'None'}")
except Exception as e:
    print(f"Step 4 - FAIL: {e}")
    sys.exit(1)

print("\nAll steps passed!")
