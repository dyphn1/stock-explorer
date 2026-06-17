# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-17
> **Source**: Round 52 Sprint 24 Execution

## Open Questions for Daniel

### Sprint 24 Decisions — NEED CONFIRMATION

#### 1. C206 Recurring Investment Education — Scope Definition
- **Context**: Listed as Week 4 stretch goal in Sprint 24
- **No architecture doc exists yet** — needs design before implementation
- **Question**: What should C206 cover? (e.g., DCA simulation, compound interest visualization, investment scenario comparison)
- **Status**: ⏳ Pending Daniel

### Previously Open Items (Still Pending)

#### 2. C203 Supply Chain Visual Map — FinMind API Limitation
- **Context**: FinMind's supply chain API is paid-only
- **Proposal**: Redefined as "Company Ecosystem Cards" v1 — card-based layout for top 15-20 stocks using existing `group_structures.yaml` + manually curated data. No network graph in v1.
- **Revised estimate**: 12-15h (down from 36-50h)
- **Status**: ⏳ Pending Daniel — approve "ecosystem cards" approach?

#### 3. Dark/Light Theme Implementation (D-126)
- **Context**: Design review identified missing dark/light theme implementation.
- **Proposal**: Add theme preference in settings with CSS variables.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

#### 4. Missing Component: _infocard() for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component.
- **Estimated Effort**: 6-9h
- **Status**: ⏳ Pending Daniel

## Resolved This Cycle (Round 52)

| Item | Decision |
|------|----------|
| C201 implementation | ✅ Implemented and committed (`ad5b46c`) |
| Design system color compliance | ✅ Fixed 30+ violations across 4 files (`2fc60d3`) |
| All tests green | ✅ 662/662 pass |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
