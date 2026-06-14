# Review Round 37 — Developer Cost Estimates

> **Date**: 2026-06-14
> **Author**: Developer (💻)
> **Scope**: Sprint 17 cost validation, new feature estimates (C139–C146), technical risk assessment, debt resolution costs

---

## 1. Sprint 17 Cost Validation

### C14 Full Radar — Industry Benchmark Overlay + Story Card Integration

| Aspect | PM Estimate | Developer Estimate | Verdict |
|--------|------------|-------------------|---------|
| Effort | 4–8h | **6–10h** | Underestimated |
| Confidence | Medium | Medium-High | |

**Developer estimate: 6–10h** (recommend budgeting 8h midpoint)

**Rationale — Why higher than PM:**

1. **Benchmark overlay on snowflake is non-trivial Plotly work.** Current `create_health_snowflake()` (chart_stock.py:485–564) uses a single `go.Scatterpolar` trace with reference lines at 40/70. Adding an industry #1 benchmark overlay means:
   - A 6th data series (benchmark values) plotted on the same radar
   - Second `Scatterpolar` trace with different color/dash pattern
   - Legend updates, hover template updates (hover template at line 529–535 only shows one trace's data)
   - Color scheme revision — two overlapping translucent fills are visually confusing; likely need solid line + marker for the benchmark profile
   - **Estimated: 2–3h for just the chart work**, including visual QA in both light/dark themes

2. **Benchmark data plumbing doesn't exist.** `industry_benchmarks.yaml` maps industries → leader stock IDs (e.g., "半導體業" → "2330 台積電"). To get the benchmark *scores* for the overlay, we must:
   - Look up the industry #1 stock's health scores (call `compute_health_scores()` on the benchmark stock)
   - This requires the benchmark stock's data pipeline to be loaded — currently health scoring only runs on the *active* stock being viewed
   - Either: (a) lazy-load the benchmark stock's `extra_metrics`/`latest_per_pbr`/etc., or (b) pre-compute and cache benchmark scores in YAML
   - Option (a) is architecturally cleaner but requires threading data loading through `_render_health()`. Option (b) is simpler but adds a static data dependency
   - **Estimated: 2–3h for data plumbing**

3. **Story card integration is vague.** The plan says "integrate into story card above-fold." The current `_render_health()` (business_card/_sections/_health.py) is a standalone section called from `_main.py:234`. Moving it "above-fold" in the story card means reordering sections in `_main.py:126–234`, which is straightforward. But the story card itself (`_story.py`) currently renders deltas and compare stories — inserting health above deltas requires understanding the data flow. `_render_health()` takes `data` dict and `client`, and needs `extra_metrics`, `latest_per_pbr`, `financial`, `monthly_revenue` — all available in the main data dict. This is a **0.5h section reorder**, not hard.

4. **Written spec prerequisite.** The plan mandates a spec before implementation. I expect spec writing to take **1–1.5h** covering:
   - Benchmark overlay visual mockup (which Plotly traces, colors, legend)
   - Data flow for loading benchmark stock health scores
   - Story card placement logic
   - Edge cases: missing benchmark data, ETF industries, "其他" industry edge case

5. **Edge cases** (remaining after above):
   - ETF or industry with no benchmark leader → graceful skip
   - Benchmark leader is the same stock being viewed → show industry average instead, or skip overlay
   - Missing health score dimensions for benchmark stock → partial overlay
   - **Estimated: 1–1.5h**

**Total: 6–10h** (spec 1.5h + chart 2.5h + data plumbing 2.5h + section reorder 0.5h + edge cases 1.5h + testing buffer 1.5h)  
**Testing: +1h for L1 test adding a benchmark overlay test case**

---

### C134 Change Explanations — Refactor explain_delta() → TemplateExplanationProvider

| Aspect | PM Estimate | Developer Estimate | Verdict |
|--------|------------|-------------------|---------|
| Effort | 12–14h | **10–13h** | Slightly overestimated |
| Confidence | Medium | High | |

**Developer estimate: 10–13h** (recommend budgeting 12h midpoint)

**Rationale — Why slightly lower but with important caveats:**

1. **The refactoring target is well-scoped.** `explain_delta()` (delta_engine.py:90–164) is a 74-line function with 3 metric branches (月營收, 股價30日均價, 營收年增率) + a generic fallback. Each branch has 3 threshold tiers × 2 directions = 18 output text templates. The `TemplateExplanationProvider` (template_provider.py:94–131) already has a clean `explain(request)` method that takes `ExplanationRequest(metric_name, metric_value, delta)`.

2. **The catch: `explain_delta()` is written in zh-TW narrative style; `TemplateExplanationProvider` is in zh-CN.** The provider templates use simplified Chinese ("较上期成长", "每股获利能力减弱") while `explain_delta()` output uses traditional Chinese ("月營收暴增", "表現優於預期"). Two options:
   - **Option A**: Create a zh-TW template set in `TemplateExplanationProvider`. This doubles the template maintenance surface but is architecturally clean. **+2–3h**
   - **Option B**: Keep `explain_delta()` as the zh-TW provider, wrap it behind the `ExplanationProvider` protocol. Minimal code change, but the abstraction loses value. **+0.5h**
   - I recommend **Option A** for consistency but flag it as a scope decision.

3. **C39 regression tests** (per Challenger revision #4):
   - Write 6–8 test cases capturing current `explain_delta()` outputs across tiers × metrics
   - Must use `pytest` with fixtures for `change_pct` / `direction` / `metric_name` parameterization
   - **Estimated: 2–2.5h**

4. **Refactoring steps:**
   - Wrap `explain_delta()` results in `ExplanationResponse(text=..., source="template", confidence=1.0)` — **0.5h**
   - Create `DeltaExplanationProvider` class implementing `ExplanationProvider` that internally calls `explain_delta()` — **1h**
   - Wire `compute_recent_deltas()` to use `ExplanationProvider.explain()` instead of direct `explain_delta()` call — **0.5h**
   - Write unit tests for `DeltaExplanationProvider` — **1.5h**
   - Integration test: verify delta card output unchanged — **1h**

5. **Unknown: metric_name key mapping.** `explain_delta()` uses display names ("月營收", "股價（近 30 日均價）", "營收年增率") but `TemplateExplanationProvider` uses lowercase english keys ("revenue", "eps", "pe_ratio"). This mapping doesn't exist and must be built. **+1h**

6. **Net new: factory update.** `get_explanation_provider()` needs to return the delta provider for delta requests. **+0.5h**

**Total with Option A: 10–13h**  
**Total with Option B: 8–10h** (less consistent architecture)  
**Testing: 2.5h included above**

**⚠️ KEY RISK (D-101):** `explain_delta()` has zero tests. The Challenger correctly mandated C39 regression tests before refactoring. If the regression tests miss edge cases (e.g., boundary at exactly 30%, 50%), the refactoring could silently change behavior. Budget the full 2.5h for regression tests — skip at your peril.

---

### C07 Wire Thresholds — 3 Sliders → adaptive_engine Parameters

| Aspect | PM Estimate | Developer Estimate | Verdict |
|--------|------------|-------------------|---------|
| Effort | 6–8h | **5–7h** | Reasonably close, slight overestimate |
| Confidence | Medium | High | |

**Developer estimate: 5–7h** (recommend budgeting 6h midpoint)

**Rationale:**

1. **Session state spike (1h, mandated by Challenger).** `settings.py` already stores `settings_price_threshold`, `settings_volume_threshold`, `settings_revenue_threshold` in `st.session_state`. The spike must verify these are accessible from `adaptive_engine.py` detection functions. **Key concern:** `detect_price_abnormal()` (adaptive_engine.py:411–447) takes a `threshold: float = 7.0` parameter. This is a *function parameter*, not a module-level config. The calling code must pass the session_state value. Need to trace:
   - Where is `detect_price_abnormal()` called? (Called from `run_auto_detection()` at line 595 with default threshold=7.0)
   - `run_auto_detection()` needs to read `st.session_state["settings_price_threshold"]` — but `adaptive_engine.py` is supposed to be Streamlit-free!
   - **This is the architectural tension.** The service layer should not depend on Streamlit. Solution: pass threshold as parameter from the caller (page layer). Requires tracing the UI → service call chain. Spike needed to map this.

2. **Wiring work** (after spike confirms architecture):
   - Modify `run_auto_detection()` signature to accept `price_threshold`, `revenue_threshold` parameters — **0.5h**
   - Locate and modify the UI call site(s) to pass session_state values — **1h**
   - The volume slider is per-Challenger de-scoped (removed from C07). Only price and revenue sliders need wiring now. **Volume slider remains in UI but is decorative.** **–1h savings**
   - Add `detect_revenue_event()` threshold parameter (currently hardcoded `abs(yoy_pct) < 30` at line 301) — **1h**
   - Wire `settings_revenue_threshold` to `detect_revenue_event()` — the function currently doesn't take a threshold parameter. Must add it. **+1h** (this is new code, not just wiring)

3. **Volume slider deprecation handling.** Per plan: "Volume detection REMOVED." But the slider still exists in settings.py. Need to decide:
   - Leave slider in place with a "coming soon" caption (minimal, **0.25h**)
   - Remove slider entirely (also removes session_state key, needs migration guard) — **0.5h**
   - I recommend leaving the slider with a disabled state + caption explaining it's for future use. This avoids breaking existing session_state keys.

4. **Testing:** Write 2–3 tests verifying threshold passthrough — **1h**

**Total: 5–7h** (spike 1h + signature changes 1.5h + UI wiring 1h + revenue threshold param 1h + volume slider handling 0.5h + testing 1h + buffer 1h)

**⚠️ KEY RISK:** The Streamlit ↔ service layer boundary. If the architecture review confirms `adaptive_engine.py` must remain Streamlit-free (which it should — 100% Streamlit-free service layer is a key architecture rule), then threshold values must be passed through from the page layer. The current `run_auto_detection()` is called from `_main.py` (business card). Need to verify this call chain and inject session_state values at the page level.

---

## 2. New Feature Cost Estimates (C139–C146)

### C139: "Explain This Number" — One-Click Metric Explanation

| Field | Value |
|-------|-------|
| PM Estimate | 8–12h |
| Developer Estimate | **10–14h** |
| Priority | P1 |
| Dependencies | D5 (✅ done), TemplateExplanationProvider (✅ done) |

**Underlying analysis:**
- **Infrastructure reuse: HIGH.** `ExplanationProvider` protocol + `TemplateExplanationProvider` + factory exist (D5, 5e7fde8). The protocol supports `explain(request)` with `metric_name`, `metric_value`, `delta`.
- **UI work: MODERATE.** Each metric display needs a clickable "explain" trigger. Current metric values are rendered as text in `_financial.py`, `_health.py`, and various sections. The simplest implementation: add a small "💡" button next to each metric that triggers `get_explanation_provider().explain()` and shows result in an expander or popover.
- **Metric metadata mapping: MODERATE.** `TemplateExplanationProvider` has 10 template keys: revenue, eps, pe_ratio, roe, debt_ratio, dividend_yield, gross_margin, operating_margin, net_margin, plus fallback. The business card displays ~15+ metrics. Need to build a metric_name → template_key mapping for the ones that don't match directly.
- **New files needed:**
  - `src/services/llm/metric_explainer.py` — thin service wrapping provider with metric→key mapping. **2–3h**
  - UI helper function for "explain this number" button + popover. **2–3h**
  - Wiring into existing metric displays (6–8 locations across _financial.py, _health.py, _helpers.py). **3–4h**
- **Testing:** Unit tests for metric_explainer + render tests for 3 key metric pages. **2–3h**
- **Content creation:** Expanding templates to cover 15+ displayed metrics with zh-TW text. **2–3h**
- **Risk:** UI clutter — 15+ "explain" buttons look noisy. Needs a design pass (progressive disclosure: show on hover or in an expander). **+2h for design refinement**

**Recommendation: Budget 12h. The D5 reuse saves ~3h vs. building from scratch.**

---

### C140: Historical Case Study Library

| Field | Value |
|-------|-------|
| PM Estimate | 14–20h |
| Developer Estimate | **16–22h** |
| Priority | P1 |
| Dependencies | None (standalone) |

**Underlying analysis:**
- **Infrastructure reuse: LOW.** C28 Story Timeline just shipped with `timeline_service.py` + `company_milestones.yaml` + case studies. The case study *YAML data* can be reused (e.g., `case_studies.yaml`), but the "library" implies a browseable/searchable collection view — a new page + service.
- **New files needed:**
  - `src/services/case_study_library.py` — library service: load, search, filter, category-tag. **3–4h**
  - `src/pages/case_study_library.py` — browse page with filters (industry, topic, era). **4–6h**
  - `src/data/yaml/case_study_library.yaml` — structured library with 10–15 case studies tagged by topic. Content-heavy. **4–6h content + 1h schema**
  - `src/data/yaml/case_study_categories.yaml` — category taxonomy (1h)
- **Navigation integration:** Add nav button from related pages. **1h**
- **Testing:** Unit tests for search/filter logic + render test for library page. **2–3h**
- **Content creation (40% rule):** Case studies require historian tone QA gate. Minimum 10 curated cases at 1–1.5h each = **10–15h of content**

**Recommendation: Budget 18h minimum. The content creation is the bottleneck. If content is pre-written, 10–12h for dev only.**

---

### C141: Confidence/Source Badge on Explanations

| Field | Value |
|-------|-------|
| PM Estimate | 4–6h |
| Developer Estimate | **3–4h** |
| Priority | P2 |
| Dependencies | D5 (✅ done) |

**Underlying analysis:**
- **Infrastructure reuse: HIGH.** `ExplanationResponse` already has `source` ("template" | "llm" | "fallback") and `confidence: float` fields (base.py:27–31). The data model exists.
- **UI work: LOW.** A small badge (e.g., "📝 Template" / "🤖 AI" / confidence stars) next to each explanation. The explanation text currently renders in `_info_card()` calls and delta cards. Just need to append a badge span.
- **Implementation:** 
  - Add `_render_explanation_with_badge(text, source, confidence)` helper in `_router_base.py` — **1h**
  - Wire into delta card render, metric explanation, health summary — **1–1.5h**
  - CSS for badge styling (adapt to theme) — **0.5h**
  - Test: 3 test cases, one per source type — **0.5h**

**Recommendation: Budget 4h. Simplest feature. Actually lower than PM estimate.**

---

### C142: Glossary Gate on First Encounter

| Field | Value |
|-------|-------|
| PM Estimate | 6–10h |
| Developer Estimate | **8–12h** |
| Priority | P2 |
| Dependencies | C33 Glossary (✅ done, has glossary data + tooltip system) |

**Underlying analysis:**
- **Infrastructure reuse: MODERATE.** The glossary system (C33) exists with YAML-defined terms and tooltip rendering. But "first encounter gate" implies a session-level flag tracking which terms the user has seen.
- **New logic needed:**
  - Session state tracking: `st.session_state["glossary_seen_terms"]` set — **0.5h**
  - Gate detection: when rendering a metric section, check if any glossary terms appear and haven't been seen — **2–3h**
  - Gate UI: modal/expander that shows the glossary definition before the metric detail — **2–3h**
  - Dismissal persistence: mark term as seen after user interacts — **0.5h**
  - Counter resets: clear `glossary_seen_terms` on new stock view — **0.5h**
- **Integration points:** Every metric render in _financial.py and _health.py that uses glossary term tooltips needs the gate check. **5–6 touchpoints.** This is the main cost — adding a conditional wrapper at each site. **3–4h**
- **Edge cases:** Terms appearing multiple times on same page, terms in expanders below the fold, rapid stock switching — **1–2h**

**Recommendation: Budget 10h. The gate pattern is proven (similar to tutorial overlays), but scattering it across 5–6 render sites is tedious.**

---

### C143: Implication Sentence on Delta Cards

| Field | Value |
|-------|-------|
| PM Estimate | 3–5h |
| Developer Estimate | **4–6h** |
| Priority | P2 |
| Dependencies | delta_engine.py (✅ done), C134 (change explanations) |

**Underlying analysis:**
- **Infrastructure reuse: HIGH.** `compute_recent_deltas()` (delta_engine.py:7–87) already computes change data. The "implication sentence" is one tier above the "explanation" — it interprets what the change *means* for the investor.
- **Implementation:**
  - Add `implication` field to delta dict — **0.25h**
  - Write implication generation: "If revenue +30% and stock +20%, then '基本面題材持續'" — **2–3h**
  - Render in delta card (already renders explanations in `_render_deltas()`) — **0.5h**
  - Different implications for different metric combinations (= business logic, not template) — **1–1.5h**
- **Risk: This borders on investment advice.** The historian tone QA gate is critical. "公司營收大好，建議買入" would violate the product vision. Must frame as observation: "基本面動能偏強，可持續觀察" — **QA gate adds 1h.**

**Recommendation: Budget 5h. Small but requires careful tone QA.**

---

### C144: Beginner Curated Watchlists

| Field | Value |
|-------|-------|
| PM Estimate | 6–10h |
| Developer Estimate | **8–12h** |
| Priority | P2 |
| Dependencies | watchlist infrastructure (✅ exists) |

**Underlying analysis:**
- **Watchlist exists** but "curated watchlists" implies pre-built lists for beginners (e.g., "台股入門 10 檔", "高股息 rookies").
- **New files:**
  - `src/data/yaml/curated_watchlists.yaml` — 3–5 curated lists with stock IDs + rationale. Content-heavy. **3–4h content + 0.5h schema**
  - `src/services/curated_watchlists.py` — load + serve curated lists. **1–2h**
  - `src/pages/curated_watchlists.py` — browse page showing lists + stock details. **3–4h**
  - Nav integration from main page — **0.5h**
- **Content:** 3–5 lists × 5–10 stocks + rationale text in zh-TW. Historian tone required. **4–6h content creation**
- **Testing:** Unit tests + render test — **1h**

**Recommendation: Budget 10h. If content is pre-written, 6h dev only.**

---

### C145: Sector Rotation Narrative

| Field | Value |
|-------|-------|
| PM Estimate | 10–14h |
| Developer Estimate | **14–20h** |
| Priority | P2 |
| Dependencies | market data (exists), industry benchmarks (⚠️ minimal) |

**Underlying analysis:**
- **This is a MARKET-LEVEL feature, not single-stock.** It requires cross-stock data aggregation that the current architecture doesn't support well.
- **Data gap:** Stock Explorer fetches data per-stock via FinMind API. Sector rotation analysis requires:
  - Multi-stock performance comparison (5–10 sector leaders)
  - Relative momentum indicators
  - Capital flow inference from volume/price data
- **New files:**
  - `src/services/sector_rotation.py` — aggregation of multi-stock data into sector momentum scores — **5–7h**
  - `src/pages/sector_rotation.py` — page showing rotation narrative + chart — **3–5h**
  - `src/data/yaml/sector_rotation_config.yaml` — sector definitions + benchmark weights — **1h**
  - Narrative generation template (3–4 rotation states: risk-on, risk-off, mixed, transition) — **3–4h**
- **Mock data needed:** Since real sector data requires batch API calls that may hit rate limits — **2–3h**
- **Testing:** Integration tests with mock data — **2h**

**Recommendation: Budget 18h. This is architecturally the most ambitious — it's the first market-wide view in a single-stock app. Consider deferring to Sprint 19+ and doing a data feasibility spike first (3–4h).**

---

### C146: Emoji-Based Sentiment Indicators

| Field | Value |
|-------|-------|
| PM Estimate | 4–6h |
| Developer Estimate | **3–5h** |
| Priority | P2 |
| Dependencies | risk_analyzer.py (✅ exists), news event detection (✅ exists) |

**Underlying analysis:**
- **Ultra-lightweight.** Replace text-heavy severity labels with emoji + color badges:
  - 🔴 high risk / negative sentiment
  - 🟡 medium risk / neutral
  - 🟢 low risk / positive
- **Implementation:**
  - Create `_sentiment_badge(severity)` helper — **0.5h**
  - Replace text severity labels in event renders, risk sections — **2–3h**
  - CSS for badge rendering — **0.5h**
  - Testing — **0.5h**

**Recommendation: Budget 4h. Trivial if batched with other UI polish. Risk: meaninglessly decorative if sentiment logic isn't data-driven — must tie emoji to actual severity scores, not random assignment.**

---

### Summary Table — New Features

| ID | Feature | PM Est. | Dev Est. | Confidence | Key Risk |
|----|---------|---------|----------|------------|----------|
| C139 | Explain This Number | 8–12h | **10–14h** | Medium-High | UI clutter, content expansion to 15+ metrics |
| C140 | Case Study Library | 14–20h | **16–22h** | Medium | Content creation is bottleneck (40% rule) |
| C141 | Confidence/Source Badge | 4–6h | **3–4h** | High | Almost trivial — data model exists |
| C142 | Glossary Gate | 6–10h | **8–12h** | Medium | Scattered integration across 5–6 render sites |
| C143 | Implication Sentence | 3–5h | **4–6h** | Medium | Historian tone QA gate is critical |
| C144 | Curated Watchlists | 6–10h | **8–12h** | Medium | Content creation for descriptions |
| C145 | Sector Rotation | 10–14h | **14–20h** | Medium | First market-wide view; data feasibility unknown |
| C146 | Emoji Sentiment | 4–6h | **3–5h** | High | Trivial; risk of meaningless decoration |
| **Total** | | **55–94h** | **66–97h** | | |

---

## 3. Technical Risk Assessment — Sprint 17 Items

### C14 Full Radar — Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **Plotly radar overlay visual confusion** — two overlapping translucent fills are hard to read in dark theme | Medium | High | Use solid contrasting colors + different marker shapes. Reserve fill for user stock only; use dashed border for benchmark. Design review before implementation. |
| **Benchmark data loading circular dependency** — loading benchmark stock's financial data may trigger same FinMind API calls, rate-limiting | Medium | Medium | Cache benchmark scores in YAML (precomputed). Avoid live API calls for benchmarks. Load once at startup. |
| **"Industry #1" not always meaningful** — "其他" industry maps to 台積電 which isn't representative | Low | High | Add a "benchmark available" flag in `industry_benchmarks.yaml`. Skip overlay for industries where the benchmark is clearly not representative. |
| **Spec becomes stale** — written spec may not cover edge cases discovered during implementation | Low | Medium | Spec is a living document; update during implementation. 1h buffer included. |
| **Story card reordering breaks mobile layout** — current sections use `st.columns(5)` which doesn't stack well on mobile | Medium | Medium | Test at 375px width. Consider making health section full-width instead of 5-col layout. |

### C134 Change Explanations — Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **D-101: explain_delta() untested** — refactoring changes behavior silently | **High** | High | Mandatory C39 regression tests (Challenger requirement). Lock current outputs as golden master. |
| **zh-TW vs zh-CN template inconsistency** (D-5 uses zh-CN, product is zh-TW) | Medium | High | Budget 2–3h for zh-TW template variants. This is a real localization gap. |
| **Template key mapping explosion** — 15+ display metrics but only 10 template keys | Medium | Medium | Fallback templates handle unknown metrics gracefully. Expand templates incrementally after launch. |
| **Factory function returns wrong provider for delta context** | Medium | Low | Integration test explicitly verifies `compute_recent_deltas()` output after refactoring. |
| **Performance: TemplateExplanationProvider is fast but factory indirection adds latency** | Low | Low | Negligible. Factory returns cached singleton. |

### C07 Wire Thresholds — Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **Streamlit dependency in service layer** — `adaptive_engine.py` is 100% Streamlit-free (architecture rule). Wiring session_state into it violates this. | **High** | Medium | 1h spike MUST confirm call chain. Solution: inject thresholds as parameters at the page layer (UI reads session_state, passes to service). Service code stays framework-agnostic. |
| **detect_revenue_event() has hardcoded threshold** — line 301: `abs(yoy_pct) < 30`. Not configurable. | Medium | High (certain) | Must add `threshold` parameter to `detect_revenue_event()`. This is new code, not wiring. Budgeted 1h above. |
| **Integer slider step=0.5 vs integer revenue step=1.0** — inconsistent UX between price (0.5 steps, 0–20) and revenue (1.0 steps, 0–50) | Low | High | Acceptable UX. Different thresholds have different sensitivities. No change needed. |
| **Stale session_state after defaults change** — if `_DEFAULT_PRICE_THRESHOLD` is updated, existing users keep old values | Low | Medium | Use `_init_defaults()` which only sets if key not present. Document migration path. |
| **Threshold = 0 edge case** — price_threshold=0 means "every tick is an event" → floods events.yaml | Medium | Low | Validation exists in settings.py (line 89–94). Add warning in adaptive_engine when threshold < 1.0. |

---

## 4. Debt Resolution Cost Estimates

### D-099: settings.py Non-Standard Function Signature

| Field | Value |
|-------|-------|
| Description | `render_settings_page()` is the standard pattern, but helpers like `_init_defaults()`, `_reset_defaults()`, `_value_label_pricerange()`, `_value_label_volume()` use non-standard naming/capitalization patterns |
| Severity | Low |
| Effort | **0.5h** |

**Resolution:** Pure naming/style fix. Rename `_value_label_pricerange` → `_value_label_price_range` (standard PEP 8). No logic change. No tests needed — these are internal helpers not imported elsewhere.

---

### D-100: TemplateExplanationProvider Untested

| Field | Value |
|-------|-------|
| Explanation | `TemplateExplanationProvider` (template_provider.py:94–131) was delivered in Sprint 16b (commit 5e7fde8) with zero tests. It is the D5 deliverable and will be exercised by C134. |
| Severity | Low |
| Effort | **1–1.5h** |

**Resolution:** 
- Write 10+ parameterized tests: one per template metric (revenue, eps, pe_ratio, roe, debt_ratio, dividend_yield, gross_margin, operating_margin, net_margin) + fallback + unknown metric
- Test `_resolve_direction()` with "+5.2%", "-3.1%", "持平", None, edge strings
- Test `is_available()` always returns True
- Test `ExplanationResponse` has `source="template"` and `confidence=1.0`
- **Note: These tests can be written as part of C134's test pass** (C134 needs similar tests anyway). If C134 is done in Sprint 17, D-100 is resolved as part of that work. Incremental cost: **0h** if done with C134; standalone: **1–1.5h**.

---

### D-101: explain_delta() Untested — C134 Refactoring Risk

| Field | Value |
|-------|-------|
| Description | `explain_delta()` (delta_engine.py:90–164) has zero tests. C134 requires refactoring this function to delegate to TemplateExplanationProvider. Without regression tests, refactoring is high-risk. |
| Severity | **Medium** |
| Effort | **2–2.5h** |

**Resolution:**
- Write regression tests BEFORE refactoring (Challenger requirement #4):
  - Parameterize across 3 metrics × 3 thresholds × 2 directions = 18 test cases minimum
  - Capture current output strings as golden master assertions
  - Test boundary values: change_pct at exactly 10% (edge of detection), 29.9%, 30.0%, 30.1%, 49.9%, 50.0%, 50.1%
  - Test all-three-metric present, single-metric present, no-delta case
  - Note: `compute_recent_deltas()` filters to `abs(change_pct) > 10`, so test cases near 10% are important
- **This is NOT optional.** The Challenger explicitly mandated this. Skipping it means accepting silent behavior change risk.
- **Overlap: These tests complement D-100.** D-100 tests the provider; D-101 tests the integration. Combined: **3–4h** for full C134 test coverage.

---

### D-102: get_timeline() Untested

| Field | Value |
|-------|-------|
| Description | `get_timeline()` in `timeline_service.py` (Sprint 16b, commit ca49d2c) has zero tests. It's the core compose-and-enrich pipeline for C28 Story Timeline. |
| Severity | Low |
| Effort | **1.5–2h** |

**Resolution:**
- Write tests for the compose-and-enrich pipeline:
  - Test with all 3 sources present (events + case_studies + milestones)
  - Test with missing sources (empty YAML files → graceful degradation)
  - Test deduplication logic: same-day same-type events get count badges
  - Test severity coding: correct CSS class assignment
  - Test date sorting: chronological order
  - Test empty state: returns empty list, not error
- Mock YAML data fixtures: create test event/case_study/milestone YAML files under `tests/fixtures/`
- Time estimate: 2 test functions × 45min each + fixture setup 30min + edge cases 30min = **1.5–2h**

---

### Debt Resolution Summary

| ID | Description | Severity | Standalone Effort | Bundled Effort | Notes |
|----|-------------|----------|-------------------|----------------|-------|
| D-099 | settings.py naming | Low | 0.5h | 0.5h | Pure rename, no logic change |
| D-100 | TemplateExplanationProvider untested | Low | 1–1.5h | **0h** | Resolved as part of C134 testing |
| D-101 | explain_delta() untested (C134 risk) | Medium | 2–2.5h | **2–2.5h** | Mandatory for C134 |
| D-102 | get_timeline() untested | Low | 1.5–2h | 1.5–2h | Independent of Sprint 17 work |
| **Total** | | | **5.5–6.5h** | **4–5h** | |

**Recommendation:** Bundle D-101 into C134 test pass (0h incremental). D-102 can wait until Sprint 18 (C28 is already deployed; adding tests to working code is low risk). D-099 is a 15-min naming fix — do it when touching settings.py for C07. D-100 is absorbed by C134.

---

## Summary

### Sprint 17 True Cost

| Item | PM Estimate | Developer Estimate | Delta | Driver |
|------|------------|-------------------|-------|--------|
| C14 Full Radar | 4–8h | 6–10h | +2h | Benchmark data plumbing + Plotly overlay complexity |
| C134 Change Explanations | 12–14h | 10–13h | –1h | Well-scoped refactoring; zh-TW templates offset savings |
| C07 Wire Thresholds | 6–8h | 5–7h | –1h | Volume de-scope saves effort; but needs revenue threshold param |
| **Sprint 17 Total** | **22–30h** | **21–30h** | **~0h** | |

**Bottom line: PM estimates are accurate in aggregate.** The apparent delta is actually a redistribution — C14 runs higher than expected, but C134 and C07 run slightly lower. The total holds at **21–30h**.

### Key Adjustments Recommended

1. **C14 spec: Budget 1.5h for spec writing.** The Challenger is right — without a spec, the benchmark overlay becomes a visual guessing game.
2. **C134: Choose template localization strategy upfront.** zh-TW templates (Option A, +2–3h) vs. wrapper pattern (Option B, +0.5h). Recommend Option A for consistency.
3. **C07: Confirm Streamlit boundary in the 1h spike.** If `adaptive_engine.py` must stay Streamlit-free, wiring requires parameter injection at the page layer. This is fine but must be verified.
4. **D-101 is the highest-risk debt going into Sprint 17.** It's the precondition for C134 and the Challenger's explicit requirement. Do not skip.

### New Feature Pipeline Recommendation

Given Sprint 17 at 21–30h, the realistic next-sprint capacity is **20–25h** (assuming similar team availability). This means only **1 P1 + 1–2 P2** features fit in Sprint 18.

| Sprint | Recommended | Total Effort | Rationale |
|--------|-------------|--------------|-----------|
| Sprint 18 | C139 (Explain This Number) + C141 (Badges) + C143 (Implications) | 17–23h | C139 exercises D5; C141/C143 are small and align with C14 integrations |
| Sprint 19 | C140 (Case Study Library) — if content is ready | 16–22h | Content-dependent; start pre-writing now |
| Sprint 20 | C142 (Glossary Gate) + C146 (Emoji) | 11–17h | Lighter sprint |
| Sprint 21+ | C145 (Sector Rotation) | 14–20h | Needs data feasibility spike first |
| When convenient | C144 (Curated Watchlists) | 8–12h | Good fit for content + dev sprint |

### Architectural Health Check

- L0: 110 | L1: 20 | **Target after Sprint 17: L0: 115, L1: 23** (+5 L0 tests from C134 + C07 + C14, +3 L1 from C134 pipeline)
- God modules: **0** (maintain)
- Streamlit-free services: **100%** (maintain — C07 spike must confirm)
- Debt items resolved this round: **D-100 + D-101 bundled into C134** = 2 of 4 new items cleared at zero incremental cost

---

*End of Review Round 37 — Developer Cost Estimates*
