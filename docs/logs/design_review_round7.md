# Design Compliance Review — Round 7 (2026-06-12)

> **Reviewer**: PM (coordinating Design Reviewer analysis)
> **Date**: 2026-06-12
> **Scope**: All page files, chart.py, main.py, _router_base.py against design_system.md
> **Previous rounds**: R2–R6 found 81+ issues, overall grade improved from D+ to C

---

## Executive Summary

Round 6 confirmed DR-01 fully resolved (no more `#F39C12` or `linear-gradient` in src/). Business card restored to 462 lines. Overall grade: C.

This round verifies Round 6 fixes and searches for remaining/new issues.

---

## Verification of Round 6 Issues

| Issue | Description | R6 Status | R7 Verification |
|-------|-------------|-----------|-----------------|
| D-002/D-029 | business_card.py truncated | ✅ Fixed | ✅ **CONFIRMED** — 462 lines, all sections render |
| D-059 | `_info_card()` border `#F39C12` | ✅ Fixed | ✅ **CONFIRMED** — `_router_base.py:145` uses `#3498DB` |
| D-012 | `@st.cache_data` in peer_comparison.py | ✅ Fixed | ✅ **CONFIRMED** — 0 occurrences in src/ |
| D-016 | `@st.cache_data` in etf_browser.py | ✅ Fixed | ✅ **CONFIRMED** — 0 occurrences in src/ |
| DR-01 | All `#F39C12` + gradients | ✅ Fixed | ✅ **CONFIRMED** — `rg '#F39C12'` and `rg 'linear-gradient'` both return 0 results in src/ |

---

## Remaining Issues from Round 6 (Still Open)

### Color System Violations

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-063 | `business_card.py` | 153 | `#F0F7FF` | Not in palette | Company facts card background |
| D-064 | `business_card.py` | 359 | `#BDC3C7` | Not in palette | Table header border |
| D-065 | `business_card.py` | 414,449 | `#5D6D7E` | `#7F8C8D` | Revenue item + news summary text |
| D-066 | `business_card.py` | 450 | `#95A5A6` | Not in palette | News source/date text |
| D-067 | `business_card.py` | 458 | `#F9E79F`/`#7D6608` | Not in palette | Disclaimer section |
| D-068 | `chart.py` | 30 | `#555555` | `#7F8C8D` | Axis label text |
| D-069 | `chart.py` | 31 | `#333333` | `#2C3E50` | Chart titles |
| D-070 | `chart.py` | 96 | `px.colors.qualitative.Set3` | Explicit palette | Pie chart arbitrary colors |
| D-071 | `_router_base.py` | 147 | `#5D6D7E` | `#7F8C8D` | `_info_card()` content |
| — | `group_structure.py` | 245 | `#ECF0F1` | Not in palette | Subsidiary card border |
| — | `main.py` | 50,54 | `#F9E79F`/`#7D6608` | Not in palette | Disclaimer CSS |
| — | `main.py` | 94,266 | `#95A5A6` | Not in palette | Welcome page text |
| — | `etf_detail.py` | 307 | `#F9E79F`/`#7D6608` | Not in palette | Disclaimer section |

### Component Consistency Issues

| # | File | Line | Issue |
|---|------|------|-------|
| D-005 | `_router_base.py` | 129-130 | `_section_title()` auto-prepends 📊 — emoji prefix conflict |
| D-009 | `financial_health.py` | 188-196 | Custom health card doesn't use shared components |
| D-011 | `peer_comparison.py` | 92 | Uses `st.metric()` instead of `_白话_card()` |
| D-025 | `watchlist_page.py` | 204-224 | Raw flexbox HTML card instead of `_白话_card()` |
| D-041 | `category_browser.py` | 170-181 | Stock cards use raw HTML instead of `_白话_card()` |
| D-042 | `etf_browser.py` | 302-321 | ETF category cards use raw HTML instead of `_白话_card()` |
| D-044 | `etf_detail.py` | 183-188 | Dividend explanation raw HTML card |
| D-045 | `etf_detail.py` | 250-256 | Institution explanation raw HTML card |
| D-047 | `business_card.py` | 409 | Revenue breakdown uses `box-shadow` not in design system |
| D-048 | `category_browser.py` | 170-181 | Industry stock cards use raw HTML |
| D-051 | `group_structure.py` | 245 | `border-radius:16px` — design system specifies `12px` |
| D-052 | `group_structure.py` | 283 | Uses `st.bar_chart` instead of Plotly |

### PPT Style Violations

| # | File | Line | Issue |
|---|------|------|-------|
| D-003 | `operation_checkup.py` | 62-70 | Trend messages exceed 200-char limit |
| D-008 | `financial_health.py` | — | Only 1 chart for 4 sections |
| D-010 | `peer_comparison.py` | 333-367 | Metric analysis text could reach 400+ chars |
| D-036 | `financial_health.py` | 70-73 | Funnel analysis text ~280 chars |
| D-037 | `financial_health.py` | 234-244 | Cash flow text ~500 chars |
| D-038 | `group_structure.py` | 326-330 | Strategy text exceeds limit |
| D-039 | `watchlist_page.py` | 157-226 | Page is table/list oriented, no chart |
| D-049 | `category_browser.py` | 38-49 | 3 unrelated sections on one page |

### Zone Separation Violations

| # | File | Line | Issue |
|---|------|------|-------|
| D-001 | `business_card.py` | 56-72 | Watchlist buttons in navbar (Zone A) |
| D-040 | `business_card.py` | 95-128 | Watchlist popover UI in Zone A |

### Responsive Design Issues

| # | File | Line | Issue |
|---|------|------|-------|
| D-015 | `etf_browser.py` | 165, 437 | 6-column layout breaks on narrow screens |
| D-019 | `category_browser.py` | 105 | 6-column layout breaks on narrow screens |

### Accessibility Issues

| # | File | Line | Issue |
|---|------|------|-------|
| D-020 | `category_browser.py` | 141 | Hidden label on industry radio |
| D-022 | `event_dashboard.py` | 21-26 | Severity badges use emoji without text alternatives |

---

## NEW Issues Found in Round 7

### 🟡 NEW-D-073: `business_card.py` company facts card uses non-palette background

**File**: `business_card.py:153`
**Issue**: `background:#F0F7FF` — light blue not in design system palette
**Fix**: Replace with `#F8F9FA` (card background) or `#EBF5FB` (light blue from design system)
**Effort**: 1 minute

### 🟡 NEW-D-074: `business_card.py` disclaimer section uses non-palette colors

**File**: `business_card.py:458`
**Issue**: `background:#FEF9E7;border:1px solid #F9E79F;color:#7D6608` — these are warning colors but the design system specifies `#FEF9E7` for warning background (this is actually correct per design system). However, `#7D6608` for text and `#F9E79F` for border are not in the palette.
**Fix**: Use `#FEF9E7` background + `#3498DB` border + `#2C3E50` text (standard info card pattern)
**Effort**: 1 minute

### 🟢 NEW-D-075: `main.py` disclaimer uses non-palette colors

**File**: `main.py:49-56`
**Issue**: `#F9E79F` border, `#7D6608` text — not in palette
**Fix**: Use standard card styling
**Effort**: 1 minute

### 🟢 NEW-D-076: `etf_detail.py` disclaimer uses non-palette colors

**File**: `etf_detail.py:307`
**Issue**: Same `#F9E79F`/`#7D6608` pattern
**Fix**: Use standard card styling
**Effort**: 1 minute

---

## Page Grades

| Page | Grade | Change | Notes |
|------|-------|--------|-------|
| business_card.py | B | ← No change | 462 lines, all services called, minor color issues |
| chart.py | B+ | ← No change | Major colors correct, 3 minor violations |
| _router_base.py | B+ | ← No change | D-059 border fix confirmed |
| event_dashboard.py | A- | ← No change | Best-graded page |
| financial_health.py | C+ | ← No change | DR-03 fix integrated, text still heavy |
| operation_checkup.py | C | ← No change | Text violations remain |
| peer_comparison.py | C | ← No change | Component inconsistency |
| watchlist_page.py | C- | ← No change | Multiple component issues |
| etf_browser.py | C- | ← No change | 6-column layout + component issues |
| etf_detail.py | C- | ← No change | Raw HTML cards |
| group_structure.py | D | ← No change | Structural issues remain |
| category_browser.py | D | ← No change | Structural issues remain |
| main.py | C | ← No change | Welcome page color issues |

---

## Top 5 Recommended Fixes

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 1 | D-005: Fix `_section_title()` emoji conflict | 15 min | Affects all pages |
| 2 | D-068+D-069: Fix chart.py theme colors (`#555555`→`#7F8C8D`, `#333333`→`#2C3E50`) | 15 min | Affects all charts globally |
| 3 | D-070: Replace Set3 palette in pie charts with explicit design system colors | 30 min | Affects all pie charts |
| 4 | D-063+D-064+D-065+D-066: Fix business_card.py non-palette colors | 10 min | Main page polish |
| 5 | D-071+D-072: Fix `_info_card()` content color `#5D6D7E`→`#7F8C8D` | 5 min | Affects all info cards |

---

## Overall Design Grade: C+

**Rationale**: Upgraded from C because:
- DR-01 fully resolved (no more orange/gradients in src/)
- Business card fully restored and functional
- Chart.py mostly compliant
- Event dashboard is best-in-class (A-)

**Blockers to B grade**:
- 13+ non-palette color instances across 6 files
- 12 component consistency issues
- 8 PPT style violations
- 2 zone separation issues
- 2 responsive design issues

---

*Last updated: 2026-06-12 by PM after Round 7 design review.*
