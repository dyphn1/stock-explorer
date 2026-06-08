"""Check if FinMind is importable from .venv."""
import sys
import os

# Set up path
project_root = "/Users/daniel.chang/Desktop/GitHub/stock-explorer"
os.chdir(project_root)
sys.path.insert(0, project_root)

# Try importing
try:
    from FinMind.data import DataLoader
    print("FinMind: OK")
except ImportError as e:
    print(f"FinMind: FAILED - {e}")

try:
    import streamlit
    print(f"Streamlit: OK (v{streamlit.__version__})")
except ImportError as e:
    print(f"Streamlit: FAILED - {e}")

try:
    import plotly
    print(f"Plotly: OK")
except ImportError as e:
    print(f"Plotly: FAILED - {e}")

try:
    import pandas
    print(f"Pandas: OK")
except ImportError as e:
    print(f"Pandas: FAILED - {e}")

# Now test the client
try:
    from src.data.finmind_client import FinMindClient
    client = FinMindClient(cache_dir=".cache")
    print("FinMindClient: OK")
    
    # Quick test
    info = client.get_stock_info("2330")
    if len(info) > 0:
        print(f"Stock info test: OK - {info.iloc[0]['stock_name']}")
    else:
        print("Stock info test: No data")
except Exception as e:
    print(f"FinMindClient: FAILED - {e}")
