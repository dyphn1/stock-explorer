# Handoff – Discussion Round 40 (2026-06-14)

## Summary
- **Topic**: Discussion (💡) — Sprint 20 Roadmap: AI Screener, Learn First Gate, Beginner Mode
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger
- **Sprint Status**: Sprint 19 🔧 IN PROGRESS (5/6 done, C152 spike deferred) → Sprint 20 📋 PLANNED

---

## Key Discovery: 4 Features Already Complete

The Developer's analysis revealed that 4 of 8 candidate features are already implemented:

| Feature | Status | Effort Needed |
|---------|--------|---------------|
| C37 Key Takeaways Summary Card | ✅ DONE | 0h — `key_takeaways.py` + `_render_takeaways()` |
| C36 Visual Revenue Tree | ✅ DONE | 0h — `revenue_tree.py` standalone page |
| C39 What Changed Delta Card | ✅ DONE | 0h — `delta_engine.py` + `_render_deltas()` |
| C41 Read Next Recommendations | ✅ DONE | 0h — `_render_read_next()` |

---

## Idea Proposals

| Idea ID | Description | Proposed By | Status |
|---------|-------------|-------------|--------|
| DIR-A | Narrative Intelligence Layer (C167 + C152) | Architect | C167 → Sprint 20, C152 → Sprint 21 (with swap condition) |
| DIR-B | Progressive Disclosure System (C163 + C40) | Architect | Both → Sprint 20 (revised order: C163 before C40) |
| DIR-C | Visual Discovery & Education (enhancements) | Architect | Deferred to Sprint 21 |

---

## Decisions Made

### Sprint 20 Final Plan (Post-Challenge)

| Order | Feature | Estimate | Running Total |
|-------|---------|----------|---------------|
| 1 | C167: AI Screener Explanations | 12-16h | 12-16h |
| 2 | C163: Learn First Gate | 10-14h | 22-30h |
| 3 | C40: Beginner/Expert Mode Toggle | 8-12h | 30-42h |
| — | C152: Multi-Factor Event Narratives | 14-18h | Deferred to Sprint 21 (see swap condition) |

### 7 Challenger Conditions (Binding)

1. **Priority order: C167 → C163 → C40** (revised from preliminary C167 → C40 → C163)
2. **Shared "beginner experience spec"** must be written as part of C163 design phase, before C40 implementation
3. **C152 swap condition**: If Sprint 19 C152 spike produces high-quality artifacts, C152 replaces C40 in Sprint 20
4. **Content creation plan**: PM writes C167 narrative templates during Sprint 19 remaining time; Designer writes C163 educational cards before Sprint 20 Day 3; placeholder fallback if not ready
5. **Design system compliance**: Must use existing components (_info_card, _summary_card, _白话_card); new components documented
6. **C167 historian framing**: Screener explanations use historian tone with disclaimer "篩選結果僅供學習參考，不構成投資建議"
7. **Sprint 20 retrospective** must evaluate competitive positioning against StockStory and Stockopedia AI

### Key Architectural Decisions

- **C167 leverages ExplanationProvider protocol**: New `ScreenerExplanationProvider` implements the same protocol used by `delta_explanation_provider.py`
- **C163 builds on C103 first visit guide**: Extends 2-card primer to multi-step gate with router integration
- **C40 evolves C105 simple mode toggle**: Renames to "新手/專家模式" with per-section complexity variants
- **All features use existing infrastructure**: compose-and-enrich pipeline, YAML-backed services, _router_base.py card components

### Competitor Intelligence (Round 8-9)

- **StockStory** (HIGH threat): AI-generated company narratives + TW coverage → C152 is the direct counter
- **Stockopedia AI** (HIGH threat): AI Explain + TW Market Education Hub → C167 partial counter
- **財報狗**: Screener is #1 feature but lacks narratives → C167 differentiates
- **No TW competitor** combines narrative + plain-language + visual-first → "historian" positioning is genuine white space

---

## Action Items

| Item ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| R40-DISC1 | Write C167 narrative templates (15-20 templates for screener outcomes) | PM | 🔴 Before Sprint 20 Day 1 |
| R40-DISC2 | Write C163 educational cards (3-5 onboarding cards) | Designer | 🔴 Before Sprint 20 Day 3 |
| R40-DISC3 | Write shared "beginner experience spec" | PM + Designer | 🔴 During C163 design phase |
| R40-DISC4 | Evaluate C152 spike artifacts for swap condition | PM + Architect | 🔴 Sprint 19 close |
| R40-DEV1 | Implement C167 AI Screener Explanations (first priority) | Developer | 🔴 Sprint 20 |
| R40-DEV2 | Implement C163 Learn First Gate (second priority) | Developer | 🔴 Sprint 20 |
| R40-DEV3 | Implement C40 Beginner/Expert Mode Toggle (third priority) | Developer | 🟡 Sprint 20 |
| R40-QA1 | Run regression suite before Sprint 20 development | QA | 🔴 Day 1 |

---

## Feature Pipeline (Updated)

| Sprint | Features | Effort | Status |
|--------|----------|--------|--------|
| Sprint 19 | C147+C140+D-113+D-114+C152 spike | 30-44h | 🔧 IN PROGRESS (5/6 done) |
| Sprint 20 | C167+C163+C40 (+ C152 swap condition) | 30-42h | 📋 Planned |
| Sprint 21 | C152 (if not swapped) + enhancements | TBD | 🔮 Future |

---

## Next Cycle
🔧 Development Round 41: Complete remaining Sprint 19 item (C152 spike evaluation), then transition to Sprint 20 development starting with C167.
