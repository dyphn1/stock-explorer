# Stock Explorer — Developer Estimates: Round 14 Review Items

> **Date**: 2026-06-19
> **Author**: Developer
> **Sprint Status**: Sprint 3 completing (C38 + D16 remaining), Sprint 4 starting
> **Codebase**: ~6,800 LOC across `src/`, 12 service modules, 12 page modules, 4-layer architecture
> **Confidence**: High for design fixes and architecture debt. Medium-High for new features (based on thorough codebase review and competitor research).

---

## Codebase Context for Estimation

**Current State**: `business_card.py` is 561 lines. `analogy_engine.py` is 850 lines. `risk_analyzer.py` is 567 lines (clean service layer, zero Streamlit/API imports). `_router_base.py` is 177 lines (mixes data loading + UI helpers).

**Key Patterns Observed**:
- Service modules: pure functions, no Streamlit imports, threshold-based classification
- YAML config files: proven pattern for content (company_facts, events, watchlist)
- Session state: ad-hoc pattern, 8+ keys in business_card.py alone
- Chart module: consistent `_apply_theme_layout` pattern, Plotly-based
- `_router_base.py`: provides `_白话_card()`, `_info_card()`, `_summary_card()` — but `_summary_card()` has wrong background color (#FFF8F0 instead of #F8F9FA)
- `business_card.py` C41 section (lines 504-544): inline HTML for peer cards + direct `client.get_stock_info()` call in view layer
- `business_card.py` C44 section (lines 66-83): `_render_risk_dimension()` uses `#FFF8F0` background instead of `#F8F9FA`
- `business_card.py` C44 section (lines 53-61): `_RISK_BADGES` and `_RISK_COLORS` constants embedded in page file
- Design system: `#F8F9FA` is the standard card background. `#FFF8F0` (warm orange tint) and `#F5F5F5` (medium gray) are violations.

**Verification Overhead**: All changes require L0 (import/syntax) + L1 (layer architecture) verification. New features additionally need L2 (cross-page integration) verification. Estimates include verification time.

---

## Part 1: Design Fixes (Round 14 Design Review)

### D-035: Fix C41 Peer Cards to Use Shared Components

| Attribute | Value |
|-----------|-------|
| **Effort** | 1.5–2.5h |
| **Complexity** | Low-Medium |
| **Priority** | P2 |
| **Dependencies** | None (can be done independently) |

**What needs to change**:
- `business_card.py` lines 516-539: Replace inline HTML string concatenation (`_peer_html = f"<div>..."`) with a shared component function
- Create `render_peer_card(peer_name, peer_id, peer_industry, navigate_fn)` helper — either in `_router_base.py` or inline in the page
- The peer card HTML uses inline styles that duplicate the `_info_card()` / `_白话_card()` visual pattern but with different CSS
- Extract to a reusable function, then call it in the loop

**Technical risks**:
- Low risk: purely presentational refactor, no logic changes
- Risk of slightly changing card appearance during migration — must match existing design exactly
- The `navigate_to()` call within the button must be preserved correctly

**Batching**: Can be combined with D-038 (moving API call to router) since both touch C41 code. Combined batch: 2.5–4h.

---

### D-036: Fix C44 Risk Cards Background Color

| Attribute | Value |
|-----------|-------|
| **Effort** | 0.25–0.5h (15–30 min) |
| **Complexity** | Low |
| **Priority** | P2 |
| **Dependencies** | None |

**What needs to change**:
- `business_card.py` line 72: Change `background:#FFF8F0` → `background:#F8F9FA` in `_render_risk_dimension()`
- This is a single-line CSS string change inside the `_render_risk_dimension()` function
- The border-left color (based on risk level) should remain unchanged — only the background changes

**Technical risks**:
- Trivial change. Verify that `#F8F9FA` renders correctly with the existing border-left colors (#E74C3C, #F39C12, #27AE60)
- Must verify all 3 risk levels still look good against the new background

**Batching**: Can be combined with D-037 (same type of fix, same file area). Combined: 0.5–1h.

---

### D-037: Fix _白话_card Background Color

| Attribute | Value |
|-----------|-------|
| **Effort** | 0.25h (15 min) |
| **Complexity** | Low |
| **Priority** | P2 |
| **Dependencies** | None |

**What needs to change**:
- `_router_base.py` line 91: Change `background:#F5F5F5` → `background:#F8F9FA` in `_白话_card()`
- This affects ALL pages that use `_白话_card()` (business_card.py, operation_checkup.py, financial_health.py, peer_comparison.py)
- Single-line change in the shared component

**Technical risks**:
- Very low risk: one-line change in a shared component
- Must verify visual consistency across all pages that use `_白话_card()` — the change from medium gray (#F5F5F5) to light gray (#F8F9FA) is subtle
- L0/L1 verification will catch any import issues; visual check across 4 pages needed

**Batching**: Can be combined with D-036 (both are color fixes). Combined: 0.5–1h.

---

### D-038: Move C41 API Call from View Layer to Router Data Dict

| Attribute | Value |
|-----------|-------|
| **Effort** | 1.5–2.5h |
| **Complexity** | Low-Medium |
| **Priority** | P2 |
| **Dependencies** | None |

**What needs to change**:
- `business_card.py` lines 505-512: Remove `client.get_stock_info()` call and `_peers` DataFrame construction from the view layer
- `_router_base.py` `get_stock_data()`: Add a new task `("peer_stocks", lambda: _get_peer_stocks(client, stock_id, industry))` to the tasks list
- The `_get_peer_stocks()` helper filters `client.get_stock_info()` by industry, excludes current stock, returns top 5
- `business_card.py` receives `data["peer_stocks"]` pre-computed
- The `client` parameter in `_render_business_card(data, client)` is currently used for `get_stock_info()` in C41 — after this fix, `client` may no longer be needed for the peer section (though it's still used for other things)

**Technical risks**:
- Medium risk: Moving data loading to the ThreadPoolExecutor changes the loading sequence. The peer stocks load in parallel with other data, but the `industry` value comes from `stock_info` which is fetched sequentially first — this is fine since the gate check already completed
- Must ensure `peer_stocks` is `None`-safe in the view (handle missing key gracefully)
- The `_get_peer_stocks()` function needs to handle cases where `get_stock_info()` returns empty
- Small risk: the current implementation creates a new `FinMindClient` in `_render_business_card` if none provided — after this change, the client from the router's ThreadPoolExecutor context should be reused

**Batching**: Should be combined with D-035 (both modify C41 code in business_card.py). Combined: 2.5–4h.

---

## Part 2: Architecture Debt (Round 14 Architecture Review)

### D24: Extract business_card.py to Sub-directory

| Attribute | Value |
|-----------|-------|
| **Effort** | 2–3h (confirmed from tech_debt.md) |
| **Complexity** | Medium |
| **Priority** | 🔴 HIGH — Must be FIRST in Sprint 4 |
| **Dependencies** | None (prerequisite for C48, D32, D33) |

**What needs to change**:
- Create `src/pages/business_card/` sub-directory with `__init__.py`
- Split `business_card.py` (561 lines) into section files:
  - `sections/read_next.py` (C41, ~60 lines + extracted peer logic)
  - `sections/risk.py` (C44, ~114 lines)
  - `sections/delta.py` (C39, ~40 lines)
  - `sections/summary.py` (C37, ~30 lines)
  - `sections/metrics.py` (key numbers, dividend, ~80 lines)
  - `sections/base.py` (shared layout, watchlist buttons, ~60 lines)
  - `__init__.py` re-exports `_render_business_card`
- Update all imports in `router.py`
- Move presentation helpers (`get_health_dimension_explanation`, `_render_risk_dimension`, `_RISK_BADGES`, `_RISK_COLORS`) to section files or shared module

**Technical risks**:
- Medium risk: import chain changes. `router.py` imports `_render_business_card` from `business_card.py` — must update to `business_card.__init__.py`
- All session_state keys must remain accessible (no breakage to watchlist popup state)
- The `client` parameter in `_render_business_card(data, client)` must be passed through correctly
- L0 verification will catch import errors; L1 ensures no layer violations introduced
- This is a pure refactor — no behavior changes. Existing tests (if any) must still pass.

**Batching**: This is the Sprint 4 opener. D16 can follow immediately after.

---

### D16: Split analogy_engine.py

| Attribute | Value |
|-----------|-------|
| **Effort** | 2–3h (confirmed from tech_debt.md) |
| **Complexity** | Medium |
| **Priority** | 🔴 HIGH — Must complete before C48 |
| **Dependencies** | None (prerequisite for C48's story_composer.py) |

**What needs to change**:
- `analogy_engine.py` (850 lines) → split into 4 modules:
  - `src/services/analogy_engine.py` — keep only analogy functions (lines 1–136, ~90 lines after cleanup)
  - `src/services/key_takeaways.py` — `generate_key_takeaways()` + `_KEY_TAKEAWAYS` data (~150 lines)
  - `src/services/delta_engine.py` — `compute_recent_deltas()` + `explain_delta()` (~120 lines)
  - `src/services/health_scoring.py` — all `_score_*` + `compute_health_scores()` + `get_health_summary()` (~270 lines)
- Update imports in all consumers: `business_card.py`, `operation_checkup.py`, `financial_health.py`, `peer_comparison.py`, `chart.py`, `financial_metrics.py`
- Update `src/services/__init__.py` if needed

**Technical risks**:
- Medium risk: Many import statements across the codebase reference `analogy_engine.py`. Each must be updated to the correct new module
- The `_KEY_TAKEAWAYS` dict (120 lines of hardcoded data) moves to `key_takeaways.py` — this is a pure data relocation
- Health scoring functions are pure functions — no state to worry about
- L0 will catch any missed imports; L1 ensures no new layer violations
- Risk: circular imports if modules reference each other. Mitigation: analogy_engine.py should not import from the new modules (it's the base layer)

**Batching**: Sequential after D24. Total D24 + D16: 4–6h. Should be first two items of Sprint 4.

---

### D31: Monitor risk_analyzer.py

| Attribute | Value |
|-----------|-------|
| **Effort** | 0h (monitoring only) |
| **Complexity** | N/A |
| **Priority** | Low |
| **Dependencies** | N/A |

**Assessment**: `risk_analyzer.py` is 567 lines with clean architecture (zero Streamlit imports, zero API calls). Well-structured internally with 3 independent assessment functions + 7 helpers + orchestrator. No immediate action needed.

**Trigger for action**: If additional risk dimensions (volatility, cyclicality, governance) are added, pushing it beyond ~700 lines, split into `customer_risk.py`, `financial_risk.py`, `event_risk.py`.

---

### D32: Move Presentation Helpers to Shared UI Module

| Attribute | Value |
|-----------|-------|
| **Effort** | 1–2h |
| **Complexity** | Low-Medium |
| **Priority** | P2 |
| **Dependencies** | D24 (best done during business_card.py extraction) |

**What needs to change**:
- `business_card.py` lines 43-83: Move 3 presentation functions to shared module
  - `get_health_dimension_explanation(dim_name, score)` — pure function, reusable
  - `_render_risk_dimension(dim, stock_name)` — renders risk card HTML
  - `_RISK_BADGES` and `_RISK_COLORS` dicts — style constants
- Options for destination:
  - Extend `_router_base.py` (simplest, but adds to an already mixed-concern file)
  - Create `src/services/ui_components.py` (cleanest, but new file)
  - Add to the `business_card/sections/` files during D24 extraction (most targeted)
- Recommended: Move to `_router_base.py` during D24 extraction since that's where other UI helpers live

**Technical risks**:
- Low risk: pure refactoring, no behavior changes
- `_render_risk_dimension()` uses `st.markdown(..., unsafe_allow_html=True)` — this is a UI function, belongs in presentation layer
- If moved to `_router_base.py`, the file grows slightly but stays under 250 lines
- Must update imports in `business_card.py` (or section files after D24)

**Batching**: Do during D24 extraction. Marginal additional cost: 0.5–1h on top of D24.

---

### D33: Move C41 Data Access to Router

| Attribute | Value |
|-----------|-------|
| **Effort** | 0.5–1h |
| **Complexity** | Low |
| **Priority** | P2 (Low per tech_debt.md) |
| **Dependencies** | None (but best done with D-038 which addresses the same issue) |

**What needs to change**:
- Same as D-038 above. D-038 is the design review version; D33 is the architecture review version. They are the same fix.
- Pre-compute peer stocks in `_router_base.py`'s `get_stock_data()` and include in `data` dict

**Technical risks**: Same as D-038. Low priority since `get_stock_info()` is cached by FinMindClient.

**Batching**: This IS D-038. Single fix addresses both issues. 1.5–2.5h total.

---

## Part 3: New Features (Round 14 Competitor Research)

### C69: Paper Trading Simulator

| Attribute | Value |
|-----------|-------|
| **Effort** | 16–24h |
| **Complexity** | High |
| **Priority** | P2 |
| **Dependencies** | D24 (business_card.py extraction — if adding portfolio section to business card) |

**What needs to change**:
- New `src/pages/simulator.py` — portfolio management page with buy/sell interface
- New `src/services/virtual_portfolio.py` — portfolio CRUD, P&L calculation, position tracking
- New `config/virtual_portfolio.yaml` — persistent storage for virtual positions (file-lock pattern from watchlist.py)
- New `src/services/portfolio_chart.py` — portfolio performance chart (reuses chart.py theme)
- Router integration: Add "模擬交易" to navbar
- UI components: Position table, buy/sell form, performance summary card, transaction history

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `virtual_portfolio.py` service | 3h | 4h | CRUD + P&L calc + file persistence. ~150 LOC |
| `simulator.py` page | 4h | 6h | Buy/sell form, position table, summary cards. ~200 LOC |
| Portfolio performance chart | 2h | 3h | Equity curve + benchmark comparison. Reuses chart theme |
| Portfolio analytics service | 2h | 3h | Return calculation, diversification metrics |
| Content: initial stock universe | 1h | 2h | Seed with top 50 stocks by market cap |
| Router + navbar integration | 0.5h | 1h | Add to router.py |
| Testing & edge cases | 1.5h | 2h | Empty portfolio, sell more than held, concurrent writes |
| **Total** | **14h** | **21h** | **Midpoint: 17.5h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Position tracking complexity (splits, dividends) | Medium | Incorrect P&L | MVP: track shares + cost basis only. Ignore splits/dividends initially |
| File lock contention with watchlist.yaml | Medium | Slow writes | Separate `virtual_portfolio.yaml` with own lock |
| Real-time price updates | Medium | Stale prices | Use FinMind cached prices (same as rest of app). No real-time requirement |
| Position validation (sell > held) | Low | Negative positions | Validate on sell. Reject if insufficient shares |
| Historian positioning risk | Medium | Feature feels like "stock picker" | Frame as "Practice what you learned" — educational, not competitive. No leaderboard |

**Recommended Approach**:
1. Create `virtual_portfolio.py` with `buy(stock_id, shares, price)`, `sell(stock_id, shares, price)`, `get_positions()`, `get_performance()`
2. Create `simulator.py` page with: portfolio summary → buy/sell form → position table → performance chart
3. Store positions in `config/virtual_portfolio.yaml` with file-lock pattern
4. **Scope control**: No short selling, no margin, no options. Shares only. Start with 10 pre-loaded stocks.
5. **Positioning**: "練習模式" (Practice Mode) framing. "You've analyzed 12 companies — now practice what you learned."

---

### C70: "Why This Matters" Conclusion

| Attribute | Value |
|-----------|-------|
| **Effort** | 6–10h |
| **Complexity** | Medium |
| **Priority** | P1 |
| **Dependencies** | D24 (if adding to business_card.py) |

**What needs to change**:
- New `src/services/conclusion_engine.py` — generates "Why This Matters" narrative for each stock
- New section in business_card.py (or `business_card/sections/conclusion.py` after D24)
- Template-based narrative synthesis: combines key takeaways + health scores + risk summary into 3-5 sentence conclusion
- Plain-language, historian tone: "Based on what we know about [company], here's what matters for understanding this company"
- NOT investment advice — purely educational synthesis of existing data

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `conclusion_engine.py` service | 2.5h | 4h | Template-based synthesis from existing data. ~120 LOC |
| Conclusion UI component | 1h | 2h | Card component with icon + narrative text. Reuses `_info_card` pattern |
| Integration into business_card.py | 1h | 2h | Add section at bottom of page (before Read Next). Requires D24 if file > 600 LOC |
| Content templates | 1.5h | 2h | 5-6 conclusion templates based on company archetype (growth, value, dividend, cyclical, etc.) |
| **Total** | **6h** | **10h** | **Midpoint: 8h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Conclusion sounds like investment advice | Medium | Positioning violation | Strict template review. No forward-looking language. Historian tone enforcement |
| Generic/repetitive conclusions | Medium | Users stop reading | Use data-driven templates (different conclusions for different company archetypes) |
| Integration with business_card.py bloat | High | File exceeds 600 lines | Must do D24 first. Add to `sections/conclusion.py` in sub-directory |

**Recommended Approach**:
1. Create `conclusion_engine.py` with `generate_conclusion(data) -> str` — pure function
2. Templates based on company archetype (determined from health_scores + extra_metrics)
3. Add conclusion section as the LAST section on business card (before disclaimer)
4. **Scope control**: 3-5 sentences max. No charts. Pure narrative synthesis.

---

### C71: Learning Streak

| Attribute | Value |
|-----------|-------|
| **Effort** | 8–12h |
| **Complexity** | Medium |
| **Priority** | P2 |
| **Dependencies** | None (standalone feature) |

**What needs to change**:
- New `src/services/learning_streak.py` — tracks daily learning activity, computes streak
- New `config/learning_streak.yaml` — persistent storage for streak data (file-lock pattern)
- Session state integration: `st.session_state["learning_streak"]`
- UI components: Streak counter widget (sidebar or homepage), streak milestone badges
- Activity tracking: page views, stocks analyzed, quiz answers, etc.

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `learning_streak.py` service | 2.5h | 4h | Streak calculation, activity recording, persistence. ~150 LOC |
| Streak UI widget | 2h | 3h | Streak counter + milestone display. Reuses card components |
| Activity tracking integration | 1.5h | 2.5h | Hook into router.py to record page views as learning activity |
| Milestone badges | 1h | 1.5h | 7-day, 30-day, 100-day milestones with celebration UI |
| Testing & edge cases | 1h | 1h | Streak reset, timezone handling, first visit |
| **Total** | **8h** | **12h** | **Midpoint: 10h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Session state loss on refresh | High | Streak resets | Persist to YAML file (like watchlist). Read on page load |
| Timezone handling for "daily" | Medium | Streak breaks incorrectly | Use server time (UTC+8 for TW). Acceptable for MVP |
| Activity definition ambiguity | Medium | Streak feels arbitrary | Define clearly: "analyzed 1 stock page = 1 learning activity" |
| Gamification vs. education balance | Low | Feature feels gimmicky | Keep it subtle. Streak counter in sidebar, not hero section |

**Recommended Approach**:
1. Create `learning_streak.py` with `record_activity(activity_type)`, `get_streak()`, `get_milestones()`
2. Persist to `config/learning_streak.yaml` with date-stamped activity log
3. Show streak counter in sidebar (below stock search) — "🔥 連續學習 N 天"
4. **Scope control**: No leaderboard, no social sharing. Personal streak only. Milestone badges at 7/30/100 days.

---

### C72: TL;DR First

| Attribute | Value |
|-----------|-------|
| **Effort** | 4–8h |
| **Complexity** | Low-Medium |
| **Priority** | P1 |
| **Dependencies** | None (can be added to any page independently) |

**What needs to change**:
- New `src/services/tldr_engine.py` — generates one-paragraph summary for each page/company
- Modify `business_card.py` (or `business_card/sections/base.py` after D24) to show TL;DR at top
- Template-based: combines one-liner + key takeaway + health score into 2-3 sentence summary
- UI: Expandable "TL;DR" card at the top of each page — collapsed by default on subsequent visits

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `tldr_engine.py` service | 1.5h | 2.5h | Template-based synthesis. ~80 LOC |
| TL;DR UI component | 1h | 2h | Expandable card at top of page. Reuses `_info_card` pattern |
| Integration into business_card.py | 0.5h | 1.5h | Add as first section. Requires D24 if file > 600 LOC |
| Session state: collapse preference | 0.5h | 1h | Remember if user collapsed TL;DR |
| Testing & edge cases | 0.5h | 1h | Missing data, very long summaries |
| **Total** | **4h** | **8h** | **Midpoint: 6h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| TL;DR duplicates C37 summary | High | Redundant content | Position TL;DR as "ultra-short" (2-3 sentences) vs C37's "short" (5 bullets) |
| Generic summaries | Medium | Users don't read them | Use data-driven templates. Different TL;DR for different company types |
| Clutter at top of page | Low | Overwhelms users | Collapsible by default. "點擊查看重點" label |

**Recommended Approach**:
1. Create `tldr_engine.py` with `generate_tldr(data) -> str` — pure function, 2-3 sentences
2. Add TL;DR card as the FIRST section on business card (below header, above key takeaways)
3. **Scope control**: One paragraph only. No charts. No expandable details. Pure text summary.
4. **Positioning**: "10 秒版本" (10-second version) — aligns with "ten-second test" design principle.

---

### C73: Super Investor Thesis

| Attribute | Value |
|-----------|-------|
| **Effort** | 12–16h |
| **Complexity** | High |
| **Priority** | P1 |
| **Dependencies** | D24 (business_card.py extraction) |

**What needs to change**:
- New `src/services/investor_thesis.py` — generates "super investor" investment thesis for each stock
- New `config/super_investor_theses.yaml` — curated theses for top 30 stocks (content creation: ~8h)
- New section in business_card.py (or `business_card/sections/thesis.py` after D24)
- UI: "超級投資人的觀點" card with investor name, thesis summary, key metrics they care about
- Historian framing: "Here's what famous investors have said about this company" — past tense, factual

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `investor_thesis.py` service | 2h | 3h | Load YAML, lookup by stock, return structured data. ~80 LOC |
| `super_investor_theses.yaml` content | 4h | 6h | 30 stocks × (investor name, thesis text, key metrics, source). Content creation heavy |
| Thesis UI component | 2h | 3h | Card with investor avatar placeholder, thesis text, key metrics highlight |
| Integration into business_card.py | 1.5h | 2.5h | Add section. Requires D24 if file > 600 LOC |
| Testing & edge cases | 0.5h | 1h | Missing thesis, very long text |
| **Total** | **10h** | **15.5h** | **Midpoint: 13h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Investment advice perception | High | Positioning violation | Strict historian framing: "Warren Buffett said in 2019..." — past tense, attributed quotes only |
| Content accuracy | Medium | Misattributed quotes damage credibility | Only use well-documented, public statements. Source every thesis |
| Content creation bottleneck | High | 30 theses is a lot | Start with 10 stocks (TSMC,鴻海,聯發科,台達電,富邦金,台泥,中鋼,台塑,華碩,廣達) |
| Thesis becomes outdated | Low | Stale content | Add date field to YAML. Show "as of YYYY" disclaimer |

**Recommended Approach**:
1. Create `super_investor_theses.yaml` with 10 pilot stocks (not 30)
2. Create `investor_thesis.py` — pure function: `get_thesis(stock_id) -> dict`
3. Add thesis section to business card (after health scores, before risk analysis)
4. **Scope control**: 10 stocks MVP. One thesis per stock. 2-3 sentences max. Attributed quotes only.
5. **Positioning**: "超級投資人的觀點" — educational, not advisory. Always past tense + attributed.

---

### C74: Interactive What-If Scenarios

| Attribute | Value |
|-----------|-------|
| **Effort** | 14–20h |
| **Complexity** | High |
| **Priority** | P1 |
| **Dependencies** | D24 (business_card.py extraction) |

**What needs to change**:
- New `src/services/what_if_engine.py` — calculates scenario outcomes based on user inputs
- New section in business_card.py (or `business_card/sections/what_if.py` after D24)
- UI: Interactive sliders/inputs for key variables (revenue growth %, margin change, etc.)
- Real-time recalculation of health scores, valuation, and risk based on scenario
- Historian framing: "What would the numbers look like IF..." — educational exploration, not prediction

**Sub-estimates**:
| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `what_if_engine.py` service | 3h | 5h | Scenario calculation engine. Pure functions. ~200 LOC |
| What-If UI component | 3h | 5h | Sliders + real-time chart updates. Streamlit reactive pattern |
| Scenario templates | 2h | 3h | 5-6 pre-built scenarios (revenue +20%, margin -5%, etc.) |
| Chart: scenario comparison | 2h | 3h | Side-by-side or overlay chart. Reuses chart.py theme |
| Integration into business_card.py | 1.5h | 2.5h | Add section. Requires D24 if file > 600 LOC |
| Testing & edge cases | 1.5h | 2.5h | Extreme values, negative margins, missing data |
| **Total** | **13h** | **21h** | **Midpoint: 17h** |

**Technical risks**:
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Users interpret scenarios as predictions | High | Positioning violation | Clear labeling: "這是假設情境，不是預測" (This is a hypothetical scenario, not a prediction) |
| Complex UI in Streamlit | Medium | Clunky interaction | Use `st.slider()` + `st.session_state` for reactivity. Keep it simple: 3-4 sliders max |
| Calculation accuracy | Medium | Wrong scenario results | Use simple linear models. Document assumptions clearly |
| Performance with real-time updates | Low | Slow page interaction | Debounce slider changes. Cache base calculations. |

**Recommended Approach**:
1. Create `what_if_engine.py` with `calculate_scenario(base_data, adjustments) -> dict` — pure function
2. UI: 3 sliders (營收變化 %, 毛利率變化 %, 負債比變化 %) + "重置" button
3. Show scenario impact on: health scores (radar chart update), risk level, valuation
4. **Scope control**: 3 variables only. Linear models only. No Monte Carlo. No probability distributions.
5. **Positioning**: "如果...會怎樣？" — educational exploration tool. Always show "實際數據 vs 假設情境" comparison.

---

## Consolidated Effort Table

### Design Fixes (D-035 to D-038)

| ID | Item | Low (h) | High (h) | Mid (h) | Complexity | Priority |
|----|------|---------|----------|---------|------------|----------|
| D-035 | C41 peer cards → shared components | 1.5 | 2.5 | 2.0 | Low-Medium | P2 |
| D-036 | C44 risk cards color #FFF8F0→#F8F9FA | 0.25 | 0.5 | 0.4 | Low | P2 |
| D-037 | _白话_card color #F5F5F5→#F8F9FA | 0.25 | 0.5 | 0.4 | Low | P2 |
| D-038 | C41 API call → router data dict | 1.5 | 2.5 | 2.0 | Low-Medium | P2 |
| **Design Fixes Total** | | **3.5** | **6.0** | **4.8** | | |

### Architecture Debt (D24, D16, D31, D32, D33)

| ID | Item | Low (h) | High (h) | Mid (h) | Complexity | Priority |
|----|------|---------|----------|---------|------------|----------|
| D24 | business_card.py → sub-directory | 2 | 3 | 2.5 | Medium | 🔴 HIGH |
| D16 | Split analogy_engine.py | 2 | 3 | 2.5 | Medium | 🔴 HIGH |
| D31 | Monitor risk_analyzer.py | 0 | 0 | 0 | N/A | Low |
| D32 | Move presentation helpers to shared UI | 1 | 2 | 1.5 | Low-Medium | P2 |
| D33 | C41 data access → router (same as D-038) | — | — | — | Low | P2 |
| **Architecture Debt Total** | | **5** | **8** | **6.5** | | |

### New Features (C69-C74)

| ID | Feature | Low (h) | High (h) | Mid (h) | Complexity | Priority |
|----|---------|---------|----------|---------|------------|----------|
| C69 | Paper Trading Simulator | 16 | 24 | 20 | High | P2 |
| C70 | "Why This Matters" Conclusion | 6 | 10 | 8 | Medium | P1 |
| C71 | Learning Streak | 8 | 12 | 10 | Medium | P2 |
| C72 | TL;DR First | 4 | 8 | 6 | Low-Medium | P1 |
| C73 | Super Investor Thesis | 12 | 16 | 14 | High | P1 |
| C74 | Interactive What-If Scenarios | 14 | 20 | 17 | High | P1 |
| **New Features Total** | | **60** | **90** | **75** | | |

### Grand Total

| Category | Low (h) | High (h) | Mid (h) |
|----------|---------|----------|---------|
| Design Fixes (D-035–D-038) | 3.5 | 6.0 | 4.8 |
| Architecture Debt (D24, D16, D32) | 5 | 8 | 6.5 |
| New Features (C69–C74) | 60 | 90 | 75 |
| **Grand Total** | **68.5** | **104** | **86.3** |

---

## Recommended Priority Order

### Sprint 4 Opener (Must Do First — 2 items, 4.5–6h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 1 | **D24** | business_card.py → sub-directory | 2–3h | 🔴 HARD PREREQUISITE. File is 561 lines. Must extract before adding ANY new sections. Blocks C48, C70, C72, C73, C74. |
| 2 | **D16** | Split analogy_engine.py | 2–3h | 🔴 HARD PREREQUISITE for C48. Must complete before story_composer.py starts. |

### Sprint 4 Parallel Track (Design Fixes — 3 items, 3.5–6h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 3 | **D-036** | C44 risk cards color fix | 0.25–0.5h | Quick win. Fix while D24 is fresh. |
| 4 | **D-037** | _白话_card color fix | 0.25h | Quick win. One-line change. |
| 5 | **D-035** + **D-038** | C41 refactor (components + router) | 2.5–4h | Batch together — both touch C41 code. Do after D24 extracts read_next.py. |

### Sprint 4 Quick Feature Win (1 item, 4–8h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 6 | **C72** | TL;DR First | 4–8h | Lowest complexity new feature. High user value. No dependencies. Can start immediately after D24. |

### Sprint 5 Features (2 items, 14–22h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 7 | **C70** | "Why This Matters" Conclusion | 6–10h | Medium complexity. Uses existing data. High educational value. |
| 8 | **C71** | Learning Streak | 8–12h | Standalone feature. No dependencies. Drives daily engagement. |

### Sprint 6 Features (2 items, 26–36h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 9 | **C73** | Super Investor Thesis | 12–16h | Content-heavy. Start content creation in Sprint 5. |
| 10 | **C74** | Interactive What-If Scenarios | 14–20h | Highest complexity new feature. Requires careful UI design. |

### Sprint 7+ Feature (1 item, 16–24h)

| Order | ID | Item | Hours | Rationale |
|-------|----|------|-------|-----------|
| 11 | **C69** | Paper Trading Simulator | 16–24h | Highest risk (positioning). Defer until education core is solid. |

---

## Batch Opportunities

### Batch 1: Color Fixes (D-036 + D-037)
- **Combined effort**: 0.5–1h
- **Rationale**: Both are single-line CSS changes. Same type of fix, same verification process.
- **Files**: `business_card.py` (D-036), `_router_base.py` (D-037)

### Batch 2: C41 Refactor (D-035 + D-038)
- **Combined effort**: 2.5–4h
- **Rationale**: Both modify C41 code in business_card.py. D-035 extracts peer card HTML to shared component; D-038 moves API call to router. Together they clean up the entire C41 section.
- **Files**: `business_card.py`, `_router_base.py`

### Batch 3: Architecture Cleanup (D24 + D16 + D32)
- **Combined effort**: 5.5–8h
- **Rationale**: D24 extracts business_card.py, D16 splits analogy_engine.py, D32 moves presentation helpers. All are architecture cleanup that should happen at Sprint 4 start.
- **Files**: `business_card.py`, `analogy_engine.py`, `_router_base.py`

### Batch 4: Education Features (C70 + C72)
- **Combined effort**: 10–18h
- **Rationale**: Both are narrative synthesis features. C72 (TL;DR) is the "ultra-short" version; C70 (Conclusion) is the "short" version. They share template patterns and can share a `narrative_engine.py` base.
- **Files**: New `tldr_engine.py` + `conclusion_engine.py` (or combined `narrative_engine.py`)

---

## Risk Register (Round 14 Items)

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| D24 extraction breaks business_card.py imports | Medium | Page doesn't render | L0 verification catches import errors. Test all section files import correctly. Keep backup of original file. |
| D16 split breaks analogy_engine consumers | Medium | Multiple pages break | Update all imports systematically. L0 verification catches misses. |
| C73 content accuracy (investor quotes) | High | Misattributed quotes damage credibility | Only use well-documented public statements. Source every thesis. Start with 10 stocks. |
| C74 scenario UI complexity in Streamlit | Medium | Clunky interaction | Keep to 3 sliders. Use session_state for reactivity. Debounce changes. |
| C69 positioning risk (paper trading = stock picker) | High | Contradicts historian framing | Frame as "練習模式". No leaderboard. No competition. Educational only. |
| C70/C72 narrative quality | Medium | Generic/repetitive text | Data-driven templates. Different outputs for different company archetypes. |
| business_card.py continues growing during Sprint 4 | High | File exceeds 600 lines despite D24 | D24 MUST be first. No feature work on business_card.py until extraction is complete. |
| Session state bloat from C71 + C72 + C74 | Medium | Performance degradation, key collisions | Namespace all keys (`streak_*`, `tldr_*`, `whatif_*`). Audit in Sprint 5. |

---

## Dependency Graph (Round 14 Items)

```
D24 (business_card.py extraction) ──→ C70 (Why This Matters)
                                    ──→ C72 (TL;DR First)
                                    ──→ C73 (Super Investor Thesis)
                                    ──→ C74 (What-If Scenarios)
                                    ──→ D-035 (C41 peer cards refactor)
                                    ──→ D-038 (C41 API call to router)

D16 (split analogy_engine.py) ────→ C48 (Company Story Card, Sprint 4)
                                    ──→ C70 (uses analogy functions)

D-036 (risk card color) ──→ (independent, can do anytime)
D-037 (_白话_card color) ──→ (independent, can do anytime)

C71 (Learning Streak) ──→ (independent, no dependencies)
C69 (Paper Trading) ──→ (independent, but defer to Sprint 7+)
```

---

## Key Recommendations

1. **D24 + D16 first, non-negotiable**: These are hard prerequisites for 5+ other items. Do them before ANY feature work in Sprint 4. Combined: 4.5–6h.

2. **Batch color fixes**: D-036 + D-037 are 0.5–1h total. Do them immediately after D24 while the files are fresh.

3. **C72 (TL;DR) as first feature**: Lowest complexity (4–8h), no dependencies, high user value. Can start immediately after D24 extraction.

4. **C73 content creation starts early**: Super Investor Thesis needs 10-30 curated theses. Start content creation in Sprint 4 as a parallel workstream (not blocking engineering).

5. **C74 is the riskiest new feature**: Highest complexity (14–20h), Streamlit UI challenges, positioning risk. Place in Sprint 6 after simpler features validate the patterns.

6. **C69 deferred to Sprint 7+**: Paper Trading has the highest positioning risk and complexity. Defer until education core (C70, C72, C73) is solid and proves the educational framing works.

7. **D32 during D24**: Move presentation helpers to shared UI module during business_card.py extraction. Marginal cost: 0.5–1h. Don't do as a separate task.

8. **D31 no action needed**: risk_analyzer.py is well-structured at 567 lines. Monitor only.

---

*Created: 2026-06-19*
*Role: Developer*
*Review cycle: Round 14*
*Confidence level: High for design fixes and architecture debt. Medium-High for new features (based on thorough codebase review of all source files, tech_debt.md, and competitor research).*
