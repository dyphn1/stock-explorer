# Architect Discussion — Round 11: New Feature Feasibility (C48–C54)

## 2026-06-18 Technical Analysis — Round 11 New Feature Feasibility

### Context

Sprint 2 complete (C37, C39, C43, C45 shipped). Sprint 3 in progress (C44, C41, C38, R1, D16).
Round 11 competitor research identified 7 new features (C48–C54) inspired by competitor analysis.
This document assesses each for technical feasibility, architecture fit, and proposes 2–3 strategic directions.

---

### Feasibility Assessment per Feature

#### C48: Company Story Card (30-sec visual summary) — Est. 8–12h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ **High** |
| **Dependencies** | `analogy_engine.py` (one-liners, analogies), `company_facts.py`, `chart.py` (existing charts), `_info_card()` / `_白话_card()` |
| **Architecture Fit** | Clean. This is a **presentation-layer composition** of existing data. No new data sources. The "story" is assembled from: one-liner + key takeaway + health snowflake + valuation band + revenue trend — all of which already exist. |
| **Risks** | — Feels redundant with the existing business card (C37/C39/C43/C45 already show much of this data). The value is in the **curation and layout**, not the data. Risk of "yet another card" fatigue. |
| **Architecture Debt Interaction** | D16 (god module): The story card would import from `analogy_engine.py` (857 lines) for ~200 lines of analogy functions. D18 (hardcoded takeaways): The curated story elements are in a 120-line Python dict. Both should be resolved first. |
| **Verdict** | **Feasible but needs positioning clarity.** The technical work is a new `story_composer.py` service + a section/tab in `business_card.py`. The real question is: what does the Story Card show that the existing business card doesn't? Answer: a **single-screen narrative** (one-liner → key metrics → health → what changed) without scrolling. |

#### C49: Daily Market Pulse (automated market summary) — Est. 10–14h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | 🟡 **Medium** |
| **Dependencies** | FinMind API (market-wide endpoints), new `market_pulse.py` service, new page or sidebar widget |
| **Architecture Fit** | Moderate. This is the first feature that requires **cross-stock aggregation** at the market level (not single-stock). The current architecture is built around a single stock_id → data dict pattern. Market pulse needs a different data flow: fetch market-wide data → aggregate → render. |
| **Risks** | — **Data source gap**: FinMind API has market-level endpoints (Taiwan stock market daily, index prices) but the `FinMindClient` wrapper currently only wraps stock-specific endpoints. Need to add market-level API methods. — **Scheduling**: "Daily" implies a cron or scheduled refresh. Streamlit's native re-render on every interaction doesn't support "push" updates. Would need `st.fragment` with `st.rerun()` timer or a simple "last updated" timestamp with manual refresh. — **Scope creep**: Could become a full dashboard. Must be scoped to 5–8 key metrics. |
| **Architecture Debt Interaction** | D7/D8 (sequential API calls): Market pulse would need to fetch data for multiple stocks/indices. Must use batch patterns from R3. |
| **Verdict** | **Feasible with scope control.** The core challenge is architectural: this is a **market-level view** in a **single-stock app**. It needs a new data flow path. Best implemented as a new `src/services/market_pulse.py` + a lightweight homepage/sidebar widget. |

#### C50: Learning Progress Tracker (concept mastery) — Est. 12–16h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | 🟡 **Medium** (conceptually) / 🔴 **Low** (with full spaced-repetition) |
| **Dependencies** | Persistent storage (beyond session_state), concept taxonomy, user interaction tracking |
| **Architecture Fit** | **Poor fit with current architecture.** This is a **user profile / persistence** feature. The current app has no user accounts, no database, no persistent state beyond `watchlist.yaml`. Learning progress requires: (1) a concept taxonomy, (2) per-user progress tracking, (3) spaced-repetition scheduling. |
| **Risks** | — **No persistence layer**: Streamlit's `session_state` resets on server restart. `watchlist.yaml` is the only persistent store and it's user-agnostic (shared file). — **No user identity**: No login, no user profiles. Progress tracking is meaningless without per-user data. — **Concept taxonomy**: Defining "concepts" and mapping them to stocks/pages requires significant content work. |
| **Architecture Debt Interaction** | This feature would require **new infrastructure** (D22: user persistence layer) that doesn't exist. |
| **Verdict** | **Not feasible in current architecture without a persistence layer.** A lightweight version (track which pages the user has visited using `session_state` + localStorage via `st.query_params` or `st.session_state`) is possible but not true "mastery tracking." Defer until user accounts or a persistence layer is established. |

#### C51: Sector Heatmap (visual market overview) — Est. 8–12h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ **High** |
| **Dependencies** | FinMind API (sector-level data or per-stock data aggregated by sector), `chart.py` (Plotly heatmap), `category_browser.py` (sector data partially exists) |
| **Architecture Fit** | Clean. This is a **chart + data aggregation** feature. Plotly supports heatmap natively (`px.imshow` or `go.Heatmap`). The data can be derived from the existing stock universe + sector classifications. |
| **Risks** | — **Data granularity**: FinMind provides per-stock data, not sector-level aggregates. Need to aggregate by sector in Python. For ~1,800 stocks × 20 sectors, this is manageable but requires batch API calls (D7/P1). — **Sector classification**: The current `category_browser.py` has sector groupings but they may not map cleanly to standard industry sectors. May need a `src/data/sector_mapping.yaml`. |
| **Architecture Debt Interaction** | D7 (N+1 API calls): Must batch-fetch data for heatmap. Depends on R3. D6 (hardcoded data): Sector mapping should go in YAML. |
| **Verdict** | **Feasible and high-impact.** This is the most visually compelling feature and aligns with the "visual-first" competitor insight. Best implemented as a new `sector_heatmap.py` service + new page or tab. Depends on R3 (batch API) for performance. |

#### C52: Quiz Mode (interactive assessment) — Est. 10–14h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | 🟡 **Medium** |
| **Dependencies** | Quiz question bank (YAML), `analogy_engine.py` (for answer explanations), `st.session_state` (for quiz state) |
| **Architecture Fit** | Moderate. Quiz is a **new interaction pattern** (Q&A → feedback → score) that doesn't fit the current "display data for one stock" pattern. It needs: (1) a question bank, (2) a quiz state machine, (3) a scoring/review system. |
| **Risks** | — **Question bank curation**: 50–100 questions needed for a minimal viable quiz. This is a significant content creation effort (10–15h just for content). — **No persistence**: Quiz scores reset on session end. Without user accounts, "progress" is ephemeral. — **Question types**: Multiple-choice is easiest. "Calculate PER from data" is harder (needs dynamic question generation from real data). |
| **Architecture Debt Interaction** | D6 (hardcoded data): Questions must go in YAML, not Python. |
| **Verdict** | **Feasible as a lightweight MVP.** A static question bank (YAML) + session-state quiz flow + simple scoring is achievable in 10h. The content creation effort is the real cost. Dynamic question generation (from real stock data) would be a Phase 2. |

#### C53: Social Sharing (shareable analysis cards) — Est. 6–10h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ **High** (basic) / 🟡 **Medium** (polished) |
| **Dependencies** | HTML-to-image export, URL parameter encoding (existing `url_sync.py`), `st.query_params` |
| **Architecture Fit** | Clean. The existing `url_sync.py` already encodes stock_id + tab in URL parameters. Sharing a "card" can be as simple as: (1) encode current view state in URL, (2) render a shareable summary from URL params. For image sharing, `plotly.io.write_image()` + HTML-to-image (e.g., `imgkit` or `playwright`) can generate a card image. |
| **Risks** | — **Image generation**: HTML-to-image in Streamlit is fragile. `plotly.io.write_image()` works for charts but not for HTML/CSS cards. May need `kaleido` (for Plotly) + `st.markdown` screenshot approach. — **Social meta tags**: For proper link previews (Twitter/X cards), need HTML meta tags. Streamlit supports this via `st.set_page_config()` + custom HTML head injection. — **Scope**: "Sharing" can mean URL sharing (easy), image sharing (medium), or social media integration (hard). |
| **Architecture Debt Interaction** | D3 (inline HTML): The shareable card HTML should use the standardized UI components from R9, not inline HTML. |
| **Verdict** | **Feasible as URL sharing + basic image export.** The 6–10h estimate is realistic for: URL-based sharing (existing infrastructure) + a "copy link" button + a simple card image export. Full social media integration (OG tags, Twitter cards) adds 4–6h. |

#### C54: Video/Audio Explanation — Est. 20–30h

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | 🔴 **Low** (for production) / 🟡 **Medium** (for prototype) |
| **Dependencies** | TTS/STT API, LLM for script generation, audio/video rendering pipeline |
| **Architecture Fit** | **Poor fit.** This is a **media generation** feature that requires: (1) LLM to generate explanation script, (2) TTS to generate audio, (3) visual rendering for video, (4) hosting/delivery of media files. None of this exists in the current architecture. |
| **Risks** | — **No LLM integration**: D5 (no LLM abstraction) is still open. C54 depends on LLM for script generation. — **No media pipeline**: No TTS, no video rendering, no media hosting. — **Cost**: TTS API calls (e.g., OpenAI TTS at $0.015/1K chars) would add ongoing cost. For a stock explanation (~500 chars), that's $0.0075/explanation. At 1000 daily users = $7.50/day. — **Complexity**: 20–30h is optimistic. A production-quality feature would need 40–60h. |
| **Architecture Debt Interaction** | D5 (no LLM abstraction) is a hard blocker. |
| **Verdict** | **Not recommended for near-term.** This is a platform-level feature that requires LLM integration (D5), TTS infrastructure, and media delivery. The 20–30h estimate is for a bare-bones prototype. Defer to Sprint 5+ and revisit after LLM architecture (D5/R7) is resolved. |

---

### Feature Clustering & Shared Infrastructure

Several features share infrastructure and should be planned together:

| Shared Infrastructure | Features | New Module Needed |
|----------------------|----------|-------------------|
| **Market-level data aggregation** | C49 (Market Pulse), C51 (Sector Heatmap) | `src/services/market_data.py` — batch-fetch market-wide data, aggregate by sector/index |
| **YAML content banks** | C52 (Quiz), C48 (Story Card curated elements) | `src/data/quiz_questions.yaml`, `src/data/story_elements.yaml` |
| **Export/render pipeline** | C53 (Social Sharing), C48 (Story Card as image) | `src/services/export_service.py` — HTML-to-image, URL generation |
| **LLM integration** | C54 (Video/Audio), C48 (Story Card with AI narrative) | `src/services/llm/` (from R7) |

**Key insight**: C49 + C51 share the same data pipeline (market-wide → aggregate → visualize). Building `market_data.py` once serves both. Similarly, C48 + C53 both need a "render a card as shareable content" pipeline.

---

### Proposed Feature Directions

#### Direction A: "Quick Wins + Visual Impact" (Recommended)

**Features**: C48 (Story Card) + C51 (Sector Heatmap) + C53 (Social Sharing)

**Rationale**:
- All three are **feasible with current architecture** (no new infrastructure needed beyond batch API calls).
- C51 (Sector Heatmap) is the highest-impact new feature — it's the only **market-level view** in a single-stock app, directly addressing the "visual-first" competitor insight.
- C48 (Story Card) is a **composition of existing features** — low risk, high polish.
- C53 (Social Sharing) leverages existing `url_sync.py` infrastructure — lowest effort.
- Together they form a coherent "make Stock Explorer more visual and shareable" theme.

**Pros**:
- No new infrastructure dependencies (beyond R3 batch API for C51).
- All three can be built within Sprint 3–4 (8+8+6 = 22h to 12+12+10 = 34h).
- Directly addresses competitor insights #4 (visual-first) and #1 (social learning).
- C49 (Market Pulse) can be deferred — it overlaps with C51's data pipeline.

**Cons**:
- C48 may feel redundant with existing business card (needs clear positioning).
- C51 depends on R3 (batch API) for performance — if R3 is delayed, C51 performance suffers.
- Doesn't address the "education/assessment" competitor insight (#5).

**Effort**: 22–34h (Sprint 3–4)

---

#### Direction B: "Engagement Loop + Education"

**Features**: C52 (Quiz Mode) + C48 (Story Card) + C49 (Daily Market Pulse)

**Rationale**:
- Addresses competitor insights #3 (daily engagement loops) and #5 (assessment).
- Quiz + Story Card create a **learning loop**: read story → test understanding → track progress.
- Daily Market Pulse gives users a reason to return daily.

**Pros**:
- Directly targets the "engagement loop" gap — the app currently has no daily-use feature.
- Quiz mode is a differentiated feature (Zerodha quizzes are popular).
- Story Card provides the content that Quiz tests against.

**Cons**:
- C49 requires market-level data infrastructure (new data flow path).
- C52 requires significant content creation (50–100 quiz questions = 10–15h content effort).
- C50 (Learning Progress Tracker) is deferred but is the natural companion to C52 — without it, quiz scores are ephemeral.
- Highest total effort: 10+8+14 = 32h minimum, plus content creation.

**Effort**: 32–46h (Sprint 3–5, plus content creation)

---

#### Direction C: "Platform Transformation"

**Features**: C54 (Video/Audio) + C50 (Learning Progress) + C52 (Quiz) + C49 (Market Pulse)

**Rationale**:
- The most ambitious direction — transforms Stock Explorer from a data viewer into a **learning platform**.
- Aligns with the long-term vision of "structured education becoming table stakes."

**Pros**:
- Highest long-term value — creates a genuinely differentiated product.
- Addresses 4 of 7 competitor insights.
- Would position Stock Explorer as the "Khan Academy of stocks."

**Cons**:
- **Not feasible in current architecture.** Requires: LLM integration (D5/R7), TTS pipeline, user persistence layer (D22), content management system.
- C54 alone is 20–30h and depends on unresolved architecture debt.
- Total effort: 50–80h minimum, spanning 2–3 sprints.
- High risk of over-engineering before product-market fit is established.

**Effort**: 50–80h (Sprint 4–6, requires D5 + D22 resolution first)

---

### Technical Risks & Dependencies Summary

| Risk | Severity | Affects | Mitigation |
|------|----------|---------|------------|
| **No market-level data pipeline** | 🔴 High | C49, C51 | Build `market_data.py` with batch API calls (R3) as shared infrastructure |
| **No LLM integration (D5)** | 🔴 High | C54, C48 (AI-enhanced) | Defer C54; C48 can use existing template-based analogies |
| **No persistence layer (D22)** | 🟡 Medium | C50, C52 (progress tracking) | Defer C50; C52 can use session_state for ephemeral quiz scores |
| **Content creation bottleneck** | 🟡 Medium | C52 (quiz), C48 (story elements) | Budget 10–15h for content creation separate from engineering |
| **Batch API performance (R3)** | 🟡 Medium | C51, C49 | Must complete R3 before C51/C49. Without it, heatmap/pulse will be slow (30–60s) |
| **analogy_engine.py god module (D16)** | 🟡 Medium | C48 (imports from it) | Complete D16 split before C48 to avoid coupling to unstable module |
| **Inline HTML duplication (D3)** | 🟡 Low | C53 (shareable cards) | Use R9 UI components for shareable card rendering |

### Dependency Graph

```
R3 (batch API) ──→ C51 (Sector Heatmap)
                ──→ C49 (Market Pulse)

D16 (split analogy_engine) ──→ C48 (Story Card)

R5 (YAML migration) ──→ C48 (story elements)
                     ──→ C52 (quiz questions)

R7 (LLM abstraction) ──→ C54 (Video/Audio) [FUTURE]

D22 (persistence layer) ──→ C50 (Learning Progress) [FUTURE]
                        ──→ C52 (persistent scores) [FUTURE]
```

---

### Recommendation

**Adopt Direction A ("Quick Wins + Visual Impact") for Sprint 3–4**, with one modification:

1. **C51 (Sector Heatmap)** — **Highest priority new feature.** This is the most impactful addition and the most architecturally interesting (introduces market-level data flow). Depends on R3. Start by building `market_data.py` as a shared service.

2. **C48 (Story Card)** — **Second priority.** Low-risk composition of existing features. Provides a "wow factor" for demos and presentations. Depends on D16 (split analogy_engine) for clean imports.

3. **C53 (Social Sharing)** — **Third priority.** Lowest effort, leverages existing `url_sync.py`. Can be implemented incrementally (URL sharing first, image export second).

**Defer to Sprint 5+**:
- C49 (Market Pulse) — shares data pipeline with C51 but adds scheduling complexity. Build after C51's `market_data.py` is stable.
- C52 (Quiz Mode) — feasible but content-heavy. Plan for Sprint 5 with dedicated content creation time.
- C50 (Learning Progress) — requires persistence infrastructure (D22). Not feasible without user accounts.
- C54 (Video/Audio) — requires LLM integration (D5/R7) + TTS pipeline. Long-term feature.

**Architecture debt sequencing for Sprint 3–4**:
1. R1 + D16 (financial_metrics extraction + split analogy_engine) — unblocks C48, C38, C44
2. R3 (batch API calls) — unblocks C51, C49
3. R5 (YAML migration) — unblocks C48 content, C52 content
4. C51 + C48 + C53 — the new feature trio

This sequencing ensures architecture debt is resolved **before** (or **alongside**) new feature development, not after.

---

*Created: 2026-06-18*
*Maintainer: System Architect*
*Next review: After Sprint 3 feature implementation*
