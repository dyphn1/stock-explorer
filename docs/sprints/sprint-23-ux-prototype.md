# Sprint 23 UX Prototype Document

## 1. Scrolling Fix

### Problem
The main stock detail page displays too many UI elements vertically, causing excessive scrolling on typical screen sizes. Specifically, the layout includes:
- Navigation bar
- Three metric cards (Revenue YoY, Net Margin, ROE) in a row
- Two-column layout: chart (width ratio 2) and debt ratio card (width ratio 1)

This arrangement often requires vertical scrolling to view all content, especially on laptops or smaller monitors.

### Solution
Replace the current fixed layout with a tabbed interface to reduce initial vertical footprint while maintaining access to all information.

#### Proposed Changes
1. **Keep the navigation bar** at the top (unchanged).
2. **Introduce `st.tabs`** with two tabs:
   - **Tab 1: "Key Metrics"** - Displays all four metric cards in a 2x2 grid
   - **Tab 2: "Financial Chart"** - Displays the revenue trend chart

#### Implementation Details
In `src/main.py`, replace the current metric rendering code (lines 340-387) with:

```python
# render cards using tabs
tab1, tab2 = st.tabs([t("main.tab.key_metrics"), t("main.tab.financial_chart")])

with tab1:
    # 2x2 grid for metric cards
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        render_metric_card(
            title=f"📊 {t('metric_education.revenue_yoy_display_name')}",
            value=fmt_percent(revenue_yoy),
            description=t("metric_education.revenue_yoy_explanation") if revenue_yoy is not None else "",
            analogy="",
            is_positive=(revenue_yoy is not None and revenue_yoy >= 0),
        )
    with m_col2:
        render_metric_card(
            title=f"💰 {t('metric_education.net_margin_display_name')}",
            value=fmt_percent(net_margin),
            description=t("metric_education.net_margin_explanation") if net_margin is not None else "",
            analogy="",
            is_positive=(net_margin is not None and net_margin >= 0),
        )
    m_col3, m_col4 = st.columns(2)
    with m_col3:
        render_metric_card(
            title=f"📈 {t('metric_education.roe_display_name')}",
            value=fmt_percent(roe),
            description=t("metric_education.roe_explanation") if roe is not None else "",
            analogy="",
            is_positive=(roe is not None and roe >= 0),
        )
    with m_col4:
        render_metric_card(
            title=f"⚖️ {t('metric_education.debt_ratio_display_name')}",
            value=f"{debt_to_equity:.2f}" if debt_to_equity is not None else "-",
            description=t("metric_education.debt_ratio_explanation") if debt_to_equity is not None else "",
            analogy="",
            is_positive=False,
        )

with tab2:
    # Financial chart (full width)
    st.markdown(
        """
        <div class=\"card\" style=\"background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.05);border:1px solid #E1E4E8;\">
            <div class=\"card-title\">📉 Revenue Trend (Last 12 Months)</div>
            <div class=\"chart-placeholder\" style=\"width:100%;height:250px;background:#f9f9f9;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#aaa;border-radius:8px;margin-top:10px;\">
                [ Plotly Line Chart: Monthly Revenue Trend ]
            </div>
            <div style=\"font-size:12px;color:#7F8C8D;margin-top:10px;text-align:right;\">Source: FinMind API</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
```

#### Required Locale Updates
Add the following keys to `locales/en.yaml` and `locales/zh-TW.yaml` under a new `main.tab` section:

```yaml
# In en.yaml
main:
  tab:
    key_metrics: "Key Metrics"
    financial_chart: "Financial Chart"

# In zh-TW.yaml
main:
  tab:
    key_metrics: "主要指標"
    financial_chart: "財務圖表"
```

#### Target Max Height
With this tabbed layout, the initial visible area (navigation bar + tab headers) consumes approximately 150px vertical space. The content within each tab is designed to fit within a 600px viewport height, eliminating vertical scrolling on most screens.

## 2. Navigation Header Removal

### Problem
The test suite (`tests/test_ui_streamlit.py`) verifies that no element containing the text "導覽" (Chinese for "navigation") appears in the sidebar. User feedback indicates this element is non-interactive and serves no purpose.

### Current State
Our codebase search revealed no literal "navigation_header" strings or components. However, the test `test_no_navigation_header` explicitly checks for the absence of this text, suggesting it was previously present and removed.

### Solution
Ensure the sidebar rendering code does not inadvertently produce a "導覽" element. No changes are needed to the current sidebar implementation, but we must verify and guard against reintroduction.

#### Files to Verify
- `src/main.py`: Lines 97-160 (`_render_sidebar` function)
  - Confirm no `st.markdown`, `st.header`, or similar calls use text that could resolve to "導覽"
  - Current implementation renders:
    - `t("sidebar.search_header")` → "搜尋" / "Search"
    - `t("main.welcome.subtitle")` → "認識一家公司，從這裡開始" / "Get to know a company, start here"
    - No navigation-related text

#### Action
No modifications required. The sidebar already complies with the requirement. However, if during development a navigation header is reintroduced, it must be removed.

## 3. Playwright Smoke Test Plan

### Objective
Define functional UI tests to verify critical user flows and element presence without visual regression. Tests should run against a live Streamlit instance.

### Test Scenarios
1. **Main page loads successfully**
   - Verify the app title is visible (translated Chinese: "股識" or English: "Stock Explorer")
   - Verify the welcome message is present

2. **Search box is functional**
   - Verify the search input box is present with correct placeholder
   - Verify entering a valid stock ID (e.g., "2330") navigates to the stock detail page

3. **Sidebar hot stocks section works**
   - Verify the "熱門股票" / "Hot Stocks" expander is present
   - Verify clicking a hot stock button (e.g., "2330 台積電") navigates to that stock's detail page

4. **Sidebar hot ETFs section works**
   - Verify the "熱門ETF" / "Hot ETFs" expander is present
   - Verify clicking a hot ETF button navigates to the ETF detail page

5. **Stock detail page displays navbar**
   - After navigating to a stock page, verify the navigation bar shows:
     - Stock name and ID
     - Latest price and change
     - Horizontal radio tabs for page navigation (Business Card, Financial Statements, etc.)

6. **Metric cards are visible on detail page**
   - Verify all four metric cards (Revenue YoY, Net Margin, ROE, Debt Ratio) are present in the "Key Metrics" tab
   - Verify the financial chart is present in the "Financial Chart" tab

7. **No raw i18n keys visible**
   - Verify no untranslated keys like "main.home.title" or "sidebar.search_header" appear as visible text on any page

8. **Responsive behavior**
   - Verify at viewport width 320px (mobile), the tabbed layout still functions and content is accessible (no overlapping elements)

### Implementation Notes
- Use Playwright's `query_selector` with text selectors for Chinese/English labels
- Wait for network idle and short timeouts after page actions to account for Streamlit reruns
- Tests should be independent and able to run in any order
