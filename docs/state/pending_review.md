# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-16
> **Source**: Discussion Round 10 — Challenger required revisions

## Open Questions for Daniel

### 1. C34 vs C46 Priority for Sprint 5
- **Context**: Sprint 5 can fit C34 (Company Story Timeline, 16-24h) + one of C46 (Moat Analysis, 20-28h) or C47 Phase 1 (5 lessons, 12h). Not all three.
- **C34 (Story Timeline)**: The purest expression of "historian" positioning. Round 7 identified it as "#1 thing competitors DON'T have." Depends on C38 (Sprint 3) data structures.
- **C46 (Moat Analysis)**: No TW competitor has moat analysis. Morningstar's moat rating is iconic but US-only. Manual curation for top 20 stocks.
- **C47 Phase 1 (Education Academy)**: 5 pilot lessons. Transforms product from tool to platform. Long-term differentiator.
- **Recommendation**: C34 is the vision P1 — it should be the Sprint 5 primary feature. Choose C46 or C47 Phase 1 as secondary based on whether you want depth (moat) or breadth (education).
- **Status**: ⏳ Pending Daniel

### 2. C47 Education Academy Phase 1 Scope
- **Context**: C47 is 28-41h total. Challenger recommends splitting into phases.
- **Option A**: Phase 1 = 5 pilot lessons (12h), Phase 2 = remaining lessons post-plan
- **Option B**: Phase 1 = 10 lessons (20h), Phase 2 = remaining lessons post-plan
- **Recommendation**: Option A (5 lessons) — validate quality before scaling
- **Status**: ⏳ Pending Daniel

### 3. Business Card Page Information Architecture
- **Context**: The business card page now has 13 sections after Sprint 2. Adding C44 as a 14th requires progressive disclosure.
- **Proposal**: C37 + C43 are "above the fold" ten-second answer. C44 is collapsible above the fold. C46 and C36 are in tabs. Everything else below the fold.
- **Status**: ⏳ Pending Daniel — approve the "above the fold" definition?

### 4. Dark/Light Theme Implementation (D-126)
- **Context**: Design review identified missing dark/light theme implementation; settings page lacks theme toggle.
- **Proposal**: Add theme preference in settings with CSS variables for colors, improving accessibility and user comfort.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

### 5. _infocard() Component for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards that combine icons, mini-charts, and text.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component for visual-first metric presentation.
- **Estimated Effort**: 6-9h
- **Status**: ⏳ Pending Daniel

### 6. _calculator_card() Component for Interactive Financial Tools (D-128)
- **Context**: Missing _calculator_card() component for interactive financial modeling tools.
- **Proposal**: Create _calculator_card() component with input fields and real-time output for simple financial modeling.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

### 7. _ai_explanation_card() Component for AI Explanations (D-129)
- **Context**: Missing _ai_explanation_card() component for AI-driven move explanations with visual cues.
- **Proposal**: Create _ai_explanation_card() component with visual indicator (e.g., robot icon) and AI-generated explanation.
- **Estimated Effort**: 5-8h
- **Status**: ⏳ Pending Daniel

## Resolved This Cycle (Round 10)

| Item | Decision |
|------|----------|
| C42 priority | Confirmed P1 enabler for Sprint 4 (not P1 vision — C34 is vision P1) |
| C44 scope | MVP: 3 risk dimensions, top 20 stocks, progressive disclosure |
| C44 tone risk | Elevated to HIGH — tone review checkpoint required |
| C34 scheduling | Explicitly scheduled for Sprint 5 (with C46 or C47 P1) |
| C47 scope | Split into Phase 1 (5 lessons, 12h) + Phase 2 (post-plan) |
| Sprint 3 contingency | If C44-MVP >14h, reduce to 2 risk dimensions |
| R3 verification | Must verify before Sprint 4 (C42 dependency) |

## Previous Pending Items (Still Open)

### C42 Stock Screener vs C46 Moat Analysis Priority
- **Context**: If Sprint 4 slips, which gets cut — screener or moat?
- **C42 (Screener)**: P1 enabler, transforms product from lookup to discovery, 19-24h
- **C46 (Moat)**: P2, manual curation bottleneck, 20-28h
- **Recommendation**: Cut C46 if needed; C42 is strategically more important
- **Status**: ⏳ Pending Daniel

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*