# Handoff – Development
## Summary
- **Topic**: Development (🔧) — Round 36, Sprint 16b
- **Date**: 2026-06-14 (Development Round 36 completed)
- **Sprint Status**: Sprint 16a ✅ COMPLETE → Sprint 16b ✅ COMPLETE → Sprint 17 planned

## Completed Items
| Issue ID | Description | Owner | Result | Commit |
|----------|-------------|-------|--------|--------|
| C28 | Story Timeline MVP — compose-and-enrich pipeline (events + case studies + milestones) | Developer | ✅ `timeline_service.py` created with `get_timeline()` pipeline; `company_milestones.yaml` for 10 TW stocks; `story_timeline.py` page with severity-coded timeline cards, dedup, empty state; nav button in story section | `ca49d2c` |
| D5 | LLM Abstraction Layer | Developer | ✅ `src/services/llm/` package: `ExplanationProvider` protocol, `ExplanationRequest`/`ExplanationResponse` dataclasses, `TemplateExplanationProvider` with 10 metric templates, `get_explanation_provider()` factory | `5e7fde8` |
| C07 | Custom Thresholds Settings Skeleton | Developer | ✅ `settings.py` page with 3 risk threshold sliders (price/volume/revenue), session_state persistence, reset-to-defaults button, validation; registered in router + url_sync | `84142f5` |
| C14+C135 | Health Score Badge + Narrative (Sprint 16a) | Developer | ✅ Enhanced simple mode with `get_health_summary()` narrative | `8051cb8` |
| C132 | Risk Simplification 1-5 Scale (Sprint 16a) | Developer | ✅ `risk_simplifier.py` with `get_risk_level()` | `8051cb8` |
| C41 | Read Next Phase A wire-up (Sprint 16a) | Developer | ✅ `_render_read_next()` wired into `_main.py` | `8051cb8` |

## Architecture Decisions
- **Timeline Service**: Pure Python compose-and-enrich pipeline merging 3 data sources (events.yaml + case_studies.yaml + company_milestones.yaml). Deduplicates same-day same-type events with count badges. All local YAML — no API calls, <200ms.
- **LLM Abstraction**: Protocol-based design (`ExplanationProvider`) with `runtime_checkable` for structural subtyping. Template fallback covers 10 financial metrics. Future `LLMProvider` can implement same interface without changing callers.
- **Settings**: Skeleton only — 3 sliders + session_state persistence. Full threshold UI deferred to Sprint 17.
- **Page Registration**: Both `story_timeline.py` and `settings.py` registered in router with URL sync.

## Verification
- **L0**: 110 passed (2 pre-existing failures in quiz_service.py — unrelated)
- **L1**: 20/20 ✅
- **Commits**: `ca49d2c`, `5e7fde8`, `84142f5`

## Next Cycle
🔧 Development Round 36 Complete → 🔍 Review Round 36 → Sprint 17 (C07 Full Thresholds + C134 Change Explanations + C29 Explain Any Metric + C14 Full Radar)

---

# Handoff – Review (Archive)
## Summary
- **Topic**: Review (🔍) — Round 34, Sprint 15 Post-Mortem
- **Date**: 2026-06-14 (Review Round 34 completed)
- **Sprint Status**: Sprint 15 ✅ COMPLETE → Sprint 16a ✅ COMPLETE → Sprint 16b planned
## Key Metrics
- Design grade: A (upgraded from A- — C126/C47/C101 demonstrate strong design discipline)
- L0: 106/106 ✅ | L1: 20/20 ✅ | Tests: 165+/165+ ✅
- Architecture: 🟢 HEALTHY — 38 service modules, 0 god modules, 100% Streamlit-free
- Sprint 15: 10 debt items resolved (D-072, D-073, D-074, D-077, D-084, D-086, D-088, D-090, chart.py split, CI enforcement)
- Sprint 16: C14 Health Score + C45 Valuation Band + C28 Story Timeline Spike + C41 Read Next Phase A (from Round 33 plan)
- New feature gaps: C132-C138 (Risk Simplification, Micro-Lessons, Change Explanations, Health Score Narrative, Goal-Based Learning, Visual Comparison, Smart Notifications)
- Inline HTML: 11 instances remaining (down from 27 in Round 26) — CI enforcement prevents new instances
## Sprint Plans (Summary)
||| Sprint | Items | Status ||
|||--------|-------|--------||
||| Sprint 3-12 | Various | ✅ Complete ||
||| Sprint 13a | C33 Glossary + C48 Story Card | ✅ Complete ||
||| Sprint 13b | D-079 + C36 Revenue Tree V2 + C46 Moat Analysis | ✅ Complete ||
||| Sprint 14 | C47 Education Academy + C40 Mode Toggle + C126 Moat Comparison | ✅ Complete ||
||| Sprint 15 | D-090 + CI + chart.py split + D-084/D-086/D-088 | ✅ Complete ||
||| Sprint 16 | C14 Health Score + C45 Valuation Band + C28 Spike + C41 Phase A | 📋 Planned ||
## Key Rules
- Content cap: 100 items max across all features
- Mandatory historian tone QA gate before each content feature ships
- Card-count limit: max 5 cards per page section (Direction A)
- Community features (C64, C67, C89) deprioritized — not feasible in Streamlit
- Content creation must be budgeted at 40% of effort for education features
- Priority resolution: vision alignment > retention impact > technical risk
- CI enforcement: no-inline-html check must pass before every commit (since Sprint 15)
## 💡 Discussion Section (Round 29 — 2026-06-18)
**Topic**: Sprint 14 Scope Validation — C40 Mode Toggle + C126 Moat Comparison + C47 Education Academy + C125 stretch
**Challenger**: ✅ CONFIRMED with 7 revisions
**Key Decisions**: C40→C126→C47 execution order; 5 complete lessons (min 3) with ten-second test quality gate; C125 stretch goal; session_state disclaimer; D-005 remediation via C40; C123 deferred (data blocker)
**Full details**: docs/state/handoff_discuss_r29.md
## 🔍 Review Section (Round 30 — 2026-06-18)
**Theme**: Review Round 30 — Sprint 13b Post-Mortem + Sprint 14 Prerequisites
### Sprint 14 Adjusted Plan
1. **Day 0**: Fix D-077 (0.5h) + C47 architecture spike (2-4h)
2. **C40 Mode Toggle**: Enhance existing C105 toggle (8-12h)
3. **C126 Moat Comparison**: Side-by-side moat comparison (12-16h)
4. **C47 Education Academy**: 5 structured lessons + quiz + progress (20-30h, 40% content)
5. **C125 Segment Profitability**: Stretch goal, needs data validation (10-14h)
## 💡 Discussion Section (Round 31 — 2026-06-18)
**Topic**: Feature Prioritization for Next Sprint — Notifications, Key Takeaways, Health Score, Company Story Timeline (spike), Beginner/Expert Mode (ongoing), PPT Export (stretch)
**Participants**: Product Manager, System Architect, Developer, Designer, Challenger
### Summary
- No items completed this cycle (discussion and planning only)
- Team preliminary decision accepted after three-round challenge with Challenger
- Prioritized features: Notifications (C02) as P0 gap, Key Takeaways (C37) as quick win, Company Story Timeline (C34) spike for de-risking, Health Score (C14) to pay down analogy_engine.py god module, Beginner/Expert Mode (C40) ongoing, PPT Export (C06) as stretch goal
- Architecture debt resolution (R2-R5) to proceed in parallel
### Idea Proposals
|| Idea ID | Description | Owner | Status ||
||---------|-------------|-------|--------||
|| C02 | Notifications System — bell icon + unseen event count from M5 engine | Architect | Accepted ||
|| C37 | Key Takeaways Summary Card — 3-5 bullet points at top of business card | Design Reviewer | Accepted ||
|| C34 | Company Story Timeline — narrative of events, revenue, price movements | Design Reviewer | Deferred (spike) ||
|| C14 | Health Score / Snowflake Analysis — 5-dimension visual health score | Architect | Accepted (after D-16 refactor) ||
|| C40 | Beginner/Expert Mode Toggle — progressive disclosure for metrics | Design Reviewer | In Progress (Sprint 14) ||
|| C06 | PPT Export — export business card as image/PDF | Developer | Stretch Goal ||
|| C35 | Market Mood Index — institutional buying pressure score | Architect | Deferred (data validation needed) ||
### Decisions Made
- Notifications (C02) is top priority for next sprint due to P0 gap and existing M5 engine readiness
- Key Takeaways (C37) to be implemented alongside notifications as low-effort, high-impact item
- Company Story Timeline (C34) requires a spike to validate narrative synthesis approach before full implementation
- Health Score (C14) will be implemented after refactoring analogy_engine.py (D-16) to reduce god module
- Beginner/Expert Mode (C40) continues as planned in Sprint 14
- PPT Export (C06) treated as stretch goal pending export capability readiness
- Architecture debt items R2 (UI helpers), R3 (batch API calls), R4 (session caching), R5 (YAML migration) to be addressed in parallel
### Action Items
|| Item ID | Description | Owner | Due Date ||
||---------|-------------|-------|----------||
|| A1 | Implement notification service and UI bell icon | Developer | Next Sprint ||
|| A2 | Implement summary_engine.py and Key Takeaways card | Developer | Next Sprint ||
|| A3 | Spike Company Story Timeline narrative architecture | Designer/Architect | Next Sprint ||
|| A4 | Refactor analogy_engine.py (D-16) to extract health scoring | Developer | Sprint after next ||
|| A5 | Continue C40 Beginner/Expert Mode implementation | Developer | Sprint 14 ||
|| A6 | Investigate PPT export capabilities (html2image/kaleido) | Developer | Stretch Sprint ||
|| A7 | Execute R2: move UI helpers out of _router_base.py | Developer | Ongoing ||
|| A8 | Execute R3: batch API calls in category_browser and etf_browser | Developer | Ongoing ||
|| A9 | Execute R4: session-level caching for watchlist and events | Developer | Ongoing ||
|| A10| Execute R5: migrate hardcoded data to YAML files | Developer | Ongoing ||
## 💡 Discussion Section (Round 33 — 2026-06-14)
**Topic**: Post-Sprint 15 Feature Planning — C14 Health Score + C45 Valuation Band + C28 Story Timeline Spike + C41 Read Next + C02 Notifications (conditional)
**Participants**: Product Manager, System Architect, Developer, Designer, Challenger
**Challenger**: ✅ CONFIRMED with 5 revisions

### Key Decisions
- **Sprint 16a (12-18h)**: C14 Health Score Badge + C45 Valuation Band + C28 Story Timeline Spike + C41 Read Next Phase A
- **Sprint 16b (conditional)**: C28 Full (26-36h) if spike passes, OR C02 Notifications + C07 Custom Thresholds (18-28h) if spike fails
- **Sprint 17 (20-29h)**: C29 Explain Any Metric + C41 Phase B + C14 Full Radar
- **Critical discovery**: Backlog is stale — C37, C39, C36, C38, C16 already implemented
- **Strategic trade-off**: C02 Notifications deferred 1-2 sprints for unique differentiators

**Full details**: docs/state/handoff_discuss_r33.md

## 🔍 Review Section (Round 32 — 2026-06-13)
**Theme**: Review Round 32 — Sprint 14 Post-Mortem + Sprint 15 Prerequisites

### Sprint 14 Development Verified
- C126 (Moat Comparison): ✅ moat_comparison.py created, uses shared components, zero inline HTML
- C47 (Education Academy): ✅ academy.py + lesson_service.py + 5 lesson YAMLs, clean separation
- D-081: ✅ Metric popover now uses _白话_card()
- D-082: ✅ _mini_score_card() created with score-based border colors
- D-083: ✅ Story card health border now color-coded

### Key Metrics
- L0: 106/106 ✅ | L1: 20/20 ✅ | Tests: 165+
- Architecture: 🟡 A- (chart.py at 842 lines — large coherent module, not god module)
- Design: A- (D-081/D-082/D-083 resolved, 5 new P2 issues consolidated)
- Service modules: 31 | Page modules: ~38

### New Debt Identified
- D-077: chart.py large coherent module (842 lines) — MEDIUM — split into chart_stock.py + chart_market.py
- D-078: _financial.py inline HTML span in _info_card() — LOW
- D-079: _financial.py dividend table unsafe_allow_html — LOW
- D-080: academy.py st.error()/st.warning() — LOW
- D-089: _financial.py growing multi-responsibility (343 lines, 6 render functions) — monitor
- D-090: Metric popover session_state accumulation — LOW — replace with st.popover()

### Challenger 3-Round Challenge: ✅ CONFIRMED with 6 conditions
1. D6 YAML migration must be FIRST task (content scaling #1 risk)
2. CI check for inline HTML must be implemented before new features
3. Any feature must pass historian filter AND ten-second test
4. Backlog Budget enforced (max 100 features, +1/-1 rule)
5. Grading criteria updated (god module vs. large coherent module)
6. Moat comparison page must include historian disclaimer

### Sprint 15 Confirmed Plan
1. **D6 YAML Migration** (3-4h) — FIRST. Migrate _CASE_STUDIES + 5 remaining blocks
2. **chart.py Split** (1-2h) — chart_stock.py + chart_market.py
3. **CI Check: No Inline HTML** (1-2h) — automated enforcement
4. **Design Cleanup** (2-3h) — batch D-084 through D-088
5. **C101 Comprehension Check Quiz** (8-12h) — story/education feature
6. **D-090 Metric Popover Fix** (0.5h) — replace with st.popover()
- Total: 15.5-23.5h

### Structural Changes
- Backlog Budget: max 100 features (currently 131, target ≤125 by Sprint 15 end)
- Feature Triage: every 3 rounds, review entire backlog
- Grading criteria: distinguish "god module" from "large coherent module"
- CI check: automated enforcement for unsafe_allow_html

## 💡 Discussion Section (Round 35 — 2026-06-14)
**Topic**: Sprint 16b Planning — C28 Story Timeline + C07 Custom Thresholds + LLM Layer
**Challenger**: ✅ CONFIRMED with 5 revisions
**Key Decisions**: C28 MVP (events + case studies), C07 settings skeleton started, D5 LLM abstraction layer built, data seeded, empty state handling, C134 deferred to Sprint 17
**Full details**: docs/state/handoff_discuss_r35.md

## Archive
See git history for previous rounds and development sections.

### Summary
- **Date**: 2026-06-13
- **Theme**: 🔧 Development — Sprint 14 Continuation
- **Participants**: Product Manager, System Architect, Developer
- **Status**: ✅ COMPLETE

# 🔍 Review Section (Round 35 — 2026-06-14)
**Theme**: Review Round 35 — Sprint 15 Post-Mortem + Sprint 16 Prerequisites

## Competitor Research Findings
QA Engineer completed analysis of competitors including StatementDog, GoodInfo, CMoney, WantGoo, Public.com, Seeking Alpha, Koyfin, Stocksera, 財報狗, JZ Invest, 鉅亨網, TEJ, Yahoo Finance Taiwan, Simply Wall St, Stockopedia, and Investopedia. Identified 18 high-potential feature opportunities from rounds 20-27, with top recommendations being:
- **Immediate Priority (P1)**: C134 (AI-Generated Change Explanations), C138 (Smart Notifications with Explanations), C119 (Glossary-First Onboarding), C98 (AI Event Interpretation Engine)
- **Strategic Opportunities (P2)**: C120 (Story Card Export), C116 (Investor Story Feed), C113 (Sector Story Timeline)

## Design Improvements
Design Reviewer analyzed current problems and competitor designs, identifying:
- **P1 Issues**: D-003 (Inconsistent Card Styling), D-006 (Mobile Responsiveness Gaps), D-005 (Business Card Page Overload Risk)
- **P2 Issues**: D-004 (Design System Documentation), D-010/D-011 (Non-PPT layouts), D-012 (No Glossary/Tooltip System), D-015 (No Structured Learning Path)
- **Proposed Plans**: Fix card styling inconsistencies, implement progressive disclosure, improve mobile responsiveness, update design system, and incorporate competitor-inspired features like Stock Screener (C42), Snowflake Health Visualization (C43), Risk Analysis (C44), Valuation Band Chart (C45), Moat Analysis (C46), Financial Education Academy (C47), Tappable Glossary (C33), and Beginner/Expert Mode Toggle (C40)

## Technical Debt Priorities
System Architect assessed architecture health as 🟢 HEALTHY with:
- **High Severity**: D5 (LLM integration layer) - blocker for C98 and LLM-dependent features
- **Medium Severity**: D6 (YAML migration completion), D-074 (test infrastructure fix), D-042/D-046 (section file growth and inline HTML)
- **Low Severity**: Various minor issues mostly resolved or deferrable
- **Architecture Metrics**: 38 service modules (89% <300 lines, 100% Streamlit-free), ~42 page modules (largest 437 lines), 0 god modules, 165+ tests passing
- **Recommendations**: Prioritize D6 YAML migration (3-4h), D5 LLM layer (2-3h), and D-074 test fix (0.25h) before Sprint 16 feature work

## Optimization & Feature Cost Estimates
Developer provided implementation cost estimates:
- **Sprint 16a** (C14 Health Score + Narrative, C132 Risk Simplification, C45 Valuation Band, C28 Story Timeline Spike): 17-24h (updated from initial 12-18h estimate)
- **Sprint 16b Conditional**: 
  - If C28 spike passes: C28 Full Story Timeline (26-36h)
  - If C28 spike fails: C02 Notifications + C07 Custom Thresholds (18-28h)
- **Technical Debt Optimization**: D6 YAML migration (3-4h), D5 LLM layer (2-3h), D-074 test fix (0.25h), Inline HTML extraction (2-3h), Performance debt fixes (3-4h)
- **Competitor Research Features**: C33 Glossary (8-12h), C34 Story Timeline (16-24h), C37 Key Takeaways (6-8h), C38 Compare Stories (12-16h), C39 Delta Card (8-10h), C40 Beginner/Expert Mode (10-14h)

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| R35-OPT1 | Complete D6 YAML migration (remaining hardcoded data blocks) | Developer | Before Sprint 16 feature work |
| R35-OPT2 | Create LLM abstraction layer (src/services/llm/) | Developer | Before Sprint 16 feature work |
| R35-OPT3 | Fix D-074 test infrastructure (add filelock dependency) | Developer/QA Engineer | Before Sprint 16 feature work |
| R35-DES1 | Fix inconsistent card styling (D-003) by enforcing shared components | Designer/Developer | Ongoing - begin Sprint 16 |
| R35-DES2 | Improve mobile responsiveness (D-006) with responsive CSS | Designer/Developer | Ongoing - begin Sprint 16 |
| R35-FEAT1 | Implement Sprint 16a planned features: C14, C132, C45, C28 Spike | Developer | Sprint 16a |
| R35-FEAT2 | Prepare for Sprint 16b decision based on C28 spike validation results | PM/Architect | End of Sprint 16a |
| R35-FEAT3 | Update design system documentation (D-004) with current components | Designer | Sprint 16 |

## Next Cycle Handoff
Reference `docs/state/handoff_review.md` for detailed review artifacts. Next theme will be determined based on Sprint 16a completion and C28 spike validation outcome.

### Completed Items
| Issue ID | Description | Owner | Result | Commit |
|----------|-------------|-------|--------|--------|
| C126 | Competitor Moat Comparison View — side-by-side moat analysis page | Developer | ✅ Created `src/pages/moat_comparison.py` with peer discovery, moat score/dimension/type/evidence comparison; registered in router + url_sync; nav button in business card "更多分析" expander | `724921c` |
| D-081 | Metric popover card uses inline HTML instead of `_白话_card()` | Developer | ✅ Replaced inline HTML in `_render_metric_popover()` in `_financial.py` with `_白话_card()` call | `724921c` |
| D-082 | Moat dimension mini-cards use `_summary_card()` with wrong styling | Developer | ✅ Created `_mini_score_card()` helper in `_router_base.py` with score-based border colors; replaced in `_moat.py` | `724921c` |
| D-083 | Story card health score border not color-coded | Developer | ✅ Added `border_color` param to `_summary_card()` in `_router_base.py`; health score now passes score-based color | `724921c` |
| C47 | Financial Education Academy — 5 structured lessons + quiz + progress | Developer | ✅ Created `lesson_service.py`, `academy.py` page, 5 lesson YAMLs (lesson_01–05), `academy_meta.yaml`; registered in router + url_sync | `85f03b6`, `5d6df6a`, `b2cac6d` |

### Architecture Decisions
- **C126**: No new service functions needed; reused `moat_analyzer.get_moat_summary()` and followed `compare_stories.py` page pattern
- **C47**: YAML-defined content + pure Python service + Streamlit page; progress tracking via `st.session_state`; no database needed for v1
- **`_mini_score_card()`**: New compact card variant in `_router_base.py` for score-based dimension displays (green ≥70, amber ≥40, red <40 border)
- **`_summary_card()` border_color param**: Optional parameter added with default `#F39C12` for backward compatibility
- **lesson_service.py**: Pure Python (no Streamlit imports); `get_progress()` accepts progress_dict parameter instead of accessing session_state directly

### Verification
- **L0**: 106/106 ✅ (0 failures, 0 warnings)
- **L1**: 20/20 ✅ (0 failures, 0 warnings)
- **Total tests**: 165+ (L0 + L1 + existing 149)

### Git Commits
| Hash | Message |
|------|---------|
| `724921c` | feat: add C126 moat comparison page + fix D-081/D-082/D-083 |
| `85f03b6` | feat: add lesson_service.py and 5 lesson YAML files for C47 Education Academy |
| `5d6df6a` | feat: add academy page and router registration for C47 Education Academy |
| `b2cac6d` | fix: remove streamlit import from lesson_service.py; wire academy page session_state management |

### Pending Items
| Issue ID | Description | Owner | Next Steps |
|----------|-------------|-------|------------|
| C125 | Segment-Level Profitability View | Developer | Stretch goal — needs data validation; deferred to next sprint |
| C34 | Company Story Timeline spike | Designer/Architect | Requires narrative synthesis spike; deferred |

### Next Cycle
🔧 Development Round 32 Complete → 🔍 Review Round 32 → Sprint 15 Planning (C125 Segment Profitability + C40 Mode Toggle refinement + architecture debt R2-R5)

---

## 🔍 Review Section (Round 34 — 2026-06-14)
**Theme**: Review Round 34 — Sprint 15 Post-Mortem + Sprint 16 Prerequisites

### Competitor Research (Round 10)
**New Competitors Researched**: 7 (Gotrade, Ellevest, StockTwits, Acorns, Datawallet, Visual Capitalist, Spiking)
**New Feature Gaps Identified**: 7 (C132-C138)

| ID | Feature | Priority | Effort | Source |
|----|---------|----------|--------|--------|
| C132 | Risk Level Simplification (1-5 Scale) | P1 | 6-10h | Gotrade |
| C133 | Daily Financial Education Micro-Lessons | P2 | 10-14h | Acorns |
| C134 | AI-Generated Change Explanations | P1 | 12-16h | Datawallet/Spiking |
| C135 | Financial Health Score with Narrative | P1 | 10-14h | Spiking |
| C136 | Goal-Based Learning Path | P2 | 14-20h | Ellevest |
| C137 | Visual Comparison Cards | P2 | 8-12h | Visual Capitalist |
| C138 | Smart Notifications with Explanations | P1 | 10-14h | Spiking |

**Key Insights**:
- "Change Explanations" are the new baseline — Datawallet, Spiking, and Copilot Money all explain WHY numbers changed
- Spiking is the most directly relevant uncovered competitor — its "Why Stock Moved" AI validates C98 + C107 direction
- Simplified risk communication is table stakes — Gotrade's 1-5 scale proves beginners need simple risk indicators

### Architecture Debt Review
**Items Verified Resolved**: 10 (D-072, D-073, D-074, D-077, D-084, D-086, D-088, D-090, chart.py split, CI enforcement)
**New Debt Items**: 7 (D-091 through D-098, all Low severity except D-097 Medium)
**Architecture Grade**: 🟢 HEALTHY — 38 service modules, 0 god modules, 100% Streamlit-free, 165+ tests

**Top 3 Architecture Recommendations for Sprint 16**:
1. Verify test coverage on Day 1 (0.25h)
2. Plan C14 Health Score chart integration — recommend new `chart_health.py` module (0.5h planning)
3. Build LLM abstraction layer before C98 (2-3h)

### Design Review
**Design Grade**: A (upgraded from A-)
**New P2 Issues**: D-091 (glossary tooltip not wired), D-092 (academy lesson list), D-093 (moat comparison sequential fetch), D-094 (dividend table inline HTML escalated), D-095 (quiz results)
**Consolidations**: D-052+D-053 documented, D-062+D-063 consolidated, D-043→D-094 escalated
**Notable**: C126 moat comparison page is the best-designed new page since C105

### Sprint 16 Readiness
**Verdict**: ✅ READY — No blockers. All prerequisites met.
**Plan** (from Round 33 Discussion):
1. **Sprint 16a (12-18h)**: C14 Health Score Badge + C45 Valuation Band + C28 Story Timeline Spike + C41 Read Next Phase A
2. **Sprint 16b (conditional)**: C28 Full (26-36h) if spike passes, OR C02 Notifications + C07 Custom Thresholds (18-28h) if spike fails

---

## 🔥 Challenge Section (Round 34 — 2026-06-14)

### Round 1: Gap Authenticity Challenge
**Challenge**: Are C132-C138 really gaps? Stock Explorer already has C43 (Health Score), C37 (Key Takeaways), C02 (Notifications planned). Don't C135 (Health Score Narrative) and C138 (Smart Notifications) duplicate existing planned work?

**Response**:
- C135 (Health Score Narrative) is a refinement of C43 — instead of just showing a score, it adds a plain-language narrative layer. This is a P1 gap because Robinhood and Spiking both have narrative health scores, and our C43 currently only shows the score without explanation. Valid gap.
- C138 (Smart Notifications with Explanations) vs C02 (Notifications): C02 is the notification delivery mechanism (bell icon, unseen count). C138 is the content quality — notifications that explain WHY something happened. These are complementary, not duplicative. Valid gap.
- C134 (AI-Generated Change Explanations) is genuinely new — no existing feature explains WHY a metric changed. This is a unique differentiator. Valid P1 gap.
- C132 (Risk Simplification 1-5 Scale) — our current risk display uses color-coded cards but no simple scale. Valid P2 gap.
- C133, C136, C137 are P2 nice-to-haves. Acceptable but not urgent.

**Verdict**: 5 of 7 gaps confirmed authentic. C133 and C136 are lower priority but valid.

### Round 2: Priority Challenge
**Challenge**: Sprint 16 plans C14 + C45 + C28 + C41 (from Round 33). The review adds 4 new P1 items (C132, C134, C135, C138). Should any of these displace the planned Sprint 16 work?

**Response**:
- C135 (Health Score Narrative) should be merged with C14 (Health Score) implementation. They're the same feature at different maturity levels. C14 should include narrative from the start.
- C134 (Change Explanations) is architecturally dependent on the LLM layer (D5). Cannot be done in Sprint 16 without first building the abstraction. Defer to Sprint 17.
- C132 (Risk Simplification) is a quick win (6-10h) that could fit in Sprint 16a alongside C14.
- C138 (Smart Notifications) depends on C02 (Notifications) which is already planned for Sprint 16b (conditional). Merge the explanation feature into C02.

**Revised Sprint 16 Plan**:
- **Sprint 16a**: C14 Health Score with Narrative (= C135 merged) + C132 Risk Simplification + C45 Valuation Band + C28 Spike
- **Sprint 16b**: C02 Notifications with Explanations (= C138 merged) + C41 Phase A, OR C28 Full

### Round 3: Goal Alignment Challenge
**Challenge**: The product vision says "Historian, not a stock picker." Do C134 (Change Explanations) and C138 (Smart Notifications) align with this? Change explanations could be seen as predictive ("this stock moved because..."), which borders on investment advice.

**Response**:
- C134 (Change Explanations) can be framed as historical: "過去這週營收成長了15%，主要是因為..." (explaining what already happened). This is historian-aligned. The key is using past-tense, factual language — not predicting future changes.
- C138 (Smart Notifications) should also be historian-framed:_notify users of past events with context, not forward-looking alerts. "台積電昨天公布了財報，重點是..." not "台積電即將大漲".
- Both features need the historian tone QA gate (already a key rule). This is manageable risk.

**Final Verdict**: ✅ **CONFIRMED** with 4 revisions:
1. C135 merged into C14 (Health Score with Narrative from day 1)
2. C132 (Risk Simplification) added to Sprint 16a
3. C138 merged into C02 (Notifications with Explanations)
4. C134 deferred to Sprint 17 (requires LLM abstraction layer first)