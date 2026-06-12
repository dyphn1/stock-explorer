# Stock Explorer — Architecture Review Round 18

> **Date**: 2026-06-12
> **Sprint**: Post-Sprint 6 → Pre-Sprint 7
> **Reviewer**: System Architect

---

## 1. `_sections.py` Status — D37 RESOLVED ✅

**D37 is fully resolved.** The `_sections.py` monolith (918 lines at Round 17) has been split into a proper sub-module directory:

| File | Lines | Responsibility |
|------|-------|----------------|
| `_sections/__init__.py` | 49 | Public API / re-exports |
| `_sections/_summary.py` | 323 | Header, one-liner, key metrics, footer |
| `_sections/_financial.py` | 244 | Dividend, revenue breakdown, revenue trend, valuation |
| `_sections/_health.py` | 88 | Health scores, risk analysis |
| `_sections/_detail.py` | 106 | News, detail sections |
| `_sections/_story.py` | 196 | Story card, compare stories, share |
| `_sections.py` | 57 | Thin orchestrator (imports + delegates) |

**Total**: 1,063 lines across 7 files (vs. 918 monolith). Net +145 lines from import headers, but each file is now independently maintainable. The split follows the D37 recommendation almost exactly (core→summary, analysis→health, detail→financial/detail, discovery→story).

**Verdict**: Clean resolution. `_sections.py` at 57 lines is now a thin orchestrator.

---

## 2. New Debt from Sprint 6 Features

Sprint 6 delivered: C83 (Investment Memo), C85 (Financial Wellness), C02 (Notification Center), C43 (Stock Screener), C45 (Expert Analysis).

### New Debt Items

#### D-048: `financial_wellness.py` — 84 `st.markdown` calls, heavy inline HTML
- **Severity**: Medium
- **Description**: `financial_wellness.py` has **84 `st.markdown` calls** — the highest of any page. Lines 117-131 contain inline HTML with hardcoded CSS (`background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid...`) for score display cards. This is the same anti-pattern as D3 (inline HTML duplication). The page also uses `st.markdown("")` as vertical spacing 8+ times.
- **Impact**: Score cards cannot be reused. CSS is duplicated if another page needs similar card styling.
- **Recommended Action**: Use `_info_card()` / `_summary_card()` from `_router_base.py` for score display. Replace `st.markdown("")` spacing with `st.write("")` or layout spacing.

#### D-049: `notification_center.py` — 47 `st.markdown` calls, presentation-layer data helpers
- **Severity**: Medium
- **Description**: `notification_center.py` defines two presentation helper functions at module level: `_severity_badge()` (lines 30-37) and `_event_type_label()` (lines 40-50). These are pure presentation functions living in a page file. The page also has 47 `st.markdown` calls including `st.markdown("")` used as vertical spacing.
- **Impact**: If another page needs severity badges or event type labels, this code cannot be reused.
- **Recommended Action**: Move `_severity_badge()` and `_event_type_label()` to `ui_components.py` (D3). Replace spacing `st.markdown("")` calls with `st.write("")`.

#### D-050: `investment_memo.py` — 35 `st.markdown` calls, minor inline HTML
- **Severity**: Low
- **Description**: `investment_memo.py` has 35 `st.markdown` calls. Most are simple headers/dividers (`st.markdown("## ...")`, `st.markdown("---\n")`). No complex inline HTML detected in first 50 lines. Uses `_info_card()` and `_section_title()` properly.
- **Impact**: Low. The page follows the established pattern. `st.markdown("---\n")` dividers are cosmetic.
- **Recommended Action**: Minor cleanup — replace `st.markdown("---\n")` with `st.divider()` for consistency.

#### D-051: `notification_service.py` — reads YAML on every call (same pattern as D9/D10)
- **Severity**: Medium
- **Description**: `notification_service.py` (188 lines) calls `_load_notifications()` (file read + YAML parse + file lock) for every operation. No in-memory caching. Same anti-pattern as D9 (watchlist) and D10 (events.yaml).
- **Impact**: Performance degradation as notification volume grows. File lock contention if multiple operations fire in quick succession.
- **Recommended Action**: Add session-level cache or in-memory store invalidated on writes. Same pattern as D9/D10 fix.

#### D-052: `financial_wellness_service.py` — hardcoded quiz data in Python (D6 pattern)
- **Severity**: Medium
- **Description**: `financial_wellness_service.py` (253 lines) contains hardcoded quiz questions, scoring rules, and interpretation thresholds directly in Python. This is the same anti-pattern as D6 (hardcoded data in Python modules).
- **Impact**: Adding/editing questions requires code changes. Non-technical content editors cannot modify quiz content.
- **Recommended Action**: Migrate quiz questions to `src/data/quiz_questions.yaml` as part of D6 YAML migration.

#### D-053: `investment_memo_service.py` — thin service, good pattern
- **Severity**: None — positive finding
- **Description**: `investment_memo_service.py` (94 lines) is clean: pure functions, no Streamlit imports, no API calls. `validate_memo_input()` and `format_memo_summary()` are properly isolated.
- **Verdict**: Model service layer implementation. No debt.

#### D-054: `stock_screener_service.py` — 232 lines, clean service boundary
- **Severity**: Low
- **Description**: `stock_screener_service.py` (232 lines) has no Streamlit imports and clean function boundaries. However, it may contain hardcoded screening criteria (needs monitoring for D6 pattern).
- **Verdict**: Acceptable for now. Monitor for hardcoded data growth.

---

## 3. Top 5 Priority Debt Items for Sprint 7

| Priority | ID | Item | Effort | Rationale |
|----------|-----|------|--------|-----------|
| **P0** | D-043 | `_sections.py` calls non-existent `get_roe_analyzer()` / `get_pbr_analyzer()` | 0.25h | **Runtime NameError crash** on business card page. Must fix immediately. |
| **P1** | D-042 | `_sections.py` split into sub-modules | — | ✅ **RESOLVED** in Sprint 6. Remove from backlog. |
| **P1** | D-046 | `_render_share_section()` uses `st.html()` with fragile JS element IDs | 1h | Feature is non-functional. Copy-to-clipboard broken. Fix before user testing. |
| **P1** | D-048 | `financial_wellness.py` — 84 `st.markdown` calls, inline HTML duplication | 2-3h | Highest `st.markdown` count of any page. Inline CSS duplicates D3 pattern. |
| **P2** | D-044 | `sector_heatmap.py` — no service-layer abstraction | 2-3h | Violates 4-layer architecture. Needs `market_data.py` extraction. |
| **P2** | D-049 | `notification_center.py` — presentation helpers in page file | 1-2h | `_severity_badge()` and `_event_type_label()` should be in `ui_components.py`. |

**Recommended Sprint 7 Sequence**:
1. **D-043** (P0 bug fix) — immediate, 15 minutes
2. **D-046** (share section fix) — 1h, before user testing
3. **C84** — Sprint 7 feature (per plan)
4. **D-048** + **D-049** — debt cleanup alongside C84
5. **D-044** — market data service extraction (if time permits)

---

## 4. P0 Bugs Found

### D-043: `_render_key_metrics()` calls non-existent functions — 🔴 P0
- **File**: `src/pages/business_card/_sections/_financial.py` (was `_sections.py` lines 437/445)
- **Error**: `get_roe_analyzer(roe)` and `get_pbr_analyzer(pbr)` do not exist
- **Correct functions**: `get_roe_analogy()` and `get_pbr_analogy()` (already imported)
- **Impact**: Runtime `NameError` crash when rendering ROE/PBR fallback columns on business card page
- **Fix**: Rename function calls on the affected lines
- **Status**: Still open — not yet fixed as of this review

### D-047: `_section_title()` inverted logic — 🟢 Low (pre-existing)
- **File**: `src/pages/_router_base.py` line 70
- **Error**: `if not title:` should be `if title:`
- **Impact**: Low — function still renders something for all inputs
- **Status**: Pre-existing, not introduced in Sprint 6

---

## 5. Architecture Health Summary

### Positive Findings
- **D37 resolved**: `_sections.py` properly split into 6 focused sub-modules
- **Service layer growth**: 4 new services added in Sprint 6 (`notification_service`, `financial_wellness_service`, `investment_memo_service`, `stock_screener_service`)
- **Clean service boundaries**: `investment_memo_service.py` (94 lines) and `notification_service.py` (188 lines) have zero Streamlit imports
- **Page-service separation**: All 3 new pages (`investment_memo.py`, `financial_wellness.py`, `notification_center.py`) import from dedicated services rather than inline logic

### Concerns
- **`st.markdown` proliferation**: `financial_wellness.py` (84 calls) and `notification_center.py` (47 calls) are heavy users
- **Inline HTML creeping back**: `financial_wellness.py` has hardcoded CSS in `st.markdown` calls
- **YAML-on-every-read pattern repeating**: `notification_service.py` repeats D9/D10 anti-pattern
- **D-043 P0 bug still open**: Runtime crash on business card page

### Debt Register Update
- **Total items**: 49 (was 43, +6 new)
- **Resolved**: D37 (now 8 total resolved: D1, D2, D16, D17, D20, D24, D26, D37)
- **New**: D-048, D-049, D-050, D-051, D-052, D-054

---

*Next review: Sprint 7 mid-point (after C84 + debt cleanup)*
