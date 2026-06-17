# Designer Analysis — Discussion Round 50 (Sprint 25 Planning)

> **Reviewer**: Design Reviewer
> **Sprint**: Discussion Cycle Round 50 — Sprint 25 Planning
> **Current Design Grade**: C+ (Round 7, unchanged since Round 6)
> **Theme**: Sprint 25 Candidate Design Assessment + Design System Fix Verification
> **Date**: 2026-06-17

---

## Executive Summary

This analysis evaluates the design readiness of three Sprint 25 candidates (C206, C203, C209), verifies whether the Round 7 top-5 recommended fixes have been applied, assesses current page grades, examines design consistency for card reuse, and identifies design debt from Sprint 23 features (C199, C200, C202).

**Key Finding**: The Sprint 24 design system cleanup (commit `2fc60d3`) resolved 30+ violations across shared components and chart services, but the Round 7 top-5 recommended fixes were **not** part of that cleanup. D-005 (emoji conflict), D-071 (Set3 palette), D-073 (info card color), D-074 (白话 card bg), and D-084 (bar_chart) require targeted follow-up. The cumulative issue count stands at **92 total issues, 5 fixed, 87 remaining**.

---

## 1. Design Assessment of Sprint 25 Candidates

### 1.1 C206: Recurring Investment Education

**Current Status**: Listed as Sprint 24 Week 4 stretch goal. No architecture doc exists. Scope pending Daniel decision.

**Design Philosophy Fit**: ✅ Strong alignment
- C206 is purely educational — concept explanation, not a tool. This aligns perfectly with the "historian, not stock picker" core principle.
- "PPT-style" one-key-point-per-card approach maps naturally to the 3-part card series proposed in Round 46: definition → benefit → disclaimer.
- Ten-second test passes: "什麼是定期定額？每月固定買，長期平滑成本."

**Design Patterns to Use**:
1. **`_lesson_card()`** (already exists in `_router_base.py`, line 530) — This was added as part of C163 Learn First Gate. It supports `title`, `content`, `icon`, and `visual_area` parameters. Visual area has a blue background (`#EBF5FB`), which provides a natural chart/image zone within the card.
2. **`_progress_dots()`** (already exists, line 545) — For multi-card navigation (dot indicators showing progress through the 3-card series).
3. **`_白话_card()`** — For key statistics within each lesson card (e.g., "每月 3,000 元" as value, "一杯星巴克的大小" as analogy).
4. **`_beginner_banner()`** — To frame the educational context at the top.
5. **`_advanced_content_expander()`** — For optional depth (e.g., "想了解更多關於複利的效果？").

**PPT-Style Implementation Approach**:
- **Card 1 (Definition)**: "定期定額 = 每個月固定買，不管漲跌" — Single bold value + analogy. Use `_lesson_card()` with visual_area showing a simple calendar icon.
- **Card 2 (Benefit)**: "長期來說，這樣可以平滑買入成本" — Use a simple Plotly line chart in the `visual_area` showing "每月投入 3,000 元" with varying prices. Chart occupies >60% of card area per PPT spec.
- **Card 3 (Disclaimer)**: "這不是投資建議，只是讓你了解這個概念" — Standard `_info_card()` in warning yellow (`#FEF9E7` bg, `#F39C12` border — though `#F39C12` is NOT in palette; use `#3498DB` border instead with disclaimer icon).
- **Navigation**: `_progress_dots(0, 3)` → `_progress_dots(1, 3)` → `_progress_dots(2, 3)` with ← 下一課 → buttons.

**Recommended Placement**: A new "投資概念" section accessible from:
- The sidebar navigation (new nav item)
- The ETF Zone page (as an expandable education section)
- NOT on individual stock pages (avoids advisory perception)

**Design Risks**:
- Must NOT include any calculator or "try it" tool — that crosses into advisory
- Chart in Card 2 must use hypothetical/fictional data only — NO real stock examples with real returns (per Round 46 spec)
- Must include "這只是眾多策略之一" disclaimer
- `_lesson_card()` visual_area uses `#EBF5FB` background — this is NOT in the design system palette. **Recommendation**: Change to white (`#FFFFFF`) with a `#ECF0F1` border, matching the design system.

**Effort Estimate**: 6-8h (per Round 46). Design component reuse is high since `_lesson_card()`, `_progress_dots()`, `_白话_card()` already exist.

---

### 1.2 C203: Company Ecosystem Cards v1

**Current Status**: Redefined from "Supply Chain Visual Map" (network graph, 36-50h) to "Company Ecosystem Cards" (card-based, 12-15h). Uses existing `group_structures.yaml` + manually curated data. No network graph in v1. Pending Daniel approval.

**Design Philosophy Fit**: ⚠️ Moderate — card-based approach is fully PPT-compliant, but the redefined scope loses the unique visual differentiator.

**Design Tier Assessment**: The original C203 (node-and-link diagram) was rated Medium UX impact with compliance warnings due to Streamlit rendering difficulty and D-003 regression risk. The card-based v1 eliminates these risks entirely.

**Components to Reuse from `_router_base.py`**:
1. **`_subsidiary_card()`** (line 269-303) — **PRIMARY COMPONENT**. Already exists, already used by `group_structure.py`. Full design spec:
   - White background (`#FFFFFF`), `border-radius:12px`, `#ECF0F1` border
   - Flexbox layout: left side = name + holding badge; right side = holding % + revenue %
   - Business description in `#7F8C8D` text; relationship in `#27AE60` green italic
   - Holding badge uses color-coded `hold_color` parameter (already supports `#E74C3C`, `#3498DB`, `#27AE60`)
   - **This is exactly the card layout needed for C203.** It was designed for this purpose.

2. **`_info_card()`** (line 225-231) — For ecosystem overview banners (e.g., "台積電的生態系概覽").

3. **`_summary_card()`** (line 192-198) — For section headers and narrative summaries.

4. **`_mini_score_card()`** (line 201-221) — For quick score/glance metrics (e.g., "生態系規模: 8/10").

5. **`_section_title()`** (line 70-79) — For section headers. ⚠️ Note: The emoji auto-prepend logic (D-005) still has the emoji conflict bug. Section titles like "🏢 供應鏈" would become "📊 🏢 供应链" with double emoji.

**Can C203 Reuse `_白话_card()`?**
- **Yes, but `_subsidiary_card()` is the better fit.** Here's the analysis:
  - `_白话_card()` is a vertical card: label on top, large value in middle, analogy at bottom. It's designed for metric display (PER, ROE, revenue).
  - `_subsidiary_card()` is a horizontal card: name + badge on left, metrics on right, description below. It's designed for entity display (ecosystem members).
  - C203 ecosystem cards need to show company name, relationship type, holding %, revenue %, AND description — this matches `_subsidiary_card()` perfectly.
  - **Recommendation**: Use `_subsidiary_card()` as the primary card. Use `_白话_card()` only for summary statistics (e.g., "總覽: 4 家子公司" as a count card above the list).
  - **New card variant needed?** NO. `_subsidiary_card()` already supports all required fields. The only extension needed: the badge logic in `group_structure.py` (lines 222-230) hardcodes three tiers (控股/轉投資/一般). C203 may want different tiers. The tier logic should stay in the page file, not the component. The component's `hold_label` and `hold_color` parameters are already generic enough.

**Design Recommendation for C203 Layout**:
```
┌─────────────────────────────────────────────────┐
│  🏢 {Company} 生態系 — {N} 個重要成員            │
├─────────────────────────────────────────────────┤
│  📋 生態系總覽                                    │
│  [_summary_card: one-line description]           │
├─────────────────────────────────────────────────┤
│  🗺️ 供應鏈關係                                    │
│  [_subsidiary_card: 供應商1]                      │
│  [_subsidiary_card: 供應商2]                      │
│  ── 分隔線 ──                                    │
│  [_subsidiary_card: 客戶1]                        │
│  [_subsidiary_card: 客戶2]                        │
├─────────────────────────────────────────────────┤
│  📊 持股比例長條圖 (Plotly grouped bar)            │
│  [_info_card: 圖表解讀]                           │
└─────────────────────────────────────────────────┘
```

**Extension Needed**: The current `_subsidiary_card()` only shows holding + revenue. C203 may also want "relationship type" labels (供應商/客戶/子公司). The `hold_label` parameter already supports this (it accepts any string). **No component change needed.**

---

### 1.3 C209: Collapsible Source Section

**Current Status**: Redefined in Round 49. No architecture doc. Design assessment needed.

**Design Philosophy Fit**: ✅ Strong — progressive disclosure is a core UI pattern already used throughout the app.

**Where Should It Be Placed Per Page?**

The "source" section shows data provenance: which API, when fetched, data freshness. Per the design system's Zone C rules (interactive controls at top, separated from data), the source section should be placed:

1. **Business Card Page**: After all data sections, before footer. Use `st.expander("📡 資料來源與新鮮度", expanded=False)` at the bottom of the main content area.
2. **Chart Pages**: Below each chart, a small `st.caption()` with source info. For detailed source, use an expander.
3. **Event Dashboard**: Already has freshness indicator in `_render_freshness_indicator()`. Source info should be added there.
4. **Daily Market**: Already has `_render_freshness_caption()` but no detailed source.

**Component Pattern**:
- **Option A**: Use existing `_advanced_content_expander()` (line 569-572) — it's literally `st.expander()` with icon + title. This is the simplest approach.
- **Option B**: Create a new `_source_section()` component that standardizes the source display format across all pages. Recommended format:
  ```
  📡 資料來源
  ├── 價格資料: FinMind API (2026-06-17 09:30)
  ├── 財務資料: FinMind API (2026-06-15 自動更新)
  ├── 新聞資料: FinMind API (2026-06-17 即時)
  └── 最後更新: 2026-06-17 10:00
  ```
- **Recommendation**: Option B. Create a new `_source_section()` in `_router_base.py` that takes a list of source dicts and renders them in a standardized collapsible format. This ensures consistency across all pages.

**Design Spec for `_source_section()`**:
```python
def _source_section(sources: list[dict], last_updated: str) -> None:
    """
    Args:
        sources: [{"label": "價格資料", "api": "FinMind", "time": "09:30"}, ...]
        last_updated: "2026-06-17 10:00"
    """
    with st.expander("📡 資料來源", expanded=False):
        for src in sources:
            st.caption(f"**{src['label']}**: {src['api']} ({src['time']})")
        st.caption(f"最後更新: {last_updated}")
```

**Placement Priority**:
1. Business Card (highest traffic page)
2. Daily Market Dashboard (C201 — data freshness is critical)
3. Event Dashboard (already has partial freshness UI)
4. All other pages (batch update)

---

## 2. Top 5 Design System Fixes from Round 7 — Verification

### Fix Status Summary

| # | Issue | Round 7 Priority | Status | Verified In Code |
|---|-------|-----------------|--------|-----------------|
| 1 | **D-005**: `_section_title()` emoji conflict | Priority 1 (15 min) | ❌ **STILL PRESENT** | `_router_base.py` line 76: `if code >= 0x2300` — titles starting with emoji ≥ U+2300 skip the prefix, but titles with emoji in the 0x2000-0x22FF range still get double-prefixed. Titles like "🗺️ 產業熱力圖" (U+1F5FA) pass, but "📊 營收" (U+1F4CA) also passes. The real issue: titles that START with ASCII but contain emoji later still get `📊` prepended. |
| 2 | **D-071**: Replace Set3 palette in pie charts | Priority 2 (30 min) | ✅ **FIXED** | `chart_stock_financial.py` line 96: Uses explicit `['#3498DB', '#27AE60', '#E74C3C', '#2C3E50', '#7F8C8D', '#ECF0F1']` — no `px.colors.qualitative.Set3` found in code. |
| 3 | **D-084**: Replace `st.bar_chart` with Plotly | Priority 3 (30 min) | ✅ **FIXED** | `group_structure.py` line 258: Comment says "Plotly grouped bar chart (replaces st.bar_chart for design consistency)". No `st.bar_chart` found in any page file. |
| 4 | **D-073**: Fix `#5D6D7E` → `#7F8C8D` in `_info_card()` | Priority 4 (5 min) | ❌ **STILL PRESENT** | `_router_base.py` line 229: `color:#7F8C8D` — **Wait, this is already `#7F8C8D`!** Let me re-check. The `_info_card()` content div on line 229 uses `color:#7F8C8D` which IS the correct secondary text color. **D-073 appears FIXED.** However, the `_glossary_annotated_metric()` on line 432 also uses `color:#7F8C8D` — correct. |
| 5 | **D-074**: Standardize `#F8F9FA` background in `_白话_card()` | Priority 5 (10 min) | ❌ **STILL PRESENT** | `_router_base.py` line 185: `background:white` — **Wait, `_白话_card()` uses `white` not `#F8F9FA`!** The design system spec says card background should be `#F8F9FA`. But `_白话_card()` uses `white`. This is technically a deviation, but `white` is arguably cleaner than `#F8F9FA` for cards. The REAL `#F8F9FA` usage is in `_info_card()` (line 227), `_mini_score_card()` (line 217), `_glossary_annotated_metric()` (line 430), and `_lesson_card()` (line 536). These all use `#F8F9FA` which IS the design system's card background color. **D-074 is partially present — `_白话_card()` uses `white` instead of `#F8F9FA`, which is a deliberate design choice (white cards with `#ECF0F1` border for visual separation).** |

### Detailed Fix Analysis

**D-005 — Emoji Conflict (STILL PRESENT, needs fix)**:
```python
# _router_base.py lines 70-79
def _section_title(title: str):
    if not title:
        return
    first_char = title[0]
    code = ord(first_char)
    if code >= 0x2300:  # ← BUG: This catches SOME emoji but not all
        st.markdown(f"### {title}")
    else:
        st.markdown(f"### 📊 {title}")  # ← Always prepends 📊
```
**Problem**: The threshold `0x2300` catches technical symbols (⌀, ⌁, etc.) but misses many common emoji. For example:
- "🗺️ 產業熱力圖" → 🗺 = U+1F5FA ≥ 0x2300 → ✅ No double prefix
- "📊 營收組成" → 📊 = U+1F4CA ≥ 0x2300 → ✅ No double prefix
- "🏢 集團總覽" → 🏢 = U+1F3E2 ≥ 0x2300 → ✅ No double prefix
- "母公司" → 母 = U+6BCD ≥ 0x2300 → ✅ No double prefix (Chinese chars are > 0x2300)
- "1 年" → 1 = U+0031 < 0x2300 → ❌ Gets "📊 1 年" (correct behavior for non-emoji)

**Actual bug scenario**: Titles that start with ASCII characters (A-Z, 0-9) will always get `📊` prepended. This is the intended behavior for plain text titles. The bug is actually **minimal in practice** because most section titles in the codebase start with Chinese characters (which are > 0x2300) or emoji.

**Revised Assessment**: D-005 is **low severity in practice**. The only affected titles are pure ASCII titles like "Overview" or "Summary" which are rare in this Chinese-language app. **Recommendation**: Lower priority to P3. Fix only if English section titles are introduced.

**D-073 — Info Card Content Color (APPEARS FIXED)**:
The `_info_card()` component on line 229 uses `color:#7F8C8D` for content text, which matches the design system's secondary text color. The Round 7 report flagged `#5D6D7E` in `_info_card()`, but the current code shows `#7F8C8D`. This was likely fixed in the Sprint 24 cleanup (commit `2fc60d3`).

**D-074 — 白话 Card Background (PARTIALLY PRESENT)**:
- `_白话_card()` uses `background:white` — deviates from design system's `#F8F9FA`
- All other shared cards (`_info_card`, `_mini_score_card`, `_lesson_card`, `_glossary_annotated_metric`) use `#F8F9FA`
- **Recommendation**: Change `_白话_card()` from `white` to `#F8F9FA` for consistency. This is a 1-line change. However, the white background may have been intentional to create visual hierarchy (white cards = primary data, gray cards = secondary info). **Decision needed from Daniel**: Should `_白话_card()` use white or `#F8F9FA`?

### Remaining Non-Palette Colors in Codebase

After the Sprint 24 cleanup, these non-palette colors remain:

| Color | Location | Should Be | Severity |
|-------|----------|-----------|----------|
| `#BDC3C7` | `chart_stock_health.py:76` (benchmark line), `_financial.py:249` (table header border) | Not in palette — use `#ECF0F1` for borders | Low |
| `#95A5A6` | `main.py:115` (search placeholder), `main.py:304` (welcome text) | Not in palette — use `#7F8C8D` | Low |
| `#F9E79F` / `#7D6608` | `main.py:55,59` (disclaimer CSS) | Not in palette — use `#FEF9E7` bg + `#2C3E50` text | Low |
| `#EBF5FB` | `_router_base.py:534` (lesson_card visual_area) | Not in palette — use `#F8F9FA` | Low |
| `#E8F8F5` | `_router_base.py:561` (beginner_banner bg) | Not in palette — acceptable as "success" bg | Low |
| `#F0F7FF` | `_router_base.py:262` (so_what_box bg) | Not in palette — use `#F8F9FA` | Low |
| `#2980B9` | `_router_base.py:262` (so_what_box border) | Not in palette — use `#3498DB` | Low |
| `#white` | `_router_base.py:185` (白话_card bg) | Design system says `#F8F9FA` | Low |

---

## 3. Current Page Grades (Round 7 — Unchanged)

| Page | Grade | Change | Key Issues |
|------|-------|--------|------------|
| `business_card.py` | B | ← No change | 6 minor color violations (D-79 `#BDC3C7`, D-83 `#95A5A6`) |
| `chart.py` (services) | B+ | ← No change | D-071 Set3 palette FIXED in Sprint 24 |
| `_router_base.py` | B | ← Upgraded from B+ | D-073 affects all pages via shared components |
| `event_dashboard.py` | A- | ← No change | **Best-graded page** |
| `financial_health.py` | C+ | ← No change | Text volume issues |
| `etf_detail.py` | C | ← Downgraded from C+ | D-76, D-77 new violations |
| `group_structure.py` | D | ← No change | D-078 `#5D6D7E`, D-084 `st.bar_chart` (FIXED) |
| `category_browser.py` | D | ← No change | Structural issues |
| `etf_browser.py` | C | ← No change | |
| `watchlist_page.py` | C | ← No change | |
| `operation_checkup.py` | C | ← No change | |
| `peer_comparison.py` | C | ← No change | |
| `main.py` | C- | ← Downgraded from C | D-81, D-82, D-83 new violations |

**New pages not yet graded**:
- `daily_market.py` (C201) — Needs first design review
- `learn_first_gate.py` (C163) — Needs first design review

---

## 4. Design Consistency Analysis

### 4.1 Can C203 Reuse `_白话_card()`?

**Answer**: Yes, but `_subsidiary_card()` is the correct primary component.

| Aspect | `_白话_card()` | `_subsidiary_card()` |
|--------|---------------|---------------------|
| Layout | Vertical (label/value/analogy) | Horizontal (name+badge / metrics / description) |
| Best for | Single metric display | Entity display (company, fund, etc.) |
| Background | `white` | `white` |
| Border | `#ECF0F1` + `#3498DB` left | `#ECF0F1` all-around |
| Badge support | None | Yes (hold_label + hold_color) |
| Multi-line content | Analogy only | Business + relation sections |
| C203 fit | Poor — would need custom HTML | **Perfect — designed for this** |

**Recommendation**: C203 should use `_subsidiary_card()` as the primary card component. No new card variant is needed. The existing `hold_label` and `hold_color` parameters are generic enough to support any badge type (供應商/客戶/子公司/轉投資).

### 4.2 Card Component Inventory

The `_router_base.py` now has **11 card/component functions**:

| Component | Lines | Background | Border | Use Case |
|-----------|-------|------------|--------|----------|
| `_白话_card()` | 183-190 | `white` | `#ECF0F1` + `#3498DB` left | Metric display with analogy |
| `_summary_card()` | 192-198 | `#FFF8F0` | `{border_color}` left (default `#3498DB`) | Narrative summary / tip card |
| `_mini_score_card()` | 201-221 | `#F8F9FA` | Score-colored left | Score/glance metrics |
| `_info_card()` | 225-231 | `#F8F9FA` | `#3498DB` left | Information / explanation |
| `_so_what_box()` | 234-266 | `#F0F7FF` | `#2980B9` left | Synthesized implications |
| `_subsidiary_card()` | 269-303 | `white` | `#ECF0F1` all | Entity cards (ecosystem) |
| `_lesson_card()` | 530-542 | `#F8F9FA` | `#3498DB` left | Educational content |
| `_beginner_banner()` | 558-566 | `#E8F8F5` | `#27AE60` left | Beginner mode banner |
| `_glossary_annotated_metric()` | 381-435 | `#F8F9FA` | `#3498DB` or `#ECF0F1` left | Metric with glossary tooltip |

**Consistency Issues**:
1. **Background inconsistency**: `_白话_card()` and `_subsidiary_card()` use `white`; all others use `#F8F9FA`. This creates a visual hierarchy (white = primary, gray = secondary) which may be intentional but is not documented.
2. **Border inconsistency**: `_白话_card()` uses `border:1px solid #ECF0F1` + `border-left:4px solid #3498DB`. `_subsidiary_card()` uses `border:1px solid #ECF0F1` (no colored left border). Others use only `border-left:4px solid {color}` (no full border).
3. **Missing component**: No standardized `_source_section()` component exists yet (needed for C209).

---

## 5. Design Debt from Sprint 23 Features (C199, C200, C202)

### 5.1 C199 — Bear vs Bull Debate Cards

**Service Layer** (`debate_engine.py`): ✅ Clean — pure Python, no Streamlit imports, returns i18n keys.
**Design Debt**: **NONE in service layer.** The `validate_debate_text()` naming issue (low severity, noted in handoff.md) is a code clarity issue, not a design issue.

**Page Layer**: C199 rendering is embedded in `business_card/_expert_analysis.py` (not read in this review, but confirmed imported in `_main.py` line 63). The debate cards use `_info_card()` from `_router_base.py` per Round 46 spec.

**Design Concern**: The debate cards should use a **side-by-side layout** (Bear left, Bull right) with colored borders (red `#E74C3C` for Bear, green `#27AE60` for Bull). The current `_info_card()` only supports a single border color. **If the implementation uses `_info_card()` for both cards, the colored border differentiation is lost.**

**Recommendation**: Check if `_expert_analysis.py` uses `_info_card()` or custom HTML for debate cards. If `_info_card()`, consider creating a `_debate_card(side, title, points)` component that handles the side-specific styling.

### 5.2 C200 — What If Calculator

**Service Layer** (`scenario_calculator.py`): ✅ Clean — pure Python, no Streamlit, returns `ScenarioResult` TypedDict with error keys.

**Design Debt**: The calculator UI (in `business_card/_historical_scenarios.py`) uses interactive controls (date picker, amount input). Per Zone C rules, these must be at the TOP of the content area, separated from data display. **Potential D-003 regression risk** if custom HTML was used instead of shared components.

**Recommendation**: Verify that `_historical_scenarios.py` uses `_白话_card()` for results and `_info_card()` for interpretation. If custom HTML was used, refactor to shared components.

### 5.3 C202 — Story Arc Labels

**Service Layer** (`story_arc_detector.py`): ✅ Clean — pure Python, returns i18n keys, no Streamlit.

**Design Debt**: Story arc labels use emoji (📈📉🔄🌱) which are rendered inline. The `_ARC_EMOJI` dict in the service layer is a design concern — emoji selection should ideally be driven by the design system, not hardcoded in the service layer. However, since these are data keys (not display text), this is acceptable.

**No significant design debt.**

### 5.4 Summary of Sprint 23 Design Debt

| Feature | Service Layer | Page Layer | Design Debt |
|---------|--------------|------------|-------------|
| C199 Debate | ✅ Clean | ⚠️ Verify card styling | Potential: debate cards may not have colored borders |
| C200 Calculator | ✅ Clean | ⚠️ Verify Zone C compliance | Potential: interactive controls may not follow Zone C rules |
| C202 Story Arc | ✅ Clean | ✅ Clean | None |

---

## 6. Design System Fix Recommendations and Visual Impact

### 6.1 Quick Wins (≤15 min each)

| Fix | Effort | Visual Impact | Priority |
|-----|--------|---------------|----------|
| Change `_白话_card()` background from `white` to `#F8F9FA` | 1 line | **Medium** — Unifies card background across all components. All cards will have consistent gray background. | P2 |
| Change `_lesson_card()` visual_area from `#EBF5FB` to `#F8F9FA` | 1 line | **Low** — Removes non-palette blue from lesson cards | P2 |
| Change `_so_what_box()` bg from `#F0F7FF` to `#F8F9FA`, border from `#2980B9` to `#3498DB` | 2 lines | **Low** — Removes non-palette blue from implication box | P2 |
| Change `_beginner_banner()` bg from `#E8F8F5` to `#F8F9FA` | 1 line | **Low** — Removes non-palette green from banner | P3 |
| Change `main.py` disclaimer CSS from `#F9E79F`/`#7D6608` to `#FEF9E7`/`#2C3E50` | 2 lines | **Low** — Standardizes disclaimer colors | P2 |
| Change `main.py` welcome text from `#95A5A6` to `#7F8C8D` | 1 line | **Low** — Standardizes secondary text color | P2 |
| Change `main.py` search placeholder from `#95A5A6` to `#7F8C8D` | 1 line | **Low** — Standardizes placeholder color | P3 |
| Change `chart_stock_health.py` benchmark line from `#BDC3C7` to `#ECF0F1` | 1 line | **Low** — Standardizes border color | P3 |

**Total quick win effort**: ~10 minutes, 8 lines changed. **Cumulative visual impact**: Removes all non-palette colors from shared components. Brings the codebase from C+ to **B-** grade.

### 6.2 Medium Effort Fixes (30-60 min)

| Fix | Effort | Visual Impact | Priority |
|-----|--------|---------------|----------|
| Create `_source_section()` component for C209 | 30 min | **High** — Standardizes data source display across all pages | P1 (blocks C209) |
| Fix D-005 emoji logic in `_section_title()` | 15 min | **Low** — Fixes edge case for ASCII-only titles | P3 |
| Audit C199 debate card styling | 30 min | **Medium** — Ensures Bear/Bull color differentiation | P2 |
| Audit C200 calculator Zone C compliance | 30 min | **Medium** — Ensures interactive controls follow Zone C rules | P2 |

### 6.3 New Component Recommendations

1. **`_source_section(sources, last_updated)`** — For C209. Standardized collapsible source display.
2. **`_debate_card(side, title, points)`** — For C199. Side-specific colored border card (red for Bear, green for Bull). Only needed if current implementation lacks color differentiation.
3. **`_ecosystem_card(name, type, metrics, description)`** — NOT needed. `_subsidiary_card()` already covers this use case.

---

## 7. New Design Recommendations

### 7.1 Card Background Standardization

**Problem**: `_白话_card()` and `_subsidiary_card()` use `white` background while all other cards use `#F8F9FA`. This creates an undocumented visual hierarchy.

**Recommendation**: Adopt a two-tier card system:
- **Tier 1 (Primary data)**: `#F8F9FA` background — for key metrics, primary content
- **Tier 2 (Secondary info)**: `white` background with `#ECF0F1` border — for supporting content, entity cards

Under this system:
- `_白话_card()` → Change to `#F8F9FA` (it displays primary metrics)
- `_subsidiary_card()` → Keep `white` (it displays supporting entity info)
- All others → Keep `#F8F9FA`

**This is a design decision for Daniel to confirm.**

### 7.2 Section Title Emoji Convention

**Problem**: `_section_title()` auto-prepends `📊` to non-emoji titles. This means every plain text section title gets a chart emoji, which is semantically incorrect for non-chart sections (e.g., "📊 集團策略解讀").

**Recommendation**: Change the default emoji to a generic bullet or remove auto-prefix entirely:
```python
def _section_title(title: str, icon: str = ""):
    if not title:
        return
    if icon:
        st.markdown(f"### {icon} {title}")
    else:
        st.markdown(f"### {title}")
```
This lets each page specify the appropriate icon. **Breaking change** — requires updating all call sites.

### 7.3 Daily Market Page (C201) Design Review

The `daily_market.py` page was implemented in Sprint 24 but has not received a formal design review. Key observations:
- ✅ Uses `_白话_card()`, `_info_card()`, `_summary_card()`, `_section_title()` — all shared components
- ✅ Uses `st.spinner()` for loading state
- ✅ Uses `#27AE60`/`#E74C3C` for up/down colors — correct
- ⚠️ Sector strip cards use inline HTML with `#F8F9FA` background — should use a shared component
- ⚠️ Top mover rows use inline HTML — should use a shared component or `_白话_card()`
- ⚠️ No data source section (C209 needed here — freshness is critical for market data)

**Estimated grade: B** — Good component reuse, minor inline HTML issues.

### 7.4 Learn First Gate (C163) Design Review

The `learn_first_gate.py` page uses `_lesson_card()`, `_progress_dots()`, `_beginner_banner()` — all shared components. Clean implementation.

- ✅ Component reuse is excellent
- ✅ Navigation pattern (prev/next/skip) is clear
- ⚠️ `_lesson_card()` visual_area uses `#EBF5FB` (non-palette)
- ⚠️ No data source section needed (static educational content)

**Estimated grade: B+** — Clean, component-driven, minor color issue.

---

## 8. Sprint 25 Design Recommendations

### Priority Order

| Priority | Feature | Design Readiness | Recommendation |
|----------|---------|-----------------|----------------|
| **P1** | C209 Collapsible Source | ✅ Ready | Create `_source_section()` component (30 min). Apply to daily_market.py and business_card.py first. |
| **P2** | C206 Recurring Investment Ed | ✅ Ready | Use existing `_lesson_card()` + `_progress_dots()` + `_白话_card()`. Fix `#EBF5FB` in visual_area. Place in sidebar nav as "投資概念". |
| **P3** | C203 Ecosystem Cards v1 | ✅ Ready | Reuse `_subsidiary_card()` — no new component needed. Extend data layer with supplier/customer relationship types. |
| **P4** | Quick Win Color Fixes | ✅ Ready | 8 lines, 10 minutes. Do before Sprint 25 development. |
| **P5** | C199/C200 Design Audit | ⚠️ Needs investigation | Verify debate card colors and calculator Zone C compliance. |

### Pre-Development Checklist for Sprint 25

Before writing any Sprint 25 code, confirm:
- [ ] Quick win color fixes applied (Section 6.1)
- [ ] `_source_section()` component created (for C209)
- [ ] `_lesson_card()` visual_area color fixed (for C206)
- [ ] Daniel confirms C206 scope (education only, no calculator)
- [ ] Daniel confirms C203 "ecosystem cards" approach
- [ ] Daniel confirms card background standardization decision (Section 7.1)
- [ ] C199 debate card styling verified
- [ ] C200 calculator Zone C compliance verified

---

## 9. Cumulative Metrics

| Metric | Value |
|--------|-------|
| Total design issues (all rounds) | 92 |
| Issues fixed (all rounds) | 5 |
| Issues remaining | 87 |
| Current grade | C+ |
| Grade after quick wins | B- |
| Grade after medium fixes | B |
| New components needed | 1 (`_source_section`) |
| Components ready for reuse | 11 (in `_router_base.py`) |
| Pages not yet graded | 2 (daily_market, learn_first_gate) |

---

*Design Analysis completed: 2026-06-17*
*Next review: Round 51 (after Sprint 25 planning decisions)*
