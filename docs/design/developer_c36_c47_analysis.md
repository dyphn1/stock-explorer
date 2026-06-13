# Developer Analysis: C36-C47 Feature Candidates — Implementation Cost & Risk Assessment

> **Date**: 2026-06-14
> **Author**: Developer (Round 19 Follow-up)
> **Purpose**: Validate effort estimates, identify dependencies, propose sprint groupings for 12 competitor-inspired features

---

## ⚠️ Critical Finding: Most C36-C47 Features Are Already Built

After thorough codebase review, **9 out of 12 features already have working implementations** in services and/or pages. The original competitor research (Round 8-9) identified these as gaps, but the team has been building them incrementally across Sprint 3-10. This dramatically changes the cost analysis.

### Codebase Evidence

| Feature | Service Layer | Page Layer | Status |
|---------|--------------|------------|--------|
| C36 Revenue Tree | ❌ Not built | ❌ Not built | **New** |
| C37 Key Takeaways | ✅ `key_takeaways.py` (232 lines) | ✅ `_render_takeaways()` wired in business card | **Shipped** |
| C38 Compare Stories | ✅ `compare_stories.py` (328 lines) | ✅ `_render_compare_stories()` in `_story.py` | **Shipped** |
| C39 What Changed | ✅ `delta_engine.py` (164 lines) | ✅ `_render_deltas()` in `_story.py` | **Shipped** |
| C40 Beginner/Expert | ⚠️ Partial — simple mode exists in `_main.py` `_render_simple_overview()` | ⚠️ No toggle UI yet | **Partial** |
| C41 Read Next | ⚠️ Service logic in `compare_stories.py` | ✅ `_render_read_next()` in `_story.py` | **Shipped** |
| C42 Stock Screener | ✅ `stock_screener_service.py` (232 lines) | ✅ `stock_screener.py` page (272 lines) | **Shipped** |
| C43 Snowflake Health | ✅ `health_scoring.py` (269 lines) + `chart.py` `create_health_snowflake()` | ✅ `_render_health()` in `_health.py` | **Shipped** |
| C44 Risk Analysis | ✅ `risk_analyzer.py` (567 lines) | ✅ `_render_risk()` in `_health.py` | **Shipped** |
| C45 Valuation Band | ✅ `chart.py` `create_valuation_band_chart()` | ✅ `_render_valuation()` in `_financial.py` | **Shipped** |
| C46 Moat Analysis | ❌ Not built | ❌ Not built | **New** |
| C47 Education Academy | ❌ Not built | ❌ Not built | **New** |

---

## 1. Revised Effort Estimates Table

### Already Shipped (Remaining Effort: QA/Polish Only)

| ID | Title | Original Est. | Revised Est. | Confidence | Notes |
|----|-------|-------------|-------------|------------|-------|
| C37 | Key Takeaways | 6-8h | **0-1h** | 🟢 High | Shipped. Minor: verify content QA gate |
| C38 | Compare Stories | 12-16h | **1-2h** | 🟢 High | Shipped. Minor: historian tone QA pass |
| C39 | What Changed | 8-10h | **0-1h** | 🟢 High | Shipped. Already wired in business card |
| C41 | Read Next | 6-8h | **0h** | 🟢 High | Shipped. Uses `compare_stories.py` + manual curation |
| C42 | Stock Screener | 16-24h | **2-4h** | 🟡 Medium | Shipped. R3 batch API dependency was risky; verify with real data |
| C43 | Snowflake Health | 12-16h | **1-2h** | 🟢 High | Shipped. Chart in `chart.py`, scoring in `health_scoring.py` |
| C44 | Risk Analysis | 10-14h | **1-2h** | 🟢 High | Shipped. 567-line `risk_analyzer.py` is comprehensive |
| C45 | Valuation Band | 8-10h | **0-1h** | 🟢 High | Shipped. `create_valuation_band_chart()` in `chart.py` |

### Partially Built (Needs Completion)

| ID | Title | Original Est. | Revised Est. | Confidence | Notes |
|----|-------|-------------|-------------|------------|-------|
| C40 | Beginner/Expert Mode | 10-14h | **6-10h** | 🟡 Medium | `_render_simple_overview()` exists but no session_state toggle. Need: navbar toggle, conditional section rendering across ALL business card sections, responsive show/hide logic, QA |

### New Builds (Full Effort Required)

| ID | Title | Original Est. | Revised Est. | Confidence | Notes |
|----|-------|-------------|-------------|------------|-------|
| C36 | Visual Revenue Tree | 10-14h | **12-16h** | 🟡 Medium | No existing implementation. Needs: Plotly treemap/sunburst in `chart.py`, revenue hierarchy data (FinMind provides segment data), manual curation for top 20, business card UI tab |
| C46 | Moat Analysis | 12-16h | **14-18h** | 🟡 Medium | Greenfield build. Needs: new `moat_analyzer.py` service (5 dimension scoring), moat data model (manual curation for top 20 — 40% content budget), UI section in business card, historian tone QA |
| C47 | Education Academy | 20-30h | **22-32h** | 🟡 Medium | Largest item. 40% content budget = 9-13h content creation. Needs: new `lesson_service.py`, lesson data model (10-15 lessons), new page `learning_academy.py`, quiz integration, progress tracking |

### Summary

| Category | Count | Total Revised Hours |
|----------|-------|-------------------|
| Already Shipped (QA only) | 8 | 6-15h |
| Partially Built | 1 | 6-10h |
| New Builds | 3 | 48-64h |
| **TOTAL** | **12** | **60-89h** |

---

## 2. Dependency Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEPENDENCY MAP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [INFRASTRUCTURE — Built during Sprint 11]                      │
│  D16: Split analogy_engine.py ───────────────────┐           │
│  D24: Extract business_card.py ──────┐            │           │
│  R3: Batch API utility ──────────────┼──────┐     │           │
│                                       │      │     │           │
│  [NEW SERVICES]                       │      │     │           │
│  C43 Health Scoring ◄─────────────────┼──────┤     │  (shared │
│  C44 Risk Analysis ◄─── reuses ───────┼──────┤     │  scoring │
│  scoring engine for ──────────────────┤      │     │  infra)  │
│  customer concentration              │      │     │           │
│                                       │      │     │           │
│  C46 Moat Analysis ◄─── reuses ───────┼──────┤     │           │
│  industry benchmark data from ────────┼──────┤     │           │
│  C43/C44 scoring framework           │      │     │           │
│                                       │      │     │           │
│  C42 Stock Screener ◄─────────────────┼──────┘     │  (needs  │
│  uses BatchAPI from R3 ──────────────┘            │  R3)     │
│                                                     │           │
│  C47 Education Academy ◄─── standalone, no deps ────┘           │
│  but can REUSE analogy_engine (after D16 split)                │
│                                                                 │
│  C36 Revenue Tree ◄─── standalone, new data pipeline needed    │
│  (FinMind segment data → manual curation → treemap)            │
│                                                                 │
│  C40 Beginner/Expert ◄─── depends on ALL existing sections     │
│  being stable first (worst coupling, best done last)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Dependencies

| Feature | Blocked By | Reason |
|---------|-----------|--------|
| C42 Stock Screener | R3 (Batch API) | Needs batch multi-stock fetching for 200+ stocks |
| C40 Beginner/Expert | ALL sections | Must wrap every existing section in conditional logic |
| C46 Moat Analysis | C43 scoring infra | Can reuse 5-dimension scoring framework from `health_scoring.py` |
| C47 Education Academy | D16 (analogy split) | Best to build after analogy_engine is split and stable |
| C36 Revenue Tree | FinMind data + curation | Needs segment-level revenue data that may not be available for all stocks |

---

## 3. Shared Infrastructure — Build Together

### Bundle 1: "Health & Moat Pack" (C43-polish + C44-polish + C46)
**Rationale**: C46 Moat Analysis directly reuses the 5-dimension scoring framework from `health_scoring.py`. Build them together to avoid rework.

Components:
- `moat_analyzer.py` (new service, ~80 lines following `health_scoring.py` pattern)
- UI section in `_health.py` or new `_moat.py`
- Content: ~20 curated moat analyses for top TW stocks (40% of effort)
- **Combined estimate**: 4-5h (polish C43/C44) + 14-18h (C46) = **18-23h**

### Bundle 2: "Education Double Feature" (C36 + C47)
**Rationale**: C36 Revenue Tree is a visual educational component that fits the "historian" positioning. C47 Education Academy is the structured learning path. Both need manual content curation and share the educational design language.

Components:
- C36: `chart.py` treemap + business card tab + curated data
- C47: `lesson_service.py` + `learning_academy.py` page + 10-15 lessons
- **Combined estimate**: 12-16h (C36) + 22-32h (C47) = **34-48h**

### Bundle 3: "Discovery & Accessibility" (C40 + C42-polish)
**Rationale**: C40 Beginner/Expert Mode and C42 Stock Screener both serve the "beginner onboarding" user journey. C40 wraps existing content; C42 provides entry point.

Components:
- C40: session_state toggle + conditional rendering
- C42: verify BatchAPI integration, polish UI
- **Combined estimate**: 6-10h (C40) + 2-4h (C42 polish) = **8-14h**

---

## 4. Recommended Sprint Groupings (Sprint 12-14)

### Sprint 12: "Health & Moat Pack" + Quick Wins
**Target: ~30-35h**

| Item | Hours | Type | Notes |
|------|-------|------|-------|
| C46 Moat Analysis | 14-18h | Feature | New `moat_analyzer.py` + UI + content |
| C43/C44 polish | 4-5h | QA | Historian tone QA gate + edge cases |
| C37/C39 polish | 1-2h | QA | Final content verification |
| C42 polish | 2-4h | QA | BatchAPI verification + UI polish |
| **TOTAL** | **21-29h** | | |

**Risk**: 🟡 Medium. C46 content creation (40% budget) is the main risk. Mitigation: start with template-based approach for non-top-20 stocks.

### Sprint 13: "Education Double Feature"
**Target: ~35-45h**

| Item | Hours | Type | Notes |
|------|-------|------|-------|
| C36 Visual Revenue Tree | 12-16h | Feature | New chart type + data pipeline |
| C47 Education Academy (Part 1) | 14-18h | Feature | `lesson_service.py` + first 7 lessons + page scaffold |
| C47 Content creation | 8-12h | Content | 40% of C47 effort |
| **TOTAL** | **34-46h** | | |

**Risk**: 🟡 Medium-High. C47 is the largest single item. Mitigation: split C47 into two sprints (Part 1: scaffold + 7 lessons; Part 2: remaining 8 lessons + quiz integration).

### Sprint 14: "Accessibility & Polish"
**Target: ~20-25h**

| Item | Hours | Type | Notes |
|------|-------|------|-------|
| C40 Beginner/Expert Mode | 6-10h | Feature | Toggle + conditional rendering |
| C47 Education Academy (Part 2) | 8-10h | Feature | Remaining lessons + quiz integration |
| C38/C41 polish | 1-2h | QA | Final historian tone pass |
| **TOTAL** | **15-22h** | | |

**Risk**: 🟢 Low. C40 is well-understood (simple mode already exists). C47 Part 2 is continuation.

### Alternative: Aggressive 2-Sprint Plan

If the team wants to move faster:

| Sprint | Items | Hours |
|--------|-------|-------|
| Sprint 12 | C46 + C36 + C43/44/37/39 polish | 30-40h |
| Sprint 13 | C47 (full) + C40 + C42 polish | 35-50h |

**Risk**: 🔴 High for Sprint 13. C47 alone is 22-32h. Not recommended unless content is pre-created.

---

## 5. Quick Wins vs. Major Investments

### Quick Wins (≤8h remaining effort)

| ID | Title | Remaining Effort | Value |
|----|-------|-----------------|-------|
| C37 | Key Takeaways | 0-1h | Already shipped — just verify |
| C39 | What Changed | 0-1h | Already shipped — just verify |
| C41 | Read Next | 0h | Already shipped |
| C43 | Snowflake Health | 1-2h | Already shipped — QA pass |
| C44 | Risk Analysis | 1-2h | Already shipped — QA pass |
| C45 | Valuation Band | 0-1h | Already shipped — just verify |
| C42 | Stock Screener | 2-4h | Already shipped — verify BatchAPI |

**Total quick wins**: 7 features, **4-11h** remaining effort

### Medium Investments (8-16h)

| ID | Title | Remaining Effort | Value |
|----|-------|-----------------|-------|
| C40 | Beginner/Expert Mode | 6-10h | High UX impact, enables progressive disclosure |
| C36 | Visual Revenue Tree | 12-16h | Unique visual differentiator |

### Major Investments (≥16h)

| ID | Title | Remaining Effort | Value |
|----|-------|-----------------|-------|
| C46 | Moat Analysis | 14-18h | Perfect "historian" differentiator, no TW competitor has this |
| C47 | Education Academy | 22-32h | Transforms product from lookup tool to learning platform |

---

## 6. Technical Risk Assessment

### 🔴 High Risk

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **C47 Content Creation Overrun** | 40% content budget may be insufficient. 10-15 lessons × 2-3h each = 20-45h of writing alone. | Start with 7 lessons. Use existing analogy_engine + company_facts as content source. Template-first approach. |
| **C36 Revenue Data Availability** | FinMind may not provide hierarchical segment data for all TW stocks. Manual curation for top 20 is feasible but scaling is hard. | Build for top 20 first. Fallback: show pie chart (existing) if no tree data. |
| **C40 Cross-Section Coupling** | Beginner/Expert toggle must wrap ALL business card sections. Missing one section = inconsistent UX. | Audit all `_render_*` functions. Use a decorator pattern: `@section_visibility("expert_only")`. |

### 🟡 Medium Risk

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **C46 Moat Data Curation** | Morningstar's moat analysis is their crown jewel. Our version needs to be equally insightful for TW stocks. | Use template: moat type + historical evidence + plain language. Start with 5 obvious moats (TSMC tech, Uni-President brand, etc.) |
| **C42 BatchAPI Reliability** | R3 BatchAPI may fail under load (200+ stocks). Handoff doc mentions fallback to top-50 sequential. | Implement fallback plan from R3 discussion. Test with real data in Sprint 11. |
| **C47 Quiz Integration** | `quiz_engine.py` and `comprehension_quiz_service.py` exist but may not integrate cleanly with lesson flow. | Design lesson-quiz interface early. Keep it simple: 1 quiz per lesson, 3 questions max. |

### 🟢 Low Risk

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **C37/C38/C39/C41/C43/C44/C45 Polish** | Already shipped. Only QA remaining. | Standard historian tone QA gate. |
| **C46 Scoring Framework** | Can directly reuse `health_scoring.py` patterns. | Follow same 0-100 scoring, 5-dimension pattern. |

---

## 7. Architecture Compliance Notes

All new features must follow the layered architecture:

| Feature | Data Layer | Service Layer | Page Layer |
|---------|-----------|--------------|------------|
| C36 Revenue Tree | `finmind_client.py` (existing) — segment data | `chart.py` → `create_revenue_treemap()` | `business_card/_sections/_revenue.py` → new tab |
| C46 Moat Analysis | Manual curation (JSON/YAML) | `moat_analyzer.py` (new) | `business_card/_sections/_moat.py` (new) |
| C47 Education Academy | Lesson data (JSON/YAML) | `lesson_service.py` (new) | `learning_academy.py` (new page) |
| C40 Beginner/Expert | N/A | N/A | `router.py` + all `_render_*` functions |

**Key architecture rules to enforce**:
- No Streamlit imports in service layer
- No direct API calls from page layer
- Error handling at every layer (return None, don't raise)
- No `st.cache_data` in page layer
- Session state managed at router/page layer only

---

## 8. Final Recommendations

### Priority Order (Vision Alignment > Retention Impact > Technical Risk)

1. **C46 Moat Analysis** — 🔴 Highest priority. Perfect "historian" differentiator. No TW competitor has this. Morningstar proves demand. 14-18h.
2. **C36 Visual Revenue Tree** — 🟡 High priority. Extends existing revenue visualization. Public.com/Koyfin prove demand. 12-16h.
3. **C47 Education Academy** — 🟡 High priority but split across sprints. Transforms product positioning. 22-32h total.
4. **C40 Beginner/Expert Mode** — 🟡 Medium priority. Enables progressive disclosure. 6-10h.
5. **C42/43/44 Polish** — 🟢 Low priority. Already shipped, just verify.

### Sprint Plan Summary

| Sprint | Focus | Items | Est. Hours |
|--------|-------|-------|-----------|
| Sprint 12 | Health & Moat | C46 + polish C43/44/37/39 + C42 verify | 25-35h |
| Sprint 13 | Education I | C36 + C47 Part 1 (scaffold + 7 lessons) | 30-40h |
| Sprint 14 | Education II + Accessibility | C47 Part 2 + C40 Beginner/Expert | 20-28h |

**Total remaining effort for C36-C47: ~75-103h across 3 sprints**

---

*Developer analysis complete. All estimates include architecture layer separation, testing, and QA time. Confidence levels reflect codebase maturity and data availability uncertainty.*
