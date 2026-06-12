# 2026-06-13 Technical Analysis — Discussion Round 18

**Author**: System Architect
**Role**: Technical feasibility analysis for Sprint 9 candidate features
**Scope**: C98, C101, C103 — architecture, feasibility, risks, and proposed directions

---

## Problem Description

Sprint 8 is complete (all 7 debt items addressed). Sprint 9 has three candidate features on the table:

| ID | Feature | Priority | Effort | Status |
|----|---------|----------|--------|--------|
| C98 | Event Interpretation Engine | P1 | 14-18h | CONDITIONAL |
| C101 | Comprehension Check Quiz | P2 | 8-12h | CONFIRMED |
| C103 | First Visit Guide | P2 | 10-14h | CONDITIONAL |

The core question for Sprint 9 is: **given the current architecture (4-layer Streamlit, no background worker, LLM used for translation only), which combination of these features is technically feasible, and in what order?**

The product vision is "historian, not stock picker" — every feature must reinforce education, not trading. The current state is L0: 85/85 ✅, L1: 8/18 (10 pre-existing event-alert failures unchanged).

---

## Technical Feasibility Analysis

### C98: Event Interpretation Engine

**What it does**: Adds a "why this matters" plain-language interpretation layer on top of events already detected by the M5 adaptive engine. Currently, events are displayed as raw data (title + summary keyword) in the event dashboard and event alerts.

**Current state of the M5 engine** (`src/services/adaptive_engine.py`):
- The engine already detects 4 event types: `revenue_surge`, `news_major`, `news_medium`, `price_abnormal`
- Events are stored in `config/events.yaml` with fields: `stock_id`, `date`, `type`, `severity`, `title`, `summary`
- The `summary` field is currently a template-generated string (e.g., "最近月營收 4170 億元，較去年同期增加 30%。表現亮眼，關注後續動能。")
- The event dashboard (`event_dashboard.py`) renders these as expanders with badge + type + title + summary
- The event alerts (`_render_event_alerts`) show raw title + summary in `st.error()`/`st.warning()` boxes

**What C98 needs to add**:
1. A new service (e.g., `event_interpretation_service.py`) in the Business Logic Layer
2. Takes an event dict (type, severity, title, summary, stock_id) → returns a plain-language interpretation string
3. The interpretation explains *why the event matters* in educational terms, not just *what happened*

**Critical architectural question: LLM or template?**

The current architecture states: "LLM used for plain-language translation only (not fact generation)." C98 sits at the boundary:
- **Template approach**: Pre-written interpretation templates per event type. Fast, no API cost, no latency. But limited nuance — can't contextualize "revenue surge + price drop" as a combined signal.
- **LLM approach**: Send event data + company context to LLM, get back educational interpretation. More nuanced, but adds API latency (2-5s per event), cost, and failure mode. Also requires careful prompt engineering to ensure the LLM doesn't generate investment advice (violates "historian" positioning).
- **Hybrid approach**: Template base + LLM enhancement for high-severity events only. Templates handle 80% of cases; LLM handles the nuanced 20%.

**Feasibility verdict**: ✅ FEASIBLE, but with caveats.
- The service layer slot exists and the pattern is well-established (analogy_engine.py is the template)
- The biggest risk is **latency**: if using LLM, each event interpretation adds 2-5s. With 50 events on the dashboard, that's 100-250s of LLM calls — unacceptable for page load.
- **Recommendation**: Use template-based interpretation for the dashboard (fast), with optional LLM enhancement on individual event click (lazy loading). This keeps the architecture clean and the user experience responsive.

**Integration points**:
- `event_dashboard.py` (Presentation Layer) calls new service to enrich event display
- `adaptive_engine.py` (Business Logic Layer) — no changes needed; C98 is a consumer of existing event data
- `router.py` — no changes needed; event rendering is already in the dashboard page

---

### C101: Comprehension Check Quiz

**What it does**: Contextual quiz questions that appear after users read content sections. Replaces the cancelled C52 (standalone quiz mode). Questions are multiple-choice, with adaptive feedback and learning recommendations.

**Current state**:
- `financial_wellness_service.py` already implements a full quiz engine: YAML-loaded questions, answer scoring, category mapping, weak-area detection, personalized tips
- The pattern is: YAML config → service layer (pure logic) → page layer (Streamlit UI)
- `config/quiz.yaml` has the data structure: questions with id, text, options (key/label/score), category_map, category_tips

**What C101 needs to add**:
1. A new YAML config for content-specific quiz questions (e.g., `config/comprehension_quiz.yaml`)
2. A new service (`comprehension_quiz_service.py`) — can reuse 90% of the financial_wellness_service.py pattern
3. UI integration into business card page sections (the "🧠 小測驗" button after each section)
4. Session-state tracking of answers to compute weak areas

**Feasibility verdict**: ✅ HIGHLY FEASIBLE.
- The quiz engine pattern is already proven (C85 financial_wellness_service.py)
- The YAML config pattern is proven (quiz.yaml, case_studies.yaml)
- The session-state pattern is proven (financial_wellness.py uses session_state for answers)
- The main effort is **content creation** (writing quiz questions), not engineering
- The 8-12h estimate is realistic: ~3h service + ~3h UI integration + ~2-6h content creation

**Integration points**:
- `business_card/_sections/*.py` (Presentation Layer) — add quiz button after each section
- New `comprehension_quiz_service.py` (Business Logic Layer) — quiz logic
- `config/comprehension_quiz.yaml` (Data Layer) — question bank
- `router.py` — no changes needed

**Risk**: Content scope. The competitor research says "2-3 questions per section." With 6 sections per business card page, that's 12-18 questions per stock. For 15 stocks, that's 180-270 questions — a lot of content. **Recommendation**: Start with 5-8 high-quality questions total (not per section), covering the most important concepts. Expand later.

---

### C103: First Visit Guide

**What it does**: Onboarding flow for first-time users. Shows a "Before you dive in" primer with 3-4 cards explaining what they'll learn, key terms, and estimated reading time. Users can skip it.

**Current state**:
- No onboarding system exists
- `session_state` is available for tracking first visits
- The `_render_adaptive_banner` pattern in `event_dashboard.py` shows how to display contextual info at the top of a page
- The `get_one_liner` function in `analogy_engine.py` already provides the "company in one sentence" content

**What C103 needs to add**:
1. A session-state flag system: `first_visit_to_{page}` per page per user
2. A new service (`onboarding_service.py`) that returns primer content for a given page/company
3. UI rendering in the business card page (or router) that shows the primer on first visit
4. A "skip" button that sets the flag and triggers rerun

**Feasibility verdict**: ✅ FEASIBLE, but with architectural considerations.
- The session-state pattern is straightforward
- The content can be template-based (no LLM needed): "What you'll learn on this page" can be generated from section metadata
- The main question is **where to render it**: in the router (before any page) or in each page individually?
  - **Router approach**: Cleaner, single code point. But the router doesn't have page-specific content knowledge.
  - **Page approach**: Each page renders its own primer. More code duplication, but each page knows its own content.
  - **Recommendation**: Create a shared `_render_first_visit_primer(page_name, data)` helper in `_router_base.py` that pages call at the top. This balances DRY with page-specific content.

**Integration points**:
- `_router_base.py` — add shared primer helper function
- `business_card/_main.py` — call primer helper at top of page
- New `onboarding_service.py` (Business Logic Layer) — returns primer content
- `router.py` — may need to initialize first-visit flags
- `session_state` — `first_visit_to_{page}` flags

**Risk**: The "soft gate" UX pattern is untested in this codebase. If the primer is too prominent, it blocks content. If too subtle, users miss it. **Recommendation**: Make it a collapsible `st.expander` that's expanded by default on first visit, collapsed on subsequent visits. This is the lightest-touch approach.

---

## Feature Direction A: Education Layer Stack (C98 + C101 Combined)

**Description**: Implement both C98 (Event Interpretation) and C101 (Comprehension Quiz) as a unified "education layer" that wraps existing content with interpretation and verification. C98 enriches the event dashboard; C101 adds quizzes to business card pages. Together they form a "learn → interpret → verify" loop.

**Pros**:
- Strong alignment with "historian, not stock picker" — both features are purely educational
- C101 reuses the proven C85 quiz engine pattern (low risk)
- C98 leverages existing M5 event data (no new detection logic needed)
- Combined effort (22-30h) fits within a single sprint
- The two features share a conceptual framework: C98 explains events, C101 verifies understanding
- Template-based C98 avoids LLM latency issues entirely

**Cons**:
- C98's value is limited without LLM — template interpretations may feel robotic
- C101 requires significant content creation (quiz questions) that's hard to estimate
- No onboarding improvement (C103 deferred) — new users still hit a wall of data
- C98 + C101 together are 22-30h, leaving no room for C103 in Sprint 9

**Effort**: 22-30h (C98: 14-18h + C101: 8-12h)
- C98: 4h service + 3h templates + 4h UI integration + 3-7h testing/iteration
- C101: 3h service + 3h UI + 2-6h content creation

**Technical Risks**:
- **Medium**: C98 template quality — if templates are too generic, the feature adds no value over existing summaries
- **Medium**: C101 content scope — writing good quiz questions is harder than writing code; PM/designer dependency
- **Low**: Architecture fit — both features follow established patterns
- **Low**: Performance — template-based C98 has zero latency; C101 is session-state only

---

## Feature Direction B: Template-First C98 + C103 (Interpret + Onboard)

**Description**: Implement C98 using a template-based approach (no LLM) combined with C103 (First Visit Guide). This prioritizes the two "conditional" features and creates a complete new-user experience: onboarding primer → content → event interpretation.

**Pros**:
- C103 addresses the biggest UX gap: new users have no orientation
- Template-based C98 is fast, reliable, and has no API dependencies
- Combined effort (24-32h) is manageable
- C103 is a one-time UX improvement that benefits all future features
- No LLM dependency means no latency, no cost, no failure modes

**Cons**:
- Defers C101 (CONFIRMED priority) — this is a political/process risk
- Template-based C98 may not satisfy the "interpretation" promise — templates can't contextualize multiple simultaneous events
- C103's "soft gate" pattern is untested and may need iteration
- No learning verification layer (C101) means no way to measure if users actually understand content

**Effort**: 24-32h (C98: 14-18h + C103: 10-14h)
- C98: 4h service + 5h templates (more templates needed without LLM) + 3h UI + 2-6h testing
- C103: 3h service + 3h UI + 2h session-state logic + 2-6h UX iteration

**Technical Risks**:
- **High**: C98 template coverage — without LLM, need templates for every event type × severity combination. Currently 4 types × 3 severities = 12 templates minimum. Edge cases will be missed.
- **Medium**: C103 session-state complexity — tracking first-visit per page per user could conflict with existing session_state usage
- **Low**: C103 content — primer text can be generated from existing section metadata

---

## Feature Direction C: Phased Education Stack (C101 first, then C98, then C103)

**Description**: Implement C101 first (8-12h, CONFIRMED), then use remaining sprint time for a C98 spike (2h) to validate the template approach, then implement a lightweight C103 (reduced scope: just the one-liner + section preview, no glossary). Total: 3 features, phased by risk.

**Pros**:
- C101 is CONFIRMED and lowest-risk — delivers value immediately
- C98 spike validates feasibility before committing 14-18h
- Lightweight C103 delivers onboarding value without the full 10-14h investment
- All 3 features get some attention in Sprint 9
- If C98 spike reveals template approach is insufficient, the team can decide to defer C98 without having invested full effort

**Cons**:
- Spreading effort across 3 features means none gets full attention
- C98 spike (2h) may not be enough to validate the approach — template writing itself is the risk, and 2h isn't enough to write and test 12+ templates
- Lightweight C103 may be too minimal to provide real onboarding value
- Total effort could exceed sprint capacity if all 3 are attempted

**Effort**: 20-28h (C101: 8-12h + C98 spike: 2h + C103 lite: 10-14h)
- C101: 3h service + 3h UI + 2-6h content
- C98 spike: 2h (write 3-4 templates, test on event dashboard)
- C103 lite: 2h service + 3h UI + 2h session-state + 3-7h UX

**Technical Risks**:
- **Medium**: Sprint scope creep — 3 features in one sprint is ambitious
- **Low**: C101 is proven pattern
- **Medium**: C98 spike may produce inconclusive results in 2h
- **Low**: C103 lite is simpler than full C103

---

## Recommendation

**Direction A (C98 + C101) is the strongest technical choice**, with one critical modification:

### Modified Direction A: C98 (Hybrid) + C101

1. **C98 — Hybrid approach**: Use template-based interpretation for the event dashboard (all 50 events, fast rendering). Add optional LLM interpretation on individual event click (lazy-loaded, one at a time). This gives users the fast dashboard they need PLUS the deep interpretation they want, without the latency penalty of LLM-for-all.

2. **C101 — Scoped to 5-8 questions**: Don't try to cover every section. Write 5-8 high-quality questions covering the most important financial concepts (ROE,毛利率,本益比,殖利率,負債比). These can be reused across all stock pages. This keeps content creation manageable.

3. **Defer C103 to Sprint 10**: C103 is important but not urgent. The onboarding gap exists but doesn't block current users. Sprint 10 can address it after the education layer (interpret + verify) is in place.

### Rationale:

- **Technical coherence**: C98 and C101 together form a complete "educational feedback loop" — interpret what happened, then verify understanding. This is the core of the "historian" vision.
- **Risk management**: Hybrid C98 avoids the all-templates-vs-all-LLM binary. C101's scoped content avoids the content creation black hole.
- **Architecture fit**: Both features follow established patterns (analogy_engine for templates, financial_wellness for quiz). No new infrastructure needed.
- **Sprint capacity**: 22-30h is realistic for a sprint. Leaves buffer for bug fixes and iteration.

### Key Technical Decisions Needed:

1. **C98 LLM scope**: Does the product vision allow LLM for interpretation (not fact generation)? The distinction is blurry — interpreting an event requires contextual knowledge that templates can't provide. Need PM/designer alignment on LLM usage boundaries.
2. **C101 content ownership**: Who writes the quiz questions? If it's a PM/designer task, the 8-12h dev estimate is accurate. If developers write them, add 4-6h.
3. **C98 template count**: Need to decide how many event type × severity combinations to template. Minimum viable: 4 types × 2 severities (high/medium) = 8 templates. Full coverage: 4 × 3 = 12 templates.

---

## Challenger Response Preparation

**Anticipated challenge**: "C98 without LLM is just a summary, not an interpretation. You're shipping a feature that doesn't deliver on its promise."

**Response**: Agree. That's why the hybrid approach is recommended — templates for the dashboard (where speed matters), LLM for individual event drill-down (where depth matters). The template layer alone is not sufficient for the full C98 vision, but it provides 80% of the value at 20% of the cost. The LLM layer can be added incrementally after the spike validates the approach.

**Anticipated challenge**: "C101 replaces C52 but C52 was cancelled for a reason. Why is C101 different?"

**Response**: C52 was a standalone quiz mode — a separate page with disconnected questions. C101 is contextual — questions appear after reading specific content, making them directly relevant to what the user just learned. The UX is fundamentally different: C52 was "take a test," C101 is "check your understanding." The contextual approach has higher retention value and lower user friction.

**Anticipated challenge**: "Why defer C103? First visit experience is critical for a beginner-focused product."

**Response**: Agree it's important. The recommendation to defer is purely based on sprint capacity, not feature value. If the team believes C103 is more important than C98, Direction B (C98 + C103) is the alternative. However, C101 is CONFIRMED and should not be deferred. The question is whether to pair C101 with C98 (Direction A) or C103 (Direction B variant).

---

*Analysis based on: architecture.md (4-layer architecture), adaptive_engine.py (622 lines, M5 event detection), analogy_engine.py (193 lines, template pattern), financial_wellness_service.py (176 lines, quiz engine pattern), event_dashboard.py (172 lines, current event display), events.yaml (155 lines, 20 real events), competitor_research.md (Rounds 7-9, C98-C103 gap analysis), review_report.md (Round 20, feature status), handoff.md (Sprint 8 complete, Sprint 9 next)*
