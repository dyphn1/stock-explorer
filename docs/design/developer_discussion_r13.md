## Friday, June 12, 2026 Developer Estimate — Round 13 Discussion

### Current Implementation State

**Codebase Health**: L0: 55/55 ✅ | L1: 18/18 ✅ — all verification gates green for the second consecutive cycle.

**Architecture**: 4-layer (Data → Service → Router → View) with 11 service modules, 1 data module, 12 page modules, and 1 router. Total ~6,500 LOC across `src/`.

**Sprint 3 Remaining** (3 items, ~24–29h):
| Item | Effort | Status | Notes |
|------|--------|--------|-------|
| C44 Risk Analysis MVP | 12–14h | ⏳ Next | 3 dimensions: customer concentration, financial health, event-based |
| C38 Compare Stories P1 | 10–12h | ⏳ After C44 | Structured side-by-side comparison, no LLM |
| D16 Split analogy_engine.py | 2–3h | ⏳ After C44 | Prerequisite for C48; analogy_engine.py is 850 lines |

**Key Service Inventory**:
| Service | LOC | Status | Notes |
|---------|-----|--------|-------|
| `analogy_engine.py` | 850 | ⚠️ Needs split (D16) | Largest service; D16 will extract key_takeaways, delta, health_scoring |
| `chart.py` | ~490 | ✅ Stable | 8 chart functions, consistent theme pattern |
| `adaptive_engine.py` | 590 | ✅ Stable | Event detection, freshness checking; reusable for C34/C55 |
| `financial_metrics.py` | ~120 | ✅ New (R1) | Shared module, 3 consumers; eliminates duplication |
| `revenue_analyzer.py` | ~200 | ✅ Stable | Revenue breakdown analysis |
| `health_scorer.py` | ~150 | ✅ Stable | Health dimension scoring |
| `dividend_analyzer.py` | ~100 | ✅ Stable | Dividend summary extraction |
| `company_facts.py` | ~80 | ✅ Stable | Company facts from YAML |
| `news_summarizer.py` | ~180 | ✅ Stable | News summarization |
| `watchlist.py` | ~150 | ✅ Stable | Watchlist management |

**Key Page Inventory**:
| Page | LOC | Status | Notes |
|------|-----|--------|-------|
| `business_card.py` | 509 | ⚠️ Growing | Needs D24 (sub-directory extraction) before C56/C62 additions |
| `router.py` | 175 | ✅ Stable | Page routing, navbar |
| `_router_base.py` | ~200 | ✅ Stable | Data loading + UI helper cards |

**Planned New Services** (from approved features):
| Service | For | Sprint | Status |
|---------|-----|--------|--------|
| `market_data.py` | C49 + C51 | 4 | Planned |
| `story_composer.py` | C48 | 4 | Planned |
| `export_service.py` | C48 + C53 | 4 | Planned |

**Approved Feature Pipeline** (post-Sprint 3):
| Sprint | Features | Total Effort |
|--------|----------|-------------|
| 4 | R3 + D24 + C51 + C48 + C53-1 | 24–33h |
| 5 | C58 + C62 + C56 + C60 | 42–68h |
| 6 | C57 + C55 + C61 | 30–46h |
| 7+ | C59 | 18–28h |

---

### Feature Direction A: Company Story Timeline (C34)

- **Description**: A visual, interactive timeline showing key historical events (product launches, leadership changes, regulatory shifts, market cycles) that shaped a company's present state. Each event includes a plain-language explanation of its impact, connecting past to present. This is the purest expression of the "historian" positioning — showing how history explains the present, not predicting the future. Proposed by the Architect as the primary Round 13 discussion topic.

- **New Components Needed**:
  - **New service**: `src/services/historical_timeline.py` (~200–250 LOC) — processes event data from `adaptive_engine.py` into chronological narrative structures. Pure functions: input DataFrame → output timeline event list.
  - **New data file**: `src/data/event_templates.yaml` (~100–150 lines) — event type definitions, impact explanation templates, significance scoring rules. Covers 4 event types: product launches, leadership changes, regulatory events, market cycles.
  - **New chart function** in `chart.py`: `create_timeline_chart(events: list) -> go.Figure` (~60–80 LOC) — Plotly-based interactive timeline with color-coded event types.
  - **View integration**: New collapsible section in `business_card.py` (or a new timeline sub-page if D24 extracts business_card.py into a sub-directory). Estimated ~80–100 LOC for the rendering logic.
  - **No changes to data layer** — reuses `finmind_client.py` via existing `adaptive_engine.py` event detection.

- **Dependencies**:
  - **Hard**: D16 (split analogy_engine.py) must complete first — `adaptive_engine.py` imports from analogy_engine, and the timeline service will depend on clean event detection interfaces.
  - **Hard**: D24 (business_card.py sub-directory extraction) — business_card.py is already 509 lines; adding a timeline section pushes it past 600. D24 must land before this feature.
  - **Soft**: C48 (Company Story Card) — the Architect notes potential overlap. C34 is deep historical narrative; C48 is curated present-day story. Need clear scoping to avoid duplication.
  - **Soft**: C38 (Compare Stories P1) — if C38 produces reusable narrative data structures, C34 could leverage them.

- **Effort Estimate**: **18–26h**
  | Sub-task | Low | High | Notes |
  |----------|-----|------|-------|
  | `event_templates.yaml` content creation | 3h | 5h | 4 event types × (definition + impact template + significance rules + TW examples) |
  | `historical_timeline.py` service | 4h | 6h | Event processing, chronological sorting, significance scoring |
  | `create_timeline_chart()` in chart.py | 2h | 3h | Plotly timeline with color-coded events |
  | View integration (business_card.py or sub-page) | 3h | 4h | Rendering logic, collapsible section |
  | Plain-language impact explanations | 2h | 3h | Template-based, reuses analogy_engine patterns |
  | Testing & edge cases | 2h | 3h | Empty timeline, many events, mobile layout |
  | Historian tone review | 2h | 2h | Ensure all explanations are past-tense, factual |

- **Risks**:
  | Risk | Probability | Impact | Mitigation |
  |------|------------|--------|------------|
  | **Content creation bottleneck** — 4 event types with meaningful templates + TW examples requires domain knowledge | High | Medium | Start content creation in Sprint 4 as parallel workstream. Use LLM for first drafts, human review. |
  | **Overlap with C48 (Company Story Card)** — both tell "the story" of a company | Medium | High | Define clear boundary: C34 = deep historical timeline (years/decades), C48 = curated present snapshot (current quarter/year). Coordinate with PM. |
  | **business_card.py bloat** — adding timeline section to already-growing page | High | Medium | D24 must complete first. If D24 extracts business_card.py into sub-directory, timeline becomes a separate sub-page component. |
  | **Event detection quality** — adaptive_engine.py's keyword-based detection may miss nuanced events or produce false positives | Medium | Medium | Accept imperfect detection for MVP. Focus on 4 high-confidence event types. Manual review of results for 5 test stocks. |
  | **Historian tone drift** — timeline explanations could slip into predictive language ("this event will lead to...") | Medium | High | Strict template review: all explanations must use past tense. Add automated tone check in CI. |

- **Reuses Existing Infrastructure**: `adaptive_engine.py` (event detection), `analogy_engine.py` (plain-language patterns), `chart.py` (chart theme system), `finmind_client.py` (data layer). No new API calls needed.

---

### Feature Direction B: Notification System for Learning Engagement

- **Description**: A lightweight, opt-in notification system that delivers timely educational nudges to encourage learning and re-engagement. Examples: "New analogy added for ROE — check it out!", "Your investment diary has an unwritten entry for TSMC", "Daily market fact: Semiconductor sector up 2% this week". Notifications appear as in-app toasts/banners. Proposed by the Architect as a secondary Round 13 topic.

- **New Components Needed**:
  - **New service**: `src/services/notification_service.py` (~120–150 LOC) — pure function that evaluates session state and returns notification data. No side effects. Takes `(session_state_dict, config) -> list[Notification]`.
  - **New data file**: `src/data/notification_templates.yaml` (~80–120 lines) — notification templates with conditions, messages, and frequency caps. Covers 6–8 notification types.
  - **View integration**: Toast/banner rendering in `_router_base.py` (~40–60 LOC) — `st.toast()` or custom CSS banners triggered by router on page load.
  - **Session state hooks**: Minor additions to existing pages (~20–30 LOC total) — track user actions (companies viewed, features used, diary entries) in session state.
  - **No changes to data layer** — all state is ephemeral (session_state).

- **Dependencies**:
  - **Hard**: None. Fully standalone feature.
  - **Soft**: C55 (Investment Diary) — notification system can nudge users to write diary entries, but C55 doesn't need to exist first.
  - **Soft**: C58 (Onboarding) — onboarding completion is a natural first notification, but not required.
  - **Soft**: C60 (Badges) — badge earning triggers a notification, but badges can be added later.

- **Effort Estimate**: **8–14h**
  | Sub-task | Low | High | Notes |
  |----------|-----|------|-------|
  | `notification_templates.yaml` | 2h | 3h | 6–8 notification types × (condition + message + frequency cap) |
  | `notification_service.py` | 2h | 3h | Pure function: evaluate conditions, return notification list |
  | Toast/banner rendering in `_router_base.py` | 1h | 2h | `st.toast()` integration, CSS styling |
  | Session state tracking hooks | 1h | 2h | Add tracking to existing page views |
  | User controls (opt-in/out, frequency) | 1h | 2h | Settings in session state, simple UI |
  | Testing & edge cases | 1h | 2h | No notifications, many notifications, rapid page switches |

- **Risks**:
  | Risk | Probability | Impact | Mitigation |
  |------|------------|--------|------------|
  | **Over-notification / annoyance** — users get spammed with toasts | High | High | Strict frequency caps (max 1 toast per page load). Opt-in by default, easy dismiss. |
  | **Session-state-only persistence** — notifications reset on page refresh | High | Low | Acceptable for MVP. D22 (persistence layer) is the long-term solution. |
  | **Low value without content** — notifications are only as good as the content they point to | Medium | Medium | Prioritize notification types that point to existing high-value content (C44 risk analysis, C43 health score). |
  | **Streamlit toast limitations** — `st.toast()` has limited styling options | Medium | Low | Accept default styling for MVP. Custom CSS banners as fallback. |

- **Reuses Existing Infrastructure**: `session_state` patterns (already used throughout), `_router_base.py` (UI helper pattern), `st.toast()` (Streamlit native). No new services or API calls needed.

---

### Feature Direction C: AI-Augmented Historical Narrator

- **Description**: An AI-powered feature that generates plain-language historical narratives from financial and event data, answering questions like "How did this company get to where it is today?" or "What past events explain this year's revenue change?" Uses template-based approach (not LLM) with strict historian tone enforcement. Proposed by the Architect as a tertiary Round 13 topic.

- **New Components Needed**:
  - **New service**: `src/services/historical_narrator.py` (~250–350 LOC) — template-based narrative generation. Takes financial metrics + company facts + event data → outputs structured narrative text. Pure function, no side effects.
  - **New data file**: `src/data/narrative_templates.yaml` (~150–200 lines) — narrative templates for 8–10 common historical patterns (revenue growth story, margin expansion story, turnaround story, cyclical recovery, etc.).
  - **View integration**: New section in `business_card.py` or standalone page (~60–80 LOC) — renders narrative text with supporting mini-charts.
  - **No changes to data layer** — reuses existing `financial_metrics.py`, `company_facts.py`, `adaptive_engine.py` outputs.

- **Dependencies**:
  - **Hard**: D16 (split analogy_engine.py) — narrator service will import from analogy_engine for plain-language patterns.
  - **Hard**: D24 (business_card.py sub-directory extraction) — if adding to business_card.py.
  - **Soft**: C44 (Risk Analysis MVP) — narrator could incorporate risk context, but not required.
  - **Soft**: C56 (Explain This Metric) — narrator could link to metric explanations, but not required.

- **Effort Estimate**: **14–22h**
  | Sub-task | Low | High | Notes |
  |----------|-----|------|-------|
  | `narrative_templates.yaml` content creation | 4h | 6h | 8–10 narrative patterns × (template + conditions + TW examples) |
  | `historical_narrator.py` service | 4h | 6h | Template selection logic, data binding, narrative assembly |
  | View integration | 2h | 3h | Rendering narrative text with mini-charts |
  | Historian tone enforcement | 2h | 3h | Template review, automated tense checking |
  | Testing & edge cases | 2h | 4h | Missing data, conflicting patterns, long narratives |

- **Risks**:
  | Risk | Probability | Impact | Mitigation |
  |------|------------|--------|------------|
  | **Template repetition** — users see the same narrative patterns repeatedly | High | Medium | Create 10+ distinct templates. Add variation through data-driven interpolation. |
  | **Content creation time** — 8–10 narrative templates with TW examples is significant | High | Medium | Start content creation in Sprint 4. Reuse analogy_engine patterns where possible. |
  | **Overlap with C56 + C59** — C56 explains metrics, C59 answers questions, C34 tells timeline — narrator could duplicate all three | High | High | Define clear boundary: narrator = auto-generated summary of "how we got here." C56 = interactive metric drill-down. C59 = user-driven Q&A. C34 = visual timeline. |
  | **Historian tone drift** — templates could slip into predictive language | Medium | High | Strict template review + automated tense check. All templates must use past tense only. |
  | **User expectations** — "AI" in the name sets high expectations for template-based output | Medium | Medium | Rename to "Company Story" or "Historical Summary" to manage expectations. |

- **Reuses Existing Infrastructure**: `financial_metrics.py` (shared calculations), `company_facts.py` (company data), `adaptive_engine.py` (event data), `analogy_engine.py` (plain-language patterns), `chart.py` (mini-charts).

---

### Feature Direction D: Quick Wins Bundle (C62 + C60 + C55)

- **Description**: A bundle of three low-risk, standalone features that can be delivered immediately after Sprint 4 without complex dependencies. These are the "Quick Wins First" from the Round 12 developer estimate, now confirmed by the Designer and Architect as high-value, low-risk additions. This is not a new direction but a reaffirmation of the approved Sprint 5 plan with refined estimates based on deeper codebase analysis.

- **Components Needed**:
  - **C62 (Pre-Investment Checklist)**: `checklist_items.yaml` (~50 lines) + ~80 LOC in `business_card.py` bottom section + ~30 LOC for session state tracking.
  - **C60 (Concept Mastery Badges)**: `badges.yaml` (~60 lines) + new standalone page `achievement_page.py` (~120 LOC) + ~40 LOC for session state tracking hooks.
  - **C55 (Investment Diary)**: `diary_storage.py` service (~100 LOC, session state + local JSON) + ~80 LOC in `business_card.py` bottom section + new standalone page `diary_page.py` (~100 LOC).

- **Dependencies**:
  - **Hard**: None for C62 and C60. C55 is also standalone.
  - **Soft**: D24 (business_card.py sub-directory extraction) — C62 and C55 both add to business_card.py. D24 should complete first to prevent >600-line file.
  - **Soft**: C52 (Quiz Mode) — C60 badges can track quiz completions, but C52 doesn't exist yet. Session-only tracking is sufficient for MVP.

- **Effort Estimate**: **26–40h** (refined from Round 12's 26–44h)
  | Feature | Low | High | Notes |
  |---------|-----|------|-------|
  | C62 Pre-Investment Checklist | 8h | 12h | Reduced estimate: anchor links simplified (no auto-scroll, just labels) |
  | C60 Concept Mastery Badges | 6h | 10h | Reduced estimate: session-only MVP, no persistence layer needed |
  | C55 Investment Diary | 10h | 14h | Confirmed: session state + local JSON, event connection is nice-to-have |
  | Cross-feature integration | 2h | 4h | Badge triggers from checklist completion, diary entry counts |

- **Risks**:
  | Risk | Probability | Impact | Mitigation |
  |------|------------|--------|------------|
  | **business_card.py bloat** — C62 + C55 both add to business_card.py | High | Medium | D24 must complete first. If D24 extracts sub-directory, both features become separate components. |
  | **Session state scalability** — 3 features all add session state keys | Low | Low | Session state is per-user, per-session. Volume is low. Monitor for performance. |
  | **User adoption of diary** — getting users to actually write entries is hard | Medium | Low | Provide sentence starters, prompts based on the company. Low friction UI. |
  | **Checklist credibility** — users check boxes without understanding | Low | Low | This is a learning tool, not certification. Items link to relevant sections. |

- **Reuses Existing Infrastructure**: `session_state` patterns, `_router_base.py` card components (new `_checklist_card()`, `_diary_card()`, `_badge_card()` per Designer's spec), `st.checkbox`, `st.text_area` (Streamlit native).

---

### Implementation Recommendations

#### 1. Prioritize Direction D (Quick Wins Bundle) for Sprint 5

**Rationale**: C62, C60, and C55 are all low-risk, standalone features that deliver visible user value immediately. They require no complex dependencies, have clear scope, and build momentum before tackling more complex features. This aligns with the Round 12 "Quick Wins First" recommendation, now confirmed by both Designer and Architect.

**Refined Sprint 5 Plan**:
| Priority | Feature | Effort | Dependencies |
|----------|---------|--------|-------------|
| 1 | C62 Pre-Investment Checklist | 8–12h | D24 (Sprint 4) |
| 2 | C60 Concept Mastery Badges | 6–10h | — |
| 3 | C55 Investment Diary | 10–14h | D24 (Sprint 4) |
| 4 | C58 Beginner Onboarding Flow | 14–18h | — |
| **Total** | | **38–54h** | |

#### 2. Defer Direction A (Company Story Timeline) to Sprint 6+

**Rationale**: C34 is the most architecturally complex Round 13 proposal. It requires D16 + D24, has content creation risk, and overlaps with C48. The historian value is real but the implementation risk is high. Recommend deferring to Sprint 6 when:
- D24 has extracted business_card.py into sub-directory (clean integration point)
- C48 has shipped (clear boundary between present-story and historical-timeline)
- Content creation for event templates can start in Sprint 4 as parallel workstream

#### 3. Defer Direction C (AI-Augmented Historical Narrator) to Sprint 7+

**Rationale**: The Architect's own recommendation is to start with template-based MVP, which overlaps significantly with C56 (Explain This Metric) and C59 (AI Q&A Chatbot). Building this after C56 and C57 are stable allows the narrator to leverage existing metric explanations and concept comparisons, reducing content creation effort. The "AI" label also sets high expectations that template-based output may not meet.

#### 4. Consider Direction B (Notification System) as Sprint 5 Parallel Track

**Rationale**: At 8–14h, the notification system is low-effort and fully standalone. It can be developed in parallel with C62/C60/C55 without resource contention. However, its value is proportional to the content it points to — it's most effective when there are diary entries, badges, and checklists to nudge users about. Recommend implementing it alongside the Quick Wins Bundle so notifications have content to reference from day one.

#### 5. Critical Path & Dependency Management

```
Sprint 3: C44 → C38 → D16
                          ↓
Sprint 4: R3 → D24 → C51 → C48 → C53-1
                          ↓
Sprint 5: C62 + C60 + C55 + C58 (+ Notification System)
                          ↓
Sprint 6: C56 + C57 + C61 (+ C34 if approved)
                          ↓
Sprint 7+: C59 (+ C3 if approved)
```

**Key dependency**: D24 (business_card.py sub-directory extraction) is the single most critical enabler for Sprint 5. Without it, C62 and C55 both risk bloating business_card.py past 600 lines. D24 must be completed in Sprint 4.

#### 6. Content Creation Parallel Workstream

The biggest hidden cost across all directions is **content creation**, not coding:
| Content File | For | Estimated Writing Effort |
|-------------|-----|------------------------|
| `event_templates.yaml` | C34 | 3–5h |
| `narrative_templates.yaml` | C3 | 4–6h |
| `notification_templates.yaml` | C2 | 2–3h |
| `checklist_items.yaml` | C62 | 2–3h |
| `badges.yaml` | C60 | 2–3h |
| `metric_explanations.yaml` | C56 | 3–5h (already planned for Sprint 4) |
| `concept_pairs.yaml` | C57 | 3–5h (already planned for Sprint 4) |
| **Total new content** | | **19–30h** |

**Recommendation**: Start content creation for C62 (`checklist_items.yaml`) and C60 (`badges.yaml`) in Sprint 4 as a parallel workstream. These are the simplest content files and unblock Sprint 5 development. Defer C34/C3 content to Sprint 5.

#### 7. Risk Summary

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **business_card.py bloat** — multiple features adding to same file | High | High | D24 is non-negotiable. Must complete in Sprint 4. |
| **Content creation bottleneck** — YAML writing takes longer than coding | High | Medium | Start content creation early (Sprint 4). Use LLM for first drafts. |
| **Feature overlap** — C34/C3/C56/C59 all involve "explaining" | Medium | High | Clear scope definitions per feature. Coordinate with PM. |
| **Historian tone drift** — templates slip into predictive language | Medium | High | Automated tense checking. Manual review checklist. |
| **Streamlit limitations** — onboarding overlays, anchor links, toasts | High | Medium | Simplified implementations. Accept imperfection for MVP. |
| **Session state scalability** — too many keys from multiple features | Low | Low | Monitor. Refactor to session state manager if needed (D25). |

#### 8. Total Effort Summary

| Direction | Sprint | Effort (Low) | Effort (High) | Risk |
|-----------|--------|-------------|--------------|------|
| D: Quick Wins (C62+C60+C55) | 5 | 26h | 40h | 🟢 Low |
| B: Notification System | 5 | 8h | 14h | 🟢 Low |
| A: Company Story Timeline (C34) | 6 | 18h | 26h | 🟡 Medium |
| C: Historical Narrator (C3) | 7+ | 14h | 22h | 🟡 Medium |
| **Total new (Round 13)** | | **66h** | **102h** | |
| **With 20% buffer** | | **79h** | **122h** | |

Adding to the existing approved pipeline (Sprints 4–7: 114–175h), the **total remaining effort** including Round 13 proposals is **180–277h** (216–332h with buffer).

---

*Created: 2026-06-12*
*Role: Developer*
*Discussion cycle: Round 13*
*Confidence level: High (based on thorough codebase review of all source files, architecture constraints, and Round 12 estimate validation)*
