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

## 📋 Roadmap Approval (NEW — 2026-06-11, from Discussion Round 4)

### 5. Revised Feature Roadmap (Post-Challenger)
- **Issue**: After team discussion + 3 rounds of Challenger review, the revised roadmap is:
  - **Phase 0 — Stabilize** (11-15h): business_card.py restore + 5 quick tech debt + DR-03 Financial Health
  - **Phase 1 — Foundation** (18-22h): D01 M5 verification + C16 "Did You Know?" + C07 Custom Thresholds
  - **Phase 2 — Core Features** (44-54h): C19 Learning Path + C14 Health Score + C02 Email
  - **Phase 3 — Share & Expand** (34-38h): C06 PPT Generation + C04 Market Thermometer
  - **Post-MVP** (18-24h): YAML→SQLite + C17 AI Q&A + C13 Quiz
- **Total estimated effort**: ~125-153h (with 20% buffer: ~150-184h)
- **Key change**: C06 (PPT Generation) moved from Phase 1 to Phase 3 — advances zero core values, should not be built before pages are excellent
- **Key change**: C19 (Learning Path) elevated to Phase 2 — best "Story first" alignment
- **Key change**: C15 (Paper Trading) CANCELLED — positioning violation
- **Decision needed**: Approve this roadmap or adjust priorities?

---

## 🔴 Critical Blocker (NEW — 2026-06-11)

### 6. business_card.py P0 Regression — Approval to Fix
- **Issue**: The main page of the app is severely broken. `business_card.py` is only 128 lines — it imports 15+ service functions but renders NONE of them. Every user sees a blank page (stock name + price + watchlist button only).
- **Impact**: #1 cause of user churn. The 10-second test is impossible to pass.
- **Proposed fix**: Git-based recovery (restore from commit 24d785b, rebase multi-list watchlist changes). Estimated: 10-12h.
- **Team recommendation**: Fix BEFORE any new features. This is a regression, not a feature.
- **Decision needed**: Approve immediate fix? Any concerns about the git-based recovery approach?

---

## 🔴 Awaiting Daniel's Decision (NEW — 2026-06-12, Discussion Round 5)

### 7. C14 Health Score: Scope Decision
- **Issue**: The Challenger flagged that C14's 8.5h estimate is unrealistic for a quality implementation with plain-language explanations. The team proposes two options:
  - **Option A: Health Score Badge** (4-6h) — Simple 0-100 score with color coding (green/yellow/red) displayed on business_card.py. No radar chart, no per-axis breakdown.
  - **Option B: Full 5-Axis Radar Chart** (14-20h) — Profitability/Growth/Financial Health/Dividend/Stability with click-to-expand plain-language explanations per axis. The key differentiator from competitors.
- **Challenger's recommendation**: Option A given D+ design grade. The radar deserves a better-designed app.
- **Decision needed**: Which option, or defer C14 entirely?

### 8. Revised Roadmap (Post-Discussion Round 5 + Challenger)
- **Issue**: After team discussion + 3 rounds of Challenger review, the approved roadmap is:
  - **Sprint 1** (4-6h): D01 M5 Verification + Integration
  - **Sprint 2** (4-5h): DR-03+C01 Financial Health Integrated Redesign
  - **Sprint 3** (2-3h): C01 Ex-dividend countdown + badge (business_card)
  - **Sprint 4** (4-6h): C16 "Did You Know?" Company Facts
  - **Sprint 5** (4-20h): C14 Health Score (scope depends on Daniel's decision #7 above)
  - **Total**: 18-40h
- **Key change from previous roadmap**: D01 moved from Phase 1 to Sprint 1 (must be first). C16 added (cheapest "Story first" feature). DR-03 and C01 financial_health.py merged into single integrated redesign.
- **Decision needed**: Approve this roadmap?

### 9. Pages Needing Structural Design Redesign
- **Issue**: The Design Reviewer identified 2 pages at grade D (lowest): Category Browser and Group Structure. These need structural redesigns, not just polish.
- **Current approach**: These are not in the current 5-sprint plan. Team recommends addressing them after Sprint 5, once the design system is better enforced.
- **Decision needed**: Include in current roadmap or defer to post-MVP?

---

*Updated: 2026-06-12 by PM after discussion round 5 + challenger 3-round challenge*
