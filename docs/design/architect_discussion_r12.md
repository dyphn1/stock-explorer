## 2026-06-18 Technical Analysis — Round 12 Discussion

### Problem Description

Round 12 competitor research (eToro, Webull, Robinhood, 富邦e富, 元大證券, 永豐金證券, 玉山證券, Magnify.money, Tastytrade) identified 8 new feature proposals (C55-C62). The team needs a technical feasibility analysis and a coherent grouping strategy before committing these to sprints. The current sprint plan has Sprint 3 (in progress) → Sprint 4 (planned) → Sprint 5 (planned), with a total of 60-80h already allocated. Adding 8 features (82-132h total effort) requires careful sequencing, dependency management, and strategic grouping.

Key constraints:
- **Stack**: Python + Streamlit + Plotly + FinMind API. No LLM in production (templates only). No native mobile app. No persistence layer (session state only).
- **Architecture health**: L0: 55/55, L1: 18/18 — first time all gates green. Must not regress.
- **Product vision**: "Historian, not a stock picker" — all features must pass "explain, don't predict" test.
- **business_card.py risk**: Currently 447 lines; D-025 (expandable card) and D24 (sub-dir extraction) are non-negotiable to prevent >600-line file.
- **No user identity**: No login system, no database. All user data is session-state only. This fundamentally limits features that require persistence (C55 diary, C60 badges, C58 onboarding replay).

---

### Feature Feasibility Analysis

#### C55: Investment Diary (10-14h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ⚠️ Medium — Core challenge is persistence. Session-state-only means diary entries are lost on page close. |
| **Dependencies** | None (standalone page + session state) |
| **Risks** | **Critical**: No persistence layer. Users close browser → all notes gone. This undermines the entire "personal learning archive" value proposition. Workaround: export-to-file or localStorage via Streamlit's `st.query_params` + JS injection, but both are hacks. |
| **Stack fit** | ✅ Streamlit forms + text input work fine. No new libraries needed. |
| **Vision fit** | ✅✅ Perfect "historian of self" — users become historians of their own journey. |
| **Verdict** | Buildable as session-only MVP, but must set user expectations clearly ("此為暫時性筆記，關閉頁面後將清空"). Full value requires D22 (persistence layer) which is blocked. |

#### C56: Explain This Metric (12-16h, P1)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ High — Template-based explanations in YAML, "❓" button + expander pattern, Plotly mini-charts. All within current stack. |
| **Dependencies** | None. Extends existing analogy_engine.py patterns. |
| **Risks** | Low. Main risk is content quality — writing 10 metric explanations with analogies + examples takes domain effort, not technical effort. |
| **Stack fit** | ✅✅ Perfect fit. `metric_explanations.yaml` + `st.expander()` + Plotly charts. Already have the pattern from analogy_engine.py. |
| **Vision fit** | ✅✅ Directly addresses "ten-second test" — every metric becomes a 10-second learning opportunity. |
| **Verdict** | Highest ROI feature. Low technical risk, high educational impact, P1 priority justified. |

#### C57: Compare Concepts (10-14h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ High — Pre-written content for 10 concept pairs. Dropdown selection + template rendering. No dynamic generation needed. |
| **Dependencies** | None. Standalone page. |
| **Risks** | Low. Content creation effort (writing 10 concept pair comparisons with TW examples) dominates over technical effort. |
| **Stack fit** | ✅ Pure Streamlit + templates. No new libraries. |
| **Vision fit** | ✅ "Point-to-point knowledge construction" — helps users understand metrics as tools, not answers. |
| **Verdict** | Buildable but content-heavy. Best paired with C56 (shared content structure). |

#### C58: Beginner Onboarding Flow (14-20h, P1)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ⚠️ Medium — Streamlit has limited onboarding/tutorial capabilities. No native step-by-step overlay system. |
| **Dependencies** | None (session state flag `onboarding_complete`) |
| **Risks** | **Medium**: Streamlit's UI model doesn't support multi-step modals with element highlighting. Workarounds: (1) sequential `st.info()` / `st.success()` banners, (2) custom CSS/JS overlay via `st.markdown(unsafe_allow_html=True)`, (3) dedicated "wizard" page with `st.progress()` bar. Option 2 is fragile across Streamlit versions. |
| **Stack fit** | ⚠️ Streamlit's limitations require creative workarounds for guided tours. |
| **Vision fit** | ✅✅ Critical for beginner retention — without onboarding, users bounce before discovering value. |
| **Verdict** | P1 priority is correct for user retention, but implementation will require careful Streamlit workaround design. Budget extra 2-4h for CSS/JS debugging. |

#### C59: AI Q&A Chatbot (16-24h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ⚠️ Medium — Pattern-matching approach (not LLM) is feasible. LLM approach is blocked (no production LLM, R7 not scheduled). |
| **Dependencies** | analogy_engine.py (for response templates), FinMind client (for data fetching) |
| **Risks** | **Medium**: Pattern-matching chatbot has limited question coverage. Users will ask unexpected questions → poor experience. Must design graceful fallback ("我還沒學會回答這個問題，試試問：這家公司賺什麼錢？"). Risk of disappointing users who expect ChatGPT-level answers. |
| **Stack fit** | ✅ Streamlit chat UI (`st.chat_input`, `st.chat_message`) works well. Pattern matching is pure Python. |
| **Vision fit** | ✅ "Story first" — natural language is the most beginner-friendly interface. But must be limited to historical/factual questions only (no predictions). |
| **Verdict** | Buildable as pattern-matching MVP. Set expectations clearly. LLM upgrade path exists via R7 but not in near-term roadmap. |

#### C60: Concept Mastery Badges (8-12h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ⚠️ Medium — Badge definition + criteria tracking in session state is simple. But "shareable badges" (C53 integration) requires image generation. |
| **Dependencies** | C52 (Quiz Mode) for quiz-related badges. C53 (Social Sharing) for shareable badge images. |
| **Risks** | **Medium**: Without persistence (D22), badges reset on session close. Gamification loses meaning if achievements are ephemeral. Also depends on C52 which is Sprint 5. |
| **Stack fit** | ✅ Session state tracking + YAML badge definitions. Image generation via Pillow or Plotly export. |
| **Vision fit** | ✅ Gamification drives engagement, but must be "explain, don't predict" — badges for learning, not for "correct predictions." |
| **Verdict** | Buildable as session-only MVP, but full value requires D22 persistence + C52 quiz mode. Best deferred to Sprint 6+. |

#### C61: Sector Rotation Visualizer (10-14h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ High — Extends C51 (Sector Heatmap) with time-series dimension. FinMind has sector performance data. |
| Dependencies | **C51** (Sector Heatmap) — builds on its `market_data.py` service and sector data fetching. |
| **Risks** | Low. Main risk is C51 not being complete yet — C61 must wait for C51's data layer. |
| **Stack fit** | ✅✅ Perfect fit. Plotly heatmap + time selector. Already proven pattern from C51. |
| **Vision fit** | ✅ "Benchmark-oriented analysis" + "adaptive and self-evolving" — explains sector momentum, doesn't predict. |
| **Verdict** | Technically straightforward, but hard-blocked by C51. Must be Sprint 5 or later. |

#### C62: Pre-Investment Checklist (8-12h, P2)

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | ✅ High — Simple checkbox list with anchor links. Pure Streamlit. |
| **Dependencies** | None. Self-contained component added to business_card.py. |
| **Risks** | Very low. Simplest feature technically. |
| **Stack fit** | ✅✅ `st.checkbox()` + anchor links. No new libraries. |
| **Vision fit** | ✅✅ Perfect "historian" feature — teaches what to look for, doesn't say what to do. |
| **Verdict** | Lowest effort, highest vision alignment. Should be prioritized early. |

---

### Direction A: Education-First (Recommended)

**Philosophy**: Double down on Stock Explorer's core differentiator — being the best educational tool for beginner investors. Every feature teaches something.

- **Features**: C56 (Explain This Metric) + C57 (Compare Concepts) + C62 (Pre-Investment Checklist) + C55 (Investment Diary)
- **Rationale**: These 4 features form a complete learning loop:
  1. **C62**: "Before you decide, check these things" — scaffolding
  2. **C56**: "What does this metric mean?" — just-in-time explanation
  3. **C57**: "How do these concepts relate?" — relational understanding
  4. **C55**: "What did I learn?" — reflection and retention
- **Pros**:
  - Tightest vision alignment — all 4 directly serve "point-to-point knowledge construction"
  - Shared content infrastructure — `metric_explanations.yaml` (C56) extends naturally to concept pairs (C57)
  - Lowest technical risk — all template-based, no LLM, no persistence required
  - C62 is the lowest-effort feature (8-12h) — quick win to validate the education-first approach
  - C56 is already P1 — validated by 3+ competitors
- **Cons**:
  - Doesn't address beginner retention (no onboarding)
  - Doesn't drive engagement/gamification
  - C55's persistence limitation remains
- **Effort**: 40-56h (C62: 8-12h + C56: 12-16h + C57: 10-14h + C55: 10-14h)

---

### Direction B: Onboarding + Engagement

**Philosophy**: Fix the #1 UX gap (beginners don't know where to start) and build engagement loops to retain users.

- **Features**: C58 (Beginner Onboarding) + C60 (Concept Mastery Badges) + C59 (AI Q&A Chatbot)
- **Rationale**: These 3 features address the full user journey:
  1. **C58**: First-time user discovers the tool → guided tour
  2. **C59**: User has a question → natural language interface
  3. **C60**: User learns → recognized for progress → shares → returns
- **Pros**:
  - Addresses the critical retention gap (C58 is the #1 UX complaint)
  - C59 is the most "magical" feature — natural language Q&A feels like the future
  - C60 creates engagement loop with social sharing (C53)
  - Competitor validation is strong: 玉山證券 (C58), 元大證券 (C59), Robinhood (C60)
- **Cons**:
  - Highest technical risk — C58 requires Streamlit workaround wizard, C59 requires pattern-matching design, C60 requires C52 dependency
  - C60 blocked by D22 (persistence) — badges reset on session close
  - C59's pattern-matching approach may disappoint users expecting AI
  - Highest total effort: 38-56h (C58: 14-20h + C59: 16-24h + C60: 8-12h)
- **Effort**: 38-56h

---

### Direction C: Market Context + Exploration

**Philosophy**: Help users understand the broader market context, not just individual companies. Expand from "company explorer" to "market explorer."

- **Features**: C61 (Sector Rotation Visualizer) + C59 (AI Q&A Chatbot) + C55 (Investment Diary)
- **Rationale**: These 3 features expand scope from single-company to market-level:
  1. **C61**: "What's happening across sectors?" — market momentum
  2. **C59**: "Ask me anything about any stock" — natural language market exploration
  3. **C55**: "What have I learned about the market?" — personal market journal
- **Pros**:
  - Expands product scope beyond single-company pages
  - C61 builds on C51 (already in Sprint 4) — natural extension
  - Creates a "market dashboard" feel that competitors like 永豐金證券 have
  - Aligns with "adaptive and self-evolving" core value
- **Cons**:
  - C61 is hard-blocked by C51 (Sprint 4) — can't start until Sprint 5
  - C59 is the most complex feature (16-24h)
  - C55's persistence limitation is more painful for market-level diary
  - Weakest alignment with "historian" positioning — sector rotation edges toward prediction
  - Doesn't address the beginner onboarding gap
- **Effort**: 34-50h

---

### Recommendation

**Adopt Direction A (Education-First) as the primary direction, with C58 (Beginner Onboarding) added as a prerequisite.**

**Rationale**:

1. **Vision alignment**: Direction A features are the purest expression of "historian, not a stock picker." C62 (Pre-Investment Checklist) is the single best embodiment of the product vision — it teaches users what to look for without telling them what to do.

2. **Technical feasibility**: All Direction A features are template-based, require no new libraries, no LLM, and no persistence layer. They build on existing patterns (analogy_engine.py → metric_explanations.yaml → concept_pairs.yaml). This is the safest path to maintain L0/L1 gates.

3. **Competitor validation**: C56 is validated by Magnify.money + Robinhood + 永豐金證券 (3 independent sources). C62 is validated by 永豐金證券 + Tastytrade. C57 is validated by Magnify.money. C55 is validated by 元大證券 + Tastytrade.

4. **Content synergy**: C56 and C57 share a content infrastructure. Building `metric_explanations.yaml` (C56) creates the foundation for `concept_pairs.yaml` (C57). This is efficient — one content architecture, two features.

5. **Add C58 as a prerequisite**: Direction A's education features are useless if beginners bounce before discovering them. C58 (14-20h) should be added as a Sprint 4 prerequisite, bringing the total to 54-76h — still within the 72-96h Sprint 4+5 budget.

**What to defer**:
- **C60 (Badges)**: Blocked by D22 persistence + C52 quiz mode. Defer to Sprint 6+.
- **C59 (AI Q&A)**: Highest risk, most complex. Defer to Sprint 6+ when pattern-matching approach can be properly designed.
- **C61 (Sector Rotation)**: Blocked by C51. Defer to Sprint 5 (after C51 completes in Sprint 4).

---

### Sprint Placement Recommendations

| Feature | Sprint | Rationale |
|---------|--------|-----------|
| **C62** Pre-Investment Checklist | **Sprint 4** (after R3, before C51) | Lowest effort (8-12h), zero dependencies, perfect vision alignment. Ideal "quick win" after infrastructure work. Adds to business_card.py but is small enough to fit before D24 extraction. |
| **C56** Explain This Metric | **Sprint 4** (after C62) | P1 priority, 12-16h, builds on analogy_engine.py patterns. Core education feature. Should be developed alongside C62 to share content infrastructure. |
| **C58** Beginner Onboarding Flow | **Sprint 5** (first item) | P1 priority for retention, 14-20h. Must come after Sprint 4's business_card.py changes (D24) so onboarding tour targets the final UI. Streamlit wizard design needs dedicated focus. |
| **C57** Compare Concepts | **Sprint 5** (after C56) | 10-14h, shares content infrastructure with C56. Natural follow-on after metric explanations are built. |
| **C55** Investment Diary | **Sprint 5** (after C57) | 10-14h, session-only MVP. Best positioned after education features (C56/C57) so users have content to reflect on. |
| **C61** Sector Rotation Visualizer | **Sprint 5** (after C51) | 10-14h, hard-blocked by C51's market_data.py. Natural extension of Sprint 4's C51. |
| **C59** AI Q&A Chatbot | **Sprint 6+** | 16-24h, highest complexity. Pattern-matching design needs careful UX work. Defer until education foundation (C56/C57) is built — chatbot can reference metric explanations. |
| **C60** Concept Mastery Badges | **Sprint 6+** | 8-12h, but blocked by D22 (persistence) + C52 (Sprint 5). Requires user identity system for meaningful gamification. |

**Sprint 4 Revised Plan** (72-96h with buffer):
1. R3 (Batch API, 1-2h) — prerequisite
2. D24 (business_card.py sub-dir, 2-3h) — prerequisite
3. **C62 (Pre-Investment Checklist, 8-12h)** — NEW, quick win
4. C51 (Sector Heatmap, 12-16h) — existing plan
5. C48 (Company Story Card, 10-14h) — existing plan
6. **C56 (Explain This Metric, 12-16h)** — NEW, P1 education
7. C53-1 (Social Sharing URL, 2-3h) — existing plan

**Sprint 5 Revised Plan** (72-96h with buffer):
1. **C58 (Beginner Onboarding, 14-20h)** — NEW, P1 retention
2. **C57 (Compare Concepts, 10-14h)** — NEW, education continuation
3. C49 (Daily Market Pulse, 14-20h) — existing plan
4. C52 (Quiz Mode, 12-18h) — existing plan
5. **C55 (Investment Diary, 10-14h)** — NEW, reflection tool
6. **C61 (Sector Rotation, 10-14h)** — NEW, extends C51
7. C53-2 (Social Sharing Image, 5-9h) — existing plan

**Sprint 6+** (future):
- C59 (AI Q&A Chatbot, 16-24h)
- C60 (Concept Mastery Badges, 8-12h + D22 persistence)
- D22 (Persistence layer) — unblocks C55/C60 long-term value

---

### Technical Dependency Graph

```
Sprint 3          Sprint 4                    Sprint 5                  Sprint 6+
─────────────────────────────────────────────────────────────────────────────────────
D16 (split        R3 (batch API) ──→ C51 (Sector Heatmap) ──→ C61 (Sector Rotation)
analogy_engine)        │                  │
  │                    ├──→ D24 (sub-dir) │
  ├──→ C44 (Risk)     │                  ├──→ C48 (Story Card)
  ├──→ C41 (Read Next)│                  └──→ C53-1 (Share URL)
  └──→ C38 (Compare)  │
                       ├──→ C62 (Checklist) ──→ C56 (Explain Metric) ──→ C57 (Compare Concepts)
                       │                                                    │
                       │                                                    └──→ C55 (Diary)
                       │
                       └──→ C58 (Onboarding) ──→ C49 (Market Pulse)
                              │                  │
                              │                  └──→ C52 (Quiz) ──→ C60 (Badges)
                              │
                              └──→ C59 (AI Q&A) [Sprint 6+]
```

### Key Technical Risks Summary

| Risk | Severity | Mitigation |
|------|----------|------------|
| business_card.py >600 lines | 🔴 High | D-025 (Sprint 3) + D24 (Sprint 4) are non-negotiable. C62 must be added before D24 to minimize merge conflicts. |
| Streamlit onboarding wizard limitations | 🟡 Medium | Budget +2-4h for CSS/JS workaround. Consider "sequential banner" approach instead of overlay highlights. |
| C55/C60 persistence gap | 🟡 Medium | Session-only MVP with clear user communication. Full value requires D22 (persistence layer) in Sprint 6+. |
| C59 pattern-matching disappointment | 🟡 Medium | Clear UX framing ("問關於這家公司的事" not "問任何問題"). Graceful fallback for out-of-scope questions. |
| Content creation effort (C56/C57) | 🟡 Medium | Start with 5 metrics (C56) and 5 concept pairs (C57). Expand based on user feedback. |
| C61 blocked by C51 | 🟢 Low | Natural Sprint 5 placement after C51 completes. No mitigation needed. |
