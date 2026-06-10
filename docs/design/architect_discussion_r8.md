# Architect Discussion — Round 8 Feature Feasibility Analysis

> **Date**: 2026-06-13
> **Author**: System Architect
> **Context**: Round 8 competitor research produced 6 new feature proposals (C36-C41).
> This document analyzes each for technical feasibility, implementation approach, risks, and refined effort.
> Sprint state: Sprint 0 complete, Sprint 1 starting (C28 Spike + LLM Architecture).

---

## Table of Contents

1. [C36: Visual Revenue Tree](#c36-visual-revenue-tree)
2. [C37: Key Takeaways Summary Card](#c37-key-takeaways-summary-card)
3. [C38: Compare Stories Side-by-Side](#c38-compare-stories-side-by-side)
4. [C39: What Changed Recently Delta Card](#c39-what-changed-recently-delta-card)
5. [C40: Beginner/Expert Mode Toggle](#c40-beginnerexpert-mode-toggle)
6. [C41: Read Next Recommendations](#c41-read-next-recommendations)
7. [Overall Recommendation & Priority Matrix](#overall-recommendation)

---

## C36: Visual Revenue Tree

### 1. Technical Feasibility: **Medium**

The core charting capability exists — `chart.py` already has `create_revenue_pie_chart()` and uses Plotly. A treemap/sunburst is a natural extension within the same library. The main complexity is **data**: FinMind does not provide hierarchical revenue breakdowns (segment → customer), so the tree data must be manually curated.

### 2. Recommended Implementation Approach

**Layers involved**: Service (chart) + Presentation (business_card)

| Layer | File | Change |
|-------|------|--------|
| Service | `src/services/chart.py` | Add `create_revenue_treemap()` function. Input: list of `{name, value, parent, description}` dicts. Uses `plotly.express.treemap` or `go.Sunburst`. Follows existing `_apply_theme_layout()` pattern. |
| Service | `src/services/revenue_analyzer.py` | Add `analyze_revenue_tree()` function that returns hierarchical data. Falls back to flat pie-chart data if tree data unavailable. |
| Data | `src/data/company_facts.yaml` (or new file `revenue_tree.yaml`) | Add hierarchical revenue tree data for top 20 stocks. Schema: `{stock_id: {segments: [{name, value, children: [{name, value}]}}}` |
| Presentation | `src/pages/business_card.py` | Add a `st.tabs()` under the existing revenue section: "圓餅圖" tab (existing) and "收入樹狀圖" new tab. Calls `create_revenue_treemap()`. |

**Data flow**: `revenue_tree.yaml` → `analyze_revenue_tree()` → `create_revenue_treemap()` → `st.plotly_chart()` in business_card.

### 3. Dependencies on Existing Systems

- `chart.py` theme system (`_apply_theme_layout`, `_get_chart_colors`) — **reuse directly**
- `revenue_analyzer.py` pattern for data curation — **extend**
- `business_card.py` revenue section — **add tab, no structural change**
- FinMind API — **not used** for tree data (manual curation)

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Manual curation doesn't scale beyond top 20 stocks | Medium | Acceptable for P2. Fallback to pie chart for non-curated stocks. |
| Sunburst/treemap readability on small screens | Low | Use `st.plotly_chart(use_container_width=True)` — already responsive. Test on mobile. |
| Hierarchical data schema changes as we add more stocks | Low | Use a separate YAML file (not embedded in code). Schema is simple nested dict. |
| Plotly sunburst hover text truncation for Chinese labels | Low | Test with real data; adjust `textfont` size if needed. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `create_revenue_treemap()` in chart.py | 2-3h |
| `analyze_revenue_tree()` + YAML data file (top 20 stocks) | 4-5h |
| business_card.py tab integration | 1-2h |
| Testing + responsive adjustments | 1-2h |
| **Total** | **8-12h** (vs. original 10-14h) |

**Rationale for reduction**: The competitor estimate assumed building from scratch. We already have the chart theme system, the revenue section layout, and the pie chart pattern. The treemap function is ~50 lines of Plotly code. Most effort is data curation, not engineering.

---

## C37: Key Takeaways Summary Card

### 1. Technical Feasibility: **High**

This is primarily a **presentation-layer** feature with a thin service layer. The `analogy_engine.py` already generates plain-language descriptions for individual metrics. C37 synthesizes 3-5 of these into a summary card. No new data sources needed.

### 2. Recommended Implementation Approach

**Layers involved**: Service (new) + Presentation (business_card)

| Layer | File | Change |
|-------|------|--------|
| Service | `src/services/summary_engine.py` (new) | New service. `generate_key_takeaways(data: dict) -> list[str]`. Receives the same data dict the View receives. Uses existing `analogy_engine` functions + rule-based selection of top 3-5 metrics. Returns list of 白話 bullet strings. |
| Presentation | `src/pages/business_card.py` | Add a `📋 重點摘要` card at the **top** of `_render_business_card()`, after the header but before the one-liner. Uses existing `_info_card()` HTML pattern. |

**Algorithm for key takeaways** (rule-based, no LLM needed):
1. Always include the one-liner (from `get_one_liner()`)
2. Include the most "impressive" metric (highest absolute value among gross_margin, roe, revenue_yoy, dividend_yield)
3. Include a trend observation (revenue direction, recent news sentiment)
4. Include a "did you know" fact if available
5. Cap at 5 bullets

### 3. Dependencies on Existing Systems

- `analogy_engine.py` — **reuse directly** (get_one_liner, get_gross_margin_analogy, get_yoy_analogy, etc.)
- `company_facts.py` — **reuse** for "did you know" facts
- `_info_card()` in `_router_base.py` — **reuse** for rendering
- `data` dict from router — **already available** in business_card

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Rule-based summaries feel generic/repetitive | Medium | Acceptable for P2. Can be enhanced with LLM later (C28 LLM architecture decision in Sprint 1). |
| Metric selection logic may produce odd combinations | Low | Guard with `None` checks at every step. Return fewer bullets if data is sparse. |
| Summary doesn't update on page rerun (stale) | Low | No session_state caching — recalculate every render. Data comes from fresh `data` dict. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `summary_engine.py` — rule-based generation | 3-4h |
| business_card.py integration (top of page) | 1h |
| Testing with 5-10 stocks for quality | 1-2h |
| **Total** | **5-7h** (vs. original 6-8h) |

**Rationale**: The architecture is clean — pure service function + thin view addition. The analogy engine already does the hard work. The main effort is designing the selection rules and testing output quality across different stock profiles.

---

## C38: Compare Stories Side-by-Side

### 1. Technical Feasibility: **Low-Medium**

This is the most complex feature. The existing `peer_comparison.py` compares **metrics** side-by-side. C38 adds **narrative** comparison — which requires either (a) structured narrative data per stock, or (b) an LLM to generate narratives on the fly. Option (a) requires significant data modeling; option (b) depends on the Sprint 1 LLM architecture decision.

### 2. Recommended Implementation Approach

**Recommended: Phased approach**

**Phase 1 (without LLM)**: Structured narrative comparison
- Add a "故事比較" tab to `peer_comparison.py`
- Compare structured data side-by-side: one-liner, revenue milestones, key events, business model description
- All data already exists: `get_one_liner()`, `KNOWN_COMPANY_REVENUE`, `adaptive_engine` events

**Phase 2 (with LLM, post-Sprint 1)**: Generated narrative comparison
- Feed structured data to LLM for natural language comparison
- Depends on C28 LLM architecture decision

| Layer | File | Change |
|-------|------|--------|
| Service | `src/services/narrative_comparator.py` (new) | `compare_stories(data_a: dict, data_b: dict) -> dict`. Returns structured comparison: `{one_liner: [a, b], revenue_model: [a, b], key_events: [a, b], business_focus: [a, b]}`. |
| Presentation | `src/pages/peer_comparison.py` | Add `st.tabs()` to the page: "指標比較" (existing) and "故事比較" (new). Render side-by-side columns with `_info_card()` for each narrative dimension. |

### 3. Dependencies on Existing Systems

- `analogy_engine.py` (get_one_liner) — **reuse**
- `revenue_analyzer.py` (revenue breakdown) — **reuse**
- `adaptive_engine.py` (get_events_for_stock) — **reuse** for key events
- `peer_comparison.py` existing structure — **extend with tab**
- LLM (future) — **Phase 2 only**

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Narrative comparison feels shallow without LLM | High | Phase 1 uses structured data only — may feel like "reading two business cards side by side" rather than a true narrative comparison. Set expectations accordingly. |
| Loading two companies' event data adds API calls | Medium | Events come from `events.yaml` (local), not API. But if we need fresh data, use the same pattern as `_get_benchmark_data()` with spinner. |
| Scope creep: narrative comparison could become a full product feature | Medium | Strictly limit Phase 1 to 4 narrative dimensions (one-liner, revenue model, events, business focus). Resist adding more. |
| Depends on C28 LLM architecture for Phase 2 | Low | Phase 1 is independently valuable. Phase 2 is a future enhancement. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `narrative_comparator.py` — structured comparison | 4-5h |
| peer_comparison.py tab integration | 2-3h |
| Side-by-side rendering with _info_card | 2-3h |
| Testing with multiple stock pairs | 2-3h |
| **Total** | **10-14h** (vs. original 12-16h) |

**Rationale**: The competitor estimate was accurate. This is the most complex feature because it requires a new service module and careful UI design for side-by-side narrative. The phased approach reduces risk.

---

## C39: What Changed Recently Delta Card

### 1. Technical Feasibility: **High**

The data already exists in the `data` dict. The `adaptive_engine.py` already detects revenue anomalies and price abnormalities. C39 is essentially a **presentation-layer repackaging** of existing delta calculations into a dedicated card.

### 2. Recommended Implementation Approach

**Layers involved**: Service (new, thin) + Presentation (business_card)

| Layer | File | Change |
|-------|------|--------|
| Service | `src/services/delta_engine.py` (new) | `compute_recent_changes(data: dict) -> list[dict]`. Computes: revenue delta (30d vs 60d), gross margin delta (current vs prev quarter), price delta (30d), news sentiment delta. Returns `[{icon, label, change_pct, plain_text}]`. All calculations from existing `data` dict fields. |
| Presentation | `src/pages/business_card.py` | Add a `🔄 最近有什麼變化` card after the key metrics section (三連卡). Use `_info_card()` for each significant change (>10% threshold). |

**Delta calculations**:
- Revenue: `monthly_revenue[-1]` vs `monthly_revenue[-4]` (last month vs 3 months ago)
- Gross margin: `extra_metrics["gross_margin"]` vs previous quarter's (from `financial` df)
- Price: `daily_price[-1]` vs `daily_price[-30]`
- News: count of high-impact news in last 30 days vs previous 30 days

### 3. Dependencies on Existing Systems

- `data` dict (monthly_revenue, financial, daily_price, extra_metrics) — **already loaded by router**
- `adaptive_engine.py` event detection — **reuse** for news impact counts
- `analogy_engine.py` — **reuse** for plain-language delta descriptions
- `_info_card()` — **reuse** for rendering

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Delta calculations may be noisy for volatile stocks | Medium | Use >10% threshold to filter insignificant changes. Show "持平" if no significant changes. |
| Financial data may not have quarterly granularity | Medium | Fall back to "資料不足" message. Guard with `None` checks. |
| Card may be empty for stocks with sparse data | Low | Hide the card entirely if no deltas exceed threshold. Return empty list from service. |
| Overlapping with existing event dashboard | Low | Delta card is stock-specific and recent-focused. Event dashboard is portfolio-wide and historical. Complementary, not redundant. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `delta_engine.py` — change computation | 3-4h |
| business_card.py integration | 1-2h |
| Plain-language delta descriptions | 1-2h |
| Testing with volatile vs stable stocks | 1-2h |
| **Total** | **6-10h** (vs. original 8-10h) |

**Rationale**: The adaptive engine already does the hard detection work. This is mostly a new presentation of existing calculations. The service layer is thin (~100 lines).

---

## C40: Beginner/Expert Mode Toggle

### 1. Technical Feasibility: **Medium**

This is a **cross-cutting concern** that affects every stock page. The toggle itself is trivial (session_state + st.radio), but the conditional rendering logic must be added to every section of every page. The risk is inconsistent application and maintenance burden.

### 2. Recommended Implementation Approach

**Layers involved**: Presentation (all pages) + Router (navbar)

| Layer | File | Change |
|-------|------|--------|
| Router | `src/pages/router.py` | Add mode toggle to `_render_navbar()`: `st.session_state["mode"] = st.radio(["🌱 新手模式", "🔬 進階模式"], ...)`. Default: "新手模式". |
| Service | `src/services/mode_config.py` (new) | `get_mode_config(mode: str) -> dict`. Returns visibility config: which sections to show/hide. E.g., `{"show_institutional": False, "show_debt_analysis": False, "max_metrics": 4}` for beginner mode. |
| Presentation | `src/pages/business_card.py` | Wrap advanced sections (institutional charts, detailed financial ratios, debt analysis) in `if get_mode_config(mode)["show_advanced"]`. Limit key metrics to 3-4 in beginner mode. |
| Presentation | `src/pages/operation_checkup.py` | Same pattern: hide advanced charts in beginner mode. |
| Presentation | `src/pages/financial_health.py` | Same pattern: show only pass/fail badges in beginner mode, detailed ratios in expert mode. |
| Presentation | `src/pages/peer_comparison.py` | Same pattern: show only comparison table in beginner mode, radar chart + difference analysis in expert mode. |

**Beginner mode rules**:
- Business card: one-liner ✓, key metrics (3 max) ✓, revenue pie ✓, dividend summary ✓, news ✓. Hide: institutional charts, detailed revenue breakdown descriptions.
- Operation checkup: show only revenue trend and gross margin. Hide: operating margin, detailed expense breakdown.
- Financial health: show only 3 health badges. Hide: detailed ratio tables.
- Peer comparison: show only side-by-side table. Hide: radar chart, difference analysis.

### 3. Dependencies on Existing Systems

- `session_state` — **already managed by router**
- `_render_navbar()` — **extend** with toggle
- All stock pages — **modify** with conditional rendering
- No new data sources needed

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Inconsistent application across pages | High | Create `mode_config.py` as single source of truth. All pages reference it. Add to architecture checklist. |
| Toggle state lost on page navigation | Low | Stored in `session_state["mode"]` — persists across reruns. Already managed by router. |
| Maintenance burden: every new feature must consider both modes | Medium | Document in architecture checklist. Default new features to "expert only" until explicitly added to beginner mode. |
| Beginner mode may feel too sparse | Medium | Test with real beginners (ten-second test). Adjust `mode_config` thresholds based on feedback. |
| Scope: affects 4+ pages | High | This is the widest-impact feature. Must be done systematically, not ad-hoc. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `mode_config.py` — visibility rules | 2-3h |
| router.py navbar toggle | 0.5h |
| business_card.py conditional rendering | 2-3h |
| operation_checkup.py conditional rendering | 1-2h |
| financial_health.py conditional rendering | 1-2h |
| peer_comparison.py conditional rendering | 1-2h |
| Testing across all pages + both modes | 2-3h |
| **Total** | **10-15h** (vs. original 10-14h) |

**Rationale**: The toggle is trivial, but the systematic application across all pages is the effort driver. The competitor estimate was accurate. Slight upward refinement because we have 4 stock pages to modify.

---

## C41: Read Next Recommendations

### 1. Technical Feasibility: **High**

This is a **data-driven** feature with minimal UI complexity. The data sources already exist: `group_structure.py` has parent-subsidiary relationships, `peer_comparison.py` has industry benchmark mappings, and we can add customer-supplier relationships to the existing YAML data.

### 2. Recommended Implementation Approach

**Layers involved**: Service (new) + Presentation (business_card) + Data (YAML)

| Layer | File | Change |
|-------|------|--------|
| Data | `src/data/company_facts.yaml` (or new `relationships.yaml`) | Add relationship data: `{stock_id: {peers: [stock_id, ...], customers: [...], suppliers: [...], related: [...]}}`. Start with top 20 stocks. |
| Service | `src/services/recommendation_engine.py` (new) | `get_read_next(stock_id: str, industry: str) -> list[dict]`. Logic: (1) same industry #2 player from `INDUSTRY_BENCHMARKS`, (2) parent/subsidiary from `group_structure.KNOWN_GROUP_STRUCTURES`, (3) manual relationships from YAML. Returns `[{stock_id, stock_name, reason}]`. Max 3 recommendations. |
| Presentation | `src/pages/business_card.py` | Add a `📖 接著看` section at the bottom of the page (before disclaimer). Show 3 clickable cards with reason text. Use `st.button()` with `navigate_to()` for navigation. |

### 3. Dependencies on Existing Systems

- `group_structure.py` `KNOWN_GROUP_STRUCTURES` — **reuse** for parent-subsidiary
- `peer_comparison.py` `INDUSTRY_BENCHMARKS` — **reuse** for industry peers
- `navigate_to()` from `url_sync.py` — **reuse** for click-to-navigate
- `_info_card()` — **reuse** for rendering recommendation cards

### 4. Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Recommendations may be obvious (e.g., "TSMC → UMC") | Low | Acceptable for P2. The value is in surfacing relationships beginners wouldn't know (customer-supplier, not just competitors). |
| Manual relationship data doesn't scale | Medium | Start with top 20 stocks. For stocks without manual data, fall back to industry peer only. |
| Circular recommendations (A→B→A) | Low | Not a bug — it's a feature. Shows the relationship is bidirectional. |
| Clicking recommendation triggers full page reload | Low | This is the existing navigation pattern (`navigate_to()`). Consistent with current UX. |

### 5. Refined Effort Estimate

| Component | Hours |
|-----------|-------|
| `recommendation_engine.py` — recommendation logic | 2-3h |
| Relationship YAML data (top 20 stocks) | 2-3h |
| business_card.py bottom section | 1-2h |
| Testing recommendation quality | 1h |
| **Total** | **6-9h** (vs. original 6-8h) |

**Rationale**: The competitor estimate was slightly optimistic. The service logic is simple, but curating relationship data for 20 stocks takes time. Slight upward refinement for data curation.

---

## Overall Recommendation

### Priority Matrix

| Feature | Feat. | Effort | Impact to "Historian" | Beginner Value | Dependencies | **Priority** |
|---------|-------|--------|-----------------------|----------------|--------------|-------------|
| **C37** Key Takeaways | High | 5-7h | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | None | **🥇 Sprint 2** |
| **C39** What Changed | High | 6-10h | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | None | **🥈 Sprint 2** |
| **C41** Read Next | High | 6-9h | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | None | **🥉 Sprint 3** |
| **C36** Revenue Tree | Med | 8-12h | ⭐⭐⭐⭐ | ⭐⭐⭐ | Data curation | **Sprint 3** |
| **C40** Mode Toggle | Med | 10-15h | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | All pages | **Sprint 4** |
| **C38** Compare Stories | Low-Med | 10-14h | ⭐⭐⭐⭐⭐ | ⭐⭐ | LLM (Phase 2) | **Sprint 5** |

### Recommended Sprint Allocation

**Sprint 2 (after C28 Spike + LLM decision)**: C37 + C39
- Combined effort: 11-17h (fits within Sprint 2's 15h base + buffer)
- Rationale: Both are high-feasibility, high-impact, no external dependencies. C37 directly addresses the "ten-second test" — the most critical design principle. C39 makes data feel alive, which is core to "historian" positioning.
- Both extend `business_card.py` — minimal context switching for developers.

**Sprint 3 (C28 Story Timeline)**: C41 + C36
- Combined effort: 14-21h (fits within Sprint 3's 20h base + buffer)
- Rationale: C41 creates a learning path that connects to C28's story timeline. C36 extends the revenue section that C37/C39 already touch. Both require data curation that can happen in parallel with C28 development.

**Sprint 4 (C07 + C14)**: C40
- Effort: 10-15h (fits within Sprint 4's 18h base + buffer)
- Rationale: Mode toggle should come **after** the key features (C37, C39, C41) are built, so we know what to hide/show. Building it before the features would be premature optimization.

**Sprint 5 (C29)**: C38
- Effort: 10-14h (fits within Sprint 5's 15h base + buffer)
- Rationale: Compare stories is the most complex and least beginner-critical. It depends on LLM architecture (decided in Sprint 1) and benefits from the narrative data built in C28. Deferring to Sprint 5 is prudent.

### Key Architectural Principles for Implementation

1. **No Streamlit in service layers**: All new service modules (`summary_engine.py`, `delta_engine.py`, `recommendation_engine.py`, `narrative_comparator.py`, `mode_config.py`) must be pure Python with no `st.*` imports.

2. **Data curation in YAML**: All manually curated data (revenue trees, relationships, narrative templates) goes in YAML files under `src/data/` or `config/`, not in Python code.

3. **Graceful degradation**: Every new feature must handle missing data gracefully. If curated data doesn't exist for a stock, fall back to simpler behavior or hide the section. No feature should crash or show errors.

4. **Consistent rendering**: All new cards use `_info_card()` or `_白话_card()` from `_router_base.py`. No inline HTML in new features.

5. **Session_state for mode**: C40's mode toggle must be in `session_state["mode"]` and read by all pages. The router initializes the default.

### Risk Summary

| Risk | Features Affected | Mitigation |
|------|-------------------|------------|
| LLM architecture decision (Sprint 1) blocks narrative features | C38 | Phase C38 without LLM. Use structured data. |
| Data curation bottleneck | C36, C41 | Start with top 10 stocks, not 20. Expand later. |
| C40 scope creep across pages | C40 | Strict `mode_config.py` as single source of truth. |
| Sprint 2 overload | C37 + C39 | If C31 (Daily Story) takes longer than expected, defer C39 to Sprint 3. C37 is non-negotiable (ten-second test). |

### Final Note

The "historian, not stock picker" positioning is best served by **C37 (Key Takeaways)** and **C39 (What Changed)** — they transform raw data into narrative understanding. These two features should be the highest priority regardless of sprint constraints. C38 (Compare Stories) is the most aligned with the historian vision but also the most technically risky — deferring it is the right call.

---

*Created: 2026-06-13*
*Maintainer: System Architect*
*Next review: After Sprint 1 LLM architecture decision*
