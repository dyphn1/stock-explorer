# Developer Discussion — Round 8 Feature Cost Estimates

> **Date**: 2026-06-13
> **Author**: Developer
> **Context**: Cost estimation for 6 features from Round 8 competitor research (C36-C41)
> **Architecture**: Strictly layered (View → Service → Data). No Streamlit imports in service/data layers.

---

## Assumptions

- All estimates assume a single developer familiar with the existing codebase.
- Estimates include implementation, basic error handling, and manual testing (not formal QA).
- "Manual curation" time is included where YAML/data work is needed.
- The 50% buffer from the Sprint planning discussion is **not** included in base estimates but noted separately.
- Existing infrastructure (analogy_engine, adaptive_engine, chart.py theme system, _router_base helpers) can be reused.

---

## C36: Visual Revenue Tree (營收樹狀圖)

### Description
Extend the existing revenue pie chart with a hierarchical treemap/sunburst showing how money flows through the business — e.g., "TSMC → 5nm chips (40%) → Apple (25%), NVIDIA (15%), AMD (10%)".

### Implementation Steps

1. **Service layer — Add treemap/sunburst chart function** (`src/services/chart.py`)
   - Add `create_revenue_treemap(hierarchy_data, title)` function
   - Use `plotly.express.treemap` or `go.Sunburst` for hierarchical visualization
   - Follow existing `_apply_theme_layout()` pattern for theme-aware styling
   - Input: hierarchical data structure with `labels`, `parents`, `values`, `descriptions`
   - Output: `go.Figure`
   - Time: **2-3h**

2. **Service layer — Add hierarchical revenue data builder** (`src/services/revenue_analyzer.py`)
   - Add `build_revenue_hierarchy(stock_id, financial_df, industry)` function
   - Extend `KNOWN_COMPANY_REVENUE` dict with customer/supplier breakdowns for top 20 stocks
   - Return hierarchical structure compatible with Plotly treemap
   - Time: **3-4h** (includes data research + curation for ~8 stocks that have existing pie data)

3. **View layer — Add "Revenue Tree" tab** (`src/pages/business_card.py`)
   - Add tab next to existing pie chart: `tab1, tab2 = st.tabs(["圓餅圖", "營收樹狀圖"])`
   - Call new service functions, render with `st.plotly_chart()`
   - Handle empty data gracefully (fallback message)
   - Time: **1-2h**

4. **Data curation** (YAML/Python dict)
   - Research and encode customer/supplier relationships for top stocks
   - TSMC, 鴻海, 聯發科, 台達電, 富邦金, 台泥, 中鋼, 台塑
   - Time: **2-3h**

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/services/chart.py` | Modify | Add `create_revenue_treemap()` |
| `src/services/revenue_analyzer.py` | Modify | Add `build_revenue_hierarchy()`, extend `KNOWN_COMPANY_REVENUE` |
| `src/pages/business_card.py` | Modify | Add treemap tab in revenue section |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Chart function (service) | 2.5 |
| Hierarchy builder + data curation | 6.5 |
| View tab integration | 1.5 |
| **Total** | **10.5h** |

### Technical Risks

- **Data availability**: FinMind doesn't provide customer/supplier breakdowns. All hierarchical data must be manually curated from annual reports. Risk: **Medium** — limits coverage to ~8-10 stocks initially.
- **Chart complexity**: Sunburst with 2-3 levels can become cluttered. Need careful color/label management. Risk: **Low** — Plotly handles this well.
- **Hierarchy depth variation**: Different companies have different levels (some have customer data, some only segment data). Need flexible data structure. Risk: **Low** — can use optional fields.

### Dependencies

- **Depends on**: Existing `create_revenue_pie_chart()` pattern, `analyze_revenue_breakdown()` data flow
- **Blocks**: None
- **Shares infrastructure with**: C37 (both on business card page)

---

## C37: Key Takeaways Summary Card (重點摘要)

### Description
Add a "📋 重點摘要" card at the top of the business card page with 3-5 auto-generated key takeaways synthesizing the most important information.

### Implementation Steps

1. **Service layer — Add key takeaways generator** (`src/services/analogy_engine.py`)
   - Add `generate_key_takeaways(stock_id, stock_name, industry, extra_metrics, latest_per_pbr, monthly_revenue, financial_df)` function
   - Use existing analogy functions (`get_one_liner`, `get_gross_margin_analogy`, `get_yoy_analogy`, etc.) as building blocks
   - Apply rule-based synthesis: pick top 3-5 most significant metrics/facts
   - Return list of 3-5 plain-language bullet strings
   - Time: **2-3h**

2. **View layer — Add summary card** (`src/pages/business_card.py`)
   - Add `_info_card` or custom card at the top of `_render_business_card()`, after the header but before "一句話定位"
   - Call `generate_key_takeaways()` with available data
   - Handle empty results gracefully (skip card)
   - Time: **1-2h**

3. **Enhancement — Stock-specific takeaways** (`src/services/analogy_engine.py`)
   - Add curated key takeaways for top 20 stocks (similar to `get_one_liners` pattern)
   - Fallback to auto-generated takeaways for non-curated stocks
   - Time: **2-3h** (research + writing)

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/services/analogy_engine.py` | Modify | Add `generate_key_takeaways()`, extend curated data |
| `src/pages/business_card.py` | Modify | Add summary card at top of page |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Takeaway generator (service) | 2.5 |
| View card integration | 1.5 |
| Curated takeaways for top 20 stocks | 2.5 |
| **Total** | **6.5h** |

### Technical Risks

- **Synthesis quality**: Rule-based synthesis may produce generic-sounding takeaways. Risk: **Medium** — mitigated by curated takeaways for top stocks.
- **Data dependency**: Takeaways quality depends on `extra_metrics` being populated. If data is sparse, takeaways will be thin. Risk: **Low** — graceful degradation built in.
- **Localization**: All output must be in Chinese (zh-TW). Risk: **Low** — existing analogy_engine already handles this.

### Dependencies

- **Depends on**: Existing `analogy_engine.py` functions, `extra_metrics` from `_router_base._calc_extra_metrics()`
- **Blocks**: None
- **Shares infrastructure with**: C36, C39 (all on business card page)

---

## C38: Compare Stories Side-by-Side (故事比較)

### Description
Add a "故事比較" tab to the peer comparison page showing two companies' key events, revenue milestones, and business models side-by-side with plain-language narrative.

### Implementation Steps

1. **Service layer — Add narrative comparison builder** (`src/services/analogy_engine.py`)
   - Add `compare_company_narratives(stock_data_a, stock_data_b)` function
   - Generate side-by-side comparison of: one-liner, revenue model, key metrics narrative, recent events
   - Return structured dict with comparison sections
   - Time: **2-3h**

2. **Service layer — Add narrative comparison chart** (`src/services/chart.py`)
   - Add `create_comparison_timeline(events_a, events_b, name_a, name_b)` function
   - Optional: side-by-side milestone timeline using Plotly
   - Time: **2-3h**

3. **View layer — Add "故事比較" tab** (`src/pages/peer_comparison.py`)
   - Add tab to existing page: `tab1, tab2 = st.tabs(["指標比較", "故事比較"])`
   - Reuse existing benchmark data loading (`_get_benchmark_data`)
   - Render narrative comparison cards side-by-side using `st.columns(2)`
   - Time: **3-4h**

4. **Data — Event/milestone curation** (YAML or Python dict)
   - Add key milestones for top 10 stocks (founding, major products, expansions)
   - Time: **2-3h**

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/services/analogy_engine.py` | Modify | Add `compare_company_narratives()` |
| `src/services/chart.py` | Modify | Add `create_comparison_timeline()` (optional) |
| `src/pages/peer_comparison.py` | Modify | Add "故事比較" tab, side-by-side rendering |
| New YAML or Python dict | Create | Company milestones data |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Narrative comparison builder | 2.5 |
| Timeline chart (optional) | 2.5 |
| View tab integration | 3.5 |
| Milestone data curation | 2.5 |
| **Total** | **11h** |

### Technical Risks

- **Narrative quality**: Auto-generated narrative comparisons may feel mechanical. Risk: **Medium** — mitigated by reusing analogy_engine patterns.
- **Data intensity**: Requires loading two companies' full data sets. Already handled by existing `_get_benchmark_data()` pattern. Risk: **Low**.
- **Scope creep**: Could expand to include event timeline, revenue model comparison, etc. Need to scope tightly. Risk: **Medium** — defer nice-to-haves to v2.

### Dependencies

- **Depends on**: Existing peer comparison page infrastructure, `_get_benchmark_data()`, analogy_engine
- **Blocks**: None
- **Shares infrastructure with**: C37 (both extend analogy_engine)

---

## C39: What Changed Recently Delta Card (最近有什麼變化)

### Description
Add a "🔄 最近有什麼變化" card comparing current metrics (last 30 days) vs previous period (30-60 days ago), highlighting significant changes (>10%) with plain-language explanations.

### Implementation Steps

1. **Service layer — Add delta calculator** (`src/services/adaptive_engine.py`)
   - Add `compute_recent_deltas(data: dict)` function
   - Compare: revenue (last month vs prior month), price (last 30d vs prior 30d), gross margin (latest quarter vs prior quarter)
   - Return list of delta objects: `{metric, current, previous, change_pct, direction, explanation}`
   - Time: **2-3h**

2. **Service layer — Add delta explanation generator** (`src/services/analogy_engine.py`)
   - Add `explain_delta(metric_name, change_pct, direction, stock_name, industry)` function
   - Generate plain-language explanations for significant changes
   - Reuse existing analogy patterns
   - Time: **1-2h**

3. **View layer — Add delta card** (`src/pages/business_card.py`)
   - Add card after "關鍵數字三連卡" section
   - Show deltas with emoji indicators (📈/📉) and plain-language explanations
   - Only show if significant changes detected (>10%)
   - Time: **1-2h**

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/services/adaptive_engine.py` | Modify | Add `compute_recent_deltas()` |
| `src/services/analogy_engine.py` | Modify | Add `explain_delta()` |
| `src/pages/business_card.py` | Modify | Add delta card section |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Delta calculator (service) | 2.5 |
| Delta explanation generator | 1.5 |
| View card integration | 1.5 |
| **Total** | **5.5h** |

### Technical Risks

- **Data granularity**: Monthly revenue only updates monthly, so "recent" changes may be stale. Risk: **Low** — can use daily price data for more timely signals.
- **Threshold tuning**: 10% threshold may need adjustment per metric. Risk: **Low** — easy to tune constants.
- **Overlap with adaptive_engine**: Existing `detect_revenue_event()` already detects >30% YoY changes. Need to avoid duplication. Risk: **Low** — C39 focuses on shorter time horizons (30d) and plain-language explanations.

### Dependencies

- **Depends on**: Existing `adaptive_engine.py` event detection patterns, `extra_metrics`, `monthly_revenue`, `daily_price` data
- **Blocks**: None
- **Shares infrastructure with**: C37 (both on business card page, both use analogy_engine)

---

## C40: Beginner/Expert Mode Toggle (新手/進階模式)

### Description
Add a session_state toggle ("🌱 新手模式" / "🔬 進階模式") in the navbar. Beginner mode shows only essential metrics; Expert mode shows everything.

### Implementation Steps

1. **Router layer — Add mode toggle** (`src/pages/router.py`)
   - Add mode toggle in `_render_navbar()` or as a sidebar element
   - Store mode in `st.session_state["display_mode"]` with default "beginner"
   - Time: **1-2h**

2. **Service layer — Add mode-aware data filter** (`src/pages/_router_base.py`)
   - Add `filter_data_by_mode(data: dict, mode: str) -> dict` function
   - In beginner mode: reduce to essential metrics only
   - In expert mode: pass through unchanged
   - Time: **2-3h**

3. **View layer — Business card adaptations** (`src/pages/business_card.py`)
   - In beginner mode: show only one-liner, 3 key metrics, revenue pie, and "Did You Know?"
   - Hide: detailed dividend table, institutional charts, detailed financial ratios
   - Time: **2-3h**

4. **View layer — Other page adaptations** (multiple files)
   - `operation_checkup.py`: Simplify to 3-4 key metrics
   - `financial_health.py`: Show only health score and key ratios
   - `peer_comparison.py`: Show only comparison table, hide radar chart
   - Time: **3-4h**

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/pages/router.py` | Modify | Add mode toggle in navbar |
| `src/pages/_router_base.py` | Modify | Add `filter_data_by_mode()` |
| `src/pages/business_card.py` | Modify | Conditional rendering by mode |
| `src/pages/operation_checkup.py` | Modify | Conditional rendering by mode |
| `src/pages/financial_health.py` | Modify | Conditional rendering by mode |
| `src/pages/peer_comparison.py` | Modify | Conditional rendering by mode |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Mode toggle in router | 1.5 |
| Data filter function | 2.5 |
| Business card adaptations | 2.5 |
| Other page adaptations | 3.5 |
| **Total** | **10h** |

### Technical Risks

- **Scope management**: Deciding what's "beginner" vs "expert" is subjective and may need iteration. Risk: **Medium** — start with a simple heuristic (3-4 metrics per section for beginner).
- **State persistence**: Mode preference should persist across page switches. `session_state` handles this. Risk: **Low**.
- **Testing matrix**: Each page now has 2 rendering paths. Doubles visual testing effort. Risk: **Medium** — mitigated by keeping beginner mode as a subset of expert mode.
- **Cross-page consistency**: Need to ensure mode is applied consistently across all pages. Risk: **Medium** — use shared `filter_data_by_mode()` helper.

### Dependencies

- **Depends on**: All pages that will support mode toggle
- **Blocks**: None (can be rolled out incrementally per page)
- **Shares infrastructure with**: None (standalone feature)

---

## C41: Read Next Recommendations (接著看)

### Description
Add a "📖 接著看" section to the business card page with 2-3 recommended companies based on industry peers, parent-subsidiary relationships, and customer-supplier relationships.

### Implementation Steps

1. **Service layer — Add recommendation engine** (`src/services/analogy_engine.py` or new `src/services/recommendation_engine.py`)
   - Add `get_read_next_recommendations(stock_id, industry, data: dict)` function
   - Recommendation sources:
     1. Same industry #2 player (from `INDUSTRY_BENCHMARKS` in peer_comparison.py)
     2. Parent-subsidiary relationships (from `KNOWN_GROUP_STRUCTURES` in group_structure.py)
     3. Customer-supplier relationships (manual curation for top 20 stocks)
   - Return list of `{stock_id, stock_name, reason, relationship_type}`
   - Time: **2-3h**

2. **Data curation — Relationship mapping** (YAML or Python dict)
   - Add customer-supplier relationships for top 20 stocks
   - E.g., TSMC → Apple (customer), TSMC → ASML (supplier)
   - Time: **2-3h**

3. **View layer — Add recommendations section** (`src/pages/business_card.py`)
   - Add "📖 接著看" section at the bottom of the business card page
   - Show 2-3 recommendation cards with plain-language reasons
   - Each card clickable → navigate to that stock's business card
   - Time: **1-2h**

### Files to Create/Modify

| File | Action | Change |
|------|--------|--------|
| `src/services/analogy_engine.py` (or new `recommendation_engine.py`) | Modify/Create | Add `get_read_next_recommendations()` |
| `src/pages/business_card.py` | Modify | Add recommendations section |
| New YAML or Python dict | Create | Customer-supplier relationship data |

### Refined Time Estimate

| Task | Hours |
|------|-------|
| Recommendation engine (service) | 2.5 |
| Relationship data curation | 2.5 |
| View section integration | 1.5 |
| **Total** | **6.5h** |

### Technical Risks

- **Navigation**: Clicking a recommendation needs to trigger `st.session_state["stock_id"] = new_id` + `st.rerun()`. Risk: **Low** — existing navigation patterns handle this.
- **Data coverage**: Relationship data only available for top 20 stocks. Fallback to industry peer for others. Risk: **Low** — graceful degradation.
- **Circular recommendations**: TSMC recommends UMC, UMC recommends TSMC. Not a UX problem, but should be aware. Risk: **Low**.

### Dependencies

- **Depends on**: `INDUSTRY_BENCHMARKS` from `peer_comparison.py`, `KNOWN_GROUP_STRUCTURES` from `group_structure.py`
- **Blocks**: None
- **Shares infrastructure with**: C36 (both need relationship data), C38 (both use peer data)

---

## Summary

### Total Cost for All 6 Features

| Feature | ID | Base Estimate | Refined Estimate | Range |
|---------|-----|---------------|------------------|-------|
| Visual Revenue Tree | C36 | 10-14h | **10.5h** | 10-12h |
| Key Takeaways Card | C37 | 6-8h | **6.5h** | 6-8h |
| Compare Stories | C38 | 12-16h | **11h** | 10-13h |
| What Changed Delta | C39 | 8-10h | **5.5h** | 5-7h |
| Beginner/Expert Mode | C40 | 10-14h | **10h** | 9-12h |
| Read Next | C41 | 6-8h | **6.5h** | 6-8h |
| **Total** | | **52-70h** | **40h** | **36-48h** |

> **Note**: The refined estimate (40h) is lower than the original range (52-70h) because the original estimates didn't account for significant infrastructure reuse. The existing `analogy_engine.py`, `adaptive_engine.py`, `chart.py` theme system, and `_router_base.py` helpers provide substantial building blocks.

> **With 50% buffer** (per Sprint planning convention): **60h** (range: 54-72h)

### Recommended Implementation Order

Considering dependencies, value-to-effort ratio, and risk:

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **1** | C37: Key Takeaways | Highest ROI. Directly addresses "ten-second test". Low risk. No dependencies. Quick win. |
| **2** | C39: What Changed Delta | High value, low cost. Reuses adaptive_engine patterns. Quick win. |
| **3** | C41: Read Next | Good engagement feature. Low cost. Reuses existing peer/group data. |
| **4** | C36: Visual Revenue Tree | High visual impact. Moderate cost. Data curation is the bottleneck. |
| **5** | C38: Compare Stories | Highest cost. Depends on analogy_engine extensions from C37. Defer to after C37 proven. |
| **6** | C40: Beginner/Expert Mode | Cross-cutting concern. Best implemented after all content features are in place. |

### Features That Can Share Infrastructure

1. **C37 + C39 + C41** → All extend `analogy_engine.py`. Can be implemented as a single service-layer sprint.
   - Shared: `generate_key_takeaways()`, `explain_delta()`, `get_read_next_recommendations()` all live in `analogy_engine.py`
   - Combined service-layer effort: ~6h instead of 6.5h

2. **C36 + C41** → Both need relationship/customer-supplier data curation.
   - Shared: Customer-supplier YAML/dict can serve both revenue tree and recommendations
   - Combined data curation: ~3h instead of 5h

3. **C37 + C39 + C41** → All render on the business card page.
   - Shared: Single pass through `business_card.py` modifications
   - Combined view-layer effort: ~4h instead of 5.5h

4. **C38 + C41** → Both use peer/group structure data.
   - Shared: `INDUSTRY_BENCHMARKS` and `KNOWN_GROUP_STRUCTURES` references

### Quick Wins (Highest Value-to-Effort Ratio)

| Rank | Feature | Value | Effort | V/E Ratio |
|------|---------|-------|--------|-----------|
| 1 | **C39: What Changed Delta** | High (makes data feel alive) | 5.5h | ⭐⭐⭐⭐⭐ |
| 2 | **C37: Key Takeaways** | High (ten-second test) | 6.5h | ⭐⭐⭐⭐ |
| 3 | **C41: Read Next** | Medium (engagement/discovery) | 6.5h | ⭐⭐⭐⭐ |
| 4 | **C36: Visual Revenue Tree** | High (visual impact, PPT-style) | 10.5h | ⭐⭐⭐ |
| 5 | **C40: Beginner/Expert Mode** | Medium (progressive disclosure) | 10h | ⭐⭐⭐ |
| 6 | **C38: Compare Stories** | Medium (narrative comparison) | 11h | ⭐⭐ |

### Recommended Sprint Allocation

| Sprint | Features | Base Hours | With 50% Buffer |
|--------|----------|------------|-----------------|
| Sprint 2a | C37 + C39 + C41 (quick wins) | 18.5h | 28h |
| Sprint 2b | C36 (revenue tree) | 10.5h | 16h |
| Sprint 3a | C38 (compare stories) | 11h | 16.5h |
| Sprint 3b | C40 (mode toggle) | 10h | 15h |
| **Total** | | **50h** | **75.5h** |

> **Note**: Sprint 2a bundles the three quick wins because they share `analogoy_engine.py` service-layer work and `business_card.py` view-layer modifications. Implementing them together avoids touching the same files multiple times.

---

*Created: 2026-06-13*
*Maintainer: Developer*
