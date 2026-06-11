# 2026-06-18 Developer Estimate — Round 12 Discussion

## Feature Cost Estimates

| Feature | Low Estimate | High Estimate | Risk Level | Dependencies |
|---------|-------------|---------------|------------|--------------|
| **C55** Investment Diary | 10h | 16h | 🟢 Low | business_card.py hook + standalone page |
| **C56** Explain This Metric | 12h | 18h | 🟡 Medium | business_card.py metric iteration + YAML content |
| **C57** Compare Concepts | 10h | 16h | 🟡 Medium | Standalone page, no existing service deps |
| **C58** Beginner Onboarding Flow | 14h | 22h | 🔴 High | Streamlit tour/tutorial pattern research |
| **C59** AI Q&A Chatbot | 18h | 28h | 🔴 High | Pattern matching engine + analogy_engine integration |
| **C60** Concept Mastery Badges | 8h | 14h | 🟢 Low | Session state tracking + standalone page |
| **C61** Sector Rotation Visualizer | 10h | 16h | 🟡 Medium | C51 (Sector Heatmap) must exist first |
| **C62** Pre-Investment Checklist | 8h | 14h | 🟢 Low | business_card.py bottom section + anchor links |

**Total: 90–140h** (108–168h with 20% buffer)

---

## Detailed Breakdown

### C55: Investment Diary (10–16h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| Data model & storage | 2h | 3h | Session state + local JSON file per stock; no persistence layer needed |
| "📝 投資筆記" section on business card | 2h | 3h | Text input + save button; hook into existing page |
| "My Diary" standalone page | 3h | 5h | Chronological list, filter by stock, link back to company pages |
| Event connection ("You wrote this before...") | 2h | 3h | Match note timestamps to event dashboard events |
| Polish & edge cases | 1h | 2h | Empty state, long notes, mobile layout |

**Risks**: Low. Straightforward CRUD with session state. The event-connection feature is nice-to-have; can be deferred if time-constrained.

**Parallelizable**: Can start immediately. No dependency on Sprint 3/4 features. Only touches business_card.py at the margins.

---

### C56: Explain This Metric (12–18h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| `metric_explanations.yaml` content creation | 3h | 5h | 10 metrics × (definition + analogy + example + "why it matters" + "what to watch") |
| "❓" button integration into business_card.py | 2h | 3h | Add button next to each metric; requires modifying metric rendering loop |
| Expander/dialog UI with Plotly mini-charts | 3h | 4h | st.expander with embedded chart; reuse chart.py patterns |
| Historical trend mini-charts | 2h | 3h | Fetch metric history from FinMind; Plotly sparkline |
| Testing across 10 metrics | 1h | 2h | Content QA + layout QA |
| Polish & edge cases | 1h | 1h | Missing metric fallback, long text truncation |

**Risks**: Medium. The YAML content creation is a hidden time sink — writing 10 high-quality metric explanations with TW stock examples requires research. The business_card.py integration is moderate risk since that file is already 447 lines and growing (D24 addresses this).

**Parallelizable**: YAML content can be written in parallel with other features. UI integration must wait until business_card.py is stable (post-D24).

---

### C57: Compare Concepts (10–16h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| "📊 概念比較" standalone page | 2h | 3h | New page in router.py; two dropdown selectors |
| Content data model (concept pairs) | 3h | 5h | 10 concept pairs × (definitions, formulas, pros/cons, when-to-use, TW example) |
| Side-by-side comparison UI | 2h | 3h | Two-column layout with definition, formula, pros/cons |
| "Which is better for this company?" analysis | 2h | 3h | Template-based analysis using current stock's metrics |
| Polish & edge cases | 1h | 2h | Same concept selected, missing data fallback |

**Risks**: Medium. Content creation is the biggest risk — 10 concept pairs with meaningful comparisons requires domain expertise. The "which is better" analysis needs careful templation to avoid sounding prescriptive (historian positioning guardrail).

**Parallelizable**: Fully standalone page. No dependencies on other features. Can start immediately.

---

### C58: Beginner Onboarding Flow (14–22h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| Research Streamlit onboarding patterns | 2h | 4h | Streamlit has no built-in tour widget; need custom CSS/JS or st.modal approach |
| 5-step tour content & flow design | 2h | 3h | Welcome → Search → Business Card → Event Dashboard → Watchlist |
| Session state flag & first-time detection | 1h | 2h | `onboarding_complete` flag; detect first visit |
| UI implementation (modal/overlay approach) | 4h | 6h | Custom CSS overlays or sequential st.modals; highlight UI elements |
| "Beginner Guide" PDF generation | 2h | 3h | Static PDF or markdown-to-pdf; 3 beginner-friendly company suggestions |
| "Help" button to replay tour | 1h | 2h | Navbar button; reset session state flag |
| Cross-browser/device testing | 2h | 2h | Streamlit rendering varies; CSS overlays are fragile |

**Risks**: High. Streamlit has no native onboarding/tour component. The implementation will require custom CSS overlays or a modal-based approach, both of which are fragile across Streamlit versions. The "highlight UI element" feature is particularly tricky — Streamlit doesn't expose element IDs reliably. May need to simplify to a modal-only tour without element highlighting.

**Key Decision**: Recommend modal-based tour (simpler, more reliable) over CSS overlay approach (fragile, high maintenance). This reduces estimate to 14–18h.

**Parallelizable**: Standalone feature. Can start immediately, but content design should coordinate with Designer.

---

### C59: AI Q&A Chatbot (18–28h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| "💬 問問股識" standalone page | 2h | 3h | Chat UI with st.chat_input + st.chat_message (Streamlit native) |
| Question pattern matching engine | 4h | 6h | Regex/intent classification for 15-20 question types |
| Response templates per intent | 4h | 6h | Map intents to data fetches + analogy_engine responses |
| FinMind data integration | 2h | 3h | Fetch relevant data based on question type |
| Follow-up question suggestions | 2h | 3h | 3 suggested follow-ups per answer; template-based |
| Historian guardrail enforcement | 2h | 3h | Reject/reframe predictive questions ("Will TSMC go up?") |
| Edge case handling | 2h | 4h | Unknown questions, data unavailable, rate limits |

**Risks**: High. This is the most complex feature. The pattern matching engine needs to handle varied natural language inputs in Chinese. The historian guardrail is critical — the chatbot must refuse to predict and instead redirect to historical data. Edge cases (unknown questions, ambiguous intent) will consume more time than expected.

**Key Decision**: Use pattern matching (regex + keyword), NOT LLM. LLM would add 10-15h for API integration, prompt engineering, and hallucination guardrails. Pattern matching is faster, more predictable, and aligns with the "explain from structured data" philosophy.

**Parallelizable**: Standalone page. Can start immediately, but should coordinate with analogy_engine team for response integration.

---

### C60: Concept Mastery Badges (8–14h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| `badges.yaml` definition file | 2h | 3h | Badge criteria: companies viewed, quizzes completed, features used, etc. |
| User action tracking in session state | 2h | 3h | Hook into existing page views, quiz completions, feature interactions |
| Badge award logic | 1h | 2h | Check criteria on each action; trigger badge notification |
| "🏆 學習成就" page | 2h | 4h | Badge grid with earned/unearned states; link to related companies |
| Badge notification UI | 1h | 2h | Toast/animation when badge earned; st.balloons or custom |

**Risks**: Low. Straightforward implementation using existing session state patterns. The main risk is deciding which actions to track — need to coordinate with PM on badge criteria.

**Parallelizable**: Fully standalone. Can start immediately. Integrates with C52 (Quiz Mode) when built, but doesn't depend on it.

---

### C61: Sector Rotation Visualizer (10–16h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| Extend C51 with time-series view | 3h | 4h | Add 1W/1M/3M time selector to existing Sector Heatmap |
| Sector momentum calculation | 2h | 3h | Compute momentum change over time windows |
| "Rotation" detection & highlighting | 2h | 3h | Identify sectors changing direction; visual highlight |
| Plain-language explanations | 2h | 4h | Template-based: "Semiconductor sector has been bearish for 3 months but started turning bullish last week — driven by AI chip demand recovery" |
| Company connection ("If you're interested in...") | 1h | 2h | Link to top 3 companies in rotating sector |

**Risks**: Medium. Depends on C51 (Sector Heatmap) existing first — C51 is in Sprint 4, so C61 cannot start until Sprint 4 completes. The plain-language explanation templates need careful wording to avoid predictive language.

**Parallelizable**: Must wait for C51 completion. Can prepare templates and momentum calculation logic in advance.

---

### C62: Pre-Investment Checklist (8–14h)

| Sub-task | Low | High | Notes |
|----------|-----|------|-------|
| Checklist content definition | 2h | 3h | 5-7 items: understand business, check P/E, check debt, know risks, compare peers, understand sector, check recent events |
| "📋 投資前檢查清單" section on business card | 2h | 3h | Collapsible section at bottom of business_card.py |
| Checkbox UI with session state tracking | 1h | 2h | st.checkbox per item; track completion in session state |
| Anchor link scrolling | 2h | 4h | Click item → scroll to relevant section; Streamlit anchor links are limited |
| Progress indicator | 1h | 2h | "3/7 completed" progress bar |

**Risks**: Low. The main technical risk is anchor link scrolling — Streamlit has limited support for this. May need to use st.markdown with HTML anchors or accept that clicking items won't auto-scroll (reducing estimate by 2h).

**Parallelizable**: Can start immediately. Only touches business_card.py at the bottom (low conflict risk with other changes).

---

## Implementation Directions

### Direction A: "Quick Wins First" (Recommended)

**Philosophy**: Deliver visible user value fast, build momentum, defer complex features.

**Sprint 5 (immediately after Sprint 4):**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C62 Pre-Investment Checklist | 8–12h | Lowest effort, perfect "historian" differentiator, no dependencies |
| C60 Concept Mastery Badges | 8–12h | Low effort, drives engagement, standalone |
| C55 Investment Diary | 10–14h | Unique "historian of self" feature, standalone |

**Sprint 6:**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C56 Explain This Metric | 12–16h | P1 feature, but needs business_card.py stable (post-D24) |
| C57 Compare Concepts | 10–14h | Standalone, content can be prepared in parallel |
| C61 Sector Rotation Visualizer | 10–14h | Extends C51 (completed in Sprint 4) |

**Sprint 7:**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C58 Beginner Onboarding Flow | 14–18h | P1 feature, needs research time; simplified modal approach |
| C59 AI Q&A Chatbot | 18–24h | Most complex feature; benefits from all other features being stable |

**Timeline**: 3 sprints (Sprints 5–7)
**Total effort**: 90–124h (108–149h with buffer)
**Parallelization**: C62 + C60 can be parallelized (different developers). C55 is solo. C56 + C57 can be parallelized. C58 + C59 are solo (complex).

**Risks**: Low. Each sprint has a clear focus. P1 features (C56, C58) are spread across sprints to avoid overload.

---

### Direction B: "P1 Priority Push"

**Philosophy**: Front-load P1 features to address the most critical gaps first.

**Sprint 5:**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C56 Explain This Metric | 12–16h | P1, directly addresses "ten-second test" |
| C58 Beginner Onboarding Flow | 14–18h | P1, critical for beginner retention |
| C62 Pre-Investment Checklist | 8–12h | Quick win alongside P1 features |

**Sprint 6:**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C59 AI Q&A Chatbot | 18–24h | Most complex, but P2; benefits from C56's metric explanations |
| C55 Investment Diary | 10–14h | Unique differentiator |
| C60 Concept Mastery Badges | 8–12h | Quick win |

**Sprint 7:**
| Feature | Effort | Rationale |
|---------|--------|-----------|
| C57 Compare Concepts | 10–14h | Standalone educational tool |
| C61 Sector Rotation Visualizer | 10–14h | Extends C51 |

**Timeline**: 3 sprints (Sprints 5–7)
**Total effort**: 90–124h (108–149h with buffer)
**Parallelization**: C56 + C58 are risky to parallelize (both complex, both need design input). C62 can be done in parallel with either.

**Risks**: Medium. Sprint 5 is heavy (34–46h for one developer). C56 + C58 together may cause design resource contention. C59 in Sprint 6 is a large solo block.

---

### Direction C: "Parallel Track" (2-Developer Scenario)

**Philosophy**: If a second developer is available, split features across two tracks.

**Track 1 — Education Features (Developer A):**
| Sprint | Feature | Effort |
|--------|---------|--------|
| 5 | C56 Explain This Metric | 12–16h |
| 5 | C57 Compare Concepts | 10–14h |
| 6 | C59 AI Q&A Chatbot | 18–24h |

**Track 2 — Engagement Features (Developer B):**
| Sprint | Feature | Effort |
|--------|---------|--------|
| 5 | C62 Pre-Investment Checklist | 8–12h |
| 5 | C60 Concept Mastery Badges | 8–12h |
| 5 | C55 Investment Diary | 10–14h |
| 6 | C58 Beginner Onboarding Flow | 14–18h |
| 6 | C61 Sector Rotation Visualizer | 10–14h |

**Timeline**: 2 sprints (Sprints 5–6)
**Total effort**: 90–124h across two developers
**Parallelization**: Maximum parallelization. Track 1 focuses on education content, Track 2 on engagement features. Minimal merge conflict risk (different files).

**Risks**: Requires two developers. C56 touches business_card.py, which may conflict with Track 2's C62 (also touches business_card.py). Need to coordinate on business_card.py changes.

---

## Recommendation

**Recommend Direction A ("Quick Wins First")** for the following reasons:

1. **Low risk, high confidence**: C62, C60, and C55 are all low-risk, standalone features that can be delivered with high confidence. This builds team momentum before tackling complex P1 features.

2. **Dependencies respected**: C61 (Sector Rotation) correctly waits for C51 completion. C56 waits for business_card.py stabilization (D24 in Sprint 4).

3. **P1 features get proper focus**: C56 and C58 are each given dedicated sprint space, ensuring they receive adequate design and QA attention.

4. **C59 is appropriately sequenced last**: The AI Q&A Chatbot benefits from all other features being stable — it can reference metric explanations (C56), concept comparisons (C57), and badge progress (C60).

5. **Contingency-friendly**: If any sprint runs over, the next sprint's features can be deferred without breaking dependencies.

**If a second developer becomes available**, Direction C compresses the timeline to 2 sprints with minimal risk.

---

## Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **business_card.py bloat** — C56 and C62 both modify this file; with C48 (Sprint 4) also touching it, merge conflicts and complexity are likely | High | Medium | D24 (sub-directory extraction) in Sprint 4 must be completed before C56/C62. Coordinate closely with Architect. |
| **Streamlit onboarding limitations** — No native tour/onboarding widget; CSS overlays are fragile across versions | High | High | Use simplified modal-based tour (st.modal) instead of CSS overlays. Accept that UI element highlighting won't be pixel-perfect. |
| **C59 Chinese NLP complexity** — Pattern matching for Chinese natural language questions is harder than English | High | Medium | Start with 10-15 high-frequency question patterns. Use keyword matching + regex. Defer edge cases to "I don't understand, try rephrasing" response. |
| **YAML content creation time** — C56 (10 metrics) and C57 (10 concept pairs) require significant content writing | Medium | Medium | Start content creation in Sprint 4 (parallel workstream). Use LLM assistance for first drafts, then human review. |
| **C61 depends on C51** — If C51 is delayed, C61 cannot start | Medium | Low | C61 is P2 and can be deferred without impacting core value. Prepare templates in advance. |
| **Historian positioning drift** — C59 (AI chatbot) and C57 ("which is better") risk sounding prescriptive | Medium | High | Explicit review checklist: "Does this feature explain or predict?" All responses must use past tense and historical data. |
| **Session state scalability** — C55 (diary), C60 (badges), C62 (checklist) all add session state keys; may cause performance issues | Low | Low | Session state is per-user, per-session. Volume is low. Monitor and refactor to a session state manager if needed. |
| **C58 design resource contention** — Onboarding flow needs close Designer collaboration; Designer may be busy with Sprint 4 features | Medium | Medium | Start onboarding content design in Sprint 4. Use placeholder UI for first implementation, iterate with Designer in Sprint 5. |

---

## Summary for Team Discussion

**Total estimated effort**: 90–140h (108–168h with 20% buffer) across 8 features
**Recommended timeline**: 3 sprints (Sprints 5–7) with Direction A
**Critical path**: C51 (Sprint 4) → C61 (Sprint 6); D24 (Sprint 4) → C56 (Sprint 6)
**Highest risk items**: C58 (onboarding — Streamlit limitations), C59 (chatbot — Chinese NLP)
**Quick wins**: C62 (checklist), C60 (badges), C55 (diary) — all <14h, low risk, standalone
**P1 features**: C56 (Explain This Metric), C58 (Beginner Onboarding) — need dedicated sprint space and design support
