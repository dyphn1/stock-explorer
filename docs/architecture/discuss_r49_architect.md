# 2026-06-17 Technical Analysis — Discussion Round 49

> **Author**: System Architect
> **Context**: Sprint 23 ✅ COMPLETE (C199, C200, C202). Sprint 24 IN PROGRESS — C201 design complete but not yet implemented. This is a DISCUSSION cycle evaluating C201 readiness and feasibility of C203/C209 for Sprint 24+.
> **Architecture Health**: B+ (545 tests passing, all green. i18n cleanup complete.)
> **Key Constraint**: All data must come from free FinMind APIs. No paid APIs. Template-based narratives only (no LLM).

---

## 1. C201 Readiness Assessment

### Status: ✅ READY TO IMPLEMENT — No Blockers

**Evidence**:
- Architecture design doc is complete: `docs/architecture/c201_daily_market.md` (714 lines, §1-10)
- All data sources are confirmed free FinMind APIs via existing `FinMindClient` + `BatchAPI` + `market_data` service layer
- All UI components to be reused from `_router_base.py` (`_白话_card`, `_info_card`, `_summary_card`, `_section_title`)
- Effort estimate: **6-8 hours** (single new file + minor router/i18n changes)

### What Needs to Be Done

| Step | File | Change | Hours |
|------|------|--------|-------|
| 1 | `src/pages/daily_market.py` | **CREATE** — new page module with `_render_daily_market(client)` + 6 helper functions | 3-4 |
| 2 | `src/pages/router.py` | Add `"daily_market"` to `PAGE_KEYS`; add import + `if page_key == "daily_market"` branch in `load_and_render_page()` | 0.5 |
| 3 | `locales/zh-TW.yaml` + `locales/en.yaml` | Add ~50 new i18n keys under `daily_market:` section | 1.5 |
| 4 | `src/pages/url_sync.py` | Add `"今日市場動態"` to `VALID_PAGES` set | 0.25 |
| 5 | Testing | Verify all 5 sections render; verify i18n; verify freshness indicator | 1-2 |

### Confirmed Details

- **No new API methods needed**: All data via `market_data.get_sector_grid_data()` which already fetches all stock info + batch summaries + computes sector metrics
- **No new services needed**: Reuses `adaptive_engine.get_all_recent_events()` for events section
- **Template-based narrative**: No LLM. Uses i18n template strings with `{placeholders}` — deterministic, testable, i18n-friendly
- **Pattern follows existing conventions**: Same pattern as `investor_story_feed.py` (C116) and `sector_heatmap.py` — standalone page with `_render_navbar_minimal()` + `st.spinner()` + section helpers

### Open Questions from Design Doc (§10)

1. **TAIEX index data**: Does FinMind's free tier provide TAIEX directly? If not, compute proxy from all stock summaries. → **Recommendation**: Use proxy for MVP; verify FinMind `taiwan_stock_daily` with `"TAIEX"` ticker
2. **Volume baseline**: 5-day average volume requires historical storage. → **Recommendation**: Show absolute volume only for MVP (simpler, no new data needed)
3. **Event filtering**: `get_all_recent_events()` returns per-stock events; need market-level filter. → **Recommendation**: Post-filter by event type (earnings, dividend, institutional) or add `market_only=True` parameter

### Risks

- **Low risk**: All dependencies exist. No new data sources. No new services. Purely additive.
- **Only risk**: Page load time if `get_sector_grid_data()` is slow (fetches all stocks). Mitigated by existing 24h cache on stock info.

---

## 2. C203 Supply Chain Visual Map — Feasibility Assessment

### Status: 🟡 FEASIBLE WITH CONSTRAINTS — Defer to Sprint 25+

**Context from prior analysis**:
- `docs/state/handoff.md`: C203 estimated 18-25h, HIGH risk, scheduled for Sprint 25
- `docs/state/pending_review.md`: FinMind's supply chain API (`taiwan_stock_industry_chain`) is **paid-only**
- `docs/architecture/discuss_r46_architect.md`: Recommended deferring as capstone feature

### Data Source Analysis

| Source | Availability | Cost | Coverage |
|--------|-------------|------|----------|
| FinMind `taiwan_stock_industry_chain` | Paid API only | ❌ Violates free-only constraint | Full TW market |
| `src/data/group_structures.yaml` | ✅ Exists (112 lines) | Free | Parent-subsidiary only (12 stocks) |
| Manual curation (annual reports) | ✅ Possible | Free | Labor-intensive |
| Public sources (TWSE, company websites) | ✅ Possible | Free | Inconsistent format |

### What C203 Would Require

1. **Data layer**: New `src/services/supply_chain_service.py` — loads relationship data, enriches with FinMind price data for overlay (stock price change of key suppliers/customers)
2. **Visualization**: Network-style graph (Plotly or D3.js). No existing network diagram component in codebase. `chart.py` has `create_funnel_chart()` but not network graphs.
3. **Page**: New `src/pages/supply_chain_map.py` — dedicated page with stock selector + network visualization
4. **Data curation**: Customer-supplier relationships for top 20-50 TW stocks. `group_structures.yaml` has parent-subsidiary data for ~12 stocks but NOT customer-supplier relationships.

### Feasibility Verdict

- **Technical feasibility**: 🟡 Medium. Network visualization is new territory for the codebase. Plotly `scatter` + `line` traces can approximate a network graph but true force-directed layout requires D3.js (heavy dependency) or `networkx` + Plotly.
- **Data feasibility**: 🔴 Low. True supply chain data (customer-supplier relationships) is not available via free APIs. Manual curation is the only option — estimated 2-4 hours per stock for research + data entry.
- **Alignment with historian positioning**: 🟡 Medium. Supply chain maps explain *relationships* between companies, which supports historical understanding ("TSMC matters because NVIDIA/Apple/AMD depend on it"). But it's a significant departure from the company-centric narrative focus.
- **Recommendation**: **Defer to Sprint 25+**. If pursued, use static YAML data (Option A from r46 analysis) for top 20 stocks. Do NOT attempt full market coverage. Consider a simpler "ecosystem cards" approach instead of a full network graph for v1.

### Effort Re-estimate

| Component | Hours |
|-----------|-------|
| Data curation (20 stocks × relationships) | 15-20 |
| `supply_chain_service.py` | 4-6 |
| `supply_chain_map.py` (page) | 6-8 |
| Visualization (network graph) | 8-12 |
| Testing + edge cases | 3-4 |
| **Total** | **36-50 hours** |

This is significantly higher than the original 18-25h estimate. The original estimate assumed Option A + existing data, but existing data (`group_structures.yaml`) only has parent-subsidiary relationships, NOT customer-supplier relationships needed for a true supply chain map.

---

## 3. C209 Source Transparency Layer — Feasibility Assessment

### Status: 🟡 FEASIBLE BUT LOW VALUE — Defer or Redesign

**Context from prior analysis**:
- `docs/state/handoff.md`: C209 estimated 10-15h, MEDIUM risk, Sprint 25
- `docs/CHALLENGE_LOG.md`: C209 challenged as potentially misaligned with historian positioning — "Does adding source citations for every metric enhance historical understanding, or does it clutter the interface?"

### What C209 Would Require

**Original concept** (from competitor research): Show source citations for every data point — which API endpoint, when fetched, data freshness. Similar to TipRanks' analyst track record transparency.

**Implementation components**:
1. **Data provenance tracking**: Add metadata to every API response — source API endpoint, fetch timestamp, cache status
2. **UI layer**: Small "source" link/button next to each metric that shows provenance tooltip
3. **Service changes**: Modify `FinMindClient` to attach provenance metadata to returned DataFrames
4. **Page changes**: Add provenance display to all existing pages (business_card, financial_health, etc.)

### Feasibility Verdict

- **Technical feasibility**: 🟡 Medium. Requires modifying the data layer to carry provenance metadata through the pipeline (API → service → page). Non-trivial refactoring.
- **Data feasibility**: ✅ High. All data already has known sources (FinMind API endpoints). Just need to capture and display.
- **UI feasibility**: 🟡 Medium. Adding source citations to EVERY metric on EVERY page is a significant UI change. Risk of cluttering the PPT-style layout.
- **Alignment with historian positioning**: 🔴 **Questionable**. The CHALLENGE_LOG correctly identifies the tension: "The historian's role is to interpret what the data means in the context of the company's story, not to encourage users to question every data point's provenance." Beginners don't care about API endpoints.
- **Recommendation**: **Redesign as "Data Freshness Indicator" (C213) instead**. Rather than showing source citations for every metric, show a single freshness indicator per page (which already exists via M5's `check_data_freshness()`). This delivers 80% of the transparency value with 10% of the effort. If full source transparency is desired, implement it as a collapsible "資料來源" section at the bottom of each page — not inline citations.

### Effort Re-estimate

| Approach | Hours | Value |
|----------|-------|-------|
| Original (inline citations on every metric) | 15-20 | Low — clutters UI |
| Redesigned (collapsible source section per page) | 4-6 | Medium — clean, informative |
| Minimal (reuse M5 freshness indicator) | 1-2 | Low-Medium — already exists |

---

## 4. Sprint 24 Recommendations

### Immediate Priority: Implement C201

**C201 is ready NOW**. All design is complete, all dependencies exist, no blockers. Estimated 6-8 hours. This should be the sole focus of Sprint 24 Week 1.

### Sprint 24 Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| Week 1 | C201 implementation | `daily_market.py` created, routed, i18n keys added, tested |
| Week 2 | C201 testing + bug fixes | All 5 sections verified, edge cases handled, 545+ tests still green |
| Week 3 | C203/C209 evaluation | Daniel decides on C203 static data approach; C209 redesign decision |
| Week 4 | Buffer / C206 prep | If C201 ships early, begin C206 (Recurring Investment Education) prep |

### Recommended Feature Order (Sprint 24-25)

1. **C201** (Sprint 24) — Daily Market Dashboard ✅ Ready
2. **C206** (Sprint 24 stretch) — Recurring Investment Education (6-8h, pure educational content, no new data)
3. **C203** (Sprint 25) — Supply Chain Visual Map (36-50h, needs data curation)
4. **C209** (Sprint 25+) — Source Transparency Layer (redesigned as collapsible source section, 4-6h)

### C206 Quick Assessment

- **Feasibility**: ✅ High. Pure educational content — no new data sources, no new services
- **Effort**: 6-8 hours
- **Alignment**: 🟡 Medium. Educational content about dollar-cost averaging is useful but tangential to historian positioning. Could be added to `academy.py` or as a new lesson in the existing education system.
- **Recommendation**: Bundle with C201 in Sprint 24 as stretch goal. Low risk, low effort, fills education gap.

---

## 5. Risks

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C201 page load time (all-stock batch fetch) | Medium | Medium | Existing 24h cache on stock info; spinner UI |
| C203 data curation effort exceeds estimate | High | High | Start with top 10 stocks only; use simplified "ecosystem cards" v1 |
| C209 refactoring breaks existing pages | Medium | Medium | Implement as additive layer (collapsible section), not inline changes |
| FinMind API rate limits during C201 load | Medium | Low | Existing `FinMindRateLimitError` handling in `_router_base.py` |

### Product Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C203 scope creep (full network graph vs simple cards) | High | High | Define MVP scope upfront: static YAML data, top 20 stocks, simple cards |
| C209 misalignment with historian positioning | Medium | High | Redesign as freshness indicator / collapsible source section |
| C206 regulatory concerns (investment education) | Medium | Medium | Add disclaimer; frame as educational only |

### Architecture Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| `daily_market.py` grows too large (all helpers in one file) | Low | Low | Follow existing pattern: page file + service file if logic is complex |
| i18n key proliferation (~50 new keys for C201) | Low | Low | Organized under `daily_market:` namespace; follows existing convention |
| `group_structures.yaml` becomes stale (C203 dependency) | Medium | Medium | Document data source + update schedule; add last-updated timestamp |

---

## 6. Summary

| Feature | Status | Ready? | Effort | Risk | Recommendation |
|---------|--------|--------|--------|------|----------------|
| **C201** Daily Market Dashboard | Design complete | ✅ YES | 6-8h | Low | **Implement now — Sprint 24 Week 1** |
| **C203** Supply Chain Visual Map | Concept only | ❌ NO | 36-50h | High | **Defer to Sprint 25**; needs data curation strategy |
| **C209** Source Transparency Layer | Concept only | ⚠️ Redesign | 4-6h | Medium | **Redesign** as collapsible source section; defer to Sprint 25 |
| **C206** Recurring Investment Education | Concept only | ✅ YES | 6-8h | Low | **Stretch goal for Sprint 24**; bundle with C201 |

**Bottom line**: C201 is the clear next step. It's designed, de-risked, and ready to build. C203 and C209 need significant re-evaluation before committing sprint time. C206 is a viable stretch goal if C201 ships early.
