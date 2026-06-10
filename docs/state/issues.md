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
- **Implementation (all complete):**
  - `src/services/dividend_analyzer.py` — Full dividend analysis engine ✅
  - `src/pages/business_card.py` — "💵 配息故事" section with tip card, 3 mini-cards, expandable history table ✅
  - `src/pages/business_card.py` — Ex-dividend countdown card ("⏳ 距離除息日還剩 N 天") ✅ (2026-06-12, commit `9cbdc73`)
  - `src/pages/business_card.py` — History table with "即將除息" / "已除息" badges ✅ (2026-06-12, commit `9cbdc73`)
  - `src/pages/_router_base.py` — Data loading pipeline includes dividend data fetch ✅
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
- **Status:** ✅ Done
- **Description:** Before building C07 (Custom Thresholds) on top of the adaptive engine, verify that M5 event detection works with real FinMind data.
- **Verification (2026-06-12):** `run_auto_detection()` IS called in `router.py:96` on every stock page load. 8 real events in events.yaml from real FinMind data (stocks 2317, 2330, 2454, 1101). False positive exclusion logic exists and works. Dedup with normalized titles exists and works. Added false positive test for 合併營收. Cleaned up stale false positive event. All 89 tests pass.
- **Related files:** `src/services/adaptive_engine.py`, `config/events.yaml`
- **Commit:** `b042936`, `d3645c4`

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
- **Status:** ✅ Done
- **Description:** 10+ instances of colors outside the design system palette: `#F39C12` (orange), `#2E86C1` (dark blue), `#1B4F72` (navy), `#8E44AD` (purple), `#2ECC71` (non-standard green). Also 7 `linear-gradient` instances.
- **Fix (2026-06-12):** All `#F39C12` replaced with `#3498DB`. All `linear-gradient` replaced with flat `#EBF5FB`. Zero violations remaining in `src/`. Commit `9cbdc73`.
- **Effort:** ~1h (actual: ~30min)
- **Related files:** 6 files (business_card.py, financial_health.py, etf_browser.py, watchlist_page.py, chart.py, operation_checkup.py)

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
- **Priority:** P0 (promoted from P1 by Challenger Round 4)
- **Status:** ✅ Done
- **Description:** `financial_health.py` was the most text-heavy page — 4 sections with detailed explanations, significantly exceeding 200-char limit. Only 1 chart for 4 sections (chart proportion below 60%). Grade: C+.
- **Fix (2026-06-12):** Completed as part of ISSUE-D05 integrated redesign. All text blocks reduced to <40 chars each. Dividend gauge added as visual replacement. Component consistency achieved.
- **Effort:** 4-5h (integrated with C01 dividend gauge)
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
- **Description:** The design system says "All professional terms must have plain-language translations" but there's no systematic glossary or tooltip system. Beginners encounter terms like "ROE," "P/B ratio," "institutional investors" with no inline help. This is a unique educational feature that no competitor has done well. **Validated by Round 3: Investopedia's 10,000+ term glossary confirms the value of this approach.**
- **Suggested Implementation:** Create `src/data/glossary.yaml` with term → plain-language definition. Add hover tooltips or click-to-expand definitions on all financial terms across all pages.
- **Related files:** `src/data/glossary.yaml`, all page modules
- **Estimate:** 8-12h

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

## 🌍 Round 3 — Competitor Research (2026-06-10, International + AI)

### New Feature Ideas from Round 3

#### [ISSUE-C13] Investment Personality Quiz
- **Source:** Competitor research (Round 3, Stash risk quiz)
- **Priority:** P2 (demoted from P1 — Challenger Round 3: onboarding convenience, not educational tool)
- **Status:** 📋 Todo
- **Description:**
  - Stash has a "Build Your Portfolio" risk preference quiz. Acorns also has onboarding personalization.
  - Stock Explorer has NO onboarding flow — users land on a page and don't know where to start.
  - A 5-question quiz ("How long do you plan to invest?", "How do you feel about losses?", etc.) that recommends "You're a dividend explorer → start with TSMC's dividend story" or "You're a growth hunter → start with revenue trends."
  - Aligns with "historian" positioning: uses quiz results to recommend which analysis perspectives to explore first.
- **Suggested Implementation:**
  - New `src/pages/onboarding.py` with 5 multiple-choice questions
  - Results stored in `session_state["investor_type"]`
  - Investor type influences homepage recommendations and suggested pages
  - Types to consider: `dividend_explorer`, `growth_hunter`, `value_sector`, `quality_focused`, `balanced_learner`
  - Can be retaken anytime from settings
- **Related files:** New `src/pages/onboarding.py`, `src/pages/homepage.py`
- **Estimate:** 6-10h
- **Competitive Gap:** 🟡 No TW competitor has onboarding personalization

---

#### [ISSUE-C14] Company Health Score (Visual Radar)
- **Source:** Competitor research (Round 3, Simply Wall St snowflake + Stockopedia StockRank)
- **Priority:** P1 (BLOCKED by business_card.py completion — Challenger Round 3)
- **Status:** 📋 Todo
- **Description:**
  - Simply Wall St's "snowflake" and Stockopedia's "StockRank" both provide at-a-glance company scores.
  - Stock Explorer's adaptive engine already analyzes all the data needed — it just needs a scoring layer.
  - A 5-axis radar chart (Profitability, Growth, Financial Health, Dividend, Stability) with a 0-100 score per axis.
  - Displayed on the business card page as a summary widget + explainable breakdown ("Your Profitability score is 85/100 because your gross margin is 55%, well above industry average").
  - Differentiates from Simply Wall St: our scores are explainable (plain-language reasoning per axis), not just visual.
- **Suggested Implementation:**
  - New `src/services/health_scorer.py` — scoring algorithm per axis using existing financial data
  - Plotly radar chart on business card page
  - Plain-language explanation per axis (reuse explanation_engine.py patterns)
  - Compare mode: overlay two companies' radars (Simply Wall St comparison feature)
- **Related files:** `src/services/health_scorer.py`, `src/pages/business_card.py`
- **Estimate:** 14-20h
- **Competitive Gap:** 🔴 No TW competitor has explainable company health scoring

---

#### [ISSUE-C15] Paper Trading Simulator
- **Source:** Competitor research (Round 3, Investopedia Simulator)
- **Priority:** Deferred (Challenger Round 3: positioning violation — "historian, not stock picker")
- **Status:** ❌ Canceled (requires Daniel approval to reframe as educational back-testing)
- **Description:**
  - Investopedia's stock simulator is the gold standard for beginner practice.
  - NO Taiwanese competitor offers paper trading.
  - Virtual $1M NTD portfolio: users "buy" stocks based on what they learned on Stock Explorer.
  - Tracks virtual P&L using real FinMind price data.
  - Educational framing: "Practice what you learned — no risk, no regret."
  - Aligns with "historian" position: the goal is "did you understand the company" not "did you make money."
- **Suggested Implementation:**
  - New `src/pages/simulator.py` — portfolio management page
  - Virtual portfolio stored in `config/virtual_portfolio.yaml`
  - Buy/sell interface with position tracking
  - P&L calculation using FinMind real-time price feeds (read-only, no real trading)
  - Performance summary: "You've analyzed 12 companies and 'invested' in 7. Your best pick: +12% (TSMC), worst: -3% (Foxconn)"
- **Related files:** New `src/pages/simulator.py`, `src/services/virtual_portfolio.py`, `config/virtual_portfolio.yaml`
- **Estimate:** 20-30h
- **Competitive Gap:** 🟡 P2 (no TW competitor has this, but also not core to education mission)

---

#### [ISSUE-C16] "Did You Know?" Contextual Company Tips
- **Source:** Competitor research (Round 3, Stash "Stock Bits")
- **Priority:** P2
- **Status:** ✅ Done
- **Description:**
  - Stash embeds mini-facts next to stock details. Stock Explorer does this with contextual facts matching the analysis framework.
- **Implementation (complete):**
  - `src/data/company_facts.yaml` — 70 facts for 7 stocks (2330, 2454, 2317, 1101, 2881, 0050) ✅
  - `src/services/company_facts.py` — Service layer with `get_company_facts()` and `get_random_fact()` ✅
  - `src/pages/business_card.py` lines 142-157 — UI rendering with rotating tip card ✅
- **Related files:** `src/data/company_facts.yaml`, `src/services/company_facts.py`, `src/pages/business_card.py`
- **Estimate:** Already implemented (was 4-6h, done in prior cycle)
- **Competitive Gap:** 🟡 Unique feature — no TW competitor has contextual company facts

---

#### [ISSUE-C17] AI Company Q&A
- **Source:** Competitor research (Round 3, emerging LLM wrapper trend)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Since 2024, "LLM + FinMind" wrappers have proliferated on GitHub.
  - Stock Explorer already has the best structured analysis — but lacks freeform Q&A.
  - Add "Ask about this company" input on each company page.
  - Uses existing `explanation_engine.py` context + LLM to answer natural language questions.
  - Example: "Why is TSMC's capex so high?" → "TSMC spends ~$30B/year building new factories because chip demand keeps growing..."
  - Defense against LLM wrapper competitors: our answers are grounded in verified FinMind data + adaptive framework.
- **Suggested Implementation:**
  - New `src/services/qa_engine.py` — formats existing analysis context as LLM prompt
  - Input box on each company page (subtle, not prominent — add-on, not replacement)
  - Full conversation context from current page data (reduces hallucination)
  - Rate limiting to manage API costs
  - **Architecture decision required:** Use local LLM (privacy, cost) or API (quality, latency)?
- **Related files:** New `src/services/qa_engine.py`, all company page modules
- **Estimate:** 10-14h
- **Competitive Gap:** 🔴 Defensive feature — counters "LLM wrapper" threat from 2024+ TW startups

---

#### [ISSUE-C18] Gamified Learning Progress (Badges + Streaks)
- **Source:** Competitor research (Round 3, cross-cutting analysis — NO competitor has this)
- **Priority:** Deferred (Challenger Round 3: no core value alignment, add to D+ product premature)
- **Status:** 📋 Todo (post-MVP)
- **Description:**
  - Cross-cutting analysis across ALL 15+ competitors (TW + international) reveals that NO platform gamifies stock education.
  - Duolingo proved that gamification (streaks, XP, badges) dramatically increases retention.
  - Stock Explorer application: track learning progress, award badges, show streaks.
  - Badges: "Analyst in Training" (analyze 3 companies), "Dividend Detective" (explore dividend data for 5 companies), "Peer Reviewer" (compare 10 peer pairs)
  - Streak: "You've explored companies for 5 days straight! 🔥"
  - Progress: "You've completed 4/8 analysis sections for TSMC"
  - This is a WHITE SPACE that NO competitor occupies — first-mover advantage.
- **Suggested Implementation:**
  - New `src/services/gamification.py` — badge definitions, progress tracking, streak calculation
  - Track in `config/user_progress.yaml`
  - Badge display on homepage and business card page
  - Progress bar on company pages ("You've explored 3/7 sections")
  - **Key design constraint:** Gamification must SUPPORT education, not distract from it (no leaderboards, no social comparison)
- **Related files:** New `src/services/gamification.py`, `config/user_progress.yaml`, homepage, all company pages
- **Estimate:** 12-16h
- **Competitive Gap:** 🔴 Unique — NO competitor (TW or international) gamifies stock education

---

#### [ISSUE-C19] Structured Learning Path with Guidance
- **Source:** Competitor research (Round 3, Investopedia structured paths + Acorns Money Basics)
- **Priority:** P1 (elevated from P2 — Challenger Round 3: strongest alignment with "Story first" and "Point-to-point" core values)
- **Status:** 📋 Todo
- **Description:**
  - Investopedia and Acorns both use structured learning paths ("Start here → next → next → quiz").
  - Stock Explorer's pages ARE a learning path (business card → operations → financial health → peers → events), but there's no explicit guidance or flow.
  - Beginners see 9 pages in the sidebar and don't know which to click first.
  - Add an explicit "Start Here" guided flow on homepage that walks through one company end-to-end.
  - "Start with TSMC → Step 1: What does TSMC make? (Business Card) → Step 2: Is it making money? (Operations) → ..."
- **Suggested Implementation:**
  - New `src/pages/learning_path.py` — guided step-by-step walkthrough
  - Each step embeds the relevant page section with instructional overlay
  - "Next" button guides to the next analysis step
  - Complete the path → earn "First Analysis Complete" badge (links to ISSUE-C18)
  - Multiple paths: "Quick Overview" (3 steps), "Deep Dive" (7 steps), "Dividend Focus" (4 steps)
- **Related files:** New `src/pages/learning_path.py`, homepage
- **Estimate:** 14-18h
- **Competitive Gap:** 🟡 P2 — No TW competitor has guided learning flow

---

## 📊 Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 25 |
| 🔄 In progress | 0 |
| ✅ Done | 7 |
| ❌ Canceled | 0 |

| Priority | Count |
|----------|-------|
| P0 | 4 |
| P1 | 8 |
| P2 | 15 |

---

*Last updated: 2026-06-11 (Challenger Round 3 stress test — business_card.py truncation P0 identified, priorities adjusted)*

---

## 🔴 Round 3 Challenger Critical Finding

### [ISSUE-D-002-NEW] business_card.py Severely Truncated — P0 Regression
- **Source:** Challenger Round 3 direct source code verification (2026-06-11)
- **Priority:** P0 (CRITICAL — regression from B+ to D+)
- **Status:** ✅ Done
- **Fix (2026-06-12):** Restored from 128 lines to 370 lines. All 7 rendering sections restored: one-liner, key metrics cards, dividend story, revenue pie chart, revenue trend, news, disclaimer. Multi-list watchlist UI preserved.
- **Description:**
  - `business_card.py` is only 128 lines. The `_render_business_card()` function imports 15+ service functions (chart, revenue, analogy, dividend, news) but calls **NONE** of them
  - Page renders ONLY: stock name, price, watchlist buttons
  - Revenue chart, pie chart, news, dividend, analogy sections are all imported but never rendered
  - This is the main entry page of the app — every user sees this broken page first
  - **Regression:** Round 2 grade was B+, now D+. Something broke between rounds.
- **Challenger's user journey evidence:**
  ```
  User opens Stock Explorer → Types "2330" → Clicks "TSMC" →
  → Sees: "TSMC 2330 ｜ 半導體業" + price + watchlist button
  → Nothing else. No revenue chart. No news. No dividend. No analogy.
  → User thinks: "Is this broken?" → Closes tab.
  ```
- **Impact:** Every user on every visit to the main page sees a blank page. #1 cause of user churn.
- **Estimated effort to fix:** 8-12 hours (revenue section ~3h, dividend section ~2h, news section ~2h, key metrics cards ~2h, testing ~2h)
- **Unblocks:** C14 (Health Radar), C16 ("Did You Know?"), C01 dividend rendering
- **Related files:** `src/pages/business_card.py`
- **Verification:** Direct read of source file confirmed zero calls to imported services
- **Reference:** `docs/workflow/challenge_log.md` — Round 1 Q2, Round 2 Q2

---


---

## 💡 Discussion Round 4 — 2026-06-11 (Team Discussion + Challenger)

### Process Summary
- **Architect** (nemotron-120b): Root cause = commit 9277bbd truncated 173 lines during multi-list watchlist refactor. Recommends git-based Option A recovery (restore from commit 24d785b + rebase multi-list changes). Effort: 45min-3h for restore, but full integration ~10h. "MVP = stabilize, not add."
- **Design Reviewer** (gemma-31b): Defined minimum viable card (Tier 1: revenue pie + trend + one-liner + key metrics). C14 Health Score = highest UX impact. Estimated 15h for design-complete MVP. C17 AI Q&A = HIGH RISK (hallucination).
- **Developer** (owl-alpha): 10-subtask breakdown (~10.6h total). Missing import `list_names` at line 78. Revenue breakdown limited to 8 hardcoded companies. C07→C14→C06 recommended order.
- **Challenger** (gpt-oss-120b): **REJECTED** team plan — 3 rounds of challenge. Key objections: C06 advances zero core values; C01 "Done" is false; plan doesn't advance "Story first"; building C14 on broken page = compound risk.

### Challenger's 3-Round Summary
| Round | Focus | Key Objection |
|-------|-------|---------------|
| 1 | Feature Direction | C06 is delivery mechanism for content that isn't ready; C01 status is wrong |
| 2 | Priority | M5 must precede C07; YAML→SQLite premature; DR-03 should be P0 |
| 3 | Goal Alignment | Zero features advance "Story first"; no verification gates; C02 rabbit hole un-scoped |

### Revised Roadmap (Post-Challenger Confirmed)

| Phase | Items | Hours | Gate |
|-------|-------|-------|------|
| **Phase 0 — Stabilize** | business_card.py restore + 5 quick tech debt + DR-03 Financial Health | 11-15h | Main page grades B+ |
| **Phase 1 — Foundation** | D01 M5 verification + C16 "Did You Know?" + C07 Custom Thresholds | 18-22h | M5 accuracy >80% |
| **Phase 2 — Core Features** | C19 Learning Path + C14 Health Score + C02 Email | 44-54h | business_card.py complete |
| **Phase 3 — Share & Expand** | C06 PPT Generation + C04 Market Thermometer | 34-38h | All pages B+ |
| **Post-MVP** | YAML→SQLite + C17 AI Q&A + C13 Quiz + TD-11/12/15 | 18-24h | Multi-user need |

### New Issues from Discussion Round

#### [ISSUE-C20] C01 Ex-Dividend Calendar Status Correction
- **Source:** Discussion Round 4 (Challenger Round 1)
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:** ISSUE-C01 is marked ✅ Done in issues.md but the dividend rendering section was never wired into business_card.py due to the truncation regression. The `dividend_analyzer.py` service exists and works, but `_render_business_card()` never calls `extract_dividend_summary()`. Must be restored as part of business_card.py fix.
- **Related files:** `src/pages/business_card.py`, `src/services/dividend_analyzer.py`
- **Effort:** Included in D-002-NEW fix

#### [ISSUE-DR-06] Financial Health Page P0 Promotion
- **Source:** Discussion Round 4 (Challenger Round 2)
- **Priority:** P0 (promoted from P1)
- **Status:** 📋 Todo
- **Description:** DR-03 (Financial Health text-heavy) promoted to P0 by Challenger. Only 1.5h fix, worst-graded core page (C+), highest-ROI fix in backlog. Must be done before C06 (PPT Generation) since PPT captures page content.
- **Related files:** `src/pages/financial_health.py`
- **Effort:** 1.5 hours

### Status Changes from Discussion Round

| Issue | Previous Status | New Status | Reason |
|-------|----------------|------------|--------|
| C06 PPT Generation | Phase 1 | Phase 3 | Advances zero core values; pages must be excellent first |
| C19 Learning Path | P2 | Phase 2 (P1) | Best "Story first" alignment; addresses #1 UX problem |
| C15 Paper Trading | Deferred | ❌ Canceled | Positioning violation ("historian, not stock picker") |
| C18 Gamification | P2 | Deferred post-MVP | No core value alignment for D+ product |
| DR-03 Financial Health | P1 | P0 | Highest-ROI fix; worst-graded core page |
| C01 Ex-Dividend | ✅ Done | 📋 Todo (status false) | Never wired into business_card.py |

### Updated Issue Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 23 |
| ✅ Done | 7 |
| ❌ Canceled | 2 |
| 🔄 In progress | 0 |

| Priority | Count |
|----------|-------|
| P0 | 5 |
| P1 | 6 |
| P2 | 10 |

---

## 🌍 Round 4 — Competitor Research (2026-06-11, New Angles: AI-Native, TW Startups, ELI5)

### Process Summary
- **Focus areas:** Emerging AI-powered tools (2025-2026), TW fintech startups, international beginner apps, financial literacy platforms, ELI5 approaches
- **8 new competitors analyzed** not covered in Rounds 1-3
- **2 critical threats identified:** Plotch.ai (story cards ≈ PPT style) and TW LLM wrapper bots (messaging-native UX)
- **7 new feature ideas generated** (3 high priority, 3 medium, 1 low)

### New Competitors Analyzed

| Competitor | Type | Threat Level | Key Finding |
|---|---|---|---|
| Plotch.ai | AI story cards | 🔴 High | Direct UX overlap with PPT style; social sharing built-in |
| 股市AI / TW LLM Bots | LINE/Telegram bots | 🔴 High | Messaging-native UX; zero learning curve; proliferating |
| Yahoo Finance AI Reports | AI summaries | 🟡 Medium | Bull/Bear framing; massive distribution |
| Magnify / Compose AI | AI doc analysis | 🟡 Medium | Cross-period comparison; no education framework |
| Kavout | AI stock scoring | 🟢 Low | US-only; no education features |
| TipRanks | Analyst tracking | 🟢 Low | Active trader audience; not beginner-focused |
| FinGuild / Communities | Community learning | 🟢 Low | Complements Stock Explorer; validates demand |
| Taster.finance | Micro-learning | 🟢 Low | Different category; spaced repetition is innovative |

### New Feature Ideas from Round 4

#### [ISSUE-C21] LINE Bot Interface for Stock Explorer
- **Source:** Competitor research round 4 (股市AI / TW LLM bots)
- **Priority:** P1 (elevated from P2 — counters critical messaging-native threat)
- **Status:** 📋 Todo
- **Description:**
  - Taiwanese LLM wrapper bots on LINE/Telegram are proliferating — zero learning curve, messaging-native UX
  - Stock Explorer has NO messaging presence; users must open a website
  - Phase 1: Read-only bot — user sends "2330" → bot replies with TSMC summary card
  - Phase 2: Interactive — user taps "Tell me more about revenue" → bot sends revenue card
  - Phase 3: Push — bot proactively sends event alerts
  - Technology: LINE Messaging API + FastAPI backend + existing analysis services
  - Competitive Gap: 🔴 Critical — counters "LLM wrapper bot" threat
- **Related files:** New `src/bot/line_bot.py`, `src/bot/card_builder.py`
- **Estimate:** 16-24h for Phase 1
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 5

---

#### [ISSUE-C22] Bull Case / Bear Case Balanced Framing
- **Source:** Competitor research round 4 (Yahoo Finance AI Research Reports)
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - Yahoo Finance's AI Research Reports present balanced bull/bear cases for stocks
  - No TW platform offers balanced framing — most are either neutral or bullish
  - Add optional "Bull Case / Bear Case" section to business card page
  - Example for TSMC:
    - 🐂 Bull Case: "TSMC controls 90% of advanced chip manufacturing. AI demand growing 30%/year."
    - 🐻 Bear Case: "TSMC spends $30B/year on factories. Geopolitical risk from Taiwan tensions."
  - Aligns with "historian" positioning: presents multiple perspectives without recommending
  - Competitive Gap: 🟡 Medium — no TW platform does balanced framing
- **Related files:** `src/pages/business_card.py`, new `src/services/bull_bear_engine.py`
- **Estimate:** 8-12h
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 3

---

#### [ISSUE-C23] "Why Now" Narrative Card
- **Source:** Competitor research round 4 (Plotch.ai "Why Now" card)
- **Priority:** P1
- **Status:** 📋 Todo
- **Description:**
  - Plotch.ai's "Why Now" card connects companies to current events and trends
  - Stock Explorer's event dashboard shows WHAT happened but not WHY it matters
  - Add "Why This Company Matters Right Now" card to business card page
  - Example: "TSMC matters right now because: (1) AI chip demand surging — NVIDIA, Apple, AMD all need 3nm chips. (2) Arizona factories could change global supply chains."
  - Makes company data feel relevant and timely for beginners
  - Competitive Gap: 🟡 Medium — connects data to narrative context
- **Related files:** `src/pages/business_card.py`, new `src/data/why_now.yaml`
- **Estimate:** 6-10h (manual content for top 20 stocks, then template)
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 7

---

#### [ISSUE-C24] Interactive "Calculate It Yourself" Exercises
- **Source:** Competitor research round 4 (Taster.finance interactive exercises)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Taster.finance has mini interactive exercises where users manually calculate metrics
  - Stock Explorer shows metrics but never asks users to calculate them (passive vs. active learning)
  - Add 5 mini-exercises to financial health page:
    - "TSMC's annual dividend is $11/share. Stock price is $850. What's the dividend yield?"
    - "Revenue $100B, costs $60B. What's the gross margin?"
  - Immediate feedback: "Correct! 1.3% — that's lower than the bank's savings rate."
  - Competitive Gap: 🟡 Medium — no TW stock platform has interactive exercises
- **Related files:** `src/pages/financial_health.py`
- **Estimate:** 4-6h for 5 exercises
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 8

---

#### [ISSUE-C25] Social Sharing Buttons
- **Source:** Competitor research round 4 (Plotch.ai story card sharing)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Plotch.ai has built-in social sharing — every shared story card = new user acquisition
  - Stock Explorer has ZERO viral distribution mechanism
  - Add "Share to LINE / Facebook / Copy Link" buttons to each analysis page
  - Generate shareable summary card (image format) with key metrics + one analogy
  - Example share card: "台積電 TSMC ｜ 半導體業 ｜ 毛利率 55% → 每賣100元賺55元 ｜ 🏭 護城河：全球90%先進晶片"
  - Competitive Gap: 🟡 Medium — zero-cost user acquisition channel
- **Related files:** All page modules, new `src/services/share_card.py`
- **Estimate:** 6-10h
- **Reference:** `docs/research/competitor_research_round4.md` — White Space Analysis

---

#### [ISSUE-C26] "Today's Company" Daily Narrative
- **Source:** Competitor research round 4 (Taster.finance "Today's Company")
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Taster.finance uses one company as the example for ALL concepts each day
  - Creates narrative continuity and daily engagement loop
  - Add "Company of the Day" to Stock Explorer homepage
  - All metric explanations on that day use the featured company as the example
  - Creates reason to return daily (new company each day)
  - Competitive Gap: 🟢 Low — engagement/retention feature, not core education
- **Related files:** `src/pages/homepage.py`, new `src/data/company_of_day.yaml`
- **Estimate:** 4-6h
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 8

---

#### [ISSUE-C27] Spaced Repetition Concept Review
- **Source:** Competitor research round 4 (Taster.finance spaced repetition)
- **Priority:** P2 (post-MVP)
- **Status:** 📋 Todo
- **Description:**
  - Taster.finance retests previously learned concepts over time (Duolingo model)
  - Stock Explorer has no retention mechanism — users learn a metric once, never see it again
  - Track which financial concepts the user has encountered
  - Periodically retest: "You learned P/E ratio 7 days ago. Quick refresher!"
  - Competitive Gap: 🟢 Low — unique education feature, no competitor has it
  - Post-MVP: requires user tracking infrastructure
- **Related files:** New `src/services/spaced_repetition.py`, `config/user_progress.yaml`
- **Estimate:** 10-14h
- **Reference:** `docs/research/competitor_research_round4.md` — Competitor 8

---

### Updated Issue Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 30 |
| ✅ Done | 7 |
| ❌ Canceled | 2 |
| 🔄 In progress | 0 |

| Priority | Count |
|----------|-------|
| P0 | 5 |
| P1 | 9 |
| P2 | 15 |

---

---

## 💡 Discussion Round 5 — 2026-06-12 (Team Discussion + Challenger 3-Round Challenge)

### Process Summary
- **Architect** (nemotron-120b): Proposed 3 directions — D01 M5 verification (6-8h), DR-03+C16 combined (6-8h), C14 Health Score (10-14h). Excluded C02 (blocked by D02), C06 (wrong order), C07 (needs D01 first).
- **Design Reviewer** (gemma-31b): Provided DR-03 deep dive with line-level rewrite plan for financial_health.py. Ranked all 9 pages by design urgency. Category Browser and Group Structure are worst (grade D).
- **Developer** (owl-alpha): ROI ranking — DR-03 (3h) > C02 in-app (2h) > C01 (5h) > D01 (6.5h) > C07 (5.5h) > C14 (8.5h). Key finding: M5 is already wired and events.yaml has 8 real events. business_card.py already has dividend UI.
- **Challenger** (gpt-oss-120b): **REJECTED** initial PM proposal. Required modifications: (1) D01 must be first (not third), (2) Merge DR-03+C01 financial_health.py into single integrated redesign, (3) Add C16 "Did You Know?" (cheapest "Story first" feature), (4) Add design checkpoint before C14, (5) C14 budget is 8.5h underestimate — realistically 14-20h

### Challenger's 3-Round Summary
| Round | Focus | Key Objection |
|-------|-------|---------------|
| 1 | Feature Direction | ZERO items advance "Story first" (#1 core value); team is in "safe planning" mode |
| 2 | Priority | D01 should be first not third; DR-03+C01 financial_health.py are mutually exclusive; C14 at 8.5h is underestimated |
| 3 | Goal Alignment | 5 overlooked risks (scoring validation, DR-03+C01 conflict, design system enforcement, 22-28h is 35-45% underestimated) |

### Final Decision (Post-Challenger Confirmed)

| Order | Item | Hours | Core Value |
|-------|------|-------|------------|
| 1 | **D01**: M5 Verification + Integration | 4-6h | #3 Adaptive |
| 2 | **DR-03+C01**: Financial Health Redesign (integrated) | 4-5h | #2 PPT-style |
| 3 | **C01**: Ex-dividend countdown + badge (business_card only) | 2-3h | Data completeness |
| 4 | **C16**: "Did You Know?" Company Facts | 4-6h | #1 Story first |
| 5 | **C14**: Health Score Badge (reduced scope, 4-6h) OR Full Radar (14-20h) | 4-20h | #2 PPT-style, #5 Benchmark |

**Total: 18-40h** (depending on C14 scope decision)

### C01 Status Correction
- C01 status corrected: dividend UI was restored in business_card.py P0 fix (370 lines)
- Remaining C01 work: countdown-to-ex-date, visual badge (2-3h)
- Financial_health.py dividend wiring merged into DR-03 redesign

### Design Pages Urgency Ranking (Design Reviewer)
1. Category Browser (D) + Group Structure (D) — worst, need structural redesign
2. My Watchlist (C-) — high-frequency page
3. Operational Checkup (C) — #2 in tab order
4. Peer Comparison (C) — comparison needs clear hierarchy
5. Financial Health (C+) — DR-03 addresses this
6. Business Card (C+) — P0 fix restored content
7. ETF Detail (B+) — minor polish
8. Event Dashboard (A-) — best, extract patterns

### New Issues from Discussion Round

#### [ISSUE-D04] M5 Event Detection Pipeline Integration
- **Source:** Discussion Round 5 (Team + Challenger)
- **Priority:** P0
- **Status:** ✅ Done
- **Description:** M5 event detection engine is built and wired. Error isolation added for run_auto_detection() in router.py. False positive filtering and dedup with normalized titles verified working.
- **Fix (2026-06-12):** Added try/except around all M5 event detection + rendering calls in router.py. Verified false positive exclusion works. Added test for 合併營收 false positive. Cleaned up stale false positive in events.yaml.
- **Estimate:** 4-6h (actual: ~3h — core integration was already done)
- **Related files:** `src/services/adaptive_engine.py`, `src/pages/_router_base.py`, `src/pages/event_dashboard.py`
- **Commit:** `b042936`, `d3645c4`

#### [ISSUE-D05] DR-03 + C01 Financial Health Integrated Redesign
- **Source:** Discussion Round 5 (Challenger Round 2 — merged DR-03 and C01 financial_health.py)
- **Priority:** P0
- **Status:** ✅ Done
- **Description:** DR-03 (text reduction) and C01 (dividend wiring) both target financial_health.py — must be a single integrated redesign. Specific text-cut targets: (1) Profit funnel _info_card (lines 70-74, ~220 chars → ~35 chars), (2) Eliminate redundant funnel section card (lines 40-75), (3) Cash flow 3-branch _info_card (lines 235-244, ~62 chars → ~16 chars), (4) Debt health HTML block (lines 188-196, ~140 chars → ~20 chars with gauge bar), (5) Balance sheet 3 cards (lines 164-171, ~103 chars → ~15 chars with stacked bar). Add dividend gauge as one visual replacement.
- **Fix (2026-06-12):** All 3 parts completed. Text reduced across all 4 sections. Dividend gauge added as Section 5. Component consistency achieved — #F39C12 replaced with #3498DB. Line count: 248→275. L0: 54/54 ✅ | L1: 15/15 ✅.
- **Related files:** `src/pages/financial_health.py`

#### [ISSUE-D06] C14 Health Score Scope Decision
- **Source:** Discussion Round 5 (Challenger Round 3)
- **Priority:** P1
- **Status:** 📋 Todo (awaiting Daniel's decision on scope)
- **Description:** Challenger flagged 8.5h estimate as unrealistic for quality implementation. Options: (A) Health Score Badge (simple 0-100 with color coding, 4-6h) or (B) Full 5-axis Radar Chart with plain-language explanations per axis (14-20h). **Requires Daniel's decision.**
- **Estimate:** 4-6h (Option A) or 14-20h (Option B)
- **Related files:** `src/services/health_scorer.py` (new), `src/pages/business_card.py`

#### [ISSUE-C16-NEW] "Did You Know?" Company Facts
- **Source:** Discussion Round 5 (Challenger Round 1 — replaced C14 as story-first feature)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:** Add contextual company facts to business_card.py. Create `src/data/company_facts.yaml` with {stock_id: [{fact, category}]} structure. Display as rotating tip card. Seed with 20-30 facts for top 10 stocks. "💡 你知道嗎？台積電生產全球 90% 的先進晶片，每一支 iPhone 15 Pro 裡面都有台積電的 3 奈米晶片。"
- **Estimate:** 4-6h
- **Related files:** `src/data/company_facts.yaml` (new), `src/pages/business_card.py`

### Status Changes from Discussion Round

| Issue | Previous Status | New Status | Reason |
|-------|----------------|------------|--------|
| C01 Ex-Dividend | 📋 Todo (falsely Done) | 📋 Todo (corrected) | business_card.py restored dividend UI; remaining: countdown (2-3h) |
| DR-03 Financial Health | P1 → P0 | P0 (confirmed) | Integrated with C01 into single redesign |
| C14 Health Score | P1 | P1 (scope decision needed) | Challenger: 8.5h → 14-20h; needs Daniel decision: badge vs radar |

### Updated Issue Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 27 |
| 🔄 In progress | 0 |
| ✅ Done | 12 |
| ❌ Canceled | 2 |

| Priority | Count |
|----------|-------|
| P0 | 3 |
| P1 | 8 |
| P2 | 15 |

---

*Last updated: 2026-06-12 (Discussion Round 5 — team discussion + Challenger 3-round challenge)*

---

## 🌍 Round 5 — Competitor Research (2026-06-12, Emerging Trends: 2025-2026 Launches, AI-Native, TW/Asian Market)

### Process Summary
- **Focus areas:** 2025-2026 AI-first financial education tools, mobile-first stock education apps, novel teaching methods, TW/Asian fintech startups, emerging patterns
- **8 new competitors analyzed** not covered in Rounds 1-4
- **2 critical threats identified:** StockStory (AI narratives + TW coverage) and Stockopedia AI (comprehensive AI education + TW coverage)
- **6 new feature ideas generated** (2 high priority, 3 medium, 1 low)

### New Competitors Analyzed

| Competitor | Type | Threat Level | Key Finding |
|---|---|---|---|
| StockStory | AI company narratives | 🔴 High | AI-generated "stock stories" + TW coverage + "Turning Points" timeline = direct overlap with "historian" positioning |
| Stockopedia AI | AI stock analysis + education | 🔴 High | 2025 AI relaunch added "AI Explain" + "AI Stock Story" + "TW Market Education Hub" |
| Moomoo / Futubull | AI education features | 🟡 Medium-High | AI Course Generator + Social Learning Feed + Paper Trading with AI Feedback |
| Sensical | Daily micro-learning | 🟡 Medium | AI-adaptive learning path + Traditional Chinese support (targeting TW/HK) |
| 玉山證券 | Broker education push | 🟡 Medium | "Beginner Village" + ESG Screener + Investment Health Check |
| Finqle | Gamified learning (TW) | 🟡 Medium | Swipe-based UX + daily challenges + "Learn & Earn" model; validates gamification demand |
| Finimize | AI financial newsletter | 🟡 Medium | "Finimize Academy" + "Ask Finimize" AI Q&A + "Market Mood" indicator |
| TW Telegram Bots | Messaging-native bots | 🟡 Medium-High | Evolving rapidly; now offer structured analysis, interactive charts, paper trading |

### Emerging Trends (2025-2026)

1. **AI-Generated Company Narratives** — becoming table stakes; multiple platforms offer this
2. **Personalized Learning Paths** — AI-generated adaptive learning is the new standard
3. **Social + Mobile-First Learning** — TikTok-style feeds, swipe-based UX, messaging-native
4. **ESG Integration in Education** — growing area of beginner interest
5. **AI Q&A as Table Stakes** — users expect natural language Q&A
6. **Gamification of Financial Education** — "Duolingo for finance" model gaining traction

### New Feature Ideas from Round 5

#### [ISSUE-C28] Company Story Timeline with AI-Generated Narrative
- **Source:** Competitor research round 5 (StockStory AI narratives, Stockopedia AI "AI Stock Story")
- **Priority:** P1 (elevated from P2 — AI narratives are becoming table stakes; StockStory + Stockopedia AI both have this with TW coverage)
- **Status:** 📋 Todo
- **Description:**
  - StockStory (Singapore, 2025) generates AI narratives for TW stocks with "Turning Points" timeline
  - Stockopedia AI (2025 relaunch) has "AI Stock Story" + "TW Market Education Hub" in Traditional Chinese
  - Both directly compete with Stock Explorer's "historian" positioning
  - Add a "Company Story" tab to each company page with: (1) chronological narrative from FinMind data, (2) "Turning Points" timeline (5-10 key moments), (3) "Story Updates" for recent events, (4) "Compare Stories" for peer comparison
  - This is the #1 feature gap from Round 5 — AI-generated company narratives are becoming standard
- **Suggested Implementation:**
  - New `src/services/narrative_engine.py` — generates company narrative from FinMind data + event history
  - New `src/pages/company_story.py` — story timeline page with turning points
  - "Turning Points" algorithm: identify top 5-10 events by impact (revenue spike, price crash, major news)
  - "Compare Stories" mode: overlay two companies' timelines (extends ISSUE-C11)
- **Related files:** New `src/services/narrative_engine.py`, new `src/pages/company_story.py`, `src/services/adaptive_engine.py`
- **Estimate:** 20-30h
- **Competitive Gap:** 🔴 Critical — AI-generated company narratives are becoming table stakes; StockStory + Stockopedia AI both have this with TW coverage
- **Reference:** `docs/research/competitor_research_round5.md` — Competitor 2 (StockStory), Competitor 7 (Stockopedia AI)

---

#### [ISSUE-C29] AI-Powered "Explain Any Metric" Feature
- **Source:** Competitor research round 5 (Stockopedia AI "AI Explain", Finimize "Ask Finimize")
- **Priority:** P1 (elevated from P2 — AI-powered metric explanations are becoming standard)
- **Status:** 📋 Todo
- **Description:**
  - Stockopedia AI's "AI Explain" lets users highlight any metric and get a plain-language explanation with context
  - Finimize's "Ask Finimize" Q&A answers natural language questions about any financial concept
  - Stock Explorer currently shows metrics but offers no contextual explanation — users must already know what "ROE: 28.5%" means
  - Add an "Explain" button (ℹ️ icon) next to every financial metric across all pages
  - Clicking opens: (1) what the metric means, (2) how to interpret the current value, (3) what's "good" vs "bad" for this industry, (4) a real-world analogy
  - Example: "ROE: 28.5% → Return on Equity measures how efficiently a company uses shareholder money. 28.5% means TSMC generates $28.50 profit for every $100 of shareholder equity. This is excellent — the semiconductor industry average is 15%."
  - Differentiates from ISSUE-C12 (Glossary): glossary is a reference document; "Explain Any Metric" is contextual, inline, and adaptive to the specific value
- **Suggested Implementation:**
  - New `src/services/metric_explainer.py` — generates contextual explanations for any metric
  - Template-based explanations with industry-specific benchmarks
  - ℹ️ icon next to every metric in all page modules
  - Expandable tooltip or modal with the explanation
  - Can be enhanced with LLM in v2 (ISSUE-C17 integration)
- **Related files:** New `src/services/metric_explainer.py`, all page modules (add ℹ️ icons)
- **Estimate:** 12-18h
- **Competitive Gap:** 🔴 High — AI-powered metric explanations are becoming standard; Stockopedia AI already has this
- **Reference:** `docs/research/competitor_research_round5.md` — Competitor 7 (Stockopedia AI)

---

#### [ISSUE-C30] ESG Education Integration
- **Source:** Competitor research round 5 (玉山證券 ESG Screener, international ESG education trend)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - 玉山證券 launched an ESG stock screener with plain-language explanations in 2025
  - International platforms (Sensical, Finimize) increasingly integrate ESG into financial education
  - Beginners are increasingly asking "Is this company good for the world?" alongside "Is this company profitable?"
  - No TW stock education platform teaches ESG concepts alongside financial analysis
  - Add an ESG section to the Business Card page or as a new page
  - Content: (1) what ESG means (Environmental, Social, Governance), (2) why it matters for investors, (3) how to evaluate a company's ESG performance, (4) plain-language ESG scores for TW companies
  - Example: "TSMC's ESG Score: 85/100. 🌱 Environmental: A (renewable energy investment, water recycling). 👥 Social: B+ (good benefits, but long fab hours). 🏛️ Governance: A (independent board, transparent reporting)."
- **Suggested Implementation:**
  - New `src/services/esg_analyzer.py` — ESG scoring and explanation engine
  - ESG section on Business Card page (compact) or new ESG page (comprehensive)
  - Plain-language ESG explanations with emoji indicators (🌱👥🏛️)
  - ESG data source: TWSE ESG reports, or manual curation for top 50 stocks initially
- **Related files:** New `src/services/esg_analyzer.py`, `src/pages/business_card.py` or new ESG page
- **Estimate:** 10-16h
- **Competitive Gap:** 🟡 Medium — growing area of beginner interest; no TW platform does this well
- **Reference:** `docs/research/competitor_research_round5.md` — Competitor 4 (玉山證券)

---

#### [ISSUE-C31] Daily Financial Challenge
- **Source:** Competitor research round 5 (Finqle daily challenges, Taster.finance daily lessons, Sensical weekly quiz)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Finqle (TW, 2025) has daily financial challenges with points and leaderboards
  - Taster.finance has daily lessons with "Today's Company" concept
  - Sensical has weekly quizzes with "Weekly Wisdom" summary cards
  - Stock Explorer has NO daily engagement mechanism — users visit when they want to look up a stock, with no reason to return daily
  - Add a "Daily Challenge" card to the homepage — a single question that tests a financial concept using real stock data
  - Users answer, get immediate feedback, and track their streak
  - Example: "Today's Challenge: TSMC's stock price is $850. It pays $11 in annual dividends. What's the dividend yield? A) 1.3% B) 2.5% C) 5.0%"
  - Correct answer → "Correct! 1.3%. That's like a savings account — but TSMC also grows its dividend over time."
  - Streak tracking: "You've answered 5 days straight! 🔥"
  - Lightweight gamification — no leaderboards, no social comparison (aligns with ISSUE-C18 design constraints)
- **Suggested Implementation:**
  - New `src/services/daily_challenge.py` — challenge generator with question bank
  - Question bank: 100+ questions covering key financial concepts (dividend yield, P/E, ROE, gross margin, etc.)
  - Each question uses real FinMind data for a random stock
  - Streak tracking in `session_state` (no backend required)
  - Daily challenge card on homepage
- **Related files:** New `src/services/daily_challenge.py`, `src/pages/homepage.py`
- **Estimate:** 6-10h
- **Competitive Gap:** 🟡 Medium — daily engagement loop drives retention; no TW platform does this
- **Reference:** `docs/research/competitor_research_round5.md` — Competitor 6 (Finqle), Competitor 8 (TW Telegram Bots)

---

#### [ISSUE-C32] "Market Mood" Sentiment Indicator
- **Source:** Competitor research round 5 (Finimize "Market Mood" indicator)
- **Priority:** P2
- **Status:** 📋 Todo
- **Description:**
  - Finimize has a "Market Mood" indicator (😰 Fear → 😊 Neutral → 🤩 Greed) that aggregates news sentiment, social media buzz, and market data
  - This validates ISSUE-C04 (Market Thermometer) with a simpler, more engaging UX
  - Instead of a complex thermometer with multiple data sources, a single emoji-based mood indicator with a one-sentence explanation
  - Example: "Market Mood: 😊 Neutral — Institutional investors are buying slightly more than selling. No major news today. Market is calm."
  - Displayed on the homepage or event dashboard
  - Can be expanded to sector-level mood: "Semiconductor sector mood: 🤩 Greed — AI chip demand news driving optimism"
- **Suggested Implementation:**
  - New `src/services/market_mood.py` — sentiment aggregation engine
  - Data sources: institutional investor buy/sell (FinMind), news event frequency (adaptive engine), market volume
  - Simple 3-level mood: 😰 Fear / 😊 Neutral / 🤩 Greed
  - One-sentence plain-language explanation
  - Display on homepage (compact) and event dashboard (detailed)
- **Related files:** New `src/services/market_mood.py`, `src/pages/homepage.py`, `src/pages/event_dashboard.py`
- **Estimate:** 8-12h
- **Competitive Gap:** 🟢 Low — validates existing ISSUE-C04; Finimize's version is simpler and more engaging
- **Reference:** `docs/research/competitor_research_round5.md` — Competitor 3 (Finimize)

---

### Updated Issue Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 37 |
| ✅ Done | 7 |
| ❌ Canceled | 2 |
| 🔄 In progress | 0 |

| Priority | Count |
|----------|-------|
| P0 | 6 |
| P1 | 10 |
| P2 | 21 |

---

*Last updated: 2026-06-12 (Round 5 Competitor Research — 8 new competitors, 5 new feature ideas, 2 critical threats identified)*
