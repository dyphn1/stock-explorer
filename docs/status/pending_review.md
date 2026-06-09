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

## 🔴 Positioning Decision (NEW — 2026-06-10, from Challenger)

### 4. Portfolio P&L: Feature or Positioning Violation?
- **Issue**: The team proposed C05 (Portfolio P&L Management) as Phase 1. The Challenger flagged it as a **positioning violation** — adding cost basis + holdings tracking turns the app into a portfolio tracker, contradicting "historian, not stock picker."
- **Options**:
  - **A) Reject C05 entirely** — Stay pure "historian," no portfolio tracking
  - **B) Reframe as "Paper Portfolio for Learning"** — Educational framing, no P&L display, focus on "what if I had invested $X?"
  - **C) Approve as-is** — Accept the positioning shift toward portfolio management
- **Challenger's recommendation**: Reject or radically reframe
- **Team's technical estimate**: 8-12h if approved
- **Decision needed**: Which option, or defer?

---

## 📋 Roadmap Approval (NEW — 2026-06-10, from Team Discussion)

### 5. Revised Feature Roadmap
- **Issue**: After team discussion + 3 rounds of Challenger review, the revised roadmap is:
  - **Phase 1**: C06 (PPT Generation) + C07 (Custom Thresholds)
  - **Phase 2**: C02 (Email Notifications) + C04 (Market Thermometer)
  - **Phase 3**: C05 (Portfolio P&L, conditional on Daniel's approval above)
  - **New prerequisites**: ISSUE-D01 (M5 verification), ISSUE-D02 (background worker investigation)
- **Total estimated effort**: ~62-84h (without C05)
- **Decision needed**: Approve this roadmap or adjust priorities?

---

*Updated: 2026-06-10 by PM after team discussion + challenger round*
