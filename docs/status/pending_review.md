# Stock Explorer Pending Daniel Review

> Items here require human judgment and cannot be auto-resolved by agents.

## 🎨 Design Decisions

### 1. Navbar: 9-button row vs `st.tabs()` dropdown — ✅ RESOLVED
- **Decision**: Use `st.radio(horizontal=True)` — preserves bidirectional sync with URL/session_state, native responsive behavior (wraps to dropdown on narrow screens), minimal code change, stable public API.
- **Rationale**: `st.tabs()` cannot sync with `session_state["page"]` for sidebar/URL navigation. CSS media queries are fragile and don't solve discoverability. `st.radio` gives the best of both worlds.
- **Implemented**: 2026-06-09 in P2-2 sprint.
- **File**: `src/pages/router.py`

### 2. Seasonal Industry List
- **Issue**: The ROE seasonal note (UX Issue 5) needs a list of known seasonal industries.
- **Proposal**: Which industries should receive the warning label?
- **Default suggestion**: Tourism, agriculture, retail, and semiconductors.
- **Decision needed**: Confirm the industry list or defer the seasonal note until after MVP.
- **File**: `src/pages/financial_health.py`

### 3. ETF Classification Severity
- **Issue**: ETF misclassification (ARCH Issue 5) ranked P1, but may be P0 for M4 readiness
- **Impact**: Beginners exploring ETFs see the wrong analysis framework
- **Decision needed**: Upgrade to P0 (fix now) or keep P1 (fix after P0 band)?
- **File**: `src/services/watchlist.py`

---

*Updated: 2026-06-09 by PM after P2-2 implementation*
