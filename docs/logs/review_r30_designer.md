# Design Review — Review Round 30 (Sprint 13b Post-Mortem + Sprint 14 Design Prerequisites)

> **Date**: 2026-06-18
> **Reviewer**: Design Reviewer
> **Scope**: Sprint 13b design verification (D-079, C36 Revenue Tree V2, C46 Moat Analysis), new issue identification (D-081+), Sprint 14 design prerequisites

---

## 1. Design Grade: **A-**

**Justification**: Sprint 13b delivered 3 features with generally strong design, but introduced 2 regressions and left 1 known issue (D-080) unresolved. The overall design quality remains high — all features follow PPT-style principles and use shared components. However, the regressions prevent maintaining the straight-A streak.

**Grade trajectory**: A (R28) → **A- (R30)**

---

## 2. Sprint 13b Design Verification

### 2.1 D-079 Fix — Dual Tooltip Pattern Merged ✅ RESOLVED+

**File**: `src/pages/business_card/_sections/_financial.py` lines 33-79

**What was verified**:
- `_render_metric_popover()` now accepts `glossary_service` parameter and merges glossary definition + metric education into a single interaction
- The separate `_glossary_tooltip()` calls were removed from `_render_key_metrics()` — no more dual tooltips on the same metric
- Single ❓ button per metric flows: glossary definition → analogy → example → plain-language explanation → analogy → direction → historical context
- All 6 metric call sites (PER, gross_margin, revenue_yoy, ROE, dividend_yield, PBR) updated consistently

**Design system compliance**:
- ✅ One help icon per metric (design system Section IV interaction rule)
- ✅ Uses `_METRIC_GLOSSARY_MAP` dict for clean term mapping
- ✅ St.expander for popover content works across all Streamlit versions
- ⚠️ **REGRESSION**: The metric card itself (lines 41-47) uses `unsafe_allow_html=True` with inline HTML instead of `_白话_card()`. This was introduced as part of the D-079 fix — the card HTML is identical to `_白话_card()` but rendered inline to accommodate the side-by-side ❓ button layout (`st.columns([5, 1])`). This is a **D-003 regression** tracked as D-081.

**Verdict**: D-079 dual tooltip issue is fully resolved. The single-interaction pattern is clean and follows the design system. The inline HTML trade-off is acceptable given the two-column layout requirement, but should be addressed as a new reusable component.

### 2.2 C36 Revenue Tree V2 — ✅ WELL-DESIGNED

**Files**: `src/pages/revenue_tree.py`, `src/services/chart.py` lines 190-242, `src/pages/business_card/_main.py` lines 253-255

**What was verified**:

**Standalone page (`revenue_tree.py`)**:
- ✅ Page header uses `_section_title()` helper (not inline HTML or raw st.markdown)
- ✅ Pie chart as default view with `st.toggle("🔬 切換樹狀圖", value=False)` for treemap toggle
- ✅ Concentration warning: triggers at >60% threshold via `_info_card("⚠️ 營收集中風險", ...)` — uses shared component correctly
- ✅ Trend mini-chart: 12-month sparkline via `create_revenue_trend_chart` at height=200px with `showlegend=False`
- ✅ Revenue detail cards use `_白话_card()` for each source (plain-language analogy)
- ✅ Empty state uses `st.info("目前沒有詳細營收組成資料")` — acceptable (D-009 notes inconsistency)
- ✅ Historian disclaimer via `_historian_disclaimer("revenue_tree")`
- ✅ YoY growth context uses `_info_card()` with directional emoji (📈/📉)

**Treemap chart (`chart.py`)**:
- ✅ Uses Plotly `go.Treemap` with white cell borders, color-coded cells (10-color palette)
- ✅ Hover template shows `name: value%` + description
- ✅ Theme-aware: transparent background via `_get_chart_colors()`, consistent with other charts
- ✅ `textfont=dict(size=14, color="white")` for readability on colored cells
- ✅ `pathbar=dict(visible=False)` for clean appearance

**Business Card integration**:
- ✅ Revenue tree appears in `"🌳 營收結構樹"` expander (detailed mode only) — proper progressive disclosure
- ✅ Standalone page accessible via `"🔬 更多分析"` expander → button navigation

**PPT-style compliance**:
- Charts visible first, text below ✅
- One key point per page: "深入拆解這家公司靠什麼賺錢" ✅
- Concentration warning uses orange-colored `_info_card` (warning pattern) ✅
- Total text under 200 chars (excluding chart labels) ✅

**Verdict**: C36 V2 is a well-designed feature that follows the design system closely. The treemap is a professional addition, the concentration warning is appropriately styled, and the trend sparkline adds context without clutter.

### 2.3 C46 Moat Analysis — ✅ WELL-DESIGNED (with minor issues)

**Files**: `src/pages/business_card/_sections/_moat.py`, `src/services/moat_analyzer.py`, `src/pages/business_card/_main.py` lines 273-275

**What was verified**:

**Visual layout**:
- ✅ Moat type badge via `_info_card("護城河類型", ..., "🏰")` — blue info card, shared component
- ✅ Moat score via `_summary_card("護城河強度", ..., "🏰")` — orange hero card, shared component
- ✅ 5 dimension mini-cards in `st.columns(5)` with 🟢/🟡/🔴 color-coded emoji prefixes
- ✅ Evidence list via `_info_card("歷史證據", ..., "📋")` — single card with bullet points

**Scoring system (`moat_analyzer.py`)**:
- ✅ 5 dimensions: 品牌力, 成本優勢, 網路效應, 轉換成本, 規模經濟
- ✅ Template scoring for non-curated stocks (brand from gross margin, network from revenue yoy, switching from revenue CV, scale from ROE+GM)
- ✅ Moat type classification: highest-scoring dimension → type, with threshold <40 → "無明顯護城河"
- ✅ YAML data source for 20 curated TW stocks (separation of data from logic)
- ✅ Zero Streamlit imports in service layer

**Design system compliance**:
- ✅ All cards use shared components (`_info_card`, `_summary_card`) — zero inline HTML
- ✅ Color coding: 🟢 (≥70), 🟡 (≥40), 🔴 (<40) — consistent with health score color system
- ✅ Progressive disclosure: appears in `"🏰 護城河分析"` expander (detailed mode)
- ✅ Evidence-first design: historical facts, no stock-picking language
- ⚠️ **ISSUE**: Dimension mini-cards (line 49) use `_summary_card()` with a single icon emoji prefix `""` — this renders with the orange border/summary style for what are essentially data display cards. Should use a dedicated `_mini_card()` or an info-card variant. Tracked as D-082.

**Architecture**:
- ✅ Service layer: 166 lines, zero Streamlit dependency
- ✅ Data/moat_data.yaml: stock_id → {moat_type, moat_score, dimensions, evidence}
- ✅ C124 Moat Type merged into C46 as required by Challenger R29

**Verdict**: C46 is a well-architected, evidence-first design that avoids stock-picking drift. The visual layout is clean and uses shared components. The mini-card styling is the only minor concern.

### 2.4 D-080 — Story Card Health Score Border Color ❌ NOT RESOLVED

**File**: `src/pages/business_card/_sections/_summary.py` line 142

**Status**: The `_summary_card()` component uses a fixed `border-left:4px solid #F39C12` (orange) regardless of health score. D-080 requested dynamic border color by health level (green ≥70, amber ≥40, red <40).

**Current code**: `_summary_card("整體健康度", f"{overall_health:.0f}/100 {health_label}", "🏰")` — always orange border.

**Impact**: Low. The health label already shows 🟢/🟡/🔴 emoji. The orange border is a minor inconsistency.

**Recommendation**: Address as part of Sprint 14 C40 Mode Toggle work (see design prerequisites below).

---

## 3. New Design Issues (D-081+)

### D-081: Metric Popover Card Uses Inline HTML Instead of _白话_card() (D-003 Regression)

- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30
- **Description**: `_render_metric_popover()` in `_financial.py` (lines 41-47) renders the metric card using `unsafe_allow_html=True` with inline HTML instead of calling `_白话_card()`. The inline HTML is a near-exact copy of `_白话_card()`'s styling (`background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB`). This was introduced as part of the D-079 fix — the card needs to be rendered inline to share a row with the ❓ help button via `st.columns([5, 1])`.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py` lines 41-47
- **Proposed Fix**: Create a `_白话_card_with_help(label, value, analogy, help_key)` helper in `_router_base.py` that renders the card + button in a two-column layout using shared component styling. Alternatively, modify `_白话_card()` to accept an optional `help_icon` parameter.
- **Effort**: 0.5-1h
- **Note**: This is a D-003 regression, but the trade-off is architecturally justified (two-column layout requirement). Still should be consolidated into a shared component.

### D-082: Moat Dimension Mini-Cards Use _summary_card() with Empty Icon

- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30
- **Description**: The 5 moat dimension mini-cards in `_moat.py` (line 49) use `_summary_card(f"{color_emoji} {dim_name}", f"{score_val:.0f} 分", "")`. The `_summary_card()` renders with orange `border-left:4px solid #F39C12` and `#FFF8F0` background — a "hero card" style that's inappropriate for dimension score cards that should be neutral information display. The empty icon parameter `""` also renders an empty icon slot in the card header. This creates a visual mismatch with the rest of the page.
- **Affected Files**: `src/pages/business_card/_sections/_moat.py` line 49
- **Proposed Fix**: Create a `_mini_score_card(label, score)` helper in `_router_base.py` with compact styling: `background:#F8F9FA;border-radius:8px;padding:0.5rem;border-left:4px solid {score_color}`. Use score-based border color (green/amber/red).
- **Effort**: 0.5h

### D-083: Story Card Health Score Border Not Color-Coded by Health Level (D-080 Follow-up)

- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30 (continuation of D-080)
- **Description**: The health score in the story card (line 142 `_summary_card("整體健康度", ...)`) always renders with orange border (#F39C12). D-080 identified this in Round 28 but was not resolved in Sprint 13b. The health label shows 🟢/🟡/🟠 emoji but the card border doesn't match. This creates a visual disconnect.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` line 142
- **Proposed Fix**: Add optional `border_color` parameter to `_summary_card()` in `_router_base.py`. Pass health-score-based color: `#27AE60` (≥70), `#F39C12` (≥40), `#E74C3C` (<40).
- **Effort**: 0.25h
- **Note**: This is the same fix as D-080 but now tracked separately for Sprint 14.

---

## 4. Sprint 14 Design Prerequisites

### 4.1 C40 Mode Toggle (Simple/Detailed)

**Current State**: Already implemented as `st.toggle("簡易模式", value=True)` in `_main.py` line 203. The toggle exists and works. However, C40 should formalize and enhance it.

**Design Spec for Enhancement**:

**Current behavior**: Toggle between `_render_simple_overview()` and full sections. This is well-designed but could be enhanced:

1. **Rename toggle**: "簡易模式" → "🔰 新手模式" / "📖 專業模式" for clearer UX
2. **Visual distinction**: Add a colored indicator — green badge for beginner, blue for expert
3. **Persistent choice**: Already uses `st.session_state["simple_mode"]` ✅
4. **On first visit**: Default to beginner mode (`value=True`) — already correct ✅
5. **Mode-specific content hints**: In beginner mode, show "💡 提示：切換到專業模式查看更多數據" as `st.caption()`

**Design system implications**:
- The toggle itself uses `st.toggle()` — this is a Streamlit primitive, not a shared component
- Consider creating `_mode_toggle(label, key)` in `_router_base.py` for consistency
- Mode state should propagate to child sections via `data` dict or session_state

**UX implications**:
- Beginner mode should show: Story Card → Takeaways → Deltas → Simple Overview
- Expert mode should show: Story Card → Takeaways → Deltas → Full Health + all expanders
- The "🔬 更多分析" expander should appear in both modes
- **Concern**: In beginner mode, C46 Moat Analysis is hidden (inside an expander that's only rendered in expert mode). Consider showing a compact moat indicator in beginner mode (one-line summary).

### 4.2 C126 Moat Comparison

**Design Spec — Two-Stock Comparison Layout**:

**Purpose**: Compare moat scores between two stocks side-by-side.

**Required C46 prerequisites** (already satisfied):
- ✅ 5-dimension scoring system exists
- ✅ Dimension names are consistent (品牌力, 成本優勢, 網路效應, 轉換成本, 規模經濟)
- ✅ Scores are 0-100 numeric values
- ✅ Moat type classification exists

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│  🏰 護城河比較                                               │
│                                                             │
│  TSMC (2330)          vs          鴻海 (2317)               │
│  品牌護城河                        成本護城河                 │
│  72/100                            58/100                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  品牌力    成本優勢   網路效應   轉換成本   規模經濟   │    │
│  │  85  ⬅️    70  ⬅️    60  ➡️    75  ⬅️    90  ⬅️   │    │
│  │  TSMC 較大  TSMC 較大  鴻海 較大  TSMC 較大  TSMC 較大 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  📊 雷達圖比較                          📋 證據對比          │
│  [dual radar chart]                    [side-by-side cards]  │
└─────────────────────────────────────────────────────────────┘
```

**Components needed**:
- Dual radar chart overlay (similar to `create_comparison_radar()` — already exists in `chart.py`)
- Dimension comparison row with directional arrows (⬅️/➡️)
- Side-by-side evidence cards using `_info_card()`
- Moat type badges using `_info_card()`

**Required from design system**:
- Radar chart: `create_comparison_radar()` already exists ✅
- Card components: `_info_card()`, `_summary_card()` already exist ✅
- Colors: Use design system blue (#3498DB) for stock A, red (#E74C3C) for stock B ✅ (already in `create_comparison_radar()`)

**New component needed**:
- `_comparison_row(label, value_a, value_b, stock_a_name, stock_b_name)` for dimension-by-dimension comparison

### 4.3 C47 Education Academy

**Design Spec — Structured Learning Path**:

**Purpose**: 10-15 structured lessons organized by difficulty, each using real TW stock examples.

**Layout — Lesson Card Pattern**:
```
┌─────────────────────────────────────────────────────────────┐
│  📚 投資學習學院                                             │
│                                                             │
│  🔰 入門                                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  第1課：什麼是股票？                                    │  │
│  │  📖 10 分鐘  |  ✅ 已完成  |  用台積電當例子            │  │
│  │  [開始課程]                                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  📗 中級                                                   │  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  第2課：怎麼看數字？                                    │  │
│  │  📖 15 分鐘  |  🔲 未完成  |  用鴻海當例子              │  │
│  │  [繼續課程]                                            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Components needed**:
1. `_lesson_card(title, duration, status, example_stock, level)` — new component
2. `_lesson_progress(current, total)` — progress indicator
3. Lesson content renderer using existing `_section_title()`, `_info_card()`, `_白话_card()`
4. Quiz integration at end of each lesson (uses existing `_summary_card()` with score feedback)

**Ten-second test**: A beginner should be able to see the lesson list and understand what they'll learn within 10 seconds. The card grid with level badges + duration + status achieves this.

**Content requirements**:
- Minimum 5 complete lessons for Sprint 14 (per R29 Challenger spec)
- Each lesson must pass ten-second test quality gate
- Historian tone QA required for all content
- Content budget: 40% of effort (per R29 Challenger condition)

**Design system compliance**:
- Uses existing card types for lesson cards ✅
- Quiz cards use existing `_summary_card()` pattern ✅
- Progress indicator uses `st.progress()` ✅
- All charts use Plotly with theme-aware colors ✅

---

## 5. Design System Updates Needed

### 5.1 New Components to Add to `docs/design/design_system.md`

1. **Metric Popover Card** (from D-081): Document the two-column card + help button pattern
2. **Mini Score Card** (from D-082): Compact dimension card with score-based border color
3. **Dynamic Summary Card**: `_summary_card()` with optional `border_color` parameter (from D-083)
4. **Lesson Card**: For C47 Education Academy — level badge, duration, status, example stock
5. **Comparison Row**: For C126 Moat Comparison — dimension-by-dimension with directional arrows

### 5.2 Existing Components to Update

1. **`_summary_card()`**: Add optional `border_color` parameter for health-score-aware rendering
2. **`_白话_card()`**: Add optional `help_icon` parameter for inline help button support
3. **`_glossary_tooltip()`**: Already documented in Round 28 but not yet added to `design_system.md` — add Section 3.6 Glossary Components

### 5.3 New Interaction Pattern to Document

**Mode Toggle** (C40): Document the beginner/expert mode pattern:
- Toggle placement: top-right of Zone C
- Default: beginner mode (value=True)
- State persistence: session_state
- Visual: caption explaining current mode

---

## 6. Summary

### Sprint 13b Design Assessment

| Feature | Design Quality | Issues |
|---------|---------------|--------|
| D-079 Tooltip Merge | ✅ Excellent | D-081 inline HTML regression (P2) |
| C36 Revenue Tree V2 | ✅ Excellent | None |
| C46 Moat Analysis | ✅ Good | D-082 mini-card style (P2) |

### New Issues: 3
- D-081: Metric popover inline HTML (P2)
- D-082: Moat mini-card _summary_card misuse (P2)
- D-083: Story card health border not color-coded (P2, D-080 continuation)

### Open Issues Status
- Total: 76 (was 73 + 3 new)
- P0: 0 ✅
- P1: 3 (D-003, D-005, D-006)
- P2: 32 (+3 from this round)
- Resolved: 27

### Sprint 14 Readiness
- **C40 Mode Toggle**: 🟢 READY — toggle exists, needs enhancement only
- **C126 Moat Comparison**: 🟢 READY — C46 scoring system is comparison-ready
- **C47 Education Academy**: 🟡 NEEDS DESIGN — lesson card component required, content creation budget needed
- **C125 Segment Profitability**: 🟡 NEEDS RESEARCH — similar to C123, needs TW data validation

### Design System Health: 🟡 UPDATE NEEDED
- 5 new components/patterns to document
- 2 existing components need parameter additions
- 1 interaction pattern to formalize

---

*Design Review completed by Design Reviewer. Next update: After Sprint 14 feature implementation (Review Round 31).*
