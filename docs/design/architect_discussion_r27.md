# 2026-06-13 Technical Analysis — Sprint 13b Feature Candidates

## Problem Description

Sprint 13a delivered C33 (Glossary, 99 terms with tooltips) and C48 (Story Card, always visible). The architecture remains healthy: 30 service modules, 0 god modules, 100% Streamlit-free business logic, L0: 101/101, L1: 20/20, Tests: 149/149.

Sprint 13b candidates from the roadmap:
- **C46 Moat Analysis** (14-20h): 5-dimension moat scoring, manual curation for top 20 stocks
- **C36 Revenue Tree** (12-18h): Plotly hierarchical treemap/sunburst showing how company makes money

Both features align with the "historian" positioning (Core Value #1: Story first) and address competitive gaps identified in Rounds 8-9. This analysis evaluates technical feasibility, architectural impact, and recommends a direction.

---

## Current Codebase State (Relevant to Sprint 13b)

### What Already Exists

1. **Revenue Tree page** (`src/pages/revenue_tree.py`): Already implemented as a standalone page registered in the router as "營收結構樹". Currently renders a flat pie chart + description cards. NOT yet a hierarchical treemap/sunburst.
2. **Health Scoring service** (`src/services/health_scoring.py`): Full 5-dimension scoring engine (`compute_health_scores`, `get_health_summary`) with industry-relative benchmarks. Score dimensions: 獲利能力, 成長性, 財務健康, 股利品質, 估值合理性.
3. **Health Snowflake chart** (`src/services/chart.py` line 494): `create_health_snowflake()` renders a radar chart with color-coded scores, reference lines at 40/70, hover text with metric details. Fully implemented.
4. **Valuation Band Chart** (`src/services/chart.py` line 596): Historical P/E range visualization with percentile positioning. Already implemented.
5. **Revenue Analyzer** (`src/services/revenue_analyzer.py`): `analyze_revenue_breakdown()` with manually curated revenue data for 9 stocks (2330, 2317, 2454, 2308, 2881, 1101, 2002, 1301). Flat structure (no hierarchy).
6. **Data curation pattern**: YAML-based (`src/data/company_facts.yaml`, `src/data/glossary.yaml`, `src/data/case_studies.yaml`) with stock_id keys.
7. **Router**: Already imports and routes `revenue_tree` page. No moat page exists yet.
8. **No moat code exists** anywhere in the codebase (grep for "moat" returned zero results).

---

## Option A: C36 Revenue Tree Upgrade — Hierarchical Treemap/Sunburst

### Description
Upgrade the existing `revenue_tree.py` page from a flat pie chart to a hierarchical visualization. Two levels deep: company → business segments → sub-segments/customers. Use Plotly Express `treemap` or `sunburst` for the interactive chart. Manually curate hierarchical data for top 20 stocks in a new YAML file (`src/data/revenue_tree_data.yaml`).

### Architecture Changes

| Layer | Changes |
|-------|---------|
| **Data** | New `src/data/revenue_tree_data.yaml` — hierarchical revenue data per stock_id |
| **Service** | New service `src/services/revenue_tree.py` — reads YAML, returns hierarchical data structure. New chart function `create_revenue_treemap()` and/or `create_revenue_sunburst()` in `chart.py` |
| **Page** | Modify `src/pages/revenue_tree.py` — replace pie chart with treemap/sunburst, keep existing description cards |
| **Router** | No changes needed (page already registered) |

### Pros
- **Low architectural risk**: Reuses existing page registration, data curation pattern (YAML), and chart infrastructure. No new router entry needed.
- **Incremental upgrade**: Existing flat data (9 stocks in `revenue_analyzer.py`) → hierarchical data (20 stocks in new YAML). Flattening logic in new service ensures backward compatibility.
- **Plotly Express treemap/sunburst is straightforward**: `px.treemap()` and `px.sunburst()` accept `names`, `parents`, `values` columns — trivial DataFrame conversion.
- **Aligns with competitor validation**: Public.com and Koyfin both have hierarchical revenue breakdowns (Round 8 research). No TW competitor has this.
- **Testable**: Pure functions (YAML → DataFrame → fig) are easy to unit test.

### Cons
- **Manual curation effort**: Top 20 stocks × ~5 segments × ~3 sub-segments = ~300 data points to research and enter. This is the bulk of the 12-18h estimate.
- **Limited data source**: FinMind doesn't provide hierarchical revenue breakdowns. All data must be manually curated from annual reports. No API fallback.
- **Sunburst vs. treemap**: Sunburst is more visually "tree-like" but takes more screen space. Treemap is more compact but less intuitive for beginners. UX testing needed.
- **Revenue Tree page is already "done"**: This is an upgrade, not a new feature. Sprint velocity metrics may not count it as new functionality.

### Effort
| Component | Hours |
|-----------|-------|
| New YAML data file (20 stocks) | 6-8 |
| New `revenue_tree.py` service | 2-3 |
| New chart functions in `chart.py` | 2-3 |
| Page redesign (replace pie with treemap/sunburst) | 2-3 |
| Tests (service + chart) | 2-3 |
| Polish (responsive layout, hover text) | 1-2 |
| **Total** | **15-22h** |

### Technical Impact
- **Architecture layers impacted**: Data (new YAML), Service (new module + chart functions), Page (modify existing)
- **New files**: 1 YAML, 1 service module
- **Modified files**: `chart.py` (add functions), `revenue_tree.py` (replace visualization)
- **No architectural violations**: Follows existing layer separation, data curation pattern, and error handling conventions
- **Risk level**: 🟢 LOW

---

## Option B: C46 Moat Analysis — New Page with Manual Curation

### Description
Create a new "🏰 護城河分析" (Moat Analysis) page as a standalone page for each stock. Assess 5 moat dimensions (technology, brand, cost advantage, network effects, switching scores) with strength ratings (wide/narrow/none), historical evidence, and plain-language explanations. Manual curation for top 20 stocks via new YAML file. Template-based fallback for other stocks.

### Architecture Changes

| Layer | Changes |
|-------|---------|
| **Data** | New `src/data/moat_data.yaml` — moat assessments per stock_id with 5 dimensions |
| **Service** | New `src/services/moat_analyzer.py` — reads YAML, computes moat score, generates plain-language moat summary |
| **Page** | New `src/pages/moat_analysis.py` — renders moat dimension cards, radar chart (reuse `create_health_snowflake`), historical evidence, plain-language explanations |
| **Router** | Add import + routing for "護城河分析" page in `router.py` |

### Pros
- **High competitive differentiation**: Morningstar has moat ratings for US stocks only. No TW competitor has moat analysis. This is a "historian" feature — explain what the moat IS and how it protected the company historically, without predicting the future.
- **Reuses existing infrastructure**: Health snowflake radar chart can be reused for moat dimension visualization. Analogy engine patterns for explanations.
- **Strong beginner value**: "Does this company have a durable competitive advantage?" is a fundamental investing question. Answering it in plain language is core to the "historian" positioning.
- **Manual curation = high-quality content**: Unlike automated scores, curated moat analysis provides genuine educational value. Each stock's moat story is unique.

### Cons
- **Highest manual curation effort**: Researching moat dimensions, historical evidence, and writing plain-language explanations for 20 stocks. This is the bulk of the 14-20h estimate.
- **New page = more surface area**: Requires new router entry, new navbar entry, new import. More code to maintain.
- **Template fallback for non-top-20 stocks**: Stocks without curated data will show generic/template moat analysis, which may feel low-quality. Need a graceful "coming soon" message.
- **Subjectivity risk**: Moat assessment involves judgment calls. Different analysts may disagree. Need clear criteria for each dimension to maintain consistency.
- **No FinMind data source**: All moat data is manually curated. Zero API fallback possible.

### Effort
| Component | Hours |
|-----------|-------|
| New YAML data file (20 stocks × 5 dimensions) | 8-10 |
| New `moat_analyzer.py` service | 3-4 |
| New `moat_analysis.py` page | 3-4 |
| Router + navbar integration | 1 |
| Reuse/adapt health snowflake chart | 1 |
| Tests (service + page) | 2-3 |
| Polish (layout, fallback handling) | 1-2 |
| **Total** | **19-28h** |

### Technical Impact
- **Architecture layers impacted**: Data (new YAML), Service (new module), Page (new file), Router (modified)
- **New files**: 1 YAML, 1 service module, 1 page module
- **Modified files**: `router.py` (add import + route + navbar entry)
- **No architectural violations**: Follows existing patterns. New service is pure (YAML → data → fig), no Streamlit imports.
- **Risk level**: 🟡 MEDIUM (higher effort, more new code, subjective content quality)

---

## Option C: Combined Approach — Moat Analysis as Tab on Business Card + Revenue Tree V2

### Description
Instead of standalone pages, integrate both features into the existing Business Card page:
1. **Moat section on Business Card**: Add a "🏰 護城河" section (collapsible expander) at the top of the business card page, showing the moat radar chart + top 2 moat dimensions with explanations. Uses existing `moat_analyzer` service.
2. **Revenue Tree V2**: Upgrade the existing Revenue Tree page as described in Option A.

This approach prioritizes the Business Card as the "hub" and avoids adding new standalone pages. The moat analysis is always visible on the business card (like the Story Card from C48), and the revenue tree remains a deep-dive page.

### Architecture Changes

| Layer | Changes |
|-------|---------|
| **Data** | Two new YAML files: `moat_data.yaml` + `revenue_tree_data.yaml` |
| **Service** | New `moat_analyzer.py` + new `revenue_tree.py` service. New chart functions in `chart.py`. |
| **Page** | Modify `business_card/_main.py` (add moat expander). Modify `revenue_tree.py` (upgrade visualization). |
| **Router** | Minor — "護城河分析" can be a section trigger or a standalone page. Revenue tree already registered. |

### Pros
- **Maximum visibility for moat analysis**: Moat is shown on the Business Card (first page users see), not buried in a standalone page. Aligns with C48 Story Card pattern (always visible).
- **Reduced page proliferation**: 21 pages in router already. Adding another standalone page increases navbar complexity. Embedding moat in Business Card avoids this.
- **Synergy**: Moat analysis references revenue concentration risks (connects to Revenue Tree data). Both features share the "historian" narrative.
- **Incremental delivery**: Can deliver Revenue Tree V2 first (lower risk), then moat section on Business Card.

### Cons
- **Business Card page is growing**: Already has many sections. Adding moat analysis increases page length and initial load time (more data to render).
- **Mixed granularity**: Moat section on Business Card is summary-level; full moat analysis may need a dedicated page eventually.
- **Highest total effort**: Delivering both features in one sprint means ~34-50h total (combined estimates), which exceeds a single sprint capacity.
- **Requires modifying business_card/_main.py**: This is a core page. Any changes risk regressions. Need thorough testing.

### Effort
| Component | Hours |
|-----------|-------|
| Option A (Revenue Tree V2) | 15-22 |
| Option B minus standalone page (Moat section only) | 12-16 |
| Integration + cross-feature synergy | 2-3 |
| **Total** | **29-41h** |

### Technical Impact
- **Architecture layers impacted**: Data (2 new YAMLs), Service (2 new modules), Page (2 files), Router (minor)
- **New files**: 2 YAMLs, 2 service modules
- **Modified files**: `chart.py`, `revenue_tree.py`, `business_card/_main.py`, `router.py`
- **Risk level**: 🟡 MEDIUM-HIGH (highest surface area, modifies core page, combined effort exceeds sprint capacity)

---

## Technical Risks Summary

| Risk | Option A | Option B | Option C |
|------|----------|----------|----------|
| Data availability (no API fallback) | 🟡 Medium — revenue data exists in annual reports | 🟡 Medium — moat analysis requires expert judgment | 🟡 Medium — both |
| Manual curation burden | 🟡 Medium — 20 stocks × ~8 data points | 🟠 High — 20 stocks × 5 dimensions with evidence | 🟠 High — both combined |
| Architectural violations | 🟢 None | 🟢 None | 🟢 None |
| Regression risk | 🟢 Low — modifies existing page | 🟢 Low — new page isolated | 🟡 Medium — modifies Business Card |
| Effort within sprint (20h budget) | 🟢 Fits (15-22h) | 🟡 Tight (19-28h) | 🟠 Exceeds (29-41h) |
| Test coverage | 🟢 Easy to test | 🟢 Easy to test | 🟡 More test surface |
| Competitive differentiation | 🟡 Medium — Public.com/Koyfin have similar | 🟢 High — no TW competitor | 🟢 High — both |

---

## Recommendation

### Pursue Option A (Revenue Tree V2) first, then Option B (Moat Analysis) in a follow-up sprint.

**Rationale:**

1. **Revenue Tree V2 is the lowest-risk, highest-certainty delivery.** The page already exists, the router is already configured, and the data curation pattern is proven (revenue_analyzer.py already has 9 stocks). The upgrade from pie chart → treemap/sunburst is a well-scoped visualization change that directly competes with Public.com and Koyfin.

2. **Moat Analysis is strategically more important but riskier.** It's the feature with the highest competitive differentiation (no TW competitor has it) and strongest "historian" alignment. The 14-20h effort estimate is realistic for the full standalone page. Rushing it in the same sprint as Revenue Tree V2 would compromise quality. Moat data curation requires careful research and editorial judgment — this is not work to rush.

3. **Sprint capacity is ~20h.** Option A (15-22h) fits within a single sprint with modest overflow. Option B (19-28h) is tight but feasible if treated as the sole sprint focus. Combining both (Option C, 29-41h) exceeds capacity.

4. **Dependency ordering matters.** Moat analysis can reference revenue concentration as a risk factor (e.g., "TSMC's moat is deep but 90% revenue from 3 customers is a risk"). Building Revenue Tree V2 first creates a data foundation that enriches the subsequent Moat Analysis.

5. **Recommended Sprint 13b scope:**
   - **Primary**: C36 Revenue Tree V2 — hierarchical treemap/sunburst, 20 stocks, new `revenue_tree.py` service, new chart functions
   - **Stretch**: If C36 finishes early, begin `moat_data.yaml` curation and `moat_analyzer.py` service scaffold (data + pure functions, no page yet)

6. **Sprint 13c scope:**
   - C46 Moat Analysis page — full standalone page with radar chart, 5 dimensions, historical evidence, plain-language explanations

### Key Implementation Notes for the Developer

**For Revenue Tree V2:**
- Create `src/data/revenue_tree_data.yaml` with structure:
  ```yaml
  "2330":
    - name: "先進製程"
      value: 55
      children:
        - name: "3nm"
          value: 30
        - name: "5nm"
          value: 25
    - name: "成熟製程"
      value: 20
  ```
- New service function: `get_revenue_tree_data(stock_id) -> pd.DataFrame` with columns `[labels, parents, values]`
- Use `plotly.express.treemap()` / `sunburst()` — requires only `names`, `parents`, `values`
- Keep the existing description cards below the chart (they add educational value)

**For Moat Analysis (future):**
- Create `src/data/moat_data.yaml` with structure:
  ```yaml
  "2330":
    moat_type: "technology"
    strength: "wide"
    dimensions:
      技術領先: {score: 90, evidence: "3nm量產領先競爭對手2年以上"}
      規模效應: {score: 80, evidence: "全球最大晶圓代工廠，市佔率55%"}
      客戶黏著度: {score: 75, evidence: "轉換成本極高，客戶需重新設計晶片"}
      資本障礙: {score: 85, evidence: "一座先進晶圓廠需投資100億美元"}
      專利壁壘: {score: 70, evidence: "擁有超過5萬項專利"}
    summary: "台積電的護城河建立在技術領先和規模效應上..."
  ```
- Reuse `create_health_snowflake()` for the radar chart (input: 5-dimension scores)
- New service: `get_moat_analysis(stock_id) -> dict` + `get_moat_summary(stock_id) -> str`
- Graceful fallback: "此公司目前尚未建立詳細護城河分析" for non-curated stocks

---

*Analysis by System Architect. Review deadline: before Sprint 13b planning meeting.*
