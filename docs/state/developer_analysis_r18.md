# Developer Estimate — Discussion Round 18

**Date:** 2026-06-13
**Author:** Developer (owl-alpha)
**Sprint:** 9 (C98 + C101 + C103)
**Context:** Sprint 8 complete (7/7 debt items). L0: 85/85 ✅. L1: 8/18 (10 pre-existing event-alert failures unchanged).

---

## C98: Event Interpretation Engine

### Architecture Analysis

C98 adds plain-language interpretation to events already detected by `adaptive_engine.py`. The existing event detection produces structured dicts with `type`, `severity`, `title`, and `summary` fields. C98 must transform these into richer, contextual, historian-tone narratives.

**Key observation:** The codebase has NO existing LLM client. Both `news_summarizer.py` and `compare_stories.py` explicitly state "不使用 LLM" (no LLM). The architecture doc says "LLM for plain-language translation only." C98's interpretation engine needs either:
- (A) A template-based approach (following `news_summarizer.py` pattern) — lower quality ceiling but zero infrastructure cost
- (B) An LLM-backed approach — higher quality but requires new infrastructure (API client, key management, rate limiting, cost)

The review report says "LLM for plain-language translation only" as a constraint, and the product vision update (structural change #6) expands LLM scope to "interpretation with data citation." This means C98 is the FIRST feature that would use LLM for interpretation, not just translation. This is a significant architectural decision that the 2h spike must resolve.

### Subtask Breakdown

#### Phase 0: Spike (Conditional Gate)
- **S0.1:** Evaluate template-based vs LLM-backed approach. Build 3-sample prototype of each using real events from `events.yaml`. Compare output quality, latency, and cost. (1h)
- **S0.2:** If LLM route: design `llm_client.py` service (API abstraction, rate limiting, error handling, mock for tests). If template route: design interpretation template schema. (1h)
- **Spike total: 2h**

#### Phase 1: Core Service (assuming LLM route chosen)
- **S1.1:** Create `src/services/event_interpretation_engine.py` — interpretation service with `interpret_event(event_dict, stock_context) -> str` public API. Must follow service layer conventions (no streamlit import, no side effects, pure function). (3h)
- **S1.2:** Create `src/services/llm_client.py` — lightweight LLM client wrapper. Must support: sync call, timeout, error fallback, mock mode for testing. No streaming (Streamlit request-response architecture). (3h)
- **S1.3:** Design and create interpretation prompt templates per event type (`revenue_surge`, `news_major`, `news_medium`, `price_abnormal`). Each template must include: event data, stock context (name, industry), historian tone instructions, data citation requirement. (2h)
- **S1.4:** Implement fallback chain: LLM → template-based interpretation → raw summary passthrough. No layer may raise uncaught exceptions. (1.5h)
- **S1.5:** Add in-memory result cache (event_id + stock_id → interpretation) to avoid re-interpreting same events on re-render. TTL = session duration (use dict, not file cache). (1h)
- **Phase 1 total: 10.5h**

#### Phase 2: Integration
- **S2.1:** Integrate into `event_dashboard.py` — add interpretation text below each event's existing summary in the expander. Use `st.spinner("解讀中...")` during LLM call. Handle timeout gracefully. (2h)
- **S2.2:** Integrate into `event_dashboard.py` `_render_event_alerts()` — add 1-line interpretation to existing alert display on stock pages. (1h)
- **S2.3:** Add `interpretation` field to event dict in `adaptive_engine.py` `record_event()` flow — or keep interpretation on-demand (recommend on-demand to avoid blocking event recording). (1h)
- **Phase 2 total: 4h**

#### Phase 3: Testing & Verification
- **S3.1:** Unit tests for `event_interpretation_engine.py` — mock LLM client, test all event types, test fallback chain, test cache. (2h)
- **S3.2:** Unit tests for `llm_client.py` — test timeout, error handling, mock mode. (1h)
- **S3.3:** L0 verification — all 85 existing tests must still pass. (0.5h)
- **S3.4:** L1 verification — no new L1 failures. (0.5h)
- **Phase 3 total: 4h**

### Total Estimate

| Scenario | Hours |
|----------|-------|
| Spike (S0) | 2h |
| Phase 1 — Core (S1) | 10.5h |
| Phase 2 — Integration (S2) | 4h |
| Phase 3 — Testing (S3) | 4h |
| **Contingency (15%)** | 3h |
| **TOTAL (LLM route)** | **23.5h** |
| **TOTAL (template route, if spike rejects LLM)** | **16h** |

**PM estimate was 14-18h. My estimate is 16-23.5h.** The gap is because:
1. No existing LLM client — building one is 3h of infrastructure that PM estimate may have assumed exists
2. Fallback chain is mandatory (architecture error handling rules) — adds 1.5h
3. Caching is needed to avoid re-calling LLM on every re-render — adds 1h
4. The 2h spike is a hard prerequisite — if LLM route fails spike validation, we fall back to templates and the 16h estimate applies

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **No existing LLM client** — must build from scratch. API key management, rate limiting, timeout handling all new code. | High | Certain | Spike validates approach first. `llm_client.py` is a reusable service for future features. |
| **LLM latency in Streamlit request-response** — LLM calls are synchronous and may take 2-5s. Streamlit will block. | High | High | Use `st.spinner()` during call. Set aggressive timeout (5s). Fallback to template if timeout. Cache results. |
| **LLM cost unpredictability** — each event interpretation is a separate API call. 50 events × multiple users = cost. | Medium | Medium | Cache aggressively. Consider batch interpretation. Template fallback reduces LLM calls. |
| **Prompt quality for historian tone** — LLM may not consistently produce historian-framed interpretations. | Medium | Medium | Careful prompt engineering with examples. Add tone validation in tests. |
| **Event dict schema mismatch** — `adaptive_engine.py` events have varying fields. Interpretation engine must handle missing/extra fields gracefully. | Medium | Medium | Defensive dict access with defaults. Test with real events from `events.yaml`. |
| **Spike may reject LLM route** — if latency/cost is unacceptable, template approach is fallback with lower quality. | Medium | Medium | Template approach is viable (see `news_summarizer.py` pattern). Quality is lower but still valuable. |
| **Dependency on external API** — LLM downtime = feature degradation. | Low | Low | Fallback chain ensures graceful degradation to template → raw summary. |

### Dependencies
- `adaptive_engine.py` — event detection output schema (stable, well-tested)
- `event_dashboard.py` — integration target (stable)
- `news_summarizer.py` — template pattern reference (if template route chosen)
- Architecture layer rules — service layer must not import streamlit

---

## C101: Comprehension Check Quiz

### Architecture Analysis

C101 replaces the cancelled C52 (Quiz Mode). The pattern is well-established in the codebase: `financial_wellness.py` + `financial_wellness_service.py` is a nearly identical pattern — a standalone quiz page with YAML-backed questions, session-state answer tracking, scoring, and results display.

**Key difference from C85:** C101 tests comprehension of stock-specific content (what the user learned about a stock they viewed), not general financial wellness. This means:
- Questions must be dynamically generated or selected based on the stocks the user has studied
- Question content must reference actual stock data/events the user has seen
- The quiz is likely a stock-page section (not standalone page), integrated into the study flow

**Alternative interpretation:** C101 could be a standalone "comprehension check" page that quizzes users on general stock concepts (like C85 quizzes on financial behavior). This would be simpler but less connected to the historian mission.

Given the "historian" positioning and that C101 replaces C52 (which was "Quiz Mode" for stock content), I'll assume the stock-specific comprehension quiz interpretation.

### Subtask Breakdown

#### Core Service
- **S1.1:** Create `src/services/comprehension_quiz_service.py` — quiz logic service. Public API: `generate_quiz(stock_id, study_context) -> list[Question]`, `grade_answers(answers) -> QuizResult`, `get_explanation(question_id, correct_answer) -> str`. No streamlit import. (3h)
- **S1.2:** Create question bank in YAML (`config/comprehension_quiz.yaml`) — 20-30 template questions parameterized by stock data. Categories: revenue understanding, event interpretation, financial health assessment, peer comparison. Each question: id, template_text, options, correct_answer, explanation_template, category. (2.5h)
- **S1.3:** Implement question selection algorithm — select 5-8 questions based on: (a) stocks user studied today (from study_log), (b) events detected for those stocks, (c) variety across categories. Avoid repeating questions within session. (2h)
- **S1.4:** Implement answer grading with explanations — for each answered question, provide: correct/answer indicator, plain-language explanation citing actual stock data, "learn more" link to relevant page. (1.5h)

#### Presentation Layer
- **S2.1:** Create `src/pages/comprehension_quiz.py` — standalone page following `financial_wellness.py` pattern. Quiz form with `st.form`, radio buttons per question, submit button, results display with score + per-question feedback. (2.5h)
- **S2.2:** Register in router (`router.py`) as standalone page (no stock_id required). Add to navbar. (0.5h)
- **S2.3:** Add "Take Quiz" CTA to study log section (`_study_log.py`) — after user views 3+ stocks, show prompt to test comprehension. (1h)

#### Testing & Verification
- **S3.1:** Unit tests for `comprehension_quiz_service.py` — test question generation, grading, explanation generation, edge cases (no study history, single stock, many stocks). (2h)
- **S3.2:** L0 + L1 verification. (0.5h)
- **Phase 3 total: 2.5h**

### Total Estimate

| Subtask | Hours |
|---------|-------|
| S1.1 — Quiz service | 3h |
| S1.2 — YAML question bank | 2.5h |
| S1.3 — Question selection | 2h |
| S1.4 — Grading + explanations | 1.5h |
| S2.1 — Quiz page UI | 2.5h |
| S2.2 — Router registration | 0.5h |
| S2.3 — Study log CTA | 1h |
| S3.1 — Unit tests | 2h |
| S3.2 — L0/L1 verification | 0.5h |
| **Contingency (10%)** | 1.5h |
| **TOTAL** | **17h** |

**PM estimate was 8-12h. My estimate is 17h.** The gap is because:
1. PM estimate likely assumed a simpler static quiz (like C85). Stock-specific comprehension requires dynamic question generation/selection — adds ~4h
2. Question bank creation (YAML) is content-heavy — 2.5h for 20-30 quality questions with explanations
3. Question selection algorithm (avoiding repeats, balancing categories, matching study history) is non-trivial — 2h
4. I'm being conservative on UI since quiz UX is deceptively complex (form state, results display, explanations)

**If scoped down to static quiz (no stock-specific questions, just general concept quiz like C85):** ~11h (within PM range).

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **Question quality** — auto-generated or template-based questions may feel generic or test trivia not comprehension. | High | High | Manual question writing (not auto-generated). Historian tone QA gate before shipping. |
| **Study log dependency** — if user hasn't studied enough stocks, quiz has no context. | Medium | Medium | Fallback to general questions when study history is sparse. Minimum 3 stocks needed for stock-specific mode. |
| **Session state complexity** — quiz state (answers, results, current question) must survive page switches. | Medium | Low | Use `st.session_state` with prefixed keys (like C85 does). Well-established pattern. |
| **Content maintenance** — YAML question bank needs updates as features/stocks change. | Low | High | Keep questions general enough to be evergreen. Separate content update from code changes. |
| **LLM not needed** — unlike C98, C101 can be fully template-based. This is actually lower risk. | Low | Certain | No LLM dependency. Fully deterministic. |

### Dependencies
- `financial_wellness_service.py` — reference pattern for quiz service architecture
- `financial_wellness.py` — reference pattern for quiz page UI
- `_study_log.py` — study history for question selection context
- `adaptive_engine.py` — event data for event-related questions
- Architecture layer rules — service layer separate from presentation

---

## C103: First Visit Guide

### Architecture Analysis

C103 is an onboarding flow for first-time users. This is a **standalone page** that must:
1. Detect first visit (no prior session state / no study history)
2. Guide users through the app's key features in a narrative, historian-framed way
3. Not feel like a tutorial — feel like an invitation to explore

**Key architectural question:** Is this a separate page in the nav, or an overlay/modal that appears on first visit? Given Streamlit's architecture (no background worker, request-response), an overlay would require custom JS or careful session_state management. A dedicated "welcome" page that auto-redirects on first visit is cleaner.

**Recommended approach:** A standalone "歡迎" page that:
- Auto-shows on first visit (router detects `"_first_visit"` not in session_state)
- Uses `_summary_card()` and `_info_card()` components for consistent styling
- Has 3-4 steps: (1) What is Stock Explorer, (2) How to explore a stock, (3) What makes it different (historian angle), (4) Start exploring (search box)
- Sets `"_first_visit_complete"` in session_state after completion
- Can be re-accessed from nav as "使用指南"

### Subtask Breakdown

#### Core Logic
- **S1.1:** Create `src/services/first_visit_service.py` — service with `is_first_visit(session_state) -> bool`, `get_guide_steps() -> list[GuideStep]`, `mark_complete(session_state)`. No streamlit import. (1.5h)
- **S1.2:** Create guide content in YAML (`config/first_visit_guide.yaml`) — 4-6 steps, each with: title, body_text, icon, highlight_feature, cta_text. Content must pass historian tone QA. (2h)
- **S1.3:** Implement first-visit detection in router — if first visit, auto-navigate to guide page. After completion, redirect to category browser (entry point for exploration). (1h)

#### Presentation Layer
- **S2.1:** Create `src/pages/first_visit_guide.py` — standalone page. Step-by-step layout using existing card components. Progress indicator. "Skip" and "Next" buttons. Final step has search box to start exploring. (3h)
- **S2.2:** Register in router as standalone page. Add "使用指南" to navbar (last position, muted style). (0.5h)
- **S2.3:** Add route guard in `router.py` — on first visit (no `"_first_visit_complete"` in session_state and no study history), auto-redirect to guide page. (1h)

#### Testing & Verification
- **S3.1:** Unit tests for `first_visit_service.py` — test first visit detection, guide step retrieval, completion marking. (1h)
- **S3.2:** L0 + L1 verification. (0.5h)
- **Phase 3 total: 1.5h**

### Total Estimate

| Subtask | Hours |
|---------|-------|
| S1.1 — First visit service | 1.5h |
| S1.2 — Guide content YAML | 2h |
| S1.3 — Router detection | 1h |
| S2.1 — Guide page UI | 3h |
| S2.2 — Router registration | 0.5h |
| S2.3 — Route guard | 1h |
| S3.1 — Unit tests | 1h |
| S3.2 — L0/L1 verification | 0.5h |
| **Contingency (10%)** | 1h |
| **TOTAL** | **11.5h** |

**PM estimate was 10-14h. My estimate is 11.5h.** This is well within PM range. The feature is straightforward with no new infrastructure needed.

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **First visit detection reliability** — session_state is per-browser-session. Incognito/private browsing = "first visit" every time. | Medium | High | Acceptable. Guide is helpful even on repeat "first visits." Don't over-engineer persistence. |
| **Content quality** — guide must be engaging, not boring tutorial text. Historian tone is hard to maintain in onboarding. | High | Medium | PM/Designer must write content. Dev provides structure only. Historian tone QA gate applies. |
| **Route guard complexity** — auto-redirect in router could cause redirect loops if not careful. | Medium | Low | Set `"_first_visit_complete"` BEFORE redirect. Test thoroughly. |
| **Streamlit limitations** — no true modal/overlay. Page-based guide is less elegant than modal tutorial. | Low | Certain | Accept the limitation. Page-based is actually cleaner in Streamlit. |
| **i18n consideration** — guide is in Traditional Chinese. If app expands to other languages, YAML structure supports this but it's future work. | Low | Low | Out of scope for Sprint 9. |

### Dependencies
- `_router_base.py` — card components (`_summary_card`, `_info_card`)
- `router.py` — registration and route guard
- `_section_title()` — for step headers
- `historian_disclaimer()` — for tone consistency
- No dependency on C98 or C101

---

## Recommended Implementation Order

### Priority Order: C103 → C101 → C98

**Rationale:**

1. **C103 first (First Visit Guide)** — Lowest risk, no dependencies, no new infrastructure. Can be built and tested independently. Validates the "historian onboarding" concept that C98 and C101 build on. Quick win that unblocks user testing.

2. **C101 second (Comprehension Check Quiz)** — Medium risk, no LLM dependency, follows established C85 pattern. Builds on study_log infrastructure. Can be developed in parallel with C98 spike. If C101 is scoped as static quiz, it's low-risk.

3. **C98 last (Event Interpretation Engine)** — Highest risk, requires spike first, may need new LLM infrastructure. Benefits from C101 being done first (quiz can test comprehension of interpreted events). The 2h spike must complete before committing to full C98 development.

### Alternative: C101 + C103 parallel, then C98

If two developers are available: C101 and C103 can be built simultaneously (no shared dependencies). C98 starts with spike while C101/C103 are in development.

### What NOT to do

- Do NOT start C98 without completing the spike. The LLM vs template decision changes the entire architecture.
- Do NOT build C101 as stock-specific quiz without validating question generation approach. Start with static questions, add dynamic selection in v2.
- Do NOT make C103 a modal/overlay. Streamlit doesn't support this cleanly. Page-based is the right call.

---

## Total Sprint 9 Effort

| Feature | Low Estimate | High Estimate | Most Likely |
|---------|-------------|---------------|-------------|
| C98 spike | 2h | 2h | 2h |
| C98 dev (if LLM route) | 18h | 24h | 21h |
| C98 dev (if template route) | 12h | 16h | 14h |
| C101 | 14h | 20h | 17h |
| C103 | 10h | 13h | 11.5h |
| **TOTAL (LLM route)** | **44h** | **59h** | **51.5h** |
| **TOTAL (template route)** | **38h** | **51h** | **44.5h** |

**PM estimate was 34-46h. My estimate is 44.5-51.5h (LLM) or 38-51h (template).**

The gap is primarily from:
1. C98 infrastructure (LLM client) not accounted for in PM estimate — +3h
2. C101 stock-specific scope is larger than static quiz — +5h
3. Contingency buffers — +4h

**If the team wants to fit within PM's 34-46h budget:**
- C98: Use template route (saves ~7h)
- C101: Use static quiz only, no stock-specific questions (saves ~6h)
- C103: As estimated (within range)
- **Adjusted total: ~36-42h** (within PM range)

---

## Challenger Response Preparation

**Anticipated challenges and my responses:**

1. **"C98 is too expensive — can we use templates only?"**
   - Yes. The spike will validate. Template approach follows `news_summarizer.py` pattern and delivers 70% of the value at 60% of the cost. Recommend spike-first gate.

2. **"C11 is too expensive — why not just copy C85?"**
   - C85 is a general behavioral quiz. C101 tests stock-specific comprehension, which requires dynamic question selection based on study history. If we scope it down to a static concept quiz, cost drops to ~11h.

3. **"Can we do all three in one sprint?"**
   - At 44-51h, this is a heavy sprint but feasible if the team has ~25h/week capacity (2-week sprint = 50h). Risk: C98 spike failure could block the largest feature. Mitigate by starting spike on day 1.

4. **"Why does C98 need a new LLM client? Can't we just call the API directly?"**
   - Architecture rules require service layer abstraction. Direct API calls from service layer without a client wrapper would violate error handling conventions, make testing impossible, and create tech debt. The `llm_client.py` is a reusable investment.

5. **"C103 seems low-value for Sprint 9."**
   - Agree it's the lowest-value feature. But it's also the lowest-risk and can be completed in parallel. It improves first-user experience which affects retention metrics. Recommend keeping it but deprioritizing if sprint capacity is tight.

---

*Analysis complete. All estimates based on actual codebase review of adaptive_engine.py (622 lines), analogy_engine.py (193 lines), financial_wellness_service.py (176 lines), financial_wellness.py (215 lines), event_dashboard.py (172 lines), news_summarizer.py (158 lines), router.py (211 lines), and _router_base.py (226 lines).*
