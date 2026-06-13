# 2026-06-13 Design Review — Round 21 Discussion

> **Author**: Design Reviewer
> **Context**: Sprint 11 complete, Sprint 12 planned
> **Design Grade**: A (15th consecutive A/A-)
> **Scope**: Sprint 12 UX evaluation + Info Hierarchy redesign + Post-Sprint 12 priorities

---

## I. Sprint 12 UX Evaluation

### C37 / C39 / C43 / C45 — QA Design Assessment

These four features were implemented across Sprints 2-4 and are now entering QA. From a design perspective, the key quality concerns are:

#### C37 — Key Takeaways Summary Card

**UX Issues to Verify:**
1. **Bullet count compliance**: Spec calls for 3-5 bullets; implementation must cap at 3 (per D-017 fix). QA should verify no stock shows more than 3 bullets.
2. **Plain-language quality**: Auto-generated bullets for non-top-20 stocks use fallback templates. QA should spot-check 5+ fallback stocks for readability — do the bullets pass the "grandmother test"?
3. **Placement**: C37 must be the FIRST element in Zone C, before all other sections. If any section renders above it, that's a P1 layout bug.
4. **Text length**: Each bullet ≤ 50 characters. Total text ≤ 200 characters (design system Section V.2).

**Recommendations:**
- QA should test with 3 beginner users: can they summarize the company after reading only the C37 card? If not, the bullets need rewriting.
- Verify the orange/amber `_summary_card()` styling is used (not `_info_card()`) — this is the visual distinction that makes C37 the "hero" of the page.

#### C39 — What Changed Recently Delta Card

**UX Issues to Verify:**
1. **Delta count cap**: Max 2 deltas shown (per D-019 fix). QA should verify no stock shows more than 2.
2. **Directional color coding**: Positive deltas must use `#27AE60` (green), negative must use `#E74C3C` (red). No other colors for direction.
3. **Empty state**: When no deltas exceed the 10% threshold, the "近期無顯著變化" info card must appear. QA should test with a stable stock (e.g., 中華電信) to verify the empty state renders.
4. **Placement**: C39 must appear directly after C37, before C43. Order: Summary → What Changed → Health → Details.
5. **Threshold sensitivity**: The 10% threshold means C39 will be "silent" for most stocks most of the time. This is correct behavior — don't lower the threshold to make it more visible.

**Recommendations:**
- QA should verify the delta card doesn't appear to be "broken" when empty. The empty state card must look intentional, not like a missing data error.
- Test with a stock that recently had a major event (e.g., earnings miss) to verify the delta detection triggers correctly.

#### C43 — Company Snowflake Health Visualization

**UX Issues to Verify:**
1. **Hover template**: Must show metric values as bullet points (per D-034 fix). Hovering over "獲利能力" should show "ROE 25%" not just "85分".
2. **Dimension cards**: Must display raw metric values in blue text below the score. QA should verify all 5 dimensions show actual numbers.
3. **Color coding**: 3-state system — `#27AE60` (4-5), `#F39C12` (2-3), `#E74C3C` (0-1). Verify no other colors are used for dimension indicators.
4. **Benchmark overlay**: The industry leader's score should appear as a dotted line on the radar chart. QA should verify this renders for at least TSMC (where the benchmark is 聯電).
5. **Ten-second test**: Can a beginner look at the snowflake and within 10 seconds say "TSMC is strong in profitability and growth, but valuation is average"?

**Recommendations:**
- The radar chart is the most complex visual on the page. QA should test with 5+ stocks to ensure no dimension labels overlap or get clipped.
- Verify the snowflake doesn't break on stocks with missing data for some dimensions (e.g., no dividend history → dividend dimension should show N/A, not crash).

#### C45 — Valuation Band Chart

**UX Issues to Verify:**
1. **5-year window**: Must use 5-year P/E range (per D-023 fix), not 2-year. QA should verify the x-axis spans 5 years.
2. **Current P/E marker**: Blue vertical line (`#3498DB`) must be clearly visible against the gray range bar.
3. **Industry average**: Dotted green line (`#27AE60`) for industry average P/E. Verify it renders.
4. **Plain-language interpretation**: ≤ 2 sentences, must include the current P/E value, the historical range, and the position within that range.
5. **Color-coded position**: Bottom 25% = green + "估值偏低", Middle 50% = yellow + "估值合理", Top 25% = red + "估值偏高".

**Recommendations:**
- Test with a stock at the extreme of its range (e.g., very high or very low P/E) to verify the color coding and interpretation text are correct.
- Verify the chart doesn't break for stocks with less than 5 years of data (graceful fallback to available data).

---

### Business Card Info Hierarchy Redesign

**Current Problem (D-005):** The Business Card page has 13+ sections. Even with C44 using `st.expander`, the page is long and risks violating the "one key point per page" PPT-style principle.

**Above-the-Fold Definition:**
"Above the fold" = everything visible without scrolling on a 1920×1080 viewport with the sidebar expanded. This is approximately:
- Zone A (navbar + tabs): ~120px
- Zone C first screen: ~600px of content
- **Total above-fold budget: ~720px = approximately 3 cards**

**Recommended Above-the-Fold Content (in order):**
1. **C37 Key Takeaways** (3 bullets, ~150px)
2. **C39 What Changed Recently** (2 deltas or empty state, ~120px)
3. **C43 Company Snowflake** (radar chart + 5 mini-dimension cards, ~400px)

This uses the full 720px budget. Everything else scrolls.

**Progressive Disclosure Strategy:**
- **Always visible (above fold)**: C37 + C39 + C43
- **Collapsed by default (`st.expander`, `expanded=False`)**: C44 Risk Analysis, C45 Valuation Band, C41 Read Next
- **Visible on scroll (no expander)**: Revenue breakdown, dividend history, key metrics — these are the "detail" sections that interested users will scroll to
- **Removed from Business Card page**: C36 Revenue Tree → move to its own tab; C38 Compare Stories → move to Peer Comparison tab

**Card-Count Limit:**
The design system specifies "max 5 cards per page section." The Business Card page should have:
- **Above fold**: 3 cards (C37, C39, C43) — this is the "dashboard layer"
- **Below fold**: Max 5 additional cards/sections, with at least 2 in `st.expander`
- **Total**: Max 8 cards/sections on the Business Card page (down from 13+)

**Recommended Section Order:**
```
Zone C: Main Content Area
├── C37: 📋 重點摘要 (always visible, above fold)
├── C39: 🔄 最近有什麼變化 (always visible, above fold)
├── C43: ❄️ Company Snowflake (always visible, above fold)
├── ───────────────────────────────── (visual separator)
├── 💰 營收組成 (revenue pie chart — existing)
├── 📊 關鍵數字三連卡 (key metrics — existing)
├── 💡 你知道嗎 (Did You Know — existing)
├── ───────────────────────────────── (visual separator)
├── 📊 估值區間 (C45 — st.expander, collapsed)
├── ⚠️ 風險分析 (C44 — st.expander, collapsed)
├── 📖 推薦閱讀 (C41 — st.expander, collapsed)
└── 🔗 分享這張名片 (C53-1 — always visible, bottom)
```

---

### C40 — Beginner/Expert Mode

**Important Context:** C40 was **cut** in the Sprint 1 planning discussion and replaced with "beginner mode by default" as a design principle. However, Sprint 12 includes "C40 Beginner/Expert Mode navbar toggle" in the plan. This needs clarification.

**UX Implications if Reinstated:**

1. **Zone A placement problem**: A mode toggle in the navbar violates the design system rule that Zone A "Must NOT contain: search box, filters, or any interactive controls." A toggle is an interactive control.
2. **Recommended placement**: If C40 is reinstated, the toggle should be at the TOP of Zone C (main content area), not in Zone A. Use the `_content_toggle()` pattern recommended in the Round 22 review.
3. **Beginner mode definition**: Max 3 cards per page (C37 + C39 + C43 only). All other sections hidden behind a "查看更多" button.
4. **Expert mode definition**: All sections visible, no expanders collapsed.
5. **Default**: Beginner mode (aligns with "beginner-first" philosophy).
6. **Session persistence**: `st.session_state["content_mode"]` persists across page navigations.

**Recommendation:** If Sprint 12 capacity is limited, C40 should remain cut. The "beginner by default" approach (above-the-fold redesign + progressive disclosure) achieves 80% of C40's UX benefit without the complexity of a toggle. C40 can be revisited in Sprint 14+ when the page is more stable.

---

### User Feedback Mechanism

**Streamlit Constraints:** Streamlit has no built-in feedback widget. No native toast/snackbar for "feedback submitted." No persistent storage without a database or file system.

**Recommended Approach: Simple Feedback Button**

1. **Placement**: Bottom of Zone C on the Business Card page, after all content. A subtle `st.button("💬 這個頁面有幫助嗎？")` with `type="secondary"`.
2. **Interaction flow**:
   - Click → `st.popover()` opens with:
     - "這個頁面對您有幫助嗎？" + two buttons: "👍 有幫助" / "👎 沒有幫助"
     - If "👎": show `st.text_area("請告訴我們如何改進", key="feedback_text")` + "送出" button
     - On submit: append to `feedback_log.jsonl` (one JSON per line) + `st.toast("感謝您的回饋！")`
3. **No rating stars**: Stars are subjective and don't produce actionable feedback. Binary helpful/not-helpful + optional text is more useful.
4. **No login required**: Keep it anonymous. Adding login friction will kill response rates.
5. **Data format**:
   ```json
   {"timestamp": "2026-06-13T12:00:00", "stock_id": "2330", "page": "business_card", "helpful": false, "text": "估值區間看不太懂"}
   ```
6. **Privacy**: Add a `st.caption("回饋內容僅用於改善產品體驗，不會與第三方分享")` below the form.

**Why Not These Alternatives:**
- **st.form with submit**: Too heavy for a simple feedback button. Popover is lighter.
- **Sidebar feedback**: Sidebar is Zone B (navigation). Feedback is page content → Zone C.
- **st.survey or third-party**: Streamlit doesn't support embedded surveys. External services (Typeform) break the single-page experience.
- **Emoji reaction bar (👍/😐/👎)**: Looks nice but the middle option produces no actionable data. Binary is better.

**Competitor Reference:** Finimize uses a simple "Was this helpful?" at the end of each article. Khan Academy uses a thumbs up/down after each lesson. Both prove that simplicity drives response rates.

---

## II. Post-Sprint 12 UX Priorities

### Unscheduled Features Ranked by UX Impact

From the full backlog (C36, C38, C40, C42, C46, C47, C48, C51, C52, C56, C58, C68, C88, C94, C100, C107, C117), here are the top features by UX impact:

#### Tier 1: Highest UX Impact (Next 2 Sprints)

| Rank | ID | Title | UX Impact Rationale | Effort |
|------|----|-------|---------------------|--------|
| 1 | **C48** | Company Story Card | **Ten-second test made real.** A 30-second visual summary at the top of every company page — the "hook" that keeps users exploring. Directly addresses the #1 design principle. | 8-12h |
| 2 | **C56** | Explain This Metric | **Design system fulfillment.** The design system *requires* "All professional terms must have plain-language translations" — this delivers it interactively. Transforms every data point into a learning opportunity. | 12-16h |
| 3 | **C42** | Stock Screener | **Product transformation.** Converts Stock Explorer from a lookup tool (user must know the stock) into a discovery tool (user explores by criteria). Addresses D-007 (no discovery mechanism). | 16-24h |

#### Tier 2: High UX Impact (Sprints 14-15)

| Rank | ID | Title | UX Impact Rationale | Effort |
|------|----|-------|---------------------|--------|
| 4 | **C58** | Beginner Onboarding Flow | **Retention-critical.** Without onboarding, beginners bounce before discovering any other feature. Every other feature's value is gated by this. | 14-20h |
| 5 | **C52** | Quiz Mode | **Active learning.** Transforms passive reading into active recall. Khan Academy proves this is the gold standard for education retention. Builds on C101's quiz infrastructure. | 10-14h |
| 6 | **C46** | Moat Analysis | **Unique TW differentiator.** Morningstar's moat rating is iconic but US-only. No TW competitor has this. Perfect "historian" feature — explains competitive advantage through history. | 12-16h |

#### Tier 3: Medium UX Impact (Sprints 16+)

| Rank | ID | Title | UX Impact Rationale | Effort |
|------|----|-------|---------------------|--------|
| 7 | **C117** | In-Context Metric Education | Tap-to-explain with analogies. Similar to C56 but more interactive. Lower priority because C56 covers the same need. | 10-14h |
| 8 | **C36** | Visual Revenue Tree | Shows how money flows through the business. Beautiful visualization but limited to top 10 stocks due to data curation. | 10-14h |
| 9 | **C38** | Compare Stories | Narrative comparison of two companies. High complexity, depends on LLM architecture decisions. | 12-16h |
| 10 | **C47** | Education Academy | The "endgame" feature that transforms Stock Explorer from tool to platform. High effort (20-30h) — plan carefully. | 20-30h |

### Key UX Insights for Post-Sprint 12

1. **C48 (Story Card) should be the #1 priority** — It's the single most impactful feature for the ten-second test, has the best effort-to-impact ratio (8-12h), and no competitor in the TW market has it.

2. **C56 (Explain This Metric) is the design system's unfinished business** — The design system *requires* plain-language translations for all professional terms. C56 delivers this interactively. Without it, the design system requirement is only partially met.

3. **C42 (Screener) transforms the product** — But it's the highest effort (16-24h) and carries the highest design risk (screening interfaces are inherently complex). Must use beginner-friendly presets, not raw metric filters.

4. **C58 (Onboarding) is retention-critical but can wait** — The C103 Lite first-visit guide already provides basic onboarding. C58 (full guided tour) can wait until after C48 and C56 are shipped.

5. **Don't build C40 (Mode Toggle) yet** — The "beginner by default" approach + progressive disclosure achieves 80% of the benefit. Revisit after the page is stable.

---

## III. Design System Impact

### Components Needed for Sprint 12

| Component | Purpose | Used By | Priority |
|-----------|---------|---------|----------|
| `_feedback_button()` | User feedback collection | Business Card page | P1 (new) |
| `_feedback_popover()` | Feedback form in popover | Business Card page | P1 (new) |
| `_content_toggle()` | Beginner/Expert mode (if C40 reinstated) | Zone C top | P2 (conditional) |

### Components Needed for Post-Sprint 12

| Component | Purpose | Used By | Priority |
|-----------|---------|---------|----------|
| `_story_card()` | 30-second visual summary (C48) | Business Card top | P1 |
| `_explain_trigger()` | ❓ button + expander (C56) | All metric cards | P1 |
| `_preset_button()` | Screener preset cards (C42) | Screener page | P1 |
| `_onboarding_step()` | Guided tour step (C58) | Onboarding flow | P2 |
| `_moat_indicator()` | Moat strength visual (C46) | Business Card | P2 |

### Color System Updates

**No new colors needed for Sprint 12.** The existing 7-color system covers all Sprint 12 features.

**Post-Sprint 12 consideration:** If C52 (Quiz Mode) is implemented, consider adding:
- **Quiz/Purple**: `#9B59B6` — for quiz mode, concept comparison, and educational interactive elements. This is NOT a status color (red/green/blue rule still applies) — it's an interaction color for educational features.

### Text Limit Adjustment Needed

**Current rule**: 200 characters per page (Section V.2).
**Problem**: Interactive content (expanders, explanations) needs more space.
**Proposal**: 200 characters for *static* text. Interactive content (expanders, explanations) can have up to 400 characters total, but the *visible* text before expansion must still be ≤ 200 characters.

This is needed for C56 (Explain This Metric) which requires ~300 characters for definition + analogy + "why it matters."

### Layout Pattern Updates

| Pattern | Description | Needed For | Impact |
|---------|-------------|------------|--------|
| Dashboard Top Layer | Stacked cards at top of Business Card page | C37+C39+C43 (already implemented) | Already in place |
| Feedback Section | Bottom-of-page feedback button | User Feedback (Sprint 12) | Low — new section at bottom |
| Content Toggle | Simple/Detailed mode switch | C40 (conditional) | Low — small addition to Zone C top |
| Story Card Hero | Large hero card at top of page | C48 (post-Sprint 12) | Moderate — new hero zone above dashboard |

### Typography Updates

**No new typography needed for Sprint 12.** All new components use existing type scales.

**Post-Sprint 12 consideration:** Add a "mini chart label" style for inline sparklines in C56:
- Mini chart labels: `font-size: 0.75rem, color: #7F8C8D`

---

## IV. Summary of Recommendations

### Sprint 12 Must-Do (Design Perspective)

1. **QA the 4 implemented features** (C37/C39/C43/C45) against the design system checklist — especially placement order, color compliance, and ten-second test
2. **Redesign Business Card info hierarchy** — above-the-fold = C37+C39+C43 only; everything else scrolls or is in expanders
3. **Implement user feedback mechanism** — simple binary helpful/not-helpful + optional text, stored in JSONL
4. **Defer C40 (Mode Toggle)** — "beginner by default" + progressive disclosure achieves the same goal

### Post-Sprint 12 Priority Order

1. **C48 Story Card** (8-12h) — highest UX impact, lowest effort
2. **C56 Explain This Metric** (12-16h) — design system fulfillment
3. **C42 Stock Screener** (16-24h) — product transformation
4. **C58 Onboarding Flow** (14-20h) — retention
5. **C52 Quiz Mode** (10-14h) — active learning
6. **C46 Moat Analysis** (12-16h) — unique differentiator

### Design System Maintenance

- Add `_feedback_button()` and `_feedback_popover()` components
- Update text limit rules for interactive content (200 static / 400 expandable)
- Document the "dashboard top layer" layout pattern
- Plan for `_story_card()` and `_explain_trigger()` components (post-Sprint 12)

---

*This design discussion was prepared by the Design Reviewer for the Stock Explorer team. It evaluates Sprint 12 from a UX/design perspective, prioritizes post-Sprint 12 features by UX impact, and identifies design system updates needed. All recommendations align with the PPT-style design system, the ten-second test principle, and the "historian, not stock picker" product positioning.*
