# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Post-Sprint 10 Feature Directions
- **Date**: 2026-06-13
- **Participants**: Product Manager, System Architect, Designer, Developer, Challenger
- **Sprint Status**: Sprint 9 ✅ COMPLETE → Sprint 10 in progress

## Sprint Plans (Summary)
| Sprint | Items | Status |
|--------|-------|--------|
| Sprint 3 | C44, C41, C38, D16, D-025 | ✅ Complete |
| Sprint 4 | R3, C48, C38, C51, C53-1 | ✅ Complete |
| Sprint 5 | D-039/040/041 + D37 + C71 + C74 + C73 | ✅ Complete |
| Sprint 6 | C83 + C85 + C02 + C43 + C45 | ✅ Complete |
| Sprint 7 | C84 + D3 + D6 + D7 + D-044 | ✅ Complete |
| Sprint 8 | D-048 + D6 + D-055 + D-050 + D8/D9/D10 | ✅ Complete |
| Sprint 9 | D-057 + C103 Lite + C101 + C98 | ✅ Complete |
| Sprint 10 | C34 + C105 + M5 remediation + D-061 | 📋 In Progress |
| Sprint 11 | D16 + D24 + R3 + C51 + C53 | 📋 Planned |
| Sprint 12 | C58 + C42 + C56 + C43-verify | 📋 Planned |
| Sprint 13 | C48 + C68 + C84 | 📋 Planned |
| Sprint 14 | C50 + C60 + C52 + C104 + C66 | 📋 Planned |
| Sprint 15+ | D5 (LLM layer) → C86, C100, C59 | 📋 Deferred |

## Key Rules
- Content cap: 100 items max across all features
- Mandatory historian tone QA gate before each content feature ships
- C63 weekly only (start with 12 quarterly, not 52)
- Card-count limit: max 5 cards per page section (Direction A)
- Community features (C64, C67, C89) deprioritized — not feasible in Streamlit
- Content creation must be budgeted at 40% of effort for education features

## 💡 Discussion Section

### Round 19 — Post-Sprint 10 Feature Directions (2026-06-13)

**Topic**: What should we build after Sprint 10?

**Challenger Verdict**: ❌ REJECTED → ✅ CONFIRMED after revision (see below)

**Key Revisions from Challenge**:
1. Moved C58 (Beginner Onboarding) from Sprint 13 → Sprint 12 (retention-critical, gates all other features)
2. Added C43 (Snowflake verification) to Sprint 12 (already built, needs design system alignment check)
3. Clarified C44/C45 already built — removed from future backlog
4. Reduced Sprint 12 from 4 features → 3 features + C43 verification
5. Restructured Sprint 13 from 4 features → 3 features with explicit content creation budget
6. Added R3 fallback plan: C42 degrades to top-50 stocks sequential if batch API fails
7. Established priority resolution: product vision alignment > user retention > technical risk

**Team Final Decision — 3 Directions:**

### Direction A: Discovery & Screening (Sprint 11-12)
- **C42 Stock Screener** (P1, 18-26h) — #1 competitive gap. MVP: top 200 stocks + 5 presets
- **C51 Sector Heatmap** (P2, 12-16h) — Visual market overview, creates market_data.py
- **C49 Daily Market Pulse** (P2, 12-16h) — Deferred to Sprint 13+
- **Feasibility**: 🟡 Medium (conditional on R3). R3 fallback: top-50 sequential mode

### Direction B: Deep Education (Sprint 12-13) — HIGHEST UX PRIORITY
- **C58 Beginner Onboarding** (P1, 16-22h) — Sprint 12. 5-step guided tour. Skip option always visible
- **C56 Explain This Metric** (P1, 10-14h) — Sprint 12. Interactive tooltip system for all metrics
- **C48 Company Story Card** (P2, 10-14h) — Sprint 13. Hero card at top of business page
- **C68 Concept Storytelling** (P1, 10-14h) — Sprint 13. Narrative-based concept explanations
- **Feasibility**: 🟡 Medium-High. Content creation is 40% of effort

### Direction C: Smart Narrative (Sprint 13+, deferred)
- **C98 Event Interpretation** (P1, 14-18h) — Template-first, leverages M5 remediation
- **C86 AI Narrative Agent** (P2, 24-34h) — Deferred to Sprint 15+ (needs D5 LLM layer)
- **C100 Natural Language Screener** (P1, 22-30h) — Deferred to Sprint 15+ (needs C42 + D5)
- **Feasibility**: 🟡 Medium (template) / 🔴 Low (AI-powered)

### Architecture Debt Resolution (Sprint 11 priority order):
1. **D16**: Split analogy_engine.py (850 lines → 4 modules) — 2-3h
2. **D24**: Extract business_card.py to sub-directory — 2-3h
3. **R3**: Batch API calls utility — 1-2h (with fallback plan)

### Design System Updates (needed for Sprint 12+):
- 4 new components: Hero Story Card, Risk Card, Metric Explanation Expander, Quiz Card
- 1 new color: Purple `#9B59B6` for educational interactive elements
- Text limit adjustment: 200 chars static, 400 chars expandable
- Mini chart label typography: 0.75rem, #7F8C8D

### Priority Resolution Framework (established this round):
When roles disagree on priorities, decide by:
1. **Product vision alignment** — Does it serve "historian, not stock picker"?
2. **User retention impact** — Does it reduce bounce rate or increase return visits?
3. **Technical risk** — Can it be built with current architecture?

## Decisions Made
1. **C58 Onboarding moved to Sprint 12** — retention-critical, gates all other features
2. **C43 verified as already built** — Sprint 12 includes design alignment check, not new build
3. **C44/C45 confirmed as already built** — removed from future backlog
4. **Sprint 13 reduced to 3 features** — explicit 40% content creation budget added
5. **R3 fallback defined** — C42 degrades to top-50 sequential if batch API fails
6. **Community features (C64, C67, C89) deprioritized** — not feasible in Streamlit, revisit for v2
7. **D5 (LLM layer) scheduled for Sprint 15** — unblocks AI features (C86, C100, C59)
8. **Content creation budget established** — 40% of effort for education features across all sprints

## Action Items
| Item | Description | Owner | Due |
|------|-------------|-------|-----|
| D16 | Split analogy_engine.py into 4 modules | Developer | Sprint 11 |
| D24 | Extract business_card.py to sub-directory | Developer | Sprint 11 |
| R3 | Create batch_fetch_prices utility | Developer | Sprint 11 |
| C53 | Social sharing (HTML-to-image export) | Developer | Sprint 11 |
| C51 | Sector Heatmap with market_data.py | Developer | Sprint 11 |
| C58 | Beginner Onboarding Flow | Developer | Sprint 12 |
| C42 | Stock Screener (top-200 MVP) | Developer | Sprint 12 |
| C56 | Explain This Metric (tooltip system) | Developer | Sprint 12 |
| C43-verify | Snowflake design alignment check | Designer | Sprint 12 |
| C48 | Company Story Card (hero element) | Developer | Sprint 13 |
| C68 | Financial Concept Storytelling | Developer | Sprint 13 |
| C84 | Market Event Case Study | Developer | Sprint 13 |
| Design System | 4 new components + color + typography | Designer | Sprint 12 |
| D5 | LLM abstraction layer | Architect | Sprint 15 |

## Next Cycle
🔍 Review Round 22 → Sprint 10 (C34 + C105 + M5 remediation + D-061)
