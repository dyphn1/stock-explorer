## Design Review — Round 38

> **Date**: 2026-06-14
> **Reviewer**: Design Reviewer
> **Scope**: Sprint 17 design verification (C14 + C134 + C07 + D-101), new debt identification, Sprint 18 design readiness, competitor patterns
> **Context**: Sprint 17 COMPLETE. Sprint 18 next (C139 + C141 + C143 + D-097 + Tone QA).

---

### Design Grade: **A** (5th consecutive A since R34)

**Rationale**: Sprint 17 maintained the design discipline established in R34-R37. All three features (C14, C134, C07) use shared components, produce zero new inline HTML regressions in the features themselves, and pass the ten-second test. The benchmark overlay (C14) is a visually clean ghost-line pattern that adds information without clutter. The settings page (C07) uses `_section_title()` consistently. Two minor new design debt items identified (D-108, D-109) — both P2, neither blocking.

---

### Sprint 17 Design Verification

| Feature | Shared Components | Inline HTML | Ten-Second Test | Verdict |
|---------|-------------------|-------------|-----------------|---------|
| **C14 Benchmark Overlay** | ✅ `_info_card()` for "vs 同業" comparison card; `_summary_card()` with `border_color` for health score; `create_health_snowflake()` extended with `benchmark_scores` param | ⚠️ 5-dimension mini-cards use inline HTML (`unsafe_allow_html=True`, lines 222-232 of `_health.py`) — pre-existing pattern (D-042), not a regression | ✅ User sees "健康度 75 vs 台積電 82 → ⬇️ 低於台積電 7 分" in <10s | **Excellent** — Clean ghost-line overlay, graceful degradation when no benchmark |
| **C134 Change Explanations** | ✅ `DeltaExplanationProvider` composes `TemplateExplanationProvider` (shared); `delta_engine.py` delegates via `ExplanationRequest` protocol | ✅ Zero inline HTML — pure Python service layer | ✅ "月營收暴增 60%，可能是大訂單入帳或旺季效應" — immediately understandable | **Sound** — Protocol-based design, backward-compatible, all 54 D-101 tests pass |
| **C07 Wire Thresholds** | ✅ Uses `_section_title()` for section headers; `st.slider()` + `st.caption()` for controls; `st.success()` for info box | ⚠️ 2 instances of inline HTML for visual feedback boxes (lines 101-108, 168-176 of `settings.py`) — `unsafe_allow_html=True` with `background-color:#f0f2f6` divs | ✅ "調整閾值控制事件偵測敏感度" — sliders with 🔴/🟡/🟢 labels are self-explanatory | **Functional** — Clean slider UX, but visual feedback boxes should use shared component |
| **D-101 explain_delta tests** | ✅ N/A (test suite) | ✅ N/A | ✅ 54 tests cover all metric types × directions × magnitudes | **Thorough** — Exact string regression tests, boundary values, generic fallback |

---

### New Design Debt (2 items)

| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| **D-108** | Settings page visual feedback boxes use inline HTML instead of shared component | P2 | 0.5-1h |
| **D-109** | C14 "vs 同業" benchmark card in `_summary.py` fetches benchmark data inline (~100 lines) instead of calling `_fetch_benchmark_health_scores()` from `_health.py` — D-003 regression pattern (duplicated logic) | P2 | 1-2h |

#### D-108 Details
- **Location**: `settings.py` lines 101-108, 168-176
- **Issue**: Two visual feedback boxes (`✅ 目前有效閾值：X%`) use `unsafe_allow_html=True` with inline-styled divs (`background-color:#f0f2f6; border-radius:8px; padding:12px 16px`). These are functionally identical to `_info_card()` but implemented as inline HTML. This is a D-003 regression.
- **Proposed Fix**: Create a `_feedback_box(message, icon="✅")` helper in `_router_base.py` with standard card styling, or use `_info_card()` if the content structure matches. Alternatively, use `st.success()` / `st.info()` which Streamlit renders with consistent styling.
- **Effort**: 0.5-1h

#### D-109 Details
- **Location**: `_summary.py` lines 183-288 vs `_health.py` lines 46-163
- **Issue**: `_render_story_card()` in `_summary.py` contains ~100 lines of inline benchmark data fetching (API calls, metric computation for gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe) that duplicates the logic in `_fetch_benchmark_health_scores()` from `_health.py`. Both functions follow identical patterns: look up `INDUSTRY_BENCHMARKS` → fetch benchmark data → compute metrics → call `compute_health_scores()`. This is a D-003 regression (duplicated logic across files).
- **Proposed Fix**: Extract benchmark health score fetching into a shared service function (e.g., `health_scoring.get_benchmark_scores(client, industry, stock_id)`). Both `_health.py` and `_summary.py` call this function. This also resolves D-106 (architecture debt).
- **Effort**: 1-2h
- **Note**: The architect's review (review38_architect.md) already identified this as D-107. D-109 is the design counterpart.

---

### Sprint 18 Design Readiness

#### C139 "Explain This Number" — Design Considerations
- **Popover pattern**: Decision to use `st.popover()` with `💡` trigger button is sound. The existing `_render_metric_popover()` in `_financial.py` proves the pattern works. Extending to 5-7 metrics on the business card page is the right scope.
- **Key design risk**: The `💡` button must be subtle (0.8rem, no border, light gray) to avoid visual clutter on a page that already has 15+ sections. Must not compete with the primary metric value for attention.
- **Shared component opportunity**: The new `_explain_button()` helper in `_router_base.py` (planned) should follow the design system's button conventions — unique `key` following `{function}_{stock_id}` format.
- **Ten-second test**: The popover content must answer "what does this number mean?" in <10 seconds. Template explanations from D5 are already written at the right reading level.
- **Scope concern**: 5-7 metrics is appropriate for Sprint 18. Expanding to all 15+ metrics across all pages would risk quality. The business card page is the highest-impact location.
- **Tone QA**: C139 content must pass the expanded tone blocklist (值得關注, 需要密切關注, 表現優於預期 are flagged). Current D5 templates contain some of these phrases — needs audit before C139 ships.

#### C141 "Source Badge" — Design Considerations
- **Design is minimal by intent**: `st.caption()` at 0.7rem gray text is the right approach. No new component needed. The `ExplanationResponse.source` field already exists ("delta_template", "template", etc.).
- **Badge text options**: `📊 系統估算` (template-based) vs `📊 FinMind` (API data) — the distinction matters for trust transparency. Template explanations are generated, not sourced from data.
- **Placement**: Should appear directly below the explanation text, not separated by whitespace. `st.caption()` naturally renders close to the preceding element.
- **Competitive justification**: Public.com and Finimize both show source/confidence on explanations. This is table stakes for any "explain this" feature. Users increasingly expect to know if content is AI-generated or data-sourced.
- **Risk**: Low. This is a 2-3h bundled task with zero visual complexity.

#### C143 "Implication Sentence" — Design Considerations
- **Highest design risk in Sprint 18**: The implication sentence borders on investment advice. The approved framing — "如果你正在觀察這家公司，[factual past-tense observation]" — is the right historian approach.
- **Card replacement design**: The decision to REPLACE (not supplement) the existing explanation on delta cards is critical. The existing explanation moves to the 💡 popover. This prevents card overload and keeps the implication sentence as the primary takeaway.
- **Card styling**: Using `_白话_card()` with `label="觀察重點"` and the implication sentence in the analogy field is consistent with existing patterns. No new card type needed.
- **Tone QA is non-negotiable**: The expanded blocklist (建議, 應該, 買, 賣, 推薦, 進場, 出場, 值得關注, 需要密切關注, 值得持續追蹤, 表現優於預期) must be enforced. Current `delta_explanation_provider.py` templates contain "值得關注後續動能" and "需要密切關注" — these MUST be rewritten before C143 ships.
- **Content creation effort**: Writing implication templates for 3 delta metric types × directions (up/down) = 6 templates minimum. Each must pass tone QA. Budget 2-3h for content creation and review.
- **Visual separation**: The implication sentence should be visually distinct from the raw delta value. Using the analogy field (italic, green text per design system) provides this separation naturally.

---

### Competitor Design Patterns

1. **Magnify.money "Explain This Number"**: Every metric has a one-click explanation with analogy + plain language. The explanation appears in a popover (not a new page). Key insight: Magnify uses a **lightbulb icon** (💡) as the universal "explain this" trigger — exactly what C139 plans. Their explanations are 1-2 sentences max, matching our design system's 200-character text limit.

2. **Public.com Story Cards**: Public.com displays stock narratives as "story cards" with a clear hierarchy: (1) headline metric, (2) plain-language explanation, (3) source badge at the bottom in small gray text. The source badge reads "Based on [source]" in 0.7rem text — nearly identical to C141's `st.caption()` approach. Public.com also uses implication-like sentences: "Revenue grew 15% — this suggests strong demand." C143's framing is more hedged ("如果你正在觀察這家公司") which is appropriate for the historian positioning.

3. **Koyfin Metric Descriptions**: Koyfin shows metric descriptions as **hover tooltips** (not popovers). Each metric name is underlined with a dotted line; hovering reveals a 1-2 sentence definition. For TW market beginners, hover is less discoverable than an explicit 💡 button. C139's popover-first approach is more beginner-friendly. Koyfin also groups related metrics under expandable section headers — similar to our `_section_title()` + `st.expander()` pattern.

4. **Source Badge Patterns (Finimize / Public.com)**: Finimize uses a **confidence meter** (bar indicator) showing explanation reliability. Public.com uses a simple text badge ("Based on company filings" / "System estimate"). For Stock Explorer, the `ExplanationResponse.source` field maps cleanly: "template" → `📊 系統估算`, API data → `📊 FinMind`. The `st.caption()` approach is the right level of subtlety — visible but not competing with content.

5. **Implication Sentence Patterns (FinChat / Inderes / Stockstory)**: Three distinct approaches found: (A) **FinChat.io** uses "Data → Context → Implication" three-part structure — the most sophisticated. (B) **Inderes.fi** uses direct "This implies that..." language. (C) **Stockstory** uses a dedicated "💡 So What?" box with distinct visual treatment (amber background, separate from data card). Stock Explorer's C143 uses approach B (direct historian framing) but could evolve toward approach C in a future sprint (C149 "So What?" box). The current approach is the safest for tone compliance.

6. **Simply Wall St Benchmark Ghost Layer**: Simply Wall St overlays industry average as a **dashed gray line** on their snowflake chart — visually identical to C14's ghost-line pattern. This validates C14's design as an industry-standard pattern. Simply Wall St also shows the benchmark company name in the legend (not just "industry average") — C14 does this correctly with `benchmark_label`.

---

### Top 3 Design Recommendations

1. **Audit and rewrite delta_explanation_provider.py templates before C143 ships** (Priority: 🔴 BLOCKING)
   - Current templates contain tone blocklist violations: "值得關注後續動能" (line 30), "需要密切關注" (line 35). These phrases trigger the expanded tone blocklist and would fail CI if `tests/test_tone_qa.py` is implemented as planned.
   - Rewrite to factual past-tense: e.g., "可能是大訂單入帳或旺季效應，動能變化值得持續觀察" → "可能是大訂單入帳或旺季效應，後續動能可留意"
   - Effort: 1-2h for template audit + rewrite. Must be done before C143 development starts.
   - This directly supports Sprint 18's Tone QA automation task (2-3h CI pipeline addition).

2. **Extract `_feedback_box()` shared component from settings.py inline HTML** (Priority: 🟢 Quick win, 0.5-1h)
   - The two visual feedback boxes in `settings.py` (lines 101-108, 168-176) are near-exact copies of `_info_card()` styling but implemented as inline HTML. This is a D-003 regression.
   - Create `_feedback_box(message, icon="✅")` in `_router_base.py` or replace with `_info_card()` / `st.success()` calls.
   - This should be done during C07 enhancements or as a standalone cleanup. It sets the pattern for future settings page additions.

3. **Plan C149 "So What?" implication box as a future visual enhancement** (Priority: 📋 Sprint 19+)
   - Stockstory's "💡 So What?" box pattern (distinct visual card with amber background after each metric section) is the natural evolution of C143. C143 generates the content (Sprint 18); C149 gives it the visual treatment.
   - Design spec: warm amber background (`#FFF8E1` — matches design system tip background), `💡 這代表什麼?` header, 14px implication text, "了解更多" expand for detailed explanation.
   - This separates data (what happened) from implication (what it means) more clearly than the current `_白话_card()` analogy field approach.
   - No action needed in Sprint 18 — document as future enhancement.

---

### Summary

Sprint 17 design quality remains at **Grade A** (5th consecutive). The benchmark overlay (C14) is a clean, industry-standard ghost-line pattern. C134's protocol-based design is architecturally sound. C07's settings page is functional with minor inline HTML issues. Two new P2 design debt items (D-108, D-109) are identified but non-blocking.

Sprint 18 design readiness is **strong**. C139 extends a proven popover pattern. C141 is minimal by design. C143 carries the highest tone risk but has clear historian framing and tone QA gates. The top priority is auditing delta_explanation_provider.py templates for tone blocklist violations before C143 development begins.

### Design Debt Tracker (Cumulative)

| ID | Source | Severity | Status |
|----|--------|----------|--------|
| D-003 | Inconsistent card styling | P1 | Partially fixed (ongoing) |
| D-006 | Mobile responsiveness | P1 | Open |
| D-039 | No standardized section header | P2 | Open |
| D-040 | No standardized disclaimer | P2 | Open |
| D-097 | D5 templates ignore industry context | P2 | Sprint 18 Day 1 task |
| D-108 | Settings inline HTML feedback boxes | P2 | **NEW** — fix during C07 enhancements |
| D-109 | Benchmark logic duplicated in _summary.py | P2 | **NEW** — extract to shared service |
