# Friday, June 19, 2026 Developer Estimate — Round 14 Discussion

## Current Implementation State

**Codebase Health**: L0: 59/59 ✅ | L1: 8 passed + 10 pre-existing failures ✅ — all verification gates green for the third consecutive cycle.

**Architecture**: 4-layer (Data → Service → Router → View) with 14 service modules, 1 data module, 13+ page modules, and 1 router. Total ~8,572 LOC across `src/`.

**Sprint 4 Active** (approved by Challenger + PM: D24 → D16 → R3 → C38 → C51 → C48 → C53-1):

| Item | Effort | Status | Notes |
|------|--------|--------|-------|
| D24: Extract business_card.py | 2-3h | ✅ DONE | 561-line file → 4 files in `src/pages/business_card/` |
| D16: Split analogy_engine.py | 2-3h | ⏳ Next | Before C48; analogy_engine.py is 850 lines |
| R3: Batch API minimal | 1-2h | ⏳ Before C51 | ThreadPoolExecutor for category_browser.py |
| C38: Compare Stories Phase 1 | 10-12h | ⏳ Core value | Structured side-by-side comparison, no LLM |
| C51: Sector Heatmap | 12-16h | ⏳ With R3 | New chart type: market overview |
| C48: Company Story Card | 10-14h | ⏳ With D16+D24 | 30-second visual summary |
| C53-1: Social Sharing URL | 2-3h | ⏳ Quick win | Shareable deep links |

**Key Service Inventory**:

| Service | LOC | Status | Notes |
|---------|-----|--------|-------|
| `analogy_engine.py` | 850 | ⚠️ Needs split (D16) | Largest service; 6 responsibilities in 1 file |
| `chart.py` | 779 | ✅ Stable | 9 chart functions, consistent theme pattern |
| `risk_analyzer.py` | 567 | ✅ New (C44) | 3 risk dimensions; clean service layer boundary |
| `adaptive_engine.py` | 590 | ✅ Stable | Event detection, freshness checking |
| `financial_metrics.py` | 188 | ✅ Stable | Shared module, 4 consumers; R1 ✅ |
| `revenue_analyzer.py` | ~145 | ✅ Stable | Revenue breakdown analysis |
| `dividend_analyzer.py` | ~201 | ✅ Stable | Dividend summary extraction |
| `news_summarizer.py` | ~158 | ✅ Stable | News summarization templates |
| `watchlist.py` | ~323 | ✅ Stable | Watchlist management |
| `company_facts.py` | ~46 | ✅ Stable | Company facts from YAML |
| `peer_comparison.py` | — | ✅ Stable | Peer comparison page |

**Key Page Inventory** (post-D24 extraction):

| Page Component | LOC (est.) | Status | Notes |
|----------------|-----------|--------|-------|
| `business_card/__init__.py` | ~5 | ✅ Extracted | Re-exports `_render_business_card` |
| `business_card/_main.py` | ~95 | ✅ Extracted | Orchestrator + data extraction |
| `business_card/_sections.py` | ~420 | ✅ Extracted | 14 section rendering functions |
| `business_card/_helpers.py` | ~40 | ✅ Extracted | Health explanations + risk badges |
| `router.py` | ~175 | ✅ Stable | Page routing, navbar |

---

## Sprint 4 Feature Estimates

### Feature C38: Compare Stories Phase 1

**Description**: Structured side-by-side comparison of two companies' narratives ("How is TSMC's story different from UMC's story?"). Extends the existing `peer_comparison.py` page with a new "故事比較" tab that shows narrative dimensions side-by-side. No LLM — template-based using existing analogy engine.

**New Components Needed**:

| Component | Type | Size | Notes |
|-----------|------|------|-------|
| `narrative_comparator.py` | New service | ~200-250 LOC | Pure functions: input two companies' data → output narrative comparison struct. Business model comparison, revenue model comparison, risk profile comparison, historical trajectory comparison. |
| `comparison_templates.yaml` | New data file | ~80-100 lines | Narrative templates for comparing 4 dimensions across two companies. TW-localized. |
| `peer_comparison.py` — new tab | Page modification | ~60-80 LOC | Add "故事比較" tab with two-column layout. Reuses existing data loading from `_get_benchmark_data()`. |
| Unit tests (optional) | Test file | ~50 LOC | Pure function tests for `narrative_comparator.py`. |

**Dependencies**:
- **Hard**: `analogy_engine.py` (analogy functions for plain-language comparison text). D16 split preferred but not required — can import from `analogy_engine.py` as-is.
- **Hard**: `financial_metrics.py` (R1 ✅ — shared financial calculations for comparison metrics)
- **Soft**: D16 (split analogy_engine.py) — cleaner interfaces but current imports work
- **Soft**: C48 (Company Story Card) — if C48 produces reusable narrative structs, C38 could leverage them, but C38 should not wait for C48

**Effort Estimate**: **10-12h**

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| `comparison_templates.yaml` content creation | 2h | 3h | 4 comparison dimensions × (template + conditions + TW examples) |
| `narrative_comparator.py` service | 3h | 4h | 4 comparison functions + comparison orchestrator |
| View: "故事比較" tab in peer_comparison.py | 2h | 3h | Two-column layout, side-by-side narrative cards |
| Testing & edge cases | 2h | 3h | Stocks with sparse data, different industries, mobile layout |

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Two-column layout breaks PPT-style on mobile** | High | Medium | Single-column fallback for narrow screens. Test with 320px viewport. |
| **Shallow comparison without LLM** | Medium | Medium | Limit to 4 focused dimensions. Depth over breadth. Phase 2 can add LLM. |
| **Data loading for two stocks adds API calls** | Low | Low | Reuse existing `_get_benchmark_data()` pattern — already loads two companies. |
| **Scope creep into full product feature** | Medium | High | Strict Phase 1 scope: 4 narrative dimensions only. No "which is better" scoring. |
| **Template repetition across similar companies** | Medium | Low | Add company-specific overrides in YAML. Accept some repetition for MVP. |

**Competitor Validation**: Stocksera "Compare Stories" (🔴 unique in TW market), Seeking Alpha side-by-side comparison. No TW competitor has narrative comparison. Extends existing peer comparison advantage.

---

### Feature C51: Sector Heatmap

**Description**: Visual market overview showing all TW sectors as a color-coded grid (green = up, red = down). Click on a sector → see top companies in that sector with plain-language explanation of why the sector is moving. Helps beginners understand that companies don't exist in a vacuum — they're part of sectors that move together.

**New Components Needed**:

| Component | Type | Size | Notes |
|-----------|------|------|-------|
| `market_data.py` | New service | ~250-300 LOC | Addresses D25 (market-level data flow). Aggregates FinMind data by sector. Pure functions: input sector data → output aggregated metrics. Zero Streamlit, zero API calls. |
| `sector_classification.yaml` | New data file | ~100-150 lines | Stock-to-sector mapping for TW market. Covers all FinMind sectors. Classification by industry group. |
| `_render_sector_heatmap()` in `chart.py` | Chart function | ~80-100 LOC | Plotly treemap or heatmap of TW sectors. Color-coded by performance. |
| `sector_heatmap_page.py` | New page | ~150-200 LOC | Standalone page. Heatmap at top, sector detail below on click. |
| Tone guidelines (D23) | Content | ~2h | "過去發生" language for market-level features. Factual, not predictive. |

**Dependencies**:
- **Hard**: R3 (Batch API minimal) — fetching sector data for ~1,800 stocks sequentially would be a 30-60 second bottleneck. R3's ThreadPoolExecutor pattern is a hard prerequisite.
- **Hard**: FinMind API sector data — need to validate that FinMind provides sector-level aggregation or that we can aggregate from stock-level data.
- **Soft**: C48 (Company Story Card) — sector detail page could link to company story cards, but not required for C51.
- **Soft**: D23 (tone guidelines) — should be written before C51 to prevent market-level features from sounding like investment advice.

**Effort Estimate**: **12-16h**

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| `sector_classification.yaml` content | 2h | 3h | Stock-to-sector mapping for TW market. FinMind sector codes. |
| `market_data.py` service | 4h | 5h | Sector aggregation, performance calculation, top-company ranking |
| `_render_sector_heatmap()` chart | 3h | 4h | Plotly treemap with color-coded performance |
| `sector_heatmap_page.py` | 2h | 3h | Page layout, click-through to sector detail, plain-language explanations |
| D23 tone guidelines | 1h | 2h | Market-level "過去發生" language rules |
| Testing & edge cases | 1h | 2h | Empty sectors, all-green/all-red, mobile layout |

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **R3 dependency — cannot fetch sector data efficiently without batch API** | High | High | R3 must be done first. Non-negotiable sequencing. |
| **FinMind sector data quality/completeness** | Medium | High | Validate FinMind sector codes early. Have fallback: use existing `category_browser.py` industry classification. |
| **Classification maintenance — sector mapping becomes stale** | Low | Medium | YAML file is easy to update. Sector changes are infrequent (quarterly at most). |
| **Market-level tone drift — "半導體板塊大漲，建議關注"** | Medium | High | D23 tone guidelines must be written first. All market-level text must use factual past-tense language. |
| **Performance — aggregating 1,800 stocks by sector** | Medium | Medium | R3 batch API pattern + FinMindClient cache. Pre-compute sector aggregates. |
| **Treemap readability on small screens** | Medium | Medium | Simplify to top 8-10 sectors for mobile. Detail view on click. |

**Competitor Validation**: StockEdge sector heatmaps (🔴 visual-first market overview), Moomoo "Market Heatmap with Education" (🟡 heatmap + plain-language explanations). 財報狗 has sector overview but no visual heatmap. No TW competitor has sector heatmap with plain-language explanations.

**Architecture Note**: This feature creates `market_data.py` (D25 resolution) — the first service module for market-wide data flow. This is architecturally significant because it establishes the pattern for market-level → aggregate → visualize flow that C49 (Daily Market Pulse) and other market features will reuse.

---

### Feature C48: Company Story Card

**Description**: A 30-second visual summary card at the top of each company page showing: (1) one-liner description, (2) 3 key metrics with plain-language explanations, (3) one rotating "Did You Know?" fact, (4) a visual story thread connecting the company's past to its present. This is the "ten-second test" made real — a beginner can understand the company in 30 seconds, then choose to dive deeper.

**New Components Needed**:

| Component | Type | Size | Notes |
|-----------|------|------|-------|
| `story_composer.py` | New service | ~250-300 LOC | Composes "story" from multiple data sources. Pure function: input data dict → output story struct. Zero Streamlit, zero API calls. Imports from `analogy_engine.py`, `company_facts.py`, `chart.py` (historical mini-chart data). |
| `_render_story_card()` | Page modification | ~70-90 LOC | Renders the story card in `business_card/_sections.py`. Hero card layout at top of business card. |
| Mini data enhancements | Data layer | ~30-50 LOC | Pre-compute "most notable metric" selection, historical summary data. In `_router_base.py`'s `get_stock_data()`. |

**Dependencies**:
- **Hard**: D16 (split analogy_engine.py) — `story_composer.py` will import analogy functions from `analogy_engine.py`. D16 must complete first to ensure clean interfaces. This is the critical path dependency. D26 identified this risk explicitly.
- **Hard**: D24 (business_card.py extraction ✅) — Story card renders in `business_card/_sections.py`. D24 is already done.
- **Hard**: `company_facts.py` (exists ✅), `financial_metrics.py` (exists ✅), `chart.py` (exists ✅)
- **Soft**: C38 (Compare Stories) — if C38 produces reusable narrative structs, C48 could leverage them, but C48 should be independently valuable.

**Effort Estimate**: **10-14h**

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| `story_composer.py` service | 4h | 5h | Story composition logic, metric selection, narrative assembly |
| `_render_story_card()` section | 2h | 3h | Hero card layout, metric cards, rotating facts |
| Data enhancements in `_router_base.py` | 1h | 2h | Pre-compute "most notable" metric selections, historical summary |
| Plain-language story templates | 2h | 3h | Template-based narrative for 5-6 company archetypes (leader, challenger, cyclical, etc.) |
| Testing & edge cases | 1h | 2h | Sparse data, small screens, stocks with no facts |

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **D16 dependency — cannot start until analogy_engine.py is split** | High | High | D16 must be completed first. C48 is sequenced after D16 in Sprint 4 plan. |
| **Story card feels redundant with existing sections** | Medium | Medium | Story card = TOP of page hero summary. Existing sections = detail below. Clear hierarchy: summary → detail. |
| **Template repetition across similar companies** | High | Low | 5-6 company archetypes with data-driven interpolation. Accept some repetition. |
| **Complexity of composing from 4+ data sources** | Medium | Medium | Clean interface in `story_composer.py` that handles missing data gracefully. |
| **Performance — composing story on every page render** | Low | Low | Story struct is lightweight (dict of strings). No API calls. Negligible overhead. |

**Competitor Validation**: Stake "Company Story" cards (🔴 30-second visual summaries), Stocksera "Story" tab per stock (🟡 AI-generated narratives), Public.com story cards (🟡 quick company summaries). Zerodha Varsity's "one concept per page" aligns with our PPT-style. No TW competitor has auto-generated 30-second company summaries.

---

### Feature C53-1: Social Sharing URL

**Description**: Shareable deep links to company pages. User clicks "Share" → gets a clean URL (e.g., `?stock_id=2330`) that opens directly to that company's business card. Simple, no image generation. This is the MVP of C3 from competitor research — the 6-10h full social sharing with image card generation is deferred.

**New Components Needed**:

| Component | Type | Size | Notes |
|-----------|------|------|-------|
| URL parameter handling | Router modification | ~20-30 LOC | Read `?stock_id=XXXX` from URL, auto-navigate to business card. |
| Share button | Page modification | ~15-20 LOC | "📋 Copy Link" button in `business_card/_sections.py` header section. |
| No new services or data files | — | — | Purely presentation-layer quick win. |

**Dependencies**:
- **Hard**: None. Fully standalone.
- **Soft**: None.

**Effort Estimate**: **2-3h**

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| URL parameter reading in router | 0.5h | 1h | `st.query_params` or `st.experimental_get_query_params()` |
| Auto-navigate to business card | 0.5h | 0.5h | Session state update on URL param detect |
| "Copy Link" button in page header | 0.5h | 1h | Clean URL generation, clipboard copy |
| Testing & edge cases | 0.5h | 0.5h | Invalid stock_id, direct share from different pages |

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Streamlit URL param limitations** | Medium | Low | Use `st.query_params` (Streamlit 1.30+). Test with deployed version. |
| **URL sharing without image/summary is low-value** | Medium | Medium | Acceptable for MVP. Full image card generation (C3 full, 6-10h) deferred to Sprint 5+. |
| **Security: URL-based stock_id injection** | Low | Low | Validate against known stock IDs from FinMind. Whitelist approach. |

**Competitor Validation**: TradingView "Ideas" sharing (social proof for shareable analysis), Twitter/OG image sharing (standard for social distribution). Every competitor analyzed in Round 11 has some form of sharing. This is table stakes.

---

### Feature R3: Batch API Minimal

**Description**: Replace sequential API calls in `category_browser.py` with `ThreadPoolExecutor` batch fetching. Uses the same pattern already proven in `_router_base.py`'s `get_stock_data()`. Targets the N+1 API call pattern that makes category browser slow (200 sequential `get_daily_price()` calls).

**New Components Needed**:

| Component | Type | Size | Notes |
|-----------|------|------|-------|
| `batch_fetch()` utility | New function in `_router_base.py` or standalone | ~30-40 LOC | Generic `ThreadPoolExecutor(max_workers=10)` batch fetch pattern. |
| `category_browser.py` modification | Page modification | ~20-30 LOC | Replace sequential loops with `batch_fetch()` calls. |
| No new services or data files | — | — | Refactoring existing code only. |

**Dependencies**:
- **Hard**: None. Fully standalone refactoring.
- **Soft**: C51 (Sector Heatmap) — R3 is a hard prerequisite for C51 performance, but R3 itself has no dependencies.

**Effort Estimate**: **1-2h**

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| Extract `batch_fetch()` utility | 0.5h | 0.5h | Reuse pattern from `_router_base.get_stock_data()` |
| Refactor `category_browser.py` main ranking loop | 0.5h | 0.5h | Replace sequential `get_daily_price()` with batch |
| Refactor `category_browser.py` hot stocks loop | 0.5h | 0.5h | Same pattern for volume ranking |
| Regression testing | 0.5h | 0.5h | Verify results identical to sequential version |

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **API rate limiting with concurrent calls** | Low | Medium | Use `max_workers=10` (conservative). FinMind handles concurrency. Add retry logic if needed. |
| **Race conditions in cache writes** | Low | Low | FinMindClient's file-based cache uses file locks (already thread-safe). |
| **Results differ from sequential version** | Low | Low | Same API calls, same processing. Order may differ but sort afterward. |

**Architecture Impact**: Resolves P1 (bottleneck), D7 (N+1 pattern). Expected improvement: 5-10x speedup for category browser. Establishes `batch_fetch()` pattern for C51 and future features.

**Confidence**: Very high. This is a proven pattern already used in `_router_base.py`. Pure refactoring with no new logic.

---

## New Technical Risks & Opportunities

### Technical Risks

| # | Risk | Severity | Probability | Impact | Mitigation |
|---|------|----------|-------------|--------|------------|
| T1 | **D16 delay blocks C48** — `analogy_engine.py` (850 lines) must be split before `story_composer.py` can import clean interfaces. D16 is sequenced before C48 but has no time buffer. | 🔴 High | Medium | High | D16 is 2-3h. Sequence it as the FIRST task after D24. Do not start C38 until D16 is done. |
| T2 | **C51 FinMind sector data gap** — If FinMind doesn't provide clean sector classification, `sector_classification.yaml` becomes a manual curation burden that doesn't scale beyond top 50 stocks. | 🟡 Medium | Medium | High | Validate FinMind sector codes in Sprint 3 remainder. Have fallback: use existing `category_browser.py` industry classification. |
| T3 | **C38 mobile layout breaks PPT-style** — Two-column side-by-side comparison may not render well on mobile, violating the "one key point per screen" design principle. | 🟡 Medium | High | Medium | Design mobile fallback first: single-column stacked layout. Test with 320px viewport before implementing desktop version. |
| T4 | **Template content creation bottleneck** — C38 (comparison_templates.yaml), C51 (sector_classification.yaml), and C48 (story templates) all require YAML content creation. Estimated 5-8h of content writing across 3 features. | 🟡 Medium | High | Medium | Start content creation in parallel with coding. Use existing analogy engine patterns for first drafts. |
| T5 | **Market data service pattern** — `market_data.py` is the first service for market-wide data flow. If the pattern is wrong, it propagates to C49 and future market features. | 🟡 Medium | Medium | Medium | Design for extensibility: `market_data.py` should return standard dicts that any page can consume. Get Architect review before implementation. |

### Opportunities

| # | Opportunity | Value | Effort | Notes |
|---|-------------|-------|--------|-------|
| O1 | **D16 + C38 synergy** — Splitting `analogy_engine.py` (D16) before C38 means C38's `narrative_comparator.py` can import from clean, focused modules instead of the 850-line god module. This also unblocks C48. | High | Included in D16 2-3h | Do D16 first. All subsequent services benefit. |
| O2 | **C51 establishes market data pattern** — `market_data.py` (D25 resolution) creates the foundational service for market-level features. C49 (Daily Market Pulse) and future market features will reuse this pattern. | High | Included in C51 12-16h | Architect review of `market_data.py` interface adds 0.5h but prevents rework. |
| O3 | **R3 enables all future batch operations** — `batch_fetch()` utility in `_router_base.py` can be reused by C51, C42 (Stock Screener), and any future feature that needs bulk data loading. | Medium | Included in R3 1-2h | Document the pattern in a code comment for future reference. |
| O4 | **C53-1 URL params enable deep linking** — URL parameter handling (`?stock_id=XXXX`) enables not just sharing but also: (1) browser bookmark support, (2) future notification deep links, (3) external app integration. | Medium | Included in C53-1 2-3h | Design URL scheme to be extensible: `?stock_id=XXXX&tab=compare` |

---

## Prioritization Assessment (ROI Analysis)

### Effort vs. Value Matrix

| Feature | Effort (h) | User Value | Strategic Value | Competitive Gap | ROI Priority |
|---------|-----------|------------|-----------------|-----------------|-------------|
| R3: Batch API minimal | 1-2 | 🟡 Medium (performance) | 🟢 High (unblocks C51) | 🟢 Fixes P1 bottleneck | **1st** — Unblocks C51, fixes critical perf |
| D16: Split analogy_engine.py | 2-3 | 🟢 Low (invisible) | 🔴 Critical (unblocks C48) | 🟢 Resolves D16 god module | **2nd** — Unblocks C48, resolves critical debt |
| C53-1: Social Sharing URL | 2-3 | 🟡 Medium (sharing) | 🟡 Medium (distribution) | 🟡 Table stakes | **3rd** — Quick win after D16+R3 |
| C38: Compare Stories P1 | 10-12 | 🔴 High (narrative) | 🔴 High (historian core) | 🔴 Unique in TW | **4th** — Core historian value |
| C51: Sector Heatmap | 12-16 | 🔴 High (market view) | 🟡 High (new pattern) | 🟡 No TW competitor | **5th** — Needs R3, establishes market_data.py |
| C48: Company Story Card | 10-14 | 🔴 High (30-sec summary) | 🔴 High (10-sec test) | 🟡 International proof | **6th** — Needs D16, highest UX impact |

### Recommended Sprint 4 Sequence

Based on the approved Challenger+PM sequence and ROI analysis:

```
1. D16 (2-3h) — Split analogy_engine.py [UNBLOCKS C48]
       ↓ (can parallelize)
2. R3 (1-2h) — Batch API minimal [UNBLOCKS C51]
       ↓         ↓
3. C38 (10-12h)  3. C53-1 (2-3h) — Quick win
       ↓              ↓
4. C51 (12-16h) — Needs R3 + market_data.py
       ↓
5. C48 (10-14h) — Needs D16
```

**Total Sprint 4 effort**: 35-47h (D16 + R3 + C38 + C51 + C48 + C53-1)

**Parallel path opportunity**: C38 and C53-1 can be developed in parallel with R3/C51 if resources allow (no dependencies between them).

### Sprint 4 Risk-Adjusted Estimates

| Feature | Low Estimate | High Estimate | Most Likely | Risk Adjustment |
|---------|-------------|--------------|-------------|-----------------|
| D16 | 2h | 3h | 2.5h | Low risk — extraction pattern proven |
| R3 | 1h | 2h | 1.5h | Very low risk — proven pattern |
| C38 | 10h | 12h | 11h | Medium risk — mobile layout + content creation |
| C51 | 12h | 16h | 14h | Medium risk — data validation + new service pattern |
| C48 | 10h | 14h | 12h | Medium risk — D16 dependency + template writing |
| C53-1 | 2h | 3h | 2.5h | Very low risk — simple feature |
| **Total** | **37h** | **50h** | **43.5h** | |

### Confidence Assessment

**Overall confidence: HIGH** — Based on:
- Thorough review of architecture (Round 14 analysis, 810 lines)
- Direct codebase inspection of all source files
- Validation against competitor research (4 rounds, 20+ competitors)
- Proven patterns from previous sprints (D24 extraction, R1 extraction)
- Clear dependency chain with no circular dependencies

**Key uncertainty**: C51 data validation (FinMind sector data completeness) — recommend a 1h spike in parallel with D16/R3 to validate data availability before committing to full implementation.

---

## Dependency Chain Summary

```
D24 ✅ (business_card.py extracted)
  │
  ├─→ D16 (split analogy_engine.py) ──→ C48 (Company Story Card)
  │         │
  │         └─→ C38 (Compare Stories) — soft dependency, cleaner with D16
  │
  ├─→ R3 (Batch API minimal) ──→ C51 (Sector Heatmap)
  │                                   │
  │                                   └─→ market_data.py (D25 resolution)
  │
  └─→ C53-1 (Social Sharing URL) — no dependencies
```

**Critical path**: D16 → C48 (D16 must complete before C48 starts)
**Performance path**: R3 → C51 (R3 must complete before C51 starts)
**Independent**: C38, C53-1 (can be developed in parallel with any other work)

---

*Created: 2026-06-19*
*Role: Developer*
*Discussion cycle: Round 14*
*Confidence level: High (based on thorough architecture review, competitor validation, and proven patterns from previous sprints)*
*Sources: docs/design/architecture.md (Round 14), docs/design/developer_discussion_r13.md, docs/research/competitor_research.md (Rounds 7-12), docs/state/handoff.md*
