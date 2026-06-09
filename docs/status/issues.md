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
- **Status:** 📋 Todo
- **Description:**
  - GoodInfo and Dogga (財報狗) both have complete ex-dividend information
  - One of the most common beginner questions: "When does TSMC pay dividends and how much?"
  - Stock Explorer currently cannot answer this question at all
  - Recommendation: add a "Dividend Information" section to the Business Card page
- **Suggested Implementation:**
  - Ex-dividend/ex-rights schedule for the past 5 years (ex-dividend date, ex-rights date)
  - Historical dividends (cash dividends, stock dividends)
  - Plain-language explanation (e.g., "Over the past 5 years, TSMC has paid approximately NT$2.75 per quarter")
  - Estimated dividend yield (calculated from current stock price)
- **Data Feasibility:** FinMind has the `TaiwanStockDividend` API
- **Related files:** `src/pages/business_card.py`
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

## 📊 Statistics

| Status | Count |
|--------|-------|
| 📋 Todo | 10 |
| 🔄 In progress | 0 |
| ✅ Done | 0 |
| ❌ Canceled | 0 |

| Priority | Count |
|----------|-------|
| P0 | 3 |
| P1 | 4 |
| P2 | 3 |

---

*Last updated: 2026-06-09 (competitor research round)*
*New feature source: `docs/research/competitor_research.md` competitor research report*
