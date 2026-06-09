# Stock Explorer Cost Estimation Report

> **Date**: 2026-06-10
> **Estimator**: Developer (Subagent)
> **Scope**: Technical debt fixes, design improvements, and new features
> **Basis**: tech_debt.md (13 remaining items), design_comparison_review.md (8 design items), issues.md (6 feature items)
> **Assumptions**: Single developer, familiar with the codebase; estimates include coding + basic testing; excludes extensive QA or design review cycles.

---

## A. Technical Debt Fixes

### A1. Immediate Items (This Week)

| ID | Item | Hours | Complexity | Risk | Dependencies | Notes |
|----|------|-------|------------|------|--------------|-------|
| TD-01 | Commit `uv.lock` | 0.1 (5 min) | Low | Low | None | Run `uv lock` and commit. Trivial but needed for reproducibility. |
| TD-02 | Extract shared timeline constants | 0.2 (10 min) | Low | Low | None | Create `src/services/timeline.py` with `_TIMELINE_DAYS` dict. Have `timeline_controls.py` and `_router_base.py` import from it. Eliminates the NEW-A01 DRY violation. |
| TD-03 | Add logging to `_fetch()` inner function | 0.2 (10 min) | Low | Low | None | Add `logging.warning(f"API fetch failed for {name}: {e}")` in the `except Exception` block in `_router_base.py` line 44. Improves debuggability. |
| TD-04 | Handle `FinMindRateLimitError` visibility | 0.25 (15 min) | Low | Low | None | Add specific handler before the generic `except Exception` in `_fetch()`. Either log a warning with `st.warning()` or set `st.session_state["rate_limited"] = True`. Addresses MEDIUM-B01. |
| TD-05 | Fix `st.session_state` in tests | 0.5 (30 min) | Low | Low | None | Refactor `filter_by_timeline()` to accept optional `timeline_value` parameter, or use `unittest.mock.patch.dict(st.session_state, {...})`. Fixes MEDIUM-E03. |

**Immediate Subtotal: ~1.3 hours**

---

### A2. Short-Term Items (Next 2 Weeks)

| ID | Item | Hours | Complexity | Risk | Dependencies | Notes |
|----|------|-------|------------|------|--------------|-------|
| TD-06 | Add tests for event detection & validation | 3.0 | Medium | Low | TD-05 (test infra fix) | Write pytest tests for: `validate_stock_id()` (10+ cases), `detect_revenue_event()` (YoY thresholds), `detect_price_abnormal()`, `detect_news_event()`, `check_data_freshness()`, `detect_company_type()`, `extract_dividend_summary()`. These are pure functions — easy to test. Addresses HIGH-E01. |
| TD-07 | Make `max_workers` configurable | 0.3 (20 min) | Low | Low | None | Add `max_workers` parameter to `get_stock_data()` with default=5. Consider reading from env var or config. Addresses MEDIUM-C02. |
| TD-08 | Optimize category browser N+1 queries | 2.0 | Medium | Medium | None | Three-pronged approach: (1) reduce to top 50 by default with "show more", (2) add `@st.cache_data(ttl=86400)` on individual stock price fetches, (3) batch via ThreadPoolExecutor. Addresses HIGH-C01 — currently 30-60s load time. |
| TD-09 | Cache ETF dividend data | 1.5 | Medium | Low | None | Add `@st.cache_data(ttl=604800)` (7-day TTL) on dividend fetch calls in `etf_browser.py`. Dividends don't change daily, so weekly cache is safe. Addresses MEDIUM-C03. |
| TD-10 | Consolidate static company data | 2.0 | Medium | Low | None | Create `src/data/company_registry.yaml` with all static data (one_liners, KNOWN_COMPANY_REVENUE, KNOWN_GROUP_STRUCTURES, INDUSTRY_BENCHMARKS). Load once at startup. Refactor 4 files to import from registry. Addresses MEDIUM-D03. |
| TD-11 | Add type checking configuration | 2.0 | Medium | Low | None | Add `mypy.ini` or `[tool.mypy]` to pyproject.toml. Run mypy, fix obvious type errors, set to ignore missing stubs for third-party libs. Start with `src/services/` and `src/data/` directories only (pages are Streamlit-heavy and harder to type). |

**Short-Term Subtotal: ~10.8 hours**

---

### A3. Medium-Term Items (Post-MVP)

| ID | Item | Hours | Complexity | Risk | Dependencies | Notes |
|----|------|-------|------------|------|--------------|-------|
| TD-12 | Abstract storage + SQLite backend | 4.0 | High | Medium | TD-10 (data consolidation) | Create `src/services/storage/` with ABC interface. Implement YAMLStorage (current) and SQLiteStorage backends. Add config toggle. Watchlist CRUD operations need migration. Addresses HIGH-D01. |
| TD-13 | Fix rate limit global state | 1.0 | Medium | Low | TD-04 (rate limit visibility) | Move `_consecutive_failures` and `_last_failure_time` from module globals in `finmind_client.py` to `st.session_state` or a shared cache. Addresses MEDIUM-D02. |
| TD-14 | Integration tests with saved API responses | 3.0 | Medium | Medium | TD-06 (test foundation) | Save real FinMind API responses as JSON fixtures. Write tests that load fixtures and verify parsing/transformation pipeline. Use `responses` or `requests_mock` for HTTP mocking. Tests COLUMN_ALIASES mapping in adaptive_engine.py. Addresses MEDIUM-E02. |
| TD-15 | Pagination for large lists | 1.0 | Low | Low | TD-08 (category browser optimization) | Add `st.session_state` page tracking to category_browser.py, etf_browser.py. Show 20 items per page with navigation buttons. |
| TD-16 | "Last known good" data fallback | 2.0 | Medium | Medium | TD-12 (storage abstraction) | When API fails, serve the most recent successful response from YAML/JSON cache. Need timestamp tracking. Display staleness warning: "Data from 2026-06-09". Addresses MEDIUM-F02. |

**Medium-Term Subtotal: ~11.0 hours**

---

## B. Design Improvements

| ID | Item | Hours | Complexity | Risk | Dependencies | Notes |
|----|------|-------|------------|------|--------------|-------|
| DI-01 | Fix color system violations (6 files) | 1.0 | Low | Low | None | Search-and-replace illegal colors across 6 files: `financial_health.py:180`, `etf_browser.py:67,68,447`, `watchlist_page.py:123,124`, `chart.py:150,204`, `operation_checkup.py:135`. Replace with design system palette. Straightforward find-and-replace + verify visually. |
| DI-02 | Remove `st.cache_data` from View layer | 0.5 | Low | Medium | None | Remove `@st.cache_data` from `peer_comparison.py:51` and `etf_browser.py:12,18`. Move caching logic to FinMindClient layer where it belongs. Risk: may need to prove performance is acceptable without View-layer caching. |
| DI-03 | Fix Zone A violation in business_card.py | 0.5 | Low | Low | None | Move watchlist add/remove buttons from navbar (col3) to content area. The navbar is Zone A (no interactive controls). Place buttons below the company name in the content area instead. |
| DI-04 | Standardize card components | 2.0 | Medium | Medium | DI-03 (business_card changes) | Replace inline HTML cards with `_白话_card()` / `_info_card()` from `_router_base.py` across: `business_card.py`, `financial_health.py`, `watchlist_page.py`. Extract custom cards (gradient card, health card) to shared components in `src/pages/_components.py`. |
| DI-05 | Reduce text on financial_health.py | 1.5 | Medium | Low | DI-04 (card standardization) | Condense 4 sections to 2-3. Make explanations collapsible with `st.expander()`. Target < 200 chars of body text. Move detailed explanations from inline text to tooltip/hover info cards. |
| DI-06 | Improve responsive column layouts | 1.5 | Medium | Medium | None | Replace fixed `st.columns(n)` with responsive patterns: use CSS grid for card layouts, reduce `st.columns([0.5, 0.8, 1.5, 1.2, 1.2, 0.8])` to 2-3 columns on narrow screens. Add CSS media queries. Affects `category_browser.py`, `etf_browser.py`, `peer_comparison.py`. |
| DI-07 | Add text alternatives to severity badges | 0.3 (20 min) | Low | Low | None | In `event_dashboard.py`, change severity badges from emoji-only (`🔴🟡🟢`) to include text labels (`🔴 重大 High`, `🟡 注意 Medium`, `🟢 正常 Low`). Accessibility improvement per WCAG 1.4.1. |
| DI-08 | Standardize chart colors | 1.0 | Low | Low | DI-01 (color violations) | Replace chart-specific colors in `chart.py`: `#4A90D9` → `#3498DB`, `#2ECC71` → `#27AE60`, `#F39C12` → `#3498DB` (neutral). Verify all charts look correct with new palette. |

**Design Improvements Subtotal: ~8.3 hours**

---

## C. New Features

| ID | Item | Hours | Complexity | Risk | Dependencies | Notes |
|----|------|-------|------------|------|--------------|-------|
| NF-C02 | Notification/Push System (Email phase) | 16.0 | High | High | NF-D02 (background worker) | Phase 1: Email notifications. Create `src/services/notifier.py` with SMTP support. Implement notification preferences in `config/notifications.yaml`. Add subscription UI on watchlist page. **Risk**: Background worker architecture is unresolved (see NF-D02). May need external cron job approach. |
| NF-C06 | Auto-Generate Stock Analysis PPT | 20.0 | High | Medium | DI-04 (card standardization) | Add "Download PPT" button to each page. Use `python-pptx` to generate slides from current page data. Include: Business Card, Operations summary, Financial Health summary, Peer Comparison radar chart. **Dependency on DI-04**: Standardized card components will simplify data extraction for PPT generation. |
| NF-C07 | Customizable Event Thresholds | 12.0 | Medium | Medium | NF-D01 (M5 verification) | Add settings page for event detection sensitivity. Allow users to adjust: revenue threshold (default ±30%), price threshold (default ±7%), new event types. Store preferences in `config/events.yaml`. **Prerequisite**: Must verify M5 detection actually works (NF-D01). |
| NF-C04 | Market Thermometer | 14.0 | Medium | Medium | None | New page or homepage widget. Aggregate: institutional buy/sell surplus (5-day avg), trading volume ratio, limit-up/limit-down ratio. Display as temperature gauge with plain-language explanation. Uses existing FinMind API (`TaiwanStockInstitutionalInvestorsBuySell`). |
| NF-D01 | M5 Event Detection Verification | 4.0 | Medium | High | None | Run M5 detection against real FinMind data for 10+ stocks. Verify: revenue events match actual YoY changes, price abnormal events match actual price moves, news keyword matching works. Document findings. **Blocker for NF-C07**. |
| NF-D02 | Background Worker Architecture Investigation | 6.0 | High | High | None | Research and prototype: (1) "pull on next visit" (simplest — check for pending notifications on page load), (2) APScheduler daemon thread (works in single-process Streamlit), (3) external cron job (most robust). Create proof-of-concept for chosen approach. **Blocker for NF-C02**. |

**New Features Subtotal: ~72.0 hours**

---

## Summary Table

| Priority Group | Items | Total Hours | Complexity | Key Risks |
|----------------|-------|-------------|------------|-----------|
| **A1. Immediate** (This Week) | TD-01 through TD-05 | **1.3 hrs** | All Low | None — quick wins |
| **A2. Short-Term** (Next 2 Weeks) | TD-06 through TD-11 | **10.8 hrs** | Low-Medium | Category browser optimization (TD-08) may need iteration |
| **A3. Medium-Term** (Post-MVP) | TD-12 through TD-16 | **11.0 hrs** | Medium-High | Storage abstraction (TD-12) requires careful migration |
| **B. Design Improvements** | DI-01 through DI-08 | **8.3 hrs** | Low-Medium | Responsive layouts (DI-06) need multi-device testing |
| **C. New Features** | NF-C02, C04, C06, C07, D01, D02 | **72.0 hrs** | Medium-High | Background worker arch (D02) is a hard blocker for C02 |
| **GRAND TOTAL** | **35 items** | **103.4 hrs** | | |

---

## Recommended Execution Order

### Sprint 1 — Foundation (Week 1): ~12 hours
1. TD-01: Commit `uv.lock` (5 min)
2. TD-02: Extract timeline constants (10 min)
3. TD-03: Add logging to `_fetch()` (10 min)
4. TD-04: Handle rate limit visibility (15 min)
5. TD-05: Fix `st.session_state` in tests (30 min)
6. DI-01: Fix color system violations (1 hr)
7. DI-07: Add text alternatives to severity badges (20 min)
8. DI-03: Fix Zone A violation in business_card.py (30 min)
9. DI-02: Remove `st.cache_data` from View layer (30 min)
10. NF-D01: M5 Event Detection Verification (4 hrs) — *starts in parallel with above*
11. NF-D02: Background Worker Architecture Investigation (6 hrs) — *starts in parallel*

### Sprint 2 — Quality + Performance (Week 2): ~11 hours
12. TD-06: Add tests for event detection & validation (3 hrs)
13. TD-07: Make `max_workers` configurable (20 min)
14. TD-09: Cache ETF dividend data (1.5 hrs)
15. TD-10: Consolidate static company data (2 hrs)
16. TD-11: Add type checking configuration (2 hrs)
17. DI-08: Standardize chart colors (1 hr)

### Sprint 3 — Design Polish (Week 3): ~5-6 hours
18. DI-04: Standardize card components (2 hrs)
19. DI-05: Reduce text on financial_health.py (1.5 hrs)
20. DI-06: Improve responsive column layouts (1.5 hrs)
21. TD-15: Pagination for large lists (1 hr)

### Sprint 4 — New Features Phase 1 (Weeks 4-5): ~32 hours
22. NF-C07: Customizable Event Thresholds (12 hrs) — *after D01 verification*
23. NF-C04: Market Thermometer (14 hrs)
24. DI-04 needed for C06, so verify completion

### Sprint 5 — New Features Phase 2 (Weeks 6-7): ~36 hours
25. NF-C06: Auto-Generate Stock Analysis PPT (20 hrs)
26. NF-C02: Notification/Push System Email phase (16 hrs) — *after D02 architecture decision*

### Sprint 6 — Scalability (Post-MVP): ~11 hours
27. TD-12: Abstract storage + SQLite backend (4 hrs)
28. TD-13: Fix rate limit global state (1 hr)
29. TD-14: Integration tests with saved API responses (3 hrs)
30. TD-16: "Last known good" data fallback (2 hrs)
31. TD-08: Optimize category browser N+1 queries (2 hrs) — *deferred as it may be less impactful after caching improvements*

---

## Risk Assessment

### High Risk Items
- **NF-D02 (Background Worker Architecture)**: Streamlit is request-response only. True push notifications require external infrastructure. Risk of scope creep. Mitigation: Start with "pull on next visit" model.
- **TD-12 (Storage Abstraction)**: Schema migration for watchlist data. Risk of data loss. Mitigation: Write migration script, backup existing YAML files.
- **NF-D01 (M5 Verification)**: Event detection may have bugs that only show with real data. Could invalidate NF-C07's foundation. Mitigation: Run verification early (Sprint 1).

### Medium Risk Items
- **TD-08 (Category Browser)**: 200 sequential API calls is inherently slow. Caching helps but cold cache is still painful. Mitigation: Reduce default scope + pagination.
- **DI-06 (Responsive Layouts)**: Streamlit's `st.columns()` doesn't auto-wrap. CSS grid is good but requires testing across breakpoints. Mitigation: Use CSS with `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))`.
- **NF-C06 (PPT Generation)**: python-pptx has a learning curve. Chart rendering to images (kaleido) can be finicky. Mitigation: Start with text-only PPT, add charts incrementally.

### Low Risk Items
- All Immediate items (TD-01 through TD-05)
- All color fixes (DI-01, DI-08, DI-07)
- TD-07 (max_workers config), TD-09 (ETF dividend cache)
- TD-06 (unit tests for pure functions)

---

## Dependency Graph

```
NF-D01 (M5 Verification) ──────┐
                               ├──→ NF-C07 (Custom Thresholds)
                               │
NF-D02 (Worker Architecture) ──┴──→ NF-C02 (Notifications)

TD-05 (Test Fix) ──→ TD-06 (Event Detection Tests) ──→ TD-14 (Integration Tests)

TD-10 (Data Consolidation) ──→ TD-12 (Storage Abstraction) ──→ TD-16 (Last Known Good)

DI-04 (Card Standardization) ──→ DI-05 (Reduce Text) ──→ NF-C06 (PPT Generation)

DI-01 (Color Fixes) ──→ DI-08 (Chart Colors)
```

---

## Notes on Estimation Approach

1. **Estimates include**: Coding time, basic unit/local testing, and documentation updates.
2. **Estimates exclude**: Extensive QA cycles, cross-browser testing, design review iterations, deployment.
3. **Buffer**: Add 15-20% buffer for unexpected issues, especially for High complexity items.
4. **Parallelization**: Items within the same sprint can often be parallelized if multiple developers are available.
5. **Confidence**: Immediate items are ±10% confidence, Short-term ±20%, Medium-term ±30%, New Features ±40%.

---

*Total estimated effort: **103.4 hours** (approximately 3 developer weeks at 35 hrs/week, or ~13 days)*
*With 20% buffer: **~124 hours** (~4 developer weeks)*
