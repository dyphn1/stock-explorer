# 2026-06-17 Technical Analysis — Discussion Round 52 (Sprint 26 Architecture Assessment)

> **Author**: System Architect
> **Context**: Sprint 25 ✅ COMPLETE (C209 source section, C206 DCA lesson, pre-sprint fixes). 658 tests green. Planning Sprint 26.
> **Architecture Health**: B+ (658 tests passing, all green. i18n refactoring clean. Design system grade C+.)
> **Key Constraint**: All data must come from free FinMind APIs. No paid APIs. Template-based narratives only (no LLM).

---

## 1. C203 — Company Ecosystem Cards v1: Feasibility Assessment

### 1.1 Data Readiness

**`group_structures.yaml` status**: ✅ EXISTS — 5 parent companies, 18 subsidiaries

| Parent | Stock ID | Subsidiaries | Coverage |
|--------|----------|-------------|----------|
| 台積電 | 2330 | 4 (南京廠, 美國廠, 世界先進, SSMC) | Semiconductor |
| 鴻海 | 2317 | 4 (FII, 鴻騰, 夏普, 樺漢) | Electronics/EMS |
| 富邦金 | 2881 | 4 (人壽, 北富銀, 證券, 產險) | Financial |
| 台塑 | 1301 | 3 (南亞, 台塑石化, 台化) | Petrochemical |
| 台泥 | 1101 | 3 (台泥國際, 和平電廠, 達和環保) | Cement/Energy |

**Data quality**: All entries have `holding`, `revenue_contrib`, `business` (Chinese description), and `relation` fields. Data is sourced from annual reports (年報).

**Gap analysis for v1**:
- ✅ Parent-subsidiary relationships: Complete for 5 parents
- ✅ Revenue contribution data: Present for all subsidiaries
- ✅ Business descriptions: Present for all subsidiaries
- ❌ Customer-supplier relationships: Not in YAML (would need manual curation)
- ❌ Price data integration: Not in YAML (would be fetched via FinMind at runtime)
- ❌ Cross-holdings / ecosystem links between the 5 parents: Not modeled

**Verdict**: Data is sufficient for a **parent-subsidiary card view** (the "ecosystem" is the corporate group). Customer-supplier relationships would require 4-6h of additional research and are NOT needed for v1.

### 1.2 Component Reuse

**Existing components that can be reused**:

| Component | Location | Reuse for C203 |
|-----------|----------|---------------|
| `_subsidiary_card()` | `_router_base.py:269` | ✅ Direct reuse — renders name, holding %, revenue %, business description |
| `_info_card()` | `_router_base.py:225` | ✅ For ecosystem summary cards |
| `_section_title()` | `_router_base.py:70` | ✅ For section headers |
| `_白话_card()` | `_router_base.py:183` | ✅ For metric display cards |
| `group_structure.py` | `pages/group_structure.py` | ✅ Reference implementation — already renders group structure with `_subsidiary_card()` |
| `FinMindClient` | `src/data/finmind_client.py` | ✅ For live price data enrichment |

**New components needed**:
- `ecosystem_service.py` — Load `group_structures.yaml`, enrich with FinMind price data, provide query interface
- `ecosystem_cards.py` — Page module with card grid layout + stock selector + detail view

**Neither file exists yet** (confirmed: zero matches for `ecosystem_service` or `ecosystem_cards` in codebase).

### 1.3 Estimated Effort

| Component | Description | Hours |
|-----------|-------------|-------|
| `ecosystem_service.py` | Load YAML, enrich with FinMind price data, query interface | 3-4 |
| `ecosystem_cards.py` | Page module: card grid, selector, detail view | 4-5 |
| Data expansion | Expand from 5 to 8-10 parent companies (add 台達, 聯發科, 廣達) | 3-4 |
| i18n keys | ~25 keys under `ecosystem.*` namespace | 0.5-1 |
| Testing | Card rendering, data loading, edge cases | 1-2 |
| **Total** | | **11.5-16** |

**Risk-adjusted estimate**: 12-14h (using existing `_subsidiary_card()` significantly reduces UI effort).

### 1.4 Feasibility Verdict

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Technical | ✅ High | New service + page, but follows existing patterns exactly. No new visualization types. |
| Data | ✅ Medium-High | 5 parents ready. Expanding to 8-10 requires ~3-4h research. Parent-subsidiary is the core — no customer-supplier needed for v1. |
| UI | ✅ High | `_subsidiary_card()` already exists and is proven in `group_structure.py` + `market_event_case_study.py`. |
| Risk | 🟢 Low | Purely additive. No modifications to existing services or pages. |

**Recommendation**: ✅ **FEASIBLE for Sprint 26**. The feature is de-risked by existing `_subsidiary_card()` component. Scope should be: 5-8 parent companies (not 15-20), parent-subsidiary only (no customer-supplier), card-based layout (no network graph).

---

## 2. Design Debt Assessment (Top 5 from Round 7)

### 2.1 Status Check

| # | Issue | File | Status | Effort | Impact |
|---|-------|------|--------|--------|--------|
| **D-073** | `#5D6D7E` → `#7F8C8D` in `_info_card()` | `_router_base.py` | ✅ **ALREADY FIXED** | 5 min | GLOBAL |
| **D-071** | Replace Set3 palette in pie charts | `chart.py` / `chart_stock_financial.py` | ✅ **ALREADY FIXED** | 30 min | GLOBAL |
| **D-084** | Replace `st.bar_chart` with Plotly | `group_structure.py:258` | ✅ **ALREADY FIXED** | 30 min | Single page |
| **D-005** | Fix `_section_title()` emoji logic | `_router_base.py:70-79` | 🟡 **PARTIALLY FIXED** | 15 min | GLOBAL |
| **D-074** | Standardize `#F8F9FA` background | `_router_base.py:185` | 🟡 **PARTIALLY FIXED** | 10 min | GLOBAL |

### 2.2 Detailed Analysis

**D-073 — FIXED** ✅
The `_info_card()` function at line 227 already uses `#F8F9FA` background and `#7F8C8D` text color. No `#5D6D7E` found in `_router_base.py`. This was fixed during Sprint 25 pre-sprint cleanup.

**D-071 — FIXED** ✅
The `chart.py` module is now a re-export shim. The actual chart functions in `chart_stock_financial.py` use the design system palette (`#3498DB`, `#27AE60`, `#E74C3C`, `#2C3E50`, `#7F8C8D`, `#ECF0F1`) — no Set3 references found anywhere in chart files.

**D-084 — FIXED** ✅
`group_structure.py:258` uses `px.bar()` (Plotly Express) with comment "replaces st.bar_chart for design consistency". No `st.bar_chart` calls remain in the file.

**D-005 — PARTIALLY FIXED** 🟡
The `_section_title()` function (line 70-79) has emoji logic that prepends `📊` to Chinese titles. The logic checks `code >= 0x2300` (CJK symbols range) — this works for most Chinese titles but has edge cases:
- Titles starting with emoji (e.g., `📈 營收趨勢`) would get double-emoji (`📊 📈 營收趨勢`)
- The fix at line 76 checks `first_char.isalpha() and first_char.isascii()` for Latin titles, but doesn't check if the title already starts with an emoji

**Remaining work**: Add emoji-prefix check before prepending `📊`. ~15 min.

**D-074 — PARTIALLY FIXED** 🟡
The `_白话_card()` function (line 185) uses `background:white` instead of `#F8F9FA`. This is actually **intentional** — the white background with `#ECF0F1` border creates a cleaner card style. However, `_info_card()` uses `#F8F9FA` background. The inconsistency is:
- `_info_card()`: `#F8F9FA` background, `#3498DB` left border
- `_白话_card()`: `white` background, `#ECF0F1` border, `#3498DB` left border
- `_summary_card()`: `#FFF8F0` background (warm white)

**Remaining work**: Decide on standard. Either all cards use `#F8F9FA` or each card type has its own semantic background. ~10 min to standardize.

### 2.3 Design Debt Summary

**Effective remaining effort for top 5**: ~25 min (D-005 + D-074 only; D-073, D-071, D-084 already fixed).

**Additional design debt to track**:
- D-069+D-070: Chart theme colors — `chart_stock_financial.py` already has `_get_chart_colors()` with theme-aware colors. These may already be resolved.
- D-075 through D-083: Page-specific color violations (9 issues, 2-3h batch)

---

## 3. New Architectural Concerns for Sprint 26

### 3.1 Pre-existing Concerns (Carried Forward)

From `review_i18n_refactoring.md`:

1. **Service layer importing Streamlit** (`quiz_service.py`) — Pre-existing, not blocking
2. **Service layer directly using FinMindClient** — Pre-existing pattern, not blocking
3. **View layer using `st.cache_data`** (`category_browser.py`, `router.py`) — Pre-existing, not blocking

None of these are new. They are structural issues that should be addressed in a dedicated refactoring sprint (not Sprint 26).

### 3.2 Sprint 26-Specific Concerns

**C203: Service Layer Boundary**
- `ecosystem_service.py` should NOT import Streamlit (follow `story_arc_detector.py` pattern)
- Should receive pre-fetched FinMind data as arguments, not call `FinMindClient` directly
- Should return i18n keys, not display text

**C203: Data Layer Expansion**
- Expanding `group_structures.yaml` from 5 to 8-10 companies requires careful data validation
- Recommend: add schema validation in `ecosystem_service.py` to catch missing fields early

**D-126: Dark/Light Theme (if approved)**
- This is the highest-risk item in Sprint 26 candidate list
- Would require touching ALL chart files (`chart_stock.py`, `chart_stock_financial.py`, `chart_stock_health.py`, `chart_stock_valuation.py`, `chart_market.py`)
- Would require CSS variable system for all card components
- 8-12h estimate is realistic but could expand
- **Recommendation**: Defer to Sprint 27 unless Daniel explicitly prioritizes it

**D-127: `_infocard` Component (if approved)**
- New shared component — follows existing pattern (`_info_card`, `_白话_card`, `_summary_card`)
- 6-9h estimate is reasonable
- Risk: scope creep (responsive layout, animation, variants)
- **Recommendation**: Include as COULD, scope tightly to card grid only

### 3.3 Architecture Health Trajectory

**Current state**: B+ (stable, no new critical debt from Sprint 25)

**Sprint 26 impact prediction**:
- C203: Neutral (additive, follows existing patterns)
- Top 5 fixes: Positive (resolves 2 remaining items)
- D-126: Risky (touches many files, could introduce regressions)
- D-127: Neutral (additive, well-scoped)

---

## 4. Recommended Sprint 26 Prioritization

### MUST (Core — Sprint cannot ship without these)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| **C203 Company Ecosystem Cards v1** | 12-14h | Highest value feature. Data ready (5 parents, expandable to 8). `_subsidiary_card()` already exists. Aligns with historian positioning. |
| **D-005 emoji fix + D-074 background standardization** | 25 min | Trivial fixes. Global impact. Should be done on Day 1. |

**MUST Total**: 12.5-14.5h

### SHOULD (High value — include if time permits)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| **D-069+D-070 chart theme verification** | 15 min | Verify chart colors are already fixed (likely done in Sprint 25). Quick confirmation. |
| **D-075 through D-083 batch fix** | 2-3h | 9 page-specific color violations. Batch as single cleanup task. |

**SHOULD Total**: 2.5-3.5h

### COULD (Nice to have — defer to Sprint 27)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| **D-126 Dark/Light Theme** | 8-12h | Pending Daniel. High risk, touches many files. Defer to dedicated sprint. |
| **D-127 `_infocard` component** | 6-9h | Pending Daniel. New component, needs design spec. Defer to Sprint 27. |

### Sprint 26 Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| Week 1 | Pre-sprint fixes (D-005, D-074) + C203 `ecosystem_service.py` | Fixes applied, service layer complete |
| Week 2 | C203 `ecosystem_cards.py` + data expansion to 8 parents | Page module complete, data expanded |
| Week 3 | C203 testing + D-075-D-083 batch fix | Ecosystem cards tested, color violations fixed |
| Week 4 | Buffer + D-126/D-127 (if Daniel approves) | Regression testing, theme work |

---

## 5. Summary

| Feature | Status | Ready? | Effort | Risk | Recommendation |
|---------|--------|--------|--------|------|----------------|
| **C203** Ecosystem Cards v1 | Data ready, components exist | ✅ Ready (pending Daniel) | 12-14h | Low | **MUST** |
| **D-005** Emoji fix | Code reviewed | ✅ Ready | 15 min | None | **MUST** |
| **D-074** Background standardization | Code reviewed | ✅ Ready | 10 min | None | **MUST** |
| **D-073/D-071/D-084** Top 3 fixes | ✅ Already fixed | ✅ Done | 0 | None | ✅ Complete |
| **D-075-D-083** Color violations | Identified | ✅ Ready | 2-3h | Low | **SHOULD** |
| **D-126** Dark/Light Theme | Pending Daniel | ⚠️ Pending | 8-12h | High | **COULD** (defer) |
| **D-127** `_infocard` component | Pending Daniel | ⚠️ Pending | 6-9h | Medium | **COULD** (defer) |

**Bottom line**: Sprint 26 has a clear MUST path (C203 + 2 micro-fixes = 12.5-14.5h). The top 5 design debt items from Round 7 are effectively resolved (3 already fixed, 2 remaining = 25 min). C203 is the highest-value feature and is technically de-risked by existing `_subsidiary_card()` component. The main decision point is whether Daniel approves D-126 and/or D-127 — both are significant efforts that would consume the entire sprint if combined with C203.

**Recommended scenario**: C203 (12-14h) + D-005/D-074 (25 min) + D-075-D-083 batch (2-3h) = **14.5-17.5h total**. This leaves buffer for D-126/D-127 if Daniel approves one of them.

**Critical path**: Daniel's decision on C203 scope (approve 5-8 parent companies, parent-subsidiary only) → Sprint 26 planning finalization → Implementation.

---

*Created: 2026-06-17 by System Architect*
*References: docs/state/handoff.md, docs/architecture/discuss_r50_architect.md, docs/architecture/review_i18n_refactoring.md, src/data/group_structures.yaml, src/pages/_router_base.py, src/pages/group_structure.py, src/services/chart.py, src/services/chart_stock_financial.py*
*Verification: 658 tests passing. 3 of 5 top design debt items already fixed. No ecosystem_service.py or ecosystem_cards.py exists yet. group_structures.yaml covers 5 parents, 18 subsidiaries.*
