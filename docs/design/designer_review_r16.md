# Design Review — Round 16

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: Round 16 review — Sprint 3 complete (C37, C39, C41, C43, C44, C45), Sprint 4 starting (C38, C48, C51, C53-1), Sprint 5 prerequisites (D-039, D-040, D-041) assessed.
> **Current Design Grade**: A (4th consecutive round — under review)

---

## Table of Contents

1. [Current Grade Assessment](#current-grade-assessment)
2. [Sprint 3 Design Impact](#sprint-3-design-impact)
3. [Sprint 4 Design Risk Assessment](#sprint-4-design-risk-assessment)
4. [New Design Issues](#new-design-issues)
5. [Design System Updates Needed](#design-system-updates-needed)
6. [Sprint 5 Prerequisites Status](#sprint-5-prerequisites-status)
7. [Summary](#summary)

---

## Current Grade Assessment

### Overall Grade: A (Maintained — 5th consecutive round)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | All 14 business card sections render within Zone C. No layout intrusions into Zone A or B. |
| **PPT-Style Adherence** | A- | 14 sections on business card page. C44/C45 use `st.expander` progressive disclosure effectively. Page length is manageable but approaching the limit of the "one key point per page" principle. |
| **Card Component Consistency** | B+ | D-003 root cause persists. Five specific regression instances identified (see Sprint 3 Impact). No *new* regressions in Sprint 3, but existing ones unaddressed. |
| **Color System** | A- | D-036 (risk card `#FFF8F0`) and D-037 (`_白话_card` `#F5F5F5`) remain. Both are <0.5h fixes. Overall color discipline is strong. |
| **Plain-Language System** | A | Historian tone consistent across all sections. C44 risk descriptions and C43 dimension explanations are excellent. |
| **Visual Health Score** | A | C43 + D-034 metric value tooltips provide complete picture with raw numbers displayed below scores. |
| **Synthesis/Summary Layer** | A | C37 stable with `_summary_card()`. Page flow (summary → deltas → health → details) is correct. |
| **Valuation Context** | A | C45 stable with valuation band chart + `_info_card` interpretation. |
| **Mobile Responsiveness** | B- | D-006 unchanged. Media queries exist at 768px and 600px but only handle padding/font-size. |
| **Discovery Mechanism** | C+ | C41 provides partial in-page peer discovery. Full screener (C42) still needed. |
| **Design System Documentation** | A | D-004 resolved. `docs/design/design_system.md` exists at expected path. |
| **Component Architecture** | B+ | `_summary_card()`, `_info_card()`, `_白话_card()` in `_router_base.py` are used by most sections. But 5+ sections still use inline HTML for cards. |

### Grade Justification

The grade is maintained at **A** for a 5th consecutive round because:

- **Zero P0 issues** — no blocking design problems
- **Core design principles intact** — PPT style, ten-second test, Zone A/B/C, historian tone
- **D-004 resolved** — design system doc exists at canonical path
- **Progressive disclosure proven** — C44's `st.expander` pattern is the model for future sections
- **No new P1 issues** introduced in Sprint 3 implementation
- **Plain-language system fully operational** across all sections

**Risk to grade**: The A could slip to A- in Round 17 if:
1. Sprint 4 features (C38, C48, C51) add more inline HTML without using shared card components
2. D-003 is not addressed before Sprint 5's C71/C73/C74 add 3+ more card types
3. Page overload (D-005) worsens without applying progressive disclosure to C37/C39 sections

---

## Sprint 3 Design Impact

Sprint 3 delivered six features (C37, C39, C41, C43, C44, C45) that collectively transformed the business card page from a minimal MVP to a comprehensive company analysis page. This is the largest single-round expansion of the page in the project's history.

### Positive Design Impacts

1. **C37 (Key Takeaways)** — ✅ Uses `_summary_card()` with `#F39C12` orange border. This is the "hero card" of the page and correctly establishes the summary-first reading order.
2. **C39 (Recent Deltas)** — ✅ Uses `_info_card()` for delta display. The empty state (`"近期無顯著變化..."`) is well-designed.
3. **C43 (Health Snowflake)** — ✅ The 5-dimension score cards use inline HTML but with correct `#F8F9FA` design-system background. The color-coded indicators (🟢🟡🟴) follow the design system. D-034 fix ensures raw metric values appear below scores.
4. **C44 (Risk Analysis)** — ✅ Excellent use of `st.expander` with `expanded=False`. This sets the precedent for progressive disclosure on the business card page.

### Negative Design Impacts (Regressions)

5. **D-035: C41 Peer Cards** — C41's `_render_read_next` at line 569 uses `_info_card()` for the actual card content (good), but the section header at line 549 uses a raw `st.markdown("### 📖 推薦閱讀")` instead of the `_section_title()` helper that exists in `_router_base.py`. This is a minor inconsistency — the header should use `_section_title("推薦閱讀")` for emoji-prefix detection and consistent formatting.

6. **D-036: C44 Risk Dimension Cards** — `_render_risk_dimension()` in `_helpers.py` line 86 uses `background:#FFF8F0` (tip/warning background) instead of the standard `#F8F9FA`. While defensible for risk context, the color-coded border-left already communicates risk level. The background should be `#F8F9FA` per design system.

7. **D-037: `_白话_card` Background** — `_router_base.py` line 91 uses `background:#F5F5F5` instead of design system's `#F8F9FA`. This affects every `_白话_card()` call across the entire app (key metrics, dividend mini-cards, etc.).

8. **D-038: C41 API in View Layer** — `_render_read_next` at line 552 calls `client.get_stock_info()` directly. This is also a design concern: the API call happens on every render, causing potential layout shifts if the call is slow.

9. **Health Dimension Cards Inline HTML** — `_render_health` at line 227-236 uses inline HTML for the 5-dimension score cards instead of a shared component. These cards don't use the standard `border-radius:12px` or `padding:1.2rem` from the design system — they use `padding:0.5rem` and `border-radius:10px`, creating a visually distinct mini-card style that doesn't match the rest of the app.

### Net Assessment

Sprint 3 added significant value but introduced **5 distinct card styling inconsistencies** (D-035 header, D-036 risk bg, D-037 白话 bg, D-038 API layer, health mini-card deviation). None are new P1 issues — all are P2 and were identified in Round 14. The fact that they remain unaddressed entering Sprint 4 is concerning because Sprint 4 will add more sections.

---

## Sprint 4 Design Risk Assessment

Sprint 4 plans four features: C38 (Compare Stories), C48 (Story Card), C51 (Sector Heatmap), C53-1 (Social Sharing URL). Design risk varies significantly across these.

### C38: Compare Stories — 🔴 HIGH RISK

**Risk Level**: High — this is a completely new UI pattern for Stock Explorer.

**Concerns**:
- No existing multi-company comparison layout exists in the app. This will be the first page showing two companies side by side.
- **Card consistency risk**: Comparison cards for each company will likely use inline HTML (continuing D-003).
- **Width allocation**: Two companies in `st.columns(2)` leaves ~50% width per company — cards designed for full width will look cramped.
- **Chart scaling**: The design system requires identical scales for comparison charts (Section III, "Comparison Charts"). This must be enforced.
- **PPT-style compliance**: Two companies = two key points. This violates "one key point per page" unless the comparison *is* the single key point (e.g., "How does this company differ from its peer?").

**Recommendations**:
1. Define a `_comparison_card()` component before implementation — follows D-041 Sprint 5 prerequisite pattern.
2. Use `st.columns(2)` with a visible divider between companies.
3. Both company cards must use the *same* card component (either `_info_card()` or `_summary_card()`) for visual parity.
4. Charts must use identical y-axis ranges. The `create_health_snowflake()` function already supports multiple companies — ensure the same axis limits.
5. Limit comparison to 2 companies only. No 3-way comparisons.

### C48: Story Card — 🟡 MEDIUM RISK

**Risk Level**: Medium — this is a summary/visual card on the business card page.

**Concerns**:
- **Another card type** — without a standardized component, this will likely use inline HTML (D-003 regression).
- **Placement** — where does the story card appear? If at the top, it competes with C37's hero card. If lower, it may be overlooked.
- **Content density** — a "story card" could easily become text-heavy, violating PPT-style limits.

**Recommendations**:
1. Define a `_story_card()` component in `_router_base.py` before implementation. Suggested style: `#3498DB` border-left, `#F8F9FA` background, max 3 sentences.
2. Place C48 directly after C37 (Key Takeaways) — the story card naturally extends the summary narrative.
3. Apply the 200-character text limit (design system Section V.2).
4. This is also the TL;DR that was originally planned as C72 — keep it brief and scannable.

### C51: Sector Heatmap — 🟡 MEDIUM RISK

**Risk Level**: Medium — new visualization type but confined to its own page/context.

**Concerns**:
- **New visualization type** — Stock Explorer currently uses Plotly bar, pie, radar, and band charts. A heatmap is a new pattern.
- **Color discipline** — heatmaps require a color scale. The design system restricts status colors to red/green/blue. The heatmap must use a *gradient of one color* (e.g., light blue → dark blue) rather than red→green, which would imply buy/sell signals.
- **Mobile risk** — heatmaps with many cells become unreadable on mobile.

**Recommendations**:
1. Use a single-hue color scale (`#EBF5FB` → `#2980B9`, i.e., light blue → dark blue) to stay within design system color rules.
2. Add a `max-width` constraint and horizontal scroll for mobile rather than shrinking cells below readable size.
3. Use `plotly.graph_objects.Heatmap` with `hovertemplate` showing company name + metric value + plain-language explanation.
4. Include a plain-language caption below the chart explaining what the heatmap shows.

### C53-1: Social Sharing URL — 🟢 LOW RISK

**Risk Level**: Low — this is primarily a URL/copy mechanism, not a new visual component.

**Concerns**:
- **Share button placement** — should not compete with the watchlist button in the header.
- **Preview card** — if sharing generates a link preview (OG image/card), that preview is a new design artifact.

**Recommendations**:
1. Place the share button in the header's existing column layout (col3 area) or as a small icon button next to the stock name.
2. If generating OG preview cards, use the `_summary_card()` style for consistency.
3. The shared URL should deep-link to the specific stock + tab (e.g., `/stock/2330?tab=business-card`).

---

## New Design Issues

### D-042: Health Dimension Mini-Cards Use Non-Standard Styling
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 16
- **Description**: The 5-dimension score cards in `_render_health()` (lines 227-236 of `_sections.py`) use inline HTML with `padding:0.5rem`, `border-radius:10px`, and no `border-left`. This differs from the design system's card spec (`padding:1.2rem`, `border-radius:12px`, `border-left:4px solid`). While the compact style is appropriate for the 5-column layout, it creates a visual mismatch with all other cards on the page.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 227-236
- **Proposed Fix**: Create a `_mini_score_card(label, score, indicator, color)` helper in `_router_base.py` with standardized compact styling. This would be a recognized "mini card" variant in the design system.
- **Effort**: 0.5h

### D-043: Dividend History Table Uses Inline HTML Instead of st.dataframe
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 16
- **Description**: The dividend history table in `_render_dividend()` (lines 420-439 of `_sections.py`) builds a complete HTML table from scratch with inline styles. This bypasses Streamlit's `st.dataframe()` which provides sorting, filtering, and responsive behavior. The inline HTML table also uses `border-bottom:1px solid #F8F9FA` which is nearly invisible on white backgrounds.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 420-439
- **Proposed Fix**: Build the badge list as a separate column, then use `st.dataframe()` with column config for badges. Or, if HTML is kept, use `border-bottom:1px solid #BDC3C7` for visible row separators.
- **Effort**: 1-2h

### D-044: C41 Read Next Header Doesn't Use _section_title() Helper
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 16
- **Description**: `_render_read_next()` at line 549 uses raw `st.markdown("### 📖 推薦閱讀")` instead of the `_section_title()` helper from `_router_base.py`. This means the header doesn't get the emoji-prefix detection and consistent formatting that `_section_title()` provides.
- **Affected Files**: `src/pages/business_card/_sections.py` line 549
- **Proposed Fix**: Replace with `_section_title("📖 推薦閱讀")`.
- **Effort**: <0.5h (one-line change)

---

## Design System Updates Needed

The design system at `docs/design/design_system.md` and `docs/domain/design_system.md` needs the following updates to support Sprint 4 and Sprint 5 features:

### Update 1: Add "Mini Score Card" Variant

Current spec only defines info cards and tip cards. The health dimension cards have established a de facto "mini card" pattern. This should be formalized:

```html
<!-- Mini score card (for compact grid layouts) -->
<div style="text-align:center;padding:0.5rem;background:#F8F9FA;border-radius:10px;margin:0.2rem 0;">
    <div style="font-size:0.8rem;color:#7F8C8D;">{indicator} {label}</div>
    <div style="font-size:1.4rem;font-weight:700;color:#2C3E50;">{value}</div>
    <div style="font-size:0.7rem;color:#7F8C8D;margin-top:0.2rem;">{description}</div>
</div>
```

### Update 2: Add Story Card Specification (for C48)

```html
<!-- Story card (narrative summary) -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0 1rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.5rem;line-height:1.7;">{narrative}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{plain_language_takeaway}</div>
</div>
```

**Rules**: Story card text max 200 characters. Narrative max 3 sentences. Place after C37.

### Update 3: Add Comparison Layout Rules (for C38)

Under Section V (PPT Style), add:

**5.5 Comparison Pages**
- Comparison pages answer one question: "How does Company A differ from Company B?"
- Maximum 2 companies per comparison
- Both companies must use identical card components (same border, same background, same padding)
- Charts must use identical scales
- Place company names at the top of each column for immediate identification
- Highlight differences, not similarities

### Update 4: Add Heatmap Color Rules (for C51)

Under Section 3.1 (Color System), add:

**Heatmap Colors**:
- Use single-hue gradients only (recommend `#EBF5FB` → `#2980B9`, blue spectrum)
- Never use red→green gradients (implies buy/sell signals)
- Include a color legend with plain-language labels ("Low" / "Medium" / "High")
- Cells must show values on hover with plain-language explanations

### Update 5: Add Section Header Standard (D-039 Fix)

Under Section 3.3 (Cards), add:

**Section Headers**:
```python
def _section_title(title: str):
    """Auto-detect emoji prefix. If title starts with emoji, use as-is. Otherwise, prepend 📊."""
    # Implementation: check if first character is in emoji unicode range
    # If yes: st.markdown(f"### {title}")
    # If no: st.markdown(f"### 📊 {title}")
```

### Update 6: Add Disclaimer Component Specification (D-040 Fix)

Under Section 3.3 (Cards), add:

**Disclaimer Caption**:
```python
def _historian_disclaimer(disclaimer_type: str = "general"):
    messages = {
        "expert": "以上為分析師意見綜合，不構成投資建議。",
        "scenario": "歷史表現不代表未來結果。此為教育用途，非投資建議。",
        "general": "本頁面僅提供歷史資料分析，不構成投資建議。",
    }
    st.caption(f"⚠️ {messages[disclaimer_type]}")
```

---

## Sprint 5 Prerequisites Status

The three Sprint 5 prerequisites (D-039, D-040, D-041) were proposed in Round 15 but not yet implemented.

### D-039: Standardized Section Header Pattern — ❌ NOT STARTED

**Current State**: `_section_title()` exists in `_router_base.py` (lines 69-86) but is only used by `group_structure.py` and etf_detail/etf_browser pages. The business card page headers use a mix of:
- `_section_title()` — 0 times (despite being imported via `_sections.py` line 34... actually it's not imported in `_sections.py`)
- Raw `st.markdown("### ...")` — used in `_render_health` (line 208), `_render_one_liner` (none, uses `_info_card`), `_render_key_metrics` (line 300), `_render_revenue_breakdown` (line 455), `_render_revenue_trend` (line 478), `_render_valuation` (line 496), `_render_news` (line 525), `_render_read_next` (line 549)
- `st.expander("### ...")` — used in `_render_risk` (line 255) with a raw string

**Critical Finding**: `_section_title` is NOT imported in `_sections.py`. The import from `_router_base` at line 34 only imports `_白话_card, _info_card, _summary_card`. This means all 14 business card sections are using raw markdown headers.

**Action Required**: Add `_section_title` to the import in `_sections.py` line 34, then replace all 8 raw `st.markdown("### ...")` calls with `_section_title()`. Estimated effort: 1-2h.

### D-040: Standardized Disclaimer Component — ❌ NOT STARTED

**Current State**: The only disclaimer on the business card page is in `_render_footer()` (line 604) which uses `_info_card()` with a custom string. This is acceptable for the current single-use case, but C73 (Expert Analysis) and C74 (Historical Scenarios) will need *different* disclaimer text.

**Action Required**: Create `_historian_disclaimer()` in `_router_base.py` with type variants. Replace the footer disclaimer with `_historian_disclaimer("general")`. Estimated effort: 0.5h.

### D-041: Sprint 5 Card Components — ❌ NOT STARTED

**Current State**: No `_study_card()`, `_expert_card()`, or `_scenario_card()` components exist. C71 (Study Log), C73 (Expert Analysis), and C74 (Historical Scenarios) are planned for Sprint 5 with no standardized card components defined.

**Risk Assessment**: HIGH — without standardized components, Sprint 5 features will almost certainly use inline HTML, worsening D-003 from B+ to B- and potentially triggering a grade reduction.

**Action Required**: Before Sprint 5 implementation begins, create:
1. `_study_card(entry)` — for C71 study log entries (blue border, `#F8F9FA` bg)
2. `_expert_card(consensus, source_count)` — for C73 expert analysis (orange border, `#FFF8F0` bg)
3. `_scenario_card(scenario_name, result_text)` — for C74 scenarios (blue border, `#F8F9FA` bg)

Estimated effort: 1h for all three.

### Prerequisites Summary

| ID | Prerequisite | Status | Effort | Risk if Skipped |
|----|-------------|--------|--------|-----------------|
| D-039 | Section headers | ❌ Not started | 1-2h | C71/C73/C74 add 3+ more header inconsistencies |
| D-040 | Disclaimer component | ❌ Not started | 0.5h | Inconsistent disclaimer text across C73/C74 → regulatory risk |
| D-041 | Card components | ❌ Not started | 1h | C71/C73/C74 use inline HTML → D-003 worsens to B- |

**Total prerequisite effort**: 2.5-3.5h — this should be completed as the first Sprint 5 task, before any feature implementation.

---

## Summary

### What Changed Since Round 15

1. **Sprint 3 completed** — All 6 Sprint 3 features (C37, C39, C41, C43, C44, C45) are now live on the business card page.
2. **Design system doc verified** — D-004 remains resolved at `docs/design/design_system.md`.
3. **No new P1 issues** — The 3 active P1 issues (D-003, D-005, D-006) remain unchanged.
4. **3 new P2 issues identified** — D-042 (health mini-card styling), D-043 (dividend table HTML), D-044 (read next header).

### Design Issues Updated Counts

| Category | Previous (R15) | Current (R16) | Change |
|----------|----------------|----------------|--------|
| P0 (Blocking) | 0 | 0 | — |
| P1 (Important) | 3 | 3 | — |
| P2 (Optimization) | 13 | 16 | +3 (D-042, D-043, D-044) |
| Resolved | 15 | 15 | — |
| **Total** | **31** | **34** | **+3** |

### Grade Decision: A (Maintained — 5th consecutive round)

**Rationale**: The Sprint 3 features were well-designed overall. The progressive disclosure pattern from C44 is the single most important design pattern established this sprint. No new P1 issues were introduced. The B+ in Card Component Consistency is the weakest dimension but is offset by strengths in Plain-Language System (A), Visual Health Score (A), and Synthesis Layer (A).

### Top Priority Actions for Sprint 4

1. **Before Sprint 4 coding**: Complete all 3 Sprint 5 prerequisites (D-039, D-040, D-041) — 2.5-3.5h total.
2. **Before C38 implementation**: Define `_comparison_card()` component and comparison layout rules.
3. **Before C48 implementation**: Define `_story_card()` component and place after C37.
4. **Before C51 implementation**: Define heatmap color rules (single-hue gradient).
5. **Quick wins** (can be done any time this sprint):
   - Fix D-037: Change `#F5F5F5` → `#F8F9FA` in `_router_base.py` line 91 (<0.5h)
   - Fix D-036: Change `#FFF8F0` → `#F8F9FA` in `_helpers.py` line 86 (<0.5h)
   - Fix D-044: Use `_section_title()` in `_render_read_next` (<0.5h)

---

*Design Review maintained by Design Reviewer. Next update: After Sprint 4 feature implementation or Round 17, whichever comes first.*
