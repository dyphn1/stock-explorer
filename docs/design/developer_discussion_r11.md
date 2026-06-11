# Developer Estimates — Discussion Round 11

## 2026-06-18 Developer Estimates — Round 11 (New Feature Cost & Risk)

---

## Context: Current Codebase State

Sprint 2 shipped C37, C39, C43, C45 — all folded into existing files (primarily `analogy_engine.py` and `chart.py`), **no new service modules were created**. Sprint 3 is in progress with C44, C41, C38, R1, D16.

Key facts for estimation:
- **analogy_engine.py is 857 lines** — god module with 6 responsibilities (D16). Any feature importing from it pulls in 857 lines when it needs ~200.
- **No test infrastructure** — every new feature adds regression risk with no safety net.
- **Inline HTML duplication (D3)** — pages use raw HTML strings instead of reusable components.
- **EPS extraction triplicated (D17)** — same logic in 3 files.
- **All data loading uses ThreadPoolExecutor** pattern from `_router_base.py` — proven but only for single-stock data.
- **FinMindClient** wraps 11 endpoints, all stock-specific. No market-level endpoints wrapped yet.

---

## Feature-by-Feature Estimates

### C48: Company Story Card (30-sec visual summary)

**My estimate: 10-14h** (original: 8-12h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| `story_composer.py` service module — compose story from existing data sources | 2-3h | Pure composition, no new data. Assembles: one-liner + 3 key metrics + mini sparkline + narrative |
| UI rendering in `business_card.py` — visual card with metrics + chart + narrative | 3-4h | Must follow PPT-style design (orange/amber hero card). Needs responsive layout (3-col → 1-col) |
| Replace/merge with existing C37 Key Takeaways | 1-2h | Designer says C48 replaces C37. Need to remove or merge C37's `generate_key_takeaways()` call |
| Curated story elements data — migrate `_KEY_TAKEAWAYS` from Python dict to YAML | 1-2h | Part of R5. If R5 not done yet, this is a dependency |
| Mini sparkline chart — new Plotly figure function in `chart.py` | 1-2h | Small revenue trend line. Reuse `_apply_theme_layout()` pattern |
| L0 + L1 verification | 0.5h | |
| Polish: loading states, empty states, mobile layout | 0.5-1h | |

**Technical risks**:
- **Redundancy with C37**: C48 replaces C37 per designer. If we keep both, the page gets 14 sections. Must coordinate with designer on replacement vs. merge. Risk: **MEDIUM**.
- **D16 dependency**: C48 imports from `analogy_engine.py` (857 lines). The D16 split should happen first or alongside. Risk: **MEDIUM** — not a blocker, but working in an unstable module adds friction.
- **business_card.py is already 481 lines**: Adding C48's rendering code here pushes it past 550 lines. Consider extracting business card sections into a `src/pages/business_card/` directory. Risk: **LOW** — awareness only.

**Dependencies**: D16 (split analogy_engine) — should do first. R5 (YAML migration) — for curated story elements.

---

### C49: Daily Market Pulse (automated market summary)

**My estimate: 14-20h** (original: 10-14h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| New `market_data.py` service — batch-fetch market-wide data | 3-4h | **NEW infrastructure**. FinMind API has market-level endpoints (Taiwan stock market daily, index prices) but `FinMindClient` doesn't wrap them. Need to add `get_market_daily()`, `get_index_prices()` to client |
| Data aggregation logic — compute market-wide metrics from raw data | 2-3h | Market summary, top movers (gainers/losers), sector performance, key events |
| New page `market_pulse_page.py` — full page with hero + indices + movers + sector + events | 4-5h | 5 "slides" per designer spec. Each section needs its own rendering function |
| Sidebar nav integration — add "📰 市場日報" entry | 0.5h | |
| Plain-language explanations — integrate with `analogy_engine.py` for market commentary | 2-3h | "TAIEX rose 1.2% → 因為台積電財報優於預期" style. Template-based, no LLM needed |
| Caching strategy — market data refreshes daily, not on every interaction | 1-2h | Use `st.session_state` with TTL or `@st.cache_data(ttl=3600)` |
| L0 + L1 verification | 0.5h | |
| Polish: loading states, "last updated" timestamp, mobile layout | 1-2h | |

**Technical risks**:
- **No market-level data pipeline**: This is the **first feature** that needs cross-stock aggregation. The current architecture is built around `stock_id → data dict`. C49 needs `market → aggregate metrics`. This is a new data flow path. Risk: **HIGH**.
- **FinMind API market endpoints untested**: The `FinMindClient` has 11 stock-specific endpoints. Market-level endpoints (e.g., `TaiwanStockMarketDaily`, `TaiwanStockIndexPrice`) need to be tested for data format, rate limits, and caching behavior. Risk: **MEDIUM**.
- **"Daily" scheduling**: Streamlit can't push updates. Need `st.cache_data(ttl=3600)` or `st.fragment` with timer. Not a blocker but adds complexity. Risk: **LOW**.
- **Content freshness**: Market data is only useful if fresh. Need clear "last updated" timestamp and possibly a manual refresh button. Risk: **LOW**.

**Dependencies**: R3 (batch API calls) — **HARD BLOCKER**. Without batch API, fetching data for 1,800 stocks + indices will take 30-60s. Also depends on `FinMindClient` extension for market-level endpoints.

**Shared infrastructure with C51**: C49 and C51 share the same `market_data.py` service. Build once, serve both.

---

### C50: Learning Progress Tracker (concept mastery)

**My estimate: 16-24h** (original: 12-16h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| Concept taxonomy definition — define 10-15 financial concepts with mastery criteria | 2-3h | Content work, not pure engineering. Need to define: concept name, description, associated pages/stocks, mastery threshold |
| Progress storage system — persistent per-user progress tracking | 4-6h | **MAJOR INFRASTRUCTURE GAP**. `session_state` resets on server restart. `watchlist.yaml` is user-agnostic. Need a new persistence mechanism (per-user YAML files, or SQLite, or JSON files in `data/users/`) |
| Progress tracking UI — progress bar, concept grid, achievement badges | 3-4h | `st.progress()` + per-concept status. Simple rendering, complex state management |
| Integration with C52 Quiz — quiz results feed into progress tracker | 2-3h | Without C50, quiz scores are ephemeral. Without C52, progress has no input. These two are tightly coupled |
| Mastery logic — spaced repetition or threshold-based mastery | 2-3h | Simple: "visit page + pass quiz = mastered". Complex: spaced repetition (Anki-style). Start simple |
| New page `progress_page.py` | 1-2h | |
| L0 + L1 verification | 0.5h | |
| Polish | 1-2h | |

**Technical risks**:
- **No persistence layer (D22)**: This is the **hardest technical blocker** of all 7 features. Streamlit's `session_state` is ephemeral. `watchlist.yaml` is shared across all users (no user identity). Building a per-user persistence system is a **platform-level change**. Risk: **CRITICAL**.
- **No user identity**: Without login/user accounts, "per-user progress" is meaningless. All users share the same progress data. Risk: **HIGH**.
- **Scope creep**: A full mastery system (spaced repetition, difficulty levels, adaptive scheduling) is a research project, not a feature. Must scope to "track which pages user visited + quiz scores". Risk: **MEDIUM**.

**Dependencies**: D22 (persistence layer) — **HARD BLOCKER**. C52 (Quiz Mode) — soft dependency (can build C50 without C52, but it's not useful).

**Recommendation**: **Defer to Sprint 5+**. This feature requires infrastructure that doesn't exist and shouldn't be built lightly. A lightweight "pages visited" tracker using `session_state` is possible in 4-6h but provides minimal value.

---

### C51: Sector Heatmap (visual market overview)

**My estimate: 12-16h** (original: 8-12h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| New `market_data.py` service — shared with C49 | 3-4h | Same `market_data.py` as C49. Batch-fetch per-stock data, aggregate by sector |
| Sector classification mapping — `src/data/sector_mapping.yaml` | 1-2h | Current `category_browser.py` has sector groupings but they're not standard. Need to define ~20 sectors with stock lists |
| Heatmap chart — Plotly `px.imshow` or `go.Heatmap` with color-coded cells | 2-3h | Grid-based heatmap. Each cell = sector, color = change %, size = market cap |
| Top/bottom sectors — card-based display with plain-language explanation | 1-2h | Reuse `_info_card()` / `_白话_card()` pattern |
| New page `sector_heatmap_page.py` | 1-2h | |
| Sidebar nav integration | 0.5h | |
| Batch API optimization — depends on R3 | 1-2h | Without R3, fetching 1,800 stocks sequentially takes 30-60s. With R3 ThreadPoolExecutor, ~5-10s |
| L0 + L1 verification | 0.5h | |
| Polish: loading states, mobile responsive grid, click-to-navigate | 1-2h | |

**Technical risks**:
- **R3 dependency**: Without batch API calls, the heatmap will be **unusably slow** (30-60s load time). R3 is a **HARD BLOCKER**. Risk: **HIGH**.
- **Sector classification accuracy**: The current sector data from FinMind may not map cleanly to standard Taiwan stock sectors. Need manual curation in `sector_mapping.yaml`. Risk: **MEDIUM**.
- **Data completeness**: Not all 1,800 stocks have sector classifications. Some may be missing or misclassified. Risk: **LOW** — graceful degradation (show only classified stocks).
- **Plotly heatmap on mobile**: Small screens with 15+ sector cells need careful sizing. Risk: **LOW** — responsive grid (4-col → 3-col → 2-col).

**Dependencies**: R3 (batch API calls) — **HARD BLOCKER**. D6 (hardcoded data) — sector mapping should go in YAML.

**Shared infrastructure with C49**: Build `market_data.py` once, serve both C49 and C51.

---

### C52: Quiz Mode (interactive assessment)

**My estimate: 12-18h engineering + 10-15h content creation** (original: 10-14h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| Quiz question bank — `src/data/quiz_questions.yaml` with 50-100 questions | 10-15h | **CONTENT CREATION, not engineering**. Each question needs: question text (≤80 chars), 4 options, correct answer, explanation, concept tag, difficulty level. This is the real cost |
| Quiz state machine — `st.session_state` management for quiz flow | 2-3h | Current question, selected answer, submitted state, score, review mode |
| Quiz rendering UI — `st.radio()` for options, submit button, result feedback | 2-3h | Green success card / orange tip card per designer spec |
| Quiz scoring + review — score tracking, wrong answer review, retry | 1-2h | |
| New page `quiz_page.py` or integration into C47 Academy | 1-2h | |
| Dynamic question generation (Phase 2, optional) | 3-5h | Generate questions from real stock data. "What was TSMC's revenue in 2024?" — requires data lookup + question template |
| L0 + L1 verification | 0.5h | |
| Polish | 1-2h | |

**Technical risks**:
- **Content creation bottleneck**: 50-100 questions × 15 min each = 12-25h of content work. This is the **dominant cost**, not the engineering. Risk: **HIGH** — content creation will bottleneck the feature.
- **No persistence**: Quiz scores reset on session end. Without C50 (progress tracker), quiz results are ephemeral. Risk: **MEDIUM** — acceptable for MVP.
- **Question quality**: Bad questions (too easy, too hard, ambiguous) will make the feature feel useless. Need review/iteration. Risk: **MEDIUM**.
- **Dynamic question generation complexity**: Generating valid questions from real data is harder than it looks. Need to ensure questions are answerable from the data, options are plausible, and difficulty is appropriate. Risk: **MEDIUM** — defer to Phase 2.

**Dependencies**: D6 (hardcoded data) — questions must go in YAML. C50 (progress tracker) — soft dependency for persistent scores.

---

### C53: Social Sharing (shareable analysis cards)

**My estimate: 8-12h** (original: 6-10h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| Shareable card rendering — generate a 1200x630px image with company data | 3-4h | **HTML-to-image is the hardest part**. Options: (a) Pillow to draw card from scratch, (b) `plotly.io.write_image()` for charts + Pillow for layout, (c) `imgkit`/`playwright` for HTML-to-image. Option (a) is most reliable but most work |
| URL-based sharing — encode current view in URL params | 1-2h | Existing `url_sync.py` already does this. Mostly wiring, not new code |
| Share button UI — `📤 分享` button in business card header | 0.5-1h | Small UI element |
| Preview modal — show generated card image with download/copy options | 1-2h | `st.modal()` or `st.dialog()` for preview |
| OG meta tags — for proper link previews on social media | 1-2h | `st.set_page_config()` + custom HTML head injection. Streamlit's support is limited |
| L0 + L1 verification | 0.5h | |
| Polish: loading states, error handling for image generation failures | 1-2h | |

**Technical risks**:
- **HTML-to-image fragility**: This is the **#1 risk**. Streamlit doesn't support image export natively. Options analysis:
  - **Pillow**: Most reliable, but drawing a styled card from scratch is ~200 lines of Pillow code.
  - **imgkit** (wkhtmltopdf wrapper): External dependency, may not work in all environments.
  - **Playwright**: Heavy dependency, slow startup.
  - **st.markdown screenshot**: Not natively supported.
  Risk: **HIGH**.
- **OG meta tags in Streamlit**: Streamlit's `st.set_page_config()` supports limited meta tags. Full OG tags (og:image, og:description) require custom HTML injection via `st.markdown(..., unsafe_allow_html=True)` in the `<head>`. This is fragile. Risk: **MEDIUM**.
- **Scope creep**: "Sharing" can mean URL (easy), image (medium), social media integration (hard), or a full social feed (very hard). Must scope to URL + image. Risk: **MEDIUM**.

**Dependencies**: D3 (inline HTML) — shareable card should use standardized UI components from R9, not inline HTML.

**Recommendation**: Implement in phases — Phase 1: URL sharing only (2-3h). Phase 2: image generation (5-9h). Phase 3: OG tags (1-2h).

---

### C54: Video/Audio Explanation

**My estimate: 30-45h** (original: 20-30h — revised upward)

| Task | Hours | Notes |
|------|-------|-------|
| LLM integration for script generation — `src/services/llm/` abstraction (R7) | 3-5h | **HARD BLOCKER**. No LLM integration exists. Need to define `ExplanationProvider` protocol + `LLMExplanationProvider` implementation |
| TTS pipeline — text-to-speech for audio explanations | 4-6h | Options: OpenAI TTS ($0.015/1K chars), Google Cloud TTS, or local (pyttsx3). Each has trade-offs in quality, cost, and setup |
| Script template system — structured explanation scripts from data | 2-3h | Even with LLM, need fallback templates. This part can be done without LLM |
| Audio rendering — generate MP3 files from scripts | 2-3h | Server-side audio file generation, storage, and delivery |
| Video rendering — generate MP4 with visual + audio | 6-10h | **MOST EXPENSIVE TASK**. Requires: visual slides (Pillow/Plotly) + audio track + video composition (moviepy or ffmpeg). This is a full media pipeline |
| Media hosting/delivery — serve generated files to users | 2-4h | Streamlit can serve static files, but generated media needs caching and cleanup |
| UI integration — media player in business card page | 1-2h | `st.audio()` and `st.video()` exist in Streamlit |
| L0 + L1 verification | 0.5h | |
| Polish: loading states, progress indicators, error handling | 2-3h | |

**Technical risks**:
- **No LLM integration (D5)**: **HARD BLOCKER**. The entire feature depends on LLM for script generation. Without R7 (LLM abstraction), this can't start. Risk: **CRITICAL**.
- **No media pipeline**: No TTS, no video rendering, no media hosting. Building this from scratch is a **platform-level effort**. Risk: **CRITICAL**.
- **Ongoing cost**: TTS API calls cost money. At scale (1000 users/day × 500 chars = 500K chars/day), that's $7.50/day or $225/month. Risk: **MEDIUM** — need cost monitoring.
- **Complexity underestimated**: 20-30h is for a **bare-bones prototype** with template-based scripts (no LLM) and audio only (no video). Production-quality with LLM + video is 45-60h. Risk: **HIGH**.

**Dependencies**: R7 (LLM abstraction) — **HARD BLOCKER**. D5 (no LLM integration) — **HARD BLOCKER**.

**Recommendation**: **Defer to Sprint 5+**. This is a platform transformation feature, not an incremental addition. Revisit after LLM architecture (D5/R7) is resolved.

---

## Feature Clustering & Shared Infrastructure

| Shared Infrastructure | Features | New Module | Building This First Serves |
|----------------------|----------|------------|---------------------------|
| **Market-level data aggregation** | C49 (Market Pulse), C51 (Sector Heatmap) | `src/services/market_data.py` | Build once, both features use it |
| **YAML content banks** | C52 (Quiz), C48 (Story Card curated elements) | `src/data/quiz_questions.yaml`, `src/data/story_elements.yaml` | Content creation is the bottleneck, not the YAML format |
| **Export/render pipeline** | C53 (Social Sharing), C48 (Story Card as image) | `src/services/export_service.py` | Both need "render a card as shareable content" |
| **LLM integration** | C54 (Video/Audio), C48 (AI-enhanced story) | `src/services/llm/` (from R7) | Long-term dependency for multiple features |

**Key insight**: C49 + C51 are the strongest pair. They share `market_data.py` and together provide the "market-level view" that the current app lacks. C48 + C53 share the "render a card" pipeline. C50 + C52 are the education pair but both have infrastructure blockers.

---

## Recommended Implementation Order

### Sprint 3 (current, remaining capacity ~20-25h)

**Already in progress**: C44, C41, C38, R1, D16

**Recommendation**: Do NOT add any C48-C54 features to Sprint 3. Sprint 3 is already full with C44, C41, C38, and the critical R1/D16 refactoring. Adding new features would delay architecture debt resolution.

### Sprint 4 (~40h capacity)

| Priority | Feature | Est. Hours | Rationale |
|----------|---------|------------|-----------|
| 1 | **C51: Sector Heatmap** | 12-16h | Highest impact new feature. Introduces market-level data flow. Depends on R3 (batch API) — do R3 first or alongside. |
| 2 | **C48: Company Story Card** | 10-14h | Composition of existing features. Low risk, high polish. Depends on D16 (split analogy_engine) — should be done in Sprint 3. |
| 3 | **C53: Social Sharing (Phase 1: URL only)** | 2-3h | Lowest effort. Leverages existing `url_sync.py`. Can be done in 2-3h as a quick win. |

**Sprint 4 total**: 24-33h (fits within ~40h capacity with buffer for bug fixes and R3 if not done)

**Prerequisites for Sprint 4**:
- R3 (batch API calls) — must be done before C51. If not done in Sprint 3, it's the first task in Sprint 4.
- D16 (split analogy_engine) — must be done before C48. Should be done in Sprint 3.

### Sprint 5 (~40h capacity)

| Priority | Feature | Est. Hours | Rationale |
|----------|---------|------------|-----------|
| 4 | **C49: Daily Market Pulse** | 14-20h | Shares `market_data.py` with C51 (already built). Adds scheduling complexity. |
| 5 | **C52: Quiz Mode (MVP)** | 12-18h + 10-15h content | Content creation is the bottleneck. Start with 20 questions, expand over time. |
| 6 | **C53: Social Sharing (Phase 2: image)** | 5-9h | Depends on HTML-to-image pipeline. Can be done alongside C52. |

**Sprint 5 total**: 26-47h + content creation (tight but doable if C52 is scoped to 20 questions)

### Sprint 5+ (deferred)

| Feature | Est. Hours | Blocker |
|---------|------------|---------|
| **C50: Learning Progress Tracker** | 16-24h | D22 (persistence layer) — requires user accounts or per-user storage |
| **C54: Video/Audio Explanation** | 30-45h | D5 (no LLM integration) + TTS pipeline + media hosting |

---

## Dependency Graph

```
Sprint 3 (in progress):
  R1 (financial_metrics) ──→ C38, C44
  D16 (split analogy_engine) ──→ C48, C51, C49
  R3 (batch API calls) ──→ C51, C49

Sprint 4 prerequisites:
  R3 ──→ C51 (Sector Heatmap)
  D16 ──→ C48 (Story Card)

Sprint 4:
  C51 ──→ market_data.py (shared with C49)
  C48 ──→ story_composer.py + export_service.py (shared with C53)
  C53 (Phase 1) ──→ url_sync.py (already exists)

Sprint 5:
  market_data.py (from C51) ──→ C49 (Market Pulse)
  C52 (Quiz) ──→ quiz_questions.yaml
  C53 (Phase 2) ──→ export_service.py (from C48)

Sprint 5+ (deferred):
  R7 (LLM abstraction) ──→ C54 (Video/Audio)
  D22 (persistence layer) ──→ C50 (Learning Progress)
  C52 (Quiz) ──→ C50 (Progress needs quiz scores)
```

---

## Summary Table

| Feature | Revised Estimate | Original Estimate | Risk Level | Sprint | Key Blocker |
|---------|-----------------|-------------------|------------|--------|-------------|
| C48: Story Card | 10-14h | 8-12h | MEDIUM | Sprint 4 | D16 (split analogy_engine) |
| C49: Market Pulse | 14-20h | 10-14h | HIGH | Sprint 5 | R3 (batch API) + no market-level data pipeline |
| C50: Progress Tracker | 16-24h | 12-16h | CRITICAL | Sprint 5+ | D22 (persistence layer) + no user identity |
| C51: Sector Heatmap | 12-16h | 8-12h | HIGH | Sprint 4 | R3 (batch API) |
| C52: Quiz Mode | 12-18h + 10-15h content | 10-14h | MEDIUM | Sprint 5 | Content creation bottleneck |
| C53: Social Sharing | 8-12h | 6-10h | MEDIUM | Sprint 4 (Phase 1: 2-3h) | HTML-to-image fragility |
| C54: Video/Audio | 30-45h | 20-30h | CRITICAL | Sprint 5+ | D5 (no LLM) + no TTS pipeline |

**Total engineering hours**: 102-159h (2.5-4 sprints at 40h/sprint)
**Total content creation**: 10-25h (quiz questions, story elements)

---

## Key Developer Concerns

1. **R3 (batch API calls) is the most critical enabler** — it unblocks C51 and C49, the two highest-impact features. If R3 is delayed, Sprint 4's most valuable features are blocked.

2. **Content creation is underestimated** — C52's quiz questions (10-15h) and C48's story elements (part of R5) are pure content work that doesn't show up in engineering estimates. These need dedicated time.

3. **C50 and C54 are not just "hard" — they're different categories** — they require new infrastructure (persistence layer, LLM integration, TTS pipeline) that changes the product's technical foundation. They should be planned as separate technical initiatives, not sprint features.

4. **The business card page is at capacity** — C48 is the only new feature that adds to the business card page (replacing C37). All other features are new pages. This is good — page overload is avoided.

5. **No test infrastructure means every feature adds regression risk** — with 0 tests and 31 .py files, every new feature increases the surface area for bugs. Consider adding basic L0/L1 tests for new service modules as part of each feature's scope (already included in estimates).

---

*Created: 2026-06-18*
*Maintainer: Developer*
*Next review: After Sprint 4 planning*
