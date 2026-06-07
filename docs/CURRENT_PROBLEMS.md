# Stock Explorer — Comprehensive Project Problem Analysis Report

After conducting an in-depth breakdown of the project's architecture, data flow, and UI implementation (via three rounds of review and cross-verification), several potential issues have been identified that could severely impact stability, performance, and scalability. The current issues are categorized into three different review dimensions below:

## Layer 1: Data Flow & Architecture

1. **API Abuse and Cache Design Flaws in `get_stock_info`**
   - **Problem**: `FinMindClient.get_stock_info(stock_id)` internally calls `taiwan_stock_info()` to fetch the entire list of Taiwanese stocks, and only then filters it by `stock_id`. However, the cache key is generated based on the `stock_id`. This means that if 50 different stocks are queried, the program will send 50 requests to the FinMind API for the full stock list. This extremely wastes bandwidth and easily triggers FinMind's rate limit.
   - **Impact**: A severe performance bottleneck; querying multiple stocks will inevitably cause lag or get blocked.
2. **Daily Cache Invalidation and Missing Cleanup Mechanism**
   - **Problem**: When `FinMindClient._fetch_or_cache` calls the API, the `end_date` parameter defaults to `datetime.now().strftime("%Y-%m-%d")`. This causes the cache's hash key to change every day (after midnight), rendering the configured `cache_ttl_hours` completely useless. Furthermore, old JSON cache files are never deleted.
   - **Impact**: A guaranteed daily cache miss, and the `.cache/` directory size will expand indefinitely.
3. **Ineffective Name Search Support**
   - **Problem**: The sidebar search box explicitly suggests "Example: 2330 or TSMC", but the underlying filtering logic in `FinMindClient` is only searching by `stock_id`, completely lacking support for exact or fuzzy matching on the `stock_name` column.
   - **Impact**: If a user inputs a Chinese stock name, they will always receive a "Stock ID not found" error message.

## Layer 2: Business Logic & UI/UX

1. **Streamlit Widget Key Conflict Risk (`event_dashboard.py`)**
   - **Problem**: The keys generated for buttons in the event dashboard use the format `key=f"evt_{stock_id}_{title[:20]}"`. If a single company has two news articles with the same first 20 characters in their titles on the same day, or triggers two identical events, it will raise a `DuplicateWidgetID` error.
   - **Impact**: Once triggered, this will directly cause the entire page to crash.
2. **Failed ETF Determination Logic (`watchlist.py`)**
   - **Problem**: The `_is_etf(stock_id, name)` function is called inside `add_to_watchlist`, but the most critical third parameter, `industry_category`, is not passed. This prevents the highest-priority exact matching mechanism from executing, forcing it to fall back on less reliable name-based heuristic matching and stock ID prefix matching.
   - **Impact**: This easily leads to certain ETFs being misclassified as regular stocks, directing them to the wrong analysis framework.
3. **Unhandled API Rate Limit Edge Cases**
   - **Problem**: If the FinMind API rate limit is reached, it returns an empty DataFrame or throws an exception. The current program uniformly treats these scenarios as "No data found" or "Stock not found", without providing the user with a clear "API rate limit exceeded" warning.
   - **Impact**: Increases debugging difficulty and results in a poor user experience.
4. **Crude Annualization of Financial Indicators like ROE (`financial_health.py`)**
   - **Problem**: In `_calc_roe`, the quarterly net income is simply multiplied by 4 (`net_income * 4 / equity * 100`). This can cause extremely misleading results for companies with high seasonal variances.
   - **Impact**: Causes the financial data presentation to lose professionalism and easily leads to misestimation.

## Layer 3: Concurrency & Robustness

1. **Race Condition Risks in YAML Config Files (`watchlist.py` / `adaptive_engine.py`)**
   - **Problem**: Reading and writing the watchlist (`watchlist.yaml`) and event records (`events.yaml`) both use a "read entire list -> modify memory array -> overwrite entire file" pattern. Streamlit allows concurrent operations from multiple users (multi-session). If two users add to the watchlist simultaneously, or if a background event detection triggers concurrently, race conditions will occur, causing data loss or YAML file corruption.
   - **Impact**: A fatal risk under high-frequency access, leading to the collapse of the storage system.
2. **Event Detection Relies on Fragile Data Field Access**
   - **Problem**: Methods like `detect_revenue_event` access arrays and dictionaries directly (e.g., `latest["revenue"]`). If FinMind changes its return fields, or if there are fewer than 13 records but another bug somehow leads execution to this logic block, it will raise a `KeyError` or `IndexError`.
   - **Impact**: The background analysis engine halts randomly, failing to generate event alerts.
3. **Silent Failures in the Timeline Filter (`_router_base.py`)**
   - **Problem**: If `filter_by_timeline` encounters formatting anomalies (Exceptions) during time conversion or comparison, it directly returns the original DataFrame (ALL).
   - **Impact**: When users click the 1Y or 3Y filters, the charts won't respond, and no error message is provided, making users mistakenly think the system is lagging.

---
*Summary: The project functions smoothly under the "Happy Path", but when facing scalability, error handling, and concurrency, the underlying infrastructure (especially the cache algorithm and YAML persistence layer) is extremely fragile. Refactoring API access and implementing file locking mechanisms should be prioritized.*