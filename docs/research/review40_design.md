# Design Review Round 40 — Stock Explorer

> **Reviewer**: Design Reviewer
> **Date**: 2026-06-14
> **Scope**: Sprint 19 design verification (C147 Historical Pattern, C140 Case Study Library, D-113 tests, D-114 inline HTML fix), Sprint 20 design readiness
> **Current Design Grade**: A (6 consecutive rounds since R34)

---

## 1. Sprint 19 Design Verification

### C147: Historical Event Pattern (`_historical_pattern.py`)

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Shared Components** | ✅ Pass | Uses `_section_title()` and `_info_card()` from `_router_base.py` |
| **Inline HTML** | ✅ Pass | Zero `unsafe_allow_html`, zero `st.html()`, zero raw `<div>`/`<span>` |
| **Section Title** | ✅ Pass | Uses `_section_title("📊 歷史模式")` |
| **Card Styling** | ✅ Pass | All event matches rendered via `_info_card()` with direction emoji |
| **Disclaimer** | ✅ Pass | Uses `st.caption()` for historian disclaimer |
| **Empty State** | ✅ Pass | Uses `_info_card()` for "no data" state |
| **Ten-Second Test** | ✅ Pass | Event type → outcome summary → individual event cards with date/description/outcome. Scannable. |
| **PPT-Style** | ✅ Pass | One key point per section: "when similar events happened, what was the result" |

**Assessment**: Clean implementation. The `_info_card("", card_content, direction_emoji)` pattern (empty title, content as body) is a valid use of the component. The direction emoji mapping (positive→📈, negative→📉, mixed→↔️) is consistent with the design system's color/emoji conventions. No issues found.

### C140: Case Study Library (`case_study_library.py`)

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Shared Components** | ✅ Pass | Uses `_info_card()`, `_section_title()`, `_count_label()` from `_router_base.py` |
| **Inline HTML** | ✅ Pass | Zero `unsafe_allow_html`, zero `st.html()`, zero raw HTML |
| **Section Title** | ✅ Pass | Uses `_section_title()` for "📋 事件摘要", "🎓 歷史啟示", "📈 相關個股" |
| **Card Styling** | ✅ Pass | Historian positioning card uses `_info_card()`; case study cards use `st.container()` + `st.markdown()` + `st.caption()` + `st.button()` |
| **Disclaimer** | ✅ Pass | Uses `_historian_disclaimer("general")` from `_helpers.py` |
| **Empty State** | ✅ Pass | Uses `st.info()` for "no results" state |
| **Ten-Second Test** | ✅ Pass | Page title → historian positioning card → filters → card grid. Clear hierarchy. |
| **PPT-Style** | ✅ Pass | One key point: "browse historical case studies from a historian's perspective" |

**Assessment**: Well-designed new page. The `_render_case_study_card()` function uses `st.container()` with `st.markdown()`/`st.caption()`/`st.button()` instead of a shared card component — this is acceptable for a grid card that needs compact layout (title + caption + summary + tags + button). The `_render_case_study_detail()` view uses `_section_title()` consistently. The filter UI (`st.selectbox` in `st.columns(2)`) is clean. No issues found.

### D-114: Inline HTML Fix (`_health.py`)

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Inline HTML Removed** | ✅ Pass | `_health.py` has zero `unsafe_allow_html` usages |
| **Shared Components** | ✅ Pass | Uses `_info_card()`, `_explain_button()`, `_mini_score_card()` from `_router_base.py` |
| **Risk Dimension Cards** | ✅ Pass | `_render_risk_dimension()` in `_helpers.py` uses `background:#F8F9FA` (D-036 resolved) |
| **Section Title** | ✅ Pass | Uses `st.markdown("### 🏥 公司健康狀況")` — **see D-117 below** |

**Assessment**: D-114 fix confirmed. The `_health.py` file is clean — all shared components used correctly, zero inline HTML regressions.

### D-113: Tests

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Test Coverage** | ✅ Pass | Pattern detector and case study library services have test coverage |
| **Design Impact** | N/A | Tests don't directly affect design, but ensure design behavior is preserved |

---

## 2. New Design Debt from Sprint 19 (D-117 onwards)

### D-117: `_health.py` Uses Raw `st.markdown("### 🏥 公司健康狀況")` Instead of `_section_title()`

- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: `_render_health()` at line 184 uses `st.markdown("### 🏥 公司健康狀況")` instead of `_section_title("🏥 公司健康狀況")`. This is the only section header in `_health.py` and it bypasses the `_section_title()` helper's emoji auto-detection and consistent formatting. While the result looks identical (the emoji is already present), it creates an inconsistency with the rest of the codebase where `_section_title()` is the standard.
- **Affected Files**: `src/pages/business_card/_sections/_health.py` line 184
- **Proposed Fix**: Replace with `_section_title("🏥 公司健康狀況")`.
- **Effort**: <0.25h (one-line change)

### D-118: `_historical_pattern.py` Uses `_info_card()` with Empty Title for Event Matches

- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: The event match cards in `_render_historical_pattern()` (line 54) call `_info_card("", card_content, direction_emoji)` with an empty title string. This renders the card with an empty title div (the label div still renders but with no text). While visually acceptable (the emoji icon + content body is sufficient), it's a semantic misuse of `_info_card()` which expects a non-empty title. This could cause issues if the card styling changes (e.g., if title-specific margins are added).
- **Affected Files**: `src/pages/business_card/_sections/_historical_pattern.py` line 54
- **Proposed Fix**: Either (a) pass the match date as the title: `_info_card(match.date, card_content, direction_emoji)`, or (b) create a dedicated `_event_match_card(date, description, outcome, direction)` helper in `_router_base.py` for this pattern.
- **Effort**: 0.25-0.5h
- **Note**: This is a minor semantic issue. The current rendering is visually correct.

### D-119: `_so_what_box()` Component Not Documented in Design System

- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: The `_so_what_box()` component in `_router_base.py` (lines 184-216) is a new "So What?" implication callout box introduced in Sprint 19 (C149). It uses a distinct visual style (`background:#F0F7FF`, `border-left:4px solid #2980B9`) that differs from all other card types. It is used in `_story.py` (line 53) but is not documented in the design system. The component represents a new card variant: "implication callout" — a dedicated visual callout that answers "What does this mean?" using historian tone.
- **Affected Files**: `src/pages/_router_base.py` lines 184-216, `src/pages/business_card/_sections/_story.py` line 53
- **Proposed Fix**: Document in `docs/design/design_system.md` as a new "Implication Callout" card variant. Add to the card types table in Section 3.3.
- **Effort**: 0.25h (documentation update)
- **Design System Spec**:
```html
<!-- Implication callout (blue background, historian tone) -->
<div style="background:#F0F7FF;border-radius:12px;padding:1.2rem;border-left:4px solid #2980B9;margin:0.8rem 0 0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">🧭 所以呢？</div>
    <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;line-height:1.7;">{synthesized_implications}</div>
</div>
```

### D-120: `_summary.py` Benchmark Duplication (D-109) Still Unresolved — Now 80+ Lines

- **Severity**: P2
- **Added**: 2026-06-14 (escalation of D-109)
- **Source**: Design Review Round 40
- **Description**: D-109 identified ~100 lines of benchmark data fetching and metric computation in `_summary.py` (lines 188-294) that duplicates `_fetch_benchmark_health_scores()` in `_health.py` (lines 46-163). Both functions: (1) look up `INDUSTRY_BENCHMARKS` by industry, (2) fetch benchmark financial data via `client.get_*()`, (3) compute gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe, (4) call `compute_health_scores()`. The duplication has grown — `_summary.py` now has 107 lines of benchmark logic (lines 188-294) vs `_health.py`'s 117 lines (46-163). The `_summary.py` version also includes the comparison rendering logic (lines 276-294) which `_health.py` doesn't have, but the data fetching and metric computation are identical.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` lines 188-294, `src/pages/business_card/_sections/_health.py` lines 46-163
- **Proposed Fix**: Extract benchmark health score fetching into a shared service function (e.g., `health_scoring.get_benchmark_scores(client, industry, stock_id)`). Both `_health.py` and `_summary.py` call this function. The comparison rendering logic in `_summary.py` can remain as-is.
- **Effort**: 1-2h
- **Note**: This is a D-003 regression (duplicated logic across files) and also an architecture debt item. The architect's review (D-107) identified the same issue.

---

## 3. Design Grade Assessment

### Recommendation: **A** (maintained, 7th consecutive A since R34)

**Justification:**

Sprint 19 delivered 4 changes with excellent design discipline:

1. **C147 Historical Pattern**: Zero inline HTML, uses `_section_title()` and `_info_card()` correctly, proper disclaimer via `st.caption()`. Clean empty state. The direction emoji mapping is consistent with design system conventions.

2. **C140 Case Study Library**: Zero inline HTML, uses `_info_card()`, `_section_title()`, `_count_label()` correctly. The `_render_case_study_card()` uses `st.container()` + native Streamlit components for compact grid cards — acceptable pattern. Detail view uses `_section_title()` consistently. Proper `_historian_disclaimer()` usage.

3. **D-114 Inline HTML Fix**: Confirmed — `_health.py` has zero `unsafe_allow_html` usages. All shared components used correctly.

4. **D-113 Tests**: Test coverage for new services ensures design behavior is preserved.

**New issues identified (4):**
- D-117: `_health.py` raw `st.markdown` header (P2, <0.25h)
- D-118: `_info_card()` with empty title (P2, 0.25-0.5h)
- D-119: `_so_what_box()` undocumented (P2, 0.25h)
- D-120: Benchmark duplication escalation (P2, 1-2h)

All 4 new issues are P2 (optimization). None are regressions — they're minor consistency issues in new code. No P0 or P1 issues introduced.

**Remaining open P1 issues (3, unchanged):**
- D-003: Inconsistent card styling — `_helpers.py` still has 4 card functions with inline HTML
- D-005: Business Card page overload — mitigated by C105 toggle
- D-006: Mobile responsiveness — Streamlit limitation

**Net assessment**: Sprint 19 continues the strong design discipline established over the last 7 rounds. Zero inline HTML regressions. All new features use shared components from `_router_base.py`. The 4 new P2 issues are minor and don't block the A grade.

**Grade trajectory**: A (R34) → A (R37) → **A (R40, maintained)**

---

## 4. Sprint 20 Design Readiness

### Planned Features

| Feature | Design Complexity | Shared Components Needed | Design Risk |
|---------|------------------|-------------------------|-------------|
| **C167: AI Screener Explanations** | Medium | `_explain_button()`, `_info_card()`, `_白话_card()` | Low — uses existing components |
| **C163: Learn First Gate** | High | New `_onboarding_card()` or `_summary_card()` variant | Medium — new interaction pattern |
| **C40: Beginner/Expert Mode** | High | C105 toggle exists; needs mode-aware section rendering | Medium — builds on C105 pattern |

### C167: AI Screener Explanations

**Design Prerequisites**: ✅ Ready
- The `_explain_button()` component in `_router_base.py` already renders a 💡 popover with metric explanations
- The `TemplateExplanationProvider` (D5) provides template-based explanations
- The `_info_card()` component can wrap explanation results
- **No new components needed** — wire existing `_explain_button()` to screener results

**Design Spec** (if not already defined):
- Each screener result row should have a 💡 button that opens a popover with the explanation
- Use `_explain_button(metric_name, metric_value, key_prefix="screener")` for each metric
- Explanation text should use historian tone: "這家公司ROE為25%，表示每100元股東資金賺25元"
- Source badge: "📊 系統估算" for template, "🤖 AI 分析" for future LLM

### C163: Learn First Gate

**Design Prerequisites**: ⚠️ Needs Design Work
- **New component needed**: `_onboarding_card()` or `_first_visit_card()` in `_router_base.py`
- The C103 first visit guide (Sprint 9) has a 2-card design spec in `current_problems.md` lines 786-853
- C163 is a more comprehensive version — needs a multi-step card flow with progress indicator
- **Recommendation**: Before coding starts, create the `_onboarding_card(title, content, step, total_steps)` helper in `_router_base.py` with standardized styling (use `_summary_card()` as base with `#FFF8F0` background)

**Design Spec**:
```
┌─────────────────────────────────────────────────┐
│  👋 歡迎來到股識！                                │
│                                                 │
│  這是一個「認識公司」的工具，不是投資建議。        │
│                                                 │
│  我們用歷史學家的角度，告訴你：                    │
│  • 這家公司是做什麼的                             │
│  • 它最近發生了什麼事                             │
│  • 它的財務狀況如何                               │
│                                                 │
│  我們不會告訴你「該買」或「該賣」。               │
│                                                 │
│  步驟 1/3                                        │
│                                                 │
│  [繼續 →]                                        │
└─────────────────────────────────────────────────┘
```

**Components needed**:
1. `_onboarding_card(title, content, step, total_steps)` — card container with progress indicator
2. Navigation: `st.button("繼續 →")` with `use_container_width=True`
3. Dismiss: `st.button("跳過導覽", type="secondary")`
4. Session state: `session_state["onboarding_step"]` and `session_state["onboarding_complete"]`

### C40: Beginner/Expert Mode

**Design Prerequisites**: ✅ Mostly Ready
- C105 Simple/Detailed Toggle already implements the toggle pattern
- C40 extends this to a full "mode" concept with beginner/expert defaults
- **No new components needed** — extends existing C105 toggle

**Design Spec**:
- Replace C105's boolean toggle with a `st.radio()` or `st.segmented_control()` with "初學者" / "進階" options
- Beginner mode: shows only hero sections (story card, key metrics, health summary) + `_so_what_box()`
- Expert mode: shows all sections expanded (current default)
- Persist in `session_state["user_mode"]`
- The mode should affect: (1) which sections are visible, (2) how much detail is shown in each section, (3) whether glossary tooltips are auto-shown

**Design Risk**: Medium — the mode concept needs careful scoping to avoid becoming a "show/hide all" toggle. Each section should have a clear "beginner view" and "expert view" variant.

---

## 5. Design System Update Recommendations

The following components need to be added to `docs/design/design_system.md`:

### 5.1 New Component: So What Box (D-119)

Add to Section 3.3 Cards:

```html
<!-- So What implication callout (blue background) -->
<div style="background:#F0F7FF;border-radius:12px;padding:1.2rem;border-left:4px solid #2980B9;margin:0.8rem 0 0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">🧭 所以呢？</div>
    <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;line-height:1.7;">{synthesized_implications}</div>
</div>
```

**Usage**: Below delta sections, when 2+ active deltas exist. Answers "What does this mean?" in historian tone.

### 5.2 New Component: Onboarding Card (C163 — For Sprint 20)

Add to Section 3.3 Cards:

```html
<!-- Onboarding/first visit card -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.5rem;border-left:4px solid #F39C12;margin:1rem 0;">
    <div style="font-size:1.2rem;font-weight:700;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.8;">{content}</div>
    <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.5rem;">步驟 {step}/{total}</div>
</div>
```

### 5.3 Updated Component Count

| Component | Location | Status | Design System |
|-----------|----------|--------|---------------|
| `_白话_card()` | `_router_base.py` | ✅ Documented | Section 3.3 |
| `_info_card()` | `_router_base.py` | ✅ Documented | Section 3.3 |
| `_summary_card()` | `_router_base.py` | ✅ Documented | Section 3.3 |
| `_mini_score_card()` | `_router_base.py` | ✅ Documented | Section 3.3 |
| `_subsidiary_card()` | `_router_base.py` | ⚠️ Needs doc | Round 21 identified |
| `_count_label()` | `_router_base.py` | ⚠️ Needs doc | Round 21 identified |
| `_so_what_box()` | `_router_base.py` | ❌ Missing | **D-119 — add this round** |
| `_explain_button()` | `_router_base.py` | ❌ Missing | Add this round |
| `_glossary_tooltip()` | `_router_base.py` | ❌ Missing | Add this round |
| `_section_title()` | `_router_base.py` | ❌ Missing | Add this round |
| `_study_card()` | `_helpers.py` | ❌ Missing | Add this round |
| `_expert_card()` | `_helpers.py` | ❌ Missing | Add this round |
| `_scenario_card()` | `_helpers.py` | ❌ Missing | Add this round |
| `_historian_disclaimer()` | `_helpers.py` | ❌ Missing | Add this round |

**Recommendation**: Schedule a design system maintenance pass (1-2h) to document all undocumented components. This is D-004 (downgraded to P2 in R34).

---

## 6. Top 3 Design Recommendations

### #1: Extract Benchmark Health Score Fetching (D-120, 1-2h)

The benchmark data fetching logic is duplicated between `_health.py` (117 lines) and `_summary.py` (107 lines). This is the highest-impact P2 item because: (a) it's a D-003 regression (duplicated logic), (b) it affects two core business card sections, (c) any future changes to benchmark logic must be made in two places. Extract into `health_scoring.get_benchmark_scores(client, industry, stock_id)` shared service function.

### #2: Document `_so_what_box()` and `_explain_button()` in Design System (D-119, 0.5h)

Sprint 19 introduced `_so_what_box()` (C149) and `_explain_button()` is a core interaction component used across multiple pages. Both are stable, well-tested components that should be documented in the design system before Sprint 20 adds more features that might need similar components. This is a quick win that prevents future inconsistency.

### #3: Create `_onboarding_card()` Helper Before C163 Coding Starts (Sprint 20 Prerequisite, 0.5-1h)

C163 (Learn First Gate) will need a multi-step onboarding card flow. Rather than implementing this inline in the page (which risks D-003 regression), create a shared `_onboarding_card()` helper in `_router_base.py` first. This follows the proven pattern from D-041 (Sprint 5 card components) — create the component before the feature. The design spec is already defined in the C103 spec (current_problems.md lines 786-853).

---

## 7. Summary

### Design Grade: **A** (maintained, 7th consecutive A since R34)

### Sprint 19 Verification

| Feature | Inline HTML | Shared Components | Section Titles | Disclaimer | Overall |
|---------|-------------|-------------------|----------------|------------|---------|
| C147 Historical Pattern | ✅ Zero | ✅ `_section_title`, `_info_card` | ✅ | ✅ `st.caption()` | ✅ **Pass** |
| C140 Case Study Library | ✅ Zero | ✅ `_section_title`, `_info_card`, `_count_label` | ✅ | ✅ `_historian_disclaimer()` | ✅ **Pass** |
| D-114 Inline HTML Fix | ✅ Confirmed | ✅ All shared | ⚠️ Raw `st.markdown` (D-117) | ✅ | ✅ **Pass** |
| D-113 Tests | N/A | N/A | N/A | N/A | ✅ **Pass** |

### New Issues: 4 (all P2)
- D-117: `_health.py` raw `st.markdown` header
- D-118: `_info_card()` with empty title
- D-119: `_so_what_box()` undocumented
- D-120: Benchmark duplication escalation

### Sprint 20 Readiness
- C167 (AI Screener Explanations): ✅ Ready — uses existing components
- C163 (Learn First Gate): ⚠️ Needs `_onboarding_card()` helper before coding
- C40 (Beginner/Expert Mode): ✅ Mostly ready — extends C105 toggle pattern

### Design System Updates Needed
- Add `_so_what_box()` (implication callout)
- Add `_onboarding_card()` (for C163)
- Add `_explain_button()`, `_glossary_tooltip()`, `_section_title()` (long-overdue)
- Document `_subsidiary_card()`, `_count_label()` (from Round 21)

---

*This review was prepared by the Design Reviewer for Round 40 (2026-06-14). Next update: After Sprint 20 feature implementation.*
