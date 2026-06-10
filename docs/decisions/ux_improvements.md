# UI/UX Improvement Proposals

> Analysis date: 2026-06-08
> Analyst: Frontend/UX Agent
> Scope: Layer 4 UI/UX issues from `docs/status/current_problems.md` (14 issues)

---

## Issue 1: Sidebar Search Does Not Support Chinese Stock Names

- **Category**: Navigation
- **Severity**: P1 (Usability)
- **Current Behavior**: The sidebar search box placeholder says "例如：2330 或 台積電", but the search input is passed directly as `stock_id` to `load_and_render_page()` in `main.py` (line 147). The `FinMindClient.get_stock_info()` method (line 86 of `finmind_client.py`) only filters by `stock_id` column (`df[df["stock_id"] == stock_id]`). Typing "台積電" always returns "找不到股票代號 台積電".
- **Proposed Behavior**: Implement a two-phase search: first try exact match on `stock_id`, then fall back to matching against `stock_name` (Chinese name) in the `taiwan_stock_info` DataFrame. Return the matched `stock_id` to the router. Additionally, support fuzzy/partial matching (e.g., "台積" matches "台積電").
- **UX Rationale**: The placeholder text explicitly promises Chinese name support. Taiwanese users naturally think in Chinese stock names. Breaking this promise on the very first interaction creates immediate distrust and forces users to look up stock codes elsewhere — a critical onboarding failure.
- **Affected Components**: `src/main.py` (search input handling, lines 79-83, 147), `src/data/finmind_client.py` (`get_stock_info`, lines 77-86)
- **Implementation Notes**:
  - In `FinMindClient`, add a method `search_stock(query: str) -> str | None` that:
    1. First checks `stock_id == query`
    2. Then checks `stock_name == query` (exact)
    3. Then checks `stock_name.contains(query)` (partial, for inputs ≥ 2 chars)
    4. Returns the matched `stock_id` or `None`
  - In `main.py`, replace the direct `search_input.strip()` assignment with a call to `client.search_stock(search_input.strip())`
  - Show `st.error(f"找不到「{query}」，請輸入股票代號或完整名稱")` if no match
  - Cache the full `taiwan_stock_info` DataFrame as a class attribute to avoid re-fetching on every keystroke

---

## Issue 2: No Loading Indicator When Switching Pages

- **Category**: Navigation
- **Severity**: P1 (Usability)
- **Current Behavior**: When users click sidebar hot-stock buttons, navbar tabs, or the watchlist button, `st.session_state` is set and `st.rerun()` is called immediately. The page goes blank during data loading (which can take 5-15 seconds for API calls). No spinner or progress indicator is shown during this time. The DESIGN_SYSTEM.md (Section 4.1) explicitly requires loading states, but they are not implemented in the main navigation flow.
- **Proposed Behavior**: Wrap `load_and_render_page()` in `router.py` with a `st.spinner()` that shows contextual messages (e.g., "正在載入台積電資料..."). For sidebar navigation, show a brief inline spinner. For tab switching, show a progress bar at the top of Zone C.
- **UX Rationale**: Without loading feedback, users cannot distinguish between "app is working" and "app is frozen". This violates the DESIGN_SYSTEM requirement that "the screen must not freeze for more than 0.5 seconds without any feedback." Users may click multiple times, causing duplicate requests.
- **Affected Components**: `src/main.py` (lines 147-162), `src/pages/router.py` (`load_and_render_page`, lines 59-115), `src/pages/_router_base.py` (`get_stock_data`, lines 11-48)
- **Implementation Notes**:
  - In `router.py`, wrap the `get_stock_data()` call (line 77) with `with st.spinner(f"正在載入 {stock_id} 資料..."):`
  - For navbar tab switching, the `st.rerun()` approach means the entire page re-renders. Add a `st.session_state["loading"] = True` flag before `st.rerun()`, and at the top of `load_and_render_page`, check for this flag and show a `st.progress_bar` animation
  - Consider using `st.status()` for a more informative loading state that can show sub-steps ("取得股價... / 取得營收... / 取得財務資料...")

---

## Issue 3: Browser Back Button Does Not Work with Streamlit Page Navigation

- **Category**: Navigation
- **Severity**: P1 (Usability)
- **Current Behavior**: Page navigation uses `st.session_state["page"]` + `st.rerun()`. This does not update the URL query string, so the browser's back button cannot navigate through page history. Users lose their navigation context.
- **Proposed Behavior**: Use `st.query_params` to reflect the current page and stock_id in the URL (e.g., `?stock=2330&page=名片`). On page load, read from query params to restore state. This enables native browser back/forward navigation.
- **UX Rationale**: Browser back button is a fundamental navigation expectation. Power users especially rely on it. Streamlit's `st.query_params` (available since Streamlit 1.30) supports this pattern. Without it, users must re-navigate from the sidebar every time.
- **Affected Components**: `src/main.py` (search and navigation), `src/pages/router.py` (all navigation buttons, lines 136-145), all page files with navigation controls
- **Implementation Notes**:
  - On app startup, read `st.query_params` to initialize `session_state["stock_id"]` and `session_state["page"]`
  - After each `st.rerun()`, also call `st.query_params.update(stock_id=..., page=...)`
  - Handle the `popstate` browser event via a small JS snippet injected with `st.markdown(..., unsafe_allow_html=True)` if native query param sync is insufficient
  - Note: This is a known Streamlit limitation; full SPA-style routing requires `st.navigation()` (Streamlit 1.35+) or a custom component

---

## Issue 4: Financial Charts Show No Data Points When Only a Single Period Is Available

- **Category**: Data Display
- **Severity**: P1 (Usability)
- **Current Behavior**: In `chart.py`, `create_revenue_trend_chart()` (line 54) uses `make_subplots` with a bar chart + YoY line. The YoY calculation uses `pct_change(periods=12)`, which requires 13+ rows. If only 1-12 periods exist, the YoY subplot shows empty. More critically, `create_price_chart()` (line 117) uses `go.Candlestick` which requires `open`, `high`, `low`, `close` columns — if any are missing or if only 1 row exists, the chart may render but appear empty or broken. The funnel chart (line 180) filters out zero/negative values and shows "暫無財務資料" if all values are invalid.
- **Proposed Behavior**: 
  - For single-period data: show a bar chart instead of a line chart, with a clear annotation "僅有一期資料，無法顯示趨勢"
  - For candlestick with < 5 rows: fall back to a simple line chart of `close` price with a note "資料期間較短，以折線圖顯示"
  - Always show at least the available data with a contextual note, never an empty chart area
- **UX Rationale**: An empty chart area violates the PPT-style principle ("charts must occupy > 60% of the page area"). Users see a blank space and assume the app is broken. Showing available data with a note is always better than showing nothing.
- **Affected Components**: `src/services/chart.py` (all chart functions), `src/pages/financial_health.py` (chart rendering), `src/pages/business_card.py` (revenue trend chart)
- **Implementation Notes**:
  - In `create_revenue_trend_chart`: if `len(df) < 13`, skip the YoY subplot and show only the revenue bar chart with a note
  - In `create_price_chart`: if `len(df) < 5`, use `go.Scatter` with `close` instead of `go.Candlestick`
  - Add a helper `_data_availability_note(n_rows, min_required)` that returns a consistent Chinese annotation string
  - Ensure all chart functions return a valid `go.Figure` even with minimal data

---

## Issue 5: ROE Annualization Produces Wildly Inaccurate Values for Seasonal Businesses

- **Category**: Data Display
- **Severity**: P1 (Usability)
- **Current Behavior**: `_calc_roe()` in `financial_health.py` (line 295) and `_get_benchmark_data()` in `peer_comparison.py` (line 208) both use `net_income * 4 / equity * 100` to annualize quarterly net income. This simple multiplication by 4 assumes uniform quarterly earnings, which is wildly inaccurate for seasonal businesses (e.g., retail peaks in Q4, semiconductor seasonality). A retail company with Q1 net income of 100M would show an annualized ROE based on 400M, when the actual annual net income might be 800M.
- **Proposed Behavior**: 
  - Use trailing twelve months (TTM) net income: sum the last 4 quarters of net income instead of multiplying the latest quarter by 4
  - If fewer than 4 quarters are available, use the available quarters but add a disclaimer: "基於 {n} 季資料年化，可能與實際年度數字有差異"
  - For known seasonal industries (retail, tourism, food), add an additional note: "該公司所屬產業具季節性，季度數字波動較大"
- **UX Rationale**: ROE is one of the most important metrics for beginners. Showing an annualized ROE of 45% when the actual is 12% is not just inaccurate — it's misleading and could shape wrong impressions. The DESIGN_SYSTEM principle states "Correctness > Clarity > Completeness > Aesthetics."
- **Affected Components**: `src/pages/financial_health.py` (`_calc_roe`, lines 275-299), `src/pages/peer_comparison.py` (`_get_benchmark_data`, lines 203-208)
- **Implementation Notes**:
  - Modify `_calc_roe` to accept the full `financial_df` (not just filtered) and compute TTM net income:
    ```python
    # Sort by date descending, take last 4 quarters
    quarterly_incomes = financial_df[financial_df["type"].str.contains("淨利|Net Income")].sort_values("date").tail(4)
    ttm_net_income = quarterly_incomes["value"].sum()
    ```
  - If only 1-3 quarters available, use what's available with a warning annotation
  - Add a `seasonal_industries` list and check `industry` against it for the seasonal note
  - Update the ROE card display to show "ROE (TTM)" instead of just "ROE" for clarity

---

## Issue 6: Peer Comparison Page Shows "No Data" for Stocks Outside Top Tier Without Explanation

- **Category**: Data Display
- **Severity**: P1 (Usability)
- **Current Behavior**: In `peer_comparison.py` (lines 87-95), if the stock's `industry` is not found in `INDUSTRY_BENCHMARKS`, the page shows a generic warning "「{industry}」目前沒有設定標竿公司" and prompts for a manual benchmark ID. If the user doesn't enter one, the page returns early with no comparison data. Additionally, `_get_benchmark_data()` (line 166) can return `None` if the benchmark stock has no financial data, showing only "無法載入標竿公司資料" with no further guidance.
- **Proposed Behavior**:
  - Expand `INDUSTRY_BENCHMARKS` to cover all common Taiwanese stock industries (currently only ~25 entries)
  - When no benchmark is configured, auto-select the benchmark as the stock with the largest market cap in the same industry (requires fetching industry peers from FinMind)
  - When benchmark data fails to load, show a fallback: "無法取得標竿資料，以下僅顯示 {stock_name} 的指標" and render the single-company metrics
  - Always show at least the target company's data, even if comparison fails
- **UX Rationale**: Showing a dead-end page with no data violates the PPT-style principle. Users should always see something useful. The current flow punishes users for being interested in less popular stocks.
- **Affected Components**: `src/pages/peer_comparison.py` (entire file, especially lines 87-95, 109-111, 139-140, 155-156)
- **Implementation Notes**:
  - Add a fallback mechanism: if `INDUSTRY_BENCHMARKS` lookup fails, call `client.get_stock_info()` to find peers in the same `industry_category`, then select the one with highest revenue as benchmark
  - Wrap `_get_benchmark_data` call in a try/except with a user-friendly fallback UI
  - Show partial results: if comparison table fails, still show the target company's metrics in a single-column layout
  - Add a note explaining why the benchmark was auto-selected

---

## Issue 7: Watchlist Add/Remove Does Not Provide Visual Feedback

- **Category**: Interaction
- **Severity**: P1 (Usability)
- **Current Behavior**: In `business_card.py` (lines 47-54), the watchlist button calls `add_to_watchlist()` or `remove_from_watchlist()` followed by `st.rerun()`. The page immediately re-renders. There is no toast, confirmation message, or visual transition. Users cannot tell if the action succeeded. The same issue exists in the watchlist page itself.
- **Proposed Behavior**:
  - After adding: show `st.success("✅ 已將 {stock_name} 加入我的關注")` with a brief animation
  - After removing: show `st.info("已將 {stock_name} 從我的關注移除")`
  - Use `st.toast()` (available in Streamlit 1.35+) for a non-intrusive notification that auto-dismisses after 3 seconds
  - Consider adding a brief visual transition (e.g., button color change) before `st.rerun()`
- **UX Rationale**: Action feedback is a fundamental UX principle. Without it, users are uncertain whether their action registered. This is especially important for a "save" action like adding to watchlist — users may click multiple times or think the app is unresponsive.
- **Affected Components**: `src/pages/business_card.py` (lines 46-54), `src/pages/watchlist_page.py` (watchlist management), `src/services/watchlist.py` (add/remove functions)
- **Implementation Notes**:
  - Replace the current button logic with:
    ```python
    if st.button("➕ 加入關注", key=f"watch_{stock_id}", use_container_width=True):
        add_to_watchlist(stock_id, stock_name)
        st.toast(f"✅ 已將 {stock_name} 加入我的關注")
        st.rerun()
    ```
  - For removal, use `st.toast(f"已將 {stock_name} 從我的關注移除")` with an info icon
  - If `st.toast` is not available in the current Streamlit version, use `st.success()` / `st.info()` placed prominently at the top of the page
  - Consider returning a boolean from add/remove functions and showing conditional messages

---

## Issue 8: Event Dashboard Buttons Can Crash the Page When Duplicate Titles Exist

- **Category**: Interaction
- **Severity**: P0 (Crash)
- **Current Behavior**: In `event_dashboard.py` (line 88), button keys are generated as `key=f"evt_{stock_id}_{title[:20]}"`. If two events for the same stock have titles with the same first 20 characters (e.g., two news articles about the same earnings report), Streamlit raises `DuplicateWidgetID` and the entire page crashes with an unhandled exception.
- **Proposed Behavior**: 
  - Include a unique event identifier in the button key. Use `event.get("date", "")` + an index counter to ensure uniqueness: `key=f"evt_{stock_id}_{i}_{event.get('date', '')}"`
  - Alternatively, use `event.get("id", index)` if events have unique IDs
  - Add a try/except around the button rendering to prevent crashes even if keys somehow collide
- **UX Rationale**: A page crash is the worst possible UX. This is a data-driven bug that will occur in production whenever a company has multiple similar events on the same day. It must be fixed before any public release.
- **Affected Components**: `src/pages/event_dashboard.py` (lines 77-91)
- **Implementation Notes**:
  - Replace the inner loop with an enumerated version:
    ```python
    for i, event in enumerate(events):
        ...
        if st.button("查看名片", key=f"evt_{stock_id}_{i}_{event.get('date', '')}"):
    ```
  - Verify that all other button keys in the app follow the same uniqueness pattern per DESIGN_SYSTEM Section 3.2
  - Add a pre-render validation pass that checks for duplicate keys and logs a warning

---

## Issue 9: Timeline Filter (1Y, 3Y) Silently Fails — Charts Don't Update and No Error Is Shown

- **Category**: Interaction
- **Severity**: P1 (Usability)
- **Current Behavior**: In `_router_base.py` (lines 149-178), `filter_by_timeline()` catches all exceptions and returns the original unfiltered DataFrame (`return df` on line 178). If the `date` column has format anomalies, timezone issues, or unexpected data types, the filter silently does nothing. Users click "1Y" but see the same data as "ALL", with no indication that the filter failed. The timeline selector renders but has no effect.
- **Proposed Behavior**:
  - On exception, show `st.warning("時間篩選無法套用，顯示全部資料")` instead of silently returning unfiltered data
  - Validate the `date` column format before attempting conversion
  - Add a debug indicator: show the active filter and date range in a small caption below the chart (e.g., "顯示範圍：2025-06-08 ~ 2026-06-08 (1Y)")
  - Ensure the `date` column is consistently parsed as `datetime` when data is first loaded, not at filter time
- **UX Rationale**: Silent failures are the most dangerous UX issue — users think the filter works but see no change, leading them to doubt the app's reliability. The DESIGN_SYSTEM error handling section states "Under no circumstances should Streamlit throw an uncaught exception" — but the opposite is also true: silent failures with no feedback are equally harmful.
- **Affected Components**: `src/pages/_router_base.py` (`filter_by_timeline`, lines 149-178), `src/pages/timeline_controls.py` (selector UI), all pages that use `filter_by_timeline` (financial_health, operation_checkup)
- **Implementation Notes**:
  - Modify `filter_by_timeline` to accept an optional `context` string for error messages:
    ```python
    except Exception as e:
        if context:
            st.warning(f"⚠️ 時間篩選「{selected}」無法套用：顯示全部資料")
        return df
    ```
  - Pre-parse date columns in `get_stock_data()` (in `_router_base.py`) to ensure consistent datetime format
  - Add a small `st.caption()` below each chart showing the active filter and date range
  - Consider adding a "Reset to ALL" button that appears when a filter is active

---

## Issue 10: Switching Between 5+ Stocks in Quick Succession Triggers FinMind Rate Limits with No User-Facing Warning

- **Category**: Performance
- **Severity**: P1 (Usability)
- **Current Behavior**: Each stock switch triggers `get_stock_data()` which makes up to 11 separate FinMind API calls (price, revenue, financial statement, balance sheet, cash flow, news, institutional, dividend, etc.). The cache key includes `end_date=datetime.now().strftime("%Y-%m-%d")`, which changes daily, causing cache misses every 24 hours. When users rapidly switch stocks, the app sends 50+ API requests in minutes. FinMind returns empty DataFrames or errors, which are silently treated as "no data" — users see empty charts with no explanation.
- **Proposed Behavior**:
  - Implement request queuing/debouncing: if a new stock is selected while loading, cancel the previous request
  - Add a rate limit detector: if 3+ consecutive API calls return empty results, show `st.warning("⚠️ 資料載入較慢，已達到 API 速率限制。請稍後再試。")`
  - Show a global rate limit status indicator in the sidebar
  - Fix the cache key to not include `end_date` for daily-changing parameters (use date-only granularity for cache TTL)
- **UX Rationale**: Users see empty charts and assume the app is broken. The DESIGN_SYSTEM states "API failure: show st.warning('Data temporarily unavailable, please try again later'), do not crash." This is currently not implemented.
- **Affected Components**: `src/data/finmind_client.py` (all fetch methods, cache key generation), `src/pages/_router_base.py` (`get_stock_data`), `src/main.py` (stock switching logic)
- **Implementation Notes**:
  - Fix cache key: remove `end_date` from the cache key hash, or use only the date part (not time) and align with TTL
  - Add a `_consecutive_failures` counter to `FinMindClient` that triggers a warning after 3 empty responses
  - Implement request cancellation: use a `session_state["current_loading_stock"]` flag; if it changes mid-load, abort
  - Add a sidebar indicator: `st.sidebar.metric("API 狀態", "正常" if healthy else "速率限制中")
  - Consider batching API calls using `concurrent.futures` to reduce total request count

---

## Issue 11: Cache Never Expires Old Files — `.cache/` Directory Grows Without Bound

- **Category**: Performance
- **Severity**: P2 (Polish)
- **Current Behavior**: In `finmind_client.py` (lines 44-48), `_is_cache_valid()` checks file modification time against `cache_ttl`. However, old cache files are never deleted. The `.cache/` directory accumulates JSON files indefinitely. On a daily development machine, this can reach thousands of files (each API call generates a unique hash).
- **Proposed Behavior**:
  - Add a cache cleanup method that runs on client initialization: delete files older than `cache_ttl * 2`
  - Add a cache size limit: if `.cache/` exceeds 100MB, delete oldest files first (LRU eviction)
  - Show cache stats in the sidebar for debugging: "快取: 42 檔案 / 15.3 MB"
- **UX Rationale**: While not directly visible to end users, unbounded cache growth can cause disk space issues and slow down cache lookups. It's a maintenance concern that affects long-term reliability.
- **Affected Components**: `src/data/finmind_client.py` (cache methods, lines 36-73)
- **Implementation Notes**:
  - Add to `FinMindClient.__init__`:
    ```python
    def _cleanup_cache(self):
        for f in self.cache_dir.glob("*.json"):
            if datetime.now() - datetime.fromtimestamp(f.stat().st_mtime) > self.cache_ttl * 2:
                f.unlink()
    ```
  - Run cleanup on initialization and periodically (every N requests)
  - Add a `--clear-cache` CLI flag or a sidebar button for manual cleanup

---

## Issue 12: PPT-Style Layout Breaks on Smaller Screens / Narrow Browser Windows

- **Category**: Visual Design
- **Severity**: P1 (Usability)
- **Current Behavior**: The layout uses fixed `st.columns()` ratios and hardcoded `max-width: 1200px` (main.py line 43). Cards use fixed `padding: 1.5rem` and `font-size: 1.8rem`. On screens narrower than 1024px (tablets, laptops), the 3-column card layout becomes cramped, text overflows, and the navbar tabs wrap awkwardly. The 9-tab navbar (`router.py` line 136-137) in particular breaks badly on narrow screens.
- **Proposed Behavior**:
  - Use responsive column layouts: `st.columns([1, 1, 1])` with `vertical_alignment="top"` and allow wrapping
  - For the navbar: implement a dropdown selector (`st.selectbox`) for narrow screens instead of 9 inline buttons
  - Use CSS media queries to adjust font sizes and padding for screens < 768px
  - Set `max-width: 100%` instead of 1200px for the main container on narrow screens
- **UX Rationale**: The app targets beginners who may use laptops or tablets. A broken layout on common screen sizes directly contradicts the "10-second test" — users can't understand content if the layout is broken.
- **Affected Components**: `src/main.py` (CSS, lines 26-57), `src/pages/router.py` (navbar, lines 118-147), all page files with multi-column layouts
- **Implementation Notes**:
  - Add CSS media queries to the global stylesheet:
    ```css
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem; }
        /* Stack columns vertically */
    }
    ```
  - For the navbar, use `st.selectbox` as a fallback when screen width is detected (via JS or Streamlit's `st.width`)
  - Test with Playwright at 375px, 768px, 1024px, and 1440px widths
  - Consider using `st.tabs()` instead of button-based navigation for better mobile support

---

## Issue 13: Color Contrast on Chart Labels Is Insufficient for Readability in Dark Mode

- **Category**: Visual Design
- **Severity**: P2 (Polish)
- **Current Behavior**: Charts use `paper_bgcolor="rgba(0,0,0,0)"` and `plot_bgcolor="rgba(0,0,0,0)"` (transparent background) across all chart functions in `chart.py`. Axis labels and tick labels use default Plotly colors (gray). In Streamlit's dark mode, these gray labels become nearly invisible against the dark background. The DESIGN_SYSTEM specifies `#7F8C8D` for secondary text and `#2C3E50` for primary text — but these hex colors are not applied to Plotly chart elements.
- **Proposed Behavior**:
  - Set explicit font colors for all Plotly chart elements:
    - Axis titles: `#7F8C8D` (secondary text)
    - Tick labels: `#95A5A6` (lighter gray for dark mode readability)
    - Chart titles: `#2C3E50` (primary text)
    - Hover labels: white text on dark background
  - Use a dark-compatible background: `plot_bgcolor="#1E1E1E"` and `paper_bgcolor="#1E1E1E"` for dark mode
  - Add a `template` parameter to all charts for consistent styling
- **UX Rationale**: If users can't read chart labels, the charts are useless. This directly violates the "10-second test" and the PPT-style principle. Dark mode is a common user preference.
- **Affected Components**: `src/services/chart.py` (all chart functions), `src/main.py` (CSS for dark mode)
- **Implementation Notes**:
  - Create a shared `CHART_TEMPLATE` dict:
    ```python
    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#2C3E50", family="Noto Sans TC"),
        xaxis=dict(tickfont=dict(color="#7F8C8D")),
        yaxis=dict(tickfont=dict(color="#7F8C8D")),
    )
    ```
  - Apply this template in every chart function via `fig.update_layout(**CHART_LAYOUT)`
  - For dark mode detection, use Streamlit's `st.config.get_option("theme.base")` or inject a CSS class
  - Test all charts in both light and dark mode

---

## Issue 14: Concurrent Multi-User Access to `watchlist.yaml` Can Cause Data Loss or File Corruption

- **Category**: Robustness
- **Severity**: P1 (Usability)
- **Current Behavior**: In `watchlist.py` (lines 16-34), the watchlist uses a "read → modify → write" pattern with no file locking. If two users simultaneously add stocks to their watchlist (or if Streamlit's multi-session feature triggers concurrent writes), the second write overwrites the first, causing data loss. In extreme cases, partial writes can corrupt the YAML file.
- **Proposed Behavior**:
  - Implement file locking using `filelock` library (`pip install filelock`)
  - Wrap all read/write operations in `with FileLock("config/watchlist.yaml.lock"):`
  - Add a retry mechanism: if lock acquisition fails, wait 0.1s and retry up to 3 times
  - Add a backup mechanism: before writing, copy the current file to `watchlist.yaml.bak`
- **UX Rationale**: Data loss is unacceptable for a "save" feature. Users who add stocks to their watchlist expect them to persist. Losing saved data destroys trust in the app.
- **Affected Components**: `src/services/watchlist.py` (all functions), `config/watchlist.yaml`
- **Implementation Notes**:
  ```python
  from filelock import FileLock, Timeout
  
  LOCK_PATH = str(WATCHLIST_PATH) + ".lock"
  
  def save_watchlist(entries):
      lock = FileLock(LOCK_PATH, timeout=5)
      with lock:
          # backup
          if WATCHLIST_PATH.exists():
              shutil.copy2(WATCHLIST_PATH, WATCHLIST_PATH.with_suffix(".yaml.bak"))
          with open(WATCHLIST_PATH, "w", encoding="utf-8") as f:
              yaml.dump(entries, f, allow_unicode=True)
  ```
  - Apply the same pattern to `events.yaml` in the adaptive engine
  - Add a `try/except Timeout` handler that shows `st.error("儲存失敗，請稍後再試")`

---

## Summary Matrix

| # | Issue | Category | Severity | Effort |
|---|-------|----------|----------|--------|
| 1 | Chinese name search | Navigation | P1 | Medium |
| 2 | No loading indicator | Navigation | P1 | Medium |
| 3 | Browser back button | Navigation | P1 | High |
| 4 | Single-period empty charts | Data Display | P1 | Medium |
| 5 | ROE annualization | Data Display | P1 | Low |
| 6 | Peer comparison "No Data" | Data Display | P1 | Medium |
| 7 | Watchlist no feedback | Interaction | P1 | Low |
| 8 | DuplicateWidgetID crash | Interaction | **P0** | Low |
| 9 | Timeline filter silent fail | Interaction | P1 | Medium |
| 10 | Rate limit no warning | Performance | P1 | High |
| 11 | Cache never expires | Performance | P2 | Low |
| 12 | Layout breaks on small screens | Visual Design | P1 | High |
| 13 | Dark mode contrast | Visual Design | P2 | Medium |
| 14 | Watchlist concurrent access | Robustness | P1 | Low |

### Recommended Fix Order

1. **Immediate (P0)**: Issue 8 — DuplicateWidgetID crash (1-line fix, prevents production crashes)
2. **Sprint 1 (P1, Low Effort)**: Issues 5, 7, 11, 14 — Quick wins with high UX impact
3. **Sprint 2 (P1, Medium Effort)**: Issues 1, 2, 4, 6, 9, 13 — Core UX improvements
4. **Sprint 3 (P1, High Effort)**: Issues 3, 10, 12 — Architecture-level changes
5. **Backlog (P2)**: Issues 11, 13 — Polish when time permits

---

*Created: 2026-06-08*
*Maintainer: Frontend/UX Agent*
