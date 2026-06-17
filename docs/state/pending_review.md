# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-17
> **Source**: Sprint 26 Planning (Round 52)

## Open Questions for Daniel — ACTIVE (Need Response)

### Sprint 26 Decisions — NEED CONFIRMATION BY WEEK 1 DAY 1

#### 1. C203 Company Ecosystem Cards v1 — Scope Approval
- **Context**: Redefined from "Supply Chain Visual Map" (36-50h, paid API) to "Company Ecosystem Cards" (12-14h, existing data)
- **Proposal**: Card-based layout for 5-8 parent companies. Parent-subsidiary only (no customer-supplier). Reuses `_subsidiary_card()` — no new component needed.
- **Revised estimate**: 12-14h
- **Default if no response**: **DROP from Sprint 26** — no more deferrals (3rd sprint pending)
- **Status**: ⏳ Pending Daniel
- **Deadline**: Sprint 26 Week 1 Day 1

#### 2. Dark/Light Theme Implementation (D-126) — Sprint 27?
- **Context**: Design review identified missing dark/light theme implementation.
- **Proposal**: Add theme preference in settings with CSS variables.
- **Estimated Effort**: 12-18h (revised up from 8-12h)
- **Challenger recommendation**: Defer to Sprint 27 — requires color compliance first
- **Status**: ⏳ Pending Daniel — Sprint 27 candidate
- **Deadline**: Sprint 26 Week 1 Day 1

#### 3. Missing Component: _infocard() for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component.
- **Estimated Effort**: 6-9h
- **Challenger recommendation**: DROP — no consumer identified, no architecture doc, speculative development
- **Status**: ⏳ Pending Daniel — Sprint 27 candidate (if approved)
- **Deadline**: Sprint 26 Week 1 Day 1

## Resolved This Cycle (Sprint 25)

| Item | Decision |
|------|----------|
| C206 Recurring Investment Education | ✅ Implemented single DCA lesson with hypothetical data only (commit 1a0c426) |
| C209 Source Transparency | ✅ Integrated into 3 pages (commit 964e90c) |
| Pre-sprint color fixes | ✅ 8 non-palette colors fixed (commit 9bcbf22) |
| D-073/D-071/D-084 design fixes | ✅ Verified already fixed in Sprint 25 cleanup |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
*Next update: Sprint 26 Week 1 Day 1 (after Daniel decisions)*
