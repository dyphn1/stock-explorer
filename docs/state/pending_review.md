# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-17
> **Source**: Sprint 25 Day 1 Complete

## Open Questions for Daniel — ACTIVE (Need Response)

### Sprint 25 Decisions — NEED CONFIRMATION

#### 1. C203 Company Ecosystem Cards v1 — Scope Approval
- **Context**: Redefined from "Supply Chain Visual Map" (36-50h, paid API) to "Company Ecosystem Cards" (10-12h, existing data)
- **Proposal**: Card-based layout for 8 companies (existing 5 + 3 new). Parent-subsidiary + 2-3 well-known customer-supplier pairs. Reuses `_subsidiary_card()` — no new component needed.
- **Revised estimate**: 10-12h (down from 36-50h)
- **Default if no response**: Defer C203 to Sprint 26
- **Status**: ⏳ Pending Daniel

#### 2. C206 Recurring Investment Education — Scope Definition
- **Context**: Listed as stretch goal since Sprint 24. No architecture doc exists.
- **Proposal**: Single DCA lesson in existing academy. Hypothetical data only, NO calculator, NO real stock examples. Uses `_lesson_card()` + `_progress_dots()`.
- **Revised estimate**: 6-8h for single lesson
- **Default if no response**: Single DCA lesson, hypothetical only
- **Status**: ⏳ Pending Daniel (defaulting to single lesson)

### Previously Open Items (Still Pending)

#### 3. Dark/Light Theme Implementation (D-126)
- **Context**: Design review identified missing dark/light theme implementation.
- **Proposal**: Add theme preference in settings with CSS variables.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel — Sprint 26+ candidate

#### 4. Missing Component: _infocard() for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component.
- **Estimated Effort**: 6-9h
- **Status**: ⏳ Pending Daniel — Sprint 26+ candidate

## Resolved This Cycle (Sprint 25 Day 1)

| Item | Decision |
|------|----------|
| C209 `_source_section()` component | ✅ Created (commit 8ed9a97) |
| Pre-sprint color fixes | ✅ Applied (commit 9bcbf22) |
| `validate_debate_text()` rename | ✅ Renamed to `contains_banned_words()` |
| Timeline labels i18n | ✅ Moved to `t()` calls |
| C209 redesign | ✅ Option A: Collapsible source section |
| Pre-sprint fixes | ✅ All applied |
| C203 scope cap | ✅ 8 companies max (not 15-20) |
| C206 scope | ✅ Single lesson, hypothetical only (default if no Daniel response) |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
