# Round 28 — Design Review (2026-06-18)

## Sprint 13a Design Assessment

### C33 Glossary Tooltip Design

**Overall: 🟢 Well-executed, follows design system**

The `_glossary_tooltip()` component in `_router_base.py:166-187` uses `st.popover()` with a clean ℹ️ trigger pattern. Each tooltip shows: term name (bold), plain-language definition (italic), optional example, optional analogy. This follows the design system's "beginner-friendly" principle (Section I, #4) and the PPT-style "plain-language translations" requirement.

**Design system compliance:**
- ✅ Popover label format `ℹ️ {name}` is consistent across all 6 invocations
- ✅ Content structure (name → plain → example → analogy) matches the glossary YAML schema
- ✅ Uses `st.popover()` — a native Streamlit component, no inline HTML
- ✅ Graceful degradation: returns `None` if term not found (no broken UI)
- ✅ Placement: co-located with the metric it explains (above each metric column in `_render_key_metrics`)

**Issues identified:**

1. **Dual tooltip pattern on key metrics (D-079)** — Each key metric now has TWO interactive elements: a `ℹ️` glossary popover (from `_glossary_tooltip()`) AND a `❓` education button (from `_render_metric_popover()`). This creates visual clutter and cognitive overhead. A user sees two help icons per metric with no clear distinction between "what does this term mean" (glossary) and "explain this specific value" (education). The design system's ten-second test principle says a novice should understand the page in 10 seconds — two competing help icons per metric works against that.

2. **`_render_metric_popover()` inline HTML (D-073, pre-existing)** — The function at `_financial.py:30-36` renders its own card HTML with `unsafe_allow_html=True`, duplicating `_白话_card()` styling. This is a known P2 issue from the architect's review. The inline card uses identical CSS to `_白话_card()` (`#F8F9FA`, `border-radius:12px`, `padding:1.2rem`, `border-left:4px solid #3498DB`) but bypasses the shared component.

3. **Popover column layout asymmetry** — `_render_metric_popover()` uses `st.columns([5, 1])` to place the ❓ button beside the card. But the glossary tooltip (`_glossary_tooltip()`) is called *before* the popover, outside the column layout. This means the ℹ️ popover appears above the card while the ❓ button is to the right — an asymmetric interaction pattern that could confuse users.

### C48 Story Card Design

**Overall: 🟢 Excellent — model example of component-based design**

The always-visible story card (`_summary.py:38-146`) is a textbook implementation of PPT-style principles:

**Design system compliance:**
- ✅ **One key point per page**: The story card answers "what is this company?" — a single clear message
- ✅ **Ten-second test**: Company name → one-liner → 3 key metrics → health score → fun fact. A novice can grasp the company in <10 seconds
- ✅ **Component-only construction**: Uses `_info_card()`, `_白话_card()`, `_summary_card()` — zero inline HTML in the story card itself
- ✅ **PPT-style hierarchy**: Header (name/ticker) → one-liner (blue info card) → metrics (3-column 白话 cards) → health (orange summary card) → fun fact (blue info card). Clear visual progression
- ✅ **Typography**: Follows design system — labels at `0.85rem`/`#7F8C8D`, values at `1.6rem`/`font-weight:700`, analogies in green italic
- ✅ **Color system**: Blue border for info, orange for summary, green for positive — all match design system hex codes
- ✅ **Always visible**: No expander wrapper (D-070 resolved). The card renders directly on page load

**Health score indicator design** — The `_summary_card("整體健康度", f"{overall_health:.0f}/100 {health_label}", "🏥")` uses the orange summary card style, which correctly distinguishes it from the blue info cards. The emoji indicators (🟢/🟡/🔴) provide instant visual parsing. This follows the design system's color rules (green=positive, red=negative).

**No design regressions detected** — The story card is the cleanest component-constructed section on the entire Business Card page.

---

## Design Grade

**A (18th consecutive A/A-)**

**Justification:**
- Sprint 13a delivered two features that both follow the design system
- C33 Glossary tooltip is a clean, reusable component that advances the "beginner-friendly" principle
- C48 Story Card is now a model of PPT-style, component-based design
- Zero inline HTML in the story card (D-068 resolved)
- D-070 (expander removal) directly supports the ten-second test principle
- The dual tooltip situation (D-079) is a new P2 concern but does not rise to grade-impact level
- Pre-existing P2 issues (D-073 inline HTML in popover, D-003 card inconsistency) remain but are not Sprint 13a regressions

**Grade trajectory**: A (R19) → A- (R20) → A (R21) → A (R22) → A (R23) → A (R24) → A (R25) → A (R26) → A (R27) → **A (R28)**

---

## New Design Issues Identified

### D-079: Dual Tooltip Pattern Creates Visual Clutter on Key Metrics
- **Severity**: P2
- **Source**: Design Review Round 28 (Sprint 13a)
- **Description**: Each key metric in `_render_key_metrics()` now has two interactive help elements: a `ℹ️` glossary popover (showing term definition) and a `❓` education button (showing metric-specific explanation with value context). These two patterns serve overlapping purposes and create visual clutter. The ℹ️ popover appears above the metric card while the ❓ button appears to the right — an asymmetric layout. Users cannot easily distinguish between "term definition" and "value explanation."
- **Affected Files**: `src/pages/business_card/_sections/_financial.py:68-121`
- **Proposed Fix**: Merge both tooltip sources into a single interaction. Option A: Extend `_glossary_tooltip()` to accept an optional `metric_value` parameter and show the education content (explanation, analogy, direction) alongside the definition — replacing the separate ❓ button. Option B: Remove the glossary tooltip and enhance the ❓ popover to include the term definition at the top. Either way, one help icon per metric, not two.
- **Effort**: 1-2h
- **Design System Impact**: Would require updating the tooltip component spec in `docs/domain/design_system.md`

### D-080: Story Card Health Score Lacks Color-Coded Border
- **Severity**: P2
- **Source**: Design Review Round 28 (Sprint 13a)
- **Description**: The health score in the story card uses `_summary_card()` which has an orange border (`#F39C12`). While the summary card style is appropriate for the "hero" position, the health score's border color doesn't reflect the actual health level. A company scoring 85/🟢 and a company scoring 25/🔴 both get the same orange border. The emoji indicator (🟢/🟡/🔴) provides the signal, but the border color could reinforce it.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py:141-142`
- **Proposed Fix**: Either (a) add a `border_color` parameter to `_summary_card()` to allow dynamic border colors, or (b) create a `_health_card(score, label)` component that maps score ranges to green/yellow/red borders. This aligns with the design system's color rules (Section 3.1: red/green for status indication).
- **Effort**: 0.5-1h
- **Design System Impact**: Would add a "health card" variant to the card component spec

---

## Sprint 13b Design Recommendations

### C36 Revenue Tree

**Current state**: `revenue_tree.py` is a 73-line standalone page already using `_section_title`, `_info_card`, `_白话_card`, and `_historian_disclaimer`. It follows the design system well.

**Design direction for Sprint 13b polish:**

1. **Add glossary tooltips** — Import `_glossary_tooltip` and `glossary_service` and add tooltips for key revenue terms (營收年增率, 營業收入, 自由現金流). This brings C36 in line with the tooltip pattern established in `_financial.py`. Effort: 0.5h.

2. **Enhance the pie chart section** — The current pie chart + info cards layout (3:2 column ratio) is good. Consider adding a "revenue concentration" indicator card: if the top revenue source is >50%, show a `_summary_card("營收集中度", "高度依賴單一來源", "⚠️")` warning. This supports the PPT-style "one key point" principle by highlighting the most important revenue insight.

3. **Add a "revenue trend mini-chart"** — Below the pie chart, add a small revenue trend sparkline (using `create_revenue_trend_chart`) to show trajectory. This adds temporal context without adding a full section. Keep it compact: height ~200px.

4. **Disclaimer** — Already has `_historian_disclaimer("revenue_tree")` but the type "revenue_tree" doesn't exist in `_DISCLAIMER_TEXTS`. It falls back to "general". Add a specific revenue tree disclaimer: `"⚠️ 營收組成資料來自公開資訊觀測站，分類方式可能因公司申報方式而異。"`

5. **Empty state** — The `st.info("目前沒有詳細營收組成資料")` message should use a standardized empty state component (see D-033). For now, this is acceptable as-is.

**Design patterns to follow**: Use existing `_router_base.py` components only. No new inline HTML. Follow the same card-based PPT style as the Business Card page.

### C46 Moat Analysis

**Current state**: No existing code. Must be created from scratch.

**Design direction:**

1. **Card-based moat score display** — Use a radar/spider chart (similar to C43 health snowflake) for the overall moat score, with 5 dimensions: brand power, network effects, switching costs, cost advantages, intangible assets. Each dimension gets a `_白话_card()` with score + plain-language analogy.

2. **Moat strength indicator** — At the top of the page, show a `_summary_card("護城河評分", f"{score}/100 {label}", "🏰")` as the hero element. Use the `_summary_card` orange border for the hero position. Consider adding a color-coded border (D-080 pattern) to reflect moat strength.

3. **Per-dimension detail cards** — Below the radar chart, show 5 `_info_card()` components (one per dimension) with: dimension name, score, plain-language explanation of what this moat means for this company, and a "為什麼重要" analogy.

4. **Comparison context** — Add a `_info_card("產業對比", "這公司的護城河在[產業]中屬於前/中/後段班", "📊")` to provide benchmarking context. This follows the PPT-style principle of one key point per section.

5. **Historian disclaimer** — Use `_historian_disclaimer("general")` at the bottom. Moat analysis is inherently interpretive, so the disclaimer is important.

6. **YAML data source** — Define moat factor definitions in `moat.yaml` following the `glossary.yaml` schema pattern. Each factor: `name`, `description`, `scoring_criteria`, `data_source`. This keeps the service layer clean and the data maintainable.

7. **Page layout** — Follow Zone A/B/C strictly. The moat page should be a standalone page (like `revenue_tree.py`) to avoid adding more sections to the already-long Business Card page. This also addresses D-005 (page overload risk).

**Design anti-patterns to avoid:**
- Do NOT add moat analysis as another section on the Business Card page (would worsen D-005)
- Do NOT use inline HTML for moat cards (follow the component pattern)
- Do NOT show raw scoring rubric to users (keep it in the service layer)

---

## Design System Updates Needed

1. **Add `_glossary_tooltip()` component spec** (Section 3.3 Cards → new subsection "Tooltips"):
   ```
   ### 3.6 Tooltips
   
   | Component | Function | Usage |
   |-----------|----------|-------|
   | Glossary tooltip | `_glossary_tooltip(term_key, glossary_service)` | ℹ️ popover on financial terms |
   
   **Rules:**
   - One tooltip per metric maximum (merge glossary + education into single interaction)
   - Popover label format: `ℹ️ {term_name}`
   - Content order: name (bold) → definition (italic) → example → analogy
   - Graceful degradation: return None if term not found
   ```

2. **Add "health card" variant** (Section 3.3 Cards):
   ```
   <!-- Health card (dynamic border) -->
   <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid {color};margin:0.5rem 0;">
       <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
       <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{score}/100</div>
       <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
   </div>
   ```
   Where `{color}` = `#27AE60` (≥70), `#F39C12` (40-69), `#E74C3C` (<40).

3. **Document the "one help icon per metric" rule** (Section IV Interaction Patterns → new subsection):
   > Each metric must have at most ONE interactive help element. If both glossary definition and metric education are needed, merge them into a single popover that shows the definition first, then the value-specific explanation.

4. **Add moat analysis page spec** (Section V PPT Style → page list):
   > Moat Analysis: What competitive advantages does this company have? How durable are they?

---

## Summary

**Design health: 🟢 STRONG — 18th consecutive A grade.**

Sprint 13a was a design-clean sprint. Both C33 (Glossary) and C48 (Story Card) follow the design system and advance the core PPT-style principles. The story card is now the gold standard for component-based page construction — always visible, zero inline HTML, clear visual hierarchy, passes the ten-second test.

**Key strengths:**
- Story card is a model of PPT-style design (one key point, visual-first, beginner-friendly)
- Glossary tooltip is a clean, reusable component that addresses D-012 (no glossary system)
- Zero new inline HTML introduced in Sprint 13a
- D-068 and D-070 properly resolved

**Key concerns:**
- Dual tooltip pattern (D-079) needs resolution before more metrics get tooltips
- Pre-existing inline HTML in `_render_metric_popover()` (D-073) should be fixed in Sprint 13b
- C46 Moat Analysis needs careful design to avoid becoming another wall-of-text page

**Sprint 13b design readiness: 🟢 READY**
- C36 Revenue Tree: design is solid, needs glossary tooltips + polish
- C46 Moat Analysis: design direction is clear (radar chart + card-based layout + standalone page), but requires ground-up creation following the patterns established by C33/C48

**Recommended priority for Sprint 13b design:**
1. Fix D-079 (merge dual tooltips) before adding more tooltips to C36
2. Add glossary tooltips to C36 (quick win, 0.5h)
3. Design C46 moat page following the story card pattern (hero card → dimension cards → disclaimer)

---
*Reviewer: Design Reviewer*
*Date: 2026-06-18*
*Next review: Sprint 13b mid-point or Round 29*
