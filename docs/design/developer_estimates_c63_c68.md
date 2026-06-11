# Stock Explorer — Developer Estimates: Round 13 New Features (C63-C68)

> **Date**: 2026-06-12
> **Author**: Developer
> **Sprint Status**: Sprint 3 in progress (C44 done, C38 + D16 remaining)
> **Codebase**: ~6,500 LOC across `src/`, 11 service modules, 12 page modules, 4-layer architecture
> **Confidence**: High (based on thorough review of all source files, existing patterns, and Round 13 competitor research)

---

## Codebase Context for Estimation

**Architecture**: 4-layer (Data → Service → Router → View)
- **Data layer**: `finmind_client.py` — single module, 14 API methods, file-cache with TTL
- **Service layer**: 11 modules, pure functions, no Streamlit imports, no API calls
- **Page layer**: 12 modules, consume services + `data` dict from router, render with Streamlit
- **Router**: `router.py` (175 LOC) dispatches to page render functions; `_router_base.py` (177 LOC) loads data + provides shared UI helpers

**Key Patterns Observed**:
- Service modules: thin (~100-250 LOC), stateless pure functions, threshold-based classification
- YAML config files: used for company_facts, events, watchlist — proven pattern for content
- Session state: used for watchlist, events, page navigation — no formal session state manager yet
- Chart module: consistent `_apply_theme_layout` pattern, Plotly-based
- Analogy engine: template-based, stateless, easy to extend
- `business_card.py` is 561 LOC and growing — D24 (sub-directory extraction) is a hard prerequisite for any feature adding to this file

**Relevant Existing Services for C63-C68**:
| Service | LOC | Relevance |
|---------|-----|-----------|
| `analogy_engine.py` | 850 | C63 (sector analogies), C64 (quiz explanations), C68 (digest narratives) |
| `adaptive_engine.py` | 590 | C65 (filing event detection), C68 (market event summaries) |
| `news_summarizer.py` | 158 | C65 (filing section summaries), C68 (news digest) |
| `financial_metrics.py` | 188 | C66 (risk scoring), C67 (sentiment metrics) |
| `risk_analyzer.py` | 567 | C66 (risk profile scoring) |
| `chart.py` | 779 | C63 (sector visualization), C67 (sentiment charts) |
| `company_facts.py` | 46 | C63 (sector facts), C64 (quiz facts) |
| `watchlist.py` | 323 | C67 (watchlist-based sentiment) |

---

## C63: Sector Stories — Thematic Stock Collections

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `sector_stories.yaml` content creation | 3h | 5h | 10 sectors × (story text, key drivers, 3-5 representative stocks with descriptions) |
| `sector_story.py` service | 2h | 3h | Load YAML, lookup by sector, return structured data. Pure function, ~80 LOC |
| `create_sector_overview_chart()` in chart.py | 1.5h | 2.5h | Treemap or bar chart for sector composition. Reuses existing treemap pattern |
| New page: `sector_stories.py` | 3h | 4h | Sector grid → sector detail → stock links. Follows `category_browser.py` pattern |
| Router integration | 0.5h | 1h | Add to navbar, import in router.py |
| Testing & edge cases | 1h | 1.5h | Empty sector, mobile layout, sector with few stocks |
| **Total** | **11h** | **17h** | **Midpoint: 14h** |

### Complexity: **Medium**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Content quality for 10 sectors is uneven | Medium | Users see generic text | Start with 5 high-quality sectors (semiconductors, electronics, finance, food, textile) and expand. Use analogy_engine patterns for consistent tone |
| Sector classification mismatch between FinMind and curated lists | Medium | Stocks appear in wrong sector | Use FinMind's `industry_category` as source of truth; curated stories reference FinMind categories |
| Treemap chart readability with 10+ sectors | Low | Cluttered visualization | Use color-coded cards instead of treemap if readability issues arise; fallback to simple grid |

### Dependencies
- **Hard**: None. All data available from existing `finmind_client.get_stock_info()` and `industry_category` field
- **Soft**: C51 (Sector Heatmap) — if both land in same sprint, they can share `market_data.py` service
- **Soft**: R5 (YAML migration) — if done first, sector data loading follows established pattern

### Recommended Approach
1. Create `config/sector_stories.yaml` with 5 pilot sectors (not 10) — semiconductors, electronics, finance, food, textile
2. Create `src/services/sector_story.py` — pure function: `get_sector_story(sector_name) -> dict`
3. Add `create_sector_overview_chart()` to `chart.py` — treemap showing sector composition
4. Create `src/pages/sector_stories.py` — grid of sector cards → sector detail page with stock links
5. Add "Sector Stories" to navbar in `router.py`
6. **Scope control**: Do NOT build a sector comparison tool — that's C51's job. This is narrative-driven discovery only.

---

## C64: Daily Market Quiz — Gamified Daily Engagement

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `quiz_questions.yaml` content creation | 3h | 5h | 30 questions (one per day for a month) × (question, 4 options, correct index, explanation). Reuse existing analogy_engine explanations |
| `daily_quiz.py` service | 2h | 3h | Pure function: `get_today_question() -> dict`, `check_answer(question_id, answer) -> bool`. Deterministic daily selection (hash of date) |
| Session state integration | 1h | 2h | `st.session_state` for streak counter, last answered date, total answered. No new session state manager needed for MVP |
| Quiz UI component | 2h | 3h | Question card with radio buttons, submit button, feedback display. Reuses `_info_card` pattern |
| Integration point | 0.5h | 1h | Show on homepage (main.py) or as a new sidebar widget. NOT a separate page — should be lightweight |
| Testing & edge cases | 0.5h | 1h | First visit, streak reset, same-day revisit |
| **Total** | **9h** | **15h** | **Midpoint: 12h** |

### Complexity: **Low-Medium**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Session state loss on browser refresh | High | Streak counter resets | Acceptable for MVP. Document as known limitation. If persistence needed, add YAML-based storage (like watchlist) — adds 2h |
| Question quality/accuracy | Medium | Wrong answers damage credibility | All questions must be reviewable facts (e.g., "What is TSMC's stock ID?") not opinions. Source from `company_facts.yaml` |
| Content exhaustion (30 questions/month) | Low | Users see repeat questions | Start with 30 questions. Monthly content refresh is a content task, not engineering. Add `month` field to YAML schema for future rotation |
| Time zone handling for "daily" | Low | Users in different timezones get wrong question | Use server time (Streamlit default). Acceptable — TW market users are all UTC+8 |

### Dependencies
- **Hard**: None. All components exist (session state, YAML loading, UI cards)
- **Soft**: C52 (Quiz Mode) — C64 is a lightweight daily engagement widget; C52 is a full 20-question quiz feature. They should share the YAML schema for questions but are otherwise independent
- **Soft**: C60 (Concept Mastery Badges) — if both land in same sprint, quiz completion could feed badge progress

### Recommended Approach
1. Create `config/quiz_questions.yaml` with 30 questions. Schema: `{id, type: "market|stock|concept", question, options: [a,b,c,d], correct: 0-3, explanation, source_page}`
2. Create `src/services/daily_quiz.py` — `get_today_question()` uses `hash(date) % len(questions)` for deterministic daily selection
3. Add lightweight quiz widget to `main.py` (below stock search, above page content) — NOT a separate page
4. Session state keys: `quiz_streak`, `quiz_last_date`, `quiz_total_correct`, `quiz_today_answered`
5. **Scope control**: No leaderboard (requires user identity). No rewards. Streak counter only. Leaderboard is v2.
6. **Content strategy**: Write 10 questions for each type (market/stock/concept). Reuse existing `analogy_engine` and `company_facts` content for explanations.

---

## C65: Company Filing Explorer — AI-Parsed Annual Reports

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| Research: TW annual report data source | 2h | 4h | FinMind doesn't have annual reports. Need to identify data source (MOPS? scrape? manual upload?). This is the critical path |
| `filing_parser.py` service | 4h | 6h | Parse filing text into sections, extract key metrics. Pure function. ~150 LOC |
| `filing_explainer.py` service | 3h | 5h | Generate plain-language explanations for each section. Template-based (like news_summarizer). ~200 LOC |
| `filing_sections.yaml` content | 2h | 3h | Section definitions, explanation templates, key metric extraction rules |
| New page: `filing_explorer.py` | 3h | 5h | Section navigation sidebar, main content area with expandable explanations. Follows `financial_health.py` pattern |
| Chart: filing metrics visualization | 1.5h | 2.5h | Key metrics trend from filing data. Reuses existing chart patterns |
| Router integration | 0.5h | 1h | Add to navbar or embed as tab in business_card.py (requires D24 first) |
| Testing & edge cases | 1h | 2h | Missing sections, very long filings, mobile layout |
| **Total** | **17h** | **28.5h** | **Midpoint: 23h** |

### Complexity: **High**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **No FinMind API for TW annual reports** | **High** | **Feature cannot proceed without data source** | **Must resolve before committing to this feature.** Options: (a) MOPS web scraping (legal gray area, fragile), (b) manual curation for top 20 stocks (high effort, limited scale), (c) use FinMind financial statements as proxy (available now, less rich than full annual reports) |
| Filing format inconsistency | High | Parser breaks on unexpected formats | Start with a single format (e.g., PDF-to-text from MOPS). Build parser for one format only. Add format detection later |
| Explanation quality for complex financial sections | Medium | Explanations are too generic or inaccurate | Use template-based approach (like news_summarizer) with section-specific templates. Limit scope to 5-8 common sections |
| Performance: large filing text processing | Medium | Slow page load | Pre-process filings into structured JSON. Cache parsed results. Don't parse on every page load |
| Chinese NLP complexity | Medium | Section splitting errors on Chinese text | Use keyword-based section detection (regex on section headers). Don't attempt NLP — too complex for MVP |

### Dependencies
- **Hard**: Data source for TW annual reports. **This is a blocker until resolved.**
- **Hard**: D24 (business_card.py extraction) if embedding as a tab in business_card.py
- **Soft**: `adaptive_engine.py` — can reuse event detection for identifying significant filing changes
- **Soft**: `news_summarizer.py` — explanation generation follows same template pattern

### Recommended Approach
1. **Spike first (4-6h)**: Research and validate data source. Try FinMind's `taiwan_stock_financial_statement` as a proxy. If insufficient, evaluate MOPS scraping feasibility.
2. If using FinMind financial statements as proxy:
   - Create `src/services/filing_parser.py` — parse financial statement DataFrame into "filing sections" (revenue, costs, profit, cash flow, debt)
   - Create `src/services/filing_explainer.py` — template-based explanations for each section
   - Create `config/filing_sections.yaml` — section definitions and explanation templates
3. Create `src/pages/filing_explorer.py` — section sidebar + main content with expandable explanations
4. **Scope control**: Start with 5 sections (revenue, gross profit, operating profit, net profit, cash flow). Do NOT attempt full annual report parsing. Do NOT attempt PDF processing.
5. **Fallback**: If data source cannot be resolved, defer C65 and replace with "Financial Statement Narrator" using existing FinMind data — same concept, less rich data.

---

## C66: Risk Profile Quiz — Comprehensive Risk Assessment

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `risk_profile_quiz.yaml` content creation | 1.5h | 2.5h | 8-10 questions × (question, 3-4 options with scores, category). ~60 lines YAML |
| `risk_profile.py` service | 1.5h | 2.5h | Pure function: `calculate_risk_profile(answers) -> dict` with score ranges and profile labels. ~80 LOC |
| Quiz UI component | 1.5h | 2.5h | Multi-step quiz with progress bar. Reuses radio button pattern from existing code |
| Results display | 1h | 1.5h | Risk profile card with plain-language description and recommended content |
| Session state integration | 0.5h | 1h | Store profile in `st.session_state['risk_profile']` for homepage personalization |
| Integration point | 0.5h | 1h | Embed in C58 (Beginner Onboarding) or as standalone page. If standalone, add to router |
| Testing & edge cases | 0.5h | 1h | All answers same, partial completion, retake |
| **Total** | **7h** | **12h** | **Midpoint: 9.5h** |

### Complexity: **Low**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Risk profile labels feel arbitrary | Medium | Users don't trust the result | Use simple 3-tier system (Conservative / Balanced / Growth). Clear score ranges. Plain-language descriptions for each tier |
| Quiz abandonment (8-10 questions is long) | Medium | Users don't complete the quiz | Add progress bar. Allow "skip" for each question. Show intermediate results. Keep questions short and conversational |
| Recommendation engine complexity | Low | Personalized recommendations need content tagging | Start with simple mapping: Conservative → bond-heavy sectors, Growth → tech sectors. No ML needed. Content tagging can be added to existing YAML files |
| Session state loss | Low | Profile lost on refresh | Acceptable for MVP. If C58 includes user accounts later, persist to YAML |

### Dependencies
- **Hard**: None. All components exist.
- **Soft**: C58 (Beginner Onboarding) — C66 is designed to be embedded in C58. If C58 is Sprint 5, C66 should be Sprint 4 (ready for integration) or early Sprint 5.
- **Soft**: `risk_analyzer.py` — existing risk analysis can inform quiz question design and scoring thresholds

### Recommended Approach
1. Create `config/risk_profile_quiz.yaml` — 8 questions covering: time horizon (2), risk tolerance (2), financial goals (2), investment experience (2)
2. Create `src/services/risk_profile.py` — `calculate_risk_profile(answers) -> {tier: "conservative|balanced|growth", score: int, description: str, recommendations: [str]}`
3. Create quiz UI as a reusable component (function, not a page) — can be embedded in C58 or shown standalone
4. Results: 3 tiers with plain-language descriptions. "Conservative" → "You prefer steady growth over big swings." "Growth" → "You're comfortable with ups and downs for potentially higher returns."
5. **Scope control**: No user account persistence. No detailed portfolio recommendations. 8 questions, 3 tiers, simple content mapping.
6. **Integration**: Design as a function `render_risk_quiz()` that C58 can call. Don't create a separate page unless C58 is deferred.

---

## C67: Community Sentiment — Social Proof Indicator

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `community_sentiment.py` service | 3h | 4h | Track page views, watchlist additions. Pure functions: `record_view(stock_id)`, `get_sentiment(stock_id) -> dict`. ~120 LOC |
| `community_data.yaml` storage | 1.5h | 2h | YAML-based storage for aggregate counts (views, watchlist adds). File-lock pattern from watchlist.py |
| Sentiment UI component | 2h | 3h | "X views this week", "Y% added to watchlist". Lightweight card component |
| Emoji reaction system (optional) | 1.5h | 2.5h | 😊🤔😮 reactions. Session state for "user reacted" tracking. Adds complexity |
| Integration: business_card.py | 1h | 1.5h | Add sentiment section to business card. Requires D24 if business_card.py > 600 LOC |
| "Most viewed" leaderboard | 1h | 1.5h | Simple sorted list. Can be a sidebar widget or section |
| Privacy considerations | 0.5h | 1h | Aggregate only, no individual data. Document in code comments |
| Testing & edge cases | 0.5h | 1h | First view, concurrent writes (file lock), empty data |
| **Total** | **11h** | **16.5h** | **Midpoint: 14h** |

### Complexity: **Medium**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| File lock contention with watchlist.yaml | Medium | Slow page loads or write failures | Use separate `community_data.yaml` file with its own lock. Don't share with watchlist |
| Data staleness | Low | Sentiment numbers don't update in real-time | Acceptable — this is aggregate data, not real-time. Update on page load (write) and read from cache |
| Privacy concerns with tracking | Medium | Users uncomfortable with view tracking | Aggregate only. No individual user tracking. Document clearly. Make it opt-out via session state |
| Concurrent write corruption | Low | YAML file corruption with multiple users | FileLock pattern from watchlist.py handles this. Tested pattern |
| Low traffic = low numbers | High | Single-user dev environment shows "1 view" | Seed with minimum display threshold ("Be the one of the first to view this stock"). Acceptable for MVP |

### Dependencies
- **Hard**: None for basic metrics (views, watchlist adds)
- **Hard**: D24 (business_card.py extraction) if adding sentiment to business_card.py and file > 600 LOC
- **Soft**: `watchlist.py` — reuses file-lock pattern and watchlist data for "added to watchlist" metric
- **Soft**: C53 (Social Sharing) — if both land in same sprint, share community data infrastructure

### Recommended Approach
1. Create `src/services/community_sentiment.py` — `record_view(stock_id)`, `get_sentiment(stock_id) -> {views_week, watchlist_count, reaction_counts}`
2. Create `config/community_data.yaml` — aggregate counts per stock. File-lock pattern from watchlist.py
3. Add view tracking call in `_router_base.py` `get_stock_data()` — fires on every stock page load
4. Create lightweight sentiment card component — "👀 X 人本週查看 | ⭐ Y 人加入關注"
5. Add to business_card.py (after D24 extraction) or as a sidebar widget
6. **Scope control**: Start with view count + watchlist percentage only. Emoji reactions are v2. "Most viewed" leaderboard is v2.
7. **Privacy**: Aggregate only. No user-level tracking. Document in code.

---

## C68: Weekly Market Digest — Curated Weekly Summary

### Refined Estimate

| Sub-task | Low (h) | High (h) | Notes |
|----------|---------|----------|-------|
| `weekly_digest.py` service | 2.5h | 4h | Aggregate weekly market data: index performance, sector performance, notable stocks. Pure function: `generate_digest() -> dict`. ~150 LOC |
| `digest_template.yaml` content | 1h | 2h | Section templates, tone guidelines, linking rules |
| Digest generation logic | 2h | 3h | Compute weekly changes, identify top/bottom sectors, notable events. Uses `adaptive_engine.py` for event data |
| New page: `weekly_digest.py` | 2h | 3h | Digest layout: market summary → sector performance → notable stories → links. Follows `event_dashboard.py` pattern |
| Chart: weekly market overview | 1h | 2h | Weekly index chart + sector bar chart. Reuses existing chart functions |
| Router integration | 0.5h | 1h | Add to navbar |
| Testing & edge cases | 0.5h | 1h | Holiday weeks, missing data, first digest |
| **Total** | **9.5h** | **16h** | **Midpoint: 13h** |

### Complexity: **Low-Medium**

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data availability for "weekly" computation | Medium | FinMind daily price data may have gaps | Use last 5 trading days. Handle missing dates gracefully. Show "data unavailable" for specific metrics |
| Content feels repetitive week-over-week | Medium | Users stop reading | Vary the focus: one week emphasize sectors, next week emphasize events. Use `adaptive_engine.py` event data to highlight what actually happened |
| Auto-generation quality | Medium | Generated text feels robotic | Use template-based generation (like news_summarizer) with multiple template variants. Rotate templates |
| Overlap with C49 (Daily Market Pulse) | High | Two market update features confuse users | **C68 should complement C49, not replace it.** C68 is a curated weekly narrative; C49 is daily data snapshots. Different purposes. If C49 is deferred, C68 can absorb its scope |

### Dependencies
- **Hard**: None for basic digest. All data available from existing FinMind client.
- **Soft**: `adaptive_engine.py` — event detection for "notable stories" section
- **Soft**: `news_summarizer.py` — news summarization for digest content
- **Soft**: C49 (Daily Market Pulse) — if C49 lands first, C68 can aggregate daily content into weekly digest. If C68 lands first, it stands alone.
- **Soft**: C51 (Sector Heatmap) — sector performance data for weekly digest

### Recommended Approach
1. Create `src/services/weekly_digest.py` — `generate_digest() -> {week_ending, index_change, top_sectors, bottom_sectors, notable_events, story_links}`
2. Create `config/digest_template.yaml` — section templates with tone guidelines (historian voice, past-tense, factual)
3. Create `src/pages/weekly_digest.py` — digest page with: market summary card → sector performance chart → notable events section → links to relevant stock pages
4. Use `adaptive_engine.py` `get_all_recent_events()` for notable events
5. Use `finmind_client.get_daily_price()` for TWSE index weekly performance
6. **Scope control**: Manual curation is NOT required — fully auto-generated from existing data. No email/push notification (v2). No personalization (v2).
7. **Overlap management**: If C49 exists, add "This Week's Daily Highlights" section linking to C49 pages. If C49 doesn't exist, C68 is the sole market update feature.

---

## Consolidated Effort Table

| ID | Feature | Low (h) | High (h) | Midpoint (h) | Complexity | Confidence |
|----|---------|---------|----------|-------------|------------|------------|
| C63 | Sector Stories | 11 | 17 | 14 | Medium | High |
| C64 | Daily Market Quiz | 9 | 15 | 12 | Low-Medium | High |
| C65 | Company Filing Explorer | 17 | 28.5 | 23 | High | Low-Medium |
| C66 | Risk Profile Quiz | 7 | 12 | 9.5 | Low | High |
| C67 | Community Sentiment | 11 | 16.5 | 14 | Medium | Medium |
| C68 | Weekly Market Digest | 9.5 | 16 | 13 | Low-Medium | High |
| **Total** | | **64.5** | **105** | **85.5** | | |

---

## Recommended Sprint Placement

### Sprint 4 (Current Plan: R3 → D24 → C44 → C51 → C48 → C53-1)
**Add to Sprint 4**: C66 (Risk Profile Quiz) — 7-12h
- Lowest complexity, no dependencies, directly enhances C58
- Can be developed in parallel with C51/C48 as a small task

### Sprint 5 (Current Plan: C58 + C62 + C56 + C60)
**Add to Sprint 5**: C64 (Daily Market Quiz) — 9-15h
- Low complexity, no dependencies
- Complements C60 (Concept Mastery Badges) — quiz completion feeds badge progress
- Content creation (30 questions) can start in Sprint 4 as parallel workstream

### Sprint 6 (Current Plan: C57 + C55 + C61)
**Add to Sprint 6**: C63 (Sector Stories) — 11-17h + C68 (Weekly Market Digest) — 9.5-16h
- Combined: 20.5-33h, fits within sprint capacity
- C68 can leverage C51's sector data (from Sprint 4)
- Content creation for both can start in Sprint 5

### Sprint 7+ (Current Plan: C59)
**Add to Sprint 7**: C67 (Community Sentiment) — 11-16.5h
- Depends on D24 (business_card.py extraction)
- More valuable after other features have driven traffic

### Deferred: C65 (Company Filing Explorer) — 17-28.5h
- **Blocked on data source resolution** (no FinMind API for annual reports)
- Requires spike/prototype first (4-6h)
- If data source resolved, place in Sprint 7 alongside C67
- If data source not resolved, replace with "Financial Statement Narrator" using existing FinMind data (reduces to 12-18h)

---

## Risk Register (C63-C68)

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| C65 data source (annual reports) not available | High | Feature cannot proceed | Spike first. Fallback to FinMind financial statements as proxy |
| C64 content creation (30 quiz questions) exceeds estimate | Medium | Feature launches with fewer questions | Start with 15 questions (2 weeks). Content creation is parallel workstream, not blocking |
| C67 file lock contention with watchlist | Medium | Slow page loads | Separate YAML file with own lock. Tested pattern from watchlist.py |
| C63 sector content quality uneven | Medium | Users see generic text | Start with 5 high-quality sectors. Expand based on usage data |
| C68 overlaps with C49 (Daily Market Pulse) | High | Two market update features confuse users | Position C68 as curated weekly narrative vs C49's daily data snapshots. Complementary, not competing |
| Session state bloat from C64 + C66 + C67 | Medium | Performance degradation, key collisions | Namespace all keys (e.g., `quiz_streak`, `risk_profile`, `sentiment_view`). Audit in Sprint 5 (D25) |
| C66 risk profile labels feel arbitrary | Medium | Users don't trust results | Use simple 3-tier system with clear thresholds. Plain-language descriptions. |

---

## Key Recommendations

1. **C66 first** — Lowest effort (7-12h), no dependencies, directly enhances C58. Add to Sprint 4.

2. **C64 second** — Low effort (9-15h), no dependencies, drives daily engagement. Add to Sprint 5. Start content creation in Sprint 4.

3. **C65 requires a spike** — Highest effort (17-28.5h) AND highest risk (data source unknown). Do a 4-6h spike in Sprint 4 to validate data source before committing to full implementation.

4. **C63 + C68 together** — Both are content-driven features that benefit from shared content creation. Place in Sprint 6 with content creation starting Sprint 5.

5. **C67 after D24** — Community sentiment needs D24 (business_card.py extraction) if embedding in business card. Place in Sprint 7.

6. **Content creation is the bottleneck** — C63 (10 sectors), C64 (30 questions), and C68 (templates) all require significant content creation. Start content creation as a parallel workstream in Sprint 4, separate from engineering effort.

7. **Session state audit (D25) before C67** — C64, C66, and C67 all add session state keys. Audit in Sprint 5 (as planned) before adding C67 in Sprint 7.

---

*Created: 2026-06-12*
*Role: Developer*
*Review cycle: Round 13*
*Confidence level: High for C63, C64, C66, C68. Medium for C67. Low-Medium for C65 (data source risk).*
