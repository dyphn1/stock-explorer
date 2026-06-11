# Review Report
## Theme: Review (🔍) — Round 12
## Date: 2026-06-18

## Feature Gaps (New from this review cycle)
- **C55: Investment Diary** — Personal Reflection Journal (P2, 10-14h)
  Source: 元大證券 "Investment Diary", Tastytrade "Trade Journal"
  Alignment: Story first + Historian positioning + Point-to-point knowledge construction
- **C56: Explain This Metric** — Interactive Financial Concept Explainer (P1, 12-16h)
  Source: Magnify.money "AI Visual Explanations", 永豐金證券 "Financial Statement Visualizer", Robinhood "Metric Tooltips"
  Alignment: Point-to-point knowledge construction + Ten-second test + Story first
- **C57: Compare Concepts** — Financial Concept Comparison Tool (P2, 10-14h)
  Source: Magnify.money "Compare Concepts"
  Alignment: Point-to-point knowledge construction + Benchmark-oriented analysis
- **C58: Beginner Onboarding Flow** — Guided First Experience (P1, 14-20h)
  Source: 玉山證券 "Beginner Village", Robinhood "First Stock", eToro "Virtual Portfolio"
  Alignment: Point-to-point knowledge construction + Ten-second test + beginner-friendly
- **C59: AI Q&A Chatbot** — Natural Language Stock Questions (P2, 16-24h)
  Source: 元大證券 "Investment Chatbot", Finimize "Ask Finimize", Magnify.money "AI Visual Explanations"
  Alignment: Story first + Point-to-point knowledge construction
- **C60: Concept Mastery Badges** — Gamified Learning Achievement System (P2, 8-12h)
  Source: Robinhood "Learn → Earn", Khan Academy badges, Finimize completion certificates
  Alignment: Point-to-point knowledge construction + Ten-second test + engagement
- **C61: Sector Rotation Visualizer** — Market Momentum Map (P2, 10-14h)
  Source: 永豐金證券 "Sector Rotation Visualizer"
  Alignment: Benchmark-oriented analysis + Adaptive
- **C62: Pre-Investment Checklist** — Educational Scaffolding Tool (P2, 8-12h)
  Source: 永豐金證券 "Investment Checklist"
  Alignment: Story first + Historian positioning

## Design Improvement Suggestions
**Resolved in Round 12 (8 items):**
- D-016: C37 now uses `_summary_card()` with orange `#F39C12` border and `#FFF8F0` background
- D-017: C37 bullet cap changed from `[:5]` to `[:3]` in `analogy_engine.py:423`
- D-018: C39 moved from after 關鍵數字三連卡 to directly after C37
- D-019: Delta cap `[:2]` added at `analogy_engine.py:508`
- D-020: Directional color coding with `#27AE60`/`#E74C3C` spans added to delta text
- D-022: C43 now 3rd content section (after C37 and C39)
- D-023: Valuation window extended to 5 years (1825 days) with graceful fallback
- D-021: Partially fixed — `get_health_dimension_explanation()` added with generic 3-tier text, dimension cards show explanations

**New Issues Found (2 items):**
- D-024 (P1): `_info_card` uses wrong background `#FFF8F0` (warm orange) instead of `#F8F9FA` (neutral light gray)
- D-025 (P2): C39 has no empty state message when no deltas exceed 10% threshold

**Design Grade: A** (upgraded from A-)
Rationale: All P1 issues from Round 11 resolved except D-021 partial fix, page flow now correct, visual hierarchy significantly improved.

**Design Feasibility Assessment:**
- C44 (Risk Analysis): HIGH feasibility — needs new `_warning_card()` component, recommend expandable section
- C41 (Read Next): HIGH feasibility — reuse `_summary_card()`, place at bottom before disclaimer
- C38 (Compare Stories): MEDIUM feasibility — two-column layout challenges PPT style and mobile responsiveness, recommend starting with single "商業模式" dimension

## Architecture Debt Items
**Resolved in Round 12 (4 items):**
- D1: Duplicate financial metric calculation — RESOLVED by R1 (financial_metrics.py extraction)
- D2: `_find_financial_value` semantic duplication — RESOLVED by R1
- D17: EPS extraction logic triplicated across 3 files — RESOLVED by R1
- D20: `business_card.py` valuation interpretation duplicates `chart.py` logic — RESOLVED by D-020 fix

**Still Open (Prioritized):**
- **High Severity:**
  - D5: No LLM integration layer (2-3h)
  - D16: `analogy_engine.py` god module (850 lines, 6 responsibilities) — Split into focused modules
- **Medium Severity:** 23 items including D3-D4, D6-D15, D18-D19, D21-D26

**New Architecture Debt Identified (6 items):**
- D22: `financial_metrics.py` is a leaf service with no consumers in service layer (Low)
- D23: Tone guidelines for market-level features (Medium)
- D24/D27: `business_card.py` approaching architectural limit (Medium) — Extract to sub-directory
- D25: Market-level data flow is architecturally distinct from single-stock flow (Medium)
- D26: `story_composer.py` will import from multiple unstable services (Medium) — Blocker for C48

## Technical Debt Priorities
**High Severity (Do Next):**
1. D16: Split `analogy_engine.py` god module (2-3h) — **CRITICAL PATH ITEM**
2. D5: Add LLM integration layer abstraction (2-3h)

**Medium Severity (Sprint 3-4):**
- D3: Inline HTML duplication across pages (3-4h)
- D4: Service layer `__init__.py` wildcard imports (0.5h)
- D6: Hardcoded data in Python modules (3-4h)
- D7-D8: N+1 API call patterns (2-3h each)
- D9-D10: YAML reads on every operation (1-2h each)
- D11: No error boundary standardization (2-3h)
- D12: `_router_base.py` mixes routing and UI (1h)
- D13: No test infrastructure (3-4h initial setup)
- D14: Sidebar architecture not extracted (1-2h)
- D15: FinMind client not async-compatible (1-2h)
- D17-D18-D19-D21: Resolved or in progress
- D23: Tone guidelines for market-level features (1h content task)
- D24/D27: Extract `business_card.py` to sub-directory (2-3h)
- D25: Create `market_data.py` service (part of C51)
- D26: Blocker — complete D16 before C48

## Estimated Effort Summary
**Architecture Debt Total Effort (Remaining): 28.5 - 41.5 hours**
- High priority: 4-6h (D16 + D5)
- Medium priority: 24.5-35.5h

**Design Improvements Total Effort (Remaining): 91.5 - 130.5 hours**
- P1 issues: D-003, D-004, D-005, D-006, D-007, D-021 (partial), D-024 = 22-30h
- P2 issues: D-008, D-009, D-010, D-011, D-012, D-013, D-015, D-025 = 11.5-16.5h
- Sprint 3 design fixes (D-016 through D-023): ALREADY DONE
- New feature design work: C44 (4-6h), C41 (3-4h), C38 (6-8h)

**New Feature Development Effort:**
- C44 Risk Analysis MVP: 12-14h
- C41 Read Next Recommendations: 6-8h
- C38 Compare Stories Phase 1: 10-12h
- D16 Split analogy_engine.py: 2-3h
- D-025 Expandable card component: 2-3h
- Sprint 3 Remaining Total: 32-40h

**Sprint 4 Sequence (Revised):**
1. R3 (Batch API minimal, 1-2h) — rate-limit-safe fetching for C51
2. D24 (business_card.py sub-directory extraction, 2-3h) — NEW, before C48
3. C51 (Sector Heatmap, 12-16h) — with minimal R3 prerequisite
4. C48 (Company Story Card replaces C37, 10-14h) — hero card pattern
5. C53-1 (Social Sharing URL, 2-3h) — quick win

## Key Cross-Cutting Insights
1. **D16 is the critical path item** — Unblocks C44 (Risk Analysis), C38 (Compare Stories), and C48 (Company Story Card)
2. **Education-first competitors are accelerating** — TW brokers (富邦e富, 元大證券, 永豐金證券, 玉山證券) now have AI features, structured learning, and onboarding flows
3. **The "ten-second test" needs reinforcement** — Multiple competitors have interactive metric explanations (C56 type feature) validating its importance
4. **Beginner retention requires scaffolding** — Features like C55 (Investment Diary), C58 (Onboarding Flow), C62 (Pre-Investment Checklist) address the drop-off risk
5. **Architecture is healthy post-R1** — `financial_metrics.py` extraction successful, L0: 55/55, L1: 18/18, business_card.py actually decreased in size (479→447 lines)