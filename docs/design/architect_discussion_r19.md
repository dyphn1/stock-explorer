## Saturday, June 13, 2026 Technical Analysis — Round 19 Discussion

### Executive Summary

Sprint 10 is about to begin with C34 (Company Story Timeline), C105 (Simple/Detailed Toggle), M5 remediation, and D-061 (test infrastructure). This analysis looks beyond Sprint 10 to propose 2-3 feature directions for the **next phase** of development (post-Sprint 10, roughly Sprint 11-12).

**Key Context:**
- Codebase: ~7,818 LOC, 31-32 .py files, L0: 55/55 ✅, L1: 18/18 ✅
- Sprint 10 items are decided: C34 + C105 + M5 + D-061
- Previously deferred from Sprint 11+: C99 + C81, C64, C65, C68
- Architecture: 4-layer model healthy, critical debt items (D16, D24/D30) in progress
- Competitor landscape: 14+ rounds of research completed, narrative features becoming table stakes globally

---

### Current Architecture Health Assessment

**Resolved (4 items):** D1, D2, D17, D20 (all financial metrics/EPS duplication)

**In Progress (2 items):**
- **D16**: `analog_engine.py` god module (850 lines, 6 responsibilities) — R1 unblocks this, should complete during Sprint 3
- **D24/D30**: `business_card.py` architectural limit (~560+ lines) — D24 extraction to sub-directory planned for Sprint 4

**Critical Open Debt (Sprint 11+ impact):**
| Item | Severity | Impact on Next Phase |
|------|----------|---------------------|
| D3: Inline HTML duplication | 🟡 Medium | Every new feature adds inline HTML to page files; UI inconsistency compounds |
| D5: No LLM integration layer | 🟡 Medium | C86 (AI Narrative Agent), C98 (Event Interpretation Engine) require this abstraction |
| D6: Hardcoded data in Python | 🟡 Medium | New curated features (C46 Moat, C81 Scenarios) need YAML data migration first |
| D7/D8: Sequential API calls | 🟡 Medium | C42 (Stock Screener) will be unusably slow without batch API calls (R3) |
| D13: No test infrastructure | 🟡 Medium | D-061 (test infra) is in Sprint 10 — should be resolved before Sprint 11 features |
| D11: No error boundary standardization | 🟡 Medium | Inconsistent error handling becomes painful as feature count grows |

**Competitor Pressure Points (from Rounds 8-9):**
1. **Narrative features converging globally**: Atom Finance, Dhan, Toss Securities, and Stake all have company story cards (C48's domain). C34 (Company Story Timeline) in Sprint 10 is the right move.
2. **Stock screeners are table stakes**: 財報狗's #1 feature; StockEdge visual screening; Stockopedia StockRank. C42 (Stock Screener) is P1 but deferred.
3. **Structured education is the endgame**: Investopedia Academy, Stockopedia Academy, Zerodha Varsity all prove demand for progressive learning paths (C47/C58/C97).
4. **AI-powered explanations growing**: Groww inline "Whys", Atom Finance AI summaries, Finimize AI Q&A. C56 (Explain This Metric) and C59 (AI Q&A Chatbot) address this but are deferred.

---

### Direction A: "Discovery & Screening" — Stock Screener + Market-Level Features

**What it encompasses:**
- **C42: Stock Screener / Discovery Engine** (P1, 16-24h) — The centerpiece. Multi-condition screening on key metrics (ROE, P/E, dividend yield, revenue growth) with beginner-friendly presets ("穩定收息", "成長潛力", "便宜估值"). Results link to existing business card pages.
- **C51: Sector Heatmap** (P2, 8-12h) — Visual market overview using Plotly treemap. Click-through to sector detail with plain-language explanations. Creates `market_data.py` service (addresses D25).
- **C49: Daily Market Pulse** (P2, 10-14h) — Automated daily market summary with institutional buy/sell surplus + volume + advance/decline data. Creates a daily engagement loop (currently missing).

**Technical Feasibility: 🟡 Medium**

**Pros:**
- C42 transforms Stock Explorer from passive lookup to active discovery — the #1 gap identified across 9 rounds of competitor research (財報狗's most popular feature)
- C51 creates the first market-level page, expanding the product's scope beyond single-company analysis
- C49 creates a daily reason to return (retention mechanism), addressing Finimize's "daily engagement loop" insight
- All three features establish the market-level data flow pattern (stock_id → data dict is the current pattern; these need market-wide → aggregate → visualize)

**Cons & Risks:**
- **Performance is the #1 risk**: C42 requires screening ~1,800 stocks. Without R3 (batch API calls, addressing D7/D8), this will be unusably slow (30-60+ seconds). R3 is a **hard prerequisite**.
- **Data architecture gap (D25)**: Market-level features need a new data flow pattern. `market_data.py` must be created alongside C51, not as an afterthought.
- **Tone guidelines (D23)**: C49 (Daily Market Pulse) produces market-level content that could accidentally sound like investment advice. Must define tone guidelines before implementation.
- **C42 scope risk**: Full 100+ metric screening is a product in itself. Must strictly limit to 5 beginner-friendly presets + 5 custom filters for the MVP.

**Dependencies:**
1. **R3 (Batch API)** — HARD prerequisite for C42. Currently planned for Sprint 4. If R3 slips past Sprint 10, this entire direction is blocked.
2. **R5/D6 (YAML migration)** — Screening presets and sector data should go in YAML files, not Python modules.
3. **C28 (LLM Spike)** — If C42 results include plain-language explanations ("Why this stock passed"), needs the LLM abstraction layer (D5).
4. **D-061 (Test infra)** — Screening logic needs tests; complete D-061 before or alongside C42.

**Total Effort: 34-50h (Sprint 11-12)**
- C42: 16-24h (screener service + page + YAML data)
- C51: 8-12h (market_data.py + treemap + YAML data)
- C49: 10-14h (market pulse service + page + tone guidelines)

**Priority Recommendation: HIGH but conditional on R3.** If R3 completes during Sprint 10, this should be Direction #1 for Sprint 11. The screener (C42) addresses the #1 competitive gap across all 9 research rounds.

---

### Direction B: "Deep Education" — Learn-Path Features + Interactive Understanding Tools

**What it encompasses:**
- **C58: Beginner Onboarding Flow** (P1, 14-20h) — Guided first experience that teaches core concepts before showing stock data. Structured as 5-7 progressive screens: "What is a stock?" → "What is revenue?" → "Let's explore TSMC" using real examples.
- **C47: Financial Education Academy** (P2, 20-30h) — Structured learning path with 10-15 lessons using real TW topics. Topics: "What is revenue?", "What is ROE?", "How to read a balance sheet", "What is a dividend?". Reuses analogy engine. Inspired by Zerodha Varsity (the closest philosophical match globally).
- **C56: Explain This Metric** (P1, 12-16h) — Inline hover/click explanations for every financial metric across all pages. Instead of a separate glossary page, explanations appear contextually. Directly addresses the "ten-second test" — a beginner encountering "ROE 25%" gets "每100元股東資金賺25元" on hover.
- **C52: Quiz Mode** (P2, 10-14h) — End-of-lesson quizzes and contextual comprehension checks after reading sections. Inspired by Finimize Academy and Zerodha Varsity.

**Technical Feasibility: 🟡 Medium-High**

**Pros:**
- Directly aligns with the "historian, not stock picker" positioning and "education-first" core value
- C58 + C47 create a structured progression from beginner to competent — the "point-to-point knowledge construction" principle made executable
- C56 (inline explanations) addresses the "ten-second test" design principle that is currently aspirational but not enforced
- Zerodha Varsity proves this model works at scale (5M+ learners) — and Stock Explorer's TW-localized approach would be unique in the TW market
- Competitor validation is strong: Zerodha Varsity, Investopedia Academy, Stockopedia Academy, Finimize Academy, Khan Academy Finance all prove demand

**Cons & Risks:**
- **Content creation is the bottleneck, not code**: C47 requires 10-15 lessons written in plain TW Chinese with real stock examples. This is ~60-70% of the effort. Plan for content creation to span 2 sprints.
- **C58 scope risk**: A full onboarding flow could expand to 20+ hours if not strictly limited to 5-7 screens. Must resist scope creep.
- **D6 (hardcoded data)**: Lesson content MUST go in `src/data/academy_lessons.yaml`, not in Python. Same for quiz questions (`src/data/quiz_questions.yaml`).
- **C56 requires touching every page**: Inline metric explanations need to be added to `business_card.py`, `financial_health.py`, `peer_comparison.py`, etc. This is a widespread change that could introduce UI inconsistencies (D3) if not done with reusable components from `ui_components.py`.
- **LLM dependency (D5)**: If C56/C52 use AI-generated explanations (à la Groww's "Whys"), they need the LLM abstraction layer. Template-only explanations are feasible but less compelling.

**Dependencies:**
1. **D6 (YAML migration)** — All lesson/quiz content must be YAML-first. Schedule alongside R5.
2. **R9/D3 (UI components)** — C56's inline tooltips need a reusable `render_tooltip_metric()` component. Do R9 before C56's page-level implementation.
3. **D16 (split analogy_engine.py)** — C47 lessons reuse analogy functions. Stable interfaces needed.
4. **D-061 (test infra)** — Quiz logic and lesson progression need tests. Ensure D-061 is complete.

**Total Effort: 56-80h (Sprint 11-13)**
- C58: 14-20h (onboarding flow + content creation)
- C47: 20-30h (academy engine + YAML content + 10-15 lessons)
- C56: 12-16h (tooltip system + content creation for 30-50 metrics)
- C52: 10-14h (quiz engine + 20-30 quiz questions)

**Priority Recommendation: MEDIUM-HIGH.** This direction is strategically important (defines the "education-first" positioning) but content-heavy. Recommend starting C58 (onboarding) in Sprint 11 as the first step, then C47/C56 in Sprint 12-13 once content creation ramps up.

---

### Direction C: "Smart Narrative" — AI-Powered Analysis Layer

**What it encompasses:**
- **C98: Event Interpretation Engine** (P1, 14-18h) — "Why did this stock move?" — AI-powered plain-language explanation for every detected event. Builds on M5 (adaptive event detection) which is being remediated in Sprint 10. When M5 detects an event (e.g., revenue miss, institutional sell-off), C98 generates a plain-language explanation: "營收較預期低15%，因為蘋果訂單減少，這通常是短期利空."
- **C86: AI Narrative Agent** (P2, 20-30h) — Proactive plain-language analysis generator. Instead of requiring users to navigate to a stock page, the AI agent generates daily/weekly narrative summaries for watched stocks. "Your watchlist this week: TSMC had a strong month (+8%) because of AI chip demand. UMC was flat because..."
- **C100: Natural Language Screener** (P1, 18-24h) — Plain-Language Stock Screening with "Why It Passed" Explanations. Extension of C42 (Direction A) but with natural language input: "Show me companies that pay good dividends and aren't too expensive" → filtered results with plain-language explanations for why each passed.
- **C68: Financial Concept Storytelling** (P1, 12-16h) — Narrative-based concept explanations. Instead of defining "ROE" as a formula, tell a story: "Imagine you invest $100 in a lemonade stand. At the end of the year, you made $25 profit. That's a 25% ROE." Pure content feature using existing analogy engine.

**Technical Feasibility: 🟡 Medium (template-first) / 🔴 Low (AI-powered)**

**Pros:**
- C98 directly leverages the M5 adaptive engine being remediated in Sprint 10 — perfect timing
- C86 creates the "daily engagement loop" that Finimize, TradingView, and others use for retention
- C100 transforms screening from a technical tool into a beginner-friendly experience — "natural language" input removes the learning curve
- C68 is the purest expression of "story first, data second" — financial concepts told as stories
- All four features differentiate from every TW competitor (none have AI narrative)

**Cons & Risks:**
- **D5 (LLM integration layer) is a hard prerequisite**: All four features need the LLM abstraction layer. Without D5, these features must use template-only approaches, which significantly limits quality.
- **Quality risk (LLM hallucinations)**: The product vision explicitly states "LLM limited to plain-language translation; facts come from structured data." C98 and C100 must be carefully designed to prevent hallucinated explanations. This requires significant prompt engineering or template design.
- **C86 is the highest-effort, highest-risk feature**: Proactive AI summaries require reliable data pipelines, quality output generation, and a feedback mechanism. 20-30h estimate could easily double.
- **C100 depends on C42**: Natural language screening requires a working screener (Direction A) as the foundation. Cannot build this first.
- **Latency concerns**: AI-powered features add API call latency. Streamlit's synchronous model means the user waits for LLM responses. Need to design for async UX (spinners, streaming, caching).

**Dependencies:**
1. **D5 (LLM abstraction layer)** — HARD prerequisite. Must define `ExplanationProvider` protocol and integrate at least one LLM provider before C98/C86/C100.
2. **M5 remediation (Sprint 10)** — C98 requires a working adaptive event detection engine. Sprint 10 M5 remediation is the prerequisite.
3. **C42 (Stock Screener)** — C100 builds on C42's screening infrastructure. Direction A must complete first.
4. **C28 (LLM Spike)** — The C28 spike is meant to validate the LLM architecture approach. If C28 hasn't completed its findings, D5 design may be premature.

**Total Effort: 64-88h (Sprint 12-14)**
- C98: 14-18h (event interpretation engine + templates)
- C86: 20-30h (AI narrative agent + scheduling + output quality)
- C100: 18-24h (NL interface + "Why It Passed" explanations)
- C68: 12-16h (story content creation — mostly writing, minimal code)

**Priority Recommendation: MEDIUM (template-first now, AI-powered later).** C98 and C68 can be done with templates in the near term (Sprint 11-12). C86 and C100 should wait until D5 (LLM layer) is designed (Sprint 12+). The template-first approach delivers 70% of the value at 30% of the risk.

---

### Priority Order & Sprint Sequencing

**Recommended Sprint 11-12 Plan (Post-Sprint 10):**

| Sprint | Direction | Items | Rationale |
|--------|-----------|-------|-----------|
| **Sprint 11** | A (Discovery) | R3 (if not done) + C42 (Stock Screener) + C68 (Concept Storytelling) | Address #1 competitive gap; C68 is low-effort content that reinforces positioning |
| **Sprint 11** | B (Education) | C58 (Beginner Onboarding) | Start the education pipeline; onboarding improves retention for all subsequent features |
| **Sprint 12** | A (Discovery) | C51 (Sector Heatmap) + C49 (Market Pulse) | Expand to market-level features once screener proves the pattern |
| **Spring 12** | B (Education) | C47 (Academy) + C56 (Explain This Metric) | Deepen education features once onboarding is live |
| **Sprint 12** | C (Narrative) | C98 (Event Interpretation) — template version | Leverages M5 remediation from Sprint 10; template approach is low-risk |

**Priority Ranking (which direction first):**

1. **🥇 Direction A (Discovery & Screening)** — HIGHEST priority. The stock screener (C42) addresses the #1 gap across all 9 rounds of competitor research. R3 performance fix is the only blocker. Without discovery, Stock Explorer remains a "lookup tool" that requires users to already know what to search for.

2. **🥈 Direction B (Deep Education)** — HIGH priority. C58 onboarding + C47 academy define the "education-first" positioning that no TW competitor has. Content creation is the bottleneck, not code. Start small (C58 first) and scale.

3. **🥉 Direction C (Smart Narrative)** — MEDIUM priority (deferred). Template-based versions (C98, C68) can ship in Sprint 12. AI-powered versions (C86, C100) should wait for D5 (LLM layer) + C28 findings. The competitive window is still open — no TW competitor has AI narrative yet.

---

### Cross-Cutting Architecture Concerns for Sprint 11+

1. **D-061 (Test Infrastructure) must complete in Sprint 10.** Sprint 11 features (C42 screener, C58 onboarding) need test coverage from day one. Building features without tests after the infra is available would be a regressions risk.

2. **D6 (YAML migration / R5) should happen before Sprint 11 content-heavy features.** C47 (20-30h of content), C68 (12-16h of stories), and C100 (screening explanations) all need YAML data files. If R5 doesn't precede these features, hardcoded data debt will compound.

3. **D16 (split analogy_engine.py) must complete before C47/C56/C98.** These features import analogy/health/ delta functions from the god module. A stable split prevents interface surprises during feature development.

4. **R9 (ui_components.py) should precede C56.** Inline metric explanations need reusable tooltip components. Building C56 without R9 means every page gets its own ad-hoc tooltip implementation — exactly the D3 anti-pattern that's already a problem.

5. **Market-level data flow (D25) needs documentation before C51/C49.** The `stock_id → data dict` pattern is the backbone of the current architecture. Market-level features use a fundamentally different flow (`market-wide → aggregate → visualize`). Document both patterns before implementing.

---

### Recommendation

For the next phase of development (post-Sprint 10), the team should pursue **Direction A (Discovery & Screening) as the primary focus**, supplemented by **Direction B (Deep Education) starting with C58 (Onboarding)**. Direction C should be deferred to Sprint 12+ for template-based versions, with AI-powered features waiting on the LLM architecture decision (D5 + C28).

**Key architectural prerequisites that must complete before or alongside Sprint 11:**
1. **R3 (Batch API)** — Blocks C42 screener performance
2. **D-061 (Test infra)** — Required for all new feature testing
3. **D16 (Split analogy_engine.py)** — Required for stable import interfaces
4. **R5 (YAML migration)** — Required for content-heavy features in Directions B and C

The screener (C42) is the highest-impact feature that Stock Explorer doesn't have and every major competitor does. Pairing it with the onboarding flow (C58) creates a complete beginner journey: **discover → learn → understand** → (eventually) **analyze deeply**.

---

*Created: 2026-06-13*
*Maintainer: System Architect*
*Next review: After Sprint 10 completion / Sprint 11 kickoff*
