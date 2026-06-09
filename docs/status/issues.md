# Stock Explorer Issue Tracker

> Track every bug, feature request, and design decision here.
> Each item should include its source and priority.

---

## Format

```
### [ID] Short Title
- **Source:** Competitor research / bug report / design review / PM decision
- **Priority:** P0 / P1 / P2
- **Status:** 📋 Todo / 🔄 In progress / ✅ Done / ❌ Canceled
- **Description:** Detailed explanation
- **Related files:** Code files affected
```

---

## 🔴 P0 — Must Fix / Implement

---

### [ISSUE-C01] Ex-Dividend Calendar
- **Source:** Competitor research
- **Priority:** P0
- **Status:** ✅ Done
- **Description:**
  - GoodInfo and Dogga (財報狗) both have complete ex-dividend information
  - One of the most common beginner questions: "When does TSMC pay dividends and how much?"
  - Stock Explorer now answers this question via integrated dividend analysis
- **Implementation:**
  - `src/services/dividend_analyzer.py` — Full dividend analysis engine (frequency classification, TTM estimation, yield calculation, plain-language summaries)
  - `src/pages/business_card.py` — "💵 配息故事" section with tip card, 3 mini-cards (最近一季/預估全年/殖利率), expandable history table
  - `src/pages/_router_base.py` — Data loading pipeline includes dividend data fetch
- **Related files:** `src/pages/business_card.py`, `src/services/dividend_analyzer.py`, `config/watchlist.yaml`
- **Reference:** `docs/research/competitor_research.md` — Inspiration A

---

### [ISSUE-C02] Notification / Push System
- **Source:** Competitor research
- **Priority:** P0
- **Status:** 📋 Todo
- **Description:**
  - 財報狗 has Line Notify; CMoney has App Push
  - The event detection engine already has the data but cannot proactively notify users
  - Phase 1: email notification (low cost)
  - Phase 2: Line Notify (requires Bot account)
- **Suggested Implementation:**
  - Revenue change ±30%
  - Stock price change ±7%
  - User-customizable notification conditions
- **Technology:** Background worker + SMTP (Phase 1)
- **Related files:** `src/services/adaptive_engine.py`, new `src/services/notifier.py`
- **Reference:** `docs/research/competitor_research.md` — Inspiration B

---

### [ISSUE-C03] Multiple Watchlist Lists
- **Source:** Competitor research
- **Priority:** P0
- **Status:** ✅ Done
- **Description:** (Resolved 2026-06-10)
  - Multi-watchlist system implemented with full CRUD operations
  - `watchlist.py` supports multiple named lists
  - `watchlist_page.py` has multi-tab UI
  - Business Card page has "Add to which list?" selector
- **Description:**
  - Yahoo Finance and 財報狗 both support multiple watchlists
  - Currently there is only one "My Watchlist" with no categorization capability
  - Users need to separately track "divend stocks", "watchlist", "high dividend yield", etc.
- **Suggested Implementation:**
  - Refactor `watchlist.yaml` to a `lists` structure
  - Change `watchlist_page.py` to multi-tab pages
  - Add a "Add to which list?" selector on the Business Card page
- **Related files:** `config/watchlist.yaml`, `src/services/watchlist.py`, `src/pages/watchlist_page.py`
- **Reference:** `docs/research/competitor_research.md` — Inspiration C

---

## 🟡 P1 — Important but Not Critical

---

### [ISSUE-C04] Market Thermometer
- **Source:** Competitor research
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - 玩股網 has a "Stock Market Thermometer"; CMoney has market sentiment indicators
  - Beginners want to know "Is the market hot or cold right now?"
  - Recommendation: add a market temperature indicator to the home page or event dashboard
- **Suggested Implementation:**
  - Three major institutional investors buy/sell surplus (5-day average)
  - Market trading volume (hot vs. cold)
  - Ratio of limit-up / limit-down stocks
  - Presentation: feel-temperature (🔥 Hot / 😊 Normal / 🥶 Cold) + plain-language explanation
- **Data Feasibility:** FinMind has `TaiwanStockInstitutionalInvestorsBuySell`
- **Related files:** `src/pages/event_dashboard.py`, new `src/services/market_thermal.py`
- **Reference:** `docs/research/competitor_research.md` — Inspiration D

---

### [ISSUE-C05] Portfolio P&L Management
- **Source:** Competitor research
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - CMoney has comprehensive portfolio management features
  - Current Watchlist only has price alerts; no position P&L management
  - Evolve Watchlist into Portfolio: add cost basis, holdings quantity
- **Suggested Implementation:**
  - Cost per share, number of shares held
  - Unrealized P&L (real-time)
  - Realized P&L (historical trades)
  - Overall portfolio return rate
- **Related files:** `config/watchlist.yaml`, `src/services/watchlist.py`, `src/pages/watchlist_page.py`
- **Reference:** `docs/research/competitor_research.md` — Inspiration E

---

### [ISSUE-C06] Auto-Generate Stock Analysis PPT
- **Source:** Competitor research
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - 玩股網 has a one-click analysis report generation feature
  - Stock Explorer already has PPT-style CSS; can directly use python-pptx to generate real PPT files
  - Differentiation: Stock Explorer's PPT style is more polished and more educational than 玩股網's
- **Suggested Implementation:**
  - Add a "Download PPT" button on each page
  - Include: Company Business Card, Operations Health Check highlights, Financial Health Summary, Peer Comparison Radar Chart
  - Use python-pptx + scraped data from each page
- **Technology:** `python-pptx` library
- **Related files:** All page modules
- **Reference:** `docs/research/competitor_research.md` — Inspiration F

---

### [ISSUE-C07] Customizable Event Thresholds
- **Source:** Competitor research
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - Extension of the M5 event detection engine
  - Currently uses fixed thresholds (revenue ±30%, stock price ±7%)
  - Allow users to customize sensitivity and event types
- **Suggested Implementation:**
  - User-adjustable sensitivity
  - New event types (institutional investors buying/selling for N consecutive days, revenue declining for N consecutive months)
  - Add a settings page
- **Related files:** `src/services/adaptive_engine.py`, new settings page
- **Reference:** `docs/research/competitor_research.md` — Inspiration G

---

## 🟢 P2 — Nice-to-Have / Future Consideration

---

### [ISSUE-C08] Video Tutorials
- **Source:** Competitor research
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - CMoney has a large number of investment tutorial videos
  - Each metric could have a 30-second plain-language explanation video embedded below it
  - High production cost; recommend post-M5 manual production or embedding existing YouTube resources
- **Related files:** All page modules
- **Reference:** `docs/research/competitor_research.md` — Inspiration H

---

### [ISSUE-C09] US Stock Support
- **Source:** Competitor research
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - 財報狗 supports 500+ US stocks
  - FinMind already has US stock data
  - Target: users already familiar with the Taiwan stock analysis framework who want to extend to US stocks
  - **Requires Daniel confirmation on whether to support US stocks**
- **Related files:** All page modules
- **Reference:** `docs/research/competitor_research.md` — Inspiration I

---

### [ISSUE-C10] Global Market Map
- **Source:** Competitor research
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - 玩股網 has a global stock market map
  - The Stock Explorer version can lean toward "fundamental understanding" rather than "trading heat"
  - Presentation: 🟢 Up 🔴 Down ↔️ Flat + plain-language explanation of each market status
- **Related files:** New page
- **Reference:** `docs/research/competitor_research.md` — Inspiration J

---

---

## 💡 Discussion Round — 2026-06-10 (Team Discussion + Challenger)

### Process Summary
- **Architect** analyzed technical feasibility of all 10 feature candidates
- **Design Reviewer** evaluated UX impact and alignment with "historian" positioning
- **Developer** estimated implementation costs (62-84h total for 5 features)
- **Challenger** raised 3 rounds of challenges, verdict: **roadmap needs revision**

### Challenger's Key Objections (Round 1-3)
1. **C05 (Portfolio P&L) is a positioning violation** — contradicts "historian, not stock picker"
2. **C02 (Notifications) critically under-prioritized** — P0 gap, all competitors have it
3. **C06 (PPT Generation) strategically misranked** — leverages unique PPT-style advantage
4. **Roadmap doesn't advance educational mission** — 4/5 core values untouched
5. **M5 event detection unverified** — building C07 on unvalidated foundation

### Revised Roadmap (Post-Challenger)

#### Phase 1 — Foundation + Quick Win
- **C06: Auto-Generate Stock Analysis PPT** (moved from Phase 4 → Phase 1)
  - Rationale: Leverages existing PPT-style CSS, zero new API calls, drives organic sharing
  - Risk: Medium (python-pptx + kaleido dependency)
  - Estimate: 18-24h
- **C07: Customizable Event Thresholds** (kept in Phase 1)
  - Rationale: Builds settings infrastructure for reuse by C02, C04
  - Risk: Medium
  - Estimate: 10-14h
  - **Prerequisite**: Verify M5 event detection with real FinMind data first

#### Phase 2 — Notification + Market Awareness
- **C02: Notification/Push System — Phase 1 Email** (moved from Phase 3 → Phase 2)
  - Rationale: P0 gap, all competitors have it, makes M5 event detection valuable
  - Risk: High (requires background worker architecture investigation)
  - Estimate: 14-18h
  - **Approach**: Start with "pull on next visit" model, investigate external cron for true push
- **C04: Market Thermometer** (kept in Phase 2)
  - Rationale: Pure education, beginner-friendly, homepage feature
  - Risk: Medium-High (market-wide data aggregation)
  - Estimate: 12-16h

#### Phase 3 — Portfolio (Conditional)
- **C05: Portfolio P&L Management** (moved from Phase 1 → Phase 3, **conditional**)
  - Rationale: Challenger flagged positioning risk — needs Daniel's approval
  - **Requires Daniel confirmation**: Should we add portfolio tracking or stay pure "historian"?
  - If approved: Reframe as "Paper Portfolio for Learning" with educational framing, no P&L display
  - Risk: High (positioning risk, not just technical risk)
  - Estimate: 8-12h (if approved)

#### Rejected / Needs Daniel Input
- C05 as originally designed (cost basis + P&L tracking) — **REJECTED** unless Daniel approves reframing

### New Feature Ideas from Discussion

#### [ISSUE-D01] M5 Event Detection Verification
- **Source:** Team discussion (Challenger Round 3)
- **Priority:** P0
- **Status:** 📋 Todo
- **Description:** Before building C07 (Custom Thresholds) on top of the adaptive engine, verify that M5 event detection works with real FinMind data. Currently the detection logic is code-complete but unvalidated in production.
- **Related files:** `src/services/adaptive_engine.py`, `config/events.yaml`

#### [ISSUE-D02] Background Worker Architecture Investigation
- **Source:** Team discussion (Challenger Round 2)
- **Priority:** P0
- **Status:** 📋 Todo
- **Description:** C02 (Notifications) requires background processing but Streamlit is request-response only. Need to investigate and decide on architecture: external cron job, APScheduler daemon thread, or "pull on next visit" model.
- **Related files:** New `scripts/notification_worker.py`, `src/services/notifier.py`

#### [ISSUE-D03] Event Retention Policy
- **Source:** Architect analysis
- **Priority:** P1
- **Status:** ✅ Done
- **Description:** Events accumulate indefinitely in events.yaml. Add retention policy — prune events older than 90 days via `prune_old_events()` called on each `record_event()` write.
- **Implementation:** `prune_old_events(days=90)` in `adaptive_engine.py`, called automatically after appending new events.
- **Related files:** `src/services/adaptive_engine.py`, `config/events.yaml`

---

## 🔍 Review Round — 2026-06-10 (Review Theme)

### Process Summary
- **Architect** reviewed all remaining 13 tech debt items (down from 19), verified 9 previously "done" items against source code, identified 3 new items
- **Design Reviewer** audited all 9 pages against design_system.md, found 26 new design issues across 7 categories
- **Developer** estimated costs for 35 items totaling ~103.4 hours
- **QA Research**: Web research timed out — using existing competitor data from 2026-06-09 round

### New Technical Debt Items (from Architect)

#### [ISSUE-TD-NewA01] Timeline Constants Duplicated
- **Source:** Architect tech debt review (2026-06-10)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** `_TIMELINE_DAYS` in `_router_base.py` and `_TIMELINE_OPTIONS` in `timeline_controls.py` define the same mapping. Risk of divergence.
- **Effort:** 10 minutes
- **Related files:** `src/pages/_router_base.py`, `src/pages/timeline_controls.py`

#### [ISSUE-TD-B01] FinMindRateLimitError Silently Swallowed
- **Source:** Architect tech debt review (2026-06-10)
- **Priority:** P1
- **Status:** ✅ Done
- **Description:** `FinMindRateLimitError` is raised in `finmind_client.py` but caught by the generic `except Exception` in `_fetch()` inner function. Users never see rate limit warnings.
- **Fix:** Added separate `except FinMindRateLimitError` block in `_fetch()` that sets `st.session_state["_rate_limited"] = True` before returning None.
- **Effort:** 15 minutes
- **Commit:** `ef162e4`
- **Related files:** `src/pages/_router_base.py`, `src/data/finmind_client.py`

#### [ISSUE-TD-E01] No Tests for Event Detection Algorithms
- **Source:** Architect tech debt review (2026-06-10)
- **Priority:** P0
- **Status:** ✅ Done
- **Description:** Zero tests for `detect_revenue_event()`, `detect_price_abnormal()`, `detect_news_event()`, `check_data_freshness()`, `detect_company_type()`, `extract_dividend_summary()`, and `validate_stock_id()`. These are the core value-add algorithms.
- **Fix:** Added 59 new unit tests across 7 test classes: TestValidateStockId (9), TestDetectRevenueEvent (8), TestDetectPriceAbnormal (8), TestDetectNewsEvent (8), TestCheckDataFreshness (7), TestDetectCompanyType (10), TestExtractDividendSummary (9). Total: 88 tests (29 existing + 59 new), all passing.
- **Effort:** 3 hours
- **Commit:** `09c66ab`
- **Related files:** `tests/test_business_logic.py`, `src/services/adaptive_engine.py`, `src/services/validation.py`

### New Design Issues (from Design Reviewer)

#### [ISSUE-DR-01] Color System Violations Across 6 Files
- **Source:** Design comparison review (2026-06-10)
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:** 10+ instances of colors outside the design system palette: `#F39C12` (orange), `#2E86C1` (dark blue), `#1B4F72` (navy), `#8E44AD` (purple), `#2ECC71` (non-standard green). Affects: `financial_health.py`, `etf_browser.py`, `watchlist_page.py`, `chart.py`, `operation_checkup.py`.
- **Effort:** 1 hour
- **Related files:** 6 files

#### [ISSUE-DR-02] st.cache_data in View Layer (Architecture Violation)
- **Source:** Design comparison review (2026-06-10)
- **Priority:** P1
- **Status:** ✅ Done
- **Description:** `peer_comparison.py:51` and `etf_browser.py:12,18` use `@st.cache_data` in View layer, violating architecture Section 3.3.
- **Fix:** Removed `@st.cache_data(ttl=3600)` from `_find_fallback_benchmark` in peer_comparison.py and `_cached_get_stock_info` + `_get_all_etf_prices` in etf_browser.py. Data caching is handled by FinMindClient in the data layer.
- **Effort:** 30 minutes
- **Commit:** `ef162e4`
- **Related files:** `src/pages/peer_comparison.py`, `src/pages/etf_browser.py`

#### [ISSUE-DR-03] Financial Health Page Text-Heavy (PPT Style Violation)
- **Source:** Design comparison review (2026-06-10)
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:** `financial_health.py` is the most text-heavy page — 4 sections with detailed explanations, significantly exceeding 200-char limit. Only 1 chart for 4 sections (chart proportion below 60%). Grade: C+.
- **Effort:** 1.5 hours
- **Related files:** `src/pages/financial_health.py`

#### [ISSUE-DR-04] Component Inconsistency (Inline HTML vs Shared Components)
- **Source:** Design comparison review (2026-06-10)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** 4 pages use inline HTML cards instead of shared `_白话_card()` / `_info_card()`: `business_card.py`, `financial_health.py`, `watchlist_page.py`, `operation_checkup.py`.
- **Effort:** 2 hours
- **Related files:** 4 page files

#### [ISSUE-DR-05] Responsive Column Layouts Still Break on Narrow Screens
- **Source:** Design comparison review (2026-06-10)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** 6-column layouts in `etf_browser.py` and `category_browser.py` overflow on narrow screens. P2-2 fixed the navbar but column layouts remain broken.
- **Effort:** 1.5 hours
- **Related files:** `src/pages/etf_browser.py`, `src/pages/category_browser.py`

### Cost Estimation Summary (from Developer)

| Group | Items | Hours |
|-------|-------|-------|
| A1. Immediate (This Week) | 5 quick wins | 1.3 hrs |
| A2. Short-Term (Next 2 Weeks) | 6 items | 10.8 hrs |
| A3. Medium-Term (Post-MVP) | 5 items | 11.0 hrs |
| B. Design Improvements | 8 items | 8.3 hrs |
| C. New Features | 6 features | 72.0 hrs |
| **GRAND TOTAL** | **35 items** | **103.4 hrs** |
| With 20% buffer | | **~124 hrs** |

Critical path: D01 (M5 verification) → C07 (custom thresholds) and D02 (background worker) → C02 (notifications)

---

## 🧠 Challenger's New Feature Ideas (from Review Round)

#### [ISSUE-C11] Company Timeline Narrative (Story Thread)
- **Source:** Challenger review (2026-06-10, Round 1)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** The event dashboard (A-) is a disconnected list. What's missing is a narrative timeline — "Here's what happened to TSMC in the last 3 years, told as a story." The team has all the data (events, revenue, price) but no narrative thread connecting them. This is the #1 thing competitors DON'T have and aligns perfectly with the "historian" positioning and "Story first, data second" core value.
- **Suggested Implementation:** Add a "Story" tab to each company page that weaves events, revenue milestones, and price movements into a chronological narrative with plain-language explanations.
- **Related files:** New `src/pages/company_story.py`, `src/services/narrative_engine.py`
- **Estimate:** 16-24h

#### [ISSUE-C12] Beginner Glossary / Term Tooltip System
- **Source:** Challenger review (2026-06-10, Round 1)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** The design system says "All professional terms must have plain-language translations" but there's no systematic glossary or tooltip system. Beginners encounter terms like "ROE," "P/B ratio," "institutional investors" with no inline help. This is a unique educational feature that no competitor has done well.
- **Suggested Implementation:** Create `src/data/glossary.yaml` with term → plain-language definition. Add hover tooltips or click-to-expand definitions on all financial terms across all pages.
- **Related files:** `src/data/glossary.yaml`, all page modules
- **Estimate:** 8-12h

---

## 📊 Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 19 |
| 🔄 In progress | 0 |
| ✅ Done | 7 |
| ❌ Canceled | 0 |

| Priority | Count |
|----------|-------|
| P0 | 4 |
| P1 | 7 |
| P2 | 9 |

---

*Last updated: 2026-06-10 (review round — Architect, Design Reviewer, Developer, Challenger)*
*Challenger confirmed findings with adjustments: DR-03 promoted to P0, TD-B01 promoted to P0, C06 moved to Phase 2/3, C03 status reconciled to Done*
