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
- **Status:** 📋 Todo
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

## 📊 Statistics

| Status | Count |
|--------|-------|
|| 📋 Todo | 10 |
| 🔄 In progress | 0 |
| ✅ Done | 3 |
| ❌ Canceled | 0 |

|| Priority | Count |
|----------|-------|
|| P0 | 4 |
| P1 | 4 |
| P2 | 3 |

---

*Last updated: 2026-06-10 (team discussion + challenger round)*
*Source: Team discussion with Architect, Design Reviewer, Developer, Challenger*
