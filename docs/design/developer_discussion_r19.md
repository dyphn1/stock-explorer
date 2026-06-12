# 2026-06-19 Developer Estimate — Post-Sprint 10 Feature Directions

> **Author**: Developer
> **Context**: Sprint 10 (C34, C105, M5 remediation, D-061) is upcoming. This analysis covers everything AFTER Sprint 10.
> **Codebase state**: ~7,818 LOC, 31 .py files, 4-layer architecture. L0: 55/55 ✅, L1: 18/18 ✅

---

## Quick Wins (<8h each)

These features are low-risk, self-contained, and deliver visible user value with minimal architecture risk.

| ID | Feature | Base Estimate | Adjusted | Confidence | Justification |
|----|---------|--------------|----------|------------|---------------|
| **C37** | Key Takeaways Summary Card | 6-8h | **5-7h** | High | Already implemented in Sprint 2. N/A for future sprints — listed for reference only. |
| **C41** | Read Next Recommendations | 6-8h | **5-7h** | High | Already implemented in Sprint 3. N/A — reference only. |
| **C53** | Social Sharing | 6-10h | **5-8h** | High | HTML-to-image export + shareable URL params. Pure presentation layer. No new data sources. |
| **C83** | Investment Memo Template | 6-10h | **4-6h** | High | Pre-filled template with company data. Existing analogy engine covers explanation needs. Minimal UI. |
| **C85** | Financial Wellness Check | 8-12h | **5-7h** | High | Self-assessment quiz with scoring. Pure presentation + simple rule engine. Can reuse quiz patterns from C52. |
| **C104** | Post-Narrative Comprehension Check | 8-12h | **5-7h** | High | Quiz cards after each section. Reuse C52 quiz engine patterns. Needs per-section hook points. |
| **C66** | Conversational Tone | 6-10h | **3-5h** | High | UX writing pass — string changes only. No code architecture needed. Can batch across pages. |

**Total quick win effort: ~27-47h** (7 features). Pick 2-3 per sprint as fill items.

---

## Medium Features (8-16h each)

These require meaningful new code but follow established patterns and have clear data sources.

| ID | Feature | Base Estimate | Adjusted | Confidence | Justification |
|----|---------|--------------|----------|------------|---------------|
| **C44** | Risk Analysis | 10-14h | ✅ DONE | — | Already implemented in Sprint 3 (risk_analyzer.py, 567 lines). |
| **C45** | Valuation Band Chart | 8-10h | ✅ DONE | — | Already implemented in Sprint 2. |
| **C48** | Company Story Card | 8-12h | **10-14h** | Medium | Needs D16 (analogy_engine split) as prerequisite. story_composer.py will import from ~4 services. Business_card.py is already 561 lines — D24 extraction needed first. Adding dependency work, realistically 10-14h. |
| **C49** | Daily Market Pulse | 10-14h | **12-16h** | Medium | Needs market_data.py (D25). Market-level data flow is architecturally distinct from single-stock. New page file. First market-level feature — will establish patterns. |
| **C50** | Learning Progress Tracker | 12-16h | **10-14h** | Medium | Session state tracking + progress visualization. Reuses quiz data. Needs new service module (progress_engine.py). |
| **C51** | Sector Heatmap | 8-12h | **12-16h** | Medium | Needs R3 (batch API) or pre-computed data for performance. Needs market_data.py (D25). Chart rendering is straightforward (Plotly heatmap). Data aggregation is the hard part. |
| **C52** | Quiz Mode | 10-14h | **8-12h** | High | If C104 is built first, C52 reuses the quiz engine. Standalone quiz needs question bank YAML + scoring + UI. |
| **C55** | Investment Diary | 10-14h | **10-14h** | Medium | CRUD operations on diary entries. YAML storage. Needs new page + service. No complex data requirements. |
| **C56** | Explain This Metric | 12-16h | **10-14h** | High | Interactive tooltip/glossary system. If built as C33 (Glossary) first, this is additive. Standalone: YAML data + UI components. |
| **C57** | Compare Concepts | 10-14h | **8-12h** | High | Financial concept comparison. Static content + layout. Reuses analogy engine. Mainly a content creation task. |
| **C60** | Concept Mastery Badges | 8-12h | **6-10h** | High | Badge display + unlock conditions. Simple state tracking. Reuses progress data from C50 if built together. |
| **C61** | Sector Rotation Visualizer | 10-14h | **12-16h** | Medium | Needs market_data.py. Time-series sector performance data. Animated chart or multi-period heatmap. Data pipeline is the bottleneck. |
| **C62** | Pre-Investment Checklist | 8-12h | **6-8h** | High | Static checklist with progress tracking. Minimal service layer. Mostly presentation. |
| **C63** | Audio Market Story | 12-16h | **14-18h** | Medium | TTS integration (gTTS or similar) + market narrative generation. New dependency (audio library). Needs market_data.py. Crosses into >16h territory. |
| **C65** | Company Story Game | 10-14h | **10-14h** | Medium | Gamified drag-and-drop or multiple choice. Needs game state management + content. Medium complexity UI. |
| **C68** | Financial Concept Storytelling | 12-16h | **10-14h** | High | Narrative-based explanations for financial concepts. Content-heavy but technically simple. YAML content + rendering engine. |
| **C82** | Animated Data Story | 12-16h | **12-16h** | Medium | Scrolling animated charts. Plotly animation frames + scroll-triggered events. Streamlit's limited animation support is a risk. |
| **C84** | Market Event Case Study | 10-14h | **8-12h** | High | Historical event explorer. Uses existing event data (adaptive_engine.py). Template-based rendering. |
| **C88** | Market Narrative Feed | 14-20h | **14-18h** | Medium | AI-generated daily market narrative. Needs LLM integration (D5). Content pipeline + feed UI. Without LLM: template-based with curated data. |
| **C93** | Dividend Income Calendar | 12-16h | **10-14h** | High | Calendar view of dividend dates. Existing dividend data. New calendar UI component + income projection calculation. |
| **C94** | Earnings Story | 14-18h | **12-16h** | Medium | Post-earnings narrative. Template-based with data injection. Needs earnings calendar data from FinMind. |
| **C98** | Event Interpretation Engine | 14-18h | **14-18h** | Medium | "Why did this stock move?" — pairs price movements with events. Uses existing adaptive_engine + price data. Correlation engine. |
| **C101** | Comprehension Check (standalone) | 8-12h | **6-8h** | High | If C104 is built first, C101 is the broader implementation. Similar quiz engine. |
| **C40** | Beginner/Expert Mode Toggle | 10-14h | **8-10h** | High | Session_state toggle + conditional rendering. Actually simpler than estimated — it's a filter over existing content, not new content. |
| **C36** | Visual Revenue Tree | 10-14h | **8-10h** | High | Treemap/sunburst chart. Plotly has built-in support. Manual curation for top 10-20 stocks. Pure chart addition. |

**Total medium effort: ~240-330h** (24 features, adjusted). Realistic throughput: 2-3 per sprint.

---

## Major Projects (>16h each)

These are multi-day efforts with significant architecture implications, external dependencies, or high uncertainty.

| ID | Feature | Base Estimate | Adjusted | Confidence | Justification |
|----|---------|--------------|----------|------------|---------------|
| **C42** | Stock Screener / Discovery Engine | 16-24h | **18-26h** | Medium | Requires batch API calls (R3) or pre-computed Screening data to avoid performance death on 1,800+ stocks. New page + service module. UI for filter presets + custom filters. "Why passed" explanation adds analogy engine dependency. Performance risk is real — 財報狗 took years to build theirs. Start with top 200 stocks only. |
| **C46** | Moat Analysis | 12-16h | **16-22h** | Medium | Content curation is the bottleneck. Needs manual moat assessment for top 20-30 stocks. Morningstar's moat system is proprietary and complex. Simplified version (moat type + strength + historical evidence) is doable at 12-16h but content creation pushes it to 16-22h. Also needs template-based fallback for non-curated stocks. |
| **C47** | Financial Education Academy | 20-30h | **18-26h** | Medium | 10-15 structured lessons with content, examples, quizzes. Each lesson is ~1-2h of content creation. The architecture is simple (YAML + page + quiz engine) but the content creation dominates. Start with MVP of 5 lessons. |
| **C54** | Video Explanation | 20-30h | **22-30h** | Low | Video generation or curation at scale is hard. Slide-deck-to-video (manim or similar) has steep learning curve. Curated video links are simpler but less unique. Depends on approach chosen. High uncertainty. |
| **C58** | Beginner Onboarding Flow | 14-20h | **16-22h** | Medium | Multi-step guided flow with session state tracking. Needs onboarding content (YAML). Onboarding engine service. Blocked by D24 (business_card.py extraction) since onboarding references business card features. |
| **C59** | AI Q&A Chatbot | 16-24h | **20-30h** | Low | Requires LLM integration (D5 — not yet built). Chat interface in Streamlit (limited). Context injection (company data into prompt). Fallback for out-of-scope questions. High uncertainty given LLM dependency. The 16-24h estimate assumes LLM layer exists. Without D5: add 4-6h. |
| **C64** | Community Q&A | 16-24h | **22-32h** | Low | Backend storage for posts/comments. Moderation. User identity (even if anonymous). Thread notification. This is essentially building a forum — it's a separate product. Streamlit is NOT designed for this. Would need external backend (Firebase/Supabase) or a different framework. **Recommend: Deprioritize or rescope to "curated Q&A" using static content.** |
| **C67** | Community-Curated Stories | 14-20h | **20-28h** | Low | UGC system needs: identity, storage, moderation, voting, content guidelines. Same infrastructure concerns as C64. Without backend infrastructure, this is not feasible in Streamlit. |
| **C81** | Historical Decision Scenario | 14-20h | **16-22h** | Medium | "What would have happened if..." — backtesting + narrative. Needs historical price simulation engine + scenario definitions. Content-heavy (scenarios per stock). Backend logic is straightforward but UI is complex (interactive timeline + branching). |
| **C86** | AI Narrative Agent | 20-30h | **24-34h** | Low | Proactive plain-language analysis generation. Needs LLM integration (D5). Prompt engineering for financial narrative. Quality control / hallucination prevention. Batch generation pipeline. **Highest uncertainty feature — depend on D5 + LLM provider decision.** |
| **C87** | Explainable Analysis Layer | 12-16h | **14-18h** | Medium | Source transparency for every claim. Needs metadata tracking through the entire rendering pipeline. Non-trivial architecture change — every analysis function needs to return provenance data. Can be phased (start with key metrics only). |
| **C89** | Collaborative Company Analysis | 24-32h | **28-36h** | Low | Real-time collaborative editing + rooms. WebSocket support. User management. **Not feasible in Streamlit without major infrastructure.** Deprioritize. |
| **C91** | Adaptive Micro-Learning | 16-22h | **18-24h** | Low | Context-triggered 30-second lessons. Needs usage analytics + recommendation engine. Complex state management across sessions. Depends on progress tracking (C50) existing. |
| **C96** | Sector Ecosystem Map | 16-22h | **18-24h** | Medium | Visual supply chain map. Manual curation for top stocks. D3.js or Plotly network graph. Layout algorithms for circle positioning. Content creation is the bottleneck (relationship data). |
| **C97** | First 30 Days Onboarding | 18-24h | **20-28h** | Medium | Structured 30-day curriculum with daily micro-tasks. Combines C58 (onboarding flow) + C50 (progress tracking) + C60 (badges) + C52 (quizzes). **This is actually a meta-feature that depends on many prerequisites.** Build the components first, bundle later. |
| **C99** | Scrollytelling Mode | 16-22h | **18-24h** | Low | Animated vertical scroll through company history. Streamlit has very limited scroll-event support. Would need custom JavaScript injection. Possible but fragile. High effort for a single presentation mode. |
| **C100** | Natural Language Screener | 18-24h | **22-30h** | Low | Plain-language stock screening with "Why it passed" explanations. Combines C42 (screener) + LLM integration (D5) + analogy engine. **Triple dependency.** Build C42 first, add NLU layer later. |
| **C102** | Market Narrative Feed (alt. version) | 16-22h | **18-24h** | Medium | Similar to C88 but social-media-style UI. Needs feed pagination + market data aggregation + narrative generation. Depends on market_data.py (D25). |
| **C103** | Learn First Gate | 10-14h | **14-16h** | Medium | Soft educational onboarding before viewing stock data. Needs onboarding content + session state gating + progress tracking. Architecture is simple but content creation pushes effort up. |
| **C106** | First 7 Days Onboarding | 16-22h | **16-22h** | Medium | Compressed version of C97 with daily micro-lessons. Same dependency concerns. Needs TW stock examples for each lesson. Content creation is significant. |
| **C92** | TW Market Persona Explorer | 12-16h | **10-14h** | Medium | Investor archetypes with educational content. Actually simpler than estimated at ~10-14h. Content-heavy but technically straightforward (persona pages + quiz matching). |

**Total major effort: ~374-504h** (22 features). Realistic throughput: 1 per sprint, sometimes 1 per 2 sprints.

---

## Recommended Sprint Plan (next 3-4 sprints)

### Sprint 11: "Discovery + Market View"
**Theme**: Give beginners a way to discover stocks and see the big market picture.

| Item | Effort | Notes |
|------|--------|-------|
| **D16** (Analogy Engine split) | 2-3h | Prerequisite for many features. Extract key_takeaways.py, delta_engine.py, health_scoring.py. |
| **D24** (Business Card extraction) | 2-3h | business_card.py is 561 lines. Extract to sub-directory BEFORE adding more features. Non-negotiable. |
| **R3** (Batch API calls) | 1-2h | Prerequisite for C42 (Screener) and C51 (Sector Heatmap). Minimal version: batch_fetch_prices utility. |
| **C53** (Social Sharing) | 5-8h | Quick win. HTML-to-image export + shareable URL. |
| **C51** (Sector Heatmap) | 12-16h | Core sprint feature. Needs R3 + D25 (market_data.py). Create market_data.py service. |
| **Total** | **22-32h** | |

### Sprint 12: "Advanced Discovery + Education"
**Theme**: Advanced screening + structured learning content.

| Item | Effort | Notes |
|------|--------|-------|
| **R5** (YAML migration partial) | 3-4h | Move hardcoded data for C42, C56, C68 to YAML files. |
| **C42** (Stock Screener) | 18-26h | Major feature. Start with top 200 stocks + beginner presets. Needs R3 from Sprint 11. |
| **C56** (Explain This Metric) | 10-14h | Glossary + tooltip system. P1 priority. |
| **C62** (Pre-Investment Checklist) | 6-8h | Quick educational win. |
| **Total** | **37-52h** | Front-loaded sprint. C42 dominates. |

### Sprint 13: "Onboarding + Narrative"
**Theme**: First-time user experience + storytelling.

| Item | Effort | Notes |
|------|--------|-------|
| **C58** (Beginner Onboarding Flow) | 16-22h | Guided first experience. Needs D24 + content YAML. |
| **C48** (Company Story Card) | 10-14h | 30-second visual summary. Needs D16 (done Sprint 11). |
| **C68** (Financial Concept Storytelling) | 10-14h | Narrative-based concept explanations. Content-heavy. |
| **C84** (Market Event Case Study) | 8-12h | Historical event explorer. Reuses adaptive_engine. |
| **Total** | **44-62h** | Content-creation heavy sprint. |

### Sprint 14: "Gamification + Social"
**Theme**: Engagement loops + light social features.

| Item | Effort | Notes |
|------|--------|-------|
| **C50** (Learning Progress Tracker) | 10-14h | Prerequisite for C60, C97. Build the tracking foundation. |
| **C60** (Concept Mastery Badges) | 6-10h | Depends on C50. Gamification layer. |
| **C52** (Quiz Mode) | 8-12h | Standalone quiz with question bank YAML. |
| **C104** (Post-Narrative Comprehension Check) | 5-7h | Uses C52 quiz engine. Contextual placement. |
| **C66** (Conversational Tone) | 3-5h | UX writing pass. Can be done in parallel. |
| **Total** | **32-48h** | Moderate sprint. Good balance of features. |

### Post-Sprint 14 Vision (Sprints 15-18)

| Sprint | Focus | Key Features |
|--------|-------|-------------|
| **Sprint 15** | **LLM Integration** | **D5** (LLM abstraction layer) → **C86** (AI Narrative Agent) → **C88** (Market Narrative Feed) |
| **Sprint 16** | **Deep Finance** | **C46** (Moat Analysis) → **C93** (Dividend Calendar) → **C94** (Earnings Story) → **C96** (Sector Ecosystem Map) |
| **Sprint 17** | **Education Platform** | **C47** (Financial Education Academy) → **C97** (First 30 Days) or **C106** (First 7 Days) |
| **Sprint 18** | **AI Features** | **C100** (Natural Language Screener) → **C59** (AI Q&A Chatbot) → **C87** (Explainable Analysis Layer) |

---

## Technical Risks & Dependencies

### 🔴 Critical Risks (Must Address)

1. **business_card.py at 561 lines** (D24)
   - Adding C48, C58, C88 without extraction will push past 700 lines
   - **Mitigation**: D24 MUST be Sprint 11's first task. Non-negotiable.

2. **analogy_engine.py at 850 lines** (D16)
   - Blocks C48 (story_composer.py imports from it)
   - Blocks C86/C88 (AI narrative features need clean analogy interface)
   - **Mitigation**: D16 in Sprint 11, before C48 in Sprint 13.

3. **No LLM integration layer** (D5)
   - Blocks C59, C86, C88, C100 — all AI features
   - **Mitigation**: Schedule D5 for Sprint 15. Until then, use template-based fallbacks.

4. **Sequential API calls** (D7, D8, P1, P2)
   - C42 (Screener) will be unusably slow without batch fetching
   - **Mitigation**: R3 (batch API) in Sprint 11 before C42 in Sprint 12.

### 🟡 Medium Risks (Monitor)

5. **Market-level data flow** (D25)
   - C49, C51, C61, C88, C102 all need market-wide data aggregation
   - **Mitigation**: Create market_data.py in Sprint 11 (alongside C51).

6. **Hardcoded data in Python** (D6, D18)
   - C48, C56, C68, C96 need curated content. Hardcoding in Python doesn't scale.
   - **Mitigation**: R5 (YAML migration) in Sprint 12. All new features must use YAML data files.

7. **risk_analyzer.py at 567 lines** (D31)
   - Already approaching god-module territory. If more risk dimensions are added, it will need splitting.
   - **Mitigation**: Monitor. No immediate action.

8. **No test infrastructure** (D13)
   - At 7,818 LOC and growing, regressions are increasingly likely
   - **Mitigation**: D-061 (test infra) is in Sprint 10. Should be resolved before Sprint 11.

9. **Streamlit limitations for interactive features**
   - C64 (Community Q&A), C67 (Community Stories), C89 (Collaborative Analysis) require backend infrastructure that Streamlit doesn't provide
   - **Mitigation**: Deprioritize C64, C67, C89. Consider them for a future v2 with a different framework.

### 🟢 Low Risks (Accept)

10. **Inline HTML proliferation** (D3, D19, D32) — Will be addressed by D24 extraction + ui_components.py
11. **Session state proliferation** — Manageable with naming conventions. Audit in Sprint 15.
12. **FinMind API rate limits** — Mitigated by file-based caching. Monitor as data scope grows.

### Dependency Graph

```
Sprint 11: D16 ──┬──→ C48 (Sprint 13)
                  ├──→ C86/C88 (Sprint 15)
                  └──→ C59 (Sprint 18)

Sprint 11: D24 ──┬──→ C48 (Sprint 13)
                  ├──→ C58 (Sprint 13)
                  └──→ All business_card features

Sprint 11: R3  ──→ C42 (Sprint 12)
                     C51 (Sprint 11, same sprint OK)

Sprint 11: D25 (market_data.py) ──→ C49, C61, C88, C102

Sprint 12: R5 (YAML migration) ──→ C48, C56, C68, C96

Sprint 14: C50 ──→ C60, C97

Sprint 15: D5 (LLM layer) ──→ C59, C86, C88, C100
```

---

## Recommendations

### 1. Prioritize P1 Features First
The backlog has 10 P1 features. After Sprint 10, the remaining P1 features are:
- **C42** (Stock Screener) — 18-26h — Sprint 12
- **C56** (Explain This Metric) — 10-14h — Sprint 12
- **C58** (Beginner Onboarding) — 16-22h — Sprint 13
- **C88** (Market Narrative Feed) — 14-18h — Sprint 15 (needs D5)
- **C93** (Dividend Calendar) — 10-14h — Sprint 16
- **C94** (Earnings Story) — 12-16h — Sprint 16
- **C97** (First 30 Days) — 20-28h — Sprint 17
- **C100** (Natural Language Screener) — 22-30h — Sprint 18
- **C102** (Market Narrative Feed alt.) — 18-24h — Sprint 15

**Recommendation**: C42 and C56 are the highest-impact P1 features that can be built NOW (no LLM dependency). Prioritize them in Sprints 11-12.

### 2. Don't Build Community Features in Streamlit
C64 (Community Q&A), C67 (Community Stories), and C89 (Collaborative Analysis) require backend infrastructure (user management, real-time updates, moderation) that Streamlit fundamentally cannot provide. **Recommend deprioritizing all three to "future v2" or replacing with curated/static alternatives.**

### 3. Content Creation Is the Real Bottleneck
Features like C46 (Moat), C47 (Academy), C68 (Concept Storytelling), C96 (Ecosystem Map), and C97 (First 30 Days) are technically simple but require significant content creation. **Budget 30-50% of effort for content, not code.** Consider recruiting content contributors or using LLM-assisted content generation (once D5 exists).

### 4. LLM Integration Is the Key Enabler
D5 (LLM abstraction layer) unlocks the most differentiated features: C86 (AI Narrative Agent), C88 (Market Narrative Feed), C100 (Natural Language Screener), C59 (AI Q&A Chatbot). **Schedule D5 for Sprint 15 at the latest.** The longer it's delayed, the more the roadmap is blocked.

### 5. Keep Sprints Focused
Each sprint should have:
- 1 major feature (16-30h)
- 1-2 medium features (8-16h each)
- 0-1 quick wins (<8h)
- Architecture debt items as needed

Total sprint capacity: **30-50h** (assuming 1 developer, part-time). Don't overload sprints with 3+ major features.

### 6. Address Architecture Debt Proactively
The architecture is healthy overall (4-layer model holds, L0/L1 all green). But D16 and D24 are critical-path items that will block features if not addressed in Sprint 11. **Don't skip debt remediation to ship features — it will slow you down later.**

---

*Analysis based on: issues.md (55 backlog items), competitor_research.md (Rounds 7-9), architecture.md (Rounds 9-14, 33 debt items tracked). Adjusted estimates account for current codebase state (~7,818 LOC, 31 .py files, D1/D2/D17/D20 resolved, D16/D24/R3/D5 still open).*
