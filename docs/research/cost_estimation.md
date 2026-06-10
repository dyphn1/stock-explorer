# Stock Explorer Cost Estimation Report

> **Date**: 2026-06-11
> **Estimator**: Developer (Subagent)
> **Scope**: Technical debt fixes, design improvements, and new features
> **Basis**: tech_debt.md (12 active items + 2 new), design_comparison_review.md (26 design issues), issues.md (27 feature items), competitor_research_round4.md (7 new features)
> **Assumptions**: Single developer, familiar with the codebase; estimates include coding + basic testing; excludes extensive QA or design review cycles.
> **Previous Estimate**: 35 items, 103.4 hours (2026-06-10)

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

**Immediate Subtotal: ~1.3 hours (0.5 done, 0.8 remaining)**

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

**Design Improvements Subtotal: ~19.8 hours (0.5 done, 19.3 remaining)**

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

---

## Summary Table

| Priority Group | Items | Total Hours | Done | Remaining | Key Risks |
|----------------|-------|-------------|------|-----------|-----------|
| **A1. Immediate** (This Week) | TD-01..05, NEW-G01, G04, G08, G09 | 1.3 hrs | 0.5 hrs | 0.8 hrs | NEW-G08 is hidden crash bug |
| **A2. Short-Term** (Next 2 Weeks) | TD-06..11, NEW-G02, G05, G06 | 11.8 hrs | 3.0 hrs | 8.8 hrs | Category browser optimization may need iteration |
| **A3. Medium-Term** (Post-MVP) | TD-12..16 | 11.0 hrs | 0 hrs | 11.0 hrs | Storage abstraction requires careful migration |
| **B. Design Improvements** | DI-01..08, DR-03, D-002-NEW | 19.8 hrs | 0.5 hrs | 19.3 hrs | D-002-NEW is P0 critical (10h) |
| **C1. Core Features** | C02, C04, C06, C07, D01, D02 | 72.0 hrs | 0 hrs | 72.0 hrs | D02 is hard blocker for C02 |
| **C2. Round 4 Features** | C21..C27 | 68.0 hrs | 0 hrs | 68.0 hrs | C21 LINE Bot is highest priority |
| **C3. Other Features** | C01, C13, C14, C16, C17, C19 | 58.0 hrs | 0 hrs | 58.0 hrs | C14 blocked by business_card.py |
| **GRAND TOTAL** | **51 items** | **241.9 hrs** | **4.0 hrs** | **237.9 hrs** | |

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

## Discussion Round 4 Status Changes

| Item | Previous | New | Reason |
|------|----------|-----|--------|
| C01 Ex-Dividend Calendar | ✅ Done | 📋 Todo | Status was false — never wired into business_card.py |
| C06 PPT Generation | Phase 1 | Phase 3 | Advances zero core values; pages must be excellent first |
| C19 Learning Path | P2 | Phase 2 (P1) | Best "Story first" alignment |
| C15 Paper Trading | Deferred | ❌ Canceled | Positioning violation |
| C18 Gamification | P2 | Deferred post-MVP | No core value alignment for D+ product |
| DR-03 Financial Health | P1 | **P0** | Highest-ROI fix; worst-graded core page |
| C21 LINE Bot | — | **P1 (new)** | Counters critical messaging-native threat |

---

## Recommended Execution Order (Updated)

### Phase 0 — Stabilize (Week 1): ~11-15 hours
**Goal: Main page grades B+**

1. **D-002-NEW**: Complete business_card.py (10 hrs) — 🔴 P0 CRITICAL
   - Restore revenue chart, pie chart, news, dividend, analogy sections
   - Fix missing `list_names` import (NEW-G08, 1 min)
   - Remove unused imports (NEW-G09, 5 min)
2. **DR-03**: Fix Financial Health page text-heavy sections (1.5 hrs) — 🔴 P0
3. **DI-01**: Fix color system violations (1 hr)
4. **DI-07**: Add text alternatives to severity badges (20 min)
5. **DI-03**: Fix Zone A violation in business_card.py (30 min)
6. Quick wins: TD-02, TD-03, NEW-G01, NEW-G04, NEW-G02, NEW-G06 (~1 hr combined)

### Phase 1 — Foundation (Week 2-3): ~18-22 hours
**Goal: M5 accuracy >80%**

7. **NF-D01**: M5 Event Detection Verification (4 hrs)
8. **C16**: "Did You Know?" Contextual Tips (5 hrs)
9. **C07**: Customizable Event Thresholds (12 hrs) — after D01 verification
10. **TD-08**: Optimize category browser N+1 queries (2 hrs)

### Phase 2 — Core Features (Weeks 4-6): ~44-54 hours
**Goal: business_card.py complete, all pages B+**

11. **C19**: Structured Learning Path (16 hrs)
12. **C14**: Company Health Score (17 hrs) — unblocked by D-002-NEW
13. **C02**: Notification/Push System Email (16 hrs) — after D02
14. **NF-D02**: Background Worker Architecture (6 hrs) — can start early as investigation

### Phase 3 — Share & Expand (Weeks 7-9): ~34-38 hours
**Goal: Viral distribution + advanced features**

15. **C06**: Auto-Generate Stock Analysis PPT (20 hrs)
16. **C04**: Market Thermometer (14 hrs)
17. **C25**: Social Sharing Buttons (8 hrs) — pairs well with C06

### Phase 4 — Round 4 Competitive Response (Weeks 10-12): ~38-42 hours
**Goal: Counter messaging-native threat**

18. **C21**: LINE Bot Interface Phase 1 (20 hrs) — 🔴 Highest priority new feature
19. **C22**: Bull Case / Bear Case (10 hrs)
20. **C23**: "Why Now" Narrative Card (8 hrs)

### Post-MVP — Scalability + Advanced (Weeks 13+): ~40-50 hours
21. **TD-12**: Abstract storage + SQLite (4 hrs)
22. **TD-13**: Fix rate limit global state (1 hr)
23. **TD-14**: Integration tests (3 hrs)
24. **TD-16**: "Last known good" fallback (2 hrs)
25. **C17**: AI Company Q&A (12 hrs)
26. **C13**: Investment Personality Quiz (8 hrs)
27. **C27**: Spaced Repetition (12 hrs)
28. **TD-11**: Type checking (2 hrs)
29. **TD-15**: Pagination (1 hr)

---

## Critical Path (Updated)

```
D-002-NEW (business_card.py fix, 10h) ──→ C14 (Health Score, 17h)
                                        ──→ C01 (Dividend, included)
                                        ──→ C16 (Tips, 5h)

NF-D01 (M5 Verification, 4h) ──→ C07 (Custom Thresholds, 12h)

NF-D02 (Worker Architecture, 6h) ──→ C02 (Notifications, 16h)

D-002-NEW (business_card.py) ──→ C21 (LINE Bot, 20h) [can start after card is complete]
                                ──→ C22 (Bull/Bear, 10h)
                                ──→ C23 (Why Now, 8h)

DI-04 (Card Standardization) ──→ DI-05 (Reduce Text) ──→ C06 (PPT, 20h)
```

**Longest path to MVP**: D-002-NEW (10h) → C14 (17h) = **27 hours** for core page functionality
**Full MVP with design compliance**: Phase 0 + Phase 1 = **29-37 hours**
**Competitive parity (with Round 4 features)**: Phases 0-4 = **131-167 hours**

---

## Risk Assessment

### High Risk Items
- **D-002-NEW (business_card.py truncation)**: P0 regression. Main page is broken. Every user sees a blank page. #1 cause of churn. Must be fixed before anything else.
- **NF-D02 (Background Worker Architecture)**: Streamlit is request-response only. True push notifications require external infrastructure. Risk of scope creep.
- **C21 (LINE Bot Interface)**: New technology stack (FastAPI + LINE Messaging API). Learning curve. LINE Bot account setup and approval process.
- **NF-D01 (M5 Verification)**: Event detection may have bugs that only show with real data. Could invalidate C07's foundation.
- **C17 (AI Company Q&A)**: Hallucination risk. Architecture decision (local vs API LLM) unresolved.

### Medium Risk Items
- **TD-08 (Category Browser)**: 200 sequential API calls. Caching helps but cold cache is still painful.
- **DI-06 (Responsive Layouts)**: Streamlit's `st.columns()` doesn't auto-wrap. CSS grid requires testing.
- **C06 (PPT Generation)**: python-pptx learning curve. Chart rendering (kaleido) can be finicky.
- **C14 (Health Score)**: Scoring algorithm design requires domain expertise. Must be explainable, not black-box.
- **C22 (Bull/Bear)**: Content generation for balanced framing. Risk of appearing to give investment advice.

### Low Risk Items
- All Immediate items (TD-01..05, NEW-G01, G04, G08, G09)
- All color fixes (DI-01, DI-08, DI-07)
- TD-07, TD-09, TD-10, TD-11
- C24, C25, C26 (small scoped features)

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

TD-05 (Test Fix) ──→ TD-06 (Event Tests) ──→ TD-14 (Integration Tests)

TD-10 (Data Consolidation) ──→ TD-12 (Storage Abstraction) ──→ TD-16 (Last Known Good)

DI-04 (Card Standardization) ──→ DI-05 (Reduce Text) ──→ C06 (PPT Generation)

DI-01 (Color Fixes) ──→ DI-08 (Chart Colors)

DR-03 (Financial Health P0) ──→ C06 (PPT captures page content)
```

---

## Notes on Estimation Approach

1. **Estimates include**: Coding time, basic unit/local testing, and documentation updates.
2. **Estimates exclude**: Extensive QA cycles, cross-browser testing, design review iterations, deployment.
3. **Buffer**: Add 15-20% buffer for unexpected issues, especially for High complexity items.
4. **Parallelization**: Items within the same sprint can often be parallelized if multiple developers are available.
5. **Confidence**: Immediate items ±10%, Short-term ±20%, Medium-term ±30%, New Features ±40%, LINE Bot ±50% (new tech stack).
6. **Round 4 additions**: C21-C27 are new from competitor research round 4 (2026-06-11). Estimates are preliminary.

---

## Cost Scenarios

| Scenario | Phases | Hours | Weeks (1 dev) | Description |
|----------|--------|-------|---------------|-------------|
| **MVP Core** | Phase 0 + 1 | 29-37 hrs | 1-1.5 weeks | Main pages functional, design compliance |
| **MVP + Competitive** | Phases 0-2 | 73-91 hrs | 2-3 weeks | + Notifications, Health Score, Learning Path |
| **Full Feature** | Phases 0-3 | 107-129 hrs | 3-4 weeks | + PPT, Market Thermometer, Social Sharing |
| **With Round 4** | Phases 0-4 | 145-171 hrs | 4-5 weeks | + LINE Bot, Bull/Bear, Why Now |
| **Complete** | All phases | 238-258 hrs | 6-7 weeks | Everything including post-MVP |

---

*Total estimated remaining effort: **237.9 hours** (approximately 6-7 developer weeks at 35 hrs/week)*
*With 20% buffer: **~285 hours** (~8 developer weeks)*
*Completed so far: **4.0 hours** (5 items)*
