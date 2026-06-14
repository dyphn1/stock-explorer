# Design Review — Round 44 (2026-06-14)

> **Reviewer**: Design Reviewer
> **Sprint**: Sprint 20 (C167 ✅, C163 🔧, C40 🔧)
> **Current Design Grade**: A- (downgraded from A in Round 41 due to D-003 regression in C167)
> **Theme**: Sprint 20 Mid-Cycle — C167 Design Debt assessment + C163/C40 prerequisite review

---

## C167 Design Assessment

### ScreenerExplanationProvider UI

The `ScreenerExplanationProvider` service layer (357 lines) is architecturally excellent — pure Python, zero Streamlit imports, implements `ExplanationProvider` protocol correctly, and all templates use historian tone with mandatory disclaimer. The tone QA issue (D-123) was fixed in Round 42 (commit `75cc980`), replacing "建議" with acceptable alternatives.

However, the **page-level UI** in `stock_screener.py` (309 lines) has significant design issues:

**Preset Cards (lines 106–160) — 3 inline HTML blocks:**
Each of the 3 preset cards (穩定收息, 成長潛力, 便宜估值) uses `unsafe_allow_html=True` with manually constructed `<div>` cards. These replicate the exact styling of `_白话_card()` / `_info_card()` — `border-radius:12px`, `padding:1.2rem`, `background:#F8F9FA` — but with custom interactive card behavior (selection state via `border_color` and `bg_color` toggling). The selection-state pattern (green/blue/purple border + tinted background when selected) is a genuine UX enhancement over static cards, but it should be implemented via a shared `_selectable_card()` helper in `_router_base.py` rather than inline HTML.

Key issues:
- Line 104: Uses non-standard `#BDC3C7` for unselected border (not in design system)
- Line 105: Uses non-standard `#E8F8F5` for selected dividend background (not in design system)
- Line 124: Uses non-standard `#EBF5FB` for selected growth background (not in design system)
- Line 125: Uses `#3498DB` for selected growth border (this IS in the design system as primary accent — the only color that matches)
- Line 144: Uses non-standard `#9B59B6` for selected value border (not in design system — purple is not in the design system at all)
- Line 145: Uses non-standard `#F5EEF8` for selected value background (not in design system)

**Result Cards (lines 279–294) — 1 inline HTML block:**
The result card at line 279 uses `unsafe_allow_html=True` with inline HTML that IS consistent with the design system (`background:#F8F9FA`, `border-radius:12px`, `border-left:4px solid #3498DB`). However, it bypasses `_info_card()` / `_白话_card()` entirely. The card renders stock ID, industry, name, and key metric — this should be a shared `_result_card()` helper.

**Summary: 4 `unsafe_allow_html` instances in stock_screener.py, all D-003 regressions. D-123 (tone QA) is fixed. D-121/D-122 remain open.**

### D-121 (YAML not loaded)

**Status**: ❌ **STILL OPEN** — Confirmed by file system check.

The `screener_templates.yaml` file does not exist anywhere in the codebase. All templates (`_DIVIDEND_TEMPLATES`, `_GROWTH_TEMPLATES`, `_VALUE_TEMPLATES`, `_CUSTOM_FILTER_TEMPLATES`, `_FALLBACK_TEMPLATE`) are hardcoded as Python dicts/lines in `screener_explanation_provider.py` (lines 27–79). This is a D-121 violation — the handoff explicitly states "D-121 YAML migration → Sprint 21 infrastructure."

**Impact**: Medium. Hardcoded templates are harder for non-developers to edit, and the content cannot be updated without a code deployment. The templates are also not reusable by other services.

**Effort**: 1-2h (extract to YAML, add loader in `__init__` or module level).

### D-122 (unsafe_allow_html)

**Status**: ❌ **STILL OPEN** — 4 instances confirmed in `stock_screener.py`.

| Line | Type | Description |
|------|------|-------------|
| 115 | Preset card | 穩定收息 card (inline HTML with selection state) |
| 135 | Preset card | 成長潛力 card (inline HTML with selection state) |
| 155 | Preset card | 便宜估值 card (inline HTML with selection state) |
| 294 | Result card | Stock result card (inline HTML, design-system-consistent but bypasses shared components) |

**Effort**: 1-2h (create `_selectable_card()` and `_result_card()` helpers in `_router_base.py`).

### D-123 (tone QA — fixed)

**Status**: ✅ **FIXED** in Round 42 (commit `75cc980`).

The `建議` keyword was removed from the disclaimer and implication text. The disclaimer now reads "篩選結果僅供學習參考，不構成投資諮詢" (line 20). All tone QA tests pass. No further action needed.

### New D-003 Regressions

**No NEW D-003 regressions found in C167 files beyond D-121/D-122.**

The 4 `unsafe_allow_html` instances in `stock_screener.py` were introduced as part of C167 and are already tracked as D-122. The service layer (`screener_explanation_provider.py`) is pure Python with zero Streamlit imports — no D-003 risk there.

However, one **potential future regression** was identified: The `_build_screener_implication()` function (lines 248–284) returns plain text that is rendered via `_summary_card()` in the page layer (line 298–303). This is correct — the service layer produces text, the page layer renders it via shared components. This separation is good and should be maintained.

**D-003 net assessment for C167**: The feature introduced 4 inline HTML blocks (all in `stock_screener.py`). No inline HTML in the service layer. The regression is contained to the page file and is fixable with 2 new shared components.

---

## C163 + C40 Design Prerequisites

### C163 Full-Page Soft Gate UX

The design direction from `docs/design/discuss_c163_c40.md` is well-specified and ready for implementation. Key design decisions confirmed:

**Format**: Full-page gate (not modal, not slide-over) — ✅ Correct. This follows the existing pattern of C103 (First Visit Guide) and C47 (Academy) as standalone router pages. No zone mixing.

**Content**: 4 micro-lessons with PPT-style compliance — ✅ Well-specified. Each lesson follows one-key-point-per-screen, max 40 characters for key point, charts > 60% of area.

**Soft gate with skip**: ✅ Critical UX requirement. The "跳過教學" link must be visible on every lesson screen.

**Design prerequisites for C163 implementation**:

1. **New component needed**: `_lesson_card()` — a full-width card for lesson content with title, visual area, analogy text, and navigation controls. This is NOT the same as existing card types — it needs a large visual area (> 60% of card space) and bottom navigation (progress dots + Next button).

2. **New component needed**: `_progress_dots(current, total)` — renders dot indicators for lesson progress. Simple component but needs to be shared for consistent styling.

3. **Gateway lessons content**: `gateway_lessons.yaml` — does not exist yet. Must be created with 4 lessons covering: (1) What is a stock, (2) How companies make money, (3) Key metrics (P/E + ROE), (4) What is Stock Explorer (historian positioning). **Content creation is 3-4h effort** and should start in parallel with coding.

4. **Session state**: Must use existing `first_visit_dismissed` key for backward compatibility with C103. C103's `first_visit_guide.py` must be **deleted** (not just disabled) to avoid import conflicts.

5. **Sidebar behavior**: Zone B (sidebar) should be hidden or dimmed during the gate experience. The gate is a full-page experience — showing the sidebar would distract from the learning flow.

### C40 Sidebar Toggle Design

**Toggle placement**: Zone B sidebar, above search box — ✅ Correct. This follows the design system's Zone A rule ("Must NOT contain: search box, filters, or any interactive controls") and aligns with competitor patterns (Sharesies places level selector in main navigation area).

**Toggle component**: `st.radio` with "🌱 新手模式" / "🔬 進階模式" — ✅ Better than `st.toggle` because both options are always visible.

**Scope**: All stock pages — ✅ The per-page spec in `discuss_c163_c40.md` is comprehensive, covering Business Card, Operation Checkup, Financial Health, Peer Comparison, Group Structure, Category Browse, and ETF Zone.

**Design prerequisites for C40 implementation**:

1. **New component needed**: `_beginner_banner()` — a single-line banner for the top of Zone C in beginner mode. Uses `#FEF9E7` background (warning yellow, already in design system). Text: "🌱 新手模式：目前顯示簡化版本，切換至進階模式可查看更" (truncated for brevity).

2. **New component needed**: `_advanced_content_expander(label)` — a collapsed expander for hidden advanced sections. Label: "🔬 🔰 進階內容（切換至進階模式即可查看）". This teaches users that more content exists.

3. **Per-page beginner mode specs**: Already defined in `discuss_c163_c40.md` (Section "What Changes in Beginner Mode"). Each page shows 3-5 key sections in beginner mode. This spec must be implemented consistently across all pages.

4. **State persistence**: `st.session_state["user_experience_level"]` with 2 levels only (beginner/expert). No URL params. Default: beginner.

5. **Instant switching**: Mode change must be instant (< 0.5s), no data reload. Only DOM visibility changes.

### Design System Updates Needed

| Component | Action | Priority |
|-----------|--------|----------|
| `_lesson_card()` | **Create new** — full-width lesson card with visual area + navigation | P0 (C163 blocker) |
| `_progress_dots()` | **Create new** — lesson progress dot indicators | P0 (C163 blocker) |
| `_beginner_banner()` | **Create new** — beginner mode in-page banner | P0 (C40 blocker) |
| `_advanced_content_expander()` | **Create new** — hidden advanced content expander | P0 (C40 blocker) |
| `_selectable_card()` | **Create new** — card with selection state (for C167 fix + future use) | P1 (D-122 fix) |
| `_result_card()` | **Create new** — screener result card (for C167 fix) | P1 (D-122 fix) |
| `_subsidiary_card()` | **Document existing** — "entity card" variant with white background | P2 (D-052) |
| `_count_label()` | **Document existing** — "muted label" variant | P2 (D-053) |
| `_mini_score_card()` | **Document existing** — compact score card with score-based border | P2 (D-082 resolved, needs doc) |
| `_so_what_box()` | **Document existing** — implication callout box | P2 (D-119) |
| Color palette | **Document** — add `#9B59B6` (purple) if C167 preset cards are kept as-is, OR remove purple and use existing colors | P1 (D-122) |

---

## Design Improvement Proposals

| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-128 | Create `_selectable_card()` helper in `_router_base.py` to replace 3 inline HTML preset cards in `stock_screener.py` | Medium | 1-1.5h |
| D-129 | Create `_result_card()` helper in `_router_base.py` to replace inline HTML result card in `stock_screener.py` | Medium | 0.5-1h |
| D-130 | Extract hardcoded templates from `screener_explanation_provider.py` to `screener_templates.yaml` (D-121 fix) | Medium | 1-2h |
| D-131 | Create `_lesson_card()` and `_progress_dots()` helpers for C163 gate page | High | 1.5-2h |
| D-132 | Create `_beginner_banner()` and `_advanced_content_expander()` helpers for C40 mode | High | 1-1.5h |
| D-133 | Remove purple (`#9B59B6`) from C167 preset cards; replace with design system colors (blue `#3498DB` for growth, keep green `#27AE60` for dividend, use amber `#F39C12` for value instead of purple) | Low | 0.5h |
| D-134 | Delete `first_visit_guide.py` (C103) when C163 is implemented; remove "新手導覽" from router | Medium | 0.25h |
| D-135 | Write `gateway_lessons.yaml` content (4 lessons) before C163 coding begins | High | 3-4h |
| D-136 | Document `_subsidiary_card`, `_count_label`, `_mini_score_card`, `_so_what_box` in design system | Low | 0.5-1h |

---

## Design System Updates Required

1. **New card type: `_lesson_card()`** — Full-width card for educational content. Visual area > 60% of card space. Bottom navigation slot for Next button + progress dots. Background: `#FFF8F0` (tip/warning style) to distinguish from info cards.

2. **New card type: `_selectable_card()`** — Card with selection state. Parameters: `title`, `subtitle`, `icon`, `is_selected`, `selected_color`. Unselected: `background:#F8F9FA`, `border:2px solid #BDC3C7`. Selected: `background:{color}15`, `border:2px solid {color}`. This replaces the inline HTML preset cards in C167 and provides a reusable pattern for future selectable card grids.

3. **New card type: `_result_card()`** — Compact result card for screener results. Parameters: `stock_id`, `stock_name`, `industry`, `key_metric`. Uses standard card styling (`background:#F8F9FA`, `border-left:4px solid #3498DB`).

4. **New component: `_progress_dots(current, total)`** — Renders dot indicators for multi-step flows. Active dot: `#3498DB` (primary accent). Inactive dot: `#BDC3C7`. Used by C163 gate and future multi-step flows.

5. **New component: `_beginner_banner()`** — Single-line banner for beginner mode. `background:#FEF9E7`, `color:#2C3E50`. Text + link to switch mode.

6. **New component: `_advanced_content_expander()`** — Collapsed expander for hidden advanced sections in beginner mode. Label includes "切換至進階模式" call-to-action.

7. **Color system update**: Either (a) add `#9B59B6` (purple) to the color palette as "secondary accent" for the value preset card, OR (b) replace purple with an existing color. **Recommendation**: Use `#F39C12` (amber/orange) for the value preset — it's the only primary card color not yet used by the other two presets (green for dividend, blue for growth). This keeps the preset cards within the existing 3-color system.

8. **YAML data files**: Add `screener_templates.yaml` (for D-121 fix) and `gateway_lessons.yaml` (for C163) to the design system's data architecture section.

---

## Top 3 Design Recommendations

1. **🔴 Create shared components BEFORE coding C163/C40 — not during.**
   The single biggest design risk for Sprint 20 is the same pattern that caused D-121/D-122: implementing page-specific UI with inline HTML because shared components don't exist yet. Before C163 coding begins, create `_lesson_card()`, `_progress_dots()`, `_beginner_banner()`, and `_advanced_content_expander()` in `_router_base.py`. Before C40 coding begins, write the per-page beginner mode spec. **Estimated total: 3-4h of design-system work that will prevent 5-8h of inline HTML debt.**

2. **🟡 Fix C167 inline HTML (D-121/D-122) as Sprint 21 infrastructure — not optional debt.**
   The 4 `unsafe_allow_html` blocks in `stock_screener.py` are contained and fixable. Create `_selectable_card()` and `_result_card()` helpers, extract templates to YAML, and replace all inline HTML. This should be Day 1 Sprint 20 infrastructure work (alongside D-120 benchmark extraction). **Effort: 2-3h. Impact: Eliminates the D-003 regression that caused the A- downgrade.**

3. **🟢 Write `gateway_lessons.yaml` content NOW — in parallel with C167 debt fixes.**
   The C163 gate page architecture (`experience_service.py`, router changes, shared components) can be built by the developer while the PM/Designer writes the 4 lesson content in YAML. These are parallelizable work streams. The content is the harder part — each lesson must pass the ten-second test, use ≤ 40 characters for the key point, and include a beginner-friendly analogy. **Start content creation immediately; don't wait for the developer to finish the gate page scaffolding.**

---

## Grade Assessment

### Current Grade: **A-** (maintained from Round 41)

**Justification**: C167's D-121/D-122 inline HTML regressions remain the sole reason for the A- grade. The service layer is architecturally excellent. D-123 (tone QA) is fixed. No new regressions found. C163 and C40 design prerequisites are well-specified and ready for implementation.

**Grade trajectory**: A (R34) → A (R37) → A- (R41, C167 regression) → **A- (R44, maintained)**

**Upgrade path to A**: Fix D-121/D-122 (2-3h) in Sprint 21 infrastructure. If C163/C40 are implemented with shared components (no new inline HTML), the grade returns to A.

**Downgrade risk to B+**: If C163/C40 are implemented with inline HTML (new D-003 regressions on top of existing D-121/D-122), the grade drops to B+. This is the #1 risk for Sprint 20.

---

*Reviewer: Design Reviewer*
*Date: 2026-06-14*
*Next review: After Sprint 20 completion (C163 + C40 implementation)*
