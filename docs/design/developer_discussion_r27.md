# 2026-06-19 Developer Estimate — Sprint 13b Feature Candidates

> **Author**: Developer
> **Context**: Sprint 13a complete (C33 Glossary 99 terms + C48 Story Card). Architecture: 🟢 HEALTHY — 30 service modules, 0 god modules, 100% Streamlit-free, L0: 101/101, L1: 20/20, Tests: 149/149.
> **Sprint 13b budget**: 26-38h
> **Scope**: C46 Moat Analysis + C36 Revenue Tree — implementation cost & risk assessment

---

## C46 Moat Analysis — Implementation Estimate

### Service Layer: 4-5h

| Component | Hours | Notes |
|-----------|-------|-------|
| `moat_analyzer.py` — new service | 3-4h | Follows `health_scoring.py` pattern (269 lines, 5-dimension scoring). Core functions: `get_moat_analysis(stock_id) -> dict`, `get_moat_summary(stock_id) -> str`, `compute_moat_score(dimensions: dict) -> int`. Pure functions, no Streamlit imports. |
| Template-based quantitative scoring fallback | 1h | For non-top-20 stocks: R&D spend ratio → technology moat proxy, gross margin → cost advantage proxy, customer concentration → switching cost proxy. Uses existing `financial_metrics.py` data. Add disclaimer flag `"quantitative_estimate": true` to output dict. |

**Service layer total: 4-5h**

### View Layer: 4-5h

| Component | Hours | Notes |
|-----------|-------|-------|
| `_render_moat_section()` in business card | 3-4h | New section file `business_card/_sections/_moat.py`. Renders: 5 mini-cards in `st.columns(5)` (color-coded: green `#27AE60` / yellow `#F39C12` / red `#E74C3C`), historical evidence bullets, overall moat summary. Uses `st.expander(expanded=False)` per designer spec. Reuses `_info_card()` pattern with colored left border. |
| Mobile responsive fallback | 1h | `st.columns(5)` wraps on mobile → use `st.columns(3)` + `st.columns(2)` for narrow viewports. Test with `st.query_params` mobile preview. |

**View layer total: 4-5h**

### Data/Curation: 8-10h

| Component | Hours | Notes |
|-----------|-------|-------|
| `moat_data.yaml` — 20 stocks × 5 dimensions | 7-9h | Structure: `stock_id → {moat_type, strength, dimensions: {name: {score, evidence}}, summary}`. Each dimension needs: score (0-100), evidence (1-2 sentences, plain language), strength label (寬/窄/無). 20 stocks × ~15 min research + writing per stock = 5h content. 20 stocks × ~10 min YAML formatting + review = 2-4h. |
| Graceful fallback for non-top-20 | 1h | Template scoring from quantitative proxies + `"此為量化估算，非專業分析"` disclaimer. |

**Data/curation total: 8-10h**

### Integration: 1-2h

| Component | Hours | Notes |
|-----------|-------|-------|
| Wire into `business_card/_main.py` | 0.5h | Add import + `_render_moat_section(data)` call in render sequence. Follows existing pattern (takeaways → deltas → health → moat → risk). |
| Wire into `business_card/_sections/__init__.py` | 0.5h | Add export. |
| Tests for `moat_analyzer.py` | 1h | Unit tests: `get_moat_analysis()` returns dict with 5 dimensions, template fallback returns valid structure, score computation is deterministic. |

**Integration total: 1-2h**

### C46 Total Estimate: 17-22h

| Component | Low | High |
|-----------|-----|------|
| Service layer | 4 | 5 |
| View layer | 4 | 5 |
| Data/curation | 8 | 10 |
| Integration + tests | 1 | 2 |
| **TOTAL** | **17** | **22** |

### Technical Risks — C46

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Content creation overrun** — 20 stocks × 5 dimensions is 100 data points. At 15 min/stock average = 5h, but research for less-known stocks takes longer. | 🟡 Medium | Start with 5 obvious moats (TSMC, Uni-President, etc.) to calibrate template. Batch remaining 15 in one session. |
| **Subjectivity of moat assessment** — Different analysts may score differently. | 🟡 Medium | Define clear scoring rubric in YAML comments. Use quantitative proxies as sanity check. Add `confidence: high/medium/low` field per dimension. |
| **Template scoring accuracy** — Quantitative proxies (R&D → technology moat) are imperfect. | 🟢 Low | Disclaimer `"量化估算"` is explicit. Template is fallback only; top 20 get manual curation. |
| **Mobile layout** — 5 `st.columns(5)` cards overflow on mobile. | 🟢 Low | Use CSS media query or conditional column count. Tested pattern from C43 Snowflake. |
| **Architecture compliance** — None. New service is pure, no Streamlit imports. | 🟢 None | Follows `health_scoring.py` pattern exactly. |

---

## C36 Revenue Tree — Implementation Estimate

### Service Layer: 3-4h

| Component | Hours | Notes |
|-----------|-------|-------|
| `revenue_tree.py` — new service | 2-3h | `get_revenue_tree_data(stock_id) -> pd.DataFrame` with columns `[labels, parents, values, colors]`. Reads from `revenue_tree_data.yaml`. Pure function, returns None for missing data. |
| `create_revenue_treemap()` in `chart.py` | 1h | Uses `plotly.express.treemap(path=[...], values=..., color=...)` — straightforward API. Accepts DataFrame from service layer. Returns `go.Figure`. Blue palette (`#3498DB` family). Hover template with segment name + revenue + % + description. |

**Service layer total: 3-4h**

### View Layer: 3-4h

| Component | Hours | Notes |
|-----------|-------|-------|
| Modify `revenue_tree.py` page | 2-3h | Replace pie chart with `st.segmented_control` toggle: [圓餅圖 | 樹狀圖]. Pie chart view = existing code (unchanged). Treemap view = new `create_revenue_treemap()` call. Fallback: `st.info()` for non-top-20 stocks without hierarchical data. |
| Glossary tooltip integration | 1h | Technical terms in treemap labels get `st.tooltip()` from C33 glossary. Reuse `glossary_service.py` lookup. |

**View layer total: 3-4h**

### Data/Curation: 5-7h

| Component | Hours | Notes |
|-----------|-------|-------|
| `revenue_tree_data.yaml` — 20 stocks, hierarchical | 4-6h | Structure: `stock_id → [{name, value, children: [{name, value}]}]`. Level 2 = business segments (from FinMind, ~3-8 per stock). Level 3 = key customers (manual curation, top 20 only). 20 stocks × ~12 min = 4h content. Formatting + review = 1-2h. |
| Segment-level data from FinMind (all stocks) | 1h | FinMind `RevenueBreakdown` API provides segment-level data for most TW stocks. Write fallback in service layer: if no YAML data, attempt FinMind API → flatten to 2-level treemap. This ensures ALL stocks show SOMETHING. |

**Data/curation total: 5-7h**

### Integration: 1-2h

| Component | Hours | Notes |
|-----------|-------|-------|
| No router changes needed | 0h | `revenue_tree` page already registered in `router.py`. |
| Tests for `revenue_tree.py` service | 1h | Unit tests: `get_revenue_tree_data()` returns correct DataFrame structure, returns None for missing stock, FinMind fallback returns valid structure. |
| Tests for `create_revenue_treemap()` | 0.5h | Unit test: returns `go.Figure`, handles empty DataFrame gracefully. |

**Integration total: 1.5-2h**

### C36 Total Estimate: 12.5-17h

| Component | Low | High |
|-----------|-----|------|
| Service layer | 3 | 4 |
| View layer | 3 | 4 |
| Data/curation | 5 | 7 |
| Integration + tests | 1.5 | 2 |
| **TOTAL** | **12.5** | **17** |

### Technical Risks — C36

| Risk | Severity | Mitigation |
|------|----------|------------|
| **FinMind segment data availability** — FinMind may not provide hierarchical segment data for all TW stocks. | 🟡 Medium | Primary: manual YAML curation for top 20. Fallback: FinMind API for segment-level (2-level treemap) for all stocks. Last resort: existing pie chart. Three-tier fallback ensures no empty charts. |
| **Treemap label overflow** — Long segment names overlap in small tiles. | 🟢 Low | Limit to 8 segments at Level 2 (group smaller into "其他"). Truncate labels at 12 chars. Hover tooltip shows full name. |
| **Sunburst vs. Treemap** — Designer recommended treemap (more compact). Architect noted sunburst is more "tree-like". | 🟢 Low | Implement treemap first (simpler, more compact). Sunburst is a one-line change in Plotly (`px.sunburst` vs `px.treemap`). Can A/B test after implementation. |
| **Beginner confusion** — Treemap is less familiar than pie chart. | 🟡 Medium | Default to pie chart view. Treemap is opt-in via toggle. Designer confirmed this approach. |
| **Customer-level data scarcity** — Customer breakdown requires annual report research. | 🟡 Medium | Customer-level (Level 3) is top-20-only enhancement. Segment-level (Level 2) works for all stocks via FinMind. |
| **Architecture compliance** — None. Chart function is pure, service is pure, page handles UI only. | 🟢 None | Follows `chart.py` existing pattern (`create_revenue_pie_chart`, `create_health_snowflake`). |

---

## Combined Sprint 13b Assessment

### Total Hours (Both Features)

| Scenario | C46 | C36 | Combined |
|----------|-----|-----|----------|
| Optimistic (low) | 17 | 12.5 | **29.5** |
| Expected (mid) | 19.5 | 14.5 | **34** |
| Pessimistic (high) | 22 | 17 | **39** |

### Fits in 26-38h Budget?

**🟡 TIGHT — Fits in expected case (34h), exceeds in pessimistic case (39h).**

- **Optimistic (29.5h)**: ✅ Fits comfortably with 3.5h buffer.
- **Expected (34h)**: ✅ Fits with 4h buffer.
- **Pessimistic (39h)**: ❌ Exceeds by 1h. Content creation overrun on both features simultaneously.

### Key Observations

1. **Content creation is 47% of total effort** (13-17h of 29.5-39h). This is the primary risk. Both features require manual curation for 20 stocks. If content creation takes longer than expected, both features slip.

2. **No shared infrastructure risk**. C46 and C36 are independent — different services, different YAML files, different view code. They can be built in parallel or sequentially without coupling.

3. **C36 has lower risk and lower effort**. It reuses an existing page, existing router entry, and existing pie chart as fallback. C46 is a new section with new content. **Recommendation: Start C36 first** (quick win, builds confidence, establishes YAML pattern), then C46.

4. **Both features reuse existing patterns extensively**:
   - C46 → `health_scoring.py` scoring pattern, `_info_card()` view pattern
   - C36 → `chart.py` chart pattern, existing `revenue_tree.py` page, existing pie chart

5. **Test burden is low** (~2.5-3h total). Both services are pure functions with deterministic outputs. No async, no external API dependencies in tests (YAML mocking is trivial).

### Scope Adjustment Recommendations

**Option 1: Full Scope (Recommended)**
- Both C46 and C36 at full scope
- Expected: 34h (fits in 26-38h budget)
- Risk: Content creation overrun could push to 39h
- Mitigation: Start content curation in first 2 days. If Day 2 content is behind schedule, activate Option 2.

**Option 2: Reduced Scope (Fallback)**
- C36: Segment-level only (no customer-level Level 3). Saves 2-3h curation. All stocks get treemap from FinMind data.
- C46: Reduce manual curation from 20 to 12 stocks. Saves 3-4h. Template scoring for remaining 8.
- Revised total: 24-29h. Comfortable fit.

**Option 3: Sequential (Conservative)**
- Sprint 13b: C36 only (12.5-17h) + begin C46 `moat_data.yaml` curation
- Sprint 13c: C46 page + remaining curation
- Lowest risk, but delays C46 by one sprint.

### Final Recommendation

**Pursue Option 1 (Full Scope) with Option 2 as fallback.**

**Execution order:**
1. **Day 1-2**: Create both YAML data files (parallel curation). C36 `revenue_tree_data.yaml` first (simpler structure), then C46 `moat_data.yaml`.
2. **Day 2-3**: Build `revenue_tree.py` service + `create_revenue_treemap()` chart function (C36 service layer).
3. **Day 3-4**: Build `moat_analyzer.py` service (C46 service layer). Reuse `health_scoring.py` patterns.
4. **Day 4-5**: Build C36 view (modify `revenue_tree.py` page with toggle).
5. **Day 5-6**: Build C46 view (new `_moat.py` section in business card).
6. **Day 6-7**: Integration, tests, L0/L1 verification, polish.

**Critical path**: YAML curation → service layer → view layer → tests. C36 and C46 can be built in parallel after YAML files exist.

**Go/No-Go gate**: End of Day 2, check YAML progress. If < 12 stocks curated for both files combined, activate Option 2 (reduce scope to 12 stocks).

---

*Developer estimate complete. All estimates include architecture layer separation, testing, and QA time. Confidence: 🟡 Medium — content creation is the primary uncertainty. Technical risk is low (proven patterns, no new architecture).*
