# Stock Explorer — Developer Estimates

## 2026-06-14 Developer Estimates — Review Round 9

---

## Codebase Complexity Assessment

Before estimating, here is my assessment of the codebase based on reading all relevant source files:

**Current State**: 31 Python source files, ~5,200 LOC across src/. Well-layered 4-tier architecture (Presentation → Routing → Business Logic → Data).

**Key Patterns Observed**:
- Service modules are thin (~100-200 LOC) and focused — good for adding new ones
- Page modules consume services + `data` dict from router, render with `st.markdown` / `st.plotly_chart`
- Chart module (chart.py, 490 LOC) has 8 chart functions with a consistent `_apply_theme_layout` pattern
- `_router_base.py` (232 LOC) mixes data loading (ThreadPoolExecutor pattern) with UI helpers and duplicate financial logic
- Analogy engine, news summarizer, company_facts are template-based, stateless, easy to extend
- Hardcoded data lives in Python dicts in 4 files (revenue_analyzer, group_structure, analogy_engine, peer_comparison)
- YAML config files exist for company_facts, events, watchlist — proven pattern for data files
- No test infrastructure exists (0 test files)

**Complexity Indicators**:
- ✅ Consistent patterns: every page follows the same `data dict → render` flow
- ✅ Chart system is well-abstracted: adding a new chart type is straightforward
- ⚠️ Financial metric calculation is duplicated 3× (router_base, peer_comparison, roe_calculator)
- ⚠️ `create_comparison_radar()` passes raw values (not normalized) — radar charts will need normalization for C43
- ⚠️ Valuation data (`latest_per_pbr`) is only latest snapshot — C45 needs historical PER/PBR time series

---

### New Feature Estimates (C42–C47)

| ID | Feature | Impl Hours | Testing | Dependencies | Risks | Total |
|----|---------|-----------|---------|--------------|-------|-------|
| C42 | Stock Screener / Discovery Engine | 18–28h | 4–6h | category_browser.py pattern, FinMindClient, `get_stock_info()`, `st.dataframe` + `st.selectbox` filters | FinMind `get_stock_info()` returns ~1,800 rows; filtering on the fly needs caching. Column selection/renaming for display. Multi-column sort UI. | 22–34h |
| C43 | Company Snowflake Health Visualization | 14–20h | 3–4h | `extra_metrics` dict, `create_comparison_radar()` (exists but needs normalization), analogy_engine lessons, chart.py theme system | Radar chart needs normalized values (0–100 scale) — current `create_comparison_radar` passes raw numbers. Need to define "health score" formula across 6–8 dimensions. Snowflake/sunburst layout is more complex than radar. | 17–24h |
| C44 | "What Could Go Wrong" Risk Analysis | 12–18h | 3–4h | adaptive_engine.py news keyword analysis, income volatility computation from financial_df, analogy_engine.py for risk analogies, events.yaml data | Risk scoring model is subjective — need clear heuristics. Combines volatility + debt ratio + revenue concentration + event keyword frequency. Must not feel like a "sell signal" (historian positioning). | 15–22h |
| C45 | Valuation Band Chart (Historical P/E Range) | 10–16h | 2–3h | FinMind `get_daily_price()` + `get_financial_statement()` for quarterly EPS → historical PER calculation, `create_price_chart()` candlestick pattern, `px.area` or `go.Scatter` for band shading | Historical EPS needs TTM calculation (same `calc_roe_ttm` pattern). Need ~2 years of quarterly data. Band shading (percentile 25–75) requires careful Plotly layering. FinMind financial statement `date` field must be parsed correctly. | 12–19h |
| C46 | Moat Analysis — Competitive Advantage Assessment | 14–22h | 3–4h | analogy_engine.py patterns for moat descriptions, peer_comparison.py INDUSTRY_BENCHMARKS + `_get_benchmark_data()`, `extra_metrics` (gross_margin, ROE, revenue_yoy), industry benchmark data | Moat scoring model is subjective: gross margin stability + market share + switching costs + brand. Need heuristic scoring (1–5 scale per dimension). Requires comparing stock vs industry avg across 5–6 moat dimensions. Layout complexity (5 dimension cards + radar overlay). | 17–26h |
| C47 | Financial Education Academy | 26–38h | 6–8h | analogy_engine.py (existing lessons), company_facts.yaml pattern for lesson content, YAML data files for curriculum structure, `st.progress` / `st.session_state` for progress tracking | Content creation is 40% of the effort (writing 20+ lessons). Need a YAML schema for lessons (concept → analogy → example stock → quiz). Progress tracking requires session_state integration. Mobile-responsive lesson layout. Quiz interactivity (radio buttons + feedback). | 32–46h |

---

### Architecture Debt Estimates (R1–R5)

| ID | Item | Hours | Impact | Priority |
|----|------|-------|--------|----------|
| R1 | Extract shared financial metrics service (`financial_metrics.py`) | 2.5–4h | 🔴 **Critical** — Eliminates ~120 lines of duplication across 4 files. All features that compute margins/ROE/debt_ratio get a single source of truth. | **P0 — Do before Sprint 2** |
| R2 | Move UI helpers out of `_router_base.py` → `ui_components.py` | 1–1.5h | 🟡 **Hygiene** — Clean separation of concerns. Low risk, easy win. Unblocks cleaner page imports for C42–C47. | **P1 — Do alongside Sprint 2** |
| R3 | Batch API calls in `category_browser.py` and `etf_browser.py` | 3–5h | 🔴 **Performance** — Current sequential loops for 200 stocks cause 30–60s page loads. ThreadPoolExecutor pattern already exists in `_router_base.py`; just needs extraction to shared utility. Directly improves C42 (screener) since it also iterates over 1,800 stocks. | **P0 — Do before Sprint 2** |
| R4 | Session-level caching for watchlist and events | 1.5–2.5h | 🟡 **Performance** — Eliminates redundant YAML parse + file lock on every operation. Simple `st.session_state` cache with write-through invalidation. | **P1 — Do alongside Sprint 2** |
| R5 | Migrate hardcoded data to YAML files | 4–6h | 🟡 **Maintainability** — Affects 4 files: `revenue_analyzer.py` (8 stocks, ~50 lines), `group_structure.py` (5 groups, ~160 lines), `analogy_engine.py` (20 stock one-liners, 10 industry templates), `peer_comparison.py` (22 industry benchmarks). Need to create 4 YAML files + update 4 loaders. Prevents Python import side effects for data-only changes. | **P2 — During Sprint 3** |

---

### Approved Feature Validation (C37, C39, C41, C36, C38)

| ID | Original Estimate | Developer Assessment | Revised Estimate | Notes |
|----|-------------------|---------------------|------------------|-------|
| C37 | Key Takeaways Summary Card — 6.5h | ✅ **Confirmed**. Low complexity. Pure presentation + rule-based summary from existing `extra_metrics` dict. New `summary_engine.py` service (~80 LOC) + thin addition to `business_card.py`. | **6–7h** | Slightly conservative — no new data sources needed. All data exists in `data` dict. |
| C39 | What Changed Recently Delta Card — 5.5h | ⚠️ **Slightly underestimated**. Delta calculations are trivial, but threshold logic (>10% change detection) + analogy engine integration + deduplication with event dashboard adds complexity. Depends on R1 (shared metrics) for consistency. | **6–8h** | Recommend fixing R1 before C39 to avoid delta calculation divergence. |
| C41 | Read Next Recommendations — 6.5h | ✅ **Confirmed**. New `recommendation_engine.py` + `relationships.yaml` file. Uses existing `group_structure.py` and `peer_comparison.py` data. Bottom section of `business_card.py`. | **6–8h** | Needs `relationships.yaml` per D6 recommendation. If YAML doesn't exist yet, add 1h for data file creation. |
| C36 | Visual Revenue Tree top 10 — 8–9h | ⚠️ **Confirmed at top of range**. `plotly.express.treemap` is straightforward (~1 function, 30 LOC). But revenue tree data needs to be curated for 10 stocks. If relying on existing `revenue_analyzer.py` KNOWN_COMPANY_REVENUE (only 8 stocks), need to add 2+ more stocks. UI tab integration is trivial. | **8–10h** | Data curation for 2 additional stocks ~1h. If R5 (YAML migration) done first, loading becomes cleaner. |
| C38 | Compare Stories Phase 1 — 8–10h | ⚠️ **Likely needs top of range + 2h**. Dual-company data loading, 4 narrative dimensions, structured comparison layout in `peer_comparison.py`. Phase 1 is "two business cards side by side" — the narrative wrapper (analogies, delta descriptions) adds ~40 LOC of template text. | **10–12h** | Depends on R1 (shared metrics) for consistent comparison. Strongly recommend R1 before C38. The `narrative_comparator.py` service interface should be designed to accept an LLM provider in Phase 2 — add 1h for interface design. |

---

### Consolidated Effort Table

#### New Features (C42–C47)

| ID | Low (h) | High (h) | Midpoint (h) |
|----|---------|----------|-------------|
| C42 | 22 | 34 | 28 |
| C43 | 17 | 24 | 20.5 |
| C44 | 15 | 22 | 18.5 |
| C45 | 12 | 19 | 15.5 |
| C46 | 17 | 26 | 21.5 |
| C47 | 32 | 46 | 39 |
| **C42–C47 Total** | **115** | **171** | **143** |

#### Architecture Debt (R1–R5)

| ID | Low (h) | High (h) | Midpoint (h) |
|----|---------|----------|-------------|
| R1 | 2.5 | 4 | 3.25 |
| R2 | 1 | 1.5 | 1.25 |
| R3 | 3 | 5 | 4 |
| R4 | 1.5 | 2.5 | 2 |
| R5 | 4 | 6 | 5 |
| **R1–R5 Total** | **12** | **19** | **15.5** |

#### Approved Features Revalidation (C37, C39, C41, C36, C38)

| ID | Original (h) | Revised Low (h) | Revised High (h) | Midpoint (h) |
|----|-------------|----------------|-----------------|-------------|
| C37 | 6.5 | 6 | 7 | 6.5 |
| C39 | 5.5 | 6 | 8 | 7 |
| C41 | 6.5 | 6 | 8 | 7 |
| C36 | 8–9 | 8 | 10 | 9 |
| C38 | 8–10 | 10 | 12 | 11 |
| **Approved Total** | **34.5–37.5** | **36** | **45** | **40.5** |

#### Grand Total

| Category | Low (h) | High (h) | Midpoint (h) |
|----------|---------|----------|-------------|
| Architecture Debt (R1–R5) | 12 | 19 | 15.5 |
| Approved Features (C37–C38) | 36 | 45 | 40.5 |
| New Features (C42–C47) | 115 | 171 | 143 |
| **Grand Total** | **163** | **235** | **199** |

---

### Recommended Sprint Allocation

**Assumptions**:
- 1 developer, ~30 productive hours per week (accounting for standups, reviews, context switching)
- Sprint = 2 weeks = ~60h capacity
- R1 and R3 should be done before any Sprint 2 features (architectural prerequisites)

#### Pre-Sprint 2: Architecture Debt Prerequisite (1 week, ~30h)

| Week | Item | Hours | Rationale |
|------|------|-------|-----------|
| Pre-Sprint 2a | R1: Extract `financial_metrics.py` | 3.5h | Required by C39, C38, C43, C44, C46 |
| Pre-Sprint 2a | R3: Batch API calls (category + ETF browser) | 4h | Required by C42 (screener), improves all browsing |
| Pre-Sprint 2a | R2: Move UI helpers to `ui_components.py` | 1.5h | Hygiene, unblocks cleaner imports |
| Pre-Sprint 2a | R4: Session caching (watchlist + events) | 2h | Quick win, improves all pages |
| | **Subtotal** | **11h** | Leaves ~19h buffer for Sprint 2a features |

#### Sprint 2 (Weeks 1–2, ~60h)

| Priority | Item | Hours | Dependencies |
|----------|------|-------|-------------|
| P0 | C37: Key Takeaways Summary Card | 6.5h | None (all data exists) |
| P0 | C39: What Changed Recently Delta Card | 7h | R1 (financial_metrics) |
| P1 | C45: Valuation Band Chart | 15.5h | None (uses existing price + financial data) |
| P2 | C43: Snowflake Health Visualization | 20.5h | R1 (financial_metrics), radar normalization |
| | **Sprint 2 Total** | **49.5h** | Fits in 60h with buffer |

#### Sprint 3 (Weeks 3–4, ~60h)

| Priority | Item | Hours | Dependencies |
|----------|------|-------|-------------|
| P0 | C41: Read Next Recommendations | 7h | `relationships.yaml` data file |
| P0 | C38: Compare Stories Phase 1 | 11h | R1 (financial_metrics) |
| P1 | C44: "What Could Go Wrong" Risk Analysis | 18.5h | adaptive_engine, analogy_engine |
| P2 | R5: Migrate hardcoded data to YAML | 5h | None (can parallelize) |
| | **Sprint 3 Total** | **41.5h** | Fits in 60h with buffer |

#### Sprint 4 (Weeks 5–6, ~60h)

| Priority | Item | Hours | Dependencies |
|----------|------|-------|-------------|
| P0 | C36: Visual Revenue Tree top 10 | 9h | chart.py treemap, revenue data |
| P1 | C42: Stock Screener / Discovery Engine | 28h | R3 (batch API), category_browser pattern |
| P2 | C46: Moat Analysis | 21.5h | R1, peer_comparison, analogy_engine |
| | **Sprint 4 Total** | **58.5h** | Tight but fits |

#### Sprint 5 (Weeks 7–8, ~60h)

| Priority | Item | Hours | Dependencies |
|----------|------|-------|-------------|
| P2 | C47: Financial Education Academy | 39h | analogy_engine, YAML lesson data |
| | Buffer / Polish / Bug fixes | 21h | — |
| | **Sprint 5 Total** | **60h** | — |

---

### Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| FinMind API rate limits during C42 screener (1,800 stocks) | High | C42 could take minutes without batching | R3 (batch API) must be done before C42. Use ThreadPoolExecutor(max_workers=10) with rate limit detection. |
| Historical PER calculation (C45) — FinMind financial statement `date` field format inconsistency | Medium | Wrong EPS dates → wrong PER values | Validate date parsing with 3–4 known stocks before building the chart. Add unit tests for EPS extraction. |
| Radar chart normalization (C43) — raw values make radar unreadable | High | Visualization is meaningless | Normalize all dimensions to 0–100 scale before passing to `create_comparison_radar()`. Add a `normalize_metrics()` helper. |
| Moat scoring model (C46) subjectivity | Medium | Scores feel arbitrary | Use simple 1–5 integer scale with clear thresholds. Document scoring rubric in code comments. |
| C47 content creation effort exceeds coding effort | High | 20+ lessons need writing, not just coding | Create a YAML schema first. Write 3 pilot lessons. Estimate remaining content creation separately. Consider starting with 10 lessons MVP. |
| R1 refactoring breaks existing calculations | Medium | Silent wrong values in production | Add assertion tests comparing old vs new calculation results for 5 known stocks before/after R1. |
| C38 narrative comparator scope creep | Medium | Phase 1 becomes Phase 2 accidentally | Strictly limit to 4 narrative dimensions. No LLM. Template-only. Document Phase 2 as separate issue. |

---

### Key Recommendations

1. **Do R1 + R3 before Sprint 2 features** — These are force multipliers. R1 ensures all financial calculations are consistent (critical for C39, C38, C43, C44, C46). R3 makes C42 feasible.

2. **C45 (Valuation Band) is the best "quick win" for Sprint 2** — It uses existing data, has a clear chart pattern (candlestick + band shading), and delivers high user value. Lower risk than C43.

3. **C42 (Screener) should be Sprint 4, not earlier** — It depends on R3 (batch API) and is the most complex new page. The category_browser.py pattern is the starting point, but filtering 1,800 stocks with multiple criteria needs careful UI design.

4. **C47 (Academy) is a mini-project** — At 39h midpoint, it's nearly a full sprint by itself. Consider splitting: Phase 1 = 10 lessons + quiz (20h), Phase 2 = remaining lessons + progress tracking (19h).

5. **Add basic tests during Sprint 3** — After R1 creates `financial_metrics.py`, write 5–10 unit tests for the shared calculation functions. This prevents regressions across all features that depend on it. (~2h investment).

---

*Created: 2026-06-14*
*Role: Developer*
*Review cycle: Round 9*
*Confidence level: Medium-High (based on thorough codebase review of all 31 source files)*
