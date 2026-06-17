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

## Resolved This Cycle (Sprint 25 Day 3)

|| Item | Decision |
|------|--------|----------|
|| C206 Recurring Investment Education | ✅ Implemented single DCA lesson with hypothetical data only (commit 1a0c426) |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
