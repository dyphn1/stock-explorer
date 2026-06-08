# Stock Explorer — Pending Daniel Review

> Items here require human judgment and cannot be auto-resolved by agents.

## 🎨 Design Decisions

### 1. Navbar: 9-button row vs `st.tabs()` dropdown
- **Issue**: The 9-button navbar wraps badly on narrow screens (UX Issue 12)
- **Proposal**: Replace with `st.tabs()` which handles narrow screens natively
- **Trade-off**: `st.tabs()` has different visual style; loses the PPT-style button look
- **Decision needed**: Keep 9-button row (and fix with CSS media queries) or switch to `st.tabs()`?
- **File**: `src/pages/router.py` (lines 136-147)

### 2. Seasonal Industry List
- **Issue**: ROE seasonal note (UX Issue 5) requires a list of "known seasonal industries"
- **Proposal**: Which industries should get the warning label?
- **Default suggestion**: 觀光餐旅 (tourism), 農漁業 (agriculture), 零售 (retail), 半導體 (semiconductors)
- **Decision needed**: Confirm industry list or defer seasonal note to post-MVP
- **File**: `src/pages/financial_health.py`

### 3. ETF Classification Severity
- **Issue**: ETF misclassification (ARCH Issue 5) ranked P1, but may be P0 for M4 readiness
- **Impact**: Beginners exploring ETFs see the wrong analysis framework
- **Decision needed**: Upgrade to P0 (fix now) or keep P1 (fix after P0 band)?
- **File**: `src/services/watchlist.py`

---

*Updated: 2026-06-08 by PM after design review*
