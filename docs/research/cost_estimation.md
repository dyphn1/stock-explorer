# Stock Explorer Cost Estimation Report

> **Date**: 2026-06-12
> **Estimator**: Developer (Subagent)
> **Scope**: Technical debt fixes, design improvements, and new features
> **Basis**: tech_debt.md (12 active items + 7 new), design_comparison_review.md (39 design issues), issues.md (27 feature items), competitor_research_round4.md (7 new features), competitor_research_round5.md (5 new features)
> **Assumptions**: Single developer, familiar with the codebase; estimates include coding + basic testing; excludes extensive QA or design review cycles.
> **Previous Estimate**: 51 items, 241.9 hours (2026-06-11)
> **This Round**: +25 items, +67.8 hours → **76 items, 309.7 hours**

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ Done | Completed and verified |
| 🔄 In Progress | Currently being worked on |
| 📋 Not Started | Planned but not yet started |
| ❌ Canceled | Removed from scope |

---

## A. Technical Debt Fixes

### A1. Immediate Items (This Week)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| TD-01 | Commit `uv.lock` | 0.1 (5 min) | ✅ Done | Low | Low | None | Lock file now exists on disk. |
| TD-02 | Extract shared timeline constants | 0.2 (10 min) | 📋 Not Started | Low | Low | None | Create `src/services/timeline.py` with `_TIMELINE_DAYS` dict. |
| TD-03 | Add logging to `_fetch()` inner function | 0.2 (10 min) | 📋 Not Started | Low | Low | None | Add `logging.warning()` in `except Exception` block. |
| TD-04 | Handle `FinMindRateLimitError` visibility | 0.25 (15 min) | ✅ Done | Low | Low | None | Fixed in `_router_base.py` line 44. Sets `st.session_state["_rate_limited"]`. |
| TD-05 | Fix `st.session_state` in tests | 0.5 (30 min) | ✅ Done | Low | Low | None | Down to 1 necessary usage. |
| NEW-G08 | Add `list_names` to import block in `business_card.py` | 0.02 (1 min) | 📋 Not Started | Low | Low | None | 🔴 HIGH — runtime crash bug. Latent `NameError` at line 78. |
| NEW-G09 | Remove unused imports from `business_card.py` | 0.08 (5 min) | 📋 Not Started | Low | Low | None | 15+ service functions imported but never called. |
| NEW-G01 | Consolidate `_atomic_write` | 0.25 (15 min) | 📋 Not Started | Low | Low | None | Extract to `src/services/storage_util.py`. |
| NEW-G04 | Fix disconnected rate limit flags | 0.17 (10 min) | 📋 Not Started | Low | Low | None | `_rate_limited` session state set but never read. |
| **NEW-G10** | Remove dead `get_list_entries()` | 0.03 (2 min) | 📋 Not Started | Low | Low | None | Function defined but never called. Dead code. |
| **NEW-G11** | Remove/adopt `INDUSTRY_REVENUE_MAP` (39 lines) | 0.02 (1 min) / 1.0 (adopt) | 📋 Not Started | Low | Low | None | 39-line dict, 0 references. Remove or integrate into revenue logic. |
| **NEW-G12** | Remove dead `_section_card` assignment | 0.02 (1 min) | 📋 Not Started | Low | Low | None | Variable assigned but never read. |
| **NEW-G14** | Deduplicate `_is_etf()` logic | 0.5 (30 min) | 📋 Not Started | Low | Low | None | Same logic in watchlist.py and adaptive_engine.py. Extract to shared util. |

**Immediate Subtotal: ~2.6 hours (0.5 done, 2.1 remaining)**
*(was 1.3h; +0.07h G10 +0.02/1.0h G11 +0.02h G12 +0.5h G14 = +0.61h quick wins or +1.59h if adopting G11)*

> **NEW-G13** (`_MISSING_COL_WARNED` unbounded growth): **Deferred** — tracked as D01. No cost this round.

---

### A2. Short-Term Items (Next 2 Weeks)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| TD-06 | Add tests for event detection & validation | 3.0 | ✅ Done | Medium | Low | TD-05 | 59 new unit tests added. 88 total. |
| TD-07 | Make `max_workers` configurable | 0.3 (20 min) | 📋 Not Started | Low | Low | None | Add parameter with default=5. |
| TD-08 | Optimize category browser N+1 queries | 2.0 | 📋 Not Started | Medium | Medium | None | Reduce to top 50 + "show more" + batch fetch. |
| TD-09 | Cache ETF dividend data | 1.5 | 📋 Not Started | Medium | Low | None | `@st.cache_data(ttl=604800)` on dividend fetch. |
| TD-10 | Consolidate static company data | 2.0 | 📋 Not Started | Medium | Low | None | Create `src/data/company_registry.yaml`. |
| TD-11 | Add type checking configuration | 2.0 | 📋 Not Started | Medium | Low | None | Start with `src/services/` and `src/data/`. |
| NEW-G02 | Remove dead `models.py` or adopt it | 0.3 (5 min) | 📋 Not Started | Low | Low | None | 86 lines, 6 dataclasses, 0 imports. Remove option. |
| NEW-G05 | Fix ETF category classification priority | 0.5 (30 min) | 📋 Not Started | Low | Low | None | Document priority order or use explicit scoring. |
| NEW-G06 | Remove bare `FinMindClient()` in peer_comparison | 0.3 (20 min) | 📋 Not Started | Low | Low | None | Accept as parameter instead. |

**Short-Term Subtotal: ~11.8 hours (3.0 done, 8.8 remaining)**

---

### A3. Medium-Term Items (Post-MVP)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| TD-12 | Abstract storage + SQLite backend | 4.0 | 📋 Not Started | High | Medium | TD-10 | ABC interface + YAML/SQLite backends. |
| TD-13 | Fix rate limit global state | 1.0 | 📋 Not Started | Medium | Low | TD-04 | Move module globals to `st.session_state`. |
| TD-14 | Integration tests with saved API responses | 3.0 | 📋 Not Started | Medium | Medium | TD-06 | Snapshot tests with JSON fixtures. |
| TD-15 | Pagination for large lists | 1.0 | 📋 Not Started | Low | Low | TD-08 | 20 items per page with nav buttons. |
| TD-16 | "Last known good" data fallback | 2.0 | 📋 Not Started | Medium | Medium | TD-12 | Serve most recent successful response. |

**Medium-Term Subtotal: ~11.0 hours (all remaining)**

---

## B. Design Improvements

### B1. Quick Wins (Round 5 Additions)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| **D-046** | Remove gradient from business_card.py | 0.25 (15 min) | 📋 Not Started | Low | Low | None | One-liner CSS removal. |
| **D-047** | Revenue breakdown cards box-shadow fix | 0.5 (30 min) | 📋 Not Started | Low | Low | None | Replace box-shadow with flat design token. |
| **D-050** | etf_browser.py ETF explainer card gradient | 0.5 (30 min) | 📋 Not Started | Low | Low | None | Remove gradient, use flat background. |
| **D-051** | group_structure.py gradient banner | 0.25 (15 min) | 📋 Not Started | Low | Low | None | Remove gradient from banner CSS. |
| **D-059** | _info_card() orange border global fix | 0.25 (15 min) | 📋 Not Started | Low | Low | None | 🔴 1-line fix! Orange border leaks to ALL pages. |

**Quick Wins Subtotal: ~1.75 hours (all remaining)**

### B2. Medium Effort (Round 5 Additions)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| **D-048** | News section cards raw HTML refactor | 1.0 | 📋 Not Started | Low | Low | None | Replace raw HTML with Streamlit-native components. |
| **D-052** | group_structure.py st.bar_chart → Plotly | 1.0 | 📋 Not Started | Low | Low | None | Consistent chart library usage. |
| **D-060** | financial_health.py dividend gauge raw HTML | 1.0 | 📋 Not Started | Low | Low | None | Replace with native components. |
| **D-062** | Add CSS custom properties / design tokens | 2.0 | 📋 Not Started | Medium | Low | None | Centralize colors, spacing, typography. Enables all future design consistency. |

**Medium Effort Subtotal: ~5.0 hours (all remaining)**

### B3. Larger Effort (Round 5 Additions)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| **D-049** | category_browser.py structural redesign | 3.0 | 📋 Not Started | Medium | Medium | None | 3 unrelated sections need separation. |
| **D-053-D-058** | chart.py color constant violations (×6) | 3.0 | 📋 Not Started | Low | Low | None | 6 fixes × 30 min each. Replace hardcoded colors with design tokens. |
| **D-061** | peer_comparison.py metric card inconsistency | 1.5 | 📋 Not Started | Medium | Low | None | Align card styling with design system. |

**Larger Effort Subtotal: ~7.5 hours (all remaining)**

### B4. Previously Estimated Items

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| DI-01 | Fix color system violations (6 files) | 1.0 | 📋 Not Started | Low | Low | None | Replace illegal colors across 6 files. |
| DI-02 | Remove `st.cache_data` from View layer | 0.5 | ✅ Done | Low | Medium | None | Removed from peer_comparison.py and etf_browser.py. |
| DI-03 | Fix Zone A violation in business_card.py | 0.5 | 📋 Not Started | Low | Low | None | Move watchlist buttons from navbar to content area. |
| DI-04 | Standardize card components | 2.0 | 📋 Not Started | Medium | Medium | DI-03 | Replace inline HTML with `_白话_card()` / `_info_card()`. |
| DI-05 | Reduce text on financial_health.py | 1.5 | 📋 Not Started | Medium | Low | DI-04 | Condense 4 sections to 2-3. Add `st.expander()`. |
| DI-06 | Improve responsive column layouts | 1.5 | 📋 Not Started | Medium | Medium | None | CSS grid for card layouts, media queries. |
| DI-07 | Add text alternatives to severity badges | 0.3 (20 min) | 📋 Not Started | Low | Low | None | WCAG 1.4.1 compliance. |
| DI-08 | Standardize chart colors | 1.0 | 📋 Not Started | Low | Low | DI-01 | Replace chart-specific colors with design palette. |
| DR-03 | Financial Health page P0 promotion | 1.5 | 📋 Not Started | Medium | Low | None | **Promoted to P0 by Challenger Round 4.** Worst-graded core page (C+). Highest-ROI fix. |
| D-002-NEW | business_card.py truncation fix | 10.0 | 📋 Not Started | High | High | None | **P0 CRITICAL.** 128-line file, 15+ imports unused. Revenue/dividend/news never rendered. |

**Previously Estimated Subtotal: ~19.8 hours (0.5 done, 19.3 remaining)**

**Design Improvements Grand Total: ~34.05 hours (0.5 done, 33.55 remaining)**
*(was 19.8h; +14.25h from Round 5)*

---

## C. New Features

### C1. Core Features (MVP Path)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| NF-D01 | M5 Event Detection Verification | 4.0 | 📋 Not Started | Medium | High | None | Run against real FinMind data for 10+ stocks. **Blocker for C07.** |
| NF-D02 | Background Worker Architecture Investigation | 6.0 | 📋 Not Started | High | High | None | Research: pull-on-visit vs APScheduler vs cron. **Blocker for C02.** |
| C07 | Customizable Event Thresholds | 12.0 | 📋 Not Started | Medium | Medium | NF-D01 | Settings page for event sensitivity. |
| C04 | Market Thermometer | 14.0 | 📋 Not Started | Medium | Medium | None | Institutional buy/sell + volume + limit-up/down ratio. |
| C02 | Notification/Push System (Email phase) | 16.0 | 📋 Not Started | High | High | NF-D02 | SMTP + notification preferences. |
| C06 | Auto-Generate Stock Analysis PPT | 20.0 | 📋 Not Started | High | Medium | DI-04 | **Moved to Phase 3** per Challenger Round 4. Pages must be excellent first. |

**Core Features Subtotal: ~72.0 hours (all remaining)**

### C2. Round 4 New Features (Competitor Response)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| C21 | LINE Bot Interface (Phase 1) | 20.0 | 📋 Not Started | High | High | None | **P1 — counters critical messaging-native threat.** Read-only bot → summary card. FastAPI + LINE Messaging API. |
| C22 | Bull Case / Bear Case Balanced Framing | 10.0 | 📋 Not Started | Medium | Medium | None | **P1 — from Yahoo Finance AI Reports.** Optional balanced perspective section. |
| C23 | "Why Now" Narrative Card | 8.0 | 📋 Not Started | Medium | Medium | None | **P1 — from Plotch.ai.** Connects company to current events. Manual content for top 20 stocks. |
| C24 | Interactive "Calculate It Yourself" Exercises | 5.0 | 📋 Not Started | Medium | Low | None | **P2 — from Taster.finance.** 5 mini-exercises on financial health page. |
| C25 | Social Sharing Buttons | 8.0 | 📋 Not Started | Medium | Medium | None | **P2 — from Plotch.ai.** Share to LINE/Facebook/Copy Link. |
| C26 | "Today's Company" Daily Narrative | 5.0 | 📋 Not Started | Low | Low | None | **P2 — from Taster.finance.** Homepage daily engagement loop. |
| C27 | Spaced Repetition Concept Review | 12.0 | 📋 Not Started | Medium | Medium | None | **P2 post-MVP — from Taster.finance.** Duolingo-style concept retesting. |

**Round 4 New Features Subtotal: ~68.0 hours (all remaining)**

### C3. Other Feature Ideas (Not Prioritized)

| ID | Item | Hours | Status | Complexity | Risk | Dependencies | Notes |
|----|------|-------|--------|------------|------|--------------|-------|
| C19 | Structured Learning Path | 16.0 | 📋 Not Started | Medium | Medium | None | **Phase 2 per Discussion Round 4.** "Start Here" guided flow. |
| C14 | Company Health Score (Visual Radar) | 17.0 | 📋 Not Started | Medium | Medium | None | **BLOCKED by business_card.py completion.** 5-axis radar chart. |
| C16 | "Did You Know?" Contextual Tips | 5.0 | 📋 Not Started | Low | Low | None | **Phase 1 per Discussion Round 4.** Manual facts for top stocks. |
| C17 | AI Company Q&A | 12.0 | 📋 Not Started | High | High | None | Defensive vs LLM wrapper threat. Architecture decision needed. |
| C13 | Investment Personality Quiz | 8.0 | 📋 Not Started | Low | Low | None | Onboarding personalization. |
| C01 | Ex-Dividend Calendar (status corrected) | (included in D-002-NEW) | 📋 Not Started | — | — | — | Was falsely marked ✅ Done. Now part of business_card.py fix. |

**Other Features Subtotal: ~58.0 hours (all remaining)**

### C4. Round 5 New Features (Competitor Response)

| ID | Item | Low | High | Avg | Status | Complexity | Risk | Dependencies | Notes |
|----|-----|-----|------|-----|--------|------------|------|--------------|-------|
| **ISSUE-C28** | Company Story Timeline with AI Narrative | 16.0 | 24.0 | 20.0 | 📋 Not Started | High | High | None | **P1 — Singapore StockStory.ai inspired.** AI-generated company history timeline. Requires LLM integration + event data. |
| **ISSUE-C29** | AI-Powered "Explain Any Metric" | 10.0 | 14.0 | 12.0 | 📋 Not Started | High | High | None | **P1 — Stockopedia AI Explain inspired.** Contextual tooltips with LLM explanations. |
| **ISSUE-C30** | ESG Education Integration | 8.0 | 12.0 | 10.0 | 📋 Not Started | Medium | Medium | None | **P2 — 玉山證券 ESG inspired.** ESG scores + educational content. |
| **ISSUE-C31** | Daily Financial Challenge | 6.0 | 10.0 | 8.0 | 📋 Not Started | Medium | Low | None | **P2 — Sensical daily quiz inspired.** Gamified daily engagement. |
| **ISSUE-C32** | "Market Mood" Sentiment Indicator | 4.0 | 8.0 | 6.0 | 📋 Not Started | Low | Low | None | **P2 — Finimize Market Mood inspired.** Simple sentiment gauge. |

**Round 5 New Features Subtotal: ~56.0 hours (all remaining)**

---

## Summary Table

| Priority Group | Items | Total Hours | Done | Remaining | Key Risks |
|----------------|-------|-------------|------|-----------|-----------|
| **A1. Immediate** (This Week) | TD-01..05, NEW-G01, G04, G08, G09, G10, G11, G12, G14 | 2.6 hrs | 0.5 hrs | 2.1 hrs | NEW-G08 is hidden crash bug |
| **A2. Short-Term** (Next 2 Weeks) | TD-06..11, NEW-G02, G05, G06 | 11.8 hrs | 3.0 hrs | 8.8 hrs | Category browser optimization may need iteration |
| **A3. Medium-Term** (Post-MVP) | TD-12..16 | 11.0 hrs | 0 hrs | 11.0 hrs | Storage abstraction requires careful migration |
| **B. Design Improvements** | DI-01..08, DR-03, D-002-NEW, D-046..062 | 34.05 hrs | 0.5 hrs | 33.55 hrs | D-002-NEW is P0 critical (10h) |
| **C1. Core Features** | C02, C04, C06, C07, D01, D02 | 72.0 hrs | 0 hrs | 72.0 hrs | D02 is hard blocker for C02 |
| **C2. Round 4 Features** | C21..C27 | 68.0 hrs | 0 hrs | 68.0 hrs | C21 LINE Bot is highest priority |
| **C3. Other Features** | C01, C13, C14, C16, C17, C19 | 58.0 hrs | 0 hrs | 58.0 hrs | C14 blocked by business_card.py |
| **C4. Round 5 Features** | C28..C32 | 56.0 hrs | 0 hrs | 56.0 hrs | C28/C29 require LLM integration |
| **GRAND TOTAL** | **76 items** | **313.5 hrs** | **4.0 hrs** | **309.5 hrs** | |

---

## Completed Items (4 hours total)

| Item | Hours | Completed | Verification |
|------|-------|-----------|-------------|
| TD-01: Commit `uv.lock` | 0.1 hrs | ✅ 2026-06-10 | Lock file exists on disk |
| TD-04: Handle `FinMindRateLimitError` | 0.25 hrs | ✅ 2026-06-10 | `_router_base.py` line 44 |
| TD-05: Fix `st.session_state` in tests | 0.5 hrs | ✅ 2026-06-10 | Down to 1 usage |
| TD-06: Add tests for event detection | 3.0 hrs | ✅ 2026-06-10 | 59 new tests, 88 total |
| DI-02: Remove `st.cache_data` from View | 0.15 hrs | ✅ 2026-06-10 | 0 occurrences in src/ |

---

## Round 5 Changes Log

### New Items Added (25 items, +67.6 hours)

| Category | Items | Hours Added | Notes |
|----------|-------|-------------|-------|
| **Tech Debt** | NEW-G10, G11, G12, G13, G14 | +1.6 hrs | G13 deferred; G11 has remove (1 min) or adopt (1h) options |
| **Design** | D-046..D-062 | +14.3 hrs | 13 new design issues from Round 5 review |
| **Features** | ISSUE-C28..C32 | +56.0 hrs | 5 new competitor-inspired features from Round 5 |
| **Total** | **25 items** | **+67.6 hrs** | Previous: 241.9h → New: 309.5h (remaining) |

### Estimate Adjustments

| Item | Previous | New | Reason |
|------|----------|-----|--------|
| Design Improvements total | 19.8h | 34.05h | +14.25h from Round 5 design issues |
| Grand Total (remaining) | 237.9h | 309.5h | +71.6h from all Round 5 items |

---

## ROI Ranking (Highest ROI = Lowest Cost, Highest Impact)

### Tier 1 — Fix First (Quick Wins, High Impact)

| Rank | ID | Item | Hours | Impact | ROI Score | Notes |
|------|----|------|-------|--------|-----------|-------|
| 1 | **NEW-G08** | Fix missing `list_names` import | 0.02h (1 min) | 🔴 Critical | ⭐⭐⭐⭐⭐ | Prevents runtime crash on every page load |
| 2 | **D-059** | _info_card() orange border fix | 0.25h (15 min) | 🔴 High | ⭐⭐⭐⭐⭐ | 1-line fix, affects ALL pages |
| 3 | **NEW-G12** | Remove dead `_section_card` | 0.02h (1 min) | Low | ⭐⭐⭐⭐ | Dead code cleanup |
| 4 | **NEW-G10** | Remove dead `get_list_entries()` | 0.03h (2 min) | Low | ⭐⭐⭐⭐ | Dead code cleanup |
| 5 | **D-046** | Remove gradient business_card.py | 0.25h (15 min) | Medium | ⭐⭐⭐⭐ | One-liner CSS fix |
| 6 | **D-051** | group_structure.py gradient removal | 0.25h (15 min) | Medium | ⭐⭐⭐⭐ | One-liner CSS fix |
| 7 | **DI-07** | Add text alternatives to badges | 0.3h (20 min) | Medium | ⭐⭐⭐⭐ | WCAG compliance |
| 8 | **NEW-G11** | Remove `INDUSTRY_REVENUE_MAP` | 0.02h (1 min) | Low | ⭐⭐⭐⭐ | 39 lines dead code |

### Tier 2 — Do Next (Low Cost, Medium Impact)

| Rank | ID | Item | Hours | Impact | ROI Score | Notes |
|------|----|------|-------|--------|-----------|-------|
| 9 | **NEW-G14** | Deduplicate `_is_etf()` | 0.5h (30 min) | Medium | ⭐⭐⭐ | Reduces maintenance burden |
| 10 | **D-047** | Revenue breakdown box-shadow | 0.5h (30 min) | Medium | ⭐⭐⭐ | Design consistency |
| 11 | **D-050** | etf_browser.py gradient removal | 0.5h (30 min) | Medium | ⭐⭐⭐ | Design consistency |
| 12 | **TD-02** | Extract timeline constants | 0.2h (10 min) | Medium | ⭐⭐⭐ | Code organization |
| 13 | **TD-03** | Add logging to `_fetch()` | 0.2h (10 min) | Medium | ⭐⭐⭐ | Debugging improvement |
| 14 | **ISSUE-C32** | "Market Mood" Sentiment | 6h | Medium | ⭐⭐⭐ | Low-cost feature, high engagement |
| 15 | **DI-01** | Fix color system violations | 1.0h | Medium | ⭐⭐⭐ | Design compliance |

### Tier 3 — Plan Soon (Medium Cost, High Impact)

| Rank | ID | Item | Hours | Impact | ROI Score | Notes |
|------|----|------|-------|--------|-----------|-------|
| 16 | **ISSUE-C31** | Daily Financial Challenge | 8h | Medium | ⭐⭐ | Engagement driver |
| 17 | **ISSUE-C30** | ESG Education Integration | 10h | Medium | ⭐⭐ | Competitive parity |
| 18 | **D-062** | CSS custom properties | 2.0h | High | ⭐⭐ | Enables all future design consistency |
| 19 | **ISSUE-C29** | AI "Explain Any Metric" | 12h | High | ⭐⭐ | P1 feature, LLM integration |
| 20 | **ISSUE-C28** | Company Story Timeline | 20h | High | ⭐⭐ | P1 feature, LLM integration |

### Tier 4 — Post-MVP (High Cost, Strategic)

| Rank | ID | Item | Hours | Impact | ROI Score | Notes |
|------|----|------|-------|--------|-----------|-------|
| 21 | **D-002-NEW** | business_card.py fix | 10h | 🔴 Critical | ⭐ | P0 but high effort |
| 22 | **C21** | LINE Bot Interface | 20h | High | ⭐ | New tech stack |
| 23 | **C22** | Bull/Bear Case | 10h | Medium | ⭐ | Content generation |

---

## Recommended Execution Order (Updated)

### Phase 0 — Stabilize (Week 1): ~12-16 hours
**Goal: Main page grades B+**

1. **D-002-NEW**: Complete business_card.py (10 hrs) — 🔴 P0 CRITICAL
   - Restore revenue chart, pie chart, news, dividend, analogy sections
   - Fix missing `list_names` import (NEW-G08, 1 min)
   - Remove unused imports (NEW-G09, 5 min)
2. **DR-03**: Fix Financial Health page text-heavy sections (1.5 hrs) — 🔴 P0
3. **D-059**: Fix _info_card() orange border (15 min) — 🔴 1-line fix
4. **DI-01**: Fix color system violations (1 hr)
5. **DI-07**: Add text alternatives to severity badges (20 min)
6. **DI-03**: Fix Zone A violation in business_card.py (30 min)
7. **Quick wins batch**: NEW-G10, G11, G12, G14, D-046, D-051 (~1 hr combined)

### Phase 1 — Foundation (Week 2-3): ~20-25 hours
**Goal: M5 accuracy >80%**

8. **NF-D01**: M5 Event Detection Verification (4 hrs)
9. **C16**: "Did You Know?" Contextual Tips (5 hrs)
10. **C07**: Customizable Event Thresholds (12 hrs) — after D01 verification
11. **TD-08**: Optimize category browser N+1 queries (2 hrs)
12. **ISSUE-C32**: "Market Mood" Sentiment Indicator (6 hrs) — quick win feature

### Phase 2 — Core Features (Weeks 4-6): ~44-54 hours
**Goal: business_card.py complete, all pages B+**

13. **C19**: Structured Learning Path (16 hrs)
14. **C14**: Company Health Score (17 hrs) — unblocked by D-002-NEW
15. **C02**: Notification/Push System Email (16 hrs) — after D02
16. **NF-D02**: Background Worker Architecture (6 hrs) — can start early as investigation

### Phase 3 — Share & Expand (Weeks 7-9): ~34-38 hours
**Goal: Viral distribution + advanced features**

17. **C06**: Auto-Generate Stock Analysis PPT (20 hrs)
18. **C04**: Market Thermometer (14 hrs)
19. **C25**: Social Sharing Buttons (8 hrs) — pairs well with C06

### Phase 4 — Round 4 Competitive Response (Weeks 10-12): ~38-42 hours
**Goal: Counter messaging-native threat**

20. **C21**: LINE Bot Interface Phase 1 (20 hrs) — 🔴 Highest priority new feature
21. **C22**: Bull Case / Bear Case (10 hrs)
22. **C23**: "Why Now" Narrative Card (8 hrs)

### Phase 5 — Round 5 Competitive Response (Weeks 13-15): ~36-42 hours
**Goal: AI-powered differentiation**

23. **ISSUE-C29**: AI "Explain Any Metric" (12 hrs) — P1
24. **ISSUE-C28**: Company Story Timeline with AI (20 hrs) — P1
25. **ISSUE-C30**: ESG Education Integration (10 hrs) — P2
26. **ISSUE-C31**: Daily Financial Challenge (8 hrs) — P2

### Post-MVP — Scalability + Advanced (Weeks 16+): ~40-50 hours
27. **TD-12**: Abstract storage + SQLite (4 hrs)
28. **TD-13**: Fix rate limit global state (1 hr)
29. **TD-14**: Integration tests (3 hrs)
30. **TD-16**: "Last known good" fallback (2 hrs)
31. **C17**: AI Company Q&A (12 hrs)
32. **C13**: Investment Personality Quiz (8 hrs)
33. **C27**: Spaced Repetition (12 hrs)
34. **TD-11**: Type checking (2 hrs)
35. **TD-15**: Pagination (1 hr)

---

## Critical Path (Updated)

```
D-002-NEW (business_card.py fix, 10h) ──→ C14 (Health Score, 17h)
                                        ──→ C01 (Dividend, included)
                                        ──→ C16 (Tips, 5h)
                                        ──→ C21 (LINE Bot, 20h)
                                        ──→ C22 (Bull/Bear, 10h)
                                        ──→ C23 (Why Now, 8h)

NF-D01 (M5 Verification, 4h) ──→ C07 (Custom Thresholds, 12h)

NF-D02 (Worker Architecture, 6h) ──→ C02 (Notifications, 16h)

D-002-NEW (business_card.py) ──→ ISSUE-C28 (Story Timeline, 20h)
                                ──→ ISSUE-C29 (Explain Metric, 12h)

DI-04 (Card Standardization) ──→ DI-05 (Reduce Text) ──→ C06 (PPT, 20h)

DI-01 (Color Fixes) ──→ DI-08 (Chart Colors)

D-062 (Design Tokens) ──→ All future design consistency
```

**Longest path to MVP**: D-002-NEW (10h) → C14 (17h) = **27 hours** for core page functionality
**Full MVP with design compliance**: Phase 0 + Phase 1 = **32-41 hours**
**Competitive parity (with Round 4 features)**: Phases 0-4 = **140-173 hours**
**Full competitive (with Round 5 features)**: Phases 0-5 = **176-215 hours**

---

## Risk Assessment

### High Risk Items
- **D-002-NEW (business_card.py truncation)**: P0 regression. Main page is broken. Every user sees a blank page. #1 cause of churn. Must be fixed before anything else.
- **NF-D02 (Background Worker Architecture)**: Streamlit is request-response only. True push notifications require external infrastructure. Risk of scope creep.
- **C21 (LINE Bot Interface)**: New technology stack (FastAPI + LINE Messaging API). Learning curve. LINE Bot account setup and approval process.
- **NF-D01 (M5 Verification)**: Event detection may have bugs that only show with real data. Could invalidate C07's foundation.
- **C17 (AI Company Q&A)**: Hallucination risk. Architecture decision (local vs API LLM) unresolved.
- **ISSUE-C28 (Company Story Timeline)**: LLM integration complexity. Hallucination risk for historical facts. Requires careful prompt engineering.
- **ISSUE-C29 (AI Explain Metric)**: LLM integration. Must ensure financial accuracy. Regulatory considerations.

### Medium Risk Items
- **TD-08 (Category Browser)**: 200 sequential API calls. Caching helps but cold cache is still painful.
- **DI-06 (Responsive Layouts)**: Streamlit's `st.columns()` doesn't auto-wrap. CSS grid requires testing.
- **C06 (PPT Generation)**: python-pptx learning curve. Chart rendering (kaleido) can be finicky.
- **C14 (Health Score)**: Scoring algorithm design requires domain expertise. Must be explainable, not black-box.
- **C22 (Bull/Bear)**: Content generation for balanced framing. Risk of appearing to give investment advice.
- **ISSUE-C30 (ESG Education)**: ESG data source availability. Content accuracy requirements.
- **D-049 (category_browser.py redesign)**: Structural changes may affect existing functionality.

### Low Risk Items
- All Immediate items (TD-01..05, NEW-G01, G04, G08..G12, G14)
- All color fixes (DI-01, DI-08, DI-07, D-046..062)
- TD-07, TD-09, TD-10, TD-11
- C24, C25, C26, C31, C32 (small scoped features)

---

## Dependency Graph

```
NF-D01 (M5 Verification, 4h) ──────┐
                                    ├──→ C07 (Custom Thresholds, 12h)
                                    │
NF-D02 (Worker Architecture, 6h) ──┴──→ C02 (Notifications, 16h)

D-002-NEW (business_card.py, 10h) ──→ C14 (Health Score, 17h)
                                    ──→ C16 (Tips, 5h)
                                    ──→ C21 (LINE Bot, 20h)
                                    ──→ C22 (Bull/Bear, 10h)
                                    ──→ C23 (Why Now, 8h)
                                    ──→ ISSUE-C28 (Story Timeline, 20h)
                                    ──→ ISSUE-C29 (Explain Metric, 12h)

TD-05 (Test Fix) ──→ TD-06 (Event Tests) ──→ TD-14 (Integration Tests)

TD-10 (Data Consolidation) ──→ TD-12 (Storage Abstraction) ──→ TD-16 (Last Known Good)

DI-04 (Card Standardization) ──→ DI-05 (Reduce Text) ──→ C06 (PPT Generation)

DI-01 (Color Fixes) ──→ DI-08 (Chart Colors)

D-062 (Design Tokens) ──→ D-046..061 (All design consistency fixes)

DR-03 (Financial Health P0) ──→ C06 (PPT captures page content)
```

---

## Notes on Estimation Approach

1. **Estimates include**: Coding time, basic unit/local testing, and documentation updates.
2. **Estimates exclude**: Extensive QA cycles, cross-browser testing, design review iterations, deployment.
3. **Buffer**: Add 15-20% buffer for unexpected issues, especially for High complexity items.
4. **Parallelization**: Items within the same sprint can often be parallelized if multiple developers are available.
5. **Confidence**: Immediate items ±10%, Short-term ±20%, Medium-term ±30%, New Features ±40%, LINE Bot ±50% (new tech stack), LLM features ±50% (ISSUE-C28, C29).
6. **Round 4 additions**: C21-C27 are new from competitor research round 4 (2026-06-11). Estimates are preliminary.
7. **Round 5 additions**: ISSUE-C28-C32 are new from competitor research round 5 (2026-06-12). C28/C29 involve LLM integration — highest uncertainty.

---

## Cost Scenarios

| Scenario | Phases | Hours | Weeks (1 dev) | Description |
|----------|--------|-------|---------------|-------------|
| **MVP Core** | Phase 0 + 1 | 32-41 hrs | 1-1.5 weeks | Main pages functional, design compliance |
| **MVP + Competitive** | Phases 0-2 | 76-95 hrs | 2-3 weeks | + Notifications, Health Score, Learning Path |
| **Full Feature** | Phases 0-3 | 110-133 hrs | 3-4 weeks | + PPT, Market Thermometer, Social Sharing |
| **With Round 4** | Phases 0-4 | 140-173 hrs | 4-5 weeks | + LINE Bot, Bull/Bear, Why Now |
| **With Round 5** | Phases 0-5 | 176-215 hrs | 5-6 weeks | + AI Timeline, Explain Metric, ESG, Challenges |
| **Complete** | All phases | 310-335 hrs | 8-9 weeks | Everything including post-MVP |

---

*Total estimated remaining effort: **309.5 hours** (approximately 8-9 developer weeks at 35 hrs/week)*
*With 20% buffer: **~371 hours** (~10-11 developer weeks)*
*Completed so far: **4.0 hours** (5 items)*
*Round 5 added: **+71.6 hours** (25 items: 5 tech debt, 13 design, 5 features, 2 deferred)*
