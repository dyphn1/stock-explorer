# Security Review: ETF Browser Section

## Overview
This document outlines the security review of the ETF browser section (`src/pages/etf_browser.py`) for the Stock Explorer application.

## Review Findings

### 1. Input Validation ✅
- **Status**: No significant issues found
- **Details**: 
  - The ETF browser does not accept arbitrary user text input (no search boxes or free-form filters)
  - User interactions are limited to predefined radio button selections (sub-view choices) and button clicks
  - All data used in processing (stock IDs, names, categories) originates from internal data structures or API responses, not direct user input
  - Classification logic uses hardcoded keyword lists applied to internal stock name data

### 2. API Abuse ⚠️
- **Status**: Potential issue identified
- **Details**:
  - Parallel fetching uses `ThreadPoolExecutor(max_workers=10)` for both price data (lines 50-51) and dividend data (lines 398-402)
  - No apparent rate limiting or request throttling mechanisms
  - Data is fetched on every page/view render without caching (no `@st.cache` decorators visible on data fetching functions)
  - A user could potentially trigger excessive API calls by rapidly changing views or refreshing the page
  - **Recommendation**: Implement request rate limiting, add caching for API responses, and consider debouncing UI triggers

### 3. Data Exposure ⚠️
- **Status**: Issue identified
- **Details**:
  - Line 84: `st.error(f\"{t('etf.browser.no_stock_info')}：{e}\")` exposes raw exception details to users
  - This could leak sensitive information such as API keys, database connection details, or stack traces
  - **Recommendation**: Replace with generic error message; log detailed errors internally instead of displaying to users

### 4. LLM Safety ✅
- **Status**: No issues found
- **Details**:
  - No AI/LLM features present in this section
  - The ETF browser performs traditional data processing and display only
  - No investment advice generation or predictive analytics

### 5. Hardcoded Secrets ✅
- **Status**: No issues found
- **Details**:
  - No API keys, passwords, or other secrets visible in the code
  - The `FinMindClient` is dependency-injected, suggesting credentials are managed externally (likely via environment variables or secure config)

### 6. File Operations ✅
- **Status**: No issues found
- **Details**:
  - No file read/write operations in this module
  - The referenced `watchlist.yaml` file locking concern applies to watchlist functionality, not the ETF browser

## Additional Observations
- **HTML Safety**: Multiple uses of `unsafe_allow_html=True` (lines 167, 168, 310-313, 436-443)
  - While data appears to originate from trusted API sources, this practice carries inherent XSS risk if API data could be compromised
  - **Recommendation**: Consider using Streamlit's native components or sanitizing HTML output
- **Error Handling**: 
  - Some functions use bare `except Exception: pass` or `except Exception: return None` (lines 40-41, 364-365)
  - While this prevents error exposure, it may hide legitimate issues during debugging
  - **Recommendation**: Implement more specific exception handling with appropriate logging

## Summary of Critical Issues
1. **Data Exposure**: Raw exception details shown to users (line 84)
2. **API Abuse Potential**: No rate limiting on parallel API calls

## Recommended Actions
1. Replace detailed error messages with user-friendly generic ones
2. Implement API request rate limiting and caching mechanisms
3. Consider adding Streamlit caching (`@st.cache_data` or `@st.cache_resource`) for data fetching functions
4. Review use of `unsafe_allow_html=True` for potential XSS risks
5. Strengthen exception handling with proper logging

## Files Reviewed
- `src/pages/etf_browser.py` (448 lines)

## Conclusion
The ETF browser section has a generally sound security foundation with two primary areas for improvement: preventing internal error exposure and mitigating potential API abuse through lack of rate limiting.