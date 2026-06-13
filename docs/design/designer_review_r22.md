# Design Review — Round 22

> **Date**: 2026-06-13
> **Reviewer**: Design Reviewer
> **Scope**: Sprint 9 (C98 + C101 + C103 Lite) post-implementation design audit
> **Grade Context**: A (11th consecutive A/A-) — Round 21 upgraded from A- back to A

---

## 1. Sprint 9 Design Assessment

### C103 Lite — First Visit Guide ✅ PASS

**File**: `src/pages/first_visit_guide.py` (48 lines)

| Criterion | Result |
|-----------|--------|
| Uses shared card components | ✅ `_summary_card()` + `_白话_card()` — zero inline HTML |
| PPT-style 2-card layout | ✅ Card 1 ("你將學到什麼") + Card 2 ("關於股識") — clean two-card flow |
| Historian positioning | ✅ Card 2 explicitly states "我們是『公司紀錄者』，不是『股票推薦者』" |
| Session-level persistence | ✅ `st.session_state["first_visit_dismissed"]` with `st.rerun()` |
| Dismiss button | ✅ Centered "我知道了 ✓" with `use_container_width=True` |
| Ten-second test | ✅ A novice can understand the page in <10 seconds |

**Verdict**: Clean implementation. No design issues. This is the gold standard for Sprint 9 — new page, zero inline HTML, uses shared components exclusively.

---

### C101 — Comprehension Check Quiz ⚠️ PASS WITH ISSUES

**File**: `src/pages/comprehension_check.py` (191 lines)

| Criterion | Result |
|-----------|--------|
| Uses shared card components | ⚠️ Mostly — `_info_card()`, `_section_title()`, `_白话_card()` used correctly |
| Quiz result detail cards | ❌ **Inline HTML regression** (lines 151-166) |
| Score summary cards | ✅ Uses `_白话_card()` in 2-column layout |
| Historian disclaimer | ✅ Uses `_historian_disclaimer("general")` from `_helpers.py` |
| Finimize quiz model | ✅ 5 questions, immediate feedback, explanation after each answer |
| YAML-driven content | ✅ `config/comprehension_quiz.yaml` — no hardcoded content in view |

**Issue — D-062 (NEW): Quiz Result Detail Cards Use Inline HTML**
- **Severity**: P2
- **Location**: `comprehension_check.py` lines 151-166
- **Description**: The per-question result cards (showing ✅/❌ status, question text, and explanation) use a manually constructed HTML div with `unsafe_allow_html=True`. This card has a colored `border-left` (green `#27AE60` for correct, red `#E74C3C` for incorrect) and a nested white-background explanation area. This is a new card type (quiz result card) that should be a shared component.
- **Design system gap**: No "quiz result card" component exists in `_router_base.py`. The inline HTML creates a 5th card style variant (info, 白話, summary, subsidiary, quiz-result) that isn't documented.
- **Proposed fix**: Create `_quiz_result_card(is_correct, question_text, explanation)` in `_router_base.py` with standardized styling. Use `#27AE60` / `#E74C3C` border-left colors (matching the design system's positive/negative colors). Add to design system as "quiz result card" variant.
- **Effort**: 0.5-1h

**Issue — D-063 (NEW): Quiz Score Color Logic Duplicated in View Layer**
- **Severity**: P2
- **Location**: `comprehension_check.py` lines 110-124
- **Description**: The score color/emoji/title/desc logic (percentage → color mapping) is hardcoded in the view layer. If this pattern is reused (e.g., in C104 post-narrative quiz), it will be duplicated. This is a minor architecture concern with design implications — the color thresholds (80%/60%) should be consistent across all quiz instances.
- **Proposed fix**: Move to a helper `_get_score_style(percentage)` returning `(color, emoji, title, desc)` dict. Low priority since C104 is not yet scheduled.
- **Effort**: <0.5h

---

### C98 — Event Interpretation Engine ⚠️ PASS WITH ISSUES

**File**: `src/pages/event_dashboard.py` (224 lines, modified)
**Service**: `src/services/event_interpretation_service.py` (123 lines)
**Config**: `config/event_interpretation_templates.yaml` (34 lines, 6 event types)

| Criterion | Result |
|-----------|--------|
| Uses shared card components | ⚠️ Partially — `_summary_card()` and `_info_card()` used for interpretation |
| Key concept display | ❌ **Inline HTML** (lines 110-115) |
| Disclaimer text | ❌ **Inline HTML** (lines 133-137) |
| Adaptive banner | ⚠️ **Inline HTML** (lines 193-204) — pre-existing, not Sprint 9 |
| YAML-driven templates | ✅ `event_interpretation_templates.yaml` — 6 event types, clean separation |
| Service layer separation | ✅ `event_interpretation_service.py` — no Streamlit imports |
| Ten-second test | ✅ Interpretation card + key concept = core message in <10 seconds |
| Historian positioning | ✅ "歷史學家解讀" card + disclaimer text |

**Issue — D-064 (NEW): Key Concept Line Uses Inline HTML**
- **Severity**: P2
- **Location**: `event_dashboard.py` lines 110-115
- **Description**: The "💡 核心概念" line between the interpretation card and the drill-down button uses a bare `<div>` with inline styling (`font-size:0.85rem;color:#5D6D7E`). This is a new "key concept" text style that appears on every event. It's not a card — it's a muted text line — but it should use a shared component or `st.caption()` instead of inline HTML.
- **Design system gap**: No "muted caption" or "key concept" text style is documented. The design system specifies `#7F8C8D` for secondary text and `font-size:0.85rem` for labels — this matches, but the implementation should be consistent.
- **Proposed fix**: Replace with `st.caption(f"💡 核心概念：**{interp['key_concept']}**")` which uses Streamlit's built-in muted text style. Or create a `_key_concept(text)` helper in `_router_base.py`.
- **Effort**: <0.5h

**Issue — D-065 (NEW): Disclaimer Text Uses Inline HTML**
- **Severity**: P2
- **Location**: `event_dashboard.py` lines 133-137
- **Description**: The historian disclaimer below the drill-down interpretation uses inline HTML (`font-size:0.8rem;color:#95A5A6`). This is the same disclaimer pattern as `_historian_disclaimer()` in `_helpers.py` which uses `st.caption()`. The inline HTML creates inconsistency — some disclaimers use `st.caption()`, this one uses inline HTML.
- **Proposed fix**: Replace with `st.caption("⚠️ 以上解讀僅說明事件背景與可能意涵，不構成投資建議。")` or call `_historian_disclaimer("event")` if an event type is added.
- **Effort**: <0.5h

**Issue — D-066 (Pre-existing): Adaptive Banner Uses Inline HTML**
- **Severity**: P2 (pre-existing, not a Sprint 9 regression)
- **Location**: `event_dashboard.py` lines 193-204
- **Description**: The adaptive analysis framework banner uses inline HTML with `background:#EBF5FB` and `border-left:4px solid #3498DB`. This is functionally identical to `_info_card()` but implemented as inline HTML. Pre-existing — not introduced by Sprint 9.
- **Proposed fix**: Replace with `_info_card(title=f"🎯 分析框架：{framework['name']}", content=f"{framework['description']} — {framework['focus']}", icon="🎯")`.
- **Effort**: <0.5h

---

## 2. New Design Issues

| ID | Title | Severity | File | Lines |
|----|-------|----------|------|-------|
| D-062 | Quiz result detail cards use inline HTML | P2 | `comprehension_check.py` | 151-166 |
| D-063 | Quiz score color logic in view layer | P2 | `comprehension_check.py` | 110-124 |
| D-064 | Key concept line uses inline HTML | P2 | `event_dashboard.py` | 110-115 |
| D-065 | Disclaimer text uses inline HTML | P2 | `event_dashboard.py` | 133-137 |
| D-066 | Adaptive banner uses inline HTML (pre-existing) | P2 | `event_dashboard.py` | 193-204 |

**Net inline HTML change from Sprint 9**:
- `first_visit_guide.py`: 0 new (all shared components) ✅
- `comprehension_check.py`: 1 new instance (quiz result cards) ⚠️
- `event_dashboard.py`: 2 new instances (key concept + disclaimer) + 1 pre-existing ⚠️
- **Total new inline HTML**: 3 instances across 2 files

---

## 3. D-003 Regression Check

**D-003**: Inconsistent Card Styling — pages bypass shared components with inline HTML.

### Sprint 9 Regression Summary

| File | Status | Details |
|------|--------|---------|
| `first_visit_guide.py` | ✅ No regression | Uses only `_summary_card()` and `_白话_card()` |
| `comprehension_check.py` | ⚠️ Minor regression | Quiz result cards (lines 151-166) use inline HTML instead of a shared component. The card styling (`background:#F8F9FA`, `border-radius:12px`, `padding:1.2rem`, `border-left:4px solid`) matches the design system, but it's duplicated inline rather than using a component. |
| `event_dashboard.py` | ⚠️ Minor regression | 2 new inline HTML instances (key concept + disclaimer). Neither is a full card — both are single-line text elements. Styling is minimal and matches design system colors. |

### Assessment

The Sprint 9 inline HTML regressions are **minor and structural**, not visual:
- The quiz result card (D-062) is a **new card type** that doesn't have a shared component yet. This is a design system gap, not a developer shortcut.
- The key concept line (D-064) and disclaimer (D-065) are **single-line text elements**, not full cards. They use inline HTML for convenience but match design system colors.
- None of the regressions use non-standard colors or spacing.
- The regressions are fixable with <2h total effort.

**Comparison to Sprint 7/8**: Sprint 7 introduced 150+ lines of inline HTML in `sector_heatmap.py` (D-045/D-046). Sprint 8 fixed all of that. Sprint 9's 3 new instances are a minor blip by comparison.

**D-003 Status**: Still PARTIALLY FIXED. The overall inline HTML count increased slightly (3 new instances) but the trend is manageable. The core issue remains: new card types need shared components before implementation.

---

## 4. Sprint 10 Design Prerequisites

### C34: Company Story Timeline

**Design Pattern Recommendation: Vertical Timeline Card**

For Streamlit, the timeline should use a **vertical card-based layout** (not a Gantt chart, which would require complex Plotly configuration):

```
┌─────────────────────────────────────────────────┐
│  📅 2023年1月                                    │
│  ┌───────────────────────────────────────────┐  │
│  │  🔴 重大事件                               │  │
│  │  「台積電宣布在美設廠」                      │  │
│  │  這意味著台積電將投資 400 億美元在...        │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  📅 2022年6月                                    │
│  ┌───────────────────────────────────────────┐  │
│  │  🟡 注意事件                               │  │
│  │  「營收首次突破 2 兆」                      │  │
│  │  這代表台積電的營收規模達到...              │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  📅 2020年3月                                    │
│  ┌───────────────────────────────────────────┐  │
│  │  🟢 參考事件                               │  │
│  │  「疫情下的營收表現」                      │  │
│  │  全球疫情爆發，但台積電的營收...           │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Components from design system**:
- Card container: `_summary_card()` variant with date header (or new `_timeline_event_card()`)
- Severity badge: emoji-based (🔴/🟡/🟢) — consistent with event dashboard
- Event title: `font-weight:600;color:#2C3E50` (matches design system)
- Event description: `font-size:0.9rem;color:#5D6D7E` (matches design system secondary text)

**Key design decisions**:
1. **Use `_summary_card()` as the base** — the orange/amber border fits the "story" context
2. **Date as card header** — prepend date to title or use as a separate `st.caption()` above each card
3. **Max 5-7 events visible** — use "載入更多" button for additional events (PPT-style: don't show everything)
4. **Time range selector** — use `render_timeline_selector()` from `timeline_controls.py` (already exists from M3)
5. **Sort order** — reverse chronological (newest first), consistent with event dashboard

**New component needed**: `_timeline_event_card(date, severity, title, description)` — a variant of `_summary_card()` with date header and severity-colored border-left.

**Design system update needed**: Document "timeline event card" as a new card variant.

---

### C105: Simple/Detailed Toggle

**Design Pattern Recommendation: Session-State Toggle with Conditional Rendering**

The toggle should be a **prominent but non-intrusive button** in Zone C (main content area), not in the navbar or sidebar:

```
┌─────────────────────────────────────────────────┐
│  [🔰 簡易模式]  [📊 詳細模式]                    │
│  ─────────────────────────────────────────────  │
│  (Content changes based on mode)                │
└─────────────────────────────────────────────────┘
```

**Components from design system**:
- Toggle: `st.columns(2)` with two `st.button()` — one `type="primary"` (active), one `type="secondary"` (inactive)
- State: `st.session_state["content_mode"] = "simple" | "detailed"`
- Placement: Top of Zone C, below section title, above content

**Key design decisions**:
1. **Default to "simple" mode** — aligns with beginner-first philosophy and PPT-style principles
2. **Use `st.session_state` for persistence** — toggle state persists across page reruns
3. **Conditional rendering per section** — each section checks `st.session_state["content_mode"]` and renders simplified or detailed content
4. **Simple mode**: Show only the hero card (summary) + key metrics (白話 cards) — max 3 cards
5. **Detailed mode**: Show all sections — full business card with all 13+ sections
6. **Visual feedback**: Active button uses `type="primary"` (blue), inactive uses `type="secondary"` (gray)

**New component needed**: `_content_toggle(key="content_mode")` — a reusable toggle that renders the two buttons and returns the current mode. Should be placed in `_router_base.py`.

**Design system update needed**: Document "content toggle" as a new interaction pattern. Specify that simple mode = max 3 cards per page, detailed mode = all sections visible.

**Competitor reference**: Finimize's ELI5 toggle is the gold standard — a single toggle at the top of each article that switches between "simple" and "detailed" views. Stash uses a similar pattern with "Learn More" expandable sections.

---

## 5. Design Grade Recommendation

### Recommendation: **Maintain A**

**Justification**:

**Positive factors**:
1. **C103 Lite is exemplary** — zero inline HTML, uses shared components exclusively, clean 2-card PPT-style layout. This is the best-implemented new page in recent sprints.
2. **C101 is well-structured** — YAML-driven content, service layer separation, uses shared components for 80% of UI. The inline HTML regression is limited to one new card type (quiz result) that lacks a shared component.
3. **C98 is architecturally sound** — YAML-driven templates, service layer with no Streamlit imports, graceful fallback for unknown event types. The inline HTML regressions are minor text elements, not full cards.
4. **Design system compliance** — all colors, spacing, and typography match the design system. No non-standard colors or spacing introduced.
5. **Net inline HTML trend** — Sprint 8 removed 150+ lines. Sprint 9 added ~20 lines across 3 instances. The trend is still positive.

**Negative factors**:
1. **3 new inline HTML instances** — minor regressions in `comprehension_check.py` and `event_dashboard.py`. Not grade-blocking but need to be addressed.
2. **New card type without component** — quiz result card (D-062) should have been added to `_router_base.py` before implementation. This is a process issue, not a visual issue.

**Grade trajectory**: A (R19) → A- (R20) → A (R21) → **A (R22, maintained)**

**Condition**: The 3 new inline HTML instances (D-062, D-064, D-065) should be fixed in Sprint 10 as part of the "debt clearance" work. If they remain unfixed for 2+ sprints, consider downgrading to A-.

---

## 6. Design System Updates Needed

### New Components to Add to `_router_base.py`

| Component | Purpose | Sprint | Priority |
|-----------|---------|--------|----------|
| `_quiz_result_card(is_correct, question_text, explanation)` | Quiz result detail card with colored border | Sprint 10 | P2 |
| `_timeline_event_card(date, severity, title, description)` | Timeline event card for C34 | Sprint 10 | P1 |
| `_content_toggle(key, labels)` | Simple/Detailed mode toggle for C105 | Sprint 10 | P1 |
| `_key_concept(text)` | Muted key concept text line | Sprint 10 | P2 |

### New Component Variants to Document

| Variant | Base Component | Difference | Document Section |
|---------|---------------|------------|-----------------|
| Quiz result card (correct) | `_summary_card` | Green `#27AE60` border | Cards → Quiz variants |
| Quiz result card (incorrect) | `_summary_card` | Red `#E74C3C` border | Cards → Quiz variants |
| Timeline event card | `_summary_card` | Date header + severity border | Cards → Timeline variants |

### New Interaction Patterns to Document

| Pattern | Description | Document Section |
|---------|-------------|-----------------|
| Content toggle | Simple/Detailed mode switch | Interaction → Toggle patterns |
| Quiz flow | Question → Answer → Feedback → Next | Interaction → Quiz patterns |
| Timeline flow | Date-grouped events, reverse chronological | Interaction → Timeline patterns |

### Color System Updates

No new colors needed for Sprint 10. The existing color system covers all new components:
- Quiz correct: `#27AE60` (positive green, already in system)
- Quiz incorrect: `#E74C3C` (negative red, already in system)
- Timeline events: `#F39C12` (warning orange, already in system for summary cards)

---

## 7. Summary of All Open Design Issues

| ID | Title | Severity | Status | Sprint |
|----|-------|----------|--------|--------|
| D-003 | Inconsistent card styling | P1 | Partially fixed | Ongoing |
| D-005 | Business card page overload risk | P1 | Mitigated | Ongoing |
| D-006 | Mobile responsiveness gaps | P1 | Open | Deferred |
| D-007 | No discovery mechanism | P2 | Open | Sprint 12 |
| D-008 | Loading state inconsistency | P2 | Open | Deferred |
| D-009 | Error state inconsistency | P2 | Open | Deferred |
| D-010 | Watchlist non-PPT layout | P2 | Open | Deferred |
| D-011 | Category browser dense tables | P2 | Open | Deferred |
| D-012 | No glossary/tooltip system | P2 | Open | Sprint 12 (C33) |
| D-015 | No structured learning path | P2 | Open | Deferred |
| D-032 | No progressive disclosure | P2 | Mitigated | Ongoing |
| D-033 | No standardized empty state | P2 | Open | Deferred |
| D-035 | C41 peer cards inline HTML | P2 | Open | Sprint 10 |
| D-036 | C44 risk cards non-standard bg | P2 | Open | Sprint 10 |
| D-038 | C41 API in view layer | P2 | Open | Sprint 10 |
| D-039 | No standardized section header | P2 | Open | Sprint 10 |
| D-040 | No standardized disclaimer | P2 | Open | Sprint 10 |
| D-042 | Health mini-cards non-standard | P2 | Open | Sprint 10 |
| D-043 | Dividend table inline HTML | P2 | Open | Sprint 10 |
| D-045 | Sector grid non-standard styling | P2 | Open | Sprint 10 |
| D-048 | Share button non-functional JS | P2 | Open | Sprint 10 |
| D-051 | ETF browser table-like rows | P2 | Open | Sprint 10 |
| D-052 | `_subsidiary_card()` non-standard | P2 | Documented | Sprint 10 |
| D-053 | `_count_label()` undocumented | P2 | Documented | Sprint 10 |
| **D-062** | **Quiz result cards inline HTML** | **P2** | **NEW** | **Sprint 10** |
| **D-063** | **Quiz score logic in view** | **P2** | **NEW** | **Sprint 10** |
| **D-064** | **Key concept inline HTML** | **P2** | **NEW** | **Sprint 10** |
| **D-065** | **Disclaimer inline HTML** | **P2** | **NEW** | **Sprint 10** |
| **D-066** | **Adaptive banner inline HTML** | **P2** | **Pre-existing** | **Sprint 10** |

**Total**: 30 open design issues (3 P1 + 27 P2), 5 new this round.

---

*Design Review Round 22 — 2026-06-13*
*Next review: Round 23 (after Sprint 10)*
